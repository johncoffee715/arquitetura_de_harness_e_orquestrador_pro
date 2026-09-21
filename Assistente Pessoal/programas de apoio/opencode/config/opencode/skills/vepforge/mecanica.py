#!/usr/bin/env python3
"""
mecanica.py — vepforge (R77+R81+R85): cadeia de verificadores de evidência.
Helenizado de huzjie/vepforge (MIT). Zero dependência externa.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class Evidence:
    kind: str            # exit_code | hash | http_status | schema | test_result | stdout
    value: Any
    verified: bool = False
    detail: str = ""


@dataclass
class Verifier:
    name: str
    check: Callable[[Evidence], bool]
    detail: Callable[[Evidence], str] = lambda e: ""

    def verify(self, ev: Evidence) -> Evidence:
        try:
            ev.verified = bool(self.check(ev))
        except Exception as exc:  # noqa: BLE001
            ev.verified = False
            ev.detail = f"erro: {exc}"
        if not ev.detail:
            ev.detail = self.detail(ev)
        return ev


# ── verificadores canônicos ────────────────────────────────────────────────
EXIT_CODE = Verifier("exit_code", lambda e: e.value == 0, lambda e: f"exit={e.value}")
HASH_64 = Verifier("hash", lambda e: bool(re.fullmatch(r"[0-9a-fA-F]{64}", str(e.value))),
                   lambda e: f"hash={str(e.value)[:12]}…")
HTTP_2XX = Verifier("http_status", lambda e: isinstance(e.value, int) and 200 <= e.value < 300,
                    lambda e: f"http={e.value}")
SCHEMA = Verifier("schema", lambda e: _schema_ok(e.value), lambda e: "json-ok" if _schema_ok(e.value) else "json-invalido")
TEST_OK = Verifier("test_result", lambda e: isinstance(e.value, dict) and int(e.value.get("failed", 1)) == 0,
                   lambda e: f"failed={e.value.get('failed') if isinstance(e.value, dict) else '?'}")
NONEMPTY = Verifier("stdout", lambda e: bool(str(e.value).strip()), lambda e: "nao-vazio" if str(e.value).strip() else "vazio")


def _schema_ok(v: Any) -> bool:
    if isinstance(v, (dict, list)):
        return True
    if isinstance(v, str):
        try:
            json.loads(v)
            return True
        except Exception:  # noqa: BLE001
            return False
    return False


CHAIN: dict[str, Verifier] = {v.name: v for v in (EXIT_CODE, HASH_64, HTTP_2XX, SCHEMA, TEST_OK, NONEMPTY)}


def verify_chain(evidence: Evidence, names: Optional[list[str]] = None) -> Evidence:
    """Aplica a cadeia de verificadores; qualquer falha marca verified=False e para."""
    for name in names or [evidence.kind]:
        v = CHAIN.get(name)
        if v is None:
            evidence.detail = f"verifier desconhecido: {name}"
            evidence.verified = False
            return evidence
        evidence = v.verify(evidence)
        if not evidence.verified:
            return evidence
    return evidence


# ── Experience + Linker (rastreabilidade) ──────────────────────────────────
@dataclass
class Step:
    index: int
    action: str
    artifacts: list[str] = field(default_factory=list)
    evidences: list[Evidence] = field(default_factory=list)

    @property
    def verified(self) -> bool:
        return bool(self.evidences) and all(e.verified for e in self.evidences)


@dataclass
class Experience:
    task: str
    steps: list[Step] = field(default_factory=list)
    trajectory: list[str] = field(default_factory=list)

    def add_step(self, action: str, artifacts: list[str], evidences: list[Evidence]) -> Step:
        st = Step(index=len(self.steps) + 1, action=action, artifacts=artifacts, evidences=evidences)
        self.steps.append(st)
        self.trajectory.append(f"{st.index}:{action}:verified={st.verified}")
        return st

    def summary(self) -> dict[str, Any]:
        return {
            "task": self.task,
            "steps": len(self.steps),
            "verified_steps": sum(1 for s in self.steps if s.verified),
            "trajectory": self.trajectory,
        }


if __name__ == "__main__":
    # smoke: pipeline determinístico
    exp = Experience("teste")
    e1 = verify_chain(Evidence("exit_code", 0))
    e2 = verify_chain(Evidence("schema", '{"ok": true}'))
    e3 = verify_chain(Evidence("http_status", 500))
    exp.add_step("rodar-teste", ["out.json"], [e1, e2])
    exp.add_step("deploy", [], [e3])
    print(json.dumps(exp.summary(), ensure_ascii=False))
    assert exp.steps[0].verified is True
    assert exp.steps[1].verified is False
    print("smoke OK")