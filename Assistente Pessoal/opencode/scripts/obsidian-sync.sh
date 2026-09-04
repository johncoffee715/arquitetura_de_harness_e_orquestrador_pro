#!/usr/bin/env bash
# obsidian-sync.sh — helenização modular dos 4 scripts legados (session-saver,
# daily-finetuning, internet-reinforcement, finetuning-completo) para a árvore
# portátil + vault atual. Subcomandos:
#   session <id> [nota]   → registra sessão em sessions/
#   daily                 → log diário + estrutura do dia em diario/
#   reinforce <query> <achado> → pesquisa internet → aprendizados/
#   full                  → pacote completo do dia (daily + métricas)
set -u
VAULT="/mnt/dados/Assistente Pessoal/cerebro com IA"
TODAY=$(date '+%F')
NOW=$(date '+%T')
cmd="${1:-full}"
shift || true

mkdir -p "$VAULT/diario" "$VAULT/sessions" "$VAULT/aprendizados"

case "$cmd" in
  session)
    sid="${1:-manual}"; nota="${2:-}"
    f="$VAULT/sessions/${TODAY}_${sid:0:12}.md"
    cat > "$f" <<EOF
---
type: session
date: $TODAY
id: $sid
tags: [session]
---
# Sessão $sid — $TODAY $NOW

$nota
EOF
    echo "sessão → $f"
    ;;
  daily)
    f="$VAULT/diario/$TODAY.md"
    [ -f "$f" ] || cat > "$f" <<EOF
# Diário — $TODAY

## Tarefas
- [ ]

## Aprendizados
-

## Decisões
-
EOF
    echo "diário → $f"
    ;;
  reinforce)
    q="${1:-?}"; achado="${2:-}"
    f="$VAULT/aprendizados/${TODAY}_web_${q// /_}.md"
    cat > "$f" <<EOF
---
type: web-reinforcement
date: $TODAY
query: "$q"
tags: [pesquisa, web]
---
# Pesquisa web: $q

## Achado principal
$achado

## Aplicação no harness
-
EOF
    echo "- $TODAY web: $q → [[${TODAY}_web_${q// /_}]]" >> "$VAULT/aprendizados/log.md"
    echo "aprendizado → $f"
    ;;
  full)
    "$0" daily
    f="$VAULT/diario/$TODAY.md"
    cat >> "$f" <<EOF

## Métricas da Stack ($NOW)
\`\`\`
$(for p in 8083 9084 9086 9088 9090 9092 9093 8097; do
    h=$(curl -sf -m 2 "http://127.0.0.1:$p/health" >/dev/null 2>&1 && echo ok || echo DOWN)
    echo "$p:$h"
  done | paste -sd' ')
\`\`\`
EOF
    echo "pacote completo → $f"
    ;;
  *)
    echo "uso: obsidian-sync.sh {session|daily|reinforce|full}" >&2; exit 2 ;;
esac
