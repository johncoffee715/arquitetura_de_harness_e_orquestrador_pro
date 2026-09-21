#!/bin/bash
# respawn.sh — relançamento canônico por-slot (FIX 2026-09-17, watchdog-STALE).
# ESCOLHA DOCUMENTADA (variante mais simples que respeita a fonte canônica única):
# full-stack via start-all-models.sh foi DESCARTADO porque (a) SERVER=
# /mnt/dados/llama.cpp-master/... inexistente (erro em logs/all-qwen.log), (b) a
# tabela MODELS referencia .gguf deletados (Qwen3.5-0.8B, LLMJudge, Qwen3.8-2B/9B,
# Qwen3-1.7B, LFM2.5-230M), e (c) start-stack.sh / stack-final-flags.json /
# llm-inventory.json citados no diagnóstico NÃO existem no disco. Fonte canônica
# única adotada: modelos LLM/manifesto_llm.json (slug+ctx+ngl+device por slot) +
# padrão de flags vivo em /proc/<pid>/cmdline dos slots saudáveis.
# wd.sh chama este script SEM args a cada slot DOWN; cada alvo tem guarda
# idempotente (sobe só o ausente, NUNCA mata processo alheio).
CANON_SERVER="/mnt/dados/Assistente Pessoal/programas de apoio/opencode/llama.cpp/bin/llama-server"
MODELS_DIR="/mnt/dados/Assistente Pessoal/modelos LLM"
WATCH_LOG_DIR="/mnt/dados/Assistente Pessoal/harness/state/watcher"
WD_LOG="/mnt/dados/Assistente Pessoal/harness/logs/wd-modular.log"
mkdir -p "$WATCH_LOG_DIR"
log() { echo "[$(date '+%F %T')] $*" >> "$WD_LOG"; }
health() { curl -sf -m 3 "http://127.0.0.1:$1/health" >/dev/null 2>&1; }
# Guarda-VRAM (ComfyUI da outra sessão): slots GPU (ngl!=0) só sobem com folga
# >= GPU_MIN_FREE_MB; sob pressão o relançamento é ADIADO (log + retry próximo
# ciclo), nunca disputa VRAM. Slots CPU (ngl 0) sempre podem voltar (custo zero).
GPU_MIN_FREE_MB=1500
vram_free_mb() { # imprime MB livres, ou -1 se rocm-smi indisponível (fail-open)
  local total used
  total=$(rocm-smi --showmeminfo vram 2>/dev/null | awk '/Total Memory/{print $NF}' | head -1)
  used=$(rocm-smi --showmeminfo vram 2>/dev/null | awk '/Total Used Memory/{print $NF}' | head -1)
  if [ -n "$total" ] && [ -n "$used" ] && [ "$total" -gt 0 ] 2>/dev/null; then
    echo $(( (total - used) / 1024 / 1024 ))
  else
    echo "-1"
  fi
}
launch() { # $1=port $2=file $3=ctx $4=ngl $5+=extra-args
  local PORT="$1" FILE="$2" CTX="$3" NGL="$4"; shift 4
  health "$PORT" && { log "respawn: :$PORT já saudável — pulando"; return 0; }
  if [ "$NGL" != "0" ]; then
    local FREE_MB
    FREE_MB=$(vram_free_mb)
    if [ "$FREE_MB" -ge 0 ] && [ "$FREE_MB" -lt "$GPU_MIN_FREE_MB" ]; then
      log "respawn: :$PORT ADIADO — VRAM livre ${FREE_MB}MB < ${GPU_MIN_FREE_MB}MB (ComfyUI/outra sessão?); retry próximo ciclo"
      return 1
    fi
  fi
  if pgrep -f -- "llama-server.*--port $PORT" >/dev/null 2>&1; then
    log "respawn: :$PORT já em (re)inicialização (PID próprio/antigo) — pulando, SEM kill"
    return 0
  fi
  if ss -tln 2>/dev/null | grep -q "127.0.0.1:$PORT"; then
    log "respawn: :$PORT ocupada por processo estranho sem saúde — SEM kill (política); pular"
    return 1
  fi
  if [ ! -f "$MODELS_DIR/$FILE" ]; then
    log "respawn: :$PORT .gguf ausente ($FILE) — não há o que lançar; pular"
    return 1
  fi
  log "respawn: subindo :$PORT ($FILE ctx=$CTX ngl=$NGL)"
  setsid "$CANON_SERVER" -m "$MODELS_DIR/$FILE" --port "$PORT" --host 127.0.0.1 \
    -c "$CTX" -np 1 -b 512 -ngl "$NGL" -dev Vulkan0 \
    --flash-attn on --cache-type-k q4_0 --cache-type-v q4_0 --jinja "$@" \
    >> "$WATCH_LOG_DIR/llama-$PORT.log" 2>&1 < /dev/null & disown
  log "respawn: :$PORT lançado PID $!"
}
# 9084 RWKV7-G1d-0.4B (GPU, ctx 1048576) · 9088 Llama-3.2-1B (GPU, ctx 131072).
# 9086 LFM2.5-1.2B-Thinking (CPU, ctx 128000) — --flash-attn on OBRIGATÓRIO
#   (q4_0 V-cache exige FA neste build; manifesto "flash false" REFUTADO 2026-09-18)
#   + --reasoning off --reasoning-budget 0 (thinking-only sem isso; relay/GBNF
#   precisa de content direto; --chat-template-kwargs enable_thinking DEPRECATED).
# 9092 SmolLM2-1.7B (CPU, ctx 32768; servidor capa p/ 8192 train — benigno).
# 9093 SmolLM2-360M (CPU, ctx 4096). 9094 Qwen3-Embedding (CPU, ctx 2048).
# 9097 Embedding-GPU DESCONTINUADO 2026-09-18 (ordem usuário): política CPU-only
#   p/ embeddings — processo desligado, fora do respawn e do watchdog. :9094 CPU
#   é o único embedder canônico (0 VRAM, tempo-real).
# 9085/9087: .gguf deletados do disco — sem relançamento possível (ver decision-log).
launch 9084 "RWKV7-G1d-0.4B-Instruct-FP16.gguf" 1048576 999
launch 9088 "Llama-3.2-1B-Instruct-IQ4_XS.gguf" 131072 999 --temp 0.6
launch 9090 "Llama-3.2-3B-Instruct-UD-IQ3_XXS.gguf" 32768 0 --temp 0.6
launch 9086 "LFM2.5-1.2B-Thinking-ToMoE-Q4_K_M.gguf" 128000 0 --temp 0.05 --reasoning off --reasoning-budget 0
launch 9092 "smollm2-1.7b-instruct-q4_k_m.gguf" 32768 0 --temp 0.6
launch 9093 "SmolLM2-360M-Instruct-Q8_0.gguf" 4096 0 --temp 0.6
launch 9094 "Qwen3-Embedding-0.6B-Q8_0.gguf" 2048 0 --temp 0.0 --embedding --pooling last
log "respawn canônico concluído (7 slots idempotentes + guarda-VRAM 1500MB p/ GPU)"
