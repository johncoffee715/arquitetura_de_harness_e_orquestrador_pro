# R15 — GAPs Arquiteturais: Spec + Plano

> Pipeline MIX — deduplicação catálogo-primeiro (R8) dos 8 GAPs tabelados
> em F1. Aprovado no GATE 1 ("resolver tudo"). SHA checkpoint: `b8a119581`.

## Deduplicação (R8 — catálogo-primeiro)

| GAP | Veredito | Ação |
|-----|----------|------|
| Hot-swap VRAM | PARTIAL → GAP REAL (stub em `hot_swap()`) | 🔨 P1 |
| LangGraph vs AutoGen | NÃO-GAP (só em docs; motor real `harness/core/`) | ✂️ |
| MCP Obsidian | PARTIAL (file-based ok, sem MCP server) | 🔨 P4 |
| Skills/Plugins registry | NÃO-GAP (registry 10 categorias real) | ✂️ |
| Contratos de Conclusão | PARTIAL → GAP REAL (gates ad-hoc) | 🔨 P2 |
| Self-Learning | NÃO-GAP (loop `record_decision`→`_scores_from_log` real) | ✂️ |
| Scaffold Engine | NÃO-GAP (`ArsenalScaffold.plan()` real) | ✂️ |
| LSP Integration | PARTIAL (catalogado, sem gate automático) | 🔨 P3 |

## Plano executado (TDD por gap, commits atômicos)

1. **P1** — `harness/models/vram_guard.py` (VRAMGuard + ModelSwapper OOM-proof,
   drain-first, `/health` probe; `hot_swap()` real para local↔local) — commit `51dfe938b`
2. **P2** — `harness/safety/completion_contract.py` (schema por fase, hard-fail
   no DELIVER via `_check_gate`) — commit `76d7d3927`
3. **P3** — `harness/review/lsp_gate.py` (diagnóstico fail-safe na F5 sobre diff) — commit `14069d90d`
4. **P4** — `harness/mcp/obsidian_server.py` (MCP stdio: list/read/write notes,
   traversal-safe) + `.mcp.json` — commit `d6e4fbd74`

## Verificação
- 73/73 testes verdes (39 antigos + 33 novos) — zero regressão.
- Smoke end-to-end do MCP (initialize via Content-Length framing) OK.
