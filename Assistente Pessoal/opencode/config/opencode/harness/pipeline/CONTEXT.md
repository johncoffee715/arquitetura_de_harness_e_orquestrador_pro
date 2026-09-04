# PIPELINE CONTEXT — SWAP 9087 Qwen3.8-9B → Granite-4.2-3B Q4_K_M (concluído) + base 9086 LFM

> Camada de estado do Gran-Mestre. Working: plano, SHA, RunIDs two-phase, budget, snapshot do harness.

## Objetivo
1. **SWAP 9087 (2026-08-26, concluído):** `Qwen3.8-9B-Q5_K_M.gguf` (6.2GB, UNKNOWN, 0.4 t/s, RAM-gated 16k) → `granite-4.2-3b-Q4_K_M.gguf` (2.24GB, CONFIRMED, 3.25 t/s, 25.0 KB/tok, 131K nativo) no slot CPU :9087 (executor F4 / contexto-longo).
2. **SWAP 9086 (base):** LFM2.5-230M → LFM2.5-1.2B-Thinking-ToMoE Q4_K_M (reflexo R42) — em produção.

- [Safety] SHA snapshot (2026-08-26, pré-9087):
  - start-stack.sh        79f7b6b95b5b8caf20b7faf272741d48fa4682f0db8045923c2191bf0c063008 → patched 9087 granite -c 32768 temp 1.0 top_p 0.95
  - ctx-cost.py           f16d7077f8b58dd2805cd831cc02f62fd5a1b9024dc1b69b5885468f44e90904 → patched STACK_CPU + granite arch
  - llm-inventory.json    f3707cf292451efc2670a3672647c0f6f6471319a36233e2df03170d41cbed6f → granite-4.2-3b-q4_k_m CONFIRMED
  - AGENTS.md             84ea8dcca989b10094097f0293cef9a59fb55a488c88d79b0bda3be219d0b81b → RS7 25.0 + §13 granite 32768 RULER 67/55
  - opencode.jsonc        patched local-executor → granite-4.2-3b ctx 32768
  - manifesto_llm.json    v1.2 2026-08-26T16:30Z (969dcee2) — 9 models 8083+9083-9090 sync R52+ctx-cost+BENCH-01 → CONCLUÍDO
  - Baseline 9087: 0.4 t/s UNKNOWN KB/tok 41.2 ctx 16384 → novo: 3.25 t/s CONFIRMED KB/tok 25.0 ctx 32768

- [Budget] SWAP 9087 ~90k tok (download 2.24GB + 3 probes) · RAM 26/31→22/31 (-4GB) · swap 9.9→9.2G

## RunIDs (two-phase) — 9087
- [RunID] SWAP-9087-01 done dur_ms=~180s — download granite Q4_K_M 2.24GB (x-linked-size 2244012160, sha 20e43614) + header granite OK (40L GQA 40/8 RoPE 10M ctx 131072 KB/tok 25.0) → PASSOU_CATEGORICO
- [RunID] SWAP-9087-02 done — edições com backup (/tmp/*.bak-20260826-9087): start-stack.sh, ctx-cost.py, llm-inventory.json, AGENTS.md, opencode.jsonc + kill 259785 + launch 353715 granite :9087 /health OK → PASSOU_CATEGORICO
- [RunID] SWAP-9087-03 done — probe: health 9/9 OK · t/s 3.25 (3.25/3.18/3.35) prompt 16-18 t/s · thinking 15*37=555 OK · tool-calling Boston OK (reasoning_content+tool_calls) · KV 0.84GB @32768 → PASSOU_CATEGORICO (R28/R53)

## RunIDs — 9086 (legado)
- [RunID] SWAP-9086-01 done — LFM1.2B GGUF 730MB header lfm2 OK (n_ctx 128000 KB/tok 3.8)
- [RunID] SWAP-9086-02/03 — em produção (PID 320280 health OK)

## Estado
- [Phase] ts=2026-08-26T16:05-03:00 dur_ms=~600s F6-Entrega | SWAP 9087 DONE | Budget ~45% | PASSOU_CATEGORICO
- Decision: Granite substitui Qwen3.8-9B UNKNOWN (R52: CONFIRMED vence UNKNOWN) — afinidade: contexto-longo 5, skill-tecnica 4, tool 4, gbnf 4, refutacao 4, executor 3

## Notas
- **Qwen3.8-9B-Q5_K_M.gguf:** já removido de /modelos LLM/ antes desta sessão (não está em Trash atual). Trash atual contém apenas LFM2.5-230M-Q4_0.gguf (143M, DeletionDate 2026-08-26T16:06:53) + opencode-source (2.9G, jul/15). Qwen inode não está mais mmap'd — verificado via lsof (0 deleted handles) e ps (8083 agora Ornith-1.5-9B-Q5_K_M PID 375871 health ok). Trash 143M é LFM230M arquivado — manter como backup ou esvaziar via file manager (guard bloqueia rm -f).
- **manifesto_llm.json v1.2:** CONCLUÍDO 2026-08-26T16:30Z (969dcee2) — 9 models 8083+9083-9090, fonte R52+ctx-cost+BENCH-01.
- Guardrail R54: devolução supra-sumo ≤25 linhas aplicado.

## Progresso
- [RunID] SWAP-9087-01 done · SWAP-9087-02 done · SWAP-9087-03 done — veredito PASSOU_CATEGORICO (evidência: health 9/9, validate OK, ctx-cost TOTAL 11.99GB, t/s 3.25, tool/thinking OK)
- [RunID] MANIFESTO-01 done — v1.2 969dcee2 9 models sync → PASSOU_CATEGORICO
- [RunID] TRASH-01 done — Qwen 6.2GB já liberado (não está em Trash); LFM230M 143M em Trash é backup arquivado (guard bloqueia rm -f, esvaziar via file manager se desejar)
