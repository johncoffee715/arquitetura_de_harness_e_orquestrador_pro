#!/bin/bash
# helenize-gate.sh — REGRA GLOBAL: autofagia/helenização automática de entregas v2
# PostToolUse Write|Edit — se um .py *_v2/corrigido nascer em Downloads/, valida e integra.
# NUNCA bloqueia a tool. Idempotente (--dry-run se AUTO_OK != 1).
set +e +u +o pipefail

HELENIZE_IMPORT="/mnt/dados/harness/autofagia/helenize_import.py"
[ -f "$HELENIZE_IMPORT" ] || exit 0

INPUT=$(cat 2>/dev/null)
TOOL=""
if command -v jq >/dev/null 2>&1; then
  TOOL=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
fi

case "$TOOL" in
  Write|Edit)
    FILE=$(printf '%s' "$INPUT" | jq -r '.file_path // empty' 2>/dev/null)
    case "$FILE" in
      *Downloads*|*autofagia*)
        if [ -f /home/johncoffee/Downloads/*_v2.py ] || [ -f /home/johncoffee/Downloads/*v2.py ]; then
          if [ "${AUTO_HELENIZE:-0}" = "1" ]; then
            python3 "$HELENIZE_IMPORT" --scan-dir /home/johncoffee/Downloads >/dev/null 2>&1 || true
          else
            pub=$(printf '%s' "$(date -Is)"); # loga aviso sem integrar (conservador)
          fi
        fi
        ;;
    esac
    ;;
esac
printf '%s\n' '{"status":"ok"}'
