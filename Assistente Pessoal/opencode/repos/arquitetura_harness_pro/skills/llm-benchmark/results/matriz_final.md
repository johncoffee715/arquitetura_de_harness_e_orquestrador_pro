# Matriz SPEC — Benchmark Gran-Mestre (2026-08-19, 4 modelos)

| Modelo | ctx | MTP | KV | VRAM load | T1 prefill | T1 inv | T2 JSON | T3 vol |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ornith-1.0-9B Q4_K_M | 32768 | N/A (sem head) | q4_0/q4_0 | 10.1GB | 13608 tok / 25.0s | PASSOU | FALHOU | nota 10 |
| Qwen3.8-9B Q4_K_M | 32768 | 3 (aceite 100%) | q4_0/q4_0 | 10.6GB | 13608 tok / 26.1s | PASSOU | FALHOU | nota 10 |
| Qwen3.8-27B Ridge-3.7bpw | 16384 | 3 (aceite 100%) | q4_0/q4_0 | 16.8GB | 13608 tok / 104.4s | PASSOU | PASSOU | nota 0 |
| Qwen3-Coder-30B-A3B Q3_K_M (MoE 3B ativo) | 8192 | N/A (sem head) | q4_0/q4_0 | 16.7GB | 5788 tok / 14.9s | PASSOU | PASSOU | nota 30 |

## Ranking de impressão (R34/R37)
1. **Qwen3-Coder-30B-A3B** — T1✅ T2✅ T3 nota 30 (condição de corrida — gabarito próximo); MoE 3B ativo; VRAM 16,7 GB (no limite, funciona com KV q4_0 + np 1 + ctx 8K).
2. **Qwen3.8-27B Ridge** — T1✅ T2✅ T3 nota 0; VRAM 16,8 GB (limite, risco OOM — travou 2x).
3. **ornith-1.0-9B** — T1✅ T2❌ T3 nota 10; VRAM 10,1 GB (folga 7 GB).
4. **Qwen3.8-9B** — T1✅ T2❌ T3 nota 10; VRAM 10,6 GB (folga 6,6 GB).

## Observações
- **T3 (gabarito volatile)**: ninguém acertou o gabarito estrito (leituras consecutivas podem divergir). Coder-30B chegou mais perto (condição de corrida entre leituras). **Gabarito a calibrar**: aceitar "condição de corrida/atomicidade/stale-read" como variações defensáveis (nota ≥60).
- **T2 (JSON puro)**: só 27B e Coder-30B passaram; ornith/9B emolduram em ```json.
- **T1**: todos passaram a invariante. Coder-30B truncado p/ ctx 8K (5788 tok); demais com fixture completo (13608 tok).
- **Veredito por SPEC**: Coder-30B-A3B é o **melhor custo-benefício** — único que passa T1+T2 e chega perto do T3, com MoE leve; VRAM no limite mas estável (sem travamento). 27B cumpre T1/T2 mas arriscado (OOM 2x observado).

## Recomendações
- **KV quantizado obrigatório** p/ modelos ≥14 GB: q4_0/q4_0 + np 1. Para 9B/ornith, q8_0/q4_0 é seguro.
- **MTP**: só Qwen3.8-9B/27B têm head (aceite 100%, mean len 4.0). Coder-30B/ornith: sem head.
- **Próximo passo**: considerar Coder-30B-A3B como executor de código do harness (nível 2) — testar com tasks reais (TDD/code-review); calibrar gabarito T3; testar ctx 16K do Coder-30B se folga permitir.