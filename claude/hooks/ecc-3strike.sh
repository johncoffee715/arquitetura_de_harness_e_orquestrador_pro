#!/bin/bash
# ecc-3strike.sh — 3-Strike Protocol
# 3 tentativas antes de escalar
# Uso: hook PostToolUseFailure

STRIKE_FILE="/home/johncoffee/.ecc/autofagia/strikes.jsonl"
ERROR_COUNT=$(($(tail -1 "$STRIKE_FILE" 2>/dev/null | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('strikes',0))" 2>/dev/null || echo "0") + 1))

echo "{\"strikes\":$ERROR_COUNT,\"ts\":\"$(date -Iseconds)\",\"error\":\"$1\"}" >> "$STRIKE_FILE"

echo "[ecc-3strike] Strike $ERROR_COUNT/3 registrado"

if [ "$ERROR_COUNT" -ge 3 ]; then
    echo "[ecc-3strike] ESCALANDO: 3 strikes atingidos. Ferramenta: $1"
    echo "{\"ts\":\"$(date -Iseconds)\",\"level\":\"ESCALATION\",\"tool\":\"$TOOL\",\"strikes\":$ERROR_COUNT}" >> "/home/johncoffee/.ecc/autofagia/errors.jsonl"
fi
