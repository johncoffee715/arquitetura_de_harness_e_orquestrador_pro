#!/bin/bash
# ecc-safety-sha.sh — Safety SHA Rollback
# Salva SHA antes de Write/Edit e prepara rollback
# Uso: hook PreToolUse para Write|Edit

PLAN_DIR="/home/johncoffee/.opencode/.planning"
CONTEXT_FILE="$PLAN_DIR/context.md"

# Só executa se estiver em um git repo
if git rev-parse HEAD 2>/dev/null; then
    SHA=$(git rev-parse HEAD)
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "- [Safety] SHA: $SHA | $TIMESTAMP" >> "$CONTEXT_FILE" 2>/dev/null || true
    echo "[ecc-safety] SHA salvo: $SHA"
fi
