"""Health check SOMENTE-LEITURA dos slots LLM (Task 6.1).

Sonda os health endpoints HTTP (GET /health) em localhost com timeout curto
e lê /proc/<pid>/cmdline para extrair a flag -ngl de cada llama-server.

INVARIANTE DE SEGURANÇA (R4 / nao_fazer):
  - NUNCA inicia/para/mata processos.
  - NUNCA roda start-stack.sh em modo escrita.
  - Apenas leitura: HTTP GET + leitura de /proc/<pid>/cmdline.

Retorna um mapa {slot: {online, device_cpu_gpu, ngl}} resolvendo a divergência
9086/9090/9092 por medição real (não por fé).
"""

from __future__ import annotations

import os
import urllib.request

# Slots canônicos (porta -> papel). Fonte: device-map.md + start-stack.sh.
SLOTS = {
    "8083": "orquestrador",
    "9084": "talamus-cortex",
    "9086": "reflexo",
    "9088": "contrato-plano",
    "9090": "refutacao",
    "9092": "relay",
    "9093": "smol-360m",
    "9094": "embedder-cpu",
    "9095": "moe-2.7b",
    "9097": "embedder-gpu",
}

# Portas que NÃO são llama-server (binário nativo, /health retorna 404).
# Mantidas fora da sonda para não gerar falso-negativo.
NON_LLAMA_PORTS = {"8097", "9091"}

HEALTH_TIMEOUT = 2.0  # segundos (timeout curto)


def _http_health(port: str) -> bool:
    """GET /health com timeout curto. True se HTTP 200, False caso contrário."""
    url = f"http://127.0.0.1:{port}/health"
    try:
        with urllib.request.urlopen(url, timeout=HEALTH_TIMEOUT) as resp:
            return resp.status == 200
    except Exception:
        return False


def _pid_for_port(port: str) -> int | None:
    """Resolve o PID do processo escutando na porta via /proc/net/tcp (sem lsof)."""
    # Converte porta decimal para hex (4 dígitos) para casar com /proc/net/tcp.
    port_hex = f"{int(port):04X}"
    try:
        with open("/proc/net/tcp", "r") as f:
            lines = f.readlines()
    except OSError:
        return None

    for line in lines[1:]:  # pula header
        parts = line.split()
        if len(parts) < 10:
            continue
        local = parts[1]  # formato: IP:PORTA (hex)
        if ":" not in local:
            continue
        local_port = local.split(":")[1]
        if local_port == port_hex:
            # state == 0A (LISTEN)
            state = parts[3]
            if state == "0A":
                inode = parts[9]
                return _pid_for_inode(inode)
    return None


def _pid_for_inode(inode: str) -> int | None:
    """Varre /proc/*/fd para achar o PID dono do socket inode."""
    for pid_dir in os.listdir("/proc"):
        if not pid_dir.isdigit():
            continue
        fd_dir = f"/proc/{pid_dir}/fd"
        try:
            fds = os.listdir(fd_dir)
        except OSError:
            continue
        for fd in fds:
            try:
                link = os.readlink(f"{fd_dir}/{fd}")
            except OSError:
                continue
            if f"socket:[{inode}]" in link:
                return int(pid_dir)
    return None


def _read_ngl(pid: int) -> int | None:
    """Lê /proc/<pid>/cmdline e extrai o valor de -ngl. None se não encontrado."""
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            raw = f.read()
    except OSError:
        return None
    args = raw.split(b"\x00")
    for i, arg in enumerate(args):
        if arg == b"-ngl" and i + 1 < len(args):
            try:
                return int(args[i + 1].decode())
            except (ValueError, UnicodeDecodeError):
                return None
    return None


def _device_from_ngl(ngl: int | None) -> str | None:
    """Classifica device a partir do ngl medido.

    ngl == 0  -> CPU puro
    ngl > 0   -> GPU (Vulkan) — ngl 999 = tudo na GPU; ngl parcial = híbrido.
    ngl None  -> desconhecido.
    """
    if ngl is None:
        return None
    if ngl == 0:
        return "cpu"
    if ngl == 999:
        return "gpu"
    return "hybrid"


def check_health() -> dict:
    """Sonda todos os slots e retorna {slot: {online, device_cpu_gpu, ngl}}.

    SOMENTE-LEITURA. Não toca em nenhum processo.
    """
    result: dict = {}
    for port, papel in SLOTS.items():
        online = _http_health(port)
        pid = _pid_for_port(port)
        ngl = _read_ngl(pid) if pid is not None else None
        result[port] = {
            "online": online,
            "device_cpu_gpu": _device_from_ngl(ngl),
            "ngl": ngl,
        }
    return result


def is_healthy(health: dict | None) -> bool:
    """Health é válido e não-ambíguo?

    Válido: não-None, não-vazio, e os slots de divergência (9086/9090/9092)
    reportam device consistente (todos CPU, sem ambiguidade).
    """
    if not health:
        return False
    # Slots que historicamente divergem (device-map.md).
    divergence_ports = ("9086", "9090", "9092")
    devices = set()
    for port in divergence_ports:
        slot = health.get(port)
        if slot is None or not slot.get("online"):
            return False
        dev = slot.get("device_cpu_gpu")
        if dev is None:
            return False
        devices.add(dev)
    # Ambíguo se os três slots reportam devices diferentes.
    return len(devices) == 1