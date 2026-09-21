# Papéis no grafo — função real por slot (2026-09-16)

> Síntese da pendência "descrever função real de cada papel no grafo".
> Fonte: `modelos LLM/manifesto_llm.json` (`vocacao_grafo` por slot) + `2026-09-16-tabela-verdade-atualizada.md`.
> Nada inventado: função = declarada no manifesto; placar = medido no crivo /7.

| Porta | Modelo | Papel no grafo | Função real |
|---|---|---|---|
| 8083 | Qwen3.5-35B MoE (CPU+36ngl) | ORQUESTRADOR | Roteia/delega; 3.3/7; KV 5.76KB/1k @262k |
| 9084 | RWKV7-0.4B (GPU) | CÓRTEX L0.5 | Triagem semântica F0 (intent), 1M ctx, 143 t/s; E2E SNN vivo |
| 9086 | LFM2.5-1.2B ToMoE (CPU) | REFLEXO | Tool-calling preciso ultra-veloz, GBNF-conforme |
| 9088 | Llama-3.2-1B (GPU) | PROPOSER | Executor contexto-longo (ctx 131k, critério R84-EXEC01); 4.0/7 |
| 9090 | Llama-3.2-3B (CPU) | REFUTADOR | Refutação pesada A2A, extração GBNF 10/10 |
| 9092 | SmolLM2-1.7B (CPU) | RELAY | Refutador ágil / intermediário |
| 9093 | SmolLM2-360M (CPU) | DESCOBERTA | Micro 400 t/s, supervisão restrita (regressão C sob observação) |
| 9095 | NeoHorse-1-4B Q5 (GPU) | EXECUTOR F4 | Motor de features, tool-calling GBNF, TDD; 5.1/7; ctx 32k (2026-09-16) |
| 9098 | Noema-2B Q4 (CPU) | EXECUTOR-CEGO | Obediência estrita, forja, extração JSON; 3.0/7 |
| 9094 | Qwen3-Emb-0.6B (CPU) | EMBEDDER | Query tempo-real bibliotecário (1024-d) |
| 9097 | Qwen3-Emb-0.6B (GPU) | EMBEDDER-WARM | Lote sob demanda (toggle) |

## Auditoria de otimizações (lacunas honestas)

- 9093: placar C caiu 2.0→1.0 — sem promoção; coder só supervisionado+grammar.
- Teto do stack: 5.1 (9095). Nenhum modelo ≥ 6.0 (GM).
- Proposer (9088) exige ctx longo; NeoHorse em 32k NÃO qualifica hoje (ver recomendação na resposta de fechamento).

exit_status: ok
