---
name: llama-mtp-concept
description: >-
  Conceito Multi-Token Prediction (DeepSeek-V3, Nemotron 3) — fundamenta a feature llama-mtp; docs de arquitetura de inferência. (absorvido de tryigit/cleveres-ai)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/tryigit/cleveres-ai
helenized: true
r84: true
r77_triple: true
---
# llama-mtp-concept — conceito MTP

Helenizado de [`https://github.com/tryigit/cleveres-ai`](https://github.com/tryigit/cleveres-ai) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Conceito Multi-Token Prediction (DeepSeek-V3, Nemotron 3) — fundamenta a feature llama-mtp; docs de arquitetura de inferência. (absorvido de tryigit/cleveres-ai)

## Padrões absorvidos
- conceito MTP: MTP, conceito, arquitetura
- Origem: https://github.com/tryigit/cleveres-ai
- Domínio: conceito MTP

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `llama-mtp-concept` (tags: MTP, conceito).
2. `skill(name="llama-mtp-concept")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/tryigit/cleveres-ai
