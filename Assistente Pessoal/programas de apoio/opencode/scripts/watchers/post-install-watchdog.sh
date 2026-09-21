#!/usr/bin/env bash
# post-install-watchdog.sh — WD-PI: watchdog pós-reinstalação do opencode (2026-09-05, v2 2026-09-18)
# Restaura as pendências da reinstalação no SSD slave de IA (sdb):
#   1) binário oficial em bin/opencode (bin/opencode.real não existe mais — portátil removido)
#   2) cérebro XDG: symlink ~/.config/opencode -> config do harness (governança guard-gap-p5)
#   3) watchers vivos: config-watcher (código novo) + stack-guard — relançados desanexados (R19)
#   4) slots ESSENTIAL (:8083/:9084) healthy — revive via start-stack.sh (idempotente)
#   5) 1ª passada = restauração forçada completa (flag .post-install-first-done)
# Fail-open: nunca bloqueia; loga em state/watcher/post-install.log
set -u
ROOT="/mnt/dados/Assistente Pessoal/programas de apoio/opencode"
STATE="$ROOT/state/watcher"
LOG="$STATE/post-install.log"
FIRST_FLAG="$STATE/.post-install-first-done"
# v2 (2026-09-18): versão DINÂMICA — nunca mais congela versão.
# Consulta o registry npm a cada ciclo; se houver versão nova, faz auto-upgrade (R19 fail-open).
EXPECTED_VERSION=""
INTERVAL="${1:-300}"
mkdir -p "$STATE"

log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

latest_version() {
  # retorna a versão mais recente do opencode-ai no registry npm (ou vazia em falha)
  # timeout 10s: nunca deixa o ciclo travar (R6 anti-stall)
  timeout 10 npm view opencode-ai version 2>/dev/null | tr -d '[:space:]' || true
}

auto_upgrade() { # $1=versão alvo
  log "AUTO-UPGRADE detectado: local $LOCAL_VERSION -> registry $1"
  if "$ROOT/bin/opencode" upgrade "$1" -m curl >> "$LOG" 2>&1; then
    log "AUTO-UPGRADE OK: $1"
    return 0
  fi
  log "AUTO-UPGRADE FALHOU (fail-open, nao bloqueia)"
  return 1
}

slot_up() { curl -sf -m 3 "http://127.0.0.1:$1/health" >/dev/null 2>&1; }

ensure_watcher() { # $1=nome $2=script
  pgrep -f "$1[.]sh" >/dev/null 2>&1 && return 0
  log "$1 DOWN -> relançando desanexado (R19)"
  setsid nohup "$2" 60 > /dev/null 2>&1 < /dev/null & disown || true
}

check_binary() {
  if [ ! -x "$ROOT/bin/opencode" ]; then
    log "CRITICO bin/opencode ausente — reinstalação comprometida"
    return 1
  fi
  LOCAL_VERSION=$("$ROOT/bin/opencode" --version 2>/dev/null || echo "?")
  local latest
  latest=$(latest_version)
  if [ -z "$latest" ]; then
    log "registry indisponivel — mantendo local $LOCAL_VERSION (sem WARN)"
    return 0
  fi
  if [ "$LOCAL_VERSION" != "$latest" ]; then
    log "INFO versao local $LOCAL_VERSION != registry $latest — auto-upgrade"
    auto_upgrade "$latest"
    return 0
  fi
  log "binario OK: $LOCAL_VERSION (registry $latest)"
}

check_brain() {
  local target
  target=$(readlink "$HOME/.config/opencode" 2>/dev/null || echo "")
  if [ -L "$HOME/.config/opencode" ] && [ "$target" = "$ROOT/config/opencode" ]; then
    log "cerebro XDG OK (symlink -> harness)"
    return 0
  fi
  log "WARN ~/.config/opencode nao aponta para o harness ($ROOT/config/opencode) — pendencia: exports XDG no ~/.bashrc ou restaurar symlink"
}

check_slots() {
  local down=0 p
  for p in 8083 9084; do
    if slot_up "$p"; then
      log "slot ESSENTIAL :$p UP"
    else
      log "slot ESSENTIAL :$p DOWN"
      down=1
    fi
  done
  if [ "$down" -eq 1 ]; then
    log "revivendo stack (start-stack.sh idempotente, desanexado)"
    setsid nohup bash "$ROOT/scripts/start-stack.sh" >> "$LOG" 2>&1 < /dev/null & disown || true
  fi
}

first_pass() {
  [ -f "$FIRST_FLAG" ] && return 0
  log "===== 1a passada pos-instalacao: restauracao forcada ====="
  check_binary
  check_brain
  # config-watcher antigo roda com codigo velho (check opencode.real) — restart cirurgico
  pkill -f "config-watcher[.]sh" 2>/dev/null
  sleep 1
  ensure_watcher "config-watcher" "$ROOT/scripts/watchers/config-watcher.sh"
  ensure_watcher "stack-guard" "$ROOT/scripts/stack-guard.sh"
  check_slots
  log "1a passada concluida — modo residente (intervalo ${INTERVAL}s)"
  touch "$FIRST_FLAG"
}

first_pass
while true; do
  check_binary
  ensure_watcher "config-watcher" "$ROOT/scripts/watchers/config-watcher.sh"
  ensure_watcher "stack-guard" "$ROOT/scripts/stack-guard.sh"
  check_slots
  sleep "$INTERVAL"
done
