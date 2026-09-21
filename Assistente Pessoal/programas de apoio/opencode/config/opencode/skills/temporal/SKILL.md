---
name: temporal
description: Durable-execution triad — Workflows resilientes + Activities + Workers, crash→resume exato, dev server local (patterns only).
category: skill
model: local-forge/proposer
---

# temporal

Padrão de execução durável: Workflows (lógica resiliente) + Activities (steps com
retry) + Workers (execução), crash→resume exato, namespaces, dev server local.
Helenizado de `temporalio/temporal` (origem: https://github.com/temporalio/temporal).

> PROIBIDO como dependência/servidor (doutrina R2): vault é o estado.
> Aqui só a tríade + durabilidade.

## Quando usar

- Lógica que precisa sobreviver a crash/redeploy sem perder estado
- Orquestração de microsserviços com retries automáticos
- Dev local com paridade (dev server + CLI + Web UI)

## Como usar

1. **Workflow**: unidade durável (retoma do ponto exato pós-falha)
2. **Activities**: operações com retry (intermitência absorvida)
3. **Workers**: executam workflows/activities; namespaces isolam
4. **Dev**: `temporal server start-dev` + CLI + UI :8233

## Princípio

Falha intermitente é caso normal, não exceção: retry automático, resume exato.
