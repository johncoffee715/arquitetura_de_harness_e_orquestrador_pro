# Inventário VRAM — quem vive na MI50 (2026-09-15 18:55)

> Total: 17.16 GB · Usado: 12.77 GB (74%) · Livre: 4.39 GB
> Método: GGUF × fração ngl/layers + KV real (manifesto) — validado vs rocm-smi (Δ0.26GB)

## Habitantes da VRAM (ngl>0)

| Porta | Modelo | ngl | Frac | GGUF | KV | VRAM | % do total |
|---|---|---|---|---|---|---|---|
| 8083 | Qwen3.5-35B-A3B-UD-IQ3_XXS | 36/64 | 0.56 | 13.08 | 1.44 | **8.80 GB** | 69% |
| 9088 | Llama-3.2-1B-IQ4_XS | 999 | 1.0 | 0.74 | 1.00 | **1.74 GB** | 14% |
| 9084 | RWKV7-0.4B-FP16 | 999 | 1.0 | 0.91 | 0.00 | **0.91 GB** | 7% |
| 9097 | Qwen3-Emb-0.6B-GPU | 999 | 1.0 | 0.64 | 0.03 | **0.67 GB** | 5% |
| 9093 | SmolLM2-360M-Q8_0 | 999 | 1.0 | 0.39 | 0.01 | **0.40 GB** | 3% |
| — | buffers compute/overhead | — | — | — | — | **0.26 GB** | 2% |

## Fora da VRAM (CPU-only, ngl=0)

| Porta | Modelo | RAM |
|---|---|---|
| 9090 | Llama-3.2-3B-UD-IQ3_XXS | ~1.4GB |
| 9092 | SmolLM2-1.7B-Q4_K_M | ~1.1GB |
| 9086 | LFM2.5-1.2B-ToMoE-Q4_K_M | ~0.7GB |
| 9095 | Qwen1.5-MoE-A2.7B-Q3_K_M | ~7.4GB (MoE) |
| 9094 | Qwen3-Emb-0.6B-CPU | ~0.6GB |

## Fatos para decisão

1. **8083 domina 69% da VRAM** (8.80GB) — é o orquestrador, intocável (R39)
2. **Livre: 4.39GB** — cabe 1 modelo de até ~4GB com ctx pequeno
3. **NeoHorse-4B (3.07GB)** cabe na folga SE o ctx for pequeno (KV q4: 3.07 + ~0.3GB KV@8k = 3.4GB) — **viável**
4. **9097 embedder GPU (0.67GB)** é o candidato natural a desligar sob demanda (R5/R10) → libera 0.67GB
5. **Unificar 9094/9097**: manter :9094 CPU canônico + :9097 GPU toggle = libera 0.67GB permanente quando ocioso
6. **9095 MoE (7.4GB RAM)** é o maior consumidor de RAM — candidato a desligar se NeoHorse-4B entrar na GPU
