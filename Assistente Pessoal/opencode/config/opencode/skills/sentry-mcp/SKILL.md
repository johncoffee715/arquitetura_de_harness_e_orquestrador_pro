---
name: sentry-mcp
description: >-
  MCP remoto do Sentry (mcp.sentry.dev) — debugging orientado a anotadores de código: erros, issues, traces, performance. absorvido de getsentry/sentry-mcp; middleware remoto p/ o fluxo dev workflow (human-in-the-loop).
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/getsentry/sentry-mcp
helenized: true
r84: true
r77_triple: true
---
# sentry-mcp — MCP Sentry

Helenizado de [`https://github.com/getsentry/sentry-mcp`](https://github.com/getsentry/sentry-mcp) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
MCP remoto do Sentry (mcp.sentry.dev) — debugging orientado a anotadores de código: erros, issues, traces, performance. absorvido de getsentry/sentry-mcp; middleware remoto p/ o fluxo dev workflow (human-in-the-loop).

## Padrões absorvidos
- observabilidade: Sentry, MCP, monitoramento
- Origem: https://github.com/getsentry/sentry-mcp
- Domínio: MCP Sentry

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `sentry-mcp` (tags: Sentry, MCP).
2. `skill(name="sentry-mcp")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/getsentry/sentry-mcp
