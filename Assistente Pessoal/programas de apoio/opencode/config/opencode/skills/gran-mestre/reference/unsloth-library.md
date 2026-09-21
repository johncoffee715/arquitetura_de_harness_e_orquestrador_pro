# Unsloth — biblioteca LLM não-oficial (fonte canônica de GGUFs)

> Registrado 2026-09-04 por diretiva do usuário (guardrail R80/R36). Fonte de
> quantizações comunitárias com vasta variabilidade para fitragem → crivo → canonização.

- **Org**: `https://huggingface.co/unsloth` (+ `bartowski/*` como segunda fonte)
- **Por que**: quants dinâmicos (imatrix — preserva attention layers), range completo
  (Q2_K → Q8_0 + IQ/DQ), recomendação explícita por arquivo (Q4_K_M = default),
  `llama serve -hf <repo>:<quant>` direto, fine-tunes (GRPO) quando precisar.
- **Como usar no harness**: baixar 1 arquivo (nunca branch inteira) para `fitragem/` →
  R79 benchmark especulativo → crivo R83 local → R84 re-auditoria por nó → canoniza.
- **Evidência local**: Phi-4-mini Q4_K_M 2,49GB (guia de deploy); Qwen3-1.7B-Q4_K_M 1,28GB
  em produção :9092 com 178 t/s (R84-EXEC01).
- **Aviso**: 2-bit (Q2_K) mata modelo 3B — evidência própria 04/09 (qwen2.5-coder-3B).
  Abaixo de Q4, preferir I-quants em rocBLAS/CUDA; checar feature-matrix do llama.cpp.
