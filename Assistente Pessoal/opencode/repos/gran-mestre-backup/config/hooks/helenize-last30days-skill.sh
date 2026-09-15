#!/usr/bin/env bash
# helenize-last30days-skill.sh — hook pós-tool para o padrão absorvido de mvanhorn/last30days-skill
# Gerado automaticamente por helenize_deploy.py v2 (NÃO editar manualmente)
set -euo pipefail

INPUT=$(cat)
if command -v jq >/dev/null 2>&1; then
  TOOL=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || true)
else
  TOOL=$(printf '%s' "$INPUT" | python3 -c "import sys,json;
try:
  d=json.load(sys.stdin); print(d.get('tool_name',''))
except Exception: pass" 2>/dev/null || true)
fi

if [ -n "$TOOL" ]; then
  LOG='/home/johncoffee/.opencode/helenize'/'last30days-skill'.log
  mkdir -p '/home/johncoffee/.opencode/helenize'
  if command -v jq >/dev/null 2>&1; then
    jq -nc --arg tool "$TOOL" --arg ts "$(date -Is)" --arg origem 'mvanhorn/last30days-skill'       '{tool:$tool,ts:$ts,origem:$origem}' >> "$LOG" 2>/dev/null || true
  else
    printf 'tool=%s ts=%s origem=%s
' "$TOOL" "$(date -Is)" 'mvanhorn/last30days-skill' >> "$LOG" 2>/dev/null || true
  fi
fi
printf '%s\n' '{"status":"ok"}'
