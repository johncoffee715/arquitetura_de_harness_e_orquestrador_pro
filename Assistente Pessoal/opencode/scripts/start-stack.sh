#!/usr/bin/env bash
# start-stack.sh — sobe todos os slots LLM da stack híbrida (idempotente)
# GPU MI50: :8083 orquestrador · CPU: micro-slots especialistas
# Modo WARM (R21/R58): slots sob demanda, só ESSENTIAL sobem por padrão
# Fonte de física: manifesto_llm.json (R65/R66) — flags por slot fixadas por crivo
set -u
ROOT="/mnt/dados/Assistente Pessoal/opencode"
BIN="$ROOT/llama.cpp/bin/llama-server"
MODELS="/mnt/dados/Assistente Pessoal/modelos LLM"
LOGDIR="$ROOT/state/watcher"
mkdir -p "$LOGDIR"

# ── MODELO WARM (R21/R58): sobe SÓ sob demanda ──
MODE_WARM=${MODE_WARM:-1}
MODE_WARM_PORTS=(9086 9088 9090 9092 9093 9095)

# ── PORTAS CANÔNICAS ──
ESSENTIAL_PORTS=(8083 9084 9092 9093)
WARM_PORTS=(9086 9088 9090 9092 9093 9095)
NEEDLE_PORTS=(8097 9091)
ALL_PORTS=(8083 9084 9086 9088 9090 9092 9093 9095 8097 9091)
# 9085/9087 intencionalmente DOWN — adaptados para Gemma 9092 (R71 dual), qwen38-2b sem GGUF — wd-modular não deve reportar como falha

# ── FUNÇÃO DE LAUNCH (R19: idempotente, setsid nohup, desanexado) ──
launch() { # $1=port $2=model $3...=flags extras
  local port="$1"; local model="$2"; shift 2
  # R19: health check idempotente — se já UP, skip
  if curl -sf -m 2 "http://127.0.0.1:$port/health" >/dev/null 2>&1; then
    echo "[$port] já ativo — skip"
    return 0
  fi
  # R58: WARM slots só sobem sob demanda
  if [ "$MODE_WARM" -eq 1 ] && [[ " ${MODE_WARM_PORTS[*]} " =~ " $port " ]]; then
    echo "[$port] WARM — skip (sob demanda: ${MODE_WARM_PORTS[*]})"
    return 0
  fi
  # launch desanexado R19: setsid + nohup, stdout/stderr para log
  (setsid nohup "$BIN" -m "$MODELS/$model" --port "$port" --host 127.0.0.1 \
    "$@" > "$LOGDIR/llama-$port.log" 2>&1 < /dev/null &)
  echo "[$port] lançando $model"
}

# ── GPU MI50 · ORQUESTRADOR (:8083) · Ornith-Q5 · ctx DINÂMICO por VRAM (rocm-smi) ──
# R62 empírico: KV q4/q4 ≈ 11KB/tok → 9.10GB VRAM = 258432 (n_ctx_train 262144)
# R24: folga ≥ 200MB; custo KV q4_0/q4_0 ≈ 57KB/tok (empírico R60)
compute_ornith_ctx() {
  local total used avail kv_budget max_ctx
  total=$(rocm-smi --showmeminfo vram 2>/dev/null | grep "VRAM Total Memory" | grep -oP '\d+$' | head -1)
  used=$(rocm-smi --showmeminfo vram 2>/dev/null | grep "VRAM Total Used Memory" | grep -oP '\d+$' | head -1)
  [ -z "$total" ] || [ -z "$used" ] && { echo 27136; return; }
  avail=$((total - used))
  # pesos Q5_K_M ≈ 6.2GiB + compute buffers ≈ 0.8GiB + margem 0.5GiB
  kv_budget=$((avail - 5850000000 - 800000000 - 500000000))
  [ "$kv_budget" -lt 100000000 ] && { echo 27136; return; }
  max_ctx=$((kv_budget / 11268))
  max_ctx=$((max_ctx - (max_ctx % 128)))
  [ "$max_ctx" -gt 258432 ] && max_ctx=258432
  [ "$max_ctx" -lt 8192 ] && max_ctx=8192
  echo "$max_ctx"
}
ORNITH_CTX=$(compute_ornith_ctx)
echo "[8083] ctx dinâmico = $ORNITH_CTX (rocm-smi)"
# ══ SEÇÃO GERADA por sync-llm-stack.py · FONTE: manifesto_llm.json (não editar à mão) ══
# HIBRIDO 8083 · orquestrador · Qwen3.5-35B-A3B-UD-IQ3_XXS · ORQUESTRADOR (ngl 36, b 4096/ub 1024)
launch 8083 "Qwen3.5-35B-A3B-UD-IQ3_XXS.gguf" \
  -c 262144 -np 1 -b 4096 -ub 1024 -ngl 36 -dev Vulkan0 \
  --cache-type-k q4_0 --cache-type-v q4_0 \
  --jinja --temp 0.6 --top-p 0.95 --top-k 20 \
  --chat-template-kwargs '{"enable_thinking": false}'

# GPU 9084 · talamus-cortex · RWKV7-G1d-0.4B-Instruct-FP16 (RWKV — state fixo, ctx nativo)
launch 9084 "RWKV7-G1d-0.4B-Instruct-FP16.gguf" \
  -c 1048576 -np 1 -b 512 -ngl 999 -dev Vulkan0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja

# CPU 9086 · reflexo · LFM2.5-1.2B-Thinking-ToMoE-Q4_K_M
launch 9086 "LFM2.5-1.2B-Thinking-ToMoE-Q4_K_M.gguf" \
  -c 128000 -np 1 --flash-attn on -b 512 -ngl 0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.05

# GPU 9088 · contrato-plano · Llama-3.2-1B-Instruct-IQ4_XS (FA on)
launch 9088 "Llama-3.2-1B-Instruct-IQ4_XS.gguf" \
  -c 131072 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6

# CPU 9090 · refutacao · Llama-3.2-3B-Instruct-UD-IQ3_XXS
launch 9090 "Llama-3.2-3B-Instruct-UD-IQ3_XXS.gguf" \
  -c 32768 -np 1 --flash-attn on -b 512 -ngl 0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6

# CPU 9092 · relay · SmolLM2-1.7B-Instruct-Q4_K_M
launch 9092 "smollm2-1.7b-instruct-q4_k_m.gguf" \
  -c 32768 -np 1 --flash-attn on -b 512 -ngl 0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6

# GPU 9093 · descoberta · SmolLM2-360M-Instruct-Q8_0 (FA on)
launch 9093 "SmolLM2-360M-Instruct-Q8_0.gguf" \
  -c 4096 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6

# CPU 9094 · embedder · Qwen3-Embedding-0.6B-Q8_0 (embedding, pooling last)
launch 9094 "Qwen3-Embedding-0.6B-Q8_0.gguf" \
  -c 2048 -np 1 --flash-attn on -b 512 -ngl 0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.0 --embedding --pooling last

# CPU 9095 · descoberta · Qwen1.5-MoE-A2.7B-Q3_K_M
launch 9095 "Qwen1.5-MoE-A2.7B-Q3_K_M.gguf" \
  -c 8192 -np 1 --flash-attn on -b 512 -ngl 0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6

# GPU 9097 · embedder · Qwen3-Embedding-0.6B-Q8_0-GPU (embedding, pooling last)
launch 9097 "Qwen3-Embedding-0.6B-Q8_0.gguf" \
  -c 2048 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.0 --embedding --pooling last

# ── Needle 2 · binários nativos idempotentes (W9 2026-09-15) ──
# API real do binário: needle --serve --port N --tools <json> · POST /complete · POST /reset (sem /health → liveness via pgrep+ss)
NEEDLE_BIN="$ROOT/tools/needle2/needle"
NEEDLE_GRAPH_TOOLS="$ROOT/tools/needle2/graph-tools.json"
NEEDLE_FORJA_TOOLS="$ROOT/config/opencode/tools/needle2/forja-tools.json"
start_needle() { # $1=name $2=port $3=tools.json — idempotente: skip se porta já viva
  local name="$1" port="$2" tools="$3"
  if pgrep -f "needle --serve --port $port" >/dev/null 2>&1 || ss -ltn 2>/dev/null | grep -q ":$port "; then
    echo "[$port] needle2 $name já ativo — skip"
    return 0
  fi
  [ -x "$NEEDLE_BIN" ] || { echo "[$port] needle2 $name: binário ausente ($NEEDLE_BIN)"; return 0; }
  [ -f "$tools" ] || { echo "[$port] needle2 $name: tools ausente ($tools)"; return 0; }
  (setsid nohup "$NEEDLE_BIN" --serve --port "$port" --tools "$tools" \
    > "$LOGDIR/needle-$name-$port.log" 2>&1 < /dev/null &)
  echo "[$port] lançando needle2 $name (tools=$(basename "$tools"))"
}
# CPU · F0 TRIAGEM L0 · graph :8097 (triage_route/run_shell/delegate_task) · acoplado talâmico/triagem
start_needle "graph" 8097 "$NEEDLE_GRAPH_TOOLS"
# CPU · F4 FORJA · forja :9091 (validate_schema/write_artifact/upsert_vault/emit_manifest) · acoplado executor/planejador
start_needle "forja" 9091 "$NEEDLE_FORJA_TOOLS"

# ── BIBLIOTECARIO WATCHER (R94 gerente, 92 dirs, inotify Payload real) ──
if ! pgrep -f "bibliotecario/tooling/watcher.py" >/dev/null 2>&1; then
  (setsid nohup python3 "$HOME/.config/opencode/skills/bibliotecario/tooling/watcher.py" > /tmp/opencode/bibliotecario-watcher.log 2>&1 < /dev/null &)
  echo "[watcher] lançando bibliotecario watcher"
fi

echo "--- health check ---"
sleep 2
ok=0; total=0
for p in 8083 9084 9086 9088 9090 9092 9093 9094 9095 9097; do
  total=$((total+1))
  for i in $(seq 1 45); do
    if [ "$p" = "8097" ] || [ "$p" = "9091" ]; then
      curl -sf -m 2 -X POST "http://127.0.0.1:$p/complete" -H "Content-Type: application/json" -d '{"prompt":"ping","max_tokens":1}' >/dev/null 2>&1 && break
    else
      curl -sf -m 2 "http://127.0.0.1:$p/health" >/dev/null 2>&1 && break
    fi
    sleep 2
  done
  if [ "$p" = "8097" ] || [ "$p" = "9091" ]; then
    if curl -sf -m 2 -X POST "http://127.0.0.1:$p/complete" -H "Content-Type: application/json" -d '{"prompt":"ping","max_tokens":1}' >/dev/null 2>&1; then echo "[$p] OK"; ok=$((ok+1)); else echo "[$p] FALHOU — ver $LOGDIR/llama-$p.log"; fi
  else
    if curl -sf -m 2 "http://127.0.0.1:$p/health" >/dev/null 2>&1; then echo "[$p] OK"; ok=$((ok+1)); else echo "[$p] FALHOU — ver $LOGDIR/llama-$p.log"; fi
  fi
done
echo "health $ok/$total"