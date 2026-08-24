#!/bin/bash
# ecc-session-end.sh — REGRA GLOBAL: nunca deletar sessão sem antes
#   REGISTRAR (cognitivo) → COMPACTAR → LIMPAR.
#
# Ciclo completo via harness/cognition/compact_context.py (armazenar→compactar→limpar).
# Nunca bloqueia (exit 0 sempre) e é idempotente. Serve para o fim de sessão / deleção.
set +e +u +o pipefail

SCRIPT="/mnt/dados/harness/cognition/compact_context.py"
[ -f "$SCRIPT" ] || exit 0

# Se for uma deleção (variável do hook pode trazer o motivo), registramos explicitamente
DELETE_FLAG="${SESSION_DELETE:-0}"

if [ "$DELETE_FLAG" = "1" ]; then
  # Deleção solicitada: ciclo completo + marca no estado
  python3 "$SCRIPT" > /tmp/ecc-session-end.log 2>&1
  echo "$(date -Is) DELETED session — registro+compactacao+limpeza realizados" >> /tmp/ecc-session-end.log
else
  # Fim de sessão normal: mesmo ciclo (garante snapshot antes de qualquer release)
  python3 "$SCRIPT" > /tmp/ecc-session-end.log 2>&1
fi

printf '%s\n' '{"status":"ok"}'
