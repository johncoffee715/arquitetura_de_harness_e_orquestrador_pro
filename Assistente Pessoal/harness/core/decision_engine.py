from typing import Any, Dict


class DecisionEngine:
    """Resolves final routing: per-phase models, overrides, hooks and fallback."""

    PHASE_MODELS = {
        "planning": "local-nanbeige/nanbeige-3b",
        "implementation": "local-nanbeige/nanbeige-3b",
        "testing": "local-nanbeige/nanbeige-3b",
        "docs": "local-nanbeige/nanbeige-3b",
    }
    HOOK_MODEL = "local-lfm/lfm-2.5-1.6b"
    BONSAI = "local-bonsai/bonsai-27b"
    CLOUD_FALLBACK = "opencode/glm-5.2"
    MATH_KEYWORDS = (
        "math", "calcul", "calculo", "equa", "derivad", "integral",
        "simula", "statistic", "estatist", "quantum", "numerical",
        "numerico", "algebra",
    )

    def __init__(self, model_provider: Any):
        self.model_provider = model_provider

    def decide(self, demand, cover: list) -> Dict:
        """Build the routing decision for a demand + agent cover."""
        tags = demand.tags or {}
        complexity = demand.complexity
        phases = list(demand.phases or [])

        phase_model: Dict[str, str] = {}
        overrides: Dict[str, str] = {}
        hooks: list = []
        fallback: Dict = {}

        for phase in phases:
            model = self.PHASE_MODELS.get(phase, self.PHASE_MODELS["planning"])
            if phase == "implementation":
                override = self._implementation_override(demand, tags, complexity)
                if override:
                    overrides["implementation"] = override
                    model = override
            phase_model[phase] = model

        if "implementation" in phases and overrides.get("implementation") == self.BONSAI:
            if not self._bonsai_online():
                fallback = {"provider": self.CLOUD_FALLBACK, "redflag": True}
                phase_model["implementation"] = self.CLOUD_FALLBACK

        hooks.append(self.HOOK_MODEL)
        return {
            "demand": demand.raw,
            "complexity": complexity,
            "phases": phases,
            "phase_model": phase_model,
            "overrides": overrides,
            "hooks": hooks,
            "fallback": fallback,
            "cover": cover,
        }

    def _implementation_override(self, demand, tags: Dict[str, str],
                                 complexity: str) -> str:
        """Decide whether implementation should move to bonsai-27b."""
        if "auth" in tags and tags["auth"] == "jwt":
            return self.BONSAI
        raw = (demand.raw or "").lower()
        if any(kw in raw for kw in self.MATH_KEYWORDS):
            return self.BONSAI
        if "coding" in tags and complexity in ("COMPLEX", "CRITICAL"):
            return self.BONSAI
        return ""

    def _bonsai_online(self) -> bool:
        """Probe the heavy-execution endpoint; any failure means offline."""
        try:
            endpoint = self.model_provider._derive_endpoint("heavy_execution")
            return bool(self.model_provider._probe_endpoint(endpoint))
        except Exception:
            return False

    def summarize(self, decision: Dict) -> str:
        """Compact pt-BR summary of a decision."""
        lines = [
            f"Complexidade: {decision['complexity']}",
            f"Fases: {', '.join(decision['phases'])}",
        ]
        for phase, model in decision["phase_model"].items():
            lines.append(f"{phase} -> {model}")
        if decision["overrides"]:
            lines.append("Overrides: " + "; ".join(
                f"{p}->{m}" for p, m in decision["overrides"].items()))
        lines.append("Hooks: " + ", ".join(decision["hooks"]))
        if decision["fallback"]:
            fb = decision["fallback"]
            lines.append(f"Fallback: {fb['provider']} (redflag={fb['redflag']})")
        return "\n".join(lines)
