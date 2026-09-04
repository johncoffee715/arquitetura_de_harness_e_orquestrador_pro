---
name: colibri
description: >-
  Motor de inferência MoE puro C, zero deps: roda modelos frontier 744B-2.8T em hardware consumer tratando VRAM/RAM/storage como hierarquia única (multitiering). (absorvido de JustVugg/colibri)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/JustVugg/colibri
helenized: true
r84: true
r77_triple: true
---
# colibri — colibri framework

Helenizado de [`https://github.com/JustVugg/colibri`](https://github.com/JustVugg/colibri) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Motor de inferência MoE puro C, zero deps: roda modelos frontier 744B-2.8T em hardware consumer tratando VRAM/RAM/storage como hierarquia única (multitiering). (absorvido de JustVugg/colibri)

## Padrões absorvidos
- framework: colibri, deploy
- Origem: https://github.com/JustVugg/colibri
- Domínio: colibri framework

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `colibri` (tags: colibri, deploy).
2. `skill(name="colibri")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/JustVugg/colibri
