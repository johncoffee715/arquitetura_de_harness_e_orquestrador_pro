---
name: unsloth-zoo
description: "Fine-tune 2x mais rápido / 70-80% menos VRAM (gpt-oss, Qwen3 GRPO) — candidato p/ pipeline de fine-tune do oráculo local 9B. (absorvido de unslothai/unsloth-zoo)"
origin: absorvido:unslothai/unsloth-zoo
metadata:
  autofagia: unslothai/unsloth-zoo (2026-08-04)
  prioridade: 6
  linguagem: Python
  topics: finetune, vram, dataset
  artefatos: skill
  padroes_absorvidos: 1
---
# Unsloth Zoo

Helenizado de [`unslothai/unsloth-zoo`](https://github.com/unslothai/unsloth-zoo).

## Propósito
Fine-tune 2x mais rápido / 70-80% menos VRAM (gpt-oss, Qwen3 GRPO) — candidato p/ pipeline de fine-tune do oráculo local 9B.

## Padrões absorvidos (núcleo canônico do repo)
- Fine-tune 2x mais rápido / 70-80% menos VRAM (gpt-oss, Qwen3 GRPO) — candidato p/ pipeline de fine-tune do oráculo local 9B.

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="unsloth-zoo")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/unslothai/unsloth-zoo
