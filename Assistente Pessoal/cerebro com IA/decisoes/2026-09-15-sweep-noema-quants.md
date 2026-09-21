# Sweep de Quantizações — Noema-2B (Q2→Q5) — 2026-09-15

> Objetivo: encontrar a menor quantização viável do Noema-2B-Q8_0 para o papel executor-cego,
> respeitando as limitações de hardware (VRAM 17.16GB, folga ~3GB).
> Método: crivo A (cru — estado ótimo do executor-cego) em CPU, mesma régua p/ todos.

## Resultados

| Quant | Peso | Placar /7 | Decode t/s | Prefill t/s | Eficiência (placar/GB) | Veredito |
|---|---|---|---|---|---|---|
| Q2_K | 0.97GB | 0.4 | 14.6 | 86.1 | 0.41 | ❌ degradação severa (loops ###, **, {) |
| Q3_K_S | 1.02GB | 1.2 | 14.2 | 76.3 | 1.18 | ❌ thinking-burn, T6 parcial |
| Q3_K_M | 1.10GB | 2.4 | 14.7 | 70.2 | 2.18 | ⚠️ T11 EXATO, T4 ground pass |
| **Q4_K_S** | **1.21GB** | **3.0** | **13.7** | **82.2** | **2.48** | ✅ **MELHOR CUSTO-BENEFÍCIO** |
| Q4_K_M | 1.27GB | 2.4 | 12.9 | 83.2 | 1.89 | ⚠️ T6+T11 EXATO |
| Q5_K_S | 1.37GB | 2.4 | 12.0 | 63.7 | 1.75 | ⚠️ T6+T11 EXATO |
| Q5_K_M | 1.41GB | 2.4 | 10.9 | 50.6 | 1.70 | ⚠️ T6+T11 EXATO |
| Q8_0 (atual) | 2.01GB | 1.7 | 8.0 | 52-76 | 0.85 | ❌ pesado demais p/ GPU |

## Análise

1. **Q4_K_S é o sweet spot**: 1.21GB (40% menor que Q8_0), placar 3.0/7 (melhor do sweep), T6+T11 EXATOS
2. **Q2/Q3_S degradam** — quantização agressiva demais para o modelo 2B
3. **Q5+ não melhoram** — placar estagna em 2.4, só aumenta peso
4. **Q8_0 (atual) é o PIOR custo-benefício**: 2.01GB para 1.7/7 — pesado e não melhor

## Recomendação

**Canonizar Noema-2B.Q4_K_S (1.21GB) como executor-cego em CPU :9098**
- Peso 1.21GB → cabe na folga VRAM (3GB) se necessário GPU
- Placar 3.0/7 (melhor do sweep)
- T6+T11 EXATOS (obediência estrita preservada)
- CPU decode 13.7 t/s (mais rápido que Q8_0 8.0 t/s!)
- KV 3 KB/1k (minúsculo) → ctx 262k viável

## Ações
- [ ] Mover Noema-2B.Q4_K_S para path principal
- [ ] Canonizar como executor-cego (papel distinto do proposer)
- [ ] Registrar no manifesto + sync
- [ ] Descartar Q2_K, Q3_K_S, Q3_K_M, Q4_K_M, Q5_K_S, Q5_K_M (não melhoram)
