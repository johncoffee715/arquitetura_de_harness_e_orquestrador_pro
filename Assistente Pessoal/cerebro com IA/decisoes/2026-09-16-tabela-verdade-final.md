# Tabela da Verdade FINAL CONSOLIDADA — 2026-09-16

> Estado: 11 slots (10 UP + 1 WARM) · VRAM 15.45GB (90%) · Filtragem vazia · Sync OK
> Fonte: crivo /7 (A cru + B quarteto), manifesto, logs, GGUF parser

## Stack canônica final

| Porta | Modelo | Papel | Placar | Decode | Prefill | KV KB/1k | ctx | GB | Quant | Dev | VRAM |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 8083 | Qwen3.5-35B-A3B-UD-IQ3_XXS | orquestrador | 3.3 | 26.5 | — | 5.76 | 262144 | 12.29 | IQ3_XXS | CPU+36ngl | 8.80 |
| 9084 | RWKV7-0.4B-FP16 | córtex | 0.0 | 143.3 | — | 0.0 | 1048576 | 0.91 | FP16 | GPU | 0.91 |
| 9088 | Llama-3.2-1B-IQ4_XS | proposer | 4.0 | 240.5 | — | 8.0 | 131072 | 0.9 | IQ4_XS | GPU | 1.74 |
| 9090 | Llama-3.2-3B-UD-IQ3_XXS | refuter | 3.5 | 12.2 | — | 28.0 | 32768 | 2.0 | IQ3_XXS | CPU | 0.0 |
| 9092 | SmolLM2-1.7B-Q4_K_M | relay | 3.5 | 17.3 | — | 0.0 | 32768 | 1.1 | Q4_K_M | CPU | 0.0 |
| 9093 | SmolLM2-360M-Q8_0 | descoberta | 2.0 | 400 | — | 2.5 | 4096 | 0.4 | Q8_0 | CPU | 0.0 |
| 9086 | LFM2.5-1.2B-ToMoE | reflexo | N/A | 26.7 | — | 3.8 | 128000 | 1.0 | Q4_K_M | CPU | 0.0 |
| 9094 | Qwen3-Emb-0.6B-CPU | embedder | — | 14702 | — | 14.0 | 2048 | 0.6 | Q8_0 | CPU | 0.0 |
| 9097 | Qwen3-Emb-0.6B-GPU | embedder | — | 90982 | — | 14.0 | 2048 | 0.6 | Q8_0 | GPU-WARM | 0.0 |
| **9095** | **NeoHorse-1-4B-Q5_K_M** | **executor F4** | **5.1** | **102.2** | **184.8** | **8.0** | **262144** | **3.06** | **Q5_K_M** | **GPU** | **5.07** |
| **9098** | **Noema-2B.Q4_K_S** | **executor-cego** | **3.0** | **13.7** | **82.2** | **3.0** | **32768** | **1.21** | **Q4_K_S** | **CPU** | **0.0** |

## Resumo da sessão (canonizações + descartes)

### Canonizados
1. **NeoHorse-1-4B-Q5_K_M** :9095 executor F4 — 5.1/7 (topo), ctx 262k, quarteto completo
2. **Noema-2B.Q4_K_S** :9098 executor-cego — 3.0/7 (sweet spot sweep Q2→Q5), 1.21GB

### Descontinuados (lixeira)
- Qwen1.5-MoE-A2.7B (substituído por NeoHorse-4B)
- Ornith-1.5-9B-Q8_0 (1.92 t/s CPU)
- Ornith-1.5-9B-IQ2_M (1.5/7)
- Ornith-1.5-35B-A3B-IQ2_XXS (0.5/7, 2 versões)
- Qwen3.5-35B-UD-IQ2_XXS (2.0/7)
- Ornith-9B-Q4KM16 (arquivo parcial)
- SmolLM3-3B, Gemma-3-4B, Gemma-3-270M, Phi-3.5-mini (0-2.7/7)
- DeepSeek-V2-Lite, OLMoE, TinyLlama-MoE, Ling, JetMoE (arch/inválidos)

### Otimizações de hardware
- Embedders unificados (:9097 GPU → WARM)
- 9093 SmolLM2-360M → CPU
- VRAM: 16.76 → 15.45GB (liberou 1.3GB)

### Infra
- ComfyUI 0.36.0 instalado (:8188, pesos em /home/johncoffee/pesos confyui/)

## Decisões de papel (auditoria)
1. **Proposer (9088)**: MANTER Llama-1B (velocidade 2.4x, formato estrito)
2. **Executor F4 (9095)**: NeoHorse-4B (capacidade, ctx 262k)
3. **Executor-cego (9098)**: Noema-Q4_K_S (obediência estrita, sem quarteto)
4. **Orquestrador (8083)**: intocável (R39)

## Gargalos abertos
1. 8083: 26.5 t/s CPU (assumido)
2. 9086 LFM: thinking-burn (cura R57 em G4)
3. VRAM 90%: sem espaço p/ novos modelos GPU
