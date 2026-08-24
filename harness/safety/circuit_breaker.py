#!/usr/bin/env python3
"""Circuit-Breaker Global (R18) — N tentativas OU time-box sem progresso.

Fechamento do gap de supervisão: o subagente **vivo mas improdutivo** (repete,
gira em círculo, silencia sem tool output) não era pego por R6 (backend morto)
nem R7 (heartbeat periódico). O CircuitBreaker cobre esse buraco.

Estados:
  CLOSED    → operação normal (ok)
  OPEN      → tripado (falhas consecutivas >= max_failures OU timeout sem progresso)
  HALF_OPEN → cooldown em andamento (após timeout, permite 1 tentativa de recuperação)
  BLOCK     → rollback_max atingido → gate humano obrigatório

Ações por nível de falha:
  1ª/2ª falha → escalar (Dev Loop N1→N2→N3 + subagente fresco)
  3ª falha    → abortar task
  rollback disponível + evidência parcial → git reset --hard (máx 1x por pipeline)
  rollback já usado → BLOCK com gate humano

Log: 1 linha JSONL por transição de estado em harness/logs/circuit-breaker.jsonl.

Defaults: max_failures=3, progress_timeout_seconds=300, cooldown_seconds=60,
          rollback_max=1 (overrides via harness.circuit_breaker no harness-config.json).
"""

from __future__ import annotations

import enum
import json
import sys
import time
import threading
import argparse
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


class CBState(str, enum.Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"
    BLOCK = "BLOCK"


class CircuitBreakerError(RuntimeError):
    """Raised when the circuit is OPEN or BLOCK — no delegation allowed."""

    def __init__(self, state: CBState, task_id: str, detail: str = ""):
        self.state = state
        self.task_id = task_id
        super().__init__(f"CircuitBreaker [{state.value}] task={task_id}: {detail}")


class CircuitBreaker:
    """Per-task circuit breaker with state machine and JSONL audit log.

    Clock is injectable (``time_fn``) so tests can advance time without sleep.
    Zero network, zero sleep — pure state machine.
    """

    def __init__(
        self,
        project_root: str = "/mnt/dados",
        max_failures: int = 3,
        progress_timeout_s: float = 300.0,
        cooldown_s: float = 60.0,
        rollback_max: int = 1,
        time_fn: Optional[Callable[[], float]] = None,
        log_path: Optional[str] = None,
    ) -> None:
        self.project_root = Path(project_root)
        self.max_failures = max_failures
        self.progress_timeout_s = progress_timeout_s
        self.cooldown_s = cooldown_s
        self.rollback_max = rollback_max
        self._time = time_fn or time.time
        self._lock = threading.RLock()

        # Per-task state
        self._states: Dict[str, CBState] = {}
        self._failure_counts: Dict[str, int] = {}
        self._last_heartbeat: Dict[str, float] = {}
        self._opened_at: Dict[str, float] = {}
        self._rollback_used: Dict[str, int] = {}

        # Log path
        if log_path:
            self._log_path = Path(log_path)
        else:
            self._log_path = self.project_root / "harness" / "logs" / "circuit-breaker.jsonl"
        try:
            self._log_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass

    def _log(self, record: Dict[str, Any]) -> None:
        record.setdefault("ts", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        try:
            with self._lock:
                with open(self._log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError:
            pass

    def _transition(self, task_id: str, new_state: CBState, reason: str = "") -> None:
        old_state = self._states.get(task_id, CBState.CLOSED)
        self._states[task_id] = new_state
        self._log({
            "kind": "transition",
            "task_id": task_id,
            "from": old_state.value,
            "to": new_state.value,
            "reason": reason,
            "failure_count": self._failure_counts.get(task_id, 0),
        })

    def state(self, task_id: str) -> CBState:
        """Current state of a task's circuit (auto-transitions on timeout)."""
        with self._lock:
            current = self._states.get(task_id, CBState.CLOSED)
            # Check for progress timeout (CLOSED → OPEN)
            if current == CBState.CLOSED and task_id in self._last_heartbeat:
                elapsed = self._time() - self._last_heartbeat[task_id]
                if elapsed > self.progress_timeout_s:
                    self._transition(task_id, CBState.OPEN,
                                     f"progress_timeout ({elapsed:.0f}s > {self.progress_timeout_s}s)")
                    return CBState.OPEN
            # Check for cooldown expiry (OPEN → HALF_OPEN)
            if current == CBState.OPEN and task_id in self._opened_at:
                elapsed = self._time() - self._opened_at[task_id]
                if elapsed >= self.cooldown_s:
                    self._transition(task_id, CBState.HALF_OPEN, "cooldown_expired")
                    return CBState.HALF_OPEN
            return self._states.get(task_id, CBState.CLOSED)

    def guard(self, task_id: str) -> CBState:
        """Check if delegation is allowed. Raises CircuitBreakerError if not.

        Returns the current state if allowed (CLOSED or HALF_OPEN).
        """
        st = self.state(task_id)
        if st == CBState.OPEN:
            raise CircuitBreakerError(st, task_id, "circuit OPEN — aguarde cooldown")
        if st == CBState.BLOCK:
            raise CircuitBreakerError(st, task_id, "circuit BLOCK — gate humano necessário")
        return st

    def touch(self, task_id: str) -> None:
        """Register a heartbeat (progress signal) for a task."""
        with self._lock:
            self._last_heartbeat[task_id] = self._time()
            # If was OPEN due to timeout, reset to CLOSED on touch
            if self._states.get(task_id) == CBState.OPEN:
                self._transition(task_id, CBState.CLOSED, "heartbeat_restored")

    def record_failure(self, task_id: str) -> Dict[str, Any]:
        """Record a failure. Returns action dict: {action, detail}.

        Actions:
          - 'escalate': 1st/2nd failure → escalate via Dev Loop
          - 'abort': 3rd failure → abort task
          - 'rollback': abort + rollback available (max 1x)
          - 'block': rollback already used → gate humano
        """
        with self._lock:
            count = self._failure_counts.get(task_id, 0) + 1
            self._failure_counts[task_id] = count

            if count < self.max_failures:
                self._transition(task_id, CBState.CLOSED, f"failure_{count}_escalate")
                return {"action": "escalate", "failure_count": count,
                        "detail": f"falha #{count} — escalar (Dev Loop N+1)"}

            # max_failures reached → OPEN
            self._opened_at[task_id] = self._time()
            self._transition(task_id, CBState.OPEN, f"max_failures_reached ({count})")

            # Check rollback availability
            rb_used = self._rollback_used.get(task_id, 0)
            if rb_used < self.rollback_max:
                self._rollback_used[task_id] = rb_used + 1
                return {"action": "rollback", "failure_count": count,
                        "detail": f"falha #{count} — abort + rollback (uso {rb_used+1}/{self.rollback_max})"}

            # Rollback exhausted → BLOCK
            self._transition(task_id, CBState.BLOCK, "rollback_exhausted_gate_human")
            return {"action": "block", "failure_count": count,
                    "detail": f"falha #{count} — rollback esgotado, gate humano"}

    def record_success(self, task_id: str) -> None:
        """Record a success. Resets failure count and closes circuit."""
        with self._lock:
            self._failure_counts[task_id] = 0
            self._last_heartbeat[task_id] = self._time()
            if self._states.get(task_id) in (CBState.HALF_OPEN, CBState.OPEN):
                self._transition(task_id, CBState.CLOSED, "success_recovery")
            elif self._states.get(task_id) != CBState.CLOSED:
                self._transition(task_id, CBState.CLOSED, "success")

    def reset(self, task_id: str) -> None:
        """Full reset of a task's circuit (for testing or manual intervention)."""
        with self._lock:
            self._states.pop(task_id, None)
            self._failure_counts.pop(task_id, None)
            self._last_heartbeat.pop(task_id, None)
            self._opened_at.pop(task_id, None)
            self._rollback_used.pop(task_id, None)
            self._log({"kind": "reset", "task_id": task_id})

    def status(self, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Return status of one or all circuits."""
        with self._lock:
            if task_id:
                return {
                    "task_id": task_id,
                    "state": self.state(task_id).value,
                    "failures": self._failure_counts.get(task_id, 0),
                    "rollback_used": self._rollback_used.get(task_id, 0),
                }
            return {
                tid: {
                    "state": self._states.get(tid, CBState.CLOSED).value,
                    "failures": self._failure_counts.get(tid, 0),
                    "rollback_used": self._rollback_used.get(tid, 0),
                }
                for tid in set(list(self._states.keys()) + list(self._failure_counts.keys()))
            }

    def history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Read recent log entries."""
        if not self._log_path.is_file():
            return []
        lines = self._log_path.read_text(encoding="utf-8").splitlines()
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
        p = argparse.ArgumentParser(prog="harness.safety.circuit_breaker",
                                    description="Circuit-Breaker Global (R18)")
        sub = p.add_subparsers(dest="cmd")
        ss = sub.add_parser("status"); ss.add_argument("--task", default=None)
        sub.add_parser("history")
        sr = sub.add_parser("reset"); sr.add_argument("--task", required=True)
        args = p.parse_args(argv)
        if args.cmd == "status":
            print(json.dumps(self.status(args.task), indent=2, ensure_ascii=False))
        elif args.cmd == "history":
            print(json.dumps(self.history(), indent=2, ensure_ascii=False))
        elif args.cmd == "reset":
            self.reset(args.task)
            print(f"reset OK: {args.task}")
        else:
            p.print_help(); return 2
        return 0


def main(argv: Optional[List[str]] = None) -> int:
    return CircuitBreaker()._cli(argv)


if __name__ == "__main__":
    sys.exit(main())
