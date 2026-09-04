# Anatomia do Grafo em 5 Camadas — canonização 2026-08-24

Diretiva do usuário: modo MIX + Dev Loop globais; autofagia/helenização criteriosa de hooks/plugins/skills/subagents/mcp/lsp/features.

## O framework (analogia fundadora: Medabots/Digimon/Pokémon)
Não existe "melhor monstro" — existe o TIME MONTADO CERTO contra o adversário certo.

| Camada | Definição | Alavanca de engenharia |
|---|---|---|
| PROMPT | entrada do usuário | contrato bruto da intenção |
| CONTEXTO | filtragem pós-usuário pelo LLM responsável | seleção do que entra na janela |
| HARNESS | todo ecossistema que permeia o LLM | tools, hooks, MCP, skills, memória |
| LOOP | filtro de loopagem com aperfeiçoamento guiado | iterar = evoluir; circuit-breaker corta repetição |
| GRAFO ENGINEERING | quem faz o quê no harness | vocacional: cada slot com papel medido |

## Aplicação ao stack real (2026-08-24)
- CONTEXTO: context-selector (BM25) · memory-recall R26 · needle-dispatch L0
- HARNESS: circuit-breaker.ts · gran-mestre-state.ts · ecc-hooks · MCPs codegraph/context7 · 82 skills
- LOOP: fable-judge adversarial · refutação universal apex · benchmark GM-oficial
- GRAFO: Ornith :8083 (primário) · judge :9085 · refutação :9086 · qwen38-2b :9087 (code/tool)

## Fontes para autofagia contínua
- /mnt/win1/123 tranqueiras e projetos/engenharia de harness.md
- /mnt/win1/123 tranqueiras e projetos/Orquestrador de IA de Forma Profissional.md
- Canonizado em: rules/variants/compacto/AGENTS.md § ANATOMIA DO GRAFO

Tags: gran-mestre, doutrina, enxame, grafo-engineering
