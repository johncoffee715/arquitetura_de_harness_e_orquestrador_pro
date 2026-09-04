---
name: openwork-mcp
description: >-
  OpenWork MCP: search_capabilities + execute_capability para compartilhar skills/MCPs/conexões entre ferramentas; ATUALIZA o subagent executor-deep já absorvido. (absorvido de different-ai/openwork)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/different-ai/openwork
helenized: true
r84: true
r77_triple: true
---
# openwork-mcp — MCP OpenWork

Helenizado de [`https://github.com/different-ai/openwork`](https://github.com/different-ai/openwork) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
OpenWork MCP: search_capabilities + execute_capability para compartilhar skills/MCPs/conexões entre ferramentas; ATUALIZA o subagent executor-deep já absorvido. (absorvido de different-ai/openwork)

## Padrões absorvidos
- MCP: MCP, OpenWork
- Origem: https://github.com/different-ai/openwork
- Domínio: MCP OpenWork

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `openwork-mcp` (tags: MCP, OpenWork).
2. `skill(name="openwork-mcp")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/different-ai/openwork
