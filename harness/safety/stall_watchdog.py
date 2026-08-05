"""Stall Watchdog — torna impossível o travamento silencioso da delegação.

Supervisiona a cadeia de backends que os recursos herdam (subagents, skills,
hooks, MCPs, LSPs, plugins, tools). A cada ciclo:

1. re-sonda TODOS os backends (nunca confia em cache);
2. se não houver backend saudável → falha RÁPIDO com diagnóstico acionável
   (em vez de baixar de 30min de hang silencioso);
3. se houver → devolve o binding saudável + relatório, registrando a auditoria
   em ``harness/logs/stall-watchdog.jsonl`` para fine-tuning de orquestração.

Integra com a Regra Global R6 (supervisão anti-travamento + self-healing):
o orquestrador chama :meth:`Watchdog.check` antes de cada ignição de recurso e
periodicamente (cadência ~1min, R7); em falha, refatora a rota (fallback de
backend ou recusa preventiva) automaticamente.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from harness.models.model_inheritance import ModelInheritance, StallGuardError

WATCHDOG_LOG = "stall-watchdog.jsonl"


class StallWatchdog:
    """Periodic anti-stall supervisor over the inherited model backends."""

    def __init__(self, project_root: str = "/mnt/dados",
                 inheritance: Optional[ModelInheritance] = None,
                 healer: Any = None,
                 interval_s: float = 60.0) -> None:
        self.project_root = Path(project_root)
        self.inheritance = inheritance or ModelInheritance(project_root=project_root)
        self.healer = healer
        self.interval_s = interval_s
        self.lock = threading.RLock()
        self.log_path = self.project_root / "harness" / "logs" / WATCHDOG_LOG
        try:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
        self._stop = threading.Event()
        self.last_check: Dict[str, Any] = {}

    def _log(self, record: Dict[str, Any]) -> None:
        record.setdefault("ts", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        try:
            with self.lock:
                with open(self.log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as exc:
            print(f"[Watchdog] warning: falha ao logar: {exc}")

    def check(self) -> Dict[str, Any]:
        """One supervision cycle. Fails FAST when no backend is healthy."""
        audit = self.inheritance.stall_audit()
        record = {
            "kind": "stall_check",
            "ready": audit["ready"],
            "healthy_backend": audit["healthy_backend"],
            "down_backends": audit["down_backends"],
            "recommendation": audit["recommendation"],
        }
        if self.healer is not None and not audit["ready"]:
            try:
                ha = self.healer.check_and_heal()
                record["self_heal"] = ha
            except Exception as exc:
                record["self_heal_error"] = str(exc)
        self._log(record)
        self.last_check = audit
        return audit

    def guarded_resolve(self, resource: str, category: str = "subagent") -> Dict[str, Any]:
        """Fail-fast model binding for a resource (raises StallGuardError)."""
        binding = self.inheritance.guarded_resolve(resource, category)
        self._log({"kind": "resolve", "resource": resource, "category": category,
                   "backend": binding.backend, "healthy": binding.healthy,
                   "fallback_used": binding.fallback_used})
        return {
            "resource": resource, "category": category, "backend": binding.backend,
            "base_url": binding.base_url, "healthy": binding.healthy,
            "fallback_used": binding.fallback_used,
        }

    def run_until_stopped(self) -> None:
        """Blocking supervised loop (R7 cadence)."""
        while not self._stop.wait(self.interval_s):
            try:
                self.check()
            except Exception as exc:  # keep the loop alive
                self._log({"kind": "error", "detail": str(exc)})

    def stop(self) -> None:
        self._stop.set()

    def history(self, limit: int = 10) -> List[Dict[str, Any]]:
        if not self.log_path.is_file():
            return []
        lines = self.log_path.read_text(encoding="utf-8").splitlines()
        out: List[Dict[str, Any]] = []
        for line in lines[-limit:]:
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
        return out

    def _cli(self, argv: Optional[List[str]] = None) -> int:
        p = argparse.ArgumentParser(prog="harness.safety.stall_watchdog",
                                    description="Stall Watchdog (R6/R7)")
        sub = p.add_subparsers(dest="cmd")
        sp = sub.add_parser("check")
        sr = sub.add_parser("resolve"); sr.add_argument("--resource", required=True)
        sr.add_argument("--category", default="subagent")
        sub.add_parser("history")
        spw = sub.add_parser("watch"); spw.add_argument("--interval", type=float, default=60.0)
        args = p.parse_args(argv)
        if args.cmd == "check":
            try:
                print(json.dumps(self.check(), indent=2, ensure_ascii=False))
            except StallGuardError as e:
                print(f"STALL-GUARD: {e}", file=sys.stderr)
                self._log({"kind": "guard_fail", "detail": str(e)})
                return 1
        elif args.cmd == "resolve":
            try:
                print(json.dumps(self.guarded_resolve(args.resource, args.category),
                                 indent=2, ensure_ascii=False))
            except StallGuardError as e:
                print(f"STALL-GUARD: {e}", file=sys.stderr)
                self._log({"kind": "guard_fail", "resource": args.resource, "detail": str(e)})
                return 1
        elif args.cmd == "history":
            print(json.dumps(self.history(), indent=2, ensure_ascii=False))
        elif args.cmd == "watch":
            self.interval_s = args.interval
            self.run_until_stopped()
        else:
            p.print_help(); return 2
        return 0


def main(argv: Optional[List[str]] = None) -> int:
    return StallWatchdog()._cli(argv)


if __name__ == "__main__":
    sys.exit(main())
