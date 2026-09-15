---
name: langgraph-redis-patterns
description: Checkpoint-store pattern — graph checkpoints on key-value TTL store (concepts only, never the servers).
category: skill
model: local-forge/proposer
---

# langgraph-redis-patterns

Padrão de checkpoint store: checkpoints de grafo stateful sobre store chave-valor
com TTL (namespace por thread, expiração por desenho). Helenizado de
`redis-developer/langgraph-redis` (origem: https://github.com/redis-developer/langgraph-redis).

> PROIBIDO como dependência (doutrina R2): vault é o estado. Só o padrão.
> Irmã `langgraph-patterns` cobre o grafo; aqui só o STORE.
