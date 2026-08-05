"""Brainstorm inter-agente (A2A) — recursos conversam entre si via board.

Protocolo para que subagents/skills/tools (cada um herdando um submodelo via
ModelInheritance) troquem ideias de forma estruturada, coordenado pelo
orquestrador como ponto de ignição. O Board é markdown persistente em
``harness/brainstorm/{topic}.md``: cada participante POSTA mensagens rotuladas
numa rodada; o orquestrador pode INDUZIR novas rodadas (ex.: síntese, crítica,
contra-argumento); no fim, o transcript alimenta a decisão (spec/plano).

Complementar aos skills de brainstorming já existentes no catálogo
(``superpowers-brainstorming``), que são diálogo usuário↔orquestrador — este é o
transporte entre RECURSOS (multi-agente), resolvido por oferta-demanda (R5).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

BOARD_DIR = "brainstorm"


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class BrainstormBoard:
    """Append-only conversation board shared by multiple agents."""

    def __init__(self, project_root: str = "/mnt/dados", board_dir: Optional[str] = None) -> None:
        self.project_root = Path(project_root)
        self.lock = threading.RLock()
        base = self.project_root / "harness" / (board_dir or BOARD_DIR)
        base.mkdir(parents=True, exist_ok=True)
        self.board_dir = base

    def _path(self, topic: str) -> Path:
        safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in topic)
        return self.board_dir / f"{safe}.md"

    def start(self, topic: str, participants: List[str], context: str = "") -> str:
        """Create the board (idempotent) and return its absolute path."""
        path = self._path(topic)
        with self.lock:
            if not path.exists():
                path.write_text(
                    f"# Brainstorm — {topic}\n"
                    f"created_at: {_utcnow()}\n"
                    f"participants: {', '.join(participants)}\n"
                    f"context: {context or '-'}\n"
                    f"\n## Rodada 1\n",
                    encoding="utf-8",
                )
        return str(path)

    def post(self, topic: str, participant: str, message: str) -> str:
        """Append one labeled message under the current round; returns path."""
        path = self._path(topic)
        if not path.exists():
            return self.start(topic, [participant])
        with self.lock:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"- **[{participant}]** ({_utcnow()}) {message}\n")
        return str(path)

    def next_round(self, topic: str, title: str = "") -> str:
        """Induce a new round (e.g. síntese, crítica, contra-argumento)."""
        path = self._path(topic)
        with self.lock:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"\n## Rodada: {title or 'continuação'} ({_utcnow()})\n")
        return str(path)

    def read(self, topic: str) -> str:
        path = self._path(topic)
        if not path.is_file():
            return ""
        return path.read_text(encoding="utf-8")

    def transcript(self, topic: str) -> List[Dict[str, str]]:
        """Parse the board into structured turns (participant / message)."""
        pattern = re.compile(r"^- \*\*\[([^\]]+)\]\*\* \(([^)]*)\) (.*)$")
        turns: List[Dict[str, str]] = []
        for line in self.read(topic).splitlines():
            m = pattern.match(line.strip())
            if not m:
                continue
            turns.append({"participant": m.group(1), "ts": m.group(2),
                          "message": m.group(3)})
        return turns

    def selfcheck(self) -> Dict[str, Any]:
        tmp = Path(tempfile.mkdtemp(prefix="brainstorm_selfcheck_"))
        try:
            b = BrainstormBoard(project_root=str(tmp))
            path = b.start("tema", ["orchestrator", "model-a", "model-b"], "ctx")
            b.post("tema", "model-a", "proposta 1")
            b.post("tema", "model-b", "contraponto")
            b.next_round("tema", "síntese")
            b.post("tema", "orchestrator", "consenso: proposta 1 com ajuste")
            text = b.read("tema")
            turns = b.transcript("tema")
            checks = {
                "board_created": Path(path).is_file(),
                "has_rounds": "## Rodada" in text,
                "three_turns": len(turns) == 3,
                "first_speaker": turns[0]["participant"] == "model-a" if turns else False,
                "last_consensus": turns[-1]["message"].startswith("consenso") if turns else False,
            }
            return {"ok": all(checks.values()), "checks": checks}
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def _cli(self, argv: Optional[List[str]] = None) -> int:
        p = argparse.ArgumentParser(prog="harness.a2a.brainstorm",
                                    description="Brainstorm inter-agente (A2A board)")
        sub = p.add_subparsers(dest="cmd")
        sp = sub.add_parser("start"); sp.add_argument("--topic", required=True)
        sp.add_argument("--participants", required=True)
        sp.add_argument("--context", default="")
        pp = sub.add_parser("post"); pp.add_argument("--topic", required=True)
        pp.add_argument("--participant", required=True); pp.add_argument("--message", required=True)
        pr = sub.add_parser("round"); pr.add_argument("--topic", required=True); pr.add_argument("--title", default="")
        pt = sub.add_parser("transcript"); pt.add_argument("--topic", required=True)
        sub.add_parser("selfcheck")
        args = p.parse_args(argv)
        if args.cmd == "start":
            print(self.start(args.topic, args.participants.split(","), args.context))
        elif args.cmd == "post":
            print(self.post(args.topic, args.participant, args.message))
        elif args.cmd == "round":
            print(self.next_round(args.topic, args.title))
        elif args.cmd == "transcript":
            print(json.dumps(self.transcript(args.topic), indent=2, ensure_ascii=False))
        elif args.cmd == "selfcheck":
            print(json.dumps(self.selfcheck(), indent=2, ensure_ascii=False))
        else:
            p.print_help(); return 2
        return 0


def main(argv: Optional[List[str]] = None) -> int:
    return BrainstormBoard()._cli(argv)


if __name__ == "__main__":
    sys.exit(main())
