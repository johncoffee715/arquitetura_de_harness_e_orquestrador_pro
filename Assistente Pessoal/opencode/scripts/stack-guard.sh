#!/usr/bin/env bash
# stack-guard.sh — SH-M1: watchdog da stack física (spec autopoiética §7)
# R21: WARM slots NÃO são vigiados — só ESSENTIAL + needles
# Health 9 LLM + needle; slot DOWN → restart cirúrgico com flags idênticas (máx 2×)
# persistindo → alerta dedupe + registro em decisoes/. Nunca reinicia :8083 durante probe.
set -u
ROOT="/mnt/dados/Assistente Pessoal/opencode"
LOG="$ROOT/state/watcher/stack-guard.log"
LOCK_PROBE="$ROOT/state/watcher/.probe-lock"
INTERVAL="${1:-60}"
mkdir -p "$(dirname "$LOG")"

# R21: WARM slots NÃO são vigiados pelo guard
ESSENTIAL_PORTS=(8083 9084)
WARM_PORTS=(9086 9088 9090 9093 9095)
NEEDLE_PORTS=(8097 9091)
ALL_PORTS=(8083 9084 9086 9088 9090 9093 9095 8097 9091)

log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

probe_ativo() { pgrep -f "alucination_probe.py" >/dev/null 2>&1; }

slot_up() { curl -sf -m 3 "http://127.0.0.1:$1/health" >/dev/null 2>&1; }

restart_slot() {
  local port="$1"
  # R21: WARM slots NÃO são restarteados pelo guard
  if [[ " ${WARM_PORTS[*]} " =~ " $port " ]]; then
    log "[$port] WARM — skip (não é slot essencial, não se revive)"
    return 0
  fi
  if [ "$port" = "8083" ] && probe_ativo; then
    log ":$port DOWN mas probe ativo — NÃO reiniciar (lock)"
    return 1
  fi
  local fails=$(cat "$ROOT/state/watcher/.guard-fails-$port" 2>/dev/null || echo 0)
  if [ "$fails" -ge 2 ]; then
    log "CRITICO :$port DOWN após $fails restarts — escalando humano"
    command -v notify-send >/dev/null && notify-send -u critical "stack-guard" "slot :$port DOWN persistente" 2>/dev/null
    echo "- $(date +%F) stack-guard: slot :$port DOWN persistente → decisão humana" >> "/mnt/dados/Assistente Pessoal/cerebro com IA/decisoes/log.md"
    return 1
  fi
  echo $((fails+1)) > "$ROOT/state/watcher/.guard-fails-$port"
  log ":$port DOWN → restart cirúrgico ($((fails+1))/2)"
  bash "$ROOT/scripts/start-stack.sh" >/dev/null 2>&1 &
}

while true; do
  for p in 8083 9084 9086 9088 9090 9092 9093; do
    if slot_up "$p"; then rm -f "$ROOT/state/watcher/.guard-fails-$p"
    else restart_slot "$p"; fi
  done
  # needles: WARM, não vigiadas pelo guard
  for p in "${NEEDLE_PORTS[@]}"; do
    slot_up "$p" >/dev/null 2>&1 || {
      pgrep -f "needle.*--port $p" >/dev/null 2>&1 || {
        [ -x "$ROOT/tools/needle2/needle" ] && (setsid nohup "$ROOT/tools/needle2/needle" --serve --port "$p" \
          --tools "$ROOT/tools/needle2/graph-tools.json" > /dev/null 2>&1 < /dev/null &) && log "$p needle reiniciado"
      }
    }
  done
  sleep "$INTERVAL"
done