---
name: llama-mtp
description: >-
  Multi-Token Prediction (MTP) heads no llama.cpp (PR #22673 merged) — speculative decoding integrado, >2x speedup sem draft model separado; aplicar nos 4 modelos locais Vulkan. (absorvido de ggml-org/llama.cpp)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/ggml-org/llama.cpp
helenized: true
r84: true
r77_triple: true
---
# llama-mtp — MTP llama.cpp

Helenizado de [`https://github.com/ggml-org/llama.cpp`](https://github.com/ggml-org/llama.cpp) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Multi-Token Prediction (MTP) heads no llama.cpp (PR #22673 merged) — speculative decoding integrado, >2x speedup sem draft model separado; aplicar nos 4 modelos locais Vulkan. (absorvido de ggml-org/llama.cpp)

## Padrões absorvidos
- inferência: MTP, speculative decoding, llama.cpp
- Origem: https://github.com/ggml-org/llama.cpp
- Domínio: MTP llama.cpp

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `llama-mtp` (tags: MTP, speculative decoding).
2. `skill(name="llama-mtp")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/ggml-org/llama.cpp
