# Tabela da Verdade MÁXIMA — conflito Stack vs Candidatos (2026-09-15 18:47)

## Stack canônica (10 slots)

| Slot | Modelo | Papel | Placar | Dec CPU | Dec GPU | Pre CPU | Pre GPU | KV KB/1k | ctx serv | ctx train | GB | Quant | Veredito |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8083 | Qwen3.5-35B-A3B-UD-IQ3_XXS | orquestrador | 3.3 | 26.5 | — | — | — | 5.76 | 262144 | 262144 | 12.29 | IQ3_XXS | KEEP |
| 9084 | RWKV7-0.4B-FP16 | córtex | 0.0 | — | 143.3 | — | — | 0.0 | 1048576 | 1048576 | 0.91 | FP16 | KEEP |
| 9088 | Llama-3.2-1B-IQ4_XS | proposer | 4.0 | — | 240.5 | — | — | 8.0 | 131072 | 131072 | 0.9 | IQ4_XS | KEEP |
| 9090 | Llama-3.2-3B-UD-IQ3_XXS | refuter | 3.5 | 12.2 | — | — | — | 28.0 | 32768 | 32768 | 2.0 | IQ3_XXS | KEEP |
| 9092 | SmolLM2-1.7B-Q4_K_M | relay | 3.5 | 17.3 | — | — | — | 0.0 | 32768 | 32768 | 1.1 | Q4_K_M | KEEP (CPU) |
| 9093 | SmolLM2-360M-Q8_0 | descoberta | 2.0 | — | 400 | — | — | 2.5 | 4096 | 4096 | 0.4 | Q8_0 | KEEP |
| 9095 | Qwen1.5-MoE-A2.7B-Q3_K_M | warm | 3.0 | 4.0 | — | — | — | 1.15 | 8192 | 8192 | 1.7 | Q3_K_M | KEEP |
| 9086 | LFM2.5-1.2B-ToMoE-Q4_K_M | reflexo | N/A | 26.7 | — | — | — | 3.8 | 128000 | 128000 | 1.0 | Q4_K_M | KEEP |
| 9094 | Qwen3-Emb-0.6B-CPU | embedder | — | 14702 | — | — | — | 14.0 | 2048 | 2048 | 0.6 | Q8_0 | UNIFICAR |
| 9097 | Qwen3-Emb-0.6B-GPU | embedder | — | — | 90982 | — | — | 14.0 | 2048 | 2048 | 0.6 | Q8_0 | UNIFICAR |

## Candidatos (filtragem)

| Modelo | Placar | Dec CPU | Dec GPU | Pre CPU | Pre GPU | ctx serv | ctx train | GB | Quant | Veredito |
|---|---|---|---|---|---|---|---|---|---|---|
| **NeoHorse-1-4B-Q5_K_M** | **4.0** | **4.82-4.88** | **102.2** | 24-42 | 184.8 | 32768 | 262144 | 3.07 | Q5_K_M | **GPU-ONLY** (CPU 3.5x lento) |
| Noema-2B-Q8_0 | 2.5 | — | 153.2 | — | 556.3 | 32768 | — | 2.01 | Q8_0 | NAO_PASSOU |
| Ornith-1.5-9B-Q8_0 | 1.0 | **1.92-2.02** | — | 12-19 | — | 32768 | — | 9.79 | Q8_0 | **DESCONTINUADO** |
| NeoHorse-1-9B-Q5_K_M | 2.0 | 1.2 | — | 9.0 | — | 16384 | — | 6.47 | Q5_K_M | NAO_PASSOU |
| Gemma-3-4B-it | 2.7 | — | — | — | — | 16384 | — | 2.49 | Q4_K_M | NAO_PASSOU |
| SmolLM3-3B | 0 | 10 | — | — | — | 16384 | — | 1.92 | Q4_K_M | NAO_PASSOU |
| Phi-3.5-mini | 1.5 | — | — | — | — | 16384 | — | 2.39 | Q4_K_M | NAO_PASSOU |
| Gemma-3-270M | 0.5 | — | — | — | — | 4096 | — | 0.25 | Q4_K_M | NAO_PASSOU |
| DeepSeek-V2-Lite | 2.4 | 13.2 | — | 24 | — | 16384 | — | 8.57 | IQ4_XS | NAO_PASSOU |
| OLMoE-1B-7B | 0 | — | — | — | — | — | — | 4.21 | Q4_K_M | NAO_PASSOU |
| Ling-3.0-tiny | — | — | — | — | — | — | — | 5.64 | Q5_K_M | BLOQUEADO |
| JetMoE-8B | — | — | — | — | — | — | — | — | — | INDISPONIVEL |
| TinyLlama-x8-MoE | — | — | — | — | — | — | — | 3.64 | Q4_K_M | NAO_PASSOU |

## Conflito de substituição (auditoria)

| Slot | Atual | Candidato | Placar | Dec CPU | Dec GPU | Veredito |
|---|---|---|---|---|---|---|
| 9092 relay | SmolLM2-1.7B (3.5/7, 17.3 CPU) | NeoHorse-4B (4.0/7, 4.85 CPU / 102 GPU) | +0.5 | **-3.5x CPU** | +6x GPU | **INVIÁVEL em CPU; VIÁVEL se slot virar GPU** |
| 9090 refuter | Llama-3.2-3B (3.5/7, 12.2 CPU) | NeoHorse-4B (4.0/7) | +0.5 | -2.5x | +8x | idem |
| 8083 orq | Qwen3.5-35B (3.3/7, 26.5 CPU) | NeoHorse-4B (4.0/7) | +0.7 | -5.5x | +4x | **NÃO** (ctx 262k vs 262k mas 35B tem janela+MoE) |
| 9095 warm | Qwen1.5-MoE (3.0/7, 4.0 CPU) | NeoHorse-4B (4.0/7) | +1.0 | +0.85 | +25x | **SIM se GPU** |

## Decisões executadas
1. Ornith-1.5-9B-Q8_0 → **DESCONTINUADO** (lixeira) — 1.92 t/s CPU vs NeoHorse 4.85 (2.5x pior) e 102 GPU (53x pior)
2. NeoHorse-1-4B-Q5_K_M → **GPU-ONLY** — só entra se houver slot GPU livre (VRAM ~3GB livre atual)
3. Embedders 9094/9097 → **UNIFICAR** (proposta: :9094 canônico CPU + :9097 GPU sob demanda via stack-toggle)
