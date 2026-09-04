---
tags: [aprendizado, llm-stack, r52, r46, r54, benchmark, granite, lfm]
date: 2026-08-26
area: ai/llm-stack/auditoria
---

# Aprendizado: Swap LLM Stack CPU — 2026-08-26

## Contexto
Auditoria R52 do inventário CPU (8 slots) + dissecação R46 de 4 candidatos (Nichonauta ToMoE, G9v3-3B, Ling-3.0-tiny, Granite 4.2-3B) para 9086/9087.

## O que Funcionou
- **R52 inventário como fonte única** — `llm-inventory.json` + `ctx-cost.py --all` + `start-stack.sh` alinhados; health 9/9 validado.
- **Dissecação R46 antes de baixar** — GGUF ToMoE dense-equivalent (sem MoE nativo llama.cpp), G9 en/zh UNKNOWN, Ling 7.9B/1.3B MoE real mas 4.82GB RAM bloqueante, Granite 12 línguas com PT + RULER provado.
- **BENCH-01 real** — LFM 30.5 pico/10.3 carga, prefill 402 tok/s, thinking 1-4.8k tax; Granite 3.25 t/s, tool-calling OK.
- **R54 supra-sumo** — subagents ≤25 linhas, janela do orquestrador preservada.

## O que Não Funcionou
- **PT ausente em LFM/G9/Ling** — harness 100% pt-BR; LFM 8 línguas sem PT → JSON fenced em PT. Granite único com PT.
- **Thinking tax** — LFM max_tokens 150 → content vazio; exige ≥512. Granite resolve com enable_thinking=False.
- **Qwen3.8-9B UNKNOWN** — 6.2GB, 0.4 t/s, sem bench; Granite CONFIRMED vence.

## Padrões
- KB/tok decide -c (RS7): LFM 3.8 vs Granite 25.0 vs Qwen 41.2
- MoE real (Ling) ≠ mais rápido em CPU (routing overhead)
- Dense-equivalent GGUF ≠ MoE (ToMoE só safetensors/vLLM)
- PT nativo é critério bloqueante para GBNF/refutação

## Próximas Investigações
- Sync manifesto_llm.json v1.1 (STALE)
- Restart :8083 para liberar Qwen inode 6.2GB
- Re-medir t/s com stack enxuta (load 7.7 → 30→10)

## Sinapses
- [[decisoes/2026-08-26-swap-llm-stack]]
- [[summaries/2026-08-26-swap-llm-stack]]
- [[concepts/llm-stack-cpu-r52]]
- [[entities/granite-4.2-3b]]
