---
tags: [entity, llm, granite, executor]
updated: 2026-08-26
---

# Granite 4.2-3B

Executor F4 / contexto-longo no slot :9087 (CPU). Substituiu Qwen3.8-9B UNKNOWN em 2026-08-26.

- **Arquivo:** granite-4.2-3b-Q4_K_M.gguf (2.24GB, Q4_K_M, 40L GQA 40/8 RoPE 10M)
- **Contexto:** 131072 nativo (512K ext), RULER 64K 67.52 / 128K 55.30
- **Benchmarks:** AIME25 78.33, GPQA 54.80, MMLU-Pro 67.84, BFCL v4 52.41, τ-bench 45.78
- **Thinking:** 3 modos (full/low/non), temp 1.0 top_p 0.95
- **Línguas:** 12 com PT
- **Empírico:** 3.25 t/s, tool-calling OK

[[decisoes/2026-08-26-swap-llm-stack]] · [[aprendizados/2026-08-26_swap-llm-stack]]
