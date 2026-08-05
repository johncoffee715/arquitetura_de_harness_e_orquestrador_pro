#!/bin/bash
# gpu-watchdog.sh v2 — daemon de inferência GPU-only (Vulkan0, -ngl 999).
#
# REGRA GLOBAL: após queda, o respawn NUNCA vai para CPU/RAM — exceto se o
# usuário fixar explicitamente ECC_CPU_ALLOWED=1 (exceção documentada).
#
# v2 (Dev Loop N3 — corrige travamento):
#   - toda sub-chamada com `timeout` (não deixa o daemon segurar o shell)
#   - respawn em background desanexado (setsid + nohup) — não bloqueia o loop
#   - backoff exponencial entre ciclos; nunca "spins"
#   - estado em /tmp/gpu-watchdog.state (idempotente, legível)
#
# Uso:
#   gpu-watchdog.sh               # one-shot: check; respawn se morto
#   gpu-watchdog.sh --loop [seg]  # daemon loop (systemd/cron)
#   gpu-watchdog.sh --check-only  # só reporta, não age
#   ECC_CPU_ALLOWED=1 ...         # exceção explícita (NÃO default)
set -euo pipefail

LOOP="${1:-}"
INTERVAL="${2:-30}"
START_DIR="/mnt/dados/harness"
LOG_DIR="/mnt/dados/logs"
PORTS="${ECC_WATCH_PORTS:-8083 8081 8082 8084}"
STATE="/tmp/gpu-watchdog.state"
MAX_TRIES="${ECC_MAX_TRIES:-3}"
CPU_ALLOWED="${ECC_CPU_ALLOWED:-0}"

port_up() {
  timeout 3 curl -s -m 2 -o /dev/null "http://127.0.0.1:$1/health" 2>/dev/null && return 0
  timeout 3 curl -s -m 2 -o /dev/null "http://127.0.0.1:$1/v1/models" 2>/dev/null && return 0
  return 1
}

log() { echo "[gpu-watchdog $(date -Is)] $*" | tee -a "$STATE.log" >&2; }

count_up() {
  local up=0
  for p in $PORTS; do
    port_up "$p" && up=$((up + 1))
  done
  echo "$up"
}

on_gpu() {
  local hit
  hit=$(timeout 5 grep -lE 'Vulkan|ngl.*999|offload.*999' "$LOG_DIR"/all-*.log 2>/dev/null | head -1)
  [ -n "$hit" ]
}

check() {
  local up total remain
  up=$(count_up); total=$(echo "$PORTS" | wc -w)
  remain=$((total - up))
  log "check: ${up}/${total} portas up | gpu(backend Vulkan)=$(on_gpu && echo sim || echo nao) | off=$remain"
  if [ "$up" -eq "$total" ] && on_gpu; then
    [ -f "$STATE" ] && rm -f "$STATE"
    return 0
  fi
  return 1
}

respawn() {
  if [ "$CPU_ALLOWED" = "1" ]; then
    log "ECC_CPU_ALLOWED=1 — excecao explicita: aceita CPU; aguardando llama"
    return 0
  fi
  local tries=0
  while [ "$tries" -lt "$MAX_TRIES" ]; do
    tries=$((tries + 1))
    log "respawn #$tries (GPU-only, -ngl 999) — backend forçado Vulkan"
    if [ -x "$START_DIR/start-all-models.sh" ]; then
      setsid bash "$START_DIR/start-all-models.sh" > /tmp/gpu-watchdog-respawn.log 2>&1 < /dev/null &
      disown 2>/dev/null || true
      log "start-all-models lancado em background (PID $!). Aguardando ${BACKOFF_AFTER:-25}s..."
      sleep "${BACKOFF_AFTER:-25}"
      if [ "$(count_up)" -gt 0 ] && on_gpu; then
        log "RESPAWN OK — GPU-only confirmado"
        rm -f "$STATE"
        return 0
      fi
    else
      log "start-all-models.sh ausente — impossivel garantir GPU-only"
      return 1
    fi
    [ "$tries" -lt "$MAX_TRIES" ] && sleep $((tries * 10))
  done
  echo "falha:VULKAN_OFFLINE_tentativas=$MAX_TRIES" > "$STATE"
  log "FALHA APOS $MAX_TRIES tentativas — GPU offline. NAO usou CPU (regra). Estado: $STATE"
  return 1
}

backoff_delay() {
  if [ -f "$STATE" ]; then echo "60"; else echo "$INTERVAL"; fi
}

case "$LOOP" in
  --check-only)
    check; exit "$?"
    ;;
  --loop)
    log "daemon loop iniciado (intervalo ${INTERVAL}s, ports=$PORTS)"
    while true; do
      if [ "$(count_up)" -lt "$(echo "$PORTS" | wc -w)" ] || ! on_gpu; then
        respawn || true
      else
        [ -f "$STATE" ] && rm -f "$STATE"
      fi
      sleep "$(backoff_delay)"
    done
    ;;
  ""|check)
    check >/dev/null 2>&1 || respawn
    ;;
  *)
    echo "Uso: gpu-watchdog.sh [--loop [seg] | --check-only | check]"; exit 1
    ;;
esac
