---
name: deepspec
description: Speculative-decoding draft methodology — DSpark/DFlash/Eagle3 training-eval recipe + acceptance benchmarks (complement to llama-mtp).
category: skill
model: local-forge/proposer
---

# deepspec

Training/eval methodology for speculative-decoding draft models (DSpark, DFlash, Eagle3):
data-prep → train → eval with acceptance-rate benchmarks. Complemento da `llama-mtp`
(mecanismo MTP no llama.cpp) e da `llama-mtp-concept` (conceito) — aqui o FOCO é a
receita de treino/avaliação, nunca o motor de inferência.
Helenizado de `deepseek-ai/DeepSpec` (origem: https://github.com/deepseek-ai/DeepSpec).

> Correção de intake: o repo NÃO é "spec-driven development" — é speculative decoding.
> Evidência: "full-stack codebase for training and evaluating draft models for
> speculative decoding" (README).

## Quando usar

- Projetar/avaliar draft models (Eagle3/DFlash/DSpark) contra um target
- Medir acceptance-rate em benchmarks (gsm8k, humaneval, mbpp, mt-bench, …)
- Decidir algoritmo por tabela comparativa (paper arXiv:2607.05147)

## Como usar

1. **Data-prep**: prompts → respostas do target → target cache (atenção: TB-scale no default!)
2. **Train**: `train.py` (1 worker/GPU; `config_path` em `config/`; checkpoints `~/checkpoints/…/step_*`)
3. **Eval**: `eval.py` com `target_name_or_path` + `draft_name_or_path` nos benchmarks

## Princípio

Cite sempre com o setup de treino alinhado ao repo — senão a comparação é inválida.
Domínio específico? Re-finetune o draft (sobretudo se o target rodar em thinking mode).
