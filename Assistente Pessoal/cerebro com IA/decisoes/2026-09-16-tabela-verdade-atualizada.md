# Tabela da Verdade ATUALIZADA — 2026-09-16 (pós-canonizações)

> Estado: 11 slots (10 UP + 1 WARM) · VRAM 14.12/17.16 (82.3%) · folga 3.04GB
> Fonte: crivo /7 (A cru + B quarteto), manifesto, logs llama-server, GGUF parser

## Stack canônica

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

## Mudanças desta sessão

1. **NeoHorse-1-4B-Q5_K_M CANONIZADO :9095** (substituiu Qwen1.5-MoE) — 5.1/7 com quarteto, ctx 262k, decode 102 GPU
2. **Noema-2B.Q4_K_S CANONIZADO :9098** como executor-cego — 3.0/7 (sweet spot do sweep Q2→Q5), 1.21GB
3. **Qwen1.5-MoE-A2.7B DESCONTINUADO** (lixeira) — NeoHorse vence 8/10
4. **Embedders unificados** — :9097 GPU → WARM (toggle), :9094 CPU canônico
5. **9093 SmolLM2-360M → CPU** (liberou VRAM)
6. **Ornith-1.5-9B-Q8 DESCONTINUADO** (1.92 t/s CPU, miserável)
7. **Qwen3.8-27B-GSQ-RCO-IQ2_XS** em filtragem (não testado)

## Candidatos em filtragem

| Modelo | Status |
|---|---|
| Noema-2B-Q8_0 | ❌ superado pelo Q4_K_S (2.01GB vs 1.21GB, 1.7 vs 3.0) |
| Qwen3.8-27B-GSQ-RCO-IQ2_XS | ⏳ não testado |

## Próximas pendências
- [ ] Testar Qwen3.8-27B-GSQ-RCO-IQ2_XS (filtragem)
- [ ] Descrever função real de cada papel no grafo (auditoria de otimizações)
- [ ] Decidir se NeoHorse-4B assume também proposer (9088) — 5.1 vs 4.0

**Errata 2026-09-16 (pós-sessão, cf. manifesto `historico_ctx`):** 9095 NeoHorse
ctx 262144→**32768** (plano 8-32k; KV 2.1GB→0.25GB; relaunch `-c 32768`, health+smoke ok).
Linha 9095 da tabela acima vale com ctx 32k.

## Resolução autônoma 2026-09-16 (todas as pendências concluídas)
- [x] Qwen3.8-27B-GSQ-RCO-IQ2_XS: **DESCARTADO** — GGUF ausente local; oficial 8.42GB
  (ISTA-DASLab, IQ2_XS) >> folga VRAM 3GB; exigiria offload majoritário CPU, fora do
  perfil filtragem. Sem download. Reabrir só com folga ≥10GB.
- [x] NeoHorse-4B no proposer (9088): **DECIDIDO manter 9088** (Llama-1B 4.0).
  Critério: proposer exige ctx longo (R84-EXEC01, 131k); NeoHorse em 32k não qualifica.
  Revisão automática se NeoHorse voltar a ≥131k OU placar ≥6.0 com ctx longo.
- [x] Papéis no grafo: documentado em `decisoes/2026-09-16-papeis-no-grafo.md`.
