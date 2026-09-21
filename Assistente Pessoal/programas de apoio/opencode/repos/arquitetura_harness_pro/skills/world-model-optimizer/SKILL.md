---
name: world-model-optimizer
description: "Distill traces de agentes → modelo oráculo menor + router frontier↔small (-27% custo, RouterBench). Inspiração p/ self-learning (sem licença). (absorvido de experientiallabs/world-model-optimizer)"
---
# World Model Optimizer

Helenizado de [`experientiallabs/world-model-optimizer`](https://github.com/experientiallabs/world-model-optimizer).

## Propósito
Distill traces de agentes → modelo oráculo menor + router frontier↔small (-27% custo, RouterBench). Inspiração p/ self-learning (sem licença).

## Padrões absorvidos (núcleo canônico do repo)
- Distill traces de agentes → modelo oráculo menor + router frontier↔small (-27% custo, RouterBench). Inspiração p/ self-learning (sem licença).

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="world-model-optimizer")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/experientiallabs/world-model-optimizer
