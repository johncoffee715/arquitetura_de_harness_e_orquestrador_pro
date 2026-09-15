#!/usr/bin/env bash
# ============================================================
# sensitive-data-check.sh — bloqueia commit que contenha segredos
# Origem: padrão agent-scaffold (jeremyary) — convenção security
# Helenizado para o Gran-Mestre (mensagens em pt-BR)
#
# Modo de uso:
#   - hook de pre-commit:  git commit → roda automaticamente
#   - manual:              bash sensitive-data-check.sh [--staged|--all]
# ============================================================
set -u

# Padrões de segredo (ERE válido: ? quantifica separador opcional)
PATTERNS=(
  'api[_-]?key'
  'api[_-]?secret'
  'aws[_-]?access[_-]?key'
  'aws[_-]?secret[_-]?access[_-]?key'
  'password'
  'passwd'
  'senha'
  'pwd[[:space:]]*='
  'token'
  'access[_-]?token'
  'secret'
  'private[_-]?key'
  'BEGIN [A-Z ]*PRIVATE KEY'
  'client[_-]?secret'
  'connection[_-]?string'
  'Bearer [A-Za-z0-9._-]{20,}'
)

# Arquivos/pastas que podem conter os padrões acima legitimamente
IGNORE_PATHS=(
  '^\.git/'
  'node_modules/'
  '\.min\.'
  '\.map$'
  'package-lock\.json'
  'pnpm-lock\.yaml'
  'yarn\.lock'
  'poetry\.lock'
  'uv\.lock'
  'Cargo\.lock'
  'go\.sum'
  'Gemfile\.lock'
  '\.planning/'
  '/tests?/'
  '/testdata/'
  '/fixtures/'
  '\.md$'
  '\.json$'   # configuração pode ter placeholders — valida-se manualmente
)

MODE="${1:---staged}"

if [ "$MODE" = "--all" ]; then
  FILES=$(git ls-files)
else
  FILES=$(git diff --cached --name-only --diff-filter=ACM)
fi

if [ -z "$FILES" ]; then
  exit 0
fi

FAIL=0
# Join limpo das alternâncias (sem printf-mangling)
REGEX_JOINED=$(IFS='|'; echo "${PATTERNS[*]}")

while IFS= read -r file; do
  [ -f "$file" ] || continue
  # skip binário
  if file "$file" | grep -qiE 'binary|image|archive|font|audio|video'; then
    continue
  fi
  for ignore in "${IGNORE_PATHS[@]}"; do
    if echo "$file" | grep -qE "$ignore"; then
      continue 2
    fi
  done
  MATCHES=$(grep -inE "$REGEX_JOINED" "$file" 2>/dev/null | head -3)
  if [ -n "$MATCHES" ]; then
    echo "❌ [sensitive-data-check] potencial segredo em $file:" >&2
    echo "$MATCHES" >&2
    FAIL=1
  fi
done <<< "$FILES"

if [ $FAIL -eq 1 ]; then
  echo "" >&2
  echo "🚫 Commit BLOQUEADO: conteúdo sensível detectado." >&2
  echo "   → Remova o segredo do código (use variável de ambiente / vault / .env)." >&2
  echo "   → Se for falso positivo, ajuste IGNORE_PATHS ou adicione ao allowlist." >&2
  exit 1
fi

exit 0