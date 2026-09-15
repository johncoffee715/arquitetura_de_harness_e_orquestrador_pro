---
numero: LEGADO
tema: Regras legadas (numeracao antiga, nao vigente)
categoria: processo
setor: harness
escopo: historico
vigencia: 2026-08-18
---

> NOTA: regras com numeracao antiga R45-R51 que CONFLITAM com a numeracao vigente.
> Mantidas por historico. Na duvida, prevalecer a numeracao do AGENTS.md.

## R45 — Decomposição de Tasks Complexas (Dev-Loop)

Task complexa → decompor em 3-5 subtasks bite-sized antes de delegar.
- Agente deep NÃO deve receber escopo que ultrapasse 3 arquivos principais
- Cada subtask = 1-3 arquivos, não 10+
- Se task >3 arquivos → decompor primeiro, delegar depois

## R46 — Orquestrador NUNCA Executa Diretamente (Anti-R1)

O orquestrador NUNCA aplica melhorias diretamente em código de implementação.
- SEMPRE delegar para subagentes
- Mesmo tarefas "quick" → delegar
- Orquestrador = supervisor/orquestrador, NUNCA executor
- Exceção: apenas orquestração (edits de AGENTS.md, CONTEXT.md, SKILL.md)

## R47 — Guardrails de Execução de Regras Globais

TODAS as regras globais devem ser validadas automaticamente:

### Checklist de Validação (antes de CADA task)
1. R1: Orquestrador não executa diretamente? → SEMPRE delegar
2. R28: Critério de trânsito categórico? → veredito PASSOU/NAO_PASSOU
3. R29: Teste como usuário final? → evidência fresca
4. R34: Nota 0,0000001–100? → mínimo 97
5. R37: Autonomia total do orquestrador? → pesquisa aplicada
6. R45: Decomposição bite-sized? → ≤3 arquivos por task
7. R46: Orquestrador não executa? → SEMPRE delegar

### Validação Pós-Task
1. Syntax check: node --check
2. Testes: node --test → 36/36
3. QA: qa.mjs → 22/22 PASS
4. Screenshot: evidência visual
5. Scorecard: nota R34 com bugs concretos

### Auto-Correção
Se qualquer regra falhar:
1. Identificar regra violada
2. Corrigir imediatamente
3. Registrar no decision-log
4. Reportar ao usuário

## R48 — Monitoramento Ativo de Tasks (30s Cycle)

TODAS as tasks delegadas devem ser monitoradas a cada 30 segundos:
- Verificar se estão "running" ou "stalled"
- Acompanhar progresso com métricas de baixo nível
- Se stalled >2min → intervenir (refatorar rota ou cancelar)
- Registrar status no CONTEXT.md

### Métricas de Baixo Nível
1. Duração total da task
2. Última tool call (timestamp)
3. Número de iterações
4. Tamanho do output gerado
5. Erros/warnings

### Ação se Stalled
1. Verificar se modelo está respondendo
2. Se timeout → cancelar e relançar com modelo diferente
3. Se erro → diagnosticar e corrigir
4. Registrar no decision-log

## R49 — ContextGovernor (Prevenção OOM)

MCP JSON-RPC que calcula janela antropofágica antes de dispatch:
- Extrair metadados do .gguf (camadas, cabeças, dimensões)
- Calcular Custo_KV = camadas × cabeças × dimensões × 2 × bytes × contexto
- Verificar VRAM disponível (16GB - reserva - fragmentação)
- Aprovar/rejeitar dispatch antes de executar
- Retornar janela segura alocada

## R50 — Cache Coerência Reativa

SQLite WAL para concorrência entre módulos:
- Write-Ahead Logging para prevenir corrupção
- Fila serializada para operações de escrita
- Checkpoint periódico para liberação de memória

## R51 — Obsidian Sync Bridge

Sincronização automática com vault Obsidian:
- Decisões → `/decisoes/`
- Aprendizados → `/aprendizados/`
- Pipeline → `/pipeline/`
- Wiki → `/wiki/`

