"""Global Context Compaction for the Gran-Mestre orchestrator.

Preserves the orchestrator's context at each token window by performing an
automatic, GLOBAL compact + clear, implemented once in the harness core so
every phase, Dev Loop level and model benefits.

The 4 hard requirements (user-mandated):
1. TRIGGER THRESHOLD  — start compaction at 75%..85% of the model's max tokens
   (``trigger_ratio_min`` / ``trigger_ratio_max``; ``>= max`` -> critical).
2. STATE PRESERVATION — never wipe: emit a structured summary with task
   intent / current progress / next steps that heads the new active prompt.
3. OFFLOAD           — save the RAW history to ``/conversation_history/{id}.md``
   (persistent, append-only windows) BEFORE clearing working memory; falls back
   to ``<project>/harness/conversation_history/`` when the primary is unwritable.
4. RECENT RETENTION   — keep the last 10%..20% of tokens intact in the active
   prompt after the summary so tool calls/instructions continue seamlessly.

This module is COMPLEMENTARY to ``harness.memory.context_memory.CollectiveMemory``
(the structured RAG/SQLite index). The compactor owns the raw-history offload,
the compaction decision and the summary rendering; CollectiveMemory stays the
searchable memory index.

Stdlib-only (no third-party deps). Deterministic, dependency-free token
estimation: ``chars // 4 + 1`` — a documented proxy until real provider token
counts are available. Thread-safe via ``threading.RLock``; event log is
append-only JSONL at ``harness/metrics/compaction-events.jsonl``.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# constants / defaults
# ---------------------------------------------------------------------------
DEFAULT_TRIGGER_MIN = 0.75
DEFAULT_TRIGGER_MAX = 0.85
DEFAULT_RETAIN_MIN = 0.10
DEFAULT_RETAIN_MAX = 0.20
DEFAULT_RETAIN = 0.15
DEFAULT_MAX_CONTEXT = 8192
DEFAULT_OFFLOAD_DIR = "/conversation_history"
FALLBACK_DIR_NAME = "conversation_history"
EVENTS_FILENAME = "compaction-events.jsonl"


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# data structures
# ---------------------------------------------------------------------------
@dataclass
class CompactionPlan:
    """Decision record produced by :meth:`ContextCompactor.check` (no side effects
    beyond one ``track`` event)."""

    thread_id: str
    model: str
    used_tokens: int
    max_tokens: int
    ratio: float
    trigger: str  # 'none' | 'normal' | 'critical'
    reason: str
    retained_tokens: int = 0


@dataclass
class CompactionResult:
    """Outcome of :meth:`ContextCompactor.compact`."""

    thread_id: str
    model: str
    used_tokens: int
    max_tokens: int
    ratio_before: float
    ratio_after: float
    trigger: str
    dropped_tokens: int
    retained_tokens: int
    summary_tokens: int
    new_prompt: str
    offload_path: str
    summary: str
    created_at: str = field(default_factory=_utcnow)


# ---------------------------------------------------------------------------
# compactor
# ---------------------------------------------------------------------------
class ContextCompactor:
    """Global context compactor for the harness.

    Loads configuration from ``<project>/harness/harness-config.json`` →
    ``harness.context_compaction`` (graceful defaults when absent). Resolves the
    offload directory at construction, falling back to the project path when the
    primary ``/conversation_history`` is not writable.
    """

    def __init__(
        self,
        project_root: str = "/mnt/dados",
        config_path: Optional[str] = None,
        offload_dir: Optional[str] = None,
    ) -> None:
        self.project_root = Path(project_root)
        self.lock = threading.RLock()

        cfg: Dict[str, Any] = {}
        cfg_path = Path(config_path) if config_path else self.project_root / "harness" / "harness-config.json"
        if cfg_path.is_file():
            try:
                cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                cfg = {}

        b = (cfg.get("harness", {}) or {}).get("context_compaction", {}) or {}
        self.enabled = bool(b.get("enabled", True))
        self.trigger_ratio_min = float(b.get("trigger_ratio_min", DEFAULT_TRIGGER_MIN))
        self.trigger_ratio_max = float(b.get("trigger_ratio_max", DEFAULT_TRIGGER_MAX))
        self.retain_ratio_min = float(b.get("retain_ratio_min", DEFAULT_RETAIN_MIN))
        self.retain_ratio_max = float(b.get("retain_ratio_max", DEFAULT_RETAIN_MAX))
        raw_retain = float(b.get("retain_ratio", DEFAULT_RETAIN))
        self.retain_ratio = max(self.retain_ratio_min, min(raw_retain, self.retain_ratio_max))

        # per-model max_context overrides: {id: int}
        model_overrides: Dict[str, int] = {}
        for mid, mval in (b.get("models", {}) or {}).items():
            if isinstance(mval, dict):
                model_overrides[mid] = int(mval.get("max_context", DEFAULT_MAX_CONTEXT))
            else:
                try:
                    model_overrides[mid] = int(mval)
                except (TypeError, ValueError):
                    pass
        self.model_overrides = model_overrides

        # fallback source: harness.models (name-keyed config)
        self.models_config = cfg.get("harness", {}).get("models", {}) or {}

        # -- offload dir resolution ------------------------------------
        candidate = offload_dir or b.get("offload_dir") or DEFAULT_OFFLOAD_DIR
        try:
            Path(candidate).mkdir(parents=True, exist_ok=True)
            if os.access(str(candidate), os.W_OK):
                self.offload_dir_effective = Path(candidate)
            else:
                self.offload_dir_effective = self._fallback_dir()
        except OSError:
            self.offload_dir_effective = self._fallback_dir()

        self.events_path = Path(self.project_root) / "harness" / "metrics" / EVENTS_FILENAME
        try:
            self.events_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass

    def _fallback_dir(self) -> Path:
        path = self.project_root / "harness" / FALLBACK_DIR_NAME
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
        return path

    # ------------------------------------------------------------------
    # token estimation
    # ------------------------------------------------------------------
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Deterministic, dependency-free token proxy (``chars//4 + 1``)."""
        if not text or not text.strip():
            return 0
        return len(text) // 4 + 1

    def model_max_context(self, model_id: str) -> int:
        """Return max context for a model id (override -> harness.models -> default)."""
        override = self.model_overrides.get(model_id)
        if override is not None:
            return override
        entry = self.models_config.get(model_id)
        if isinstance(entry, dict):
            mc = entry.get("max_context")
            if isinstance(mc, int):
                return mc
        return DEFAULT_MAX_CONTEXT

    def _effective_retain_ratio(self) -> float:
        return self.retain_ratio

    def _trigger_for(self, ratio: float) -> str:
        if ratio >= self.trigger_ratio_max:
            return "critical"
        if ratio >= self.trigger_ratio_min:
            return "normal"
        return "none"

    # ------------------------------------------------------------------
    # observable event log (append-only, never raises)
    # ------------------------------------------------------------------
    def _emit(self, event: Dict[str, Any]) -> None:
        try:
            with self.lock:
                with open(self.events_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(event, ensure_ascii=False) + "\n")
        except Exception as exc:  # pragma: no cover - defensive
            print(f"[Compaction] warning: falha ao logar evento: {exc}")

    # ------------------------------------------------------------------
    # decision
    # ------------------------------------------------------------------
    def check(self, thread_id: str, model: str, used_tokens: int) -> CompactionPlan:
        """Decision only (plus one ``track`` event). Returns a plan with
        ``trigger`` in {'none','normal','critical'}."""
        max_tokens = self.model_max_context(model)
        ratio = round(used_tokens / max_tokens, 4) if max_tokens > 0 else 0.0
        if not self.enabled or used_tokens <= 0:
            trigger, reason = "none", "desabilitado ou sem tokens"
        else:
            trigger = self._trigger_for(ratio)
            reason = f"used {used_tokens}/{max_tokens} ({ratio:.1%})"
        plan = CompactionPlan(
            thread_id=thread_id, model=model, used_tokens=used_tokens,
            max_tokens=max_tokens, ratio=ratio, trigger=trigger, reason=reason,
        )
        self._emit({
            "event": "track", "thread_id": thread_id, "model": model,
            "used_tokens": used_tokens, "max_tokens": max_tokens,
            "ratio": ratio, "trigger": trigger, "offload_path": None,
        })
        return plan

    # ------------------------------------------------------------------
    # compaction pipeline
    # ------------------------------------------------------------------
    def _build_summary(
        self, thread_id: str, model: str, max_tokens: int, used_tokens: int,
        trigger: str, task_intent: str, progress: str, next_steps: str,
    ) -> str:
        intent = task_intent.strip() or "(não informado)"
        prog = progress.strip() or "(não informado)"
        nxt = next_steps.strip() or "(não informado)"
        return (
            f"# Compaction Summary — {thread_id}\n"
            f"model: {model} | max_context: {max_tokens} | used: {used_tokens} "
            f"| trigger: {trigger} | created_at: {_utcnow()}\n\n"
            f"## Intenção da Tarefa\n{intent}\n\n"
            f"## Progresso Atual\n{prog}\n\n"
            f"## Próximos Passos\n{nxt}\n"
        )

    def offload_history(
        self, thread_id: str, history: str, summary: str = "", trigger: str = "none",
        model: str = "", ratio: float = 0.0,
    ) -> str:
        """Append a timestamped window (summary + raw history) to the offload file."""
        path = self.offload_dir_effective / f"{thread_id}.md"
        max_tokens = self.model_max_context(model)
        with self.lock:
            if not path.exists():
                path.write_text(
                    f"# Conversational History — {thread_id}\n"
                    f"model: {model}\nmax_context: {max_tokens}\n",
                    encoding="utf-8",
                )
            with open(path, "a", encoding="utf-8") as f:
                f.write(
                    f"\n## Window {_utcnow()} (trigger {trigger}, ratio {ratio})\n"
                    f"{summary}\n"
                    f"### Raw History (begin)\n{history}\n### Raw History (end)\n"
                )
        return str(path)

    def _retain_tail(self, history: str, retained_tokens: int) -> str:
        if not history or retained_tokens <= 0:
            return ""
        # walk back from the end accumulating chars until the estimate >= target
        n = len(history)
        for i in range(n, 0, -1):
            chunk = history[i - 1:]
            if self.estimate_tokens(chunk) >= retained_tokens or i <= max(1, n - retained_tokens * 4):
                return chunk
        return history

    def compact(
        self, thread_id: str, model: str, history: str, used_tokens: int, *,
        task_intent: str = "", progress: str = "", next_steps: str = "",
    ) -> CompactionResult:
        """Full compaction cycle, strict order: summary -> offload -> retain -> prompt."""
        max_tokens = self.model_max_context(model)
        ratio_before = round(used_tokens / max_tokens, 4) if max_tokens > 0 else 0.0
        trigger = self._trigger_for(ratio_before)

        if trigger == "none":
            self._emit({
                "event": "compact", "thread_id": thread_id, "model": model,
                "used_tokens": used_tokens, "max_tokens": max_tokens,
                "ratio": ratio_before, "trigger": trigger, "offload_path": None,
            })
            return CompactionResult(
                thread_id=thread_id, model=model, used_tokens=used_tokens,
                max_tokens=max_tokens, ratio_before=ratio_before,
                ratio_after=ratio_before, trigger=trigger, dropped_tokens=0,
                retained_tokens=0, summary_tokens=0, new_prompt=history or "",
                offload_path="", summary="", created_at=_utcnow(),
            )

        summary = self._build_summary(
            thread_id, model, max_tokens, used_tokens, trigger,
            task_intent, progress, next_steps,
        )
        offload_path = self.offload_history(
            thread_id, history, summary=summary, trigger=trigger, model=model,
            ratio=ratio_before,
        )
        target = int(max_tokens * self._effective_retain_ratio())
        retained_tokens = min(target, used_tokens)
        retained_tail = self._retain_tail(history, retained_tokens)
        new_prompt = self.render_prompt(summary, retained_tail)
        dropped_tokens = max(0, used_tokens - retained_tokens)
        ratio_after = round(retained_tokens / max_tokens, 4) if max_tokens > 0 else 0.0
        summary_tokens = self.estimate_tokens(summary)

        self._emit({
            "event": "compact", "thread_id": thread_id, "model": model,
            "used_tokens": used_tokens, "max_tokens": max_tokens,
            "ratio": ratio_before, "trigger": trigger, "offload_path": offload_path,
        })
        return CompactionResult(
            thread_id=thread_id, model=model, used_tokens=used_tokens,
            max_tokens=max_tokens, ratio_before=ratio_before,
            ratio_after=ratio_after, trigger=trigger, dropped_tokens=dropped_tokens,
            retained_tokens=retained_tokens, summary_tokens=summary_tokens,
            new_prompt=new_prompt, offload_path=offload_path, summary=summary,
            created_at=_utcnow(),
        )

    # ------------------------------------------------------------------
    # helpers / read-back
    # ------------------------------------------------------------------
    def render_prompt(self, summary: str, retained_tail: str) -> str:
        return f"{summary}\n---\n## Retained Recent Context (tail)\n{retained_tail}"

    def load_history(self, thread_id: str) -> str:
        path = self.offload_dir_effective / f"{thread_id}.md"
        if not path.is_file():
            return ""
        return path.read_text(encoding="utf-8")

    def events(self, since_iso: Optional[str] = None) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        if not self.events_path.is_file():
            return out
        with self.lock:
            try:
                lines = self.events_path.read_text(encoding="utf-8").splitlines()
            except OSError:
                return out
        for line in lines:
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if since_iso and rec.get("ts", "") < since_iso:
                continue
            out.append(rec)
        return out

    def status(self) -> Dict[str, Any]:
        ev = self.events()
        model_table = {}
        for mid in list(self.model_overrides.keys()) + [
            k for k in self.models_config.keys() if isinstance(self.models_config.get(k), dict)
        ]:
            try:
                model_table[mid] = self.model_max_context(mid)
            except Exception:
                continue
        return {
            "enabled": self.enabled,
            "offload_dir_effective": str(self.offload_dir_effective),
            "trigger_ratio_min": self.trigger_ratio_min,
            "trigger_ratio_max": self.trigger_ratio_max,
            "retain_ratio_min": self.retain_ratio_min,
            "retain_ratio_max": self.retain_ratio_max,
            "retain_ratio_effective": self._effective_retain_ratio(),
            "model_max_context": model_table,
            "events_total": len(ev),
            "compact_events": sum(1 for e in ev if e.get("event") == "compact"),
            "last_events": ev[-5:],
        }

    # ------------------------------------------------------------------
    # selfcheck (temp dir only — never touches production paths)
    # ------------------------------------------------------------------
    def selfcheck(self) -> Dict[str, Any]:
        tmp = Path(tempfile.mkdtemp(prefix="compaction_selfcheck_"))
        try:
            c = ContextCompactor(project_root=str(tmp), offload_dir=str(tmp / "hist"))
            checks: Dict[str, bool] = {
                "trigger_none_below_min": c._trigger_for(0.749) == "none",
                "trigger_normal_at_min": c._trigger_for(0.75) == "normal",
                "trigger_critical_at_max": c._trigger_for(0.85) == "critical",
                "estimate_empty": ContextCompactor.estimate_tokens("") == 0,
            }
            res = c.compact(
                thread_id="t", model="gran_mestre", history="line\n" * 2000,
                used_tokens=204800, task_intent="ditado pela teste",
                progress="exercício", next_steps="fim",
            )
            opath = Path(res.offload_path)
            checks["offload_exists"] = opath.is_file()
            checks["offload_has_window"] = "## Window" in (opath.read_text(encoding="utf-8") if opath.is_file() else "")
            checks["prompt_starts_summary"] = res.new_prompt.startswith("# Compaction Summary")
            checks["history_roundtrip"] = bool(c.load_history("t"))
            return {"ok": all(checks.values()), "checks": checks}
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ------------------------------------------------------------------
    # CLI
    # ------------------------------------------------------------------
    def _cli(self, argv: Optional[List[str]] = None) -> int:
        p = argparse.ArgumentParser(prog="harness.context.compaction",
                                    description="Global Context Compaction")
        sub = p.add_subparsers(dest="cmd")
        sp_c = sub.add_parser("check"); sp_c.add_argument("--model", required=True); sp_c.add_argument("--used", type=int, required=True)
        sub.add_parser("status")
        sub.add_parser("selfcheck")
        pd = sub.add_parser("compact-demo"); pd.add_argument("--thread", default="demo")
        args = p.parse_args(argv)

        if args.cmd == "check":
            plan = self.check(args.thread if hasattr(args, "thread") else "cli", args.model, args.used)
            print(json.dumps(vars(plan), ensure_ascii=False))
        elif args.cmd == "status":
            print(json.dumps(self.status(), indent=2, ensure_ascii=False))
        elif args.cmd == "selfcheck":
            print(json.dumps(self.selfcheck(), indent=2, ensure_ascii=False))
        elif args.cmd == "compact-demo":
            res = self.compact(
                args.thread, "gran_mestre", "linha de contexto demo\n" * 300, 204800,
                task_intent="demo", progress="0%", next_steps="fim",
            )
            print(res.new_prompt)
        else:
            p.print_help()
            return 2
        return 0


def main(argv: Optional[List[str]] = None) -> int:
    compactor = ContextCompactor()
    return compactor._cli(argv)


if __name__ == "__main__":
    sys.exit(main())
