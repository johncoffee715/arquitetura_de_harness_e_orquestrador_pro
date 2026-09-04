#!/bin/bash
# Gran-Mestre Obsidian Daily Fine-Tuning System
# Sistema de cognição diária para o Gran-Mestre

VAULT="/home/johncoffee/ObsidianGranMestre"
TODAY=$(date '+%Y-%m-%d')
NOW=$(date '+%H:%M:%S')

# Criar estrutura diária
mkdir -p "$VAULT/diario/$TODAY"
mkdir -p "$VAULT/tarefas"
mkdir -p "$VAULT/notas"
mkdir -p "$VAULT/ideias"
mkdir -p "$VAULT/decisoes"
mkdir -p "$VAULT/aprendizados"

echo "=== Gran-Mestre Daily Fine-Tuning ==="
echo "Data: $TODAY"
echo "Hora: $NOW"

# 1. Criar log diário
cat > "$VAULT/diario/$TODAY/log.md" << EOF
# Log Diário — $TODAY

## Status
- **Data**: $TODAY
- **Hora**: $NOW
- **Gran-Mestre**: Ativo

## Tarefas do Dia
- [ ] (Tarefa 1)
- [ ] (Tarefa 2)
- [ ] (Tarefa 3)

## Decisões Tomadas
- (Decisão 1)
- (Decisão 2)

## Aprendizados
- (Aprendizado 1)
- (Aprendizado 2)

## Notas
- (Nota 1)
- (Nota 2)

## Tags
#diario #gran-mestre #$TODAY
EOF

echo "✅ Log diário criado: $VAULT/diario/$TODAY/log.md"

# 2. Criar nota de reflexão
cat > "$VAULT/diario/$TODAY/reflexao.md" << EOF
# Reflexão — $TODAY

## O que aprendi hoje?
- (Aprendizado 1)
- (Aprendizado 2)

## O que posso melhorar?
- (Melhoria 1)
- (Melhoria 2)

## O que farei amanhã?
- (Amanhã 1)
- (Amanhã 2)

## Insights
- (Insight 1)
- (Insight 2)

## Tags
#reflexao #gran-mestre #$TODAY
EOF

echo "✅ Reflexão criada: $VAULT/diario/$TODAY/reflexao.md"

# 3. Atualizar índice de tarefas
cat > "$VAULT/tarefas/pendentes.md" << EOF
# Tarefas Pendentes

## Alta Prioridade
- [ ] (Tarefa urgente 1)
- [ ] (Tarefa urgente 2)

## Média Prioridade
- [ ] (Tarefa importante 1)
- [ ] (Tarefa importante 2)

## Baixa Prioridade
- [ ] (Tarefa opcional 1)
- [ ] (Tarefa opcional 2)

## Concluídas Hoje
- [x] Criar vault Obsidian
- [x] Salvar sessions
- [x] Implementar cognição

## Tags
#tarefas #gran-mestre #pendentes
EOF

echo "✅ Tarefas atualizadas: $VAULT/tarefas/pendentes.md"

# 4. Criar nota de ideias
cat > "$VAULT/ideias/$TODAY.md" << EOF
# Ideias — $TODAY

## Ideias para Implementar
1. (Ideia 1)
2. (Ideia 2)
3. (Ideia 3)

## Melhorias Sugeridas
1. (Melhoria 1)
2. (Melhoria 2)

## Insights
1. (Insight 1)
2. (Insight 2)

## Tags
#ideias #gran-mestre #$TODAY
EOF

echo "✅ Ideias criadas: $VAULT/ideias/$TODAY.md"

# 5. Atualizar mapa cognitivo
cat >> "$VAULT/MAPA-COGNITIVO.md" << EOF

## Atualização — $TODAY
- Log diário criado
- Reflexão registrada
- Tarefas atualizadas
- Ideias documentadas
EOF

echo "✅ Mapa cognitivo atualizado"

echo ""
echo "=== Fine-Tuning Concluído ==="
echo "Arquivos criados em: $VAULT/diario/$TODAY/"
echo ""
echo "Para usar:"
echo "  1. Editar $VAULT/diario/$TODAY/log.md"
echo "  2. Preencher $VAULT/diario/$TODAY/reflexao.md"
echo "  3. Atualizar $VAULT/tarefas/pendentes.md"
echo "  4. Adicionar ideias em $VAULT/ideias/$TODAY.md"
