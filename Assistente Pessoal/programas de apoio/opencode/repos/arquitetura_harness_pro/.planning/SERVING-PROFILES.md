# PERFIS DE SERVING — parametrizados por benchmark (sessão 2026-08-23/24)

## GPU :8083 — ORQUESTRADOR (Ornith-1.5-9B-Q4_K_M)
KV: **K q8_0 / V q4_0** (empírico: K=q4 regride prefill 770→82 t/s) · Temp: **0.6** top_k20 top_p0.95 (oficial agentic unsloth) ·
Think: **preservado** (reasoning-preserve + budget 1024) · Janela: **NATIVO 262144** — GGUF exportado em 131072 causava loop de compactação com perda; produção em 262K via yarn×2.0 validado (Adenda 12 · prefill 594 t/s @98% VRAM) · Prefill: b512 (b8192 regride)

## CPU — perfis por responsabilidade
| Porta | Modelo | Papel | Temp | KV atual | Medição |
|---|---|---|---|---|---|
| :9083 | Bonsai-27B-1bit | F1 criativo pesado +GBNF | 0.8 | global | 15.72 t/s |
| :9084 | Qwen3.5-0.8b | exploração alt | 1.0 | global | 123 t/s |
| :9085 | LLMJudge-3b | judge A2A | **0.15** | global | 139 t/s |
| :9086 | LFM2.5-230m | refutação rápida | 0.4 | global | 228 t/s 🏆 |
| :9087 | Qwen38-2b | code/tool | **0.3** --jinja | global | 155 t/s warm |
| :9088 | Qwen3-1.7B | curto | 0.6 | global | 182.88 pós-cura |
| 🆕:9089 | Ternary-Bonsai-1.7B | curtas/exploração ⚡ | 0.6 | global | 137-207 t/s |
| 🆕:9090 | Ternary-Bonsai-8B | Refutação A2A intermediária | **0.4** --jinja | global | 44.5 ctx4k |

## LEIS DOS PERFIS (refutáveis)
1. K=q4_0 na MI50/HIP regride prefill ~15× — só V fica em q4 no GPU slot
2. Endless-think generativo ⇒ `--chat-template-kwargs '{"enable_thinking": false}'` (lei #7)
3. Judge/reviewer ⇒ temp ≤0.15; criativo ⇒ ≥0.8; code/tool ⇒ ≤0.3
4. Warm-cache ordena verdade: comparativos entre variantes exigem aquecimento obrigatório
5. Spec-decode: build EXPOE flags (--spec-draft-type-k/-ctkd visíveis) mas sem draft-model compatível por família o custo líquido em slots CPU tende negativo — acompanhar MTP nativo upstream p/ Qwen3.8/Ornith antes de ativar

## PENDENTE p/ próxima iteração (A/B com dados)
- [ ] KV q4/q4 nos slots CPU (largura de banda favorece — medir antes de aplicar)
- [ ] spec-decode c/ draft model nos slots code/tool se build ganhar suporte
