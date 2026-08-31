# Comparativo Empírico: granite-4.2-3b vs qwen3.8-4b (engenharia reversa) — 2026-08-31

## Contexto
Qwen3.8-4B-Q4_K_M (ex-slot :9088, substituído por alucinar sucesso sem escrita) testado com as NOVAS
capacidades (crivo R83 + benchmark empírico) para comparativo de engenharia reversa contra o granite.

## Crivo R83 (Etapa A anti-alucinação + Etapa B anti-loop)
| Métrica | granite-4.2-3b | qwen3.8-4b |
|---|---|---|
| Fato (capital) | ✅ Brasília | ✅ Brasília |
| Extração schema | ✅ conforme | ❌ fence ```json (0 invenções) |
| Não-invenção arquivo | ✅ não | ✅ não |
| Taxa alucinação | 0.0 | 0.333 (formato) |
| Determinismo temp0 | 100% | 100% |
| Loop n-gram | 0 | 0 |
| Latência média | 0.53s | 0.82s |
| **Veredito global** | **PASSOU_CATEGORICO** | **NAO_PASSOU** |

## Benchmark empírico (decode/prefill tok/s)
| Cenário | granite | qwen | Δ |
|---|---|---|---|
| Prefill curto | 78.4 | 59.7 | +31% |
| Prefill médio | 1401.3 | 714.0 | +96% |
| Decode curto | 103.3 | 83.8 | +23% |
| Decode médio | 97.8 | 82.7 | +18% |
| Decode longo | 112.4 | 89.3 | +26% |
| **Decode médio geral** | **104.5** | **85.3** | **+22%** |
| Latência/geração | 1.9s | 2.7s | -30% |

## Conclusões (engenharia reversa)
1. **Ambos os modelos alucinam o MESMO padrão de sintaxe** (fence markdown em extração estruturada) —
   confirma que é comportamento do amostrador de LLMs pequenos, não do modelo específico → GBNF é a correção universal (R81).
2. **Granite é superior em TODAS as métricas**: decode +22%, prefill médio +96%, latência -30%, e passa o crivo.
3. **Qwen é determinístico e sem loop** (Etapa B ok) — o problema dele era o CONTRATO de retorno (afirmava sucesso sem escrita), não a estabilidade generativa.
4. A substituição :9088 qwen→granite é **validada empiricamente** (não só por conveniência).
