#!/usr/bin/env python3
"""spec_cache.py — F2 Cache Semântico determinístico (R: F2-spec-cache v3.0).
Sem LLM: divide spec.md em seções (## ), sha256 por seção, compara com o
estado (.spec_cache.json) e emite SÓ o que mudou + cabeçalho truncado.
Se nada mudou, as fases seguintes reusam o cache (zero reprocessamento).
Contrato I/O: {mudou: bool, secoes_alteradas: [...], header_truncado: str}.
Forja: Gran-Mestre 2026-09-08, modo autonomo ON.
"""
import hashlib
import json
import re
import sys

STATE_DEFAULT = ".spec_cache.json"
HEADER_LINES = 12


def split_sections(text):
    parts = re.split(r"(?m)^## ", text)
    head = parts[0]
    secs = {}
    for p in parts[1:]:
        title = p.split("\n", 1)[0].strip()
        secs[title] = "## " + p
    return head, secs


def digest(secs):
    return {t: hashlib.sha256(c.encode()).hexdigest()[:16]
            for t, c in secs.items()}


def run(spec_path, state_path=STATE_DEFAULT):
    text = open(spec_path, encoding="utf-8").read()
    head, secs = split_sections(text)
    cur = digest(secs)
    try:
        prev = json.load(open(state_path))
    except (OSError, ValueError):
        prev = {}
    changed = sorted(k for k in cur if prev.get(k) != cur[k])
    added = sorted(k for k in cur if k not in prev)
    removed = sorted(k for k in prev if k not in cur)
    json.dump(cur, open(state_path, "w"), indent=1)
    header = "\n".join(head.splitlines()[:HEADER_LINES])
    return {"mudou": bool(changed or added or removed),
            "secoes_alteradas": changed,
            "secoes_novas": added, "secoes_removidas": removed,
            "header_truncado": header}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        open("/tmp/opencode/spec-demo.md", "w").write(
            "# Spec\nIntro.\n## A\nfoo\n## B\nbar\n")
        r1 = run("/tmp/opencode/spec-demo.md", "/tmp/opencode/spec-demo.json")
        assert r1["mudou"] is True and set(r1["secoes_novas"]) == {"A", "B"}, r1
        r2 = run("/tmp/opencode/spec-demo.md", "/tmp/opencode/spec-demo.json")
        assert r2["mudou"] is False, r2
        open("/tmp/opencode/spec-demo.md", "a").write("\n## C\nbaz\n")
        r3 = run("/tmp/opencode/spec-demo.md", "/tmp/opencode/spec-demo.json")
        assert r3["mudou"] is True and r3["secoes_novas"] == ["C"], r3
        print("SELFTEST-OK")
    elif len(sys.argv) > 1:
        print(json.dumps(run(sys.argv[1],
                             sys.argv[2] if len(sys.argv) > 2 else STATE_DEFAULT),
                         ensure_ascii=False, indent=1))
    else:
        print("uso: spec_cache.py <spec.md> [estado.json] | --selftest")
