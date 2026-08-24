#!/bin/bash
# Watcher Vigilante (R48) — monitora delegações + LOOP DIÁRIO DE APRENDIZADO
# Inicia junto com o OpenCode (R33). Ao final do dia gera relatório estruturado
# de ocorrências (sucessos/falhas/padrões) e ingere na memória cerebral (R26).
# Formato real do log opencode: "agent=<nome> ... providerID=... modelID=..."
LOG=${OPENCODE_LOG:-/home/johncoffee/.local/share/opencode/log/opencode.log}
OUT=/home/johncoffee/.opencode/state/subagent_watch.log
REPORT_DIR=/home/johncoffee/.opencode/state/reports
VAULT="/mnt/dados/cerebro com IA"
mkdir -p "$REPORT_DIR"
last=$(wc -l < "$LOG" 2>/dev/null || echo 0)
last_report=$(date +%Y-%m-%d)

daily_report() {
  local today=$(date +%Y-%m-%d)
  [ "$today" = "$last_report" ] && return
  last_report=$today
  local yest=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)
  local out="$REPORT_DIR/report-$yest.md"

  local total=$(grep -c "DELEGAÇÃO" "$OUT" 2>/dev/null || echo 0)
  local por_modelo=$(grep "DELEGAÇÃO" "$OUT" 2>/dev/null | grep -oE "→ [a-z0-9./-]+" | sort | uniq -c | sort -rn | head -8)
  local por_agente=$(grep "DELEGAÇÃO" "$OUT" 2>/dev/null | grep -oE "DELEGAÇÃO: \S+" | sort | uniq -c | sort -rn | head -8)

  cat > "$out" << EOF
# Relatório Diário do Watcher — $yest

## Ocorrências do dia
- Total de delegações: $total

## Delegações por modelo
\`\`\`
$por_modelo
\`\`\`

## Delegações por agente
\`\`\`
$por_agente
\`\`\`

## Observações de aprendizado (R48)
- Padrões de roteamento do dia (quais modelos mais usados por fase do grafo).
- Possíveis falhas: delegações para modelos que não respondem (checar health no dia).
- Tarefas aprendidas/melhoradas: verificar entradas do decision-log no dia.

*(Gerado automaticamente pelo watcher — R48: vigilante do orquestrador,
 retroalimentando a cognição neurológica cerebral.)*
EOF

  mkdir -p "$VAULT/aprendizados"
  cp "$out" "$VAULT/aprendizados/$yest-watcher-report.md" 2>/dev/null
  echo "- $(date +%Y-%m-%dT%H:%M:%S): relatório watcher $yest ingerido (R48)" >> "$VAULT/aprendizados/log.md"
}

while true; do
  new=$(wc -l < "$LOG" 2>/dev/null || echo 0)
  if [ "$new" -gt "$last" ]; then
    # Formato real: linhas com agent=<nome> e providerID=/modelID= (delegação)
    sed -n "$((last+1)),${new}p" "$LOG" 2>/dev/null | grep -E "agent=[A-Za-z]" | grep -vE "permission|evaluated|pattern=" | while read -r l; do
      ts=$(echo "$l" | grep -oE "timestamp=[0-9T:.Z-]+" | cut -d= -f2)
      agent=$(echo "$l" | grep -oE "agent=[A-Za-z0-9_-]+" | head -1 | cut -d= -f2)
      prov=$(echo "$l" | grep -oE "providerID=[A-Za-z0-9./_-]+" | head -1 | cut -d= -f2)
      model=$(echo "$l" | grep -oE "modelID=[A-Za-z0-9./_-]+" | head -1 | cut -d= -f2)
      echo "$l" >> "$OUT"
      echo "  [$ts] DELEGAÇÃO: $agent → ${prov:-?}/${model:-?}" >> "$OUT"
    done
    last=$new
  fi
  daily_report
  sleep 60
done
