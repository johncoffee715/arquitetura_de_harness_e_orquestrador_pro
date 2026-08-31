#!/usr/bin/env bash
# skills-security-audit.sh — Auditoria preventiva de skills (.md + scripts associados)
# Uso: bash skills-security-audit.sh [--quiet]
# Saída: resumo no stdout + log JSONL append-only.
# Exit codes: 0 = limpo/apenas avisos | 1 = achado CRITICO (gate p/ self-healing R6/R9)
# Contrato Gran-Mestre: rodar após instalar/atualizar QUALQUER skill; CRITICO => bloquear e refutar (R40).
set -uo pipefail

SKILL_ROOTS=(
  "$HOME/.agents/skills"
  "/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills"
)
LOG_DIR="/mnt/dados/Assistente Pessoal/opencode/config/opencode/logs"
LOG="$LOG_DIR/skills-security-audit.jsonl"
QUIET=false
[[ "${1:-}" == "--quiet" ]] && QUIET=true

mkdir -p "$LOG_DIR"
TS="$(date +%Y-%m-%dT%H:%M:%S%z)"
CRIT=0; WARN=0

emit() { # sev skill file line rule sample
  printf '{"ts":"%s","sev":"%s","skill":"%s","file":"%s","line":%s,"rule":"%s","sample":"%s"}\n' \
    "$TS" "$1" "$2" "$3" "${4:-0}" "$5" "${6//\"/\\\"}" >> "$LOG"
}

say() { $QUIET || printf '%s\n' "$*"; }

scan_scripts() { # $1=root
  local root="$1" rule pattern
  local -A RULES=(
    ['eval-execution']='\beval\('
    ['py-exec']='[^a-z]exec\('
    ['os-system']='os\.system\('
    ['subprocess-shell']='shell[[:space:]]*=[[:space:]]*True'
    ['pickle-deserialization']='import[[:space:]]+pickle'
    ['tls-verification-off']='verify[[:space:]]*=[[:space:]]*False'
    ['js-dynamic-function']='new[[:space:]]+Function\('
    ['js-child-process']=child_process
    ['destructive-rm']='rm[[:space:]]+-rf[[:space:]]+(/|~|\$HOME)'
    ['remote-code-pipe']='(curl|wget)[^|]*\|[[:space:]]*(ba)?sh\b'
  )
  for rule in "${!RULES[@]}"; do
    while IFS=$'\t' read -r file line text; do
      [[ -z "$file" ]] && continue
      local skill; skill=$(basename "$(dirname "$(dirname "$file")")")
      CRIT=$((CRIT+1)); emit CRITICO "$skill" "$file" "$line" "$rule" "$text"
    done < <(grep -RInE --include='*.py' --include='*.sh' --include='*.mjs' --include='*.js' --include='*.ts' \
      -e "${RULES[$rule]}" "$root" 2>/dev/null | head -100)
  done
  # segredo hardcodado em script (exclui leitura de env, que é o padrão correto)
  while IFS=$'\t' read -r file line text; do
    [[ -z "$file" ]] && continue
    case "$text" in *os.environ*|*process.env*) continue;; esac
    local skill; skill=$(basename "$(dirname "$(dirname "$file")")")
    CRIT=$((CRIT+1)); emit CRITICO "$skill" "$file" "$line" 'hardcoded-secret' "$text"
  done < <(grep -RInE --include='*.py' --include='*.sh' --include='*.mjs' --include='*.js' --include='*.ts' \
    -e '(api[_-]?key|secret|password|token)[\"'"'"'][[:space:]]*[:=][[:space:]]*[\"'"'"'][A-Za-z0-9_-]{20,}' "$root" 2>/dev/null | head -50)
}

scan_docs() { # $1=root
  local root="$1" rule pattern
  local -A RULES=(
    ['md-prompt-injection']='ignore[[:space:]]+(all[[:space:]]+)?(previous|prior)[[:space:]]+(instructions|prompts)'
    ['md-exfiltration']='exfiltrat(e|ion)'
    ['md-remote-code-pipe']='(curl|wget)[^|]*\|[[:space:]]*(ba)?sh\b'
  )
  for rule in "${!RULES[@]}"; do
    while IFS=$'\t' read -r file line text; do
      [[ -z "$file" ]] && continue
      local skill sev; skill=$(basename "$(dirname "$file")"); sev=AVISO
      [[ "$file" == *"security-review/"* ]] && sev='AVISO(allowlist-doc-vuln)'
      WARN=$((WARN+1)); emit "$sev" "$skill" "$file" "$line" "$rule" "$text"
    done < <(grep -RInE --include='*.md' -e "${RULES[$rule]}" "$root" 2>/dev/null | head -100)
  done
  # segredo hardcodado em documentação = CRÍTICO
  while IFS=$'\t' read -r file line text; do
    [[ -z "$file" ]] && continue
    local skill; skill=$(basename "$(dirname "$file")")
    CRIT=$((CRIT+1)); emit CRITICO "$skill" "$file" "$line" 'hardcoded-secret-md' "$text"
  done < <(grep -RInE --include='*.md' \
    -e '(api[_-]?key|secret|password|token)[\"'"'"'][[:space:]]*[:=][[:space:]]*[\"'"'"'][A-Za-z0-9_-]{20,}' "$root" 2>/dev/null | head -50)
}

for ROOT in "${SKILL_ROOTS[@]}"; do
  [[ -d "$ROOT" ]] || continue
  scan_scripts "$ROOT"
  scan_docs "$ROOT"
done

say "=== skills-security-audit @ $TS ==="
say "CRITICOS: $CRIT | AVISOS: $WARN | log: $LOG"
if (( CRIT > 0 )); then
  say "VEREDITO: NAO_PASSOU — bloquear skills afetadas até correção (R18/R40). Detalhes:"
  tail -n "$CRIT" "$LOG" | grep '"sev":"CRITICO"' | tail -10 | $QUIET || true
  exit 1
fi
say "VEREDITO: PASSOU_CATEGORICO — skills seguras para uso."
exit 0
