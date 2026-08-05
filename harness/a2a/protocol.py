"""A2A (Agent2Agent) protocol primitives.

Implements the 2026 A2A standard surface used by the Gran-Mestre hybrid
harness (see "Orquestrador de IA de Forma Profissional" §2.1):

* ``AgentCard``  — static advertisement used for agent discovery.
* ``Task``       — stateful unit of work exchanged between agents.
* ``A2AClient``  — in-memory transport (no network dependency yet) that
  negotiates OAuth-scope-style skill grants via ``handshake``.

Strict standard library only; no third-party imports.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _utcnow_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Task state machine
# ---------------------------------------------------------------------------
#   pending -> running -> completed | failed | needs_review
#   needs_review -> running (rework) | completed (approved) | failed
#   completed / failed are terminal.

_TASK_TRANSITIONS: Dict[str, frozenset] = {
    "pending": frozenset({"running"}),
    "running": frozenset({"completed", "failed", "needs_review"}),
    "needs_review": frozenset({"running", "completed", "failed"}),
    "completed": frozenset(),
    "failed": frozenset(),
}

TASK_STATES: List[str] = list(_TASK_TRANSITIONS)


@dataclass
class AgentCard:
    """Static agent advertisement as defined by the A2A spec.

    Each agent publishes a card so peers can discover its skills and
    capabilities; ``A2AClient.handshake`` then negotiates an
    OAuth-scope-style skill grant between two cards.
    """

    name: str
    description: str
    url: str = ""
    provider: str = "local"
    version: str = "1.0"
    skills: List[str] = field(default_factory=list)  # skill ids
    capabilities: Dict[str, Any] = field(default_factory=dict)  # e.g. {"mcp": [...], "models": [...]}

    def to_json(self) -> str:
        """Serialize this card to a JSON string."""
        return json.dumps(asdict(self), ensure_ascii=False, indent=2, default=str)

    @classmethod
    def from_json(cls, s: str) -> "AgentCard":
        """Deserialize an ``AgentCard`` from a JSON string."""
        return cls(**json.loads(s))


@dataclass
class Task:
    """A unit of work exchanged between agents (A2A ``Task``).

    State machine: ``pending -> running -> completed | failed | needs_review``.
    ``needs_review`` may return to ``running`` (rework) or reach a terminal
    state after human review.
    """

    task_id: str
    parent_task_id: str = ""
    state: str = "pending"
    payload: Dict[str, Any] = field(default_factory=dict)
    result: Dict[str, Any] = field(default_factory=dict)
    error: str = ""
    created_at: str = field(default_factory=_utcnow_iso)
    updated_at: str = ""

    def __post_init__(self) -> None:
        if self.state not in TASK_STATES:
            raise ValueError(
                f"unknown task state {self.state!r}; expected one of {TASK_STATES}"
            )
        if not self.updated_at:
            self.updated_at = _utcnow_iso()

    def advance(self, new_state: str) -> None:
        """Transition the task to ``new_state``, validating the move."""
        allowed = _TASK_TRANSITIONS.get(self.state, frozenset())
        if new_state not in allowed:
            raise ValueError(
                f"invalid task transition: {self.state!r} -> {new_state!r} "
                f"(allowed from {self.state!r}: {sorted(allowed) or 'terminal state'})"
            )
        self.state = new_state
        self.updated_at = _utcnow_iso()

    def complete(self, result: Dict[str, Any]) -> None:
        """Store ``result`` and move the task to ``completed``."""
        self.result = result
        self.advance("completed")

    def to_json(self) -> str:
        """Serialize this task to a JSON string."""
        return json.dumps(asdict(self), ensure_ascii=False, indent=2, default=str)

    @classmethod
    def from_json(cls, s: str) -> "Task":
        """Deserialize a ``Task`` from a JSON string."""
        return cls(**json.loads(s))


class A2AClient:
    """In-memory A2A transport.

    No network dependency: tasks are stored in-process and routed by agent
    name. ``handshake`` negotiates the OAuth-scope-style skill grant between
    two ``AgentCard`` advertisements.
    """

    def __init__(self, registry: Optional["AgentRegistry"] = None) -> None:
        self._registry = registry
        self._tasks: Dict[str, Task] = {}
        self._routes: Dict[str, Dict[str, str]] = {}
        self._seq = 0

    def send(self, from_agent: str, to_agent: str, task: Task) -> str:
        """Route ``task`` from ``from_agent`` to ``to_agent``.

        Returns the task id (generating one when ``task.task_id`` is empty).
        A fresh ``pending`` task is auto-accepted into ``running``.
        """
        self._seq += 1
        if not task.task_id:
            task.task_id = f"task-{self._seq:04d}"
        if task.state == "pending":
            task.advance("running")
        self._tasks[task.task_id] = task
        self._routes[task.task_id] = {"from": from_agent, "to": to_agent}
        return task.task_id

    def poll(self, task_id: str) -> Task:
        """Fetch the current task snapshot for ``task_id``."""
        if task_id not in self._tasks:
            raise KeyError(f"unknown task: {task_id!r}")
        return self._tasks[task_id]

    def handshake(self, from_card: AgentCard, to_card: AgentCard) -> Dict[str, Any]:
        """Negotiate a capability agreement between two agents.

        Returns an OAuth-scope-style grant: skills both cards advertise are
        ``allowed``; skills only the requester offers are ``denied``.
        """
        from_skills = set(from_card.skills)
        to_skills = set(to_card.skills)
        allowed = sorted(from_skills & to_skills)
        denied = sorted(from_skills - to_skills)
        return {
            "protocol": "a2a",
            "from": from_card.name,
            "to": to_card.name,
            "scope": " ".join(allowed),
            "allowed": allowed,
            "denied": denied,
            "capabilities": dict(to_card.capabilities),
        }
