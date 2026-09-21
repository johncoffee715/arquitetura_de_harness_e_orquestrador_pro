# Benchmarks — Régua Própria (oferta/demanda)

> **Não é o que funciona pra todos. É o que funciona pra nós.** Nossa MI50 16GB + Xeon E5-2699v3 (36 threads), nossas métricas medidas, nossa oferta (VRAM/CPU/disco) vs nossa demanda (feature/papel). Métrica sem nota aqui = volátil.

## Como usar
1. Bench empírico → criar `YYYY-MM-DD-<slug>.md` com template.
2. Atualizar esta tabela.
3. Referenciar no `decisoes/` e, se afetar roteamento, em `manifesto_llm.json` (R78).

## Mapa vivo

| Data | Modelo | Quant | Slot | `c`/`b`/`ub`/`ngl`/`pooling` | `t/s` (batch) | Lat p50 | KV KB/tok → KB/1k | VRAM Δ | RAM | Dim | Oferta/demanda | Veredito |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-11 | Qwen3-Embedding-0.6B | Q8_0 610M | :9094 CPU | 2048/256/256/0/last q4/q4 | 14 702 (b32) | 0.52s (b1) | 14 → 14 336 | 0 | 809M | 1024 | Bibliotecário: PT multilíngue 32k, Apache-2.0, leve | **CANÔNICO CPU (query b=1, economia VRAM)** |
| 2026-09-11 | Qwen3-Embedding-0.6B | Q8_0 610M | :9097 GPU Vulkan | 2048/256/256/99/last q4/q4 | 90 982 (b32) | 0.12s (b1) | 14 → 14 336 | +1 047M | 326M | 1024 | burst 6×, lote 16/32 paga Vulkan 1× → 90k | **CANÔNICO GPU (lote/indexação)** |
| 2026-09-10 | Llama-3.2-1B-Instruct (provisório embed) | IQ4_XS ~0.9G | :9094 CPU | 2048/512/256/0/mean q4/q4 | ~14k* (b16) | 0.56s (b16) | ~14 → 14 336 | 0 | ~800M | 2048 | provisório, sem treino retrieval | **HISTÓRICO** |
| 2026-09-10 | Carrossel Fundo | CSS | — | contain vs cover | — | — | — | 0 | 0 | — | contain = sem distorção (letterbox `--background-primary`) | **v1.3 CANÔNICO** |
| 2026-09-15 | **Stack A/B R103 completa** — 27B-GSQ-RCO-IQ2_XS: A 2.5 → B 6.2 (Δ+3.7, empata 8083 em B) | IQ2_XS 7.9G | :8090 CPU | 65536/2048/1024/0 | dec 1.7 | — | n/d | 0 | ~9G | — | quartetos valem +2.6~3.7 em 4B+, custam em micros; ver `2026-09-15-crivo-AB-consolidado-27b.md` | **filtragem: aguarda slot GPU** |
| 2026-09-16 | **Criva piso R104** — 6 candidatos; Q1 refutado 2×; piso-absorção = **~2.3bpw** | IQ1_S/IQ1_M/IQ2_S | :8090 | vários | dec 1.7-7.9 | — | n/d | 0 | — | — | "funcionar cru" ≠ "absorver quartetos"; detalhe em `2026-09-16-criva-massiva-piso-quantizacao.md` | **nenhum canoniza** |
| 2026-09-20 | **Crivo A/B REAL 13 modelos** (parsing corrigido + fork PrismML) — top: Llama-3.2-3B Δ+0.57 (B=0.86), Ternary-Bonsai CPU B=0.86 (Δ+0.07, 27B/5.5GB), Llama-3.2-1B Δ+0.50, SmolLM2-360M Δ+0.43; pior: Noema-2B Δ-0.50, Qwen3.5-0.8B Δ-0.43; Ternary-Bonsai FUNCIONAL via fork PrismML (GPU 3.3t/s, CPU 0.45t/s) | vários | vários | vários | — | — | n/d | 0 | — | — | quartetos valem +0.4~0.6 em 1-3B; Ternary-Bonsai super-habilitado (B=0.86 sem depender de quartetos); fork PrismML obrigatório para tensor type 143; ver `bibliotecario-crivo-AB-2026-09-20.md` | **Llama-3.2-3B melhor Δ; Ternary-Bonsai FUNCIONAL (Cluster S)** |

\* Llama provisório: 384 reais + 247 placebos em 2m57s (batch 32) → throughput efetivo similar mas qualidade não crivada.

## Notas
- `2026-09-11-qwen3-embedding-0.6b-cpu-vs-gpu.md` — détail CPU vs GPU (mesmo GGUF, 1.65s/2 txt, norma 1.0)
- `2026-09-10-llama-1b-provisorio.md` — bench de transição (placebo até Qwen3)
- `2026-09-10-carrossel-v1.3.md` — bench visual de enquadramento

## Template
Ver `template.md`.
