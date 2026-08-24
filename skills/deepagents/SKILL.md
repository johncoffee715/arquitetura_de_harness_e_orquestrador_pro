---
name: deepagents
description: "Harness de agente 'batteries-included': sub-agents com janelas isoladas, offload de tool outputs, memória persistente pluggável, HITL, model-agnostic e .mcp.json nativo. (absorvido de langchain-ai/deepagents)"
---
# Deepagents

Helenizado de [`langchain-ai/deepagents`](https://github.com/langchain-ai/deepagents).

## Propósito
Harness de agente 'batteries-included': sub-agents com janelas isoladas, offload de tool outputs, memória persistente pluggável, HITL, model-agnostic e .mcp.json nativo.

## Padrões absorvidos (núcleo canônico do repo)
- Harness de agente 'batteries-included': sub-agents com janelas isoladas, offload de tool outputs, memória persistente pluggável, HITL, model-agnostic e .mcp.json nativo.

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="deepagents")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/langchain-ai/deepagents
