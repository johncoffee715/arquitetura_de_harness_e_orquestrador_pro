#!/usr/bin/env bash
# restart-stack.sh — relançamento canônico TOTAL (8 slots LLM + 2 daemons needle)
# FONTE: reference/stack-final-flags.json (NUNCA o manifesto stale, NUNCA memória).
# Idempotente: pula porta com /health 200. Tudo desanexado (setsid).
# Uso: bash restart-stack.sh   (pós-reboot, pós-incidente, pós-stale-config)
set -u
BIN="/mnt/dados/Assistente Pessoal/opencode/llama.cpp/bin/llama-server"
MDL="/mnt/dados/Assistente Pessoal/modelos LLM"
QAD="/mnt/dados/Assistente Pessoal/modelos LLM/filtragem"
NDL="/mnt/dados/Assistente Pessoal/opencode/tools/needle2/needle"
NDT="/mnt/dados/Assistente Pessoal/opencode/tools/needle2"
CFG="/mnt/dados/Assistente Pessoal/opencode/config/opencode/tools/needle2"
mkdir -p /tmp/opencode
up() { curl -s -m 2 -o /dev/null -w "%{http_code}" "http://127.0.0.1:$1/health" 2>/dev/null || echo 000; }
launch() { local p="$1"; shift
  if [ "$(up "$p")" = "200" ]; then echo "slot $p UP, pulando"; return 0; fi
  setsid nohup "$BIN" "$@" > "/tmp/opencode/slot-$p.log" 2>&1 < /dev/null & disown
  echo "slot $p lançado pid $!"; }
waitup() { local p="$1" n="${2:-150}" i c
  for i in $(seq 1 "$n"); do c="$(up "$p")"
    if [ "$c" = "200" ]; then echo "slot $p UP"; return 0; fi; sleep 2; done
  echo "slot $p TIMEOUT (ver /tmp/opencode/slot-$p.log)"; return 1; }
needleup() { local p="$1" t="$2"
  if curl -s -m 5 -o /dev/null -X POST "http://127.0.0.1:$p/complete" -H 'Content-Type: application/json' -d '{"input":"ping"}'; then echo "needle $p OK"; return 0; fi
  setsid nohup "$NDL" --serve --port "$p" --tools "$t" > "/tmp/opencode/needle-$p.log" 2>&1 < /dev/null & disown
  sleep 3
  curl -s -m 10 -o /dev/null -X POST "http://127.0.0.1:$p/complete" -H 'Content-Type: application/json' -d '{"input":"ping"}' && echo "needle $p OK" || { echo "needle $p FALHOU"; return 1; }; }
KV="--cache-type-k q4_0 --cache-type-v q4_0"
launch 8083 -m "$MDL/Qwen3.5-35B-A3B-UD-IQ3_XXS.gguf" --port 8083 --host 127.0.0.1 -c 262144 -np 1 -b 2048 -ub 512 -ngl 0 $KV --jinja --temp 0.6 --top-p 0.95 --top-k 20 --chat-template-kwargs '{"enable_thinking": false}' --spec-type draft-simple --spec-draft-model "$MDL/Qwen3.5-0.8B-Q4_K_M.gguf" --spec-draft-ngl 999 --spec-draft-type-k q4_0 --spec-draft-type-v q4_0 --spec-draft-n-max 8 --spec-draft-p-min 0.75
launch 9084 -m "$MDL/RWKV7-G1d-0.4B-Instruct-FP16.gguf" --port 9084 --host 127.0.0.1 -c 1048576 -np 1 -b 512 -ngl 999 -dev Vulkan0 $KV --jinja
launch 9093 -m "$MDL/SmolLM2-360M-Instruct-Q8_0.gguf" --port 9093 --host 127.0.0.1 -c 4096 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 $KV --jinja --temp 0.6
launch 9086 -m "$MDL/LFM2.5-1.2B-Thinking-ToMoE-Q4_K_M.gguf" --port 9086 --host 127.0.0.1 -c 128000 -np 1 --flash-attn on -b 2048 -ub 512 -ngl 999 -dev Vulkan0 $KV --jinja --temp 0.05
launch 9088 -m "$MDL/Llama-3.2-1B-Instruct-IQ4_XS.gguf" --port 9088 --host 127.0.0.1 -c 131072 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 $KV --jinja --temp 0.6
launch 9090 -m "$MDL/Llama-3.2-3B-Instruct-UD-IQ3_XXS.gguf" --port 9090 --host 127.0.0.1 -c 32768 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 $KV --jinja --temp 0.6
launch 9092 -m "$MDL/smollm2-1.7b-instruct-q4_k_m.gguf" --port 9092 --host 127.0.0.1 -c 32768 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 $KV --jinja --temp 0.6
launch 9095 -m "$MDL/Qwen1.5-MoE-A2.7B-Q3_K_M.gguf" --port 9095 --host 127.0.0.1 -c 8192 -np 1 -b 512 -ngl 0 $KV --jinja --temp 0.6 --top-p 0.95 --top-k 20
for p in 9084 9093 9086 9088 9090 9092 9095 8083; do waitup "$p" 150; done
needleup 8097 "$NDT/graph-tools.json"
needleup 9091 "$CFG/forja-tools.json"
needleup 9099 "$CFG/secretario-tools.json"
echo "=== RESUMO ==="
for p in 8083 9084 9086 9088 9090 9092 9093 9095; do printf "%s:%s " "$p" "$(up "$p")"; done; echo
