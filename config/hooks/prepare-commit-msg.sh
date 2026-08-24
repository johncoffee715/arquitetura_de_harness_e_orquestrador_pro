#!/usr/bin/env bash
# ============================================================
# prepare-commit-msg.sh — anexa trailer "Assisted-by" nos commits
# Origem: padrão agent-scaffold (jeremyary) — convenção git-workflow
# Helenizado para o Gran-Mestre (rastreabilidade autoral)
#
# Rastreia que o commit foi assistido por agente do harness,
# mantendo rastreabilidade requisito→código em todo o histórico.
# ============================================================
set -u

COMMIT_MSG_FILE="${1:-}"
if [ -z "$COMMIT_MSG_FILE" ] || [ ! -f "$COMMIT_MSG_FILE" ]; then
  exit 0
fi

# Não duplica trailer se já existir
if grep -q "^Assisted-by:" "$COMMIT_MSG_FILE" 2>/dev/null; then
  exit 0
fi

# Não anexa em merges/reverts padrão do git (última linha já especial)
if grep -qE "^(Merge|Revert) " "$COMMIT_MSG_FILE" 2>/dev/null; then
  exit 0
fi

AGENT_NAME="${OPENCODE_AGENT:-Gran-Mestre Harness}"
MODEL="${OPENCODE_MODEL:-opencode/deepseek-v4-flash-free}"

# Trailer no formato git trailer block (blank line + key: value)
{
  printf '\nAssisted-by: %s <%s>\n' "$AGENT_NAME" "$MODEL"
} >> "$COMMIT_MSG_FILE"

exit 0