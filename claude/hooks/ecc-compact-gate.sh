#!/bin/bash
# ecc-compact-gate.sh — REGRA GLOBAL: compactação cognitiva a 50% de capacidade.
# PreCompact (Session Compact) — antes de qualquer compactação: ARMAZENA (Obsidian+CONTEXT),
# COMPACTA (CONTEXT_COMPACT) e LIMPA (lixo não-git). Nunca bloqueia. Idempotente.
set +e +u +o pipefail

SCRIPT="/mnt/dados/harness/cognition/compact_context.py"
[ -f "$SCRIPT" ] || exit 0

# Rodar sempre que chamado (sessão pré-compactação), com dry-run se COMPACT_DRY.
if [ "${COMPACT_DRY:-0}" = "1" ]; then
  python3 "$SCRIPT" --dry-run >/dev/null 2>&1 || true
else
  python3 "$SCRIPT" >/dev/null 2>&1 || true
fi

printf '%s\n' '{"status":"ok"}'
