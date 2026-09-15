---
name: andrej-karpathy-skills
description: Karpathy's 4 anti-pitfall gates for LLM coding — think before coding, simplicity first, surgical changes, goal-driven execution.
category: skill
model: local-forge/proposer
---

# andrej-karpathy-skills

Four enforceable principles that fix the most costly LLM coding pitfalls, derived from
Andrej Karpathy's observations. Helenizado de `multica-ai/andrej-karpathy-skills`
(origem: https://github.com/multica-ai/andrej-karpathy-skills).

## Os 4 princípios (gates)

1. **Think Before Coding** — state assumptions, present interpretations, push back, stop when confused
2. **Simplicity First** — minimum code that solves it; no speculative abstraction (teste do sênior)
3. **Surgical Changes** — touch only what the request traces to; clean only your own orphans
4. **Goal-Driven Execution** — declarative success criteria + verify loop (tests-first)

## Quando usar

- Antes de aprovar qualquer diff gerado por LLM (code review gate)
- Ao escrever prompts/specs para agentes (exigir critérios verificáveis)
- Quando um diff vem inchado ou com refactors não pedidos (apontar a violação exata)

## Tradeoff

Viés p/ cautela, não velocidade. Tarefa trivial (typo, one-liner óbvio) usa julgamento, não o rigor total.
