---
name: cerebral-wikia
description: LLM Wiki implementation for OpenCode — persistent knowledge base managed by AI agents
---

# Cerebral Wikia Agent — LLM Wiki Refatorado

Wrapper thin para a skill `cerebral-wikia`. Executa operações no cérebro persistente.

## Operações Principais

| Operação | Workflow |
|---|---|
| ingestar | LLM → resumo → atualiza wiki |
| consultar | LLM → busca → síntese |
| lintar | LLM → verifica contradições |
| status | estatísticas do cérebro |

## Triggers

- Perguntas sobre conhecimento existente no cerebro
- Novas fontes a serem arquivadas
- Verificação de saúde do wiki

## Integração

- Lê/escreve em `/mnt/dados/cerebro com IA/`
- Via skill `cerebral-wikia`
- MCP optional: open-notebook