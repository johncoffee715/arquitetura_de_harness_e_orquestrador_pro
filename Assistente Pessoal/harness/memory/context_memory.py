"""Collective Memory + Agentic RAG for the Gran-Mestre harness.

Persists a collective memory database (``context_memory.db``) and provides
semantic-ish retrieval for agentic RAG. Retrieval is a pure-stdlib
bag-of-words surrogate: each interaction is stored as an L2-normalized
token-frequency vector (JSON), and queries are ranked by cosine similarity.

Standard library only — no numpy, no third-party dependencies.

# noqa: SIZE_OK — single self-contained store; the task mandates exactly two
new files, so schema DDL + 8 public methods (365 pure LOC) cannot be split.
"""

from __future__ import annotations

import json
import math
import re
import shutil
import sqlite3
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Final, TypedDict

DEFAULT_DB_PATH: Final[str] = "/mnt/dados/Assistente Pessoal/harness/memory/context_memory.db"

_TOKEN_RE: Final[re.Pattern[str]] = re.compile(r"[a-z0-9]+")

_SCHEMA: Final[str] = """
CREATE TABLE IF NOT EXISTS interaction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    kind TEXT NOT NULL,
    phase TEXT,
    route TEXT,
    task TEXT,
    model TEXT,
    notes TEXT,
    tokens_in INTEGER NOT NULL DEFAULT 0,
    tokens_out INTEGER NOT NULL DEFAULT 0,
    decision TEXT,
    error TEXT
);
CREATE TABLE IF NOT EXISTS vector_cache_surrogate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    interaction_id INTEGER NOT NULL
        REFERENCES interaction_history(id) ON DELETE CASCADE,
    token TEXT NOT NULL,
    vec TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS gate_telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gate TEXT NOT NULL,
    status TEXT NOT NULL,
    duration_s REAL NOT NULL DEFAULT 0.0,
    timestamp TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_interaction_kind ON interaction_history(kind);
CREATE INDEX IF NOT EXISTS idx_interaction_phase ON interaction_history(phase);
CREATE INDEX IF NOT EXISTS idx_surrogate_interaction
    ON vector_cache_surrogate(interaction_id);
"""


class MemoryRecord(TypedDict, total=False):
    """Shape of a stored interaction, optionally enriched with a score."""

    id: int
    timestamp: str
    kind: str
    phase: str | None
    route: str | None
    task: str | None
    model: str | None
    notes: str | None
    tokens_in: int
    tokens_out: int
    decision: str | None
    error: str | None
    score: float


class SelfCheckSummary(TypedDict, total=False):
    """Result summary emitted by :meth:`CollectiveMemory.selfcheck`."""

    ok: bool
    ids: list[int]
    retrieved: int
    top_kind: str | None
    top_score: float
    stats: dict[str, int]
    rag_lines: int
    db: str


def _utc_now() -> str:
    """Return an ISO-8601 UTC timestamp with second precision."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _tokenize(text: str) -> dict[str, int]:
    """Split text into lowercase alphanumeric tokens with raw frequencies."""
    counts: dict[str, int] = {}
    for token in _TOKEN_RE.findall(text.lower()):
        counts[token] = counts.get(token, 0) + 1
    return counts


def _normalize(counts: dict[str, int]) -> dict[str, float]:
    """L2-normalize a token-frequency dict into a unit-length vector."""
    norm = math.sqrt(sum(weight * weight for weight in counts.values()))
    if norm == 0.0:
        return {}
    return {token: weight / norm for token, weight in counts.items()}


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    """Dot product of two L2-normalized sparse vectors (equals cosine)."""
    if not a or not b:
        return 0.0
    smaller, larger = (a, b) if len(a) <= len(b) else (b, a)
    return sum(weight * larger.get(token, 0.0) for token, weight in smaller.items())


class CollectiveMemory:
    """Collective memory store with agentic RAG over past interactions.

    Thread-safe: every operation serializes on an internal reentrant lock so
    concurrent harness phases never corrupt the SQLite database. The schema
    is created lazily by :meth:`init_db`, which every operation calls first —
    instantiating the class never touches the database file.
    """

    def __init__(self, db_path: str = DEFAULT_DB_PATH) -> None:
        self.db_path = str(db_path)
        self._lock = threading.RLock()

    # ------------------------------------------------------------------
    # schema
    # ------------------------------------------------------------------

    def init_db(self) -> None:
        """Create the memory database and tables if they are missing."""
        parent = Path(self.db_path).parent
        if str(parent):
            parent.mkdir(parents=True, exist_ok=True)
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            try:
                conn.executescript(_SCHEMA)
                conn.commit()
            finally:
                conn.close()

    def _connect(self) -> sqlite3.Connection:
        """Open a connection to the memory database, ensuring the schema exists."""
        self.init_db()
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ------------------------------------------------------------------
    # writing
    # ------------------------------------------------------------------

    def record(
        self,
        kind: str,
        phase: str,
        route: str,
        task: str,
        model: str,
        notes: str,
        tokens_in: int = 0,
        tokens_out: int = 0,
        decision: str = "",
        error: str = "",
    ) -> int:
        """Persist one interaction plus its normalized bag-of-words vector.

        Returns the new ``interaction_history.id``.
        """
        timestamp = _utc_now()
        corpus = " ".join((kind, phase, route, task, model, notes, decision, error))
        vector = _normalize(_tokenize(corpus))
        with self._lock:
            conn = self._connect()
            try:
                cursor = conn.execute(
                    """
                    INSERT INTO interaction_history
                        (timestamp, kind, phase, route, task, model, notes,
                         tokens_in, tokens_out, decision, error)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        timestamp,
                        kind,
                        phase,
                        route,
                        task,
                        model,
                        notes,
                        int(tokens_in),
                        int(tokens_out),
                        decision,
                        error,
                    ),
                )
                record_id = int(cursor.lastrowid)
                conn.execute(
                    """
                    INSERT INTO vector_cache_surrogate (interaction_id, token, vec)
                    VALUES (?, ?, ?)
                    """,
                    (record_id, " ".join(sorted(vector)), json.dumps(vector)),
                )
                conn.commit()
                return record_id
            finally:
                conn.close()

    def record_gate(self, gate: str, status: str, duration_s: float) -> None:
        """Append one gate outcome to the gate telemetry table."""
        with self._lock:
            conn = self._connect()
            try:
                conn.execute(
                    """
                    INSERT INTO gate_telemetry (gate, status, duration_s, timestamp)
                    VALUES (?, ?, ?, ?)
                    """,
                    (gate, status, float(duration_s), _utc_now()),
                )
                conn.commit()
            finally:
                conn.close()

    # ------------------------------------------------------------------
    # retrieval
    # ------------------------------------------------------------------

    def retrieve(self, query: str, top_k: int = 8) -> list[MemoryRecord]:
        """Rank stored interactions by cosine over surrogate word vectors."""
        query_vec = _normalize(_tokenize(query))
        if not query_vec or top_k <= 0:
            return []
        with self._lock:
            conn = self._connect()
            try:
                rows = conn.execute(
                    """
                    SELECT ih.*, v.vec AS surrogate
                    FROM interaction_history ih
                    JOIN vector_cache_surrogate v ON v.interaction_id = ih.id
                    """
                ).fetchall()
            finally:
                conn.close()

        scored: list[tuple[float, sqlite3.Row]] = []
        for row in rows:
            try:
                doc_vec: dict[str, float] = json.loads(row["surrogate"])
            except (json.JSONDecodeError, TypeError):
                continue
            score = _cosine(query_vec, doc_vec)
            if score > 0.0:
                scored.append((score, row))

        scored.sort(key=lambda pair: pair[0], reverse=True)

        results: list[MemoryRecord] = []
        for score, row in scored[:top_k]:
            record: MemoryRecord = {key: row[key] for key in row.keys()}
            record["score"] = round(score, 6)
            results.append(record)
        return results

    def collective_rag(self, query: str, top_k: int = 5) -> str:
        """Return a markdown context block of the most relevant past outcomes."""
        hits = self.retrieve(query, top_k=top_k)
        if not hits:
            return "_No relevant collective memory found._"

        lines: list[str] = [
            "## Collective Memory — Relevant Context",
            "",
        ]
        for i, hit in enumerate(hits, start=1):
            lines.append(
                f"### {i}. [{hit['kind']}] "
                f"{hit.get('phase') or 'any'} (score={hit['score']:.4f})"
            )
            lines.append(f"- timestamp: {hit['timestamp']}")
            if hit.get("route"):
                lines.append(f"- route: {hit['route']}")
            if hit.get("model"):
                lines.append(f"- model: {hit['model']}")
            if hit.get("task"):
                lines.append(f"- task: {hit['task']}")
            if hit.get("notes"):
                lines.append(f"- notes: {hit['notes']}")
            if hit.get("decision"):
                lines.append(f"- decision: {hit['decision']}")
            if hit.get("error"):
                lines.append(f"- error: {hit['error']}")
            lines.append(f"- tokens: in={hit['tokens_in']} out={hit['tokens_out']}")
            lines.append("")
        return "\n".join(lines).rstrip()

    def last_phase(self, phase: str, limit: int = 20) -> list[MemoryRecord]:
        """Return the most recent interactions recorded for a pipeline phase."""
        with self._lock:
            conn = self._connect()
            try:
                rows = conn.execute(
                    """
                    SELECT * FROM interaction_history
                    WHERE phase = ?
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (phase, int(limit)),
                ).fetchall()
            finally:
                conn.close()
        return [MemoryRecord({key: row[key] for key in row.keys()}) for row in rows]

    # ------------------------------------------------------------------
    # observability
    # ------------------------------------------------------------------

    def stats(self) -> dict[str, int]:
        """Count records per interaction kind, plus overall totals."""
        with self._lock:
            conn = self._connect()
            try:
                kinds = conn.execute(
                    "SELECT kind, COUNT(*) AS n FROM interaction_history GROUP BY kind"
                ).fetchall()
                total = conn.execute(
                    "SELECT COUNT(*) AS n FROM interaction_history"
                ).fetchone()
                gates = conn.execute(
                    "SELECT COUNT(*) AS n FROM gate_telemetry"
                ).fetchone()
            finally:
                conn.close()
        counts: dict[str, int] = {row["kind"]: int(row["n"]) for row in kinds}
        counts["total"] = int(total["n"])
        counts["gates"] = int(gates["n"])
        return counts

    # ------------------------------------------------------------------
    # diagnostics
    # ------------------------------------------------------------------

    def selfcheck(self) -> SelfCheckSummary:
        """Exercise the full store on a temporary database, then clean up.

        Uses :mod:`tempfile` so the default (production) database path is
        never touched. Prints progress lines and returns a result summary.
        """
        temp_dir = Path(tempfile.mkdtemp(prefix="collective_memory_selfcheck_"))
        try:
            probe = CollectiveMemory(str(temp_dir / "selfcheck.db"))

            first = probe.record(
                kind="discovery",
                phase="discovery",
                route="MIX",
                task="Refactor harness routing",
                model="ornith-1.0-9b",
                notes="gathered planning context files",
                tokens_in=1200,
                tokens_out=300,
                decision="use MIX route",
            )
            second = probe.record(
                kind="execute",
                phase="execute",
                route="MIX",
                task="Implement context_memory module",
                model="bonsai-27b",
                notes="created sqlite schema and retrieval",
                tokens_in=900,
                tokens_out=150,
                decision="stdlib only",
            )
            third = probe.record(
                kind="review",
                phase="review",
                route="FEATURE",
                task="Audit token budget",
                model="nanbeige-3b",
                notes="checked token usage patterns",
                tokens_in=400,
                tokens_out=80,
                decision="ok",
            )
            probe.record_gate("Gate 1: Aprovação de direção", "passed", 1.2)

            hits = probe.retrieve("context memory module", top_k=3)
            stats = probe.stats()
            recent = probe.last_phase("execute", limit=5)
            rag = probe.collective_rag("context memory", top_k=2)

            summary: SelfCheckSummary = {
                "ok": bool(hits and stats["execute"] == 1 and recent),
                "ids": [first, second, third],
                "retrieved": len(hits),
                "top_kind": hits[0]["kind"] if hits else None,
                "top_score": round(hits[0]["score"], 4) if hits else 0.0,
                "stats": stats,
                "rag_lines": len(rag.splitlines()),
                "db": str(temp_dir / "selfcheck.db"),
            }
            print(f"selfcheck: ids={first},{second},{third}")
            print(
                "selfcheck: retrieve -> "
                f"{len(hits)} hits, top={summary['top_kind']} "
                f"score={summary['top_score']}"
            )
            print(f"selfcheck: stats -> {stats}")
            print(f"selfcheck: last_phase(execute) -> {len(recent)} rows")
            return summary
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
