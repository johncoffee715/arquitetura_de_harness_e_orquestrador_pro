---
name: cc-harness-iai
description: >-
  Padrão PRD→tasks→impl: task-master-generator (fan-out p/ inspecionar código e gerar tasks com dependencies) + task-sequencer/tools.yaml (pontuação de tools por task, Injeção 'Available Tools'). Inspiração (sem licença). (absorvido de elberrd/cc-harness-iai)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/elberrd/cc-harness-iai
helenized: true
r84: true
r77_triple: true
---
# cc-harness-iai — harness CC IAI

Helenizado de [`https://github.com/elberrd/cc-harness-iai`](https://github.com/elberrd/cc-harness-iai) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Padrão PRD→tasks→impl: task-master-generator (fan-out p/ inspecionar código e gerar tasks com dependencies) + task-sequencer/tools.yaml (pontuação de tools por task, Injeção 'Available Tools'). Inspiração (sem licença). (absorvido de elberrd/cc-harness-iai)

## Padrões absorvidos
- harness: harness, IAI, orquestração
- Origem: https://github.com/elberrd/cc-harness-iai
- Domínio: harness CC IAI

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `cc-harness-iai` (tags: harness, IAI).
2. `skill(name="cc-harness-iai")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/elberrd/cc-harness-iai
