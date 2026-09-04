---
tags: [aprendizado, autofagia, helenizacao, pipeline, registry, mix]
date: 2026-07-29
area: ai/agent-orchestration/autofagia
---

# Aprendizado: Autofagia de 35+ Fontes com Modo MIX

## Contexto
O Gran-Mestre executou autofagia em 35+ repositórios-fontes para absorver
padrões de orquestração, verificação, memória e ferramentas. O modo MIX
(COMPLEX + CRITICAL + FEATURE) foi usado como motor de autofagia.

## O que Funcionou

### 1. Modo MIX como Motor de Autofagia
- Ativar todos os recursos simultaneamente maximiza a absorção
- 86 padrões helenizados (absorvidos criticamente) em 10 áreas
- Fable Judge em 3 fases garante verificação adversarial
- Autofagia relatório consolidado em `AUTOFAGIA_35_FONTES.md`

### 2. Helenização (Transformação Crítica)
Cada padrão absorvido foi **transformado**, não copiado:
- **oh-my-openagents:** 11 agents → 7 agents especializados (simplificação)
- **Superpowers:** Brainstorming → Fase 1 do pipeline
- **Fable Method:** 8 padrões → 3 filtros em 3 fases
- **OpenClaude:** Fork/Team/Task → sistema de delegação existente

### 3. Registry como Sistema Nervoso
- 61 subagents registrados com tags de capacidade
- Descoberta dinâmica elimina hardcoded
- Matriz de compatibilidade Fase x Recurso guia a delegação

### 4. WAL (Write-Ahead Log) Cycle
Cada ciclo WAL = 3 fases de verificação antes de tocar código:
1. **Write** — Decide se deve gravar
2. **Ahead** — Faz planejamento
3. **Log** — Executa com rastreamento

## O que Não Funcionou

### 1. Hardcoded Agents no Pipeline
- PIPELINE_MODES.md tinha agents fixos por modo
- Qualquer mudança exigia editar múltiplos arquivos
- **Solução:** Delegação dinâmica via Registry (consultado em runtime)

### 2. 6 Modos de Pipeline
- TRIVIAL e SIMPLE raramente usados
- MEDIUM ambiguo (quando usar vs COMPLEX?)
- **Solução:** Reduzir para 4 modos, MIX como default

### 3. Modelos Hardcoded
- `claude-opus-4.7`, `claude-sonnet-4.6`, `gpt-5.5` em múltiplos arquivos
- Modelos mudam com frequência
- **Solução:** `omniroute/auto/best-free` como único primário

## Padrões Identificados

1. **Delegação dinâmica > hardcoded** — Consultar Registry por tags elimina rigidez
2. **Helenização > cópia** — Todo padrão absorvido deve ser transformado
3. **WAL antes de executar** — Planejar antes de tocar código
4. **Fable Judge em cada gate** — Verificação adversarial não é opcional
5. **Registry como única fonte de verdade** — Nenhum recurso fora do registro
6. **Modo MIX como default** — Um modo que serve para tudo
7. **Dev Loop estrutura iteração** — Critérios claros de parada e escalonamento

## Próximas Investigações
- Dashboard de métricas de delegação (acertos/erros por tag)
- Self-healing preditivo (antes da falha)
- Autofagia automática sem intervenção
- Testar MIX em campo com tarefa real de desenvolvimento

## Sinapses
- [[concepts/antropofagia-tecnologica]] — metodologia de absorção
- [[concepts/delegacao-dinamica]] — padrão identificado
- [[concepts/dev-loop]] — padrão identificado
- [[entities/gran-mestre]] — entidade que executou
- [[2026-07-29-gran-mestre-v7-mix-dev-loop]] — decisão relacionada

---

*Neurônio criado em: 2026-07-29*
