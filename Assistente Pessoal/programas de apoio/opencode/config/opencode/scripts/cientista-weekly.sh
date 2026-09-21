#!/usr/bin/env bash
# gatilho semanal R106 — camada 3 (cron/systemd)
# Wrapper do Cientista: idempotente por ISO-week (lock .runs/<sem>.done).
# Instalação manual (NÃO executada pela forja):
#   systemctl --user daemon-reload && systemctl --user enable --now cientista-weekly.timer
# Reversível: systemctl --user disable --now cientista-weekly.timer
set -euo pipefail

RUNS_DIR="/mnt/dados/Assistente Pessoal/cerebro com IA/experimentos/.runs"
SEMANA="$(date +%G-W%V)"
LOCK="${RUNS_DIR}/${SEMANA}.done"

if [ -e "$LOCK" ]; then
    echo "[cientista-weekly] semana ${SEMANA} já executada (lock ${LOCK}) — no-op."
    exit 0
fi

python3 /home/johncoffee/.config/opencode/skills/cientista/mecanica.py --semana atual
