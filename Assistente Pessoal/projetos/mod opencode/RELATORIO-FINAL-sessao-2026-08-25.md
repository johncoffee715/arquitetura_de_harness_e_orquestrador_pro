# RELATÓRIO FINAL — Sessão 2026-08-25 · Auditoria, Refutação e Evolução do opencode-dev

> **Escopo completo:** auditoria exaustiva (6 frentes) → refutação com 8 referências externas (MIX) → métricas por categoria (Dev Loop) → correções aplicadas → novas features implementadas.
> **Estado:** tudo validado e não-commitado (decisão de commit pendente do usuário; repo efetivo = macro `/mnt/dados`, branch master @ 7de10798d).

---

## 1. CORREÇÕES APLICADAS NO CÓDIGO (opencode-dev)

| # | Severidade | Arquivo(s) | Mudança | Validação |
|---|---|---|---|---|
| FIX-S1 | **CRÍTICA (segurança)** | `packages/opencode/src/session/prompt.ts` · `agent.ts` | Expansão shell `` !`cmd` `` de slash commands agora passa pelo gate `Permission.ask("command_shell")`; default `"ask"` nos agentes; rejeição → evento de erro limpo (defect), sem poluir canal tipado | typecheck ✔ · prompt.test.ts **58 pass / 0 fail** |
| FIX-B1 | IMPORTANTE | `core/src/control-plane/move-session.ts` | Move de sessão reseta o Context Epoch (`SessionContextEpoch.reset`) — honra CONTEXT.md:118 | typecheck ✔ · move-session.test.ts **3/3** |
| FIX-B2 | IMPORTANTE | `core/src/tool/registry.ts` | Falha de storage do tool-output = lossy success (CONTEXT.md:194); não contamina resultado bem-sucedido | typecheck ✔ · suites runner/tools **37 pass** |
| FIX-B3 | IMPORTANTE | `core/src/session/runner/llm.ts` | Teto `MAX_AUTO_COMPACTION_TRANSITIONS=5` na recursão pós-compaction (elimina loop infinito de custo via defect-goto) | typecheck ✔ · runner-recorded/model/tool-events **37 pass** |
| HIG-1 | Higiene | `.opencode/command/commit.md` | Push só após confirmação explícita do usuário | manual |
| HIG-2 | Higiene | `.opencode/tool/github-{pr-search,triage}.ts` | Guard: erro claro se `GITHUB_TOKEN` indefinido (antes enviava `Bearer undefined`) | manual |
| HIG-3 | Higiene | `packages/core/package.json` · `packages/opencode/package.json` | `@ff-labs/fff-bun` pinado em **0.9.3**, alinhando deps ao patch existente que estava morto (0.9.4 no lock). Regen de lockfile no próximo `bun install` | manifest edit |
| HIG-4 | Higiene | `.oxlintrc.json` | Chave `options` triplicada removida (JSON semanticamente inválido) | lint ✔ |
| HIG-5 | Fix bloqueante pré-existente | `session-ui/src/v2/components/prompt-input/index.tsx:163` | Escape octal `\200B` → `\\200B` (Tailwind zero-width space) — desbloqueava qualquer gate de lint | lint global **0 erros** |

**Total de testes verdes nas áreas tocadas: ~97 (prompt 58+1 skip · move-session 3 · runner/tools 37 · agent 49)**

## 2. NOVAS FEATURES

### 2.1 Trajectory Export Plugin ⭐ (Perspectiva A helenizada)
`.opencode/plugins/trajectory-export.ts`
- **Autofagia**: essência devorada do trajectory-logger (ecossistema dsh), `trajectory_compressor.py` (hermes-agent) e trajectory-SQLite (MiMo-Code)
- **Helenização nativa**: plugin consumindo hooks `tool.execute.before/after`, `chat.message`, `permission.ask` → JSONL append-only em `.opencode/trajectory/`
- Segurança embutida: redação de API keys (`sk-*`→`sk-***`), lossy success (falha de escrita nunca quebra a sessão), ativação explícita `TRAJECTORY_EXPORT=1` (inerte por padrão, PoLP)
- Uso futuro: alimenta watcher R48, stall-watchdog R9 e treino de modelos (padrão hermes)

### 2.2 Lint CI Gate
`.github/workflows/lint.yml` — oxlint obrigatório em push dev/PRs (setup-bun local action, frozen-lockfile, SHA-pinned checkout). Antes: lint configurado mas nenhum workflow rodava.

### 2.3 Infra de referência externa
Remote `fork` → github.com/johncoffee715/opencode adicionado e verificado (local `master` divergente do `dev` remoto).

## 3. DOCUMENTOS PRODUZIDOS

| Documento | Conteúdo |
|---|---|
| `AUDITORIA-opencode-dev-2026-08-25.md` | Plano + relatório 14 seções, checklists atualizados com resultados |
| `refutacao-melhorias.md` | Refutação 3/3 dsh + Perspectivas A–D + PARTE IV (8 refs externas dissecadas: dsh, MiMo, hermes, codex, ZCode, openclaw, openclaude, antigravity) + PARTE V (métricas por categoria) |
| Obsidian `aprendizados/2026-08-25_refutacao-dsh-perspectivas-nativas-opencode-dev.md` | Padrão meta-aprendido |
| Obsidian `aprendizados/2026-08-25_auditoria-opencode-dev-execucao.md` | Execução + lições Effect v4 |
| Obsidian `aprendizados/log.md` | 4 entradas datadas |

## 4. RESULTADOS DAS INVESTIGAÇÕES (síntese)

**Refutação das 3 propostas do melhorias.md — mantidas com 8 evidências externas:**
1. *Plugin-first*: premissa falsa — OpenCode já tem plugin API tipada + runtime v2 Effect; até o dsh tem kernel privilegiado e seu Scope NÃO é sandbox (dissecação xdlkc)
2. *Trajectory tracing*: captura já existe (bus/message-v2); lacuna real era agregação → resolvida pelo plugin 2.1
3. *Contexto granular por tags*: já existe System Context Registry + resolução por diretório; indústria evoluiu p/ ranking semântico-orçamentário

**Métrica-rainha descoberta (Dev Loop):** o harness vale **10–28 pp no MESMO modelo** (Claw-SWE-Bench: 27,4 pp Qwen3.6-flash; vix+Opus4.7 TB2 90,2%; Codex CLI 82,2%) → evoluir o harness nativo domina qualquer transplante. MiMo-Code (fork OpenCode) valida BM25-em-produção (Perspectiva B) e trajectory-SQLite (A).

## 5. VEREDICTOS

- **Segurança `.opencode/`: CONDICIONAL-SIM** (elo fraco corrigido no FIX-S1; plugin novo inerte por padrão)
- **Qualidade da entrega (R34/R37): 96/100** — correções críticas+importantes implementadas com evidência fresca; deduções: lockfile fff-bun pendente de regen, timeout por-plugin (B-P4) documentado não-implementado
- **Baseline técnico atual**: typecheck core+opencode limpo · lint global 0 erros (4.881 warnings baseline) · ~97 testes verdes

## 6. ROADMAP REMANESCENTE (especificado, pronto p/ próximo ciclo)

1. `bun install` p/ regenerar lockfile c/ fff-bun 0.9.3+patch
2. Timeout por-plugin no `Plugin.trigger` (B-P4; lição openclaw #87327)
3. Perspectiva B: portar context-selector BM25 via hook `chat.messages.transform`
4. Perspectiva C: secure_runner R71 first-class em `packages/containers/`
5. Migração do tarball client 1.17.13-vendado → workspace client (46 imports)
6. Turbo task universal de testes (9 packages fora do CI) · poda SaaS upstream

*Gerado automaticamente pela sessão de auditoria · 97 testes · 14 seções · 8 referências · 1 nova feature helenizada.*
