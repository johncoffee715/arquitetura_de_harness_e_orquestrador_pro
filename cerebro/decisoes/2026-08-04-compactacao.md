---
tags: [decisao, compactacao, pipeline]
data: 2026-08-04
---

# Decisão — compactação cognitiva 2026-08-04T13:28:01.564418+00:00

# Contexto Atual — snapshot cognitivo (2026-08-04T13:28:01.564418+00:00)

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
- git:  M .git_harness_sha,  D .omo/run-continuation/ses_04cb6e0d4ffeM1PT4ykFfxEkXs.json,  M .planning/CONTEXT.md,  M "cerebro com IA/.obsidian/graph.json",  M "cerebro com IA/decisoes/2026-08-04-compactacao.md",  M harness/CONTEXT.md,  M harness/CONTEXT_COMPACT.md,  M harness/dev_loop/__pycache__/dev_loop.cpython-314.pyc,  M harness/models/__pycache__/__init__.cpython-314.pyc,  M harness/models/__pycache__/model_provider.cpython-314.pyc,  M harness/observability/__pycache__/observability_layer.cpython-314.pyc,  M node/lib/node_modules/omniroute/dist/.build/next/cache/fetch-cache/b561fbe55d2b526faa0efc680452a0a60cd7c5926b1085be6248102bc15445fc,  m opencode,  m opencode-source,  D "projetos/doom test/index-doom3d.html",  D "projetos/doom test/index.html",  D "projetos/doom test/leia-me.txt",  D "projetos/doom test/livrarias/three.module.js",  D "projetos/doom test/preview.html",  D "projetos/doom test/previews/doom3d_frame_fim.png"
- ECC_HOME: $HOME/.ecc/autofagia
- registry entries: 43

