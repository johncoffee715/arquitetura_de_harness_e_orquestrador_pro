---
name: langgraph-patterns
description: Stateful agent graph pattern — state schema + nodes + edges + checkpoint/resume + HITL interrupts + short/long memory (patterns only).
category: skill
model: local-forge/proposer
---

# langgraph-patterns

Padrão de grafo stateful para agentes resilientes: schema de estado + nós + arestas,
checkpointing (persist/resume exato), interrupts humanos em qualquer ponto e memória
curta + longa. Helenizado de `langchain-ai/langgraph`
(origem: https://github.com/langchain-ai/langgraph).

> PROIBIDO como dependência (doutrina R2): vault é a memória, catálogo é o registro.
> Aqui só o padrão de grafo stateful.

## Quando usar

- Workflow longo que precisa sobreviver a falhas (resume do ponto exato)
- Gates humanos no meio da execução (inspecionar/modificar estado em qualquer ponto)
- Agentes com memória de sessão + memória persistente entre sessões

## Como usar

1. **Estado**: schema tipado (o que o grafo carrega)
2. **Grafo**: nós (steps) + arestas (transições, condicionais inclusas)
3. **Checkpoint**: persistir por step; resume exato pós-falha
4. **Interrupts**: pontos HITL (inspecionar/modificar antes de seguir)
5. **Memória**: curta (working) + longa (persistente)

## Princípio

Durabilidade antes de velocidade: todo step persistido, todo gate explícito.
