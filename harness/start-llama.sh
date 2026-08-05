#!/bin/bash
# start-llama.sh — Inicia llama-server com modelo GGUF em GPU-only (Vulkan, -ngl 999)
# Uso: start-llama.sh <caminho-do-modelo.gguf> [porta] [grammar.gbnf] [contexto]
# Exemplo: start-llama.sh "modelos/ornith.gguf" 8083 json.gbnf 4096
#
# Regras da spec (engenharia de harness.md):
#   - "nunca permita o offloading de camadas para a CPU" -> -ngl 999
#   - Gramáticas GBNF estritas -> --grammar-file
#   - Contexto Gran-Mestre 4k/8k; Bonsai 16k+
set -euo pipefail

MODEL="$1"
PORT="${2:-8081}"
GRAMMAR="${3:-}"
CTX="${4:-4096}"
SLOTS="${5:-4}"
LOG_DIR="/mnt/dados/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/llama-server-$(basename "$MODEL" .gguf).log"

pkill -f llama-server 2>/dev/null || true
sleep 2

ARGS=(-m "$MODEL" -ngl 999 -dev Vulkan0 --port "$PORT" --host 127.0.0.1 -c "$CTX" -np "$SLOTS")
if [ -n "$GRAMMAR" ] && [ -f "/mnt/dados/harness/grammars/$GRAMMAR" ]; then
  ARGS+=(--grammar-file "/mnt/dados/harness/grammars/$GRAMMAR")
  echo "[start-llama] Grammar: $GRAMMAR"
fi

case "$(basename "$MODEL")" in
  ornith*)
    ARGS+=(--reasoning-preserve --jinja --cache-type-k q8_0 --cache-type-v q8_0)
    echo "[start-llama] Ornith: reasoning-preserve + jinja (tool-calling OpenAI-style)"
    echo "[start-llama] Ornith: cache KV q8_0 — contexto longo 256K suportado (limite = VRAM)"
    ;;
  nanbeige*)
    ARGS+=(--cache-type-k q8_0 --cache-type-v q8_0)
    echo "[start-llama] Nanbeige: cache KV q8_0 — CoT + múltiplas tool calls em janela longa"
    ;;
esac

echo "[start-llama] Modelo: $MODEL | Porta: $PORT | ctx: $CTX | slots: $SLOTS"
echo "[start-llama] GPU-only (-ngl 999, Vulkan0) — proibido offload CPU"
setsid /mnt/dados/llama.cpp-master/build/bin/llama-server "${ARGS[@]}" > "$LOG" 2>&1 &
echo "PID=$! LOG=$LOG"
sleep 15
grep -E "model loaded|listening|error|failed|out of memory" "$LOG" | tail -5 || true
