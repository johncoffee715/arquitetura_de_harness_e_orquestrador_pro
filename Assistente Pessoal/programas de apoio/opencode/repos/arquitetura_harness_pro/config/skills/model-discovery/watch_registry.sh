#!/bin/bash
# Hot-reload do registry (R44): re-escaneia ao detectar mudança no MODEL_LIBRARY.
# Polling 5s + debounce 5s (downloads parciais não geram registry sujo).
set -u
MODELS_DIR="/mnt/dados/Assistente Pessoal/modelos LLM"
OUT="/mnt/dados/opencode/benchmark/runs/registry.json"
RUN="/home/johncoffee/.config/opencode/skills/model-discovery/run.py"
LOG="/tmp/watch-registry.log"

fingerprint() {
  stat -c '%n:%Y:%s' "$MODELS_DIR"/*.gguf 2>/dev/null | md5sum | cut -d' ' -f1
}

prev="$(fingerprint)"
echo "$(date -Is) watcher iniciado (fp=$prev)" >> "$LOG"
while true; do
  sleep 5
  curr="$(fingerprint)"
  if [ "$curr" != "$prev" ]; then
    sleep 5            # debounce: espera download/escrita estabilizar
    curr="$(fingerprint)"
    [ "$curr" = "$prev" ] && continue
    if python3 "$RUN" --out "$OUT" --quiet; then
      echo "$(date -Is) registry recarregado" >> "$LOG"
      prev="$curr"
    fi
  fi
done
