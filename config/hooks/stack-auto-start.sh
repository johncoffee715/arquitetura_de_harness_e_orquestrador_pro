#!/usr/bin/env bash
# stack-auto-start.sh — SessionStart hook: sobe a stack de LLMs automaticamente
# Roda start-all-models.sh se nenhum servidor estiver ativo
#
# Hook: session.start (OpenCode)
# Non-blocking: inicia em background, não trava a sessão

HARNESS_DIR="/mnt/dados/harness"
START_SCRIPT="$HARNESS_DIR/start-all-models.sh"
LOG_DIR="/mnt/dados/logs"
LOCK="/tmp/stack-auto-start.lock"

# Verificar se já está rodando
if [ -f "$LOCK" ]; then
  LOCK_PID=$(cat "$LOCK" 2>/dev/null)
  if [ -n "$LOCK_PID" ] && kill -0 "$LOCK_PID" 2>/dev/null; then
    exit 0  # Já está subindo
  fi
fi

# Verificar se todos os 5 servers já estão no ar
ALIVE=0
for port in 8083 9084 9085 9086; do
  if curl -sf -m 2 "http://127.0.0.1:$port/health" >/dev/null 2>&1; then
    ALIVE=$((ALIVE+1))
  fi
done

# Bonsai na porta 9083 (CPU)
if curl -sf -m 2 "http://127.0.0.1:9083/health" >/dev/null 2>&1; then
  ALIVE=$((ALIVE+1))
fi

# Watcher Vigilante (R48) — sobe junto com o OpenCode, desanexado (R19).
# Independente da stack de LLMs: roda antes do early-exit abaixo.
WATCHER_SCRIPT="/mnt/dados/opencode/scripts/harness-monitor/watch_subagents.sh"
if [ -x "$WATCHER_SCRIPT" ] && ! pgrep -f "watch_subagents.sh" >/dev/null 2>&1; then
  setsid nohup "$WATCHER_SCRIPT" > /home/johncoffee/.opencode/state/watch_subagents.out 2>&1 < /dev/null &
  disown
  echo "$(date +%Y-%m-%dT%H:%M:%S) watcher iniciado (R48)" >> "$LOG_DIR/stack-auto-start.log"
fi

# Se todos já estão no ar, não fazer nada
[ "$ALIVE" -ge 5 ] && exit 0

# Subir stack em background
if [ -x "$START_SCRIPT" ]; then
  echo $$ > "$LOCK"
  nohup "$START_SCRIPT" >> "$LOG_DIR/stack-auto-start.log" 2>&1 &
  disown
  # Esperar um pouco e verificar
  sleep 3
  rm -f "$LOCK"
fi
