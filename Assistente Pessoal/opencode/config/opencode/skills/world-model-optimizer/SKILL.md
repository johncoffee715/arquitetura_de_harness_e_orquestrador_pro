---
name: world-model-optimizer
description: >-
  Distill traces de agentes → modelo oráculo menor + router frontier↔small (-27% custo, RouterBench). Inspiração p/ self-learning (sem licença). (absorvido de experientiallabs/world-model-optimizer)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/experientiallabs/world-model-optimizer
helenized: true
r84: true
r77_triple: true
---
# world-model-optimizer — otimizador world model

Helenizado de [`https://github.com/experientiallabs/world-model-optimizer`](https://github.com/experientiallabs/world-model-optimizer) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Distill traces de agentes → modelo oráculo menor + router frontier↔small (-27% custo, RouterBench). Inspiração p/ self-learning (sem licença). (absorvido de experientiallabs/world-model-optimizer)

## Padrões absorvidos
- otimização: world model, otimização
- Origem: https://github.com/experientiallabs/world-model-optimizer
- Domínio: otimizador world model

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `world-model-optimizer` (tags: world model, otimização).
2. `skill(name="world-model-optimizer")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/experientiallabs/world-model-optimizer
