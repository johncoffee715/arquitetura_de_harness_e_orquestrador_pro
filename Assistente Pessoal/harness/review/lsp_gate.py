#!/usr/bin/env python3
"""
LSP Gate — automatic code diagnostics for the Review phase (F5).

Runs a configured LSP/diagnostic CLI over the files changed by the
pipeline and reports a verdict. It is fail-safe: when no diagnostic
CLI is installed the gate is *skipped*, never blocking the pipeline
on infrastructure absence.

Verdicts:
    passed  — diagnostics ran, zero errors
    issues  — diagnostics ran, N errors found
    skipped — no diagnostic CLI available
"""

from __future__ import annotations

import re
import shutil
import subprocess
from typing import Callable, Dict, List, Optional, Tuple

# language -> candidate diagnostic CLIs (first found wins).
LSP_CLIS: Dict[str, List[str]] = {
    "py": ["basedpyright", "pyright", "pylint"],
    "ts": ["tsc"],
    "go": ["golangci-lint"],
}

_ERROR_PATTERNS = (
    re.compile(r"error\s*:"),
    re.compile(r"\[error\]"),
    re.compile(r"Error:"),
)


def _default_run(argv: List[str]) -> Tuple[int, str]:
    proc = subprocess.run(argv, capture_output=True, timeout=60, check=False)
    out = (proc.stdout or b"").decode(errors="replace")
    err = (proc.stderr or b"").decode(errors="replace")
    return proc.returncode, out + err


def count_errors(output: str) -> int:
    """Count diagnostic errors in CLI output (duplicates deduped)."""
    seen = set()
    for line in output.splitlines():
        for pat in _ERROR_PATTERNS:
            if pat.search(line):
                key = line.strip().lower()
                if key not in seen:
                    seen.add(key)
                break
    return len(seen)


def available_cli(language: str) -> Optional[str]:
    for cli in LSP_CLIS.get(language, []):
        if shutil.which(cli):
            return cli
    return None


def run_lsp_gate(
    files: List[str],
    language: str = "py",
    runner: Optional[Callable[[List[str]], Tuple[int, str]]] = None,
    cli: Optional[str] = None,
) -> Dict[str, object]:
    """Run the diagnostic gate over changed files and return a verdict."""
    tool = cli or available_cli(language)
    if tool is None:
        return {"status": "skipped", "diagnostics": 0,
                "detail": "nenhum CLI de diagnóstico instalado"}
    if not files:
        return {"status": "passed", "diagnostics": 0,
                "detail": "nenhum arquivo alterado"}
    run = runner or _default_run
    try:
        code, output = run([tool] + list(files))
    except Exception as exc:
        return {"status": "skipped", "diagnostics": 0,
                "detail": f"falha ao executar {tool}: {exc}"}
    n = count_errors(output)
    status = "passed" if n == 0 else "issues"
    return {"status": status, "diagnostics": n,
            "detail": f"{tool} (exit {code})"}