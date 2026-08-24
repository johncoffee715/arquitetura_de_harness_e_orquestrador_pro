#!/bin/bash
# start-all-models.sh — Cenário F: 1 GPU + 6 CPU (7 modelos)
# Uso: ./start-all-models.sh
# Portas: LLM Orquestrador 8083(GPU) | bonsai 9083(CPU) | qwen 9084(CPU) | lfm 9086(CPU) | qwen38-2b 9087(CPU)

#
# Arquitetura (2026-08-17, Cenário F): LLM Orquestrador sozinho na GPU (256K nativa);
# Consolidação 2026-08-18: qwen3.8-2b substituiu granite+jamba+minicpm (nível 1.5-2 + F3/F4).
# jamba/minicpm REMOVIDOS 2026-08-18 (qwen3.8-2b cobre 262K). qwen/lfm/qwen38-2b/bonsai na CPU.
#   GPU (Vulkan0, 16GB VRAM): ornith-1.0-9B → 256K ctx (KV ~9.5GB) + folga ~0.5GB
#   CPU (RAM, 31GB): bonsai 16K (F1 criativa) | qwen 256K (nível 1)
#                    lfm 128K (R42) | qwen38-2b 262K (nível 1.5-2 + F3/F4)

#
# Orçamento VRAM: ornith-1.0-9B 5.3+9.5 = 14.8GB / 16GB (folga ~0.5-1.2GB)
# Orçamento RAM:  bonsai 3.5 + qwen 0.5 + lfm 0.1 + qwen38-2b 1.3 = 5.4GB pesosrados liberam 2.5GB)sos
#                 + KV: bonsai ~1.0 + qwen ~0.5 + lfm ~0.3 + qwen38-2b ~0.85 = ~5.8GB
#                 total RAM: ~14.4GB / 31GB
set -uo pipefail

MODELS_DIR="/mnt/dados/Assistente Pessoal/modelos LLM"
SERVER="/mnt/dados/llama.cpp-master/build/bin/llama-server"
LOG_DIR="/mnt/dados/logs"
mkdir -p "$LOG_DIR"

# Lock cooperativo
exec 9>/tmp/start-all-models.sh.lock
flock -n 9 || { echo "[start-all] outra instância já está levantando os modelos — saída cooperativa"; exit 0; }

# ── Definição dos modelos ──
# Formato: arquivo|porta|grammar|ctx|slots|local(gpu|cpu)
declare -A MODELS=(
  [orchestrator]="Ornith-1.5-9B-Q4_K_M.gguf|8083|none|262144|1|gpu"
  [qwen]="Qwen3.5-0.8B.gguf|9084|none|131072|1|cpu"
      [lfm]="LFM2.5-230M-Q4_0.gguf|9086|none|128000|1|cpu"
  [qwen38-2b]="Qwen3.8-2B-Q4_K_M.gguf|9087|none|262144|1|cpu"
  [qwen31-7b]="Qwen3-1.7B-Q4_K_M.gguf|9088|none|40960|1|cpu"
  [llmjudge]="LLMJudge-Qwen2.5-3B.Q4_K_M.gguf|9085|none|32768|1|cpu"
  [ternary17]="Ternary-Bonsai-1.7B-Q2_0_g64.gguf|9089|none|32768|1|cpu"
  [ternary8b]="Ternary-Bonsai-8B-Q2_0_g64.gguf|9090|none|65536|1|cpu"
    )
KEYS=(orchestrator qwen lfm qwen38-2b qwen31-7b llmjudge ternary17 ternary8b)
N_MODELS=${#KEYS[@]}

# Health-check ANTES do pkill
declare -A UP_BY_NAME
ALIVE=0
for key in "${KEYS[@]}"; do
  IFS='|' read -r _ PORT _ _ _ _ <<< "${MODELS[$key]}"
  if curl -sf -m 2 "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
    UP_BY_NAME[$key]=1; ALIVE=$((ALIVE+1))
  else
    UP_BY_NAME[$key]=0
  fi
done

if [ "$ALIVE" -eq "$N_MODELS" ]; then
  echo "[start-all] $N_MODELS/$N_MODELS já no ar — SEM reinício."
  exit 0
fi
[ "$ALIVE" -gt 0 ] && echo "[start-all] reusando $ALIVE/$N_MODELS; subindo apenas os ausentes."
if [ "$ALIVE" -eq 0 ]; then
  # Só mata se NENHUM estiver no ar (evita derrubar modelos de outra sessão)
  for key in "${KEYS[@]}"; do
    IFS='|' read -r _ PORT _ _ _ _ <<< "${MODELS[$key]}"
    pid=$(lsof -ti :"$PORT" 2>/dev/null)
    [ -n "$pid" ] && kill -9 $pid 2>/dev/null
  done
  sleep 2
fi

# Anti-fragmentação p/ processos longevos (lição :9088 — degrade 182→11 t/s por arenas malloc)
export MALLOC_ARENA_MAX=4
export MALLOC_TRIM_THRESHOLD_=134217728

# ── Launch ──
PIDS=()
for key in "${KEYS[@]}"; do
  [ "${UP_BY_NAME[$key]:-0}" -eq 1 ] && { echo "[start-all] $key: reusando — pulando"; continue; }
  IFS='|' read -r FILE PORT GRAMMAR CTX SLOTS LOCAL <<< "${MODELS[$key]}"
  LOG="$LOG_DIR/all-$key.log"

  ARGS=(-m "$MODELS_DIR/$FILE" --port "$PORT" --host 127.0.0.1 \
    -c "$CTX" -np "$SLOTS" --flash-attn on -b 512)

  # R56 (2026-08-19, regra de ouro): TODOS os modelos usam -t 18 (núcleos físicos)
  # — empírico: ornith-1.0-9B t18=69,5 vs t36=63,9 t/s decode (hyperthreading não ajuda;
  #   GPU faz o trabalho, threads só alimentam). -t 12 já degradou 52→2,4 (R46).
  ARGS+=(-t 18)

  # GPU vs CPU
  if [ "$LOCAL" = "gpu" ]; then
    ARGS+=(-ngl 999 -dev Vulkan0 --kv-unified --context-shift --keep 4096 --cache-reuse 512)
  fi
  # CPU: sem -ngl, sem -dev

  # Grammar
  if [ "$GRAMMAR" != "none" ]; then
    ARGS+=(--grammar-file "/mnt/dados/harness/grammars/$GRAMMAR")
  fi

  ARGS+=(--cache-type-k q4_0 --cache-type-v q4_0)  # R71-b CPU: backend GGML tem kernel q4_0 nativo (o colapso 770→82 era VULKAN/GPU); economiza 31% KV RAMrtido com dados

  # Modelos específicos
  case "$FILE" in
    Qwen3.8-9B*)  ARGS+=(--jinja --temp 0.6 --top-p 0.95 --top-k 20 --chat-template-kwargs '{"enable_thinking": false}' --cache-type-k q5_0) ;;  # R60-v5
    Ornith-1.5*)  ARGS+=(--jinja --temp 0.6 --top-p 0.95 --top-k 20 --chat-template-kwargs '{"enable_thinking": false}' --cache-type-k q5_0 -b 2048 -ub 1024) ;;  # reserva R66
    Bonsai*)     ARGS+=(--reasoning-budget 1024 --temp 0.8 --cache-type-k q5_0) ;;  # R71-audit: KV 104→80 KB/tok
    Qwen3.5*)    ARGS+=(--jinja --reasoning-budget 1024 --temp 1.0) ;;
    LFM2.5*)     ARGS+=(--temp 0.4) ;;
    LLMJudge*)   ARGS+=(--temp 0.15) ;;
    Qwen3-1.7B*) ARGS+=(--temp 0.6) ;;
    qwen2.5-coder*) ARGS+=(--jinja --rope-scaling yarn --rope-scale 4.0) ;;
    Qwen3.8-2B*) ARGS+=(--jinja --temp 0.3) ;;
    Qwen3.8-4B*) ARGS+=(--jinja --reasoning-preserve --temp 0.7 --chat-template-kwargs '{"enable_thinking": false}') ;;
        MiniCPM5*) ARGS+=(--jinja) ;;
  esac

  # R19: launch desanexado (setsid) — fecha fd 9 no filho p/ liberar lock; exec mantém $! = PID real
  setsid bash -c 'exec 9>&-; exec "$@"' _ "$SERVER" "${ARGS[@]}" \
    > "$LOG" 2>&1 < /dev/null & disown
  PIDS+=("$!")
  echo "[start-all] $key: porta $PORT | ctx $CTX | slots $SLOTS | $LOCAL | PID ${PIDS[-1]}"
done

# ── Aguardar health ──
echo ""
echo "[start-all] Aguardando $N_MODELS servidores (até 180s)..."
OK=0
for i in $(seq 1 36); do
  sleep 5
  OK=0
  for key in "${KEYS[@]}"; do
    IFS='|' read -r _ PORT _ _ _ _ <<< "${MODELS[$key]}"
    if curl -sf -m 2 "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
      OK=$((OK+1))
    fi
  done
  echo "[start-all] $((i*5))s: $OK/$N_MODELS no ar"
  [ "$OK" -eq "$N_MODELS" ] && break
done

echo ""
echo "════════════════════════════════════════════"
echo "STATUS FINAL: $OK/$N_MODELS modelos no ar"
echo "════════════════════════════════════════════"
for key in "${KEYS[@]}"; do
  IFS='|' read -r _ PORT _ _ _ LOCAL <<< "${MODELS[$key]}"
  if curl -sf -m 2 "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
    echo "  ✅ $key  → http://127.0.0.1:$PORT ($LOCAL)"
  else
    echo "  ❌ $key  → log: $LOG_DIR/all-$key.log"
    grep -iE "error|failed|out of memory|device lost" "$LOG_DIR/all-$key.log" | tail -3
  fi
done
echo ""
VRAM=$(cat /sys/class/drm/card0/device/mem_info_vram_used 2>/dev/null)
if [ -n "$VRAM" ]; then
  echo "VRAM: $((VRAM / 1024 / 1024))MB / 16GB"
fi
echo "RAM: $(free -h | awk '/Mem:/{print $3 " / " $2}')"

# R68 — watchers iniciam com o orquestrador (vigias seguem o primário)
for u in gran-mestre-wd.service config-watcher.service llm-usage@8083.service; do
  systemctl --user is-active --quiet "$u" 2>/dev/null || systemctl --user start "$u" 2>/dev/null || true
done
systemctl --user is-enabled --quiet gran-mestre-wd.service 2>/dev/null || systemctl --user enable gran-mestre-wd.service 2>/dev/null || true
echo "[start-all] R68: watchers garantidos (wd modular · config-watcher · llm-usage@8083)"
