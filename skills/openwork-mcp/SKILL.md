---
name: openwork-mcp
description: "OpenWork MCP: search_capabilities + execute_capability para compartilhar skills/MCPs/conexões entre ferramentas; ATUALIZA o subagent executor-deep já absorvido. (absorvido de different-ai/openwork)"
origin: absorvido:different-ai/openwork
metadata:
  autofagia: different-ai/openwork (2026-08-04)
  prioridade: 8
  linguagem: TypeScript
  topics: mcp, capability-catalog, a2a
  artefatos: mcp+subagent
  padroes_absorvidos: 1
---
# Openwork Mcp

Helenizado de [`different-ai/openwork`](https://github.com/different-ai/openwork).

## Propósito
OpenWork MCP: search_capabilities + execute_capability para compartilhar skills/MCPs/conexões entre ferramentas; ATUALIZA o subagent executor-deep já absorvido.

## Padrões absorvidos (núcleo canônico do repo)
- OpenWork MCP: search_capabilities + execute_capability para compartilhar skills/MCPs/conexões entre ferramentas; ATUALIZA o subagent executor-deep já absorvido.

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="openwork-mcp")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/different-ai/openwork
