---
name: langfuse
description: LLM observability loop — trace (@observe), prompt versioning, datasets+runs, evals (judge/code/human), playground iteration.
category: skill
model: local-forge/proposer
---

# langfuse

Loop observar→avaliar→melhorar p/ apps LLM: tracing instrumentado, prompts
versionados, datasets com runs comparáveis, avaliações e playground.
Helenizado de `langfuse/langfuse` (origem: https://github.com/langfuse/langfuse).

> Nativo-primeiro: só o loop observability. Plataforma (docker/postgres/clickhouse)
> ou cloud NUNCA como dependência — o harness já tem MELT nativo (vault+JSONL).

## Quando usar

- Instrumentar chamadas LLM (trace com retrieval/embedding/agent actions)
- Versionar prompts sem latência extra (cache server+client)
- Avaliar (LLM-judge, code, feedback humano) sobre datasets antes do deploy
- Debugar sessão ruim: trace → playground, itera e volta

## Como usar

1. **Trace**: `@observe()` em volta das chamadas (params do modelo capturados)
2. **Prompt**: versionar e iterar colaborativamente
3. **Dataset+run**: test sets, benchmarks, experimentos estruturados
4. **Eval**: judge/code/humano/custom via API/SDK; playground p/ iteração rápida

## Princípio

Todo run comparável; todo prompt versionado; toda avaliação com evidência.
