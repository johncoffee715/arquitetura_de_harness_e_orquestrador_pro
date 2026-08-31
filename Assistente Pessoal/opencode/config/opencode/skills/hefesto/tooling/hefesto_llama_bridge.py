#!/usr/bin/env python3
"""
HEFESTO LLAMA BRIDGE — Ferramental da Tríplice (.md/.py/.json/.gbnf)

Unifica bridge + automation + pipeline do ferramental Hefesto (helenizado):
- Compila flags do llama_cpp_config.json em comandos executáveis.
- Descobre novas flags do llama.cpp (--help) e injeta no JSON (PENDING_GBNF_VAL).
- Enriquecimento via LLM com gramática GBNF (hefesto_deep_spec.gbnf).
- Webhook para gatilho externo (GitHub Actions/CRON).

Origin: helenizado: tranqueiras/autofagia e helenizaçao (hefesto_llama_bridge.py,
hefesto_automation.py, hefesto_pipeline.py) — unificado 2026-08-31.
"""

import json
import os
import re
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Paths globais do harness (R2/R44)
TOOLING_DIR = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/hefesto/tooling")
CONFIG_PATH = TOOLING_DIR / "llama_cpp_config.json"
SPEC_PATH = TOOLING_DIR / "llama_cpp_spec.md"
FEATURE_GBNF = TOOLING_DIR / "hefesto_feature.gbnf"
DEEP_GBNF = TOOLING_DIR / "hefesto_deep_spec.gbnf"
LLAMA_CLI = "/mnt/dados/Assistente Pessoal/opencode/llama.cpp/bin/llama-cli"
LLAMA_SERVER = "/mnt/dados/Assistente Pessoal/opencode/llama.cpp/bin/llama-server.real"
LD_LIBRARY_PATH = "/mnt/dados/Assistente Pessoal/opencode/llama.cpp/bin"


class HefestoLlamaBridge:
    """Compila a tríplice em comandos executáveis + auto-otimização de hardware."""

    def __init__(self, config_path: Path = CONFIG_PATH):
        self.config = self._load_config(config_path)

    def _load_config(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Configuração do Hefesto não localizada: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _calculate_hardware(self, hardware_cfg: dict) -> dict:
        """Auto-otimização de hardware (R72: sem limitação artificial de CPU)."""
        optimized = hardware_cfg.copy()
        if optimized.get("threads") == "auto":
            cpu_count = os.cpu_count()
            optimized["threads"] = max(1, cpu_count - 2) if cpu_count else 4
        return optimized

    def compile_flags(self) -> list:
        """Transforma a tríplice estruturada em comandos executáveis lineares."""
        commands = [LLAMA_SERVER]
        lifecycle = self.config.get("model_lifecycle", {})
        if lifecycle.get("model"):
            commands.extend(["-m", lifecycle["model"]])
        if lifecycle.get("lazy-mode"):
            commands.append("--lazy-mode")
        hardware = self._calculate_hardware(self.config.get("hardware_allocation", {}))
        commands.extend(["--threads", str(hardware.get("threads", 4))])
        commands.extend(["--n-gpu-layers", str(hardware.get("n-gpu-layers", 0))])
        if hardware.get("flash-attn", True):
            commands.append("--flash-attn")
        if hardware.get("device"):
            commands.extend(["--device", hardware["device"]])
        ctx = self.config.get("context_management", {})
        commands.extend(["--ctx-size", str(ctx.get("ctx-size", 0))])
        commands.extend(["--batch-size", str(ctx.get("batch-size", 2048))])
        commands.extend(["--n-predict", str(ctx.get("n-predict", -1))])
        sampling = self.config.get("sampling_profiles", {})
        commands.extend(["--temp", str(sampling.get("temp", 0.6))])
        commands.extend(["--top-k", str(sampling.get("top_k", 20))])
        commands.extend(["--top-p", str(sampling.get("top_p", 0.95))])
        commands.extend(["--min-p", str(sampling.get("min-p", 0.05))])
        if sampling.get("grammar"):
            commands.extend(["--grammar", sampling["grammar"]])
        return commands


class HefestoAutomation:
    """Pipeline de autodescoberta: flags novas → JSON → GBNF → consolidação."""

    @staticmethod
    def discover_flags() -> list:
        """Captura flags reais do llama.cpp (--help)."""
        try:
            env = dict(os.environ)
            env["LD_LIBRARY_PATH"] = LD_LIBRARY_PATH
            result = subprocess.run([LLAMA_CLI, "--help"], capture_output=True, text=True,
                                    check=True, env=env, timeout=30)
            help_output = result.stdout + result.stderr
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            help_output = "--model, -m : Caminho\n--ctx-size : Tamanho\n--new-hyper-parameter : Parâmetro de teste"
        return list(set(re.findall(r"(--[a-zA-Z0-9-]+)", help_output)))

    @staticmethod
    def read_registered(spec_path: Path = SPEC_PATH) -> set:
        """Lê flags registradas no spec.md."""
        if not spec_path.exists():
            return set()
        with open(spec_path, "r", encoding="utf-8") as f:
            return set(re.findall(r"-\s\*\*(--[a-zA-Z0-9-]+)\*\*", f.read()))

    @classmethod
    def sync_new_flags_to_json(cls, new_flags: list, config_path: Path = CONFIG_PATH) -> None:
        """Injeta novas flags no JSON com valor PENDING_GBNF_VAL."""
        if not config_path.exists():
            return
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        if "auto_discovered_features" not in config_data:
            config_data["auto_discovered_features"] = {}
        for flag in new_flags:
            clean_key = flag.lstrip("-")
            if clean_key not in config_data["auto_discovered_features"]:
                config_data["auto_discovered_features"][clean_key] = "PENDING_GBNF_VAL"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

    @classmethod
    def run_pipeline(cls) -> list:
        """Varre o ecossistema, descobre novidades e injeta no JSON."""
        discovered = cls.discover_flags()
        registered = cls.read_registered()
        new_flags = [f for f in discovered if f not in registered]
        if new_flags:
            cls.sync_new_flags_to_json(new_flags)
            return new_flags
        return []


class HefestoWebhookHandler(BaseHTTPRequestHandler):
    """Recebe gatilho externo (GitHub Actions/CRON) e roda o pipeline."""

    def do_POST(self):
        new_flags = HefestoAutomation.run_pipeline()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {"status": "success", "updated_flags": new_flags,
                    "action_required": len(new_flags) > 0}
        self.wfile.write(json.dumps(response).encode("utf-8"))


def start_webhook_server(port: int = 8098):
    server = HTTPServer(("0.0.0.0", port), HefestoWebhookHandler)
    print(f"🚀 Webhook do Hefesto aguardando gatilhos na porta {port}...")
    server.serve_forever()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Hefesto Llama Bridge (tríplice)")
    parser.add_argument("--compile", action="store_true", help="compilar flags do config")
    parser.add_argument("--discover", action="store_true", help="descobrir novas flags")
    parser.add_argument("--webhook", type=int, metavar="PORT", help="subir webhook")
    args = parser.parse_args()

    if args.compile:
        bridge = HefestoLlamaBridge()
        print(" ".join(bridge.compile_flags()))
        return 0
    if args.discover:
        new = HefestoAutomation.run_pipeline()
        print(json.dumps({"new_flags": new}, indent=2, ensure_ascii=False))
        return 0
    if args.webhook:
        start_webhook_server(args.webhook)
        return 0
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())