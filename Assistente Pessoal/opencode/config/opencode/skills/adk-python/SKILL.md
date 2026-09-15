---
name: adk-python
description: Code-first agent pattern — Agent/Workflow duality, Task API delegation, tool confirmation HITL, eval sets (patterns only).
category: skill
model: local-forge/proposer
---

# adk-python

Padrão code-first p/ agentes: `Agent` (name/model/instruction) + `Workflow`
(grafo de arestas) + Task API (delegação multi-turn) + confirmação de tools (HITL)
+ eval sets. Helenizado de `google/adk-python`
(origem: https://github.com/google/adk-python).

> PROIBIDO como dependência (doutrina R2). Aqui só o padrão Agent/Workflow/Task.

## Quando usar

- Agente simples (só `Agent`) vs orquestração ( `Workflow` com arestas)
- Delegação agente→agente com modo multi-turn
- Tools perigosas com confirmação explícita antes de executar
- Eval antes do deploy (`adk eval` + evalset)

## Como usar

1. **Agent**: name + model + instruction (+ tools)
2. **Workflow**: edges `[("START", a, b)]` p/ routing/fan-out/loops/retry/estado
3. **Task API**: delegação single-turn (output controlado) ou multi-turn
4. **Confirm**: tools sensíveis exigem HITL; eval roda no evalset versionado

## Princípio

Código primeiro (testável, versionável); no-code (`Agent Config`) só p/ casos simples.
