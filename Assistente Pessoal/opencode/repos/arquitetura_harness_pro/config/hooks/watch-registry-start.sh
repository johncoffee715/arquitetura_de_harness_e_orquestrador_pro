#!/bin/bash
# R48: vigia do registry — chamado pelo session.start; idempotente (pgrep-guard).
if ! pgrep -f 'watch_[r]egistry' >/dev/null 2>&1; then
  setsid nohup /home/johncoffee/.config/opencode/skills/model-discovery/watch_registry.sh \
    >/dev/null 2>&1 < /dev/null &
fi

# ── GATE KRON-SUBSTITUIÇÕES (15 dias · guardrail usuário 2026-08-24) ──
KRON_MARK="/mnt/dados/logs/.kron-last"
KRON_S="/mnt/dados/opencode/harness/kron-substituicoes.sh"
if [ ! -f "$KRON_MARK" ] || [ $(( $(date +%s) - $(stat -c %Y "$KRON_MARK" 2>/dev/null || echo 0) )) -ge 1296000 ]; then
  touch "$KRON_MARK"
  setsid bash "$KRON_S" >> /mnt/dados/logs/kron-subs.log 2>&1 < /dev/null &
fi
