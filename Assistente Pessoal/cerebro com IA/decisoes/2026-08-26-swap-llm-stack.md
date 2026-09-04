---
tags: [decisao, llm-stack, r52, r54, granite, lfm, swap]
data: 2026-08-26
---

# Decisão — Swap LLM Stack CPU 2026-08-26

## Contexto
Auditoria do inventário CPU (R52) + avaliação de 4 candidatos para 9086/9087. Stack anterior: 9086 LFM230M 3.8 KB/tok 205 t/s, 9087 Qwen3.8-9B 6.2GB UNKNOWN 0.4 t/s.

## Decisões
1. **9086 LFM2.5-1.2B-Thinking-ToMoE Q4_K_M fica** — 730MB, 3.8 KB/tok, 30.5 pico/10.3 carga, IFEval 88.42, GPQA 37.86, BFCLv3 56.97. PT não-oficial (8 línguas sem PT) → usar EN para GBNF. Thinking tax 1-4.8k exige max_tokens ≥512.
2. **9087 Qwen3.8-9B → Granite 4.2-3B Q4_K_M** — 2.24GB, 25.0 KB/tok, 131K nativo (RULER 67/55), BFCL 52.41, AIME 78.33, 12 línguas com PT, thinking 3 modos (full/low/non). 8× mais rápido que 9B, bench CONFIRMED.
3. **Rejeitados:** G9v3-3B (en/zh, UNKNOWN), Ling-3.0-tiny (7.9B/1.3B MoE real, 4.82GB, RAM bloqueante).
4. **R54** — Preservação da janela: Gran-Mestre delega, subagents devolvem só supra-sumo (≤25 linhas).

## Artefatos
- `scripts/start-stack.sh` (9086 -c 32768 temp 0.05, 9087 -c 32768 temp 1.0)
- `scripts/ctx-cost.py` (STACK_CPU + granite arch)
- `harness/llm-inventory.json` (9 models, empirical 30.5/3.25)
- `config/opencode/AGENTS.md` (R54, RS7 25.0, §13 granite)
- `config/opencode/opencode.jsonc` (local-executor granite)
- Backups: `/tmp/opencode/swap9086-bak/`, `/tmp/*.bak-20260826-9087`

## Pendências
- [ ] manifesto_llm.json v1.1 STALE → sync pós-Granite
- [ ] Qwen3.8-9B inode 3865081 mmap'd por :8083 (PID 338219) → restart :8083 libera 6.2GB Trash
- [ ] 8083 Ornith 212992 q4_0 health ok (não bloqueia)

## Referências
- [[summaries/2026-08-26-swap-llm-stack]]
- [[aprendizados/2026-08-26_swap-llm-stack]]
- `harness/pipeline/CONTEXT.md`
