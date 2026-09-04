# Inventário de Features — Ecossistema OpenCode

Gerado: 2026-08-30T20:17:43.283136+00:00

## Health dos slots

- `:8083` — **online**
- `:9084` — **online**
- `:9085` — **online**
- `:9086` — **online**
- `:9088` — **online**
- `:9090` — **online**

## Providers (LLM por role)

| Provider | Role | Porta | Ctx | Tool call |
|---|---|---|---|---|
| local-thalamus | ingestor | 9084 | 1048576 | False |
| local-judge | judge | 9085 | 32768 | True |
| local-reflexo | reflexo | 9086 | 32768 | True |
| local-forge | proposer | 9088 | 65536 | True |
| local-ternary | refuter | 9090 | 65536 | False |
| local-orchestrator | orchestrator | 8083 | 262144 | True |

## Agents

- **cortex-sensorial** → `local-thalamus/ingestor`
- **executor-f4** → `local-forge/proposer`
- **explorador-tool** → `local-forge/proposer`
- **explore** → `local-forge/proposer`
- **general** → `local-forge/proposer`
- **gran-mestre** → `local-orchestrator/orchestrator`
- **hefesto** → `local-forge/proposer`
- **juiz-limbico** → `local-judge/judge`
- **planejador-f23** → `local-forge/proposer`
- **prosa-f2** → `local-forge/proposer`
- **reflexo-r42** → `local-reflexo/reflexo`
- **refutador-limbico** → `local-ternary/refuter`
- **sdd-executor** → `local-thalamus/ingestor`
- **sentinel-guard** → `local-forge/proposer`

## Skills

- **context-selector** — tags: contexto, selecao, bm25, disclosure, tokens, ferramentas
- **gran-mestre** — tags: orquestracao, meta-orquestrador, pipeline, gates, delegação, task-packet, governanca, doutrina
- **guardrail-llm-fitragem** — tags: ⚠️ SEM TAGS
- **harness-kronjob-guardrail** — tags: kronjob, talamos, guardrail, arquitetura, 10-elementos, roteamento, intencao
- **hefesto** — tags: autofagia, helenizacao, decompilacao, absorcao, forja, skill, plugin, hook, subagent, mcp, lsp
- **sdd** — tags: ⚠️ SEM TAGS
- **sentinel-guard-security** — tags: seguranca, auditoria, adversarial, sentinel, guard, vulnerabilidade

## Hooks (session.start)

- ✅ python3 /mnt/dados/Assistente Pessoal/opencode/config/opencode/hooks/kronjob-talamus-filter.py
- ✅ python3 /mnt/dados/Assistente Pessoal/opencode/config/opencode/hooks/sdd/sdd-talamus-filter.py
- ✅ python3 /mnt/dados/Assistente Pessoal/opencode/config/opencode/hooks/sync-llm-stack.py
- ✅ python3 /mnt/dados/Assistente Pessoal/opencode/config/opencode/hooks/stack-health-check.py

## Plugins

- plugin/talamus-preflight.ts

## Commands

- commands/attach.md
- commands/stack-toggle.md

## Scripts

- scripts/hefesto_motor.py
- scripts/llm-inventory.py
- scripts/attach_media.py
- scripts/auto-amelioracao.py
- scripts/filtro-veloz.py
- scripts/skills-security-audit.sh

## MCP

- (nenhum)

## LSP

- (nenhum)
