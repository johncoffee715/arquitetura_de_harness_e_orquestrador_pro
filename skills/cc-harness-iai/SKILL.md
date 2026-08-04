---
name: cc-harness-iai
description: "Padrão PRD→tasks→impl: task-master-generator (fan-out p/ inspecionar código e gerar tasks com dependencies) + task-sequencer/tools.yaml (pontuação de tools por task, Injeção 'Available Tools'). Inspiração (sem licença). (absorvido de elberrd/cc-harness-iai)"
origin: absorvido:elberrd/cc-harness-iai
metadata:
  autofagia: elberrd/cc-harness-iai (2026-08-04)
  prioridade: 16
  linguagem: Shell
  topics: harness, task-decomposition, tools
  artefatos: skill+feature
  padroes_absorvidos: 1
---
# Cc Harness Iai

Helenizado de [`elberrd/cc-harness-iai`](https://github.com/elberrd/cc-harness-iai).

## Propósito
Padrão PRD→tasks→impl: task-master-generator (fan-out p/ inspecionar código e gerar tasks com dependencies) + task-sequencer/tools.yaml (pontuação de tools por task, Injeção 'Available Tools'). Inspiração (sem licença).

## Padrões absorvidos (núcleo canônico do repo)
- Padrão PRD→tasks→impl: task-master-generator (fan-out p/ inspecionar código e gerar tasks com dependencies) + task-sequencer/tools.yaml (pontuação de tools por task, Injeção 'Available Tools'). Inspiração (sem licença).

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="cc-harness-iai")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/elberrd/cc-harness-iai
