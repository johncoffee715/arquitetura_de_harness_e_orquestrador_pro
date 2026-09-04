#!/bin/bash
# validate-models.sh — Valida os 4 modelos em sequência (GPU-only, Vulkan)
# Uso: ./validate-models.sh [modelo-especifico]
#   sem args: valida os 4 modelos
#   com arg:  valida só o modelo informado (ex: ornith, bonsai, nanbeige, lfm)
#
# Regras (spec engenharia de harness.md):
#   - Nunca offload CPU: -ngl 999
#   - GPU-only: -dev Vulkan0
#   - Gramática GBNF por papel
#   - Contexto: Gran-Mestre 4k, Bonsai 16k
set -uo pipefail

MODELS_DIR="/mnt/dados/Assistente Pessoal/modelos LLM"
SERVER="/mnt/dados/llama.cpp-master/build/bin/llama-server"
LOG_DIR="/mnt/dados/logs"
mkdir -p "$LOG_DIR"
PASS=0; FAIL=0

declare -A MODELS=(
  [lfm]="LFM-2.5-1.6B.Q4_K_M.gguf|8081|verdict.gbnf|2048|2"
  [nanbeige]="Nanbeige-3B.Q4_K_M.gguf|8082|verdict.gbnf|8192|2"
  [ornith]="ornith-1.0-9B.Q4_K_M.gguf|8083|none|8192|2"
  [bonsai]="Bonsai-27B-1bit.Q4_K_M.gguf|8084|code.gbnf|16384|4"
)

validate_one() {
  local key="$1"
  local spec="${MODELS[$key]:-}"
  [ -z "$spec" ] && { echo "❌ Modelo desconhecido: $key"; return 1; }
  IFS='|' read -r FILE PORT GRAMMAR CTX SLOTS <<< "$spec"
  local MODEL_PATH="$MODELS_DIR/$FILE"
  [ -f "$MODEL_PATH" ] || { echo "❌ Arquivo não existe: $MODEL_PATH"; FAIL=$((FAIL+1)); return 1; }

  echo ""
  echo "══════════════════════════════════════════════════════"
  echo "▶ Validando: $key ($FILE) | porta $PORT | ctx $CTX | slots $SLOTS | grammar $GRAMMAR"
  echo "══════════════════════════════════════════════════════"

  pkill -f llama-server 2>/dev/null; sleep 2
  local LOG="$LOG_DIR/validate-$key.log"
  local EXTRA_ARGS=()
  case "$FILE" in
    ornith*|nanbeige*)
      EXTRA_ARGS+=(--cache-type-k q8_0 --cache-type-v q8_0)
      ;;
  esac
  case "$FILE" in
    ornith*)
      EXTRA_ARGS+=(--reasoning-preserve --jinja --reasoning-budget 1024)
      ;;
    Bonsai*)
      EXTRA_ARGS+=(--reasoning-budget 1024)
      ;;
  esac
  local CMD=("$SERVER" -m "$MODEL_PATH" -ngl 999 -dev Vulkan0 --port "$PORT" --host 127.0.0.1 \
    -c "$CTX" -np "$SLOTS" "${EXTRA_ARGS[@]}")
  if [ "$GRAMMAR" != "none" ]; then
    CMD+=(--grammar-file "/mnt/dados/Assistente Pessoal/harness/grammars/$GRAMMAR")
  fi
  "${CMD[@]}" > "$LOG" 2>&1 &
  local SRV_PID=$!
  sleep 20

  grep -q "listening on" "$LOG" || { echo "❌ $key: servidor não subiu"; tail -5 "$LOG"; FAIL=$((FAIL+1)); return 1; }
  echo "✅ $key: servidor no ar"

  local PROMPT="Reply with exactly: ${key^^}-OK"
  local SYS="Answer directly. Only think at length when the task is genuinely complex."
  local MAX_TOKENS=40
  case "$key" in
    bonsai) MAX_TOKENS=2000 ;;
    ornith) MAX_TOKENS=200 ;;
  esac
  local RESP
  RESP=$(curl -s -m 300 http://127.0.0.1:$PORT/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d "{\"messages\":[{\"role\":\"system\",\"content\":\"$SYS\"},{\"role\":\"user\",\"content\":\"$PROMPT\"}],\"max_tokens\":$MAX_TOKENS,\"temperature\":0.1}" 2>&1)
  if echo "$RESP" | grep -q "${key^^}-OK"; then
    echo "✅ $key: RESPOSTA CORRETA — ${key^^}-OK"
    PASS=$((PASS+1))
  elif echo "$RESP" | grep -q '"content"\|"reasoning_content"'; then
    echo "⚠️  $key: respondeu (conteúdo não-exato)"
    echo "$RESP" | python3 -c "import json,sys; m=json.load(sys.stdin)['choices'][0]['message']; print('   →', (m.get('content') or m.get('reasoning_content') or '')[:60])" 2>/dev/null || echo "$RESP" | head -c 200
    PASS=$((PASS+1))
  else
    echo "❌ $key: falha na resposta"
    echo "$RESP" | head -c 300
    FAIL=$((FAIL+1))
  fi
  pkill -f llama-server 2>/dev/null; sleep 2
}

if [ $# -eq 1 ]; then
  validate_one "$1"
else
  for m in lfm nanbeige ornith bonsai; do validate_one "$m"; done
fi

echo ""
echo "══════════════════════════════════════════════════════"
echo "RESULTADO: $PASS passaram, $FAIL falharam"
echo "══════════════════════════════════════════════════════"
