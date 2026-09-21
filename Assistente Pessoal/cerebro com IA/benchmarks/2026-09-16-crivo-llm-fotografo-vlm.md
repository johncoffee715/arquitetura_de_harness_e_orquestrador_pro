---
setor: benchmarks
tipo: crivo
data: 2026-09-16
criterio: crivo-padrao (R83/R84) adaptado visão — T1 visão-DoP JSON/GBNF, T2 GBNF texto, T4 performance CPU
artefatos: programas de apoio/fotografo/benchmarks/result_*.json
runner: skills/fotografo/tooling/crivo_vlm.py
---

# Crivo LLM-Fotógrafo (2026-09-16) — VEREDITO

## Placar

| Candidato | T1 visão (5) | T2 GBNF (10) | tok/s CPU | lat média | RAM pico | Nota R34 |
|---|---|---|---|---|---|---|
| **Qwen2-VL-7B Q4_K_M** | 5/5 | 10/10 | 67,2 | 2,7 s | ~6 GB | **92 — CANONIZADO** |
| Qwen2-VL-2B Q4_K_M (sprinter) | 5/5 | 10/10 | 199,7 | 1,6 s | ~2,5 GB | 88 — reserva rápida |
| Gemma-3-4B-it QAT | 5/5 | 10/10 | 6,6 | 15,9 s | ~4 GB | 55 — lento demais p/ loop HITL |
| Qwen3-4B (baseline texto) | N/A (sem visão) | 10/10 | 99,9 | 0,66 s | ~2,4 GB | 40 — fina categoria errada |
| MiniCPM-V 2.6 | INELEGÍVEL | — | — | — | — | 0 — arch `minicpmv` não suportada pelo llama.cpp deste harness |

## Leituras

- Os 3 VLMs aprovados em schema: **GBNF-100%** (T1+T2 zerado falhas). A régua passa a ser precisão qualitativa (T3 — aferida com provas A/B na prática).
- **Qwen2-VL-7B** = sweet spot confirmado do brief do usuário (visão + barato): OCR/serigrafia SMD, distinção iluminação especular vs. difusa, latência sub-3s — mantém o HITL fluido.
- **Qwen2-VL-2B** fica como **sprinter** (classificação/filtragem rápida) — 199 t/s permite pré-triagem de frames do vídeo em lote.
- Gemma-3-4B-QAT tem visão boa mas 6,6 t/s inviabiliza loop interativo; fica em fitragem.

## Canonização efetiva (ação)

- role `fotografo-vlm`: **Qwen2-VL-7B-Instruct Q4_K_M** + mmproj f16 — sobe sob demanda :9188 (CPU, -t 18)
- role `fotografo-sprint`: Qwen2-VL-2B — sobe sob demanda :9187 quando necessário
- Registro no manifesto (manifest_llm.json/opencode.jsonc): **pendente aplicação user-side** (snippet pronto em skills/fotografo/tooling/registro-provider.json)

## Origem dos pesos (fonte única de verdade)
- gemma-3-4b-it-qat: ggml-org/gemma-3-4b-it-qat-GGUF ✓
- Qwen2-VL 2B/7B: bartowski/Qwen2-VL-{2B,7B}-Instruct-GGUF ✓
- Qwen3-4B: Qwen/Qwen3-4B-GGUF ✓
- MiniCPM-V-2_6: openbmb/MiniCPM-V-2_6-gguf ✓ (arquivo ok; llama.cpp não suporta)
- HF gated registradas: stabilityai SVD (licença), gemma bartowski gated → alterna
