#!/bin/bash
# ecc-2action-rule.sh — 2-Action Rule
# A cada 2 acoes de leitura/pesquisa, salva descobertas
# Uso: hook PostToolUse para Read|Grep|WebSearch

COUNTER_FILE="/home/johncoffee/.ecc/autofagia/action-counter.jsonl"
FINDINGS_FILE="/home/johncoffee/.opencode/.planning/autofagia-ecc/findings.md"

# Incrementa contador
COUNT=$(tail -1 "$COUNTER_FILE" 2>/dev/null | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('count',0)+1)" 2>/dev/null || echo "1")
echo "{\"count\":$COUNT,\"ts\":\"$(date -Iseconds)\",\"tool\":\"$1\"}" >> "$COUNTER_FILE"

# A cada 2 acoes, salva checkpoint
if [ $((COUNT % 2)) -eq 0 ]; then
    echo "" >> "$FINDINGS_FILE" 2>/dev/null
    echo "### Checkpoint $(date '+%H:%M:%S')" >> "$FINDINGS_FILE" 2>/dev/null
    echo "[ecc-2action] Checkpoint salvo (acao #$COUNT)"
fi
