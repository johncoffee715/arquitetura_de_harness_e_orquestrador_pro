---
tags: [decisao, compactacao, pipeline]
data: 2026-08-25
---

# Decisão — compactação cognitiva 2026-08-25T02:02:04.117239+00:00

# Contexto Atual — snapshot cognitivo (2026-08-25T02:02:04.117239+00:00)

## Decisões desta sessão
- Deploy R11 real concluído: alvos.json 16→31; 158 artefatos (15 skills+15 subagents+hooks+plugins); registry 28→43
- MTP verificado no build local llama.cpp (--spec-type draft-mtp, libmtmd.so) — feature llama-mtp p/ 4 modelos Vulkan
- MCP openwork ativado em opencode/config/opencode.json (remote, oauth, mcp_openwork: allow) — aprovado pelo usuário
- Histórico HISTORICO_AUTOFAGIA.md §16 atualizado com deploy real + MCP

## Tarefas ativas / pendências
- (sem pendências)

## Próximos passos
- Aplicar BM25 em route_to_model (herdada R10)
- pytest 8 cenários do arsenal (herdada R10)
- Opcional: testar MCP openwork (requer auth OAuth no browser)

## Riscos / estado
- WORKSPACE COM MUDANÇAS NÃO-COMMITADAS (deploy R11 + MCP openwork) — commit pendente antes de reset
- Delegação de subagents falha (anti-padrão R8/R9) — usar gh api contido
- Skills ricas preservadas (hallmark, book-to-skill — guard)

## Snapshot técnico
- git:  M "cerebro com IA/aprendizados/R64_R65_manifesto_llm_auditoria_kv_2026-08-24.md",  M harness/CONTEXT.md,  M harness/CONTEXT_COMPACT.md,  M harness/logs/gpu-watchdog.log,  M harness/watchdog/slots.json,  m opencode, ?? "Assistente Pessoal/gpu-fw/", ?? "Assistente Pessoal/logs/", ?? "cerebro com IA/decisoes/2026-08-25-compactacao.md", ?? harness/ctx-catalog.audit-history.jsonl, ?? harness/evidence/, ?? harness/logs/llm-usage-8083.jsonl, ?? harness/logs/llm-usage-8090.jsonl, ?? harness/state/, ?? harness/watchdog/lib/audit.py, ?? logs/
- ECC_HOME: $HOME/.ecc/autofagia
- registry entries: 347

