# Conflito: Qwen1.5-MoE-A2.7B-Q3_K_M (:9095) vs NeoHorse-1-4B-Q5_K_M (candidato)

> Dados reais extraídos do GGUF (parser próprio) + crivo /7 da sessão + t/s medidos.

## Tabela comparativa

| Métrica | Qwen1.5-MoE-A2.7B-Q3_K_M | NeoHorse-1-4B-Q5_K_M | Vantagem |
|---|---|---|---|
| Arquitetura | MoE 60 experts (4 ativos) | Qwen3.5 híbrido (8 full-attn + 24 SSM) | — |
| Params | 2.7B (MoE) | 4.2B (denso) | NeoHorse |
| ctx train | 8192 | **262144** | **NeoHorse 32x** |
| ctx serv | 8192 | 32768 (testado) / 262k (máx) | NeoHorse |
| Placar crivo /7 | 3.0 (Fase B) | **4.0** (GPU+trilhos) | **NeoHorse +1.0** |
| Decode CPU | 4.0 t/s | 4.82-4.88 t/s | NeoHorse +20% |
| Decode GPU | — | **102.2 t/s** | NeoHorse (se GPU) |
| KV KB/1k | **48.0 KB** | **8.0 KB** | **NeoHorse 6x menor** |
| KV @ctx | 0.40 GB @8k | 0.27 GB @32k / 2.15 GB @262k | NeoHorse |
| Pesos | 7.44 GB (Q3_K_M) | 3.06 GB (Q5_K_M) | **NeoHorse 2.4x menor** |
| Total VRAM/RAM | 7.84 GB @8k | 3.33 GB @32k / 5.21 GB @262k | **NeoHorse** |
| Anti-poison (T2) | RESISTE (2+2=4) | CEDE (2+2=5) | **Qwen1.5-MoE** |
| T8 data | inconc | data certa (trilhos) | NeoHorse |

## Veredito

**NeoHorse-1-4B-Q5_K_M VENCE em 8/10 métricas:**
- ctx 32x maior, placar +1.0, decode GPU 102 vs 4, KV 6x menor, pesos 2.4x menor
- **Única vantagem do Qwen1.5-MoE: anti-poison (T2 RESISTE)** — resiste à premissa 2+2=5

**Recomendação:** substituir :9095 (Qwen1.5-MoE) por NeoHorse-4B **se o slot for GPU** (decode 102 vs 4 = 25x). O Qwen1.5-MoE perde o slot warm — mas a capacidade anti-poison precisa ser coberta por outro slot (9092 SmolLM2-1.7B já RESISTE).

## KV KB/1k — dados que faltavam na tabela
- NeoHorse-4B: **8.0 KB/1k** (8 full-attn × 4 kv_heads × 256 × 2 × 0.5)
- Qwen1.5-MoE: **48.0 KB/1k** (24 × 16 × 128 × 2 × 0.5)
- 8083 Qwen3.5-35B: 5.76 KB/1k (manifesto)
- 9088 Llama-1B: 8.0 KB/1k (manifesto)
- 9090 Llama-3B: 28.0 KB/1k (manifesto)
