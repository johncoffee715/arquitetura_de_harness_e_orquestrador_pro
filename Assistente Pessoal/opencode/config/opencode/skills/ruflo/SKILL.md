---
name: ruflo
description: Agent meta-harness patterns — swarms, vector memory (HNSW), self-learning loops, federation with zero-trust (nativo-primeiro: só padrões).
category: skill
model: local-forge/proposer
---

# ruflo

Padrões do meta-harness Ruflo (ex-Claude Flow) para orquestração: swarms coordenados,
memória vetorial rápida, aprendizado com trajetórias e federação zero-trust.
Helenizado de `ruvnet/ruflo` (origem: https://github.com/ruvnet/ruflo).

> Nativo-primeiro: o harness NÃO importa stack alheia — absorve SOMENTE os padrões
> (topologia, memória, aprendizado, federação). Nada de dependência do `npx ruflo`.

## Quando usar

- Coordenar múltiplos agentes numa task (hierarquia/mesh/adaptativo + consenso)
- Memória persistente com retrieval rápido (HNSW > força bruta acima do crossover)
- Aprender com trajetórias (padrões de sucesso viram roteamento futuro)
- Colaboração cross-máquina com zero-trust (mTLS + ed25519, PII stripada)

## Como usar

1. **Swarm**: topologia por task (hierárquica p/ comando, mesh p/ pares) + consenso
2. **Memória**: AgentDB/HNSW p/ store + recall@10; namespaces por agente
3. **Aprendizado**: SONA/trajetórias alimentam o roteador (89% alvo)
4. **Federação**: `init` → `join` → send com PII-strip; trust sobe com histórico, cai no 1º mau comportamento

## Princípio

`Agent = Model + Harness`: o modelo escreve, o harness dá tools, memória, loops e controles.
