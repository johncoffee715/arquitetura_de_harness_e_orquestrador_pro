#!/usr/bin/env bash
# Paridade tarball vendado ↔ workspace client (Ciclo E, 2026-08-25)
# Gera o manifesto exato p/ migração: símbolos consumidos vs disponíveis.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
TARBALL_TS=$(mktemp -d); OUT="client-parity-report.md"
mkdir -p "$TARBALL_TS/x" && tar -xzf packages/app/vendor/opencode-ai-client-1.17.13-v2.tgz -C "$TARBALL_TS/x" 2>/dev/null

# símbolos importados por consumidores (tipos + valores, inclusive multilinha)
CONS=$(grep -rlZ "@opencode-ai/client/promise" \
  packages/app/src packages/session-ui/src --include="*.tsx" --include="*.ts" 2>/dev/null \
  | xargs -0 perl -0777 -ne 'while(/import\s+(?:type\s+)?\{([^}]+)\}\s*from\s*"\@opencode-ai\/client\/promise"/g){print "$1\n"}' \
  | tr ',' '\n' | sed 's/type //g;s/^ *//;s/ *$//' | sort -u)

{
echo "# Client Parity Report ($(date +%F))"
echo
echo "| Símbolo consumido | Existe no workspace \`src/generated\`? | Sites afetados |"
echo "|---|---|---|"
MISSING=0; TOTAL=0
for sym in $CONS; do
  [ -z "$sym" ] && continue
  TOTAL=$((TOTAL+1))
  HITS=$(grep -rl "\b$sym\b" packages/client/src/generated/*.ts 2>/dev/null | wc -l)
  SITES=$(grep -rc "\b$sym\b" packages/app/src packages/session-ui/src --include="*.tsx" --include="*.ts" -r 2>/dev/null | awk -F: '{s+=$NF} END{print s}')
  if [ "$HITS" -gt 0 ]; then echo "| \`$sym\` | ✔ | $SITES |"; else echo "| \`$sym\` | ❌ **falta** | $SITES |"; MISSING=$((MISSING+1)); fi
done
echo
echo "**$TOTAL símbolos consumidos · $MISSING ausentes no workspace** — cada ❌ exige mapeamento manual p/ o nome novo na migração."
} > "$OUT"
rm -rf "$TARBALL_TS"
grep -c "❌" "$OUT" >/dev/null && echo "relatório: $OUT ($MISSING/$TOTAL faltantes)"
tail -4 "$OUT"
