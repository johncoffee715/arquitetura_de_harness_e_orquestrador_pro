#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stack-health-check.py — Hook session.start (R19): AUTO-REVIVE da stack LLM local.

Problema verificado: reiniciar o OpenCode mata o grupo de processos dos
llama-server -> 0/9 portas down no boot. Este hook, a cada session.start,
verifica a saúde dos 9 slots da stack local e, se QUALQUER porta estiver
down, relança `start-stack.sh` DESANEXADO (R19 — setsid nohup), sem esperar
o load completo (1-3 min). Idempotente: se start-stack.sh já roda (pgrep),
não lança segundo.

Protocolo hook OpenCode (session.start):
    stdin:  JSON {"session_id": ..., "directory": ..., "prompt": ...}
    stdout: JSON {"context": {"__STACK_HEALTH__": {...}}} — injeção de contexto.
    Fail-open: qualquer exceção -> log + "{}" (nunca bloqueia session.start).

Uso:
    python3 hooks/stack-health-check.py            (modo hook — lê stdin e emite JSON)
    python3 hooks/stack-health-check.py --test     (smoke rápido, sem rede)
"""

import json
import logging
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

# R21: WARM slots não são vigiados pelo guard (só ESSENTIAL + needles)
ESSENTIAL_PORTS = [8083, 9084]
WARM_PORTS = [9086, 9088, 9090, 9093, 9095]
NEEDLE_PORTS = [8097, 9091]
PORTS = ESSENTIAL_PORTS + WARM_PORTS + NEEDLE_PORTS
START_STACK = "/mnt/dados/Assistente Pessoal/opencode/scripts/start-stack.sh"
LOG_PATH = Path("/tmp/opencode/stack-health.log")
START_LOG = Path("/tmp/opencode/stack-health-start.log")
CURL_TIMEOUT_S = 2
CHECK_TIMEOUT_S = 15

_logger_configured = False


def setup_logger():
    """Logger com path seguro — idempotente entre invocações."""
    global _logger_configured
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    l = logging.getLogger("StackHealth")
    l.setLevel(logging.INFO)
    if not l.handlers:
        h = logging.FileHandler(LOG_PATH)
        h.setFormatter(logging.Formatter('%(asctime)s [STACK-HEALTH] %(message)s'))
        l.addHandler(h)
    _logger_configured = True
    return l


logger = setup_logger()


def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _port_ok(port: int) -> bool:
    """Health check de 1 porta: `curl -sf -m 2 http://127.0.0.1:{port}/health`."""
    try:
        r = subprocess.run(
            ["curl", "-sf", "-m", str(CURL_TIMEOUT_S), f"http://127.0.0.1:{port}/health"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=CURL_TIMEOUT_S + 1,
        )
        return r.returncode == 0
    except Exception:
        return False


def check_ports() -> list:
    """Verifica TODAS as portas em paralelo (ThreadPoolExecutor) — < 15s total."""
    down = []
    with ThreadPoolExecutor(max_workers=len(PORTS)) as pool:
        futures = {pool.submit(_port_ok, p): p for p in PORTS}
        for fut in as_completed(futures, timeout=CHECK_TIMEOUT_S):
            port = futures[fut]
            if not fut.result():
                down.append(port)
    return sorted(down)


def start_stack_running() -> bool:
    """Idempotência (R19): start-stack.sh já em execução -> não relança."""
    try:
        r = subprocess.run(
            ["pgrep", "-f", r"scripts/start-stack\.sh"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
        return r.returncode == 0
    except Exception:
        return False


def revive_stack() -> bool:
    """Relança start-stack.sh DETACHED (R19 — setsid nohup, desanexado).

    Não espera o load (1-3 min). Retorna True se lançou, False se já rodava
    (idempotente) ou se falhou ao lançar.
    """
    if start_stack_running():
        logger.info("action=SKIP motivo=ja_rodando (idempotente)")
        return False
    try:
        START_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(START_LOG, "a", encoding="utf-8") as out:
            subprocess.Popen(
                ["setsid", "nohup", "bash", START_STACK],
                stdout=out,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
            )
        logger.info("action=REVIVED pids_launched_start_stack=%s", START_STACK)
        return True
    except Exception as e:
        logger.error("action=ERROR fase=revive erro=%s", e)
        return False


def read_stdin_payload(argv) -> dict:
    """Lê JSON do stdin (session.start). Nunca quebra com stdin vazio/inválido;
    fallback: argv (flags/JSON literais) ou dict vazio (no-op)."""
    try:
        if not sys.stdin.isatty():
            raw = sys.stdin.read()
            if raw.strip():
                data = json.loads(raw)
                if isinstance(data, dict):
                    return data
    except Exception:
        pass
    joined = " ".join(argv).strip()
    if joined:
        try:
            data = json.loads(joined)
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return {}


def run() -> dict:
    """Executa o ciclo completo; sempre retorna dict de emissão hook."""
    down = check_ports()
    if not down:
        logger.info("action=OK ports_down=[] checked=%d", len(PORTS))
        return {
            "checked": True,
            "ports_down": [],
            "action": "OK",
        }

    logger.info("action=CHECK ports_down=%s checked=%d", down, len(PORTS))
    launched = revive_stack()
    if launched:
        logger.info("action=REVIVED ports_down=%s — start-stack.sh desanexado", down)
    else:
        logger.info("action=REVIVED ports_down=%s — start-stack.sh já em execução", down)
    return {
        "checked": True,
        "ports_down": down,
        "action": "REVIVED",
        "relaunched": launched,
    }


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if "--test" in argv:
        print(json.dumps({"context": {"__STACK_HEALTH__": {"checked": True, "ports_down": [], "action": "OK", "mode": "test"}}}))
        return 0

    read_stdin_payload(argv)  # consome payload — nunca deixa buffer preso
    try:
        result = run()
        emission = {"context": {"__STACK_HEALTH__": result}}
    except Exception as e:  # fail-open absoluto: nunca bloqueia session.start
        logger.error("action=ERROR erro=%s", e)
        print("{}")
        return 0

    print(json.dumps(emission, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())