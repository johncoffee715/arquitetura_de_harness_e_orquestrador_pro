#!/usr/bin/env bash
# needle-tdd-extract.sh — pipeline F4/L0: log pytest bruto → JSON estruturado
# PRIMÁRIO: regex determinística (file:line:exception 100% preciso, zero alucinação)
# Bench 25/08: Needle-45M falhou nesta tarefa (confidence 0.0001, ungrounded) —
# vocação dele é TRIAGEM/ROTEAMENTO (scripts/needle), não parsing denso.
set -euo pipefail

input="${1:-/dev/stdin}"
[ -s "$input" ] || { echo '{"failures":[]}'; exit 0; }

python3 - "$input" <<'PY'
import re, sys, json

txt = open(sys.argv[1], encoding="utf-8", errors="replace").read()
failures = []

# bloco por teste: separadores "_ _ _ nome _ _ _" ou linhas FAILED
loc_pat = re.compile(r"([^\s:]+\.py):(\d+): ([A-Za-z_][\w.]*(?:Error|Exception))")
msg_pat = re.compile(r"^E\s+(.+)$", re.M)
failed_pat = re.compile(r"^(?:FAILED|ERROR)\s+(\S+?)\s*-?\s*(.*)$", re.M)

seen = set()
for m in loc_pat.finditer(txt):
    key = (m.group(1), m.group(2))
    if key in seen:
        continue
    seen.add(key)
    failures.append({
        "file": m.group(1),
        "line": int(m.group(2)),
        "exception_type": m.group(3),
    })

for fm in failed_pat.finditer(txt):
    nodeid = fm.group(1)
    for f in failures:
        if nodeid.startswith(f["file"]) and "test_name" not in f:
            f["test_name"] = nodeid.split("::")[-1]
            break

# primeira mensagem E após cada localização (aproximação por ordem)
msgs = msg_pat.findall(txt)
for i, f in enumerate(failures):
    if i < len(msgs):
        f["message"] = msgs[i].strip()[:200]

print(json.dumps({"failures": failures}, ensure_ascii=False))
PY
