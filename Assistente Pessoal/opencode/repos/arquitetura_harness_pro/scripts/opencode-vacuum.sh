#!/usr/bin/env bash
# opencode-vacuum.sh - Executado por cron. Só roda se opencode não estiver rodando.
set -euo pipefail
DB="/mnt/dados/opencode/share-data/opencode.db"
LOCKFILE="/tmp/opencode-vacuum.lock"

# Não roda se opencode estiver ativo
if pgrep -x "opencode" > /dev/null 2>&1; then exit 0; fi

# Evita execução simultânea
[ -f "$LOCKFILE" ] && exit 0
touch "$LOCKFILE"
trap 'rm -f "$LOCKFILE"' EXIT

[ ! -f "$DB" ] && exit 0

SIZE_BEFORE=$(du -h "$DB" | cut -f1)
sqlite3 "$DB" "PRAGMA integrity_check;" 2>/dev/null | grep -q "ok" || exit 1
sqlite3 "$DB" "VACUUM;" 2>/dev/null || true
sqlite3 "$DB" "PRAGMA wal_checkpoint(TRUNCATE);" 2>/dev/null || true
SIZE_AFTER=$(du -h "$DB" | cut -f1)

logger "opencode-vacuum: $SIZE_BEFORE → $SIZE_AFTER"
