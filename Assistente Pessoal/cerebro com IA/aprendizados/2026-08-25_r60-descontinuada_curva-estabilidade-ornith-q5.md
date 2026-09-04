---
data: 2026-08-25
tipo: retificacao-regra + experimento-em-curso
tags: [r60, ornith, kv-cache, rope, curva-estabilidade, vulkan]
---

# R60 descontinuada → R60-v3: curva-de-estabilidade empírica

## O que foi refutado (com evidência local)

1. **R60 original ("131072 FIXO")** — calculou KV como não-quantizado (K=q8_0 → 52.7 KB/tok
   → 13.95GB @262K). Com KV quantizado o teto físico sobe; e o limite REAL nunca foi VRAM,
   é cognitivo.
2. **`--rope-scale 4.0` / `--rope-freq-base 1M` (consultoria externa)** — header do GGUF
   (`qwen35.rope.freq_base = 10000000`, `context_length = 262144`) prova que o modelo nasce
   com geometria para 262K. Escala manual = distorção para posição nunca treinada.
3. **`-fa` acelera/estabiliza no Vulkan** — bench A/B/C (ornith-q5, 8K tokens):
   sem fa = **80.3 t/s**, com fa = 72.5 t/s, ubatch 8192+fa = 49.7 t/s. No MI50/Vulkan desta
   build v6, `-fa` REDUZ throughput de prefill em ~10%.
4. **`--cache-reuse` com contexto unificado** — log: "not supported by this context, disabled".

## O que vale (doutrina R60-v3)

- Limite operacional do slot = **ponto de estabilidade medido por probe**
  (needle-in-haystack: recall a 5/25/50/75/95% de profundidade + detector de invenção),
  NUNCA o máximo que a KV aloca.
- Orquestrador evacua/comprime contexto ANTES do limiar medido.
- Fenômeno Q4 @146K (24/08): causa provável = erro acumulado KV-quant + atenção longa,
  não RoPE.

## Estado do slot :8083 (25/08)

| Parâmetro | Valor |
|---|---|
| Modelo | Ornith-1.5-9B-Q5_K_M (Q4 excluído pelo usuário) |
| Contexto | `-c 163840` (máx seguro com KV q5/q5: 48 KB/tok) |
| KV | K=q5_0 · V=q5_0 (decisão usuário) |
| Sampling | t0.6 tp0.95 tk20 (agentic R61); antiloop t0.45/rp1.08/pp0.15/fp0.05 = perfil opcional |
| Flags | sem -fa, sem context-shift, sem rope manual |

## Probe em curso

`scripts/watchers/alucination_probe.py` — alvos **100K · 128K · 146K · 160K** no Ornith-Q5;
saída `state/watcher/probe-verdict.json`. Resultado alimentará `limite_cognitivo_ctx`
no manifesto_llm.json e definirá o gatilho de evacuação do orquestrador.
