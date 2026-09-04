---
name: unsloth-zoo
description: >-
  Fine-tune 2x mais rápido / 70-80% menos VRAM (gpt-oss, Qwen3 GRPO) — candidato p/ pipeline de fine-tune do oráculo local 9B. (absorvido de unslothai/unsloth-zoo)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/unslothai/unsloth-zoo
helenized: true
r84: true
r77_triple: true
---
# unsloth-zoo — Unsloth Zoo

Helenizado de [`https://github.com/unslothai/unsloth-zoo`](https://github.com/unslothai/unsloth-zoo) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Fine-tune 2x mais rápido / 70-80% menos VRAM (gpt-oss, Qwen3 GRPO) — candidato p/ pipeline de fine-tune do oráculo local 9B. (absorvido de unslothai/unsloth-zoo)

## Padrões absorvidos
- fine-tuning: unsloth, fine-tuning
- Origem: https://github.com/unslothai/unsloth-zoo
- Domínio: Unsloth Zoo

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `unsloth-zoo` (tags: unsloth, fine-tuning).
2. `skill(name="unsloth-zoo")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/unslothai/unsloth-zoo
