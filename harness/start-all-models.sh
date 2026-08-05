#!/bin/bash
# start-all-models.sh — Sobe os 4 modelos SIMULTANEAMENTE (GPU-only, Vulkan)
# Uso: ./start-all-models.sh
# Portas: lfm 8081 | nanbeige 8082 | ornith 8083 | bonsai 8084
#
# Orçamento VRAM (MI50 16GB HBM2):
#   pesos:  1.1 + 1.4 + 5.5 + 3.9 = 11.9GB
#   KV q8:  ~2.1GB (ctx 2048/4096/4096/4096, slots 2)
#   total:  ~14GB → cabe em 16GB
set -uo pipefail

MODELS_DIR="/mnt/dados/Assistente Pessoal/modelos LLM"
SERVER="/mnt/dados/llama.cpp-master/build/bin/llama-server"
LOG_DIR="/mnt/dados/logs"
mkdir -p "$LOG_DIR"

# Orçamento VRAM dinâmico — llama_budget.py exporta LFM_CTX/NANBEIGE_CTX/ORNITH_CTX/BONSAI_CTX e _SLOTS
if [ -f "$(dirname "$0")/llama_budget.py" ]; then
  eval "$(python3 "$(dirname "$0")/llama_budget.py" --export 2>/dev/null)"
fi

# Lock cooperativo: apenas 1 instância sobe os modelos por vez (multi-session)
# Prevê panic/loop quando 2 sessions rodam start-all simultaneamente.
exec 9>/tmp/start-all-models.sh.lock
flock -n 9 || { echo "[start-all] outra instância já está levantando os modelos — saída cooperativa"; exit 0; }

declare -A MODELS=(
  [lfm]="LFM-2.5-1.6B.Q4_K_M.gguf|8081|verdict.gbnf|2048|2"
  [nanbeige]="Nanbeige-3B.Q4_K_M.gguf|8082|verdict.gbnf|4096|2"
  [ornith]="ornith-1.0-9B.Q4_K_M.gguf|8083|none|4096|2"
  [bonsai]="Bonsai-27B-1bit.Q4_K_M.gguf|8084|code.gbnf|4096|2"
)

# Health-check ANTES do pkill: se outra sessão já subiu, reusa e desiste de
# reiniciar (custo de reinício = 0). Só relauncamos os servidores AUSENTES.
UP_BY_NAME=()
ALIVE=0
for key in lfm nanbeige ornith bonsai; do
  IFS='|' read -r _ PORT _ _ _ <<< "${MODELS[$key]}"
  if curl -sf -m 2 "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
    UP_BY_NAME[$key]=1; ALIVE=$((ALIVE+1))
  else
    UP_BY_NAME[$key]=0
  fi
done

if [ "$ALIVE" -eq 4 ]; then
  echo "[start-all] 4/4 já no ar — outra sessão deu conta; SEM pkill, SEM reinício."
  exit 0
fi
[ "$ALIVE" -gt 0 ] && echo "[start-all] reusando $ALIVE/4 já no ar (sem pkill); subindo apenas os ausentes."
if [ "$ALIVE" -eq 0 ]; then
  pkill -9 -x llama-server 2>/dev/null
  sleep 2
fi


PIDS=()
for key in lfm nanbeige ornith bonsai; do
  [ "${UP_BY_NAME[$key]:-0}" -eq 1 ] && { echo "[start-all] $key: já no ar (reusando) — pulando launch"; continue; }
  IFS='|' read -r FILE PORT GRAMMAR CTX SLOTS <<< "${MODELS[$key]}"
  # Orçamento dinâmico: vars do llama_budget.py sobrescrevem os defaults (fallback)
  case "$key" in
    lfm)      CTX="${LFM_CTX:-$CTX}";      SLOTS="${LFM_SLOTS:-$SLOTS}" ;;
    nanbeige) CTX="${NANBEIGE_CTX:-$CTX}"; SLOTS="${NANBEIGE_SLOTS:-$SLOTS}" ;;
    ornith)   CTX="${ORNITH_CTX:-$CTX}";   SLOTS="${ORNITH_SLOTS:-$SLOTS}" ;;
    bonsai)   CTX="${BONSAI_CTX:-$CTX}";   SLOTS="${BONSAI_SLOTS:-$SLOTS}" ;;
  esac
  LOG="$LOG_DIR/all-$key.log"
  ARGS=(-m "$MODELS_DIR/$FILE" -ngl 999 -dev Vulkan0 --port "$PORT" --host 127.0.0.1 \
    -c "$CTX" -np "$SLOTS")
  if [ "$GRAMMAR" != "none" ]; then
    ARGS+=(--grammar-file "/mnt/dados/harness/grammars/$GRAMMAR")
  fi
  case "$FILE" in
    ornith*|nanbeige*|Bonsai*)
      ARGS+=(--cache-type-k q8_0 --cache-type-v q8_0)
      ;;
  esac
  case "$FILE" in
    ornith*)
      ARGS+=(--reasoning-preserve --jinja --reasoning-budget 1024)
      ;;
    Bonsai*)
      ARGS+=(--reasoning-budget 1024)
      ;;
  esac
  "$SERVER" "${ARGS[@]}" > "$LOG" 2>&1 &
  PIDS+=("$!")
  echo "[start-all] $key: porta $PORT | ctx $CTX | slots $SLOTS | PID ${PIDS[-1]}"
done

echo ""
echo "[start-all] Aguardando os 4 servidores (até 120s)..."
OK=0
for i in $(seq 1 24); do
  sleep 5
  OK=0
  for key in lfm nanbeige ornith bonsai; do
    IFS='|' read -r _ PORT _ _ _ <<< "${MODELS[$key]}"
    if grep -q "listening on" "$LOG_DIR/all-$key.log" 2>/dev/null; then
      OK=$((OK+1))
    fi
  done
  echo "[start-all] $((i*5))s: $OK/4 no ar"
  [ "$OK" -eq 4 ] && break
done

echo ""
echo "════════════════════════════════════════════"
echo "STATUS FINAL: $OK/4 modelos no ar"
echo "════════════════════════════════════════════"
for key in lfm nanbeige ornith bonsai; do
  IFS='|' read -r _ PORT _ _ _ <<< "${MODELS[$key]}"
  if grep -q "listening on" "$LOG_DIR/all-$key.log" 2>/dev/null; then
    echo "  ✅ $key  → http://127.0.0.1:$PORT"
  else
    echo "  ❌ $key  → log: $LOG_DIR/all-$key.log"
    grep -iE "error|failed|out of memory|device lost" "$LOG_DIR/all-$key.log" | tail -3
  fi
done
echo ""
VRAM=$(cat /sys/class/drm/card0/device/mem_info_vram_used 2>/dev/null)
if [ -n "$VRAM" ]; then
  echo "VRAM usada: $((VRAM / 1024 / 1024))MB / 16GB"
else
  echo "VRAM: n/d"
fi
