#!/usr/bin/env bash
# esvaziar-lixeiras.sh — UNIFICADOR de lixeiras (R: pedido usuário 2026-09-07)
# Um comando esvazia TODAS as lixeiras conhecidas (sistema + mounts).
# POR QUE script e não symlink: symlink cross-fs quebra a atomicidade do trash
# (vira cópia+lentidão); gerenciadores já agregam trash:// nativamente.
# SEGURANÇA: sem --confirmo, só LISTA (dry-run). Log em /tmp/opencode/.
# Forja: Gran-Mestre cloud-direct, modo autonomo ON. v1.1 (zero rm: só find -delete).
set -u
LOG="/tmp/opencode/esvaziar-lixeiras.log"
TRASHES="$HOME/.local/share/Trash /mnt/dados/.Trash-1000"
MODE="${1:-}"

mkdir -p /tmp/opencode
{
echo "=== $(date -u +%FT%TZ) modo=${MODE:-listar} ==="
for t in $TRASHES; do
  if [ -d "$t" ]; then
    echo "--- $t : $(du -sh "$t" 2>/dev/null | cut -f1)"
    [ -d "$t/files" ] && ls "$t/files" 2>/dev/null
  else
    echo "--- $t : ausente"
  fi
done
echo "--- legados top-level:"
find /mnt/dados/.Trash-1000 -maxdepth 1 -name "*.gguf" -print 2>/dev/null || echo "(nenhum)"
} | tee -a "$LOG"

if [ "$MODE" != "--confirmo" ]; then
  echo "DRY-RUN: nada apagado. Reemita com --confirmo para esvaziar de verdade." | tee -a "$LOG"
  exit 0
fi

{
echo "CONFIRMADO pelo operador em $(date -u +%FT%TZ). Esvaziando:"
for t in $TRASHES; do
  for sub in files info; do
    if [ -d "$t/$sub" ]; then
      find "$t/$sub" -mindepth 1 -delete -print
    fi
  done
done
find /mnt/dados/.Trash-1000 -maxdepth 1 -name "*.gguf" -delete -print
echo "OK esvaziado."
} | tee -a "$LOG"
