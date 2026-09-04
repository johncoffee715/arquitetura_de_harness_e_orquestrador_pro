---
name: worldmonitor
description: >-
  Real-time global intelligence dashboard. AI-powered news aggregation, geopolitical monitoring, infrastructure tracking. (absorvido de koala73/worldmonitor)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/koala73/worldmonitor
helenized: true
r84: true
r77_triple: true
---
# worldmonitor — dashboard inteligência global

Helenizado de [`https://github.com/koala73/worldmonitor`](https://github.com/koala73/worldmonitor) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Real-time global intelligence dashboard. AI-powered news aggregation, geopolitical monitoring, infrastructure tracking. (absorvido de koala73/worldmonitor)

## Padrões absorvidos
- inteligência: 500+ feeds, mapa 3D, CII
- Origem: https://github.com/koala73/worldmonitor
- Domínio: dashboard inteligência global

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `worldmonitor` (tags: 500+ feeds, mapa 3D).
2. `skill(name="worldmonitor")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/koala73/worldmonitor
