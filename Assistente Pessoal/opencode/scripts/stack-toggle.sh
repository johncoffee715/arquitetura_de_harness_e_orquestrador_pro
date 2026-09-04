#!/usr/bin/env bash
# stack-toggle.sh — Toggle LLM stack on/off via OpenCode command (botão ALL)
# R19: Graceful stack shutdown/shutdown
# Uso: ./stack-toggle.sh — liga/desliga TODOS os LLMs da stack
set -u
if ! mkdir /tmp/stack-toggle.lock.d 2>/dev/null; then echo "toggle já em execução — skip"; exit 0; fi
trap 'rmdir /tmp/stack-toggle.lock.d 2>/dev/null || true' EXIT INT TERM
ROOT="/mnt/dados/Assistente Pessoal/opencode"

is_stack_up() {
  # Toggle = ALL: verifica LLMs reais (health do start-stack.sh: 8083 9084 9086 9088 9090)
  # 9093/9095 não têm launch definido; needle (8097/9091) é pgrep, não /health
  local ports=(8083 9084 9086 9088 9090 9092 9093)
  local ok=0
  for p in "${ports[@]}"; do
    if curl -sf -m 2 "http://127.0.0.1:$p/health" >/dev/null 2>&1; then
      ok=$((ok+1))
    fi
  done
  [ "$ok" -eq "${#ports[@]}" ]
}

if is_stack_up; then
  echo "🔌 Stack ligada — desligando gracefully..."
  bash "$ROOT/scripts/stop-all-models.sh"
  echo "✅ Stack desligada"
else
  echo "🔌 Stack desligada — levantando (forçando ALL, ignora WARM)..."
  MODE_WARM=0 bash "$ROOT/scripts/start-stack.sh" all
  echo "✅ Stack ligada (ALL)"
fi
