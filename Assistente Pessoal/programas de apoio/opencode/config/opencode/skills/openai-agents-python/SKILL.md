---
name: openai-agents-python
description: Handoff-first multi-agent pattern — agents-as-tools, guardrails in/out, sessions auto-history, built-in tracing (patterns only).
category: skill
model: local-forge/proposer
---

# openai-agents-python

Padrão handoff-first: agentes delegam entre si com contexto, guardrails validam
in/out, sessions guardam histórico automaticamente, tracing embutido depura tudo.
Helenizado de `openai/openai-agents-python`
(origem: https://github.com/openai/openai-agents-python).

> Provider-agnostic no original (Responses + Chat + 100+ LLMs); aqui o padrão vale
> p/ qualquer motor. Framework NUNCA como dependência.

## Quando usar

- Delegação entre agentes com passagem de contexto (handoffs)
- Validação de segurança in/out (guardrails configuráveis)
- Histórico automático entre runs (sessions) + tracing p/ debug

## Como usar

1. **Agent**: instructions + tools (+ guardrails + handoffs p/ especialistas)
2. **Handoff**: delegar c/ contexto; agents-as-tools quando o modo é chamada
3. **Guardrails**: checks in/out; HITL onde sensível
4. **Sessions+Tracing**: histórico automático; trace p/ ver/debugar/otimizar

## Princípio

Leve por padrão; sandbox/voice/realtime só quando o caso pedir.
