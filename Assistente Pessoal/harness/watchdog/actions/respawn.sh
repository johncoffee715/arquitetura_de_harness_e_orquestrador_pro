#!/bin/bash
# respawn de slots ausentes — start-all-models.sh tem lock cooperativo e
# só sobe os ausentes (reusando os vivos). GPU-only garantido no launcher.
log() { echo "[$(date '+%F %T')] $*" >> "/mnt/dados/Assistente Pessoal/harness/logs/wd-modular.log"; }
log "respawn acionado — start-all-models.sh (só ausentes, GPU-only)"
bash "/mnt/dados/Assistente Pessoal/harness/start-all-models.sh" >> "/mnt/dados/Assistente Pessoal/harness/logs/gpu-watchdog.log" 2>&1
