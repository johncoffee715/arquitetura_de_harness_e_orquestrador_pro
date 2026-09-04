"""Dynamic Scaffold Engine for the Gran-Mestre harness.

Selects the "arsenal" — subagents, skills, MCPs, GBNF grammars and execution
modes — per task, by crossing *demand* (task complexity + demand tags) with
*offer* (available model VRAM / slots / capabilities).

WS-G (harness integration) usage
--------------------------------
The harness imports this module and asks for a plan before spawning work:

    from harness.core.scaffold import ArsenalScaffold

    scaffold = ArsenalScaffold()                      # reads the 3 config files
    plan = scaffold.plan(task, demand_tags,           # demand side
                         complexity="complex",        # trivial|simple|medium|complex|critical
                         vram_gb=scaffold.available_vram())   # offer side

    # Harness then uses plan to drive execution:
    for wave in range(plan.waves):                    # parallel waves
        for agent_id in plan.agents:                  # fresh subagent per task
            spawn(agent_id, slots=plan.slots, ctx=plan.ctx)
    if plan.grammar:                                  # GBNF-constrained sampling
        serve(model, grammar=plan.grammar)
    run(mode=plan.mode, debate_group=plan.debate_group)

The `route` field mirrors `mode` so a single field can be fed straight into
the observability layer (Phase/Route metrics) without remapping.

Design notes
------------
- Pure Python stdlib. No external dependencies.
- Offer x demand: subagents/skills/MCPs are scored with a simple TF-style
  token matcher (demand tokens vs. registry description tokens, light
  suffix-stemming, name boost). Top-3 agents, top-3 skills, top-2 MCPs.
- VRAM-aware budgeting: >=24GB -> ctx 16384 / slots 4; >=10GB -> ctx 4096 /
  slots 2 (Bonsai-27B-1bit profile); <10GB -> ctx 2048 / slots 1 (Bonsai
  dropped to a single slot).
- Mode routing: trivial/simple -> sequential; medium -> parallel (waves 2-3)
  or rag when retrieval is needed; complex/critical -> hierarchical, or
  debate when divergence risk is flagged; retrieval demand can force rag.
"""

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# --------------------------------------------------------------------------
# Public data contract
# --------------------------------------------------------------------------

@dataclass
class ArsenalPlan:
    """Execution blueprint returned by the Dynamic Scaffold Engine.

    Attributes:
        agents:       subagent ids from the registry (top-3 by TF score)
        skills:       skill ids from the registry (top-3 by TF score)
        mcps:         enabled MCP server names from the registry (top-2)
        mode:         sequential | parallel | debate | rag | hierarchical
        waves:        number of parallel waves if mode == parallel
        debate_group: group id to route debaters to, if mode == debate
        ctx:          recommended context window (tokens) for the workers
        slots:        recommended number of parallel inference slots
        grammar:      GBNF grammar file name, or None for free-form output
        route:        mirrors `mode` (observability-friendly)
        reason:       human-readable justification of every decision
    """

    agents: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    mcps: List[str] = field(default_factory=list)
    mode: str = "sequential"
    waves: int = 1
    debate_group: str = ""
    ctx: int = 4096
    slots: int = 2
    grammar: Optional[str] = None
    route: str = "sequential"
    reason: str = ""

    def __str__(self) -> str:  # compact, selfcheck-friendly rendering
        parts = [
            f"mode={self.mode}",
            f"waves={self.waves}",
            f"agents={self.agents or '—'}",
            f"skills={self.skills or '—'}",
            f"mcps={self.mcps or '—'}",
            f"ctx={self.ctx}",
            f"slots={self.slots}",
            f"grammar={self.grammar or 'none'}",
        ]
        if self.mode == "debate":
            parts.append(f"debate_group={self.debate_group}")
        header = " | ".join(parts)
        return f"{header}\n    reason: {self.reason}"


# --------------------------------------------------------------------------
# Small matching helpers (pure stdlib)
# --------------------------------------------------------------------------

_STOP = frozenset({
    "a", "an", "and", "as", "at", "by", "de", "do", "da", "das", "dos", "e",
    "em", "for", "from", "in", "into", "na", "no", "o", "of", "on", "or",
    "para", "per", "por", "que", "the", "to", "via", "with", "é",
})


def _tokens(text: str) -> List[str]:
    """Lowercased alphanumeric tokens, stopwords removed."""
    return [t for t in re.findall(r"[a-z0-9]+", (text or "").lower())
            if t not in _STOP]


def _stem(token: str) -> str:
    """Light suffix-stripping so 'executes'/'execution'/'executor' collide."""
    if len(token) > 5 and token.endswith("ing"):
        return token[:-3]
    if len(token) > 4 and token.endswith("ies"):
        return token[:-3] + "y"
    if len(token) > 3 and token.endswith("es"):
        return token[:-2]
    if len(token) > 4 and token.endswith("ed"):
        return token[:-2]
    if len(token) > 3 and token.endswith("s"):
        return token[:-1]
    return token


def _tf_score(demand_tokens: List[str], hay_tokens: List[str]) -> float:
    """TF-style score: how often demand stems appear in the haystack.

    A match is a stem equality or a shared prefix of >=3 chars (either
    direction), so 'execut' hits 'executes', 'execution' and 'executor'.
    """
    d_stems = [_stem(t) for t in demand_tokens if len(_stem(t)) >= 3]
    h_stems = [_stem(t) for t in hay_tokens]
    score = 0.0
    for ds in d_stems:
        for hs in h_stems:
            if hs == ds or (len(hs) >= 3 and (hs.startswith(ds) or ds.startswith(hs))):
                score += 1.0
    return score


def _demand_tokens(task: str, demand_tags: Optional[Dict[str, Any]]) -> List[str]:
    """Flatten task text + demand_tags into one token stream for matching."""
    tokens: List[str] = _tokens(task)
    tags = demand_tags or {}
    tags_list = tags.get("tags") or []
    if isinstance(tags_list, str):
        tags_list = [tags_list]
    for t in tags_list:
        tokens.extend(_tokens(str(t)))
    for key in ("phase", "domain", "goal"):
        val = tags.get(key)
        if isinstance(val, str):
            tokens.extend(_tokens(val))
    return tokens


# Curated tag->skill fallback for when descriptions are too thin to match.
_CURATED_SKILLS: Dict[str, List[str]] = {
    "security": ["gsd-secure-phase"],
    "debug": ["gsd-debug"],
    "test": ["gsd-add-tests"],
    "ui": ["gsd-ui-phase", "gsd-ui-review"],
    "plan": ["gsd-plan-phase"],
    "review": ["gsd-code-review"],
    "research": ["gsd-spike"],
    "memory": ["ck"],
    "rag": ["graphify"],
    "execute": ["gsd-execute-phase"],
    "git": ["gsd-ship"],
}


class ArsenalScaffold:
    """Selects arsenal features per task by crossing demand and offer."""

    #: complexity levels the harness emits (from ContextAnalyzer / DevLoop)
    COMPLEXITIES = ("trivial", "simple", "medium", "complex", "critical")
    MODES = ("sequential", "parallel", "debate", "rag", "hierarchical")

    def __init__(self,
                 registry_path: str = "/mnt/dados/Assistente Pessoal/harness/registry.json",
                 policies_path: str = "/mnt/dados/Assistente Pessoal/harness/policies.json",
                 config_path: str = "/mnt/dados/Assistente Pessoal/harness/harness-config.json"):
        self.registry_path = Path(registry_path)
        self.policies_path = Path(policies_path)
        self.config_path = Path(config_path)
        self.registry: Dict[str, Any] = self._load_json(self.registry_path)
        self.policies: Dict[str, Any] = self._load_json(self.policies_path)
        self.config: Dict[str, Any] = self._load_json(self.config_path)

    # -- loading -----------------------------------------------------------

    @staticmethod
    def _load_json(path: Path) -> Dict[str, Any]:
        """Read a JSON file; return {} on any failure (never crash the plan)."""
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return data if isinstance(data, dict) else {}
        except (OSError, ValueError):
            return {}

    # -- offer side: VRAM --------------------------------------------------

    def available_vram(self) -> float:
        """Probe usable GPU VRAM in GB (rocm-smi first, then nvidia-smi).

        Falls back to the harness-config `hardware.gpu.vram_gb` value, then
        to 16.0 GB (the MI50 HBM2 budget) if nothing can be probed.
        """
        gb = self._probe_rocm_smi()
        if gb is None:
            gb = self._probe_nvidia_smi()
        if gb is None or not (2.0 <= gb <= 512.0):
            gb = float(self.config.get("harness", {})
                       .get("hardware", {})
                       .get("gpu", {})
                       .get("vram_gb", 0) or 0)
        if gb <= 0:
            gb = 16.0
        return round(gb, 1)

    @staticmethod
    def _probe_rocm_smi() -> Optional[float]:
        """rocm-smi --showmeminfo vram -> total VRAM in GB (JSON or text)."""
        try:
            out = subprocess.run(
                ["rocm-smi", "--showmeminfo", "vram", "--json"],
                capture_output=True, text=True, timeout=10,
            ).stdout
            data = json.loads(out)
            totals = [float(card["VRAM Total Memory (MB)"])
                      for card in data.values()
                      if card.get("VRAM Total Memory (MB)")]
            if totals:
                return max(totals) / 1024.0
        except (OSError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired):
            pass
        # text-mode fallback: "GPU[0] : 16368 MiB used, 0 MiB reserved, 16368 MiB total"
        try:
            out = subprocess.run(
                ["rocm-smi", "--showmeminfo", "vram"],
                capture_output=True, text=True, timeout=10,
            ).stdout
            for line in out.splitlines():
                m = re.search(
                    r"(\d+)\s*MiB\s+used,\s*\d+\s*MiB\s+reserved,\s*(\d+)\s*MiB\s+total",
                    line)
                if m:
                    return float(m.group(2)) / 1024.0
        except (OSError, subprocess.TimeoutExpired):
            pass
        return None

    @staticmethod
    def _probe_nvidia_smi() -> Optional[float]:
        """nvidia-smi memory.total (MiB) -> GB."""
        try:
            out = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.total",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=10,
            ).stdout
            values = [float(v) for v in out.split() if v.replace(".", "").isdigit()]
            if values:
                return max(values) / 1024.0
        except (OSError, subprocess.TimeoutExpired):
            pass
        return None

    @staticmethod
    def _budget(vram_gb: float) -> Tuple[int, int]:
        """VRAM-aware ctx/slots budget.

        >=24GB -> ctx 16384, slots 4+  (wide parallel windows)
        >=10GB -> ctx 4096,  slots 2   (Bonsai-27B-1bit profile @ 16GB)
         <10GB -> ctx 2048,  slots 1   (Bonsai dropped to a single slot)
        """
        if vram_gb >= 24.0:
            return 16384, 4
        if vram_gb >= 10.0:
            return 4096, 2
        return 2048, 1

    # -- demand side: mode -------------------------------------------------

    @staticmethod
    def _mode_for_complexity(complexity: str) -> str:
        c = (complexity or "").lower()
        if c in ("trivial", "simple"):
            return "sequential"
        if c in ("complex", "critical"):
            return "hierarchical"
        return "parallel"

    def _select_mode(self, complexity: str, demand_tags: Dict[str, Any],
                     task: str) -> Tuple[str, int, str]:
        c = (complexity or "medium").lower()
        tl = task.lower()
        divergence = bool(demand_tags.get("divergence")) or any(
            w in tl for w in ("ambiguous", "diverg", "controv", "uncertain", "risco"))
        retrieval = bool(demand_tags.get("retrieval")) or any(
            w in tl for w in ("search", "lookup", "find", "retriev",
                              "consult", "document", "pesquis", "busc"))

        if c in ("trivial", "simple"):
            return "sequential", 1, "trivial/simple — sequential ReAct, no waves"
        if c in ("complex", "critical"):
            if divergence:
                return "debate", 1, \
                    "complex/critical with divergence risk — debate adjudicates the split"
            if retrieval:
                return "hierarchical", 1, \
                    "complex/critical — gran_mestre orchestrates sub-orchestrators (RAG included)"
            return "hierarchical", 1, \
                "complex/critical — gran_mestre orchestrates sub-orchestrators"
        # medium
        if divergence:
            return "debate", 1, "medium with divergence risk — debate group"
        if retrieval:
            return "rag", 1, "medium with retrieval needs — RAG over context store"
        return "parallel", 2, "medium — parallel waves"

    # -- grammar -----------------------------------------------------------

    def select_grammar(self, complexity: str) -> Optional[str]:
        """GBNF grammar by complexity: code/math -> code.gbnf, else None."""
        c = (complexity or "").lower()
        if c in ("medium", "complex", "critical"):
            return "code.gbnf"
        return None

    def _select_grammar(self, complexity: str, demand_tags: Dict[str, Any]) -> Optional[str]:
        """plan()-level grammar: demand tags first, then phase, then complexity."""
        tags = set(_tokens(" ".join(
            str(t) for t in (demand_tags.get("tags") or []))))
        json_words = {"json", "verdict", "compliance", "valid", "validation",
                      "validate", "filter", "schema"}
        code_words = {"code", "math", "coding", "implement", "execute",
                      "execution", "python"}
        phase = str(demand_tags.get("phase") or "").lower()
        if tags & json_words or phase in ("review", "deliver", "validate",
                                          "validation", "filter", "contract"):
            return "verdict.gbnf"
        if tags & code_words or phase in ("execute", "execution", "plan"):
            return "code.gbnf"
        return self.select_grammar(complexity)

    # -- offer x demand: resource scoring ----------------------------------

    def _score_entries(self, entries: List[Dict[str, Any]],
                       demand: List[str]) -> List[Tuple[float, str]]:
        """TF-score registry entries (subagents/skills) against demand tokens."""
        scored: List[Tuple[float, str]] = []
        for entry in entries:
            name = entry.get("name") or ""
            desc = entry.get("description") or ""
            if not desc.strip() or desc.strip() in (">-", ">-") or len(desc.strip()) < 5:
                continue
            hay = _tokens(desc) + _tokens(name)
            score = _tf_score(demand, hay)
            # name boost: a demand token present in the entry name is a strong signal
            name_tokens = {_stem(t) for t in _tokens(name)}
            for dt in demand:
                if _stem(dt) in name_tokens:
                    score += 2.0
            if score > 0:
                scored.append((score, name))
        scored.sort(key=lambda pair: (-pair[0], pair[1]))
        return scored

    def _select_agents(self, task: str, demand_tags: Dict[str, Any]) -> List[str]:
        demand = _demand_tokens(task, demand_tags)
        scored = self._score_entries(self.registry.get("subagents") or [], demand)
        agents = [name for _, name in scored[:3]]
        if not agents:
            # No description matched: fall back to the generic executor set.
            agents = ["gsd-executor", "gsd-code-reviewer"]
        return agents

    def _select_skills(self, task: str, demand_tags: Dict[str, Any]) -> List[str]:
        demand = _demand_tokens(task, demand_tags)
        scored = self._score_entries(self.registry.get("skills") or [], demand)
        skills = [name for _, name in scored[:3]]
        if not skills:
            # Curated fallback driven by explicit demand tags.
            for tag in demand_tags.get("tags") or []:
                skills.extend(_CURATED_SKILLS.get(str(tag).lower(), []))
            skills = skills[:3]
        return skills

    def _select_mcps(self, task: str, demand_tags: Dict[str, Any]) -> List[str]:
        demand = _demand_tokens(task, demand_tags)
        enabled = [m for m in (self.registry.get("mcp") or [])
                   if m.get("enabled", True)]
        scored = self._score_entries(enabled, demand)
        return [name for _, name in scored[:2]]

    # -- public API --------------------------------------------------------

    def plan(self, task: str, demand_tags: Dict[str, Any],
             complexity: str, vram_gb: float) -> ArsenalPlan:
        """Compute the arsenal blueprint for a task.

        Args:
            task:          raw task description
            demand_tags:   e.g. {"tags": ["mcp", "jwt"], "phase": "execute",
                                 "divergence": True, "retrieval": True}
            complexity:    trivial | simple | medium | complex | critical
            vram_gb:       available GPU VRAM (offer side); <=0 probes at runtime
        """
        if not isinstance(demand_tags, dict):
            demand_tags = {}
        if not vram_gb or vram_gb <= 0:
            vram_gb = self.available_vram()

        ctx, slots = self._budget(vram_gb)
        mode, waves, mode_reason = self._select_mode(complexity, demand_tags, task)
        if mode == "parallel":
            waves = 3 if vram_gb >= 24.0 else 2

        grammar = self._select_grammar(complexity, demand_tags)
        agents = self._select_agents(task, demand_tags)
        skills = self._select_skills(task, demand_tags)
        mcps = self._select_mcps(task, demand_tags)

        debate_group = ""
        if mode == "debate":
            digest = hashlib.sha1(task.encode("utf-8")).hexdigest()[:8]
            debate_group = f"grp-{digest}"

        reason = "; ".join(filter(None, [
            mode_reason,
            f"agents: {', '.join(agents)}",
            f"VRAM {vram_gb}GB -> ctx {ctx}, slots {slots}",
            f"grammar {grammar}" if grammar else "grammar: free-form",
        ]))

        return ArsenalPlan(
            agents=agents,
            skills=skills,
            mcps=mcps,
            mode=mode,
            waves=waves,
            debate_group=debate_group,
            ctx=ctx,
            slots=slots,
            grammar=grammar,
            route=mode,
            reason=reason,
        )

    @staticmethod
    def offer(capabilities: Dict[str, float]) -> ArsenalPlan:
        """Static helper: plan from a raw capabilities dict, no registry.

        Accepts keys: vram_gb, complexity (or mode_hint), tags. Used for
        quick offer-only sanity checks; `plan()` is the real entry point.
        """
        vram = float(capabilities.get("vram_gb", 0) or 0)
        if vram >= 24.0:
            ctx, slots = 16384, 4
        elif vram >= 10.0:
            ctx, slots = 4096, 2
        else:
            ctx, slots = 2048, 1

        complexity = str(capabilities.get("complexity", "") or "").lower()
        mode = str(capabilities.get("mode_hint") or
                   ArsenalScaffold._mode_for_complexity(complexity))
        if mode not in ArsenalScaffold.MODES:
            mode = "sequential"
        grammar = ArsenalScaffold._offer_grammar(complexity, capabilities)
        waves = 3 if mode == "parallel" and vram >= 24.0 else (2 if mode == "parallel" else 1)
        reason = (f"static offer: {vram}GB -> ctx {ctx}, slots {slots}, "
                  f"mode {mode}, grammar {grammar or 'none'}")
        return ArsenalPlan(mode=mode, waves=waves, ctx=ctx, slots=slots,
                           grammar=grammar, route=mode, reason=reason)

    @staticmethod
    def _offer_grammar(complexity: str, capabilities: Dict[str, Any]) -> Optional[str]:
        json_words = {"json", "verdict", "compliance", "valid", "validate",
                      "validation", "filter", "schema"}
        code_words = {"code", "math", "coding", "implement", "execute", "python"}
        tags = {str(t).lower() for t in (capabilities.get("tags") or [])}
        if tags & json_words:
            return "verdict.gbnf"
        if tags & code_words or complexity in ("medium", "complex", "critical"):
            return "code.gbnf"
        return None

    # -- selfcheck ---------------------------------------------------------

    def selfcheck(self) -> str:
        """Offline sanity check against the real registry files (no network).

        Prints registry inventory, the VRAM probe result and a sample plan
        for the canonical "MCP server PostgreSQL JWT rate limit" task.
        Returns a short status string.
        """
        lines = ["ArsenalScaffold selfcheck"]
        lines.append(f"  registry.json : "
                     f"{len(self.registry.get('subagents', []))} subagents | "
                     f"{len(self.registry.get('skills', []))} skills | "
                     f"{len(self.registry.get('mcp', []))} mcps | "
                     f"{len(self.registry.get('lsp', []))} lsps")
        lines.append(f"  policies.json : "
                     f"rbac={self.policies.get('policies', {}).get('rbac', {}).get('enabled')} "
                     f"| cloud.moe_only_on_phases="
                     f"{self.policies.get('policies', {}).get('cloud', {}).get('moe_only_on_phases')}")
        models = self.config.get("harness", {}).get("models", {})
        lines.append("  harness-config : " + ", ".join(
            f"{k}={v.get('vram_gb', '?')}GB" for k, v in models.items()))

        vram = self.available_vram()
        lines.append(f"  available_vram(): {vram} GB")

        task = "MCP server PostgreSQL JWT rate limit"
        demand_tags = {
            "tags": ["mcp", "server", "postgresql", "jwt", "rate", "limit",
                     "execution", "coding", "security"],
            "phase": "execute",
        }
        plan = self.plan(task, demand_tags, "medium", vram)
        lines.append(f"  sample plan for {task!r}:")
        lines.append("    " + str(plan).replace("\n", "\n    "))

        for line in lines:
            print(line)
        return "selfcheck OK"


if __name__ == "__main__":
    import sys
    sys.exit(0 if ArsenalScaffold().selfcheck() == "selfcheck OK" else 1)
