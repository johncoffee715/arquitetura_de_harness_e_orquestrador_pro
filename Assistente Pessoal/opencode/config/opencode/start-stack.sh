#!/usr/bin/env bash
# Start stack for executor-f4
set -e

# Configuration
RUNTIME="python"
MODEL_PATH="/mnt/dados/Assistente Pessoal/opencode/config/opencode/models/granite-4.2-3b"
CONTEXT_SIZE=163840

# Check if model file exists
if [ ! -f "$MODEL_PATH" ]; then
  echo "Model file not found: $MODEL_PATH"
  exit 1
fi

# Start the stack with the specified context window
echo "Starting stack with context window: $CONTEXT_SIZE"
echo "Model: $MODEL_PATH"

# Start the model server
python -m llama.cpp \
  --model "$MODEL_PATH" \
  --n_ctx "$CONTEXT_SIZE" \
  --n_gpu_layers 999 \
  --temp 0.7 \
  --top_p 0.9 \
  --stop_tokens ["\n", "-----"] \
  --device cuda:0 \
  --framework llama \
  --tensor-config {
    "n_ctx": $CONTEXT_SIZE,
    "n_gpu_layers": 999
  }

echo "Stack started successfully with context window: $CONTEXT_SIZE"