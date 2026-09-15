---
name: llama-mtp
description: "Multi-Token Prediction (MTP) heads no llama.cpp (PR #22673 merged) — speculative decoding integrado, >2x speedup sem draft model separado; aplicar nos 4 modelos locais Vulkan. (absorvido de ggml-org/llama.cpp)"
origin: absorvido:ggml-org/llama.cpp
metadata:
  autofagia: ggml-org/llama.cpp (2026-08-04)
  prioridade: 20
  linguagem: C++
  topics: llm, inference, speculative-decoding
  artefatos: feature
  padroes_absorvidos: 1
---
# Llama Mtp

Helenizado de [`ggml-org/llama.cpp`](https://github.com/ggml-org/llama.cpp).

## Propósito
Multi-Token Prediction (MTP) heads no llama.cpp (PR #22673 merged) — speculative decoding integrado, >2x speedup sem draft model separado; aplicar nos 4 modelos locais Vulkan.

## Padrões absorvidos (núcleo canônico do repo)
- Multi-Token Prediction (MTP) heads no llama.cpp (PR #22673 merged) — speculative decoding integrado, >2x speedup sem draft model separado; aplicar nos 4 modelos locais Vulkan.

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="llama-mtp")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/ggml-org/llama.cpp
