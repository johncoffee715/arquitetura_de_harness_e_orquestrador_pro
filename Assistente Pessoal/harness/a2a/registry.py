"""A2A agent registry seeded from the Gran-Mestre ``registry.json`` catalog.

Reads the subagents list from ``/mnt/dados/Assistente Pessoal/harness/registry.json`` (READ
ONLY — never writes) and turns every subagent into an ``AgentCard`` with
``name`` from the agent id, ``description`` from the catalog, and
capabilities derived from ``model`` / ``mode`` / ``source`` when present.

Provides discovery (``discover``), lookup (``card``), and ``A2ARegistry``,
the seeded variant used by the harness for a no-network ``selfcheck`` smoke
test that registers cards, performs a handshake and a task send/complete
round-trip.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from harness.a2a.protocol import A2AClient, AgentCard, Task

DEFAULT_REGISTRY = "/mnt/dados/Assistente Pessoal/harness/registry.json"


class AgentRegistry:
    """A2A discovery registry.

    ``discover(capability)`` matches both skill ids and capability keys /
    values, so a query such as ``"models"`` or ``"research"`` finds every
    card that can serve it.
    """

    def __init__(self, registry_path: Optional[str] = None) -> None:
        self._agents: Dict[str, AgentCard] = {}
        if registry_path:
            self.seed(registry_path)

    # -- seeding ------------------------------------------------------------
    def seed(self, registry_path: str) -> int:
        """Load the ``subagents`` list from a registry JSON catalog.

        Registers one ``AgentCard`` per subagent; returns the number of
        entries processed. The catalog file is opened read-only.
        """
        with open(registry_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        entries = data.get("subagents", []) if isinstance(data, dict) else []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            card = self._card_from_entry(entry)
            if card is not None:
                self.register(card)
        return len(entries)

    @staticmethod
    def _card_from_entry(entry: Dict[str, Any]) -> Optional[AgentCard]:
        """Build an ``AgentCard`` from one subagent catalog entry."""
        name = entry.get("name") or entry.get("id")
        if not name:
            return None

        capabilities: Dict[str, Any] = {}
        model = entry.get("model")
        if model:
            capabilities["models"] = [model] if isinstance(model, str) else list(model)
        role = entry.get("mode") or entry.get("role")
        if role:
            capabilities["role"] = role
        source = entry.get("source")
        if source:
            capabilities["source"] = source

        skills = entry.get("skills")
        skill_list = list(skills) if isinstance(skills, list) else []

        return AgentCard(
            name=str(name),
            description=str(entry.get("description") or ""),
            url=str(entry.get("url") or ""),
            provider=str(entry.get("provider") or "local"),
            version=str(entry.get("version") or "1.0"),
            skills=skill_list,
            capabilities=capabilities,
        )

    # -- public API ---------------------------------------------------------
    def register(self, card: AgentCard) -> None:
        """Register (or re-register) an agent card under ``card.name``."""
        self._agents[card.name] = card

    def discover(self, capability: str) -> List[AgentCard]:
        """Return every card that advertises ``capability``.

        Matches skill ids as well as capability keys and list values.
        """
        matches: List[AgentCard] = []
        for card in self._agents.values():
            if capability in card.skills:
                matches.append(card)
                continue
            for key, values in card.capabilities.items():
                if capability == key:
                    matches.append(card)
                    break
                if isinstance(values, list) and capability in values:
                    matches.append(card)
                    break
        return matches

    def card(self, name: str) -> Optional[AgentCard]:
        """Look up an agent card by name (``None`` when unknown)."""
        return self._agents.get(name)

    def __len__(self) -> int:
        return len(self._agents)


class A2ARegistry(AgentRegistry):
    """Seeded A2A registry with a no-network ``selfcheck`` smoke test."""

    DEMO_SKILLS: Dict[str, List[str]] = {
        "gran-mestre": ["orchestration", "routing", "planning", "delegation"],
        "gsd-advisor-researcher": ["research", "analysis", "planning"],
        "gsd-code-fixer": ["coding", "fix", "review", "planning"],
    }

    def __init__(self, registry_path: Optional[str] = None) -> None:
        path = registry_path or DEFAULT_REGISTRY
        super().__init__(path if os.path.exists(path) else None)

    def _pick_demo_cards(self) -> List[AgentCard]:
        """Pick up to 3 cards from the real registry for the smoke test.

        Prefers the named demo agents (granting them demo skills so the
        handshake yields a meaningful allowed/denied grant); falls back to
        any other seeded card to fill the set.
        """
        picked: List[AgentCard] = []
        for name in self.DEMO_SKILLS:
            card = self.card(name)
            if card is not None:
                card.skills = list(self.DEMO_SKILLS.get(name, card.skills))
                picked.append(card)
        for card in list(self._agents.values()):
            if len(picked) >= 3:
                break
            if card not in picked:
                picked.append(card)
        if len(picked) < 2:
            raise RuntimeError(
                f"A2A selfcheck requires at least 2 agents; registry has {len(self)}"
            )
        return picked[:3]

    def selfcheck(self) -> Dict[str, Any]:
        """No-network smoke test: 3 cards, a handshake and a task round-trip.

        Prints JSON progress lines and returns a JSON-serializable summary.
        """
        cards = self._pick_demo_cards()
        client = A2AClient(self)

        # 1. handshake (OAuth-scope-style skill grant)
        grant = client.handshake(cards[0], cards[1])
        print(
            json.dumps(
                {"selfcheck": "handshake", **grant},
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        # 2. task send/complete round-trip
        task = Task(
            task_id="",
            payload={"instruction": "fix review findings", "target": "harness/a2a"},
        )
        task_id = client.send(cards[0].name, cards[1].name, task)
        task.advance("needs_review")
        task.complete({"status": "ok", "files": ["harness/a2a/protocol.py"]})
        polled = client.poll(task_id)
        print(
            json.dumps(
                {"selfcheck": "roundtrip", "task": polled.to_json()},
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        return {
            "status": "ok",
            "registry_size": len(self),
            "cards": [card.name for card in cards],
            "handshake": {
                "from": grant["from"],
                "to": grant["to"],
                "allowed": grant["allowed"],
                "denied": grant["denied"],
            },
            "roundtrip": {
                "task_id": task_id,
                "state": polled.state,
                "result": polled.result,
            },
        }
