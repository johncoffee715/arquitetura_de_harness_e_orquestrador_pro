"""Self-Heal híbrido local+nuvem (Regra Global R10).

Sempre que a stack local (llama-server :8081-:8084) é detectada no chão, este
módulo:

1. emite uma REDFLAG INTERNA E SILENCIOSA (aprendizado de predição, prevenção
   e correção) em ``harness/logs/redflags.jsonl`` — não polui o usuário;
2. tenta RELANÇAR a stack local (start-all-models.sh / start-llama.sh) e
   re-prova a saúde, devolvendo o controle ao híbrido local (prioridade) +
   nuvem omniroute (cobertura enquanto locals sobem).

A transição up→down é rastreada por estado persistente, evitando redflag por
tick (só dispara na QUEDA, não em repetição). Integrated ao StallWatchdog.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from harness.models.model_inheritance import ModelInheritance

REDFLAGS_FILE = "redflags.jsonl"
LOCAL_BACKENDS = ("local-ornith", "local-bonsai", "local-nanbeige", "local-lfm")


class LocalStackHealer:
    """RedFlag silencioso + reintenção de subida da stack local."""

    def __init__(self, project_root: str = "/mnt/dados",
                 inheritance: Optional[ModelInheritance] = None,
                 launch_cmd: Optional[List[str]] = None,
                 timeout_s: int = 180) -> None:
        self.project_root = Path(project_root)
        self.lock = threading.RLock()
        self.inheritance = inheritance or ModelInheritance(project_root=project_root)
        self.launch_cmd = launch_cmd
        self.timeout_s = timeout_s
        self._prev_state: Dict[str, bool] = {}
        self.redflags_path = self.project_root / "harness" / "logs" / REDFLAGS_FILE
        try:
            self.redflags_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
        self._state_file = self.project_root / "harness" / "logs" / ".self_heal_state.json"

    def _load_state(self) -> Dict[str, bool]:
        if self._state_file.is_file():
            try:
                return json.loads(self._state_file.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                pass
        return {}

    def _save_state(self, state: Dict[str, bool]) -> None:
        try:
            self._state_file.write_text(json.dumps(state), encoding="utf-8")
        except OSError:
            pass

    def redflag(self, backend: str, detail: str, reason: str = "local_stack_down") -> Dict[str, Any]:
        """Silent internal redflag for learning (prediction/prevention/correction)."""
        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "kind": reason,
            "backend": backend,
            "detail": detail,
            "learned": {
                "predict": "verificar saúde de backends locais antes de delegar (health-probe R9)",
                "prevent": "watchdog R7 em cadência ~1min + guarda de delegação R9 (nunca delega p/ morto)",
                "correct": "relançar stack local (start-all-models.sh) + cobertura nuvem omniroute até subir",
            },
        }
        try:
            with self.lock:
                with open(self.redflags_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as exc:
            print(f"[SelfHeal] warning: falha ao gravar redflag: {exc}")
        return record

    def _local_up(self) -> Dict[str, bool]:
        health = self.inheritance.check_health()
        return {name: health.get(name, {}).get("healthy", False)
                for name in LOCAL_BACKENDS if name in health}

    def heal(self) -> Dict[str, Any]:
        """Attempt to bring the local stack back online; returns report."""
        local_up = self._local_up()
        down = [k for k, v in local_up.items() if not v]
        if not down:
            return {"attempted": False, "ok": True, "down": [], "up": [k for k, v in local_up.items() if v]}
        cmd = self.launch_cmd or [
            "bash", str(self.project_root / "harness" / "start-all-models.sh"),
        ]
        attempted = False
        result = None
        try:
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    timeout=self.timeout_s)
            attempted = True
        except FileNotFoundError:
            result = None
        except subprocess.TimeoutExpired:
            result = None
        if not attempted:
            return {"attempted": False, "ok": False, "down": down, "up": [],
                    "error": "script de launch indisponível ou timeout"}
        try:
            time.sleep(min(8, self.timeout_s // 10))
        except Exception:
            pass
        after = self._local_up()
        now_up = [k for k, v in after.items() if v]
        return {"attempted": True, "ok": len(now_up) > 0, "down": [k for k, v in after.items() if not v],
                "up": now_up, "launch_exit": getattr(result, "returncode", None)}

    def check_and_heal(self) -> Dict[str, Any]:
        """Emit redflag on up->down transition, then attempt recovery."""
        local_up = self._local_up()
        prev = self._load_state()
        report = {"down": [k for k, v in local_up.items() if not v],
                  "up": [k for k, v in local_up.items() if v],
                  "redflags": []}
        for name, healthy in local_up.items():
            was_up = prev.get(name, True)  # assume up initially to avoid cold-start spam
            if was_up and not healthy:
                rec = self.redflag(name, "stack local derrubada detectada (up→down)")
                report["redflags"].append(rec)
        self._save_state(local_up)
        if report["down"] and report["redflags"]:
            heal_result = self.heal()
            report.update(heal_result)
        return report

    def selfcheck(self) -> Dict[str, Any]:
        tmp = Path(tempfile.mkdtemp(prefix="self_heal_selfcheck_"))
        try:
            cfg = tmp / "h.json"
            cfg.write_text(json.dumps({"harness": {"model_inheritance": {
                "backends": {n: {"base_url": "http://127.0.0.1:9", "kind": "local",
                                 "priority": i} for i, n in enumerate(LOCAL_BACKENDS)},
                "defaults": {}, "overrides": {},
            }}}), encoding="utf-8")
            mi = ModelInheritance(project_root=str(tmp), config_path=str(cfg), health_timeout=1.0)
            healer = LocalStackHealer(project_root=str(tmp), inheritance=mi,
                                      launch_cmd=["true"], timeout_s=2)
            local_up = healer._local_up()
            checks = {
                "all_locals_down": all(not v for v in local_up.values()),
                "redflag_written": healer.redflag("local-ornith", "teste").get("kind") == "local_stack_down",
                "redflag_file_exists": healer.redflags_path.is_file(),
            }
            return {"ok": all(checks.values()), "checks": checks,
                    "local_up": local_up}
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def _cli(self, argv: Optional[List[str]] = None) -> int:
        p = argparse.ArgumentParser(prog="harness.safety.self_heal",
                                    description="Self-heal híbrido (R10)")
        sub = p.add_subparsers(dest="cmd")
        sub.add_parser("check")
        sub.add_parser("heal")
        sub.add_parser("selfcheck")
        args = p.parse_args(argv)
        if args.cmd == "check":
            print(json.dumps(self.check_and_heal(), indent=2, ensure_ascii=False))
        elif args.cmd == "heal":
            print(json.dumps(self.heal(), indent=2, ensure_ascii=False))
        elif args.cmd == "selfcheck":
            print(json.dumps(self.selfcheck(), indent=2, ensure_ascii=False))
        else:
            p.print_help(); return 2
        return 0


def main(argv: Optional[List[str]] = None) -> int:
    return LocalStackHealer()._cli(argv)


if __name__ == "__main__":
    sys.exit(main())
