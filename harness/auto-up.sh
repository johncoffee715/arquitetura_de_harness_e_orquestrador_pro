#!/bin/bash
# auto-up.sh — Automatiza o stack nativo llama.cpp (idempotente):
#   1. Sobe os 4 modelos (8081-8084) se não estiverem no ar
#   2. Aguarda health check nos 4 endpoints
#   3. Valida inferência real em cada endpoint
#   4. Emite relatório JSON (para orquestrador + redflags)
# Uso: ./auto-up.sh [--quiet]
# Saída: /mnt/dados/logs/auto-up-<ts>.json  (fonte de verdade do estado)
set -uo pipefail

MODELS_DIR="/mnt/dados/Assistente Pessoal/modelos LLM"
HARNESS="/mnt/dados/harness"
LOG_DIR="/mnt/dados/logs"
mkdir -p "$LOG_DIR"
QUIET="${1:-}"
TS="$(date +%Y%m%d-%H%M%S)"
OUT="$LOG_DIR/auto-up-$TS.json"

# --- modelo -> porta/esperado ---
declare -A PORTS=( [lfm]=8081 [nanbeige]=8082 [ornith]=8083 [bonsai]=8084 )

report() {  # report <key> <status> <detail>
  printf '  {"model":"%s","status":"%s","detail":"%s"}' "$1" "$2" "$3"
  [ -n "$QUIET" ] || echo "  [$1] $2 — $3"
}

# 1+2: garante stack no ar (chama start-all-models.sh que já é idempotente p/ staging)
if ! curl -s -m 3 http://127.0.0.1:8083/health >/dev/null 2>&1; then
  [ -n "$QUIET" ] || echo "[auto-up] stack nativo fora do ar — subindo..."
  bash "$HARNESS/start-all-models.sh" > "$LOG_DIR/auto-up-start.log" 2>&1 || true
fi

# 2: aguarda até os 4 responderem (máx 120s)
for i in $(seq 1 24); do
  OK=0
  for p in 8081 8082 8083 8084; do
    [ "$(curl -s -m 3 http://127.0.0.1:$p/health 2>/dev/null)" = '{"status":"ok"}' ] && OK=$((OK+1))
  done
  [ "$OK" -eq 4 ] && break
  sleep 5
done

# 3: valida inferência real + monta JSON / redflags
{
  echo '['
  FIRST=1
  for key in lfm nanbeige ornith bonsai; do
    p=${PORTS[$key]}
    if [ "$(curl -s -m 3 http://127.0.0.1:$p/health 2>/dev/null)" != '{"status":"ok"}' ]; then
      [ $FIRST -eq 0 ] && echo ','; FIRST=0
      report "$key" "DOWN" "health check falhou -> cloud fallback + redflag"
      continue
    fi
    # inferência: modelo de gramática restritiva pode devolver texto curto; aceitamos 200/3xx com corpo
    code=$(curl -s -o /tmp/auto-up-test.json -w '%{http_code}' -m 30 \
      http://127.0.0.1:$p/v1/chat/completions \
      -H "Content-Type: application/json" \
      -d "{\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}],\"max_tokens\":4,\"temperature\":0}")
    if [ "$code" = "200" ] && grep -q '"choices"' /tmp/auto-up-test.json; then
      [ $FIRST -eq 0 ] && echo ','; FIRST=0
      report "$key" "OK" "http://127.0.0.1:$p (llama.cpp Vulkan)"
    else
      [ $FIRST -eq 0 ] && echo ','; FIRST=0
      report "$key" "FAIL" "http $code — cloud fallback + redflag"
    fi
  done
  echo ''
  echo ']'
} > "$OUT"

# sintetiza resumo (aujda p/ humano)
UP=$(grep -c '"status":"OK"' "$OUT" || true)
echo "==== auto-up resumo: $UP/4 modelos nativos OK ====" > "$LOG_DIR/auto-up-status.txt"
cat "$OUT" >> "$LOG_DIR/auto-up-status.txt"

[ -n "$QUIET" ] || cat "$LOG_DIR/auto-up-status.txt"

# últimas métricas reais
if [ -r /sys/class/drm/card0/device/mem_info_vram_used ]; then
  echo "VRAM usada: $(awk '{printf "%.0fMB", $1/1024/1024}' /sys/class/drm/card0/device/mem_info_vram_used) / 16GB"
fi
echo "Relatório: $OUT"
exit 0