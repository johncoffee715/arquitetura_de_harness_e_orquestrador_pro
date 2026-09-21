---
data: 2026-09-15
tipo: tabela-da-verdade (pós-migração R102 + sonda t/s uniforme)
sucede: 2026-09-15-tabela-verdade-maxima.md
---

# Tabela da Verdade — Pós-Migração R102 (2026-09-15 ~19:00)

> Sonda uniforme: mesmo prompt PT, temp 0, max_tokens 64, sequencial. Condição: stack warm +
> 27B ativo na CPU (CPU ports degradam vs idle). Backend canônico agora vive em
> `programas de apoio/opencode/` (R102). sync-llm-stack.py --check = sincronizado.

## Stack canônica (10 slots) + candidato

| Slot | Modelo | Papel | Crivo /7 (c/ quarteto) | Crivo s/ quarteto | Dec CPU | Dec GPU | Pre CPU | Pre GPU | KV KB/1k | ctx serv | GB | Disp. | Veredito |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8083 | Qwen3.5-35B-A3B UD-IQ3_XXS | orquestrador | 3.3 | — | 11.9* | (ngl36) | 4.6* | — | 5.76 | 262k | 12.29 | GPU parcial+CPU | KEEP (intocável R39/R39) |
| 9084 | RWKV7-0.4B-FP16 | córtex | n/a (mecânico) | n/a | — | 14.6* | — | 47.0 | 0.0 | 1M | 0.91 | GPU | KEEP (intocável) |
| 9086 | LFM2.5-1.2B-ToMoE-Q4_K_M | reflexo | n/a | — | 24.2 | — | 9.5 | — | 3.8 | 128k | 1.0 | CPU | KEEP |
| 9088 | Llama-3.2-1B-IQ4_XS | proposer | 4.0 | — | — | 142.3 | — | 165.8 | 8.0 | 131k | 0.9 | GPU | KEEP |
| 9090 | Llama-3.2-3B-UD-IQ3_XXS | refuter | 3.5 | — | 10.1* | — | 7.4* | — | 28.0 | 32k | 2.0 | CPU | KEEP |
| 9092 | SmolLM2-1.7B-Q4_K_M | relay/juiz | 3.5 | — | 16.5* | — | 10.9* | — | 0.0 | 32k | 1.1 | CPU | KEEP |
| 9093 | SmolLM2-360M-Q8_0 | descoberta | 2.0 | — | — | 255.4 | — | 286.6 | 2.5 | 4k | 0.4 | GPU | KEEP |
| 9094 | Qwen3-Emb-0.6B | embedder | — | — | 14702† | — | — | — | 14.0 | 2k | 0.6 | CPU | CANÔNICO CPU |
| 9095 | NeoHorse-1-4B-Q5_K_M | warm/executor | **4.0 (T2 recusa poison)** | cede T2 | 4.82 | **6.0** ⚠️ | 24-42 | 51.9 | 8.0 | 262k | 3.07 | GPU | KEEP (ver nota VRAM) |
| 9097 | Qwen3-Emb-0.6B-GPU | embedder | — | — | — | 90982† | — | — | 14.0 | 2k | 0.6 | GPU | sob-demanda (R5) |
| **8090** | **Qwen3.8-27B-GSQ-RCO-IQ2_XS** | **candidato crivo** | **pendente** | — | **1.7*** | — | **0.7*** | — | ? | 65k | 7.9 | **CPU (VRAM cheia)** | **CRIVO PENDENTE** |

\* medido sob contenção (stack cheia + 27B co-residente); valores canônicos idle-CPU: 8083=26.5, 9090=12.2, 9092=17.3, 9086=26.7
† batch b32 (embedder)

## Fatos novos desta sessão

1. **Migração R102 efetivada**: `/mnt/dados/Assistente Pessoal/opencode/` → `programas de apoio/opencode/` (rename atômico, refs sed, guard-engine 29/29 TDD, health 10/10 + 3 needles).
2. **NeoHorse-4B já é o 9095 de fato** (GPU ngl999 ctx 262k) — decode medido 6.0 t/s vs 102 canônico: **GPU saturada/contendida com 8083** (VRAM 16.0/17.2GB). Atenção: ctx 262k sobe KV — canônico planejava ctx 8k/32k.
3. **VRAM real agora**: 16.05/17.16GB — livre ~1.1GB (era 4.39 no inventário das 18:55; Δ = NeoHorse 262k + overhead).
4. **27B IQ2_XS em CPU**: 1.7 t/s decode sob contenção — viável p/ crivo, lento p/ chat. GPU-only exigiria liberar ~8-9GB (só viável movendo 8083 p/ CPU ou removendo 9095+9088+9097+9093).
5. Prefill do 27B: 0.7 t/s → prompts longos no crivo serão o gargalo (bateria 6 métricas ≈ horas em CPU).

## Remoções de VRAM — candidatos (8083 e 9084 FORA de cogitação)

| Slot | Libera | Custo funcional |
|---|---|---|
| 9097 embed GPU | ~0.7GB | nulo (9094 CPU cobre) |
| 9093 360M | ~0.4GB | triagem degrada |
| 9088 1B | ~1.7GB | proposer p/ CPU (~0.9GB KV+pesos) |
| 9095 NeoHorse | ~3.3-5GB | executor GPU morre (volta CPU 4.8 t/s) |

Máximo recuperável sem tocar 8083/9084: **~6-7.5GB** → ainda insuficiente p/ 27B-GPU (7.9G pesos + KV). Conclusão: **27B GPU exige 8083 em CPU** (fora por ora) ou stack reduzida.
