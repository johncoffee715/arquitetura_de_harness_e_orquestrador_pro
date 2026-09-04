#!/usr/bin/env bash
# bench-kv.sh — benchmark de quantização KV + MTP (hefesto · ferramenta do harness)
# Uso: bench-kv.sh <nome> [flags-kv...]  e.g. bench-kv.sh iq4 --cache-type-k iq4_nl --cache-type-v iq4_nl
# Mede prefill t/s e decode t/s do llama-server na 8099 (doc 8K), derruba ao final.
set -u
BIN="/mnt/dados/Assistente Pessoal/opencode/llama.cpp/bin/llama-server"
MODEL="/mnt/dados/Assistente Pessoal/modelos LLM/Ornith-1.5-9B-Q5_K_M.gguf"
DOC="/tmp/opencode/bench-doc.json"
LOG="/tmp/opencode/bench-${1:-x}.log"
name="${1:-x}"; shift || true

"$BIN" -m "$MODEL" --port 8099 --host 127.0.0.1 -c 8192 -np 1 -b 2048 -ub 1024 \
  -ngl 999 -dev Vulkan0 "$@" > "$LOG" 2>&1 &
pid=$!
for i in $(seq 1 45); do curl -sf -m 2 http://127.0.0.1:8099/health >/dev/null 2>&1 && break; sleep 2; done
curl -sf -m 2 http://127.0.0.1:8099/health >/dev/null 2>&1 || { echo "[$name] FALHOU BOOT"; tail -5 "$LOG"; kill -9 $pid 2>/dev/null; exit 1; }

# aquecimento rápido
curl -s -m 30 http://127.0.0.1:8099/v1/chat/completions -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"oi"}],"max_tokens":1}' >/dev/null
# prefill doc
curl -s -m 300 http://127.0.0.1:8099/v1/chat/completions -H "Content-Type: application/json" -d @$DOC >/dev/null
# decode 60 tokens
curl -s -m 120 http://127.0.0.1:8099/v1/chat/completions -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"conte de 1 a 40 em palavras separadas por virgula"}],"max_tokens":60,"temperature":0}' >/dev/null

pf=$(grep "prompt eval time" "$LOG" | tail -1 | grep -oE "[0-9.]+ tokens per second")
ev=$(grep "eval time" "$LOG" | tail -1 | grep -oE "[0-9.]+ tokens per second")
echo "[$name] prefill=${pf:-?} t/s · decode=${ev:-?} t/s"
kill -9 $pid 2>/dev/null; sleep 2
