import json
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional


def _norm(text: str) -> str:
    """Strip accents and lowercase text for matching."""
    return "".join(
        c for c in unicodedata.normalize("NFD", text.lower())
        if unicodedata.category(c) != "Mn"
    )


class CapabilityIndex:
    """Maps registry agent capabilities to local models via greedy set cover."""

    DEFAULT_REGISTRY = "/mnt/dados/opencode/registry/agent-registry.json"
    FALLBACK_REGISTRY = "/mnt/dados/Assistente Pessoal/harness/registry.json"

    TAG_KEYWORDS = {
        "coding": ["codigo", "code", "implement", "execut", "program",
                   "desenvolv", "build", "coding", "decompil", "reversa"],
        "mcp": ["mcp", "model context protocol"],
        "auth": ["auth", "autentic", "login", "token", "jwt", "oauth", "seguranca"],
        "infra": ["infra", "database", "banco", "postgres", "sql", "redis",
                  "kafka", "docker", "cloud", "aws", "gcp"],
        "policy": ["policy", "politica", "rate", "quota", "limite", "throttl",
                   "conformidade", "validar", "verific"],
        "test": ["test", "teste", "tdd", "coverage", "cobertura", "verifica",
                 "verify", "validar", "validacao"],
        "docs": ["doc", "documenta", "readme", "memoria", "gravar", "arquivar",
                 "report"],
    }

    MODEL_ORNITH = ("gran-mestre", "prometheus", "atena")
    MODEL_BONSAI = ("atlas", "code-reviewer", "gsd-executor",
                    "gsd-planner", "gsd-debugger")
    MODEL_NANBEIGE = ("hestia", "memory-keeper", "reverser",
                      "gsd-verifier", "gsd-code-reviewer", "ghidra")

    def __init__(self, registry_path: Optional[str] = None):
        path = Path(registry_path or self.DEFAULT_REGISTRY)
        if not path.exists():
            path = Path(self.FALLBACK_REGISTRY)
        self.registry_path = path
        self.entries: List[dict] = []

    def load(self) -> List[dict]:
        """Load registry entries, tolerating missing keys."""
        self.entries = []
        if not self.registry_path.exists():
            return self.entries
        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            entries = data.get("entries") or []
            if isinstance(entries, list):
                self.entries = entries
        return self.entries

    def model_for(self, agent_id: str) -> str:
        """Local protocol model assignment for an agent id."""
        if agent_id in self.MODEL_ORNITH or agent_id.startswith("superpowers-"):
            return "local-ornith/ornith-9b"
        if agent_id in self.MODEL_BONSAI:
            return "local-bonsai/bonsai-27b"
        return "local-nanbeige/nanbeige-3b"

    def capability_overlap(self, agent_caps: List[str], tags: Dict[str, str]) -> float:
        """Normalized overlap (0..1) between agent capabilities and demand tags."""
        if not agent_caps or not tags:
            return 0.0
        covered = self._covered_keys(agent_caps, tags)
        return len(covered) / len(tags)

    def greedy_cover(self, demand) -> List[dict]:
        """Greedy set cover of demand tags by registry agents."""
        entries = self.load()
        tags = demand.tags or {}
        if not entries or not tags:
            return []
        raw = _norm(demand.raw or "")
        force_gm = (
            demand.complexity in ("COMPLEX", "CRITICAL")
            or any(kw in raw for kw in ("orquestr", "roteir", "rout"))
        )
        remaining = set(tags.keys())
        chosen = []
        gm = next((e for e in entries if e.get("id") == "gran-mestre"), None)
        if force_gm and gm:
            chosen.append(gm)
            remaining -= self._covered_tags(gm, tags)
        pool = [e for e in entries if e.get("id") != "gran-mestre"]
        while remaining:
            best = None
            best_new = set()
            for entry in pool:
                if entry in chosen:
                    continue
                new = self._covered_tags(entry, tags) & remaining
                if len(new) > len(best_new):
                    best, best_new = entry, new
            if best is None or not best_new:
                break
            chosen.append(best)
            remaining -= best_new
        result = [self._cover_item(entry, tags) for entry in chosen]
        result.sort(key=lambda item: item["score"], reverse=True)
        if force_gm and result and result[0]["id"] != "gran-mestre":
            gm_item = next((i for i in result if i["id"] == "gran-mestre"), None)
            if gm_item:
                result.remove(gm_item)
                result.insert(0, gm_item)
        return result

    def _cover_item(self, entry: dict, tags: Dict[str, str]) -> dict:
        """Build a cover result entry for one agent."""
        covered = self._covered_tags(entry, tags)
        return {
            "id": entry.get("id", "?"),
            "model": self.model_for(entry.get("id", "")),
            "covered_tags": sorted(covered),
            "score": round(len(covered) / len(tags), 2) if tags else 0.0,
        }

    def _covered_tags(self, entry: dict, tags: Dict[str, str]) -> set:
        """Return the demand tag keys covered by one registry entry."""
        caps = entry.get("capacidades") or []
        if not isinstance(caps, list):
            caps = []
        text_parts = list(caps)
        for field in ("nome", "proposito"):
            value = entry.get(field)
            if value:
                text_parts.append(str(value))
        return self._covered_keys(text_parts, tags)

    @classmethod
    def _covered_keys(cls, text_parts: List[str], tags: Dict[str, str]) -> set:
        """Return demand tag keys whose keywords appear in the agent text."""
        text = _norm(" ".join(str(p) for p in text_parts))
        covered = set()
        for key, value in tags.items():
            keywords = cls.TAG_KEYWORDS.get(key, [])
            if any(kw in text for kw in keywords):
                covered.add(key)
            elif value and value != "true" and _norm(str(value)) in text:
                covered.add(key)
        return covered
