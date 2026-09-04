---
source: pipeline/CONTEXT.md — SWAP 9086 LFM230M→LFM1.2B + SWAP 9087 Qwen9B→Granite4.2-3B
date: 2026-08-26
type: summary
tags: [summary, llm-stack, r52, r54, granite, lfm, audit]
ingest_source: harness/pipeline/CONTEXT.md
---

# Swap LLM Stack CPU — 2026-08-26

## Takeaways
1. **9086 LFM1.2B-Thinking Q4_K_M fica** — 730MB, 3.8 KB/tok, 30.5 pico/10.3 carga, IFEval 88.42, PT não-oficial (8 línguas sem PT), thinking tax 1-4.8k.
2. **9087 Granite 4.2-3B Q4_K_M substituiu Qwen3.8-9B** — 2.24GB, 25.0 KB/tok, 3.25 t/s, RULER 67/55, BFCL 52.41, AIME 78.33, 12 línguas com PT, thinking desligável.
3. **Candidatos rejeitados:** G9v3-3B (en/zh só, 1.84GB, UNKNOWN), Ling-3.0-tiny (7.9B/1.3B MoE real, 4.82GB, en/zh, RAM bloqueante).
4. **R54 guardrail** — Gran-Mestre preserva janela delegando; subagents devolvem só supra-sumo (≤25 linhas).

## Stack final 8/8 ok (KV 11.99GB)
- 9083 qwen3.5-4b-iq2xxs 40.0 32768 prosa
- 9084 qwen3.5-0.8b 15.0 262144 descoberta
- 9085 llmjudge 11.2 32768 judge
- 9086 lfm1.2b 3.8 32768 reflexo R42
- 9087 granite 25.0 32768 executor F4
- 9088 qwen3.8-4b 41.2 40960 contrato
- 9089 qwen3.8-2b 15.6 32768 tool-leve
- 9090 ternary 45.0 65536 refutação

## Evidências
- BENCH-01: LFM 30.5 pico, prefill 402 tok/s, thinking 1000-4800c
- Probe 9087: 3.25 t/s, tool-calling Boston OK, thinking 15*37=555 OK
- Health 9/9 ok (8083 Ornith 212992 q4_0)

## Sinapses
- [[entities/granite-4.2-3b]] — novo executor
- [[entities/lfm2.5-1.2b-thinking]] — reflexo mantido
- [[concepts/llm-stack-cpu-r52]] — inventário R52
- [[decisoes/2026-08-26-swap-llm-stack]] — decisão
- [[aprendizados/2026-08-26_swap-llm-stack]] — aprendizado
