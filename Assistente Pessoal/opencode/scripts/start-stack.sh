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
# CPU 8083 · orquestrador · Ornith-1.5-35B-A3B-AD-IQ3_S-IQ3_XXS · ORQUESTRADOR (CPU, ctx fixo, threads auto)
launch 8083 "Ornith-1.5-35B-A3B-AD-IQ3_S-IQ3_XXS.gguf" \
  -c 262144 -np 1 -b 8192 -ub 2048 -ngl 0 \
  --cache-type-k q4_0 --cache-type-v q4_0 \
  --jinja --temp 0.6 --top-p 0.95 --top-k 20 \
  --chat-template-kwargs '{"enable_thinking": false}' \
  --cache-prompt

# GPU 9084 · talamus-cortex · RWKV7-G1d-0.4B-Instruct-FP16 (RWKV — state fixo, ctx nativo)
launch 9084 "RWKV7-G1d-0.4B-Instruct-FP16.gguf" \
  -c 1048576 -np 1 -b 512 -ngl 999 -dev Vulkan0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja

# GPU 9086 · reflexo · LFM2.5-1.2B-Thinking-ToMoE-Q4_K_M (FA on)
launch 9086 "LFM2.5-1.2B-Thinking-ToMoE-Q4_K_M.gguf" \
  -c 128000 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.05

# GPU 9088 · contrato-plano · granite-4.2-3b-Q4_K_M (FA on)
launch 9088 "granite-4.2-3b-Q4_K_M.gguf" \
  -c 131072 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6

# GPU 9090 · refutacao · Ternary-Bonsai-8B-Q2_0_g64 (FA on)
launch 9090 "Ternary-Bonsai-8B-Q2_0_g64.gguf" \
  -c 65536 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.8

# GPU 9092 · refutacao · Gemma-2-2B-IT-Q4_K_M (FA on)
launch 9092 "Gemma-2-2B-IT-Q4_K_M.gguf" \
  -c 8192 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.8

# GPU 9093 · descoberta · SmolLM2-360M-Instruct-Q8_0 (FA on)
launch 9093 "SmolLM2-360M-Instruct-Q8_0.gguf" \
  -c 4096 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 \
  --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6

# ── CPU · F0 TRIAGEM L0 · Needle 2 (Cactus) · 28MB RAM · confidence-gated ──
NEEDLE="$ROOT/tools/needle2/needle"
if [ -x "$NEEDLE" ] && ! pgrep -f "needle2/needle --serve" >/dev/null 2>&1; then
  (setsid nohup "$NEEDLE" --serve --port 8097 --tools "$ROOT/tools/needle2/graph-tools.json" \
    > "$LOGDIR/needle-8097.log" 2>&1 < /dev/null &)
  echo "[8097] lançando needle2 triagem L0"
fi

# ── CPU · F4 FORJA · Needle 2 (Cactus) · 29MB RAM · validação schema + tool calling ──
NEEDLE_FORJA="$ROOT/tools/needle2/needle"
FORJA_TOOLS="$ROOT/config/opencode/tools/needle2/forja-tools.json"
if [ -x "$NEEDLE_FORJA" ] && [ -f "$FORJA_TOOLS" ] && ! pgrep -f "needle --serve --port 9091" >/dev/null 2>&1; then
  (setsid nohup "$NEEDLE_FORJA" --serve --port 9091 --tools "$FORJA_TOOLS" \
    > "$LOGDIR/needle-forja-9091.log" 2>&1 < /dev/null &)
  echo "[9091] lançando needle2 forja (validate_schema/write_artifact/upsert_vault/emit_manifest)"
fi

echo "--- health check ---"
sleep 2
ok=0; total=0
for p in 8083 9084 9086 9088 9090 9092 9093; do
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