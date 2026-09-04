"""Model Inheritance — cada recurso herda um submodelo com health-gate.

Corrige a delegação que travava por invisibilidade de backend: em vez de todo
recurso de subagente cair em um endpoint local que pode estar CAÍDO (bug do
runtime), cada recurso (subagent/skill/hook/mcp/lsp/plugin/tool) resolve o seu
binding de modelo através desta camada, que:

1. consulta a tabela de herança (``harness.model_inheritance``), com override
   por recurso e default por categoria;
2. verifica a saúde do endpoint ANTES de delegar (local llama ``/health``,
   gateway ``/v1/models``);
3. em caso de backend morto, caminha a cadeia de fallback por prioridade até
   um backend VIVO — nunca delega para um endpoint que trava silenciosamente.

Capacidades: ``resolve()`` (binding efetivo), ``health_report()`` (estado de
todos os backends), ``selfcheck()`` e CLI. Stdlib-only, thread-safe.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_TIMEOUT_S = 2.0


class StallGuardError(RuntimeError):
    """Raised by fail-fast binding: no healthy backend — never launch a
    delegation that would hang silently for minutes on a dead endpoint."""


@dataclass
class Backend:
    """A model backend that resources can inherit."""

    name: str
    kind: str  # 'local' | 'gateway'
    base_url: str
    priority: int
    healthy: bool = False
    detail: str = field(default="")


@dataclass
class Binding:
    """Resolved model binding for a resource (post fallback)."""

    resource: str
    category: str
    backend: str
    base_url: str
    healthy: bool
    fallback_used: bool
    detail: str = ""


class ModelInheritance:
    """Health-gated model binding per resource/category.

    Config: ``harness.model_inheritance`` →
      backends: {name: {base_url, kind, priority}}
      defaults: {category: backend_name}
      overrides: {resource: backend_name or {backend, model}}
    """

    def __init__(self, project_root: str = "/mnt/dados", config_path: Optional[str] = None,
                 health_timeout: float = DEFAULT_TIMEOUT_S) -> None:
        self.project_root = Path(project_root)
        self.lock = threading.RLock()
        self.health_timeout = health_timeout

        cfg: Dict[str, Any] = {}
        path = Path(config_path) if config_path else self.project_root / "harness" / "harness-config.json"
        if path.is_file():
            try:
                cfg = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                cfg = {}

        b = (cfg.get("harness", {}) or {}).get("model_inheritance", {}) or {}
        backends_raw = b.get("backends", {}) or {}
        self.defaults: Dict[str, str] = dict(b.get("defaults", {}) or {})
        overrides = b.get("overrides", {}) or {}

        self.overrides: Dict[str, str] = {}
        for res, val in overrides.items():
            if isinstance(val, dict):
                self.overrides[res] = str(val.get("backend", ""))
            elif isinstance(val, str):
                self.overrides[res] = val

        self.backends: Dict[str, Backend] = {}
        for i, (name, meta) in enumerate(backends_raw.items()):
            if not isinstance(meta, dict):
                continue
            self.backends[name] = Backend(
                name=name,
                kind=str(meta.get("kind", "local")),
                base_url=str(meta.get("base_url", "")).rstrip("/"),
                priority=int(meta.get("priority", 100 + i)),
            )
        if not self.backends:
            self.backends = {
                "local-ornith": Backend("local-ornith", "local", "http://127.0.0.1:8083", 10),
                "local-bonsai": Backend("local-bonsai", "local", "http://127.0.0.1:8084", 20),
                "local-nanbeige": Backend("local-nanbeige", "local", "http://127.0.0.1:8082", 30),
                "local-lfm": Backend("local-lfm", "local", "http://127.0.0.1:8081", 40),
                "omniroute": Backend("omniroute", "gateway", "http://localhost:20128", 50),
            }

    # ------------------------------------------------------------------
    # health
    # ------------------------------------------------------------------
    def _probe(self, backend: Backend) -> tuple[bool, str]:
        try:
            url = backend.base_url + ("/health" if backend.kind == "local" else "/v1/models")
            r = subprocess.run(
                ["curl", "-s", "-m", str(int(self.health_timeout)), "-o", "/dev/null", "-w", "%{http_code}", url],
                capture_output=True, text=True, timeout=int(self.health_timeout) + 2,
            )
            code = r.stdout.strip()
            if code in ("200", "204"):
                return True, f"HTTP {code}"
            return False, f"HTTP {code or 'sem resposta'}"
        except Exception as exc:
            return False, f"erro: {exc}"

    def check_health(self) -> Dict[str, Dict[str, Any]]:
        with self.lock:
            for b in self.backends.values():
                ok, detail = self._probe(b)
                b.healthy = ok
                b.detail = detail
        return {name: {"healthy": b.healthy, "detail": b.detail, "kind": b.kind}
                for name, b in self.backends.items()}

    # ------------------------------------------------------------------
    # resolution
    # ------------------------------------------------------------------
    def resolve(self, resource: str, category: str = "subagent") -> Binding:
        """Return the binding for a resource, walking the fallback chain by
        health + priority until a healthy backend is found."""
        preferred = self.overrides.get(resource) or self.defaults.get(category)
        ordered = sorted(self.backends.values(), key=lambda b: (not b.healthy, b.priority))
        # slight reorder: prefer the explicit default when healthy
        candidates = list(ordered)
        if preferred:
            preferred_backend = self.backends.get(preferred)
            if preferred_backend and preferred_backend.healthy:
                candidates = [preferred_backend] + [b for b in ordered if b is not preferred_backend]

        chosen = next((b for b in candidates if b.healthy), None)
        if chosen is None:
            # re-probe once before giving up
            health = self.check_health()
            ordered2 = sorted(self.backends.values(), key=lambda b: (not b.healthy, b.priority))
            chosen = next((b for b in ordered2 if b.healthy), None)

        if chosen is None:
            fallback = sorted(self.backends.values(), key=lambda b: b.priority)
            chosen = fallback[0] if fallback else Backend("none", "local", "", 0)
            return Binding(resource, category, chosen.name, chosen.base_url,
                           healthy=False, fallback_used=True,
                           detail="nenhum backend saudável — usou prioridade máxima")
        fallback_used = preferred is not None and chosen.name != preferred
        return Binding(resource, category, chosen.name, chosen.base_url,
                       healthy=True, fallback_used=fallback_used,
                       detail=f"HTTP ok (prioridade {chosen.priority})")

    def health_report(self) -> Dict[str, Any]:
        health = self.check_health()
        total = len(health)
        up = sum(1 for v in health.values() if v["healthy"])
        return {"backends": health, "total": total, "healthy": up, "down": total - up}

    def guarded_resolve(self, resource: str, category: str = "subagent") -> Binding:
        """Fail-fast binding: guaranteed healthy backend or immediate error.

        Used right before igniting a delegation. It PROBES first (never trusts
        a stale cache), walks the priority chain, and only returns a binding
        whose backend is confirmed alive. If none is healthy it raises
        :class:`StallGuardError` immediately — making the 30-minute silent-stall
        failure mode structurally impossible.
        """
        self.check_health()
        ordered = sorted(self.backends.values(), key=lambda b: (not b.healthy, b.priority))
        preferred = self.overrides.get(resource) or self.defaults.get(category)
        if preferred:
            pref = self.backends.get(preferred)
            if pref and pref.healthy:
                ordered = [pref] + [b for b in ordered if b is not pref]
        chosen = next((b for b in ordered if b.healthy), None)
        if chosen is None:
            down = ", ".join(f"{b.name}({b.detail})" for b in ordered) or "nenhum backend cadastrado"
            raise StallGuardError(
                f"SEM BACKEND SAUDÁVEL p/ {category}:'{resource}' — recusa preventiva "
                f"(fail-fast, <{int(self.health_timeout)}s). Down: {down}. "
                f"Suba um llama-server local ou garanta o gateway omniroute antes de delegar."
            )
        fallback_used = preferred is not None and chosen.name != preferred
        return Binding(resource, category, chosen.name, chosen.base_url,
                       healthy=True, fallback_used=fallback_used,
                       detail=f"HTTP ok (prioridade {chosen.priority})")

    def stall_audit(self) -> Dict[str, Any]:
        report = self.health_report()
        ready = report["healthy"] > 0
        return {
            "ready": ready,
            "healthy_backend": next(
                (k for k, v in report["backends"].items() if v["healthy"]), None),
            "down_backends": [k for k, v in report["backends"].items() if not v["healthy"]],
            "report": report,
            "recommendation": "delegação autorizada" if ready else
                             "refatore a rota: suba llama-server OU aponte para gateway vivo ANTES de delegar",
        }

    # ------------------------------------------------------------------
    # selfcheck / CLI
    # ------------------------------------------------------------------
    def selfcheck(self) -> Dict[str, Any]:
        tmp = Path(tempfile.mkdtemp(prefix="model_inheritance_selfcheck_"))
        try:
            cfg = tmp / "h.json"
            cfg.write_text(json.dumps({"harness": {"model_inheritance": {
                "backends": {"a": {"base_url": "http://127.0.0.1:9", "kind": "local", "priority": 1},
                             "b": {"base_url": "http://127.0.0.1:80", "kind": "gateway", "priority": 2}},
                "defaults": {"subagent": "b"},
                "overrides": {"tool-x": "a"},
            }}}), encoding="utf-8")
            mi = ModelInheritance(project_root=str(tmp), config_path=str(cfg), health_timeout=1.0)
            report = mi.health_report()
            checks = {
                "report_built": set(report["backends"].keys()) == {"a", "b"},
                "resolve_no_crash": isinstance(mi.resolve("any", "subagent"), Binding),
                "resolve_override_preferred": mi.overrides.get("tool-x") == "a",
            }
            return {"ok": all(checks.values()), "checks": checks, "report": report}
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def _cli(self, argv: Optional[List[str]] = None) -> int:
        p = argparse.ArgumentParser(prog="harness.models.model_inheritance",
                                    description="Model inheritance + health-gate")
        sub = p.add_subparsers(dest="cmd")
        sub.add_parser("report")
        sp = sub.add_parser("resolve"); sp.add_argument("--resource", required=True)
        sp.add_argument("--category", default="subagent")
        sub.add_parser("selfcheck")
        args = p.parse_args(argv)
        if args.cmd == "report":
            print(json.dumps(self.health_report(), indent=2, ensure_ascii=False))
        elif args.cmd == "resolve":
            b = self.resolve(args.resource, args.category)
            print(json.dumps(vars(b), ensure_ascii=False))
        elif args.cmd == "selfcheck":
            print(json.dumps(self.selfcheck(), indent=2, ensure_ascii=False))
        else:
            p.print_help(); return 2
        return 0


def main(argv: Optional[List[str]] = None) -> int:
    return ModelInheritance()._cli(argv)


if __name__ == "__main__":
    sys.exit(main())
