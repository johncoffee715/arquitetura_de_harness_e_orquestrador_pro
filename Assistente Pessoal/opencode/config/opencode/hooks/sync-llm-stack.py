#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync-llm-stack.py — Hook session.start (R27): vigilância do gerador canônico da stack LLM.

Roda `sync-llm-stack.py --check` a cada início de sessão. Se houver divergência,
apenda uma linha em state/watcher/sync-llm-stack.log (JSONL). Fail-open: nunca
bloqueia session.start (córtex/stack down -> sessão segue normal).

Protocolo hook OpenCode (session.start):
    stdin:  JSON {"session_id": ...}
    stdout: JSON {"context": {"__SYNC_LLM_STACK__": {...}}} — injeção de contexto.

Uso:
    python3 hooks/sync-llm-stack.py              (modo hook — lê stdin e emite JSON)
    python3 hooks/sync-llm-stack.py --check      (modo CLI — só verifica, exit 0/1)
    python3 hooks/sync-llm-stack.py --test       (smoke rápido)
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SYNC = "/mnt/dados/Assistente Pessoal/opencode/scripts/sync-llm-stack.py"
LOG = Path("/mnt/dados/Assistente Pessoal/opencode/state/watcher/sync-llm-stack.log")
MAX_DIV_TEXT = 1200


def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _check_only():
    r = subprocess.run(
        [sys.executable, SYNC, "--check"], capture_output=True, text=True, timeout=120
    )
    return r, r.returncode == 0, r.stdout.strip()


def _append_log(entry):
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass


def main(argv=None):
    ap = argparse.ArgumentParser(description="Hook de sync da stack LLM (session.start)")
    ap.add_argument("--check", action="store_true", help="modo CLI: verifica divergências (exit 0/1)")
    ap.add_argument("--test", action="store_true", help="smoke: imprime JSON e sai 0")
    args = ap.parse_args(argv)

    if args.test:
        print(json.dumps({"context": {"__SYNC_LLM_STACK__": {"ok": True, "mode": "test"}}}))
        return 0

    # consome o payload do hook (session.start JSON em stdin) — nunca deixa buffer preso
    try:
        if not sys.stdin.isatty():
            raw = sys.stdin.read()
            if raw.strip():
                json.loads(raw)
    except Exception:
        pass

    try:
        r, synced, out = _check_only()
    except Exception as exc:  # fail-open absoluto
        _append_log({"ts": _now_iso(), "synced": None, "error": str(exc)})
        print(json.dumps({"context": {"__SYNC_LLM_STACK__": {"synced": None, "error": str(exc)}}}))
        return 0

    entry = {
        "ts": _now_iso(),
        "synced": synced,
        "rc": r.returncode,
        "divergencias": out[:MAX_DIV_TEXT] if not synced else "",
    }
    _append_log(entry)

    print(json.dumps({
        "context": {
            "__SYNC_LLM_STACK__": {
                "synced": synced,
                "checked_at": _now_iso(),
                "divergencias": out[:800] if not synced else None,
            }
        }
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())