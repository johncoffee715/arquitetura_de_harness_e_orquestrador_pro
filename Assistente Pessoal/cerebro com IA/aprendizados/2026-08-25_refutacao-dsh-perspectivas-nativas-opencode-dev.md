# Refutação dsh + Perspectivas Nativas A–D (opencode-dev)

**Data:** 2026-08-25 · **Fonte:** auditoria prévia `melhorias.md` vs código real
**Artefatos:** `/mnt/dados/Assistente Pessoal/projetos/mod opencode/refutacao-melhorias.md` · plano em `AUDITORIA-opencode-dev-2026-08-25.md`

## Aprendizado central

Propostas de absorção do "DeepSeek Harness" (dsh) refutadas por evidência de código — 3/3 não sobrevivem:

1. **Plugin-first**: premissa falsa. OpenCode já tem plugin API tipada (`packages/plugin/src/index.ts:234-282`: hooks `chat.message`, `permission.ask`, `tool.execute.before/after`, `messages.transform`) + runtime v2 Effect (`v2/effect/PLAN.md`) + provedores plugáveis nativos.
2. **Trajectory tracing**: diagnóstico errado da lacuna. Captura já existe (bus global, message-v2 com estado completo de tools); falta agregação/apresentação → resolver via PLUGIN consumidor, nunca infra nova no core.
3. **Contexto granular**: propõe o que existe (System Context Registry do CONTEXT.md; resolução por diretório em `session/instruction.ts:41-44`; merge dedup em `config/config.ts:47-48`). Contradição interna: aumenta contexto enquanto condena consumo.

**Padrão meta-aprendido (reutilizável):** documentos de comparação entre harnesses baseados em conhecimento de segunda mão tendem a subestimar o sistema alvo. Antropofagia correta (R14): devorar a ESSÊNCIA (isolamento, observabilidade, economia de contexto), implementar pelo mecanismo NATIVO do alvo (hooks/Layers/bus) — nunca transplantar órgãos.

## Perspectivas aprovadas (Capítulo 9 do plano de auditoria)

| # | Perspectiva | Via nativa | Classe |
|---|---|---|---|
| A | Observabilidade como plugin (bus→JSONL→watcher R7/R48) | hook v2 `event.subscribe` | IMPORTANTE |
| B | Port context-selector BM25 p/ OpenCode | hook `chat.messages.transform` | IMPORTANTE |
| C | secure_runner R71 first-class sandbox | `permission.ask` + containers | CRÍTICA |
| D | Storage sessão trocável | Effect Layers | OPCIONAL |

Prioridade: C → A/B → D. Validação empírica pelas Frentes B/D/F da auditoria exaustiva; evidência fresca prevalece sobre análise prévia.

## Lições para o harness
- Sempre verificar catálogo real (R8) ANTES de aceitar proposta externa de feature — 3 refutações saíram de greps de ~2 min.
- Fork canônico mapeado: github.com/johncoffee715/opencode (remote `fork`), branch local `master` divergente do `dev` remoto — commits custom R60-R71 só existem localmente.
