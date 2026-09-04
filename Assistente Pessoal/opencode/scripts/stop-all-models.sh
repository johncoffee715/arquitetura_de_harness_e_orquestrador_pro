#!/usr/bin/env bash
# stop-all-models.sh — desliga slots LLM da stack híbrida gracefully (R19)
# Uso: stop-all-models.sh            → desliga TODOS os slots LLM
#      stop-all-models.sh <porta|nome> ... → desliga só os pedidos
set -u
LOCK="/tmp/stop-all-models.sh.lock"
exec 9>"$LOCK"
if ! flock -n 9; then echo "já em execução — abortando"; exit 1; fi
ROOT="/mnt/dados/Assistente Pessoal/opencode"
ALL_PORTS=(8083 9084 9086 9088 9090 9092 9093 9095)
PORTS=(8083 9084 9086 9088 9090 9092 9093)
declare -A PORT_NAME=([gm]=8083 [cortex]=9084 [reflexo]=9086 [proposer]=9088 [refuter]=9090 [judge]=9092 [smol]=9093 [vlm]=9095)
TARGETS=()
if [ "$#" -eq 0 ]; then
  TARGETS=("${PORTS[@]}")
else
  for arg in "$@"; do
    if [[ "$arg" =~ ^[0-9]+$ ]]; then TARGETS+=("$arg")
    elif [ -n "${PORT_NAME[$arg]:-}" ]; then TARGETS+=("${PORT_NAME[$arg]}")
    else echo "[stop-all] alvo desconhecido: $arg"; fi
  done
fi
mkdir -p "$ROOT/state/watcher"

stop_graceful() {
  local port="$1"
  local pid
  pid=$(lsof -ti:"$port" 2>/dev/null | head -1)
  if [ -z "$pid" ]; then
    pid=$(pgrep -f "llama-server.*--port $port" 2>/dev/null | head -1)
  fi
  if [ -n "$pid" ]; then
    echo "[$port] Enviando SIGTERM para PID $pid"
    kill "$pid" 2>/dev/null
    local waited=0
    while [ $waited -lt 10 ]; do
      if ! kill -0 "$pid" 2>/dev/null; then
        echo "[$port] PID $pid encerrado gracefully"
        return 0
      fi
      sleep 1
      waited=$((waited+1))
    done
    if kill -0 "$pid" 2>/dev/null; then
      echo "[$port] Forçando SIGKILL após timeout em PID $pid"
      kill -9 "$pid" 2>/dev/null
    fi
  else
    echo "[$port] Nenhum processo llama-server encontrado para parar"
  fi
}

for port in "${TARGETS[@]}"; do
  if curl -sf -m 3 "http://127.0.0.1:$port/health" >/dev/null 2>&1; then
    stop_graceful "$port"
  else
    echo "[$port] já estava down"
  fi
  rm -f "$ROOT/state/watcher/.guard-fails-$port" 2>/dev/null
done

echo "--- parada concluída (${#TARGETS[@]} alvos) ---"
