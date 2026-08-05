---
tags: [concept, orchestration]
related: [[entities/gran-mestre]] [[concepts/antropofagia-tecnologica]] [[concepts/dev-loop]]
last_updated: 2026-07-29
---
# Delegação Dinâmica — Pipeline Líquido

## Definição
O Gran-Mestre não tem agents hardcoded por fase. Cada fase consulta o **Registry** (`REGISTRY_SUBAGENTS.md`) em runtime, selecionando subagents, skills, MCPs, LSPs e tools por **tags de capacidade**.

## Princípio Neural
Assim como o cérebro não tem funções fixas por região — a plasticidade neural permite que qualquer área assuma qualquer função —, o pipeline do Gran-Mestre é **líquido**: a equipe de cada fase é composta dinamicamente conforme a necessidade.

## Algoritmo de Ativação
```
1. IDENTIFICAR tags relevantes para a fase
2. CONSULTAR Registry por subagents com essas tags
3. CONSULTAR Registry por skills com essas tags
4. CONSULTAR Registry por MCPs com essas tags
5. CONSULTAR Registry por LSPs com essas tags
6. COMPOR equipe dinâmica
7. DELEGAR execução
8. COLETAR resultados
9. AVALIAR métricas → reforço sináptico
```

## Tags por Fase
| Fase | Tags de Ativação Neural |
|------|------------------------|
| DESCOBERTA | discovery, research, interview, brainstorming |
| CONTRATO | spec, contract, design, validation |
| PLANO | planning, tdd, tasks, decomposition |
| EXECUÇÃO | execution, implementation, coding, review |
| REVISÃO | review, macro, architecture, audit |
| ENTREGA | delivery, verification, release, memory |

## Vantagens Neurais
1. **Plasticidade** — Pipeline se adapta a qualquer task
2. **Evolução** — Métricas fortalecem sinapses (acertos) ou enfraquecem (erros)
3. **Resiliência** — Nenhum subagent é ponto único de falha
4. **Escalabilidade** — Novos subagents entram no Registry e são descobertos automaticamente

## Sinapses
- [[entities/gran-mestre]] — orquestrador que implementa
- [[concepts/dev-loop]] — execução em 3 níveis
- [[concepts/antropofagia-tecnologica]] — origem do padrão
- [[2026-07-29-gran-mestre-v7-mix-dev-loop]] — decisão arquivada

---
*Neurônio criado em: 2026-07-29*
