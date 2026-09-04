---
name: deepagents
description: >-
  Harness de agente 'batteries-included': sub-agents com janelas isoladas, offload de tool outputs, memória persistente pluggável, HITL, model-agnostic e .mcp.json nativo. (absorvido de langchain-ai/deepagents)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/langchain-ai/deepagents
helenized: true
r84: true
r77_triple: true
---
# deepagents — deep agents

Helenizado de [`https://github.com/langchain-ai/deepagents`](https://github.com/langchain-ai/deepagents) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Harness de agente 'batteries-included': sub-agents com janelas isoladas, offload de tool outputs, memória persistente pluggável, HITL, model-agnostic e .mcp.json nativo. (absorvido de langchain-ai/deepagents)

## Padrões absorvidos
- agentes: agente profundo, hierarquia
- Origem: https://github.com/langchain-ai/deepagents
- Domínio: deep agents

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `deepagents` (tags: agente profundo, hierarquia).
2. `skill(name="deepagents")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/langchain-ai/deepagents
