---
name: longhorizon-harness
description: >-
  Harness de execução long-horizon: 3 papéis (Manager/Executor/Auditor), estado verificado durável e contexto-fresco por rodada p/ tarefas de várias horas em desktop+CLI. (absorvido de AMAP-ML/LongHorizon-Harness)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/AMAP-ML/LongHorizon-Harness
helenized: true
r84: true
r77_triple: true
---
# longhorizon-harness — harness long horizon

Helenizado de [`https://github.com/AMAP-ML/LongHorizon-Harness`](https://github.com/AMAP-ML/LongHorizon-Harness) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Harness de execução long-horizon: 3 papéis (Manager/Executor/Auditor), estado verificado durável e contexto-fresco por rodada p/ tarefas de várias horas em desktop+CLI. (absorvido de AMAP-ML/LongHorizon-Harness)

## Padrões absorvidos
- planejamento longo: long horizon, planejamento
- Origem: https://github.com/AMAP-ML/LongHorizon-Harness
- Domínio: harness long horizon

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `longhorizon-harness` (tags: long horizon, planejamento).
2. `skill(name="longhorizon-harness")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/AMAP-ML/LongHorizon-Harness
