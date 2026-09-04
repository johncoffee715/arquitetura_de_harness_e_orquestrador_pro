#!/bin/bash
set -e

MODEL_DIR="/mnt/dados/Assistente Pessoal/modelos LLM"
LLAMA_CLI="/mnt/dados/Assistente Pessoal/llama.cpp/build/bin/llama-cli"
PROMPT="Explique brevemente a teoria da relatividade em tres frases."
N_TOKENS=128
THREADS=18
BATCH_SIZE=512
CTX_SIZE=8192

echo "=== BENCHMARK RWKV7-0.4B ==="
echo "Prompt: $PROMPT"
echo "Threads: $THREADS, Batch: $BATCH_SIZE, Ctx: $CTX_SIZE, N tokens: $N_TOKENS"
echo ""

for quant in FP16 BF16; do
    if [ "$quant" = "FP16" ]; then
        MODEL_FILE="RWKV7-G1d-0.4B-Instruct-FP16.gguf"
    else
        MODEL_FILE="RWKV7-0.4B-World-BF16.gguf"
    fi

    MODEL_PATH="$MODEL_DIR/$MODEL_FILE"
    if [ ! -f "$MODEL_PATH" ]; then
        echo "ERRO: $MODEL_PATH nao encontrado"
        continue
    fi

    echo "--- Testando $quant ($MODEL_FILE) ---"
    start=$(date +%s.%N)
    output=$($LLAMA_CLI         -m "$MODEL_PATH"         -p "$PROMPT"         -n $N_TOKENS         -t $THREADS         -b $BATCH_SIZE         -c $CTX_SIZE         --temp 0.7         --top-p 0.9         --repeat-penalty 1.1         2>&1)
    end=$(date +%s.%N)
    runtime=$(echo "$end - $start" | bc)

    tps=$(echo "$output" | grep -oE 'eval time[^,]*' | head -1)
    if [ -z "$tps" ]; then
        tps=$(echo "scale=2; $N_TOKENS / $runtime" | bc)
    fi

    echo "Tempo total: ${runtime}s"
    echo "Info: $tps"
    echo ""
done
