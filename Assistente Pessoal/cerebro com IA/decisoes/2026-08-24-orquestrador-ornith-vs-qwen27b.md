---
tipo: decisão
data: 2026-08-24
status: VIGENTE
---
# Orquestrador: Ornith permanece; Qwen3.8-27B entra como Planner Warm

## Decisão
Ornith-1.5-9B-Q4_K_M :8083 GPU **permanece** Gran-Mestre.
Qwen3.8-27B IQ2_XXS assume slot WARM de Fase 1/2/5 (planner profundo) via hot-swap GPU sob demanda (R58/R65).

## Dados que sustentam
| Métrica | Ornith 9B | Qwen3.8-27B IQ2_XXS |
|---|---|---|
| GM-oficial local (spec B/D-FULL) | **76.3** | 68.5 |
| GPQA Diamond | 86.4 (HF oficial) | 89.2 (community HN) |
| Terminal-Bench 2.1 | 46.2–58.3 | **73.0** (community) |
| DeepSWE | — | **42.2** (vs Ornith-35B community: 22.0!) |
| Prefill t/s local | **770** | ~150 |
| cache-reuse | nativo ok | **disabled em runtime** (medido) |

## Racional
Orquestrador = roteador de latência mínima + aderência JSON + harness-trained (self-scaffolding é a especialidade DO Ornith).
Planner = densidade cognitiva + janela ≥96K → papel natural do Qwen27B.
Vídeo Mitjana (ZqkljdI1HT0) prova força agêntica do 27B — consistente com papel de PLANNER, não de roteador.

## Condição de reversão
Re-run GMB do qwen27b com spec idêntico: se GM-local ≥ 76.3, reabrir decisão.

## Propagação (R27 — 5 pontos de verdade)
ctx-catalog.json ✓ · llama_budget.py ✓ · start-all-models.sh ✓ · manifesto_llm.json ✓ · oh-my-openagent.json (N/A sem ctx hardcoded)

## Experimento K=q4 anexo
K=q4_0+V=q4_0 @262144 REPROVADO (prefill 81 t/s, decode 1.7 t/s). Estado fixado: -c 163840 K=q8_0 V=q4_0.
