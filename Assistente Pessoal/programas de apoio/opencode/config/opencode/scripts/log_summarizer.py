#!/usr/bin/env python3
"""
LOG SUMMARIZER — Sumarizador heurístico determinístico de logs (sem LLM).

Helenizado de atomic-agent (log-summarizer.ts + result-compressor.ts).
Conta sinais de frameworks de teste (pytest/go/jest) + erros/warnings,
comprime output verboso em resumo compacto.

Origin: helenizado:atomic-agent (2026-08-31)
"""

import argparse
import json
import re
import sys

DEFAULT_MAX_SUMMARY = 400
DEFAULT_MAX_TAIL = 12


def summarise_log(output: str) -> dict:
    """Conta sinais de frameworks de teste + erros/warnings (determinístico)."""
    lines = output.splitlines()
    err = warn = passed = failed = 0
    first_err = first_fail = None
    for ln in lines:
        if re.search(r"\b(error|exception)\b", ln, re.I):
            err += 1
            first_err = first_err or ln.strip()[:200]
        elif re.search(r"\bwarn(ing)?\b", ln, re.I):
            warn += 1
        if re.search(r"\b(PASSED|PASS|ok)\b", ln):
            passed += 1
        if re.search(r"\b(FAILED|FAIL)\b", ln):
            failed += 1
            first_fail = first_fail or ln.strip()[:200]
    return {
        "totalLines": len(lines),
        "errorLines": err,
        "warningLines": warn,
        "passCount": passed,
        "failCount": failed,
        "firstError": first_err,
        "firstFailure": first_fail,
    }


def extract_tail(output: str, max_tail: int = DEFAULT_MAX_TAIL) -> tuple[str, bool]:
    """Extrai as últimas N linhas não-vazias."""
    non_blank = [ln for ln in output.splitlines() if ln.strip()]
    truncated = len(non_blank) > max_tail
    return "\n".join(non_blank[-max_tail:]), truncated


def compress_result(output: str, max_summary: int = DEFAULT_MAX_SUMMARY,
                    max_tail: int = DEFAULT_MAX_TAIL) -> dict:
    """Comprime output verboso em resumo compacto (tail + assinatura + truncamento)."""
    summary = summarise_log(output)
    tail, tail_trunc = extract_tail(output, max_tail)
    signature = (
        f"[{summary['passCount']} pass | {summary['failCount']} fail | "
        f"{summary['errorLines']} err | {summary['warningLines']} warn]"
    )
    joined = f"{signature}\n{tail}".strip()
    over = len(joined) > max_summary
    final = f"{joined[:max_summary - 15]}\n… [truncated]" if over else joined
    return {
        "summary": final,
        "truncated": tail_trunc or over,
        "signature": signature,
        "stats": summary,
    }


def main():
    parser = argparse.ArgumentParser(description="Log Summarizer (determinístico, sem LLM)")
    parser.add_argument("--summarise", action="store_true", help="contar sinais do log")
    parser.add_argument("--compress", action="store_true", help="comprimir em resumo compacto")
    parser.add_argument("--json", action="store_true", help="saída JSON")
    parser.add_argument("file", nargs="?", help="arquivo de log (default: stdin)")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            output = f.read()
    else:
        output = sys.stdin.read()

    if args.compress:
        result = compress_result(output)
    else:
        result = summarise_log(output)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if args.compress:
            print(result["summary"])
        else:
            s = result
            print(f"linhas={s['totalLines']} erros={s['errorLines']} warns={s['warningLines']} "
                  f"pass={s['passCount']} fail={s['failCount']}")
            if s["firstError"]:
                print(f"1º erro: {s['firstError']}")
            if s["firstFailure"]:
                print(f"1ª falha: {s['firstFailure']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())