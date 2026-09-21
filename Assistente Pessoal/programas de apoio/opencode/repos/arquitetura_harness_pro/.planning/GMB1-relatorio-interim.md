# GMB-1 — RELATÓRIO INTERIM DE BENCHMARK (2026-08-23)

**Escopo:** Tríade TIER A smoke (5 testes) — GPU MI50 isolada, porta única :8083, ctx 32768 idêntico, KV q8_0/q4_0, -ngl 99, -t 18, 1 LLM GPU por vez (isolamento §2 GMB-1).
**Status:** INTERIM — cobre ~35% da matriz 100pts (categorias C-tool básico e G-verificação via A4/A5). Matriz completa (B-G) pendente.

---

## 1. Resultados Smoke (evidência fresca)

| Teste | Ornith-1.5-9B Q4 | Qwen3.8-9B-Distill Q4 | Qwen3.8-27B UD-IQ2_XXS |
|---|---|---|---|
| A1 Pelican SVG | ❌ FAIL (`raw=""`, 3ª ocorrência) 28.24 t/s / 36.3s | ❌ FAIL 66.37 t/s / 15.4s | ❌ FAIL 20.91 t/s / 49.0s |
| A2 Strawberry | ✅ 28.81 t/s | ✅ 65.84 t/s | ✅ 20.52 t/s |
| A3 JSON Extract | ✅ 26.25 t/s | ✅ 53.90 t/s | ✅ 17.50 t/s |
| A4 Tool Call | ✅ 21.28 t/s (`<tool_call>` válido) | ✅ 41.98 t/s | ✅ 16.61 t/s |
| A5 Halluc Guard | ✅ 28.68 t/s (`admits_no_access`) | ❌ **FAIL CRÍTICO** 63.86 t/s | ✅ 19.38 t/s |
| **TOTAL** | **4/5** | **3/5** | **4/5** |

Artefatos: `skills/llm-benchmark/results/smoke-{ornith-1.5-9b,qwen38-9b,qwen38-27b-iq2xxs}-gmb1.{json,md}`

## 2. Recursos e Throughput

| Métrica | Ornith 9B | Qwen 9B | Qwen 27B XXS |
|---|---|---|---|
| t/s médio smoke (GPU) | ~26 | ~58 | ~19 |
| VRAM @32K (GiB) | 14.18 | 14.92 | **15.70 (>95%)** ⚠️ |
| Warning fit | nenhum | nenhum | `W common_fit_params: failed to fit params` |
| CPU decode 8K t/s | n/m | 3.06 (:18083) | 1.63 (:18084) |
| Estabilidade | A1 falha estável 3/3 runs | A5 halluc falha 2/2 runs (antigo `alpha_vantage` + atual) | único run |

## 3. Achados Críticos

1. **Qwen9B — critical_failure recorrente (GMB-1 §9):** alucinação em A5 em 2/2 runs independentes → fabricação de dados quando não sabe. REJEITADO para slot primário autônomo.
2. **Qwen27B XXS — resource_fit insuficiente:** 98% VRAM + warning de fit → risco OOM em produção; CPU fallback 1.63 t/s inviável para swarm; quantização IQ2_XXS degrada A1 também.
3. **Ornith — gap criativo não-crítico:** A1 SVG falha determinística (raw vazio) em 3/3 runs — limitação de geração de código criativo, sem impacto em tool-call/verificação.
4. **Ambiente:** `drop_caches` requer sudo (R55 parcial); chat template Ornith/Qwen suporta `--reasoning-preserve` (não habilitado nos smokes — manter idêntico nas próximas runs).

## 4. Decisão Provisória (critérios §promoção)

| Candidato | Veredito | Justificativa |
|---|---|---|
| **Ornith-1.5-9B-Q4_K_M** | **PROMOTE_GPU (provisório)** | Único sem critical failure; VRAM saudável c/ folga; tool-call e halluc-guard sólidos; velocidade adequada (~26 t/s) |
| Qwen3.8-9B-Q4 | REJECT slot primário / usar como FAST_WORKER supervisionado | Velocidade elite (~58 t/s) mas critical recorrente exige verificador externo obrigatório |
| Qwen3.8-27B-IQ2_XXS | KEEP_FALLBACK marginal / candidato a remoção | Qualidade ok em 4/5 mas VRAM no limite + 3x mais lento + CPU inútil |

**GM-SCORE oficial:** NÃO EMITIDO — exige matriz completa (D Exec 20 tasks, E Recovery injection, F LongCtx needle 8K-256K, B Decomp multi-agente). Gate G4 permanece ABERTO até então.

## 5. Próximos Passos
1. T4.1-T4.5: implementar discovery/registry/router/graph_engine com TDD (harness/models/, harness/core/)
2. Matriz GMB-1 completa B-G para GM-SCORE oficial ≥80
3. T4.8 helenização dos gaps do arsenal
4. F5 (Atena + fable-judge sobre este relatório) → G4 → F6 (rank final + memória)

---
*Gerado pelo Gran-Mestre em 2026-08-23 — evidência: logs `/tmp/{qwen27b-gpu-gmb1,ornith-restore}.log`, resultados JSON/MD acima.*
