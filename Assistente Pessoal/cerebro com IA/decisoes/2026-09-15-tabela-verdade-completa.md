# Tabela da Verdade Completa — Stack + Candidatos (2026-09-15)

> Fonte: crivo-padrão /7 (Fase A chat + Fase C trilhos + RAW), manifesto_llm.json (física), logs llama-server (t/s), /v1/models (ctx/params). Medido = régua da sessão; manifesto = benchmark R76/R79.

## Stack canônica (10 slots UP)

| Slot | Modelo | Papel | Placar /7 | Decode t/s | Prefill t/s | KV KB/1k | KV GB@ctx | ctx serv | ctx train | GB disco | Quant | Dev |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8083 | Qwen3.5-35B-A3B-UD-IQ3_XXS | orquestrador | 3.3 | 26.5 | — | 5.76 | 1.51 | 262144 | 262144 | 12.29 | IQ3_XXS | CPU+36ngl |
| 9084 | RWKV7-0.4B-FP16 | córtex/tálamo | 0.0 (piso) | 143.3 | — | 0.0 | 0.064 | 1048576 | 1048576 | 0.91 | FP16 | GPU |
| 9088 | Llama-3.2-1B-IQ4_XS | proposer/contrato | 4.0 | 240.5 | — | 8.0 | 1.07 | 131072 | 131072 | 0.9 | IQ4_XS | GPU |
| 9090 | Llama-3.2-3B-UD-IQ3_XXS | refuter | 3.5 | 12.2 | — | 28.0 | 0.94 | 32768 | 32768 | 2.0 | IQ3_XXS | CPU |
| 9092 | SmolLM2-1.7B-Q4_K_M | relay | 3.5 | 17.3 | — | 0.0 | 0.0 | 32768 | 32768 | 1.1 | Q4_K_M | CPU |
| 9093 | SmolLM2-360M-Q8_0 | descoberta | 2.0 | 400 | — | 2.5 | 0.01 | 4096 | 4096 | 0.4 | Q8_0 | GPU |
| 9095 | Qwen1.5-MoE-A2.7B-Q3_K_M | warm | 3.0 | 4.0 | — | 1.15 | 0.01 | 8192 | 8192 | 1.7 | Q3_K_M | CPU |
| 9086 | LFM2.5-1.2B-ToMoE-Q4_K_M | reflexo | N/A | 26.7 | — | 3.8 | 0.49 | 128000 | 128000 | 1.0 | Q4_K_M | CPU |
| 9094 | Qwen3-Emb-0.6B-CPU | embedder | — | 14702 | — | 14.0 | 0.028 | 2048 | 2048 | 0.6 | Q8_0 | CPU |
| 9097 | Qwen3-Emb-0.6B-GPU | embedder | — | 90982 | — | 14.0 | 0.028 | 2048 | 2048 | 0.6 | Q8_0 | GPU |

## Candidatos (filtragem, medidos na sessão)

| Modelo | Papel proposto | Placar /7 | Decode t/s | Prefill t/s | ctx serv | ctx train | GB disco | Quant | Dev | Veredito |
|---|---|---|---|---|---|---|---|---|---|---|
| NeoHorse-1-4B-Q5_K_M | F4 executor | **4.0** | 102.2 | 184.8 | 32768 | 262144 | 3.07 | Q5_K_M | GPU | **APROVADO** (substitui :9092) |
| Noema-2B-Q8_0 | gate auditor | 2.5 | 153.2 | 556.3 | 32768 | — | 2.01 | Q8_0 | GPU | NAO_PASSOU (T1/T2 vazios) |
| Ornith-1.5-9B-Q8_0 | orq candidato | 1.0 | 3.4 | 14.9 | 32768 | — | 9.79 | Q8_0 | CPU | NAO_PASSOU (lento) |
| NeoHorse-1-9B-Q5_K_M | F6 scaffold | 2.0 | 1.2 | 9.0 | 16384 | — | 6.47 | Q5_K_M | CPU | NAO_PASSOU (lento) |
| Gemma-3-4B-it-Q4_K_M | — | 2.7 | — | — | 16384 | — | 2.49 | Q4_K_M | CPU | NAO_PASSOU |
| SmolLM3-3B-Q4_K_M | — | 0 | 10 | — | 16384 | — | 1.92 | Q4_K_M | CPU | NAO_PASSOU (content vazio) |
| Phi-3.5-mini-Q4_K_M | — | 1.5 | — | — | 16384 | — | 2.39 | Q4_K_M | CPU | NAO_PASSOU |
| Gemma-3-270M-Q4_K_M | — | 0.5 | — | — | 4096 | — | 0.25 | Q4_K_M | CPU | NAO_PASSOU (eco) |
| DeepSeek-V2-Lite-IQ4_XS | — | 2.4 | 13.2 | 24 | 16384 | — | 8.57 | IQ4_XS | CPU | NAO_PASSOU |
| OLMoE-1B-7B-Q4_K_M | — | 0 | — | — | — | — | 4.21 | Q4_K_M | CPU | NAO_PASSOU (gibberish) |
| Ling-3.0-tiny-Q5_K_M | — | — | — | — | — | — | 5.64 | Q5_K_M | — | BLOQUEADO (arch) |
| JetMoE-8B | — | — | — | — | — | — | — | — | — | INDISPONIVEL (repos vazios) |
| TinyLlama-x8-MoE-Q4_K_M | — | — | — | — | — | — | 3.64 | Q4_K_M | — | NAO_PASSOU (arch) |

## Notas de custo
- KV KB/1k: manifesto (R76 q4_0/q4_0). RWKV = 0 (state fixo). 9092 = 0 (MoE relay sem KV medido).
- t/s decode: manifesto (bench R76/R79) p/ stack; logs llama-server p/ candidatos.
- NeoHorse-4B: único candidato acima do limiar (4.0/7) — aprovado para substituir :9092.
- Ornith-9B: MTP head presente (nextn_predict_layers=1) mas sem ganho; 3.4 t/s CPU não substitui 8083.
