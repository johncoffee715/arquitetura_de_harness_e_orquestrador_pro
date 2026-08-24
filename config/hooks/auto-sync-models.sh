#!/usr/bin/env bash
# auto-sync-models.sh — Detecta mudanças nos modelos e auto-sincroniza configs
# Roda: session.start (hook), ou quando detecta gap/inconsistência

MODELS_DIR="/mnt/dados/Assistente Pessoal/modelos LLM"
SYNC_SCRIPT="/mnt/dados/harness/sync-local-models.sh"
HASH_FILE="/tmp/.local-models-hash"

# Calcular hash dos modelos disponíveis
current_hash=$(ls -la "$MODELS_DIR"/*.gguf 2>/dev/null | md5sum | cut -d' ' -f1)

# Comparar com hash anterior
if [ -f "$HASH_FILE" ]; then
  prev_hash=$(cat "$HASH_FILE")
  if [ "$current_hash" = "$prev_hash" ]; then
    exit 0  # Nada mudou
  fi
fi

# Modelo mudou ou é primeira vez — sincronizar
echo "$current_hash" > "$HASH_FILE"
bash "$SYNC_SCRIPT" 2>/dev/null
