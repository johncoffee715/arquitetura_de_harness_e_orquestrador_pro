---
name: orca
description: >-
  Orca is the ADE for working with a fleet of parallel agents. Run any coding agent with your own subscription. (absorvido de stablyai/orca)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/stablyai/orca
helenized: true
r84: true
r77_triple: true
---
# orca — Orca

Helenizado de [`https://github.com/stablyai/orca`](https://github.com/stablyai/orca) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Orca is the ADE for working with a fleet of parallel agents. Run any coding agent with your own subscription. (absorvido de stablyai/orca)

## Padrões absorvidos
- modelo: orca, modelo
- Origem: https://github.com/stablyai/orca
- Domínio: Orca

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `orca` (tags: orca, modelo).
2. `skill(name="orca")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/stablyai/orca
