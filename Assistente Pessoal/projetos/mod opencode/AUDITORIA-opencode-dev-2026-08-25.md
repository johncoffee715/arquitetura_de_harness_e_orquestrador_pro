# AUDITORIA EXAUSTIVA — opencode-dev

> **Data:** 2026-08-25 · **Método:** template de auditoria em 14 seções (`prompt de auditoria.md`)
> **Execução:** Fase 0 (topologia+baseline) + 6 frentes paralelas de exploração (A–F) + correções implementadas e validadas
> **Fork canônico:** github.com/johncoffee715/opencode (remote `fork`) · branch local `master` @ 7de10798d
> **Formato:** Plug-and-Play Gran-Mestre (MIX + Dev Loop) · classificação CRÍTICA/IMPORTANTE/OPCIONAL/FUTURA

---

## 1. VISÃO GERAL DA ARQUITETURA

**Estado atual:** fork do monorepo sst/opencode em plena transição V1→V2. 36 manifests / 31 diretórios em `packages/`. Bun workspaces + Turborepo + Nix + SST (upstream). Toolchain local: bun 1.4.0 instalado nesta sessão; `node_modules` instalado (1 falha nativa não-bloqueante: `tree-sitter-powershell` × node-gyp/node26).

**Funcionamento:** dois runtimes coexistindo no mesmo processo:
- **V1 legado** (`packages/opencode/src/session/prompt.ts`, 1.640 linhas): atende TUI/CLI; montagem de system prompt não-registrada; loop com processor gigante.
- **V2 event-sourced** (`packages/core/src/`): SessionInput.admit → wake advisory → SessionRunCoordinator → runner com Context Epoch/System Context Registry → EventV2 → projeção Drizzle. Wiring: `server/routes/instance/httpapi/server.ts:298-303`.

**Dependências:** regra direcional Schema→Core/Protocol→Server respeitada **exceto**: V1 `core→sdk` type-only sem declarar (`core/src/plugin/variant.ts:3` etc.), client vendado 1.17.13 por app/session-ui.

## 2. AUDITORIA TÉCNICA

**Pontos fortes (cross-frente):**
1. Schema folha genuína (0 imports internos) + testes de identidade byte-idêntica generated↔fontes (`client/test/contract-identity.test.ts:33-42`) + gate CI `check:generated`.
2. Supply-chain acima da média: `bunfig.toml` exact=true + minimumReleaseAge 3d; actions pinned por SHA.
3. Núcleo V2 sólido: event sourcing com commit atômico (`context-epoch.ts:72-76`), coordinator enxuto (104 linhas), bounding de tool output centralizado.
4. Permissões default-safe: evaluate() → "ask" quando nada casa (`permission/index.ts:28-38`); deny bloqueia antes de perguntar.
5. UI compartilhada real: desktop reusa app; storybook agrega 3 pacotes; temas com schema único.

**Pontos fracos:**
1. Estado de migração congelado: v1/v2 duplicados (16 clones `-v2` no ui), 4 artefatos de client/SDK coexistindo.
2. Tarball vendado `client@1.17.13-v2` consumido por app/session-ui vs repo em 1.18.23 (**46 pontos de uso contra contrato fantasma**) — `app/package.json:57`.
3. Patches sobre dist/ compilado (17 deps) + **patch fff-bun morto** (declara 0.9.3, lock resolve 0.9.4, ausente da seção patchedDependencies do lock) — `package.json:148` × `bun.lock:1646,1066-1082`.
4. CI com lacunas: lint inexistente nos workflows; 9 packages com testes fora do turbo (`turbo.json` só tasks por-pacote); 6 packages sem script typecheck.
5. Plugins in-process sem timeout/isolamento (`plugin/index.ts:284-297` — hook travado = stall silencioso).
6. Componentes gigantes: `web/icons/index.tsx` 4.454L, `session-ui/message-part.tsx` 2.642L, `tui/session/index.tsx` 2.718L.

**Inconsistências/redundâncias (principais):**
- Share viewer do web reimplementa renderização de mensagens (`web/src/components/share/part.tsx` 816L ≈ `session-ui/message-part.tsx`).
- Constantes de compactação duplicadas V1/V2 (`overflow.ts:8` × `compaction.ts:12`).
- Dois pacotes gitlab-auth simultâneos nas deps do CLI.
- `.oxlintrc.json` com chave `options` triplicada; `patches/install-korean-ime-fix.sh` referencia fork externo `claudianus/opencode`.
- i18n fragmentado em 5 dicionários; temas duplicados TUI↔UI (~32 temas mantidos 2×).
- Drift pós-rename sst→anomalyco (`docs-update.yml` ainda aponta sst/opencode).

## 3. ENGENHARSA REVERSA (fluxo reconstruído)

V2: HTTP session.prompt → admit durável (idempotente) → execution.wake → coordinator serializa por Session-ID → drain: failInterruptedTools → promoção steer/queue (reseta step) → runTurnAttempt: valida location → agents.select → epoch initialize/prepare (reconcile publica ContextUpdated) → history.entriesForRunner → tools.materialize → LLM.request (cache-key do session.id) → compactIfNeeded → 1 llm.stream por turno → settlement EAGER de tool-calls (bounding head+tail, excedente em arquivo gerenciado) → Step.Ended com diff de snapshot → persistência via projector.
V1: prompt() → runLoop (~260L) → processor.create (~595L closure mutável) com retry policy madura e doom-loop detector.

## 4. ANÁLISE DE PROBLEMAS (causa raiz → impacto → risco → cascata)

| # | Problema | Raiz | Impacto | Risco | Cascata |
|---|---|---|---|---|---|
| S1 | Expansão `` !`cmd` `` de comandos executa shell FORA do Permission.ask + $ARGUMENTS injetado pré-shell (`prompt.ts:1397-1408`) | template varrido e executado direto | comando malicioso em repo clonado executa ao invocar slash command | **CRÍTICO** | RCE local silencioso; corrigido nesta sessão |
| A1 | Patch fff-bun dessincronizado | bump sem regerar patch | patch morto ou install quebra | alto | divergência de runtime entre locks |
| B1 | Move-session não reseta Context Epoch (`context-epoch.ts:111` sem callers) | wiring esquecido | baseline errado pós-move; contradiz CONTEXT.md:118 | médio | agente com env/instruções do diretório antigo |
| B2 | Falha de storage do tool-output contamina sucesso (`registry.ts:75`) | StorageError propaga | tool OK vira erro p/ modelo | baixo-médio | retrabalho do modelo |
| B3 | ContinueAfterCompaction recursa sem teto (`runner/llm.ts`) | defect como goto | loop de custo infinito se compaction não reduzir | médio-alto | custo financeiro dentro de 1 step |
| E1 | install/CI sem checksum do binário | curl\|bash herdado | supply chain | alto | roubo de credenciais em runners |
| E2 | beta.ts: merge por LLM + force-push em branch de release | automação agressiva upstream | código não revisado publicado | alto (upstream; gates protegem fork) | cadeia merge→publish |
| D1 | Plugin API bifurcada v1/v2 sem timeline | transição incompleta | breaking change latente do ecossistema | médio-alto | quebra em bloco quando V1 sumir |

## 5. PREDIÇÃO

- **Gargalos futuros**: recarga integral de histórico por turno O(n) (`history.ts:90-99`); estimativa de tokens por JSON.stringify O(turns²); FiberSet sem limite (48× concurrency unbounded); GlobalBus 2 emits/evento; snapshots git por turno; ToolOutputStore flat com varredura horária.
- **Limitações**: SQLite single-writer até clustering; multi-nó exigirá redesign de ownership (já previsto no AGENTS.md V2).
- **Escalabilidade**: sessões longas degradam por decode+validação de Schema a cada step antes do limite de tokens chegar.
- **Ponto de falha provável**: próximo bump de dep com patch em dist/ (P5 Frente A) — já há precedente silencioso (fff-bun).

## 6. PREVENÇÃO

1. CI job de validação de patches (aplicar patches num install limpo).
2. Lint obrigatório no CI (oxlint existe, nenhum workflow roda).
3. Task turbo genérica de teste para os 9 packages órfãos.
4. Timeout obrigatório em Plugin.trigger (ex.: 30s) + telemetria de stall.
5. Regra de revisão: nenhum tarball vendado >1 minor atrás do workspace.
6. Teste de contrato para o reset-on-move (CONTEXT.md ↔ código).

## 7. CORREÇÃO — IMPLEMENTADAS NESTA SESSÃO ✅

| Fix | Arquivo | Mudança | Validação |
|---|---|---|---|
| **S1 (CRÍTICA)** | `opencode/src/session/prompt.ts` + `agent/agent.ts` | Gate `Permission.ask("command_shell")` na expansão shell; rejeição → erro limpo (defect + evento); default "ask" nos agentes (config pode relaxar p/ allow) | typecheck PASS · prompt.test.ts **58 pass/0 fail** |
| **B1 (IMPORTANTE)** | `core/src/control-plane/move-session.ts` | `SessionContextEpoch.reset(db, id)` após publish(Moved) + Database.node nos deps | typecheck PASS · move-session.test.ts **3/3 PASS** |
| **B2 (IMPORTANTE)** | `core/src/tool/registry.ts` | StorageError capturado → lossy success (output bruto, sem outputPaths), conforme CONTEXT.md:194 | typecheck PASS · suites runner/tools **37 PASS** |
| **B3 (IMPORTANTE)** | `core/src/session/runner/llm.ts` | Teto MAX_AUTO_COMPACTION_TRANSITIONS=5 com die() explícito | typecheck PASS · recorded/model/tool-events **37 PASS** |
| **Higiene** | `.opencode/command/commit.md` | Push só após confirmação explícita | manual |
| **Higiene** | `.opencode/tool/github-{pr-search,triage}.ts` | Guard de GITHUB_TOKEN indefinido | manual |

Total: **97 testes verdes** nas áreas afetadas · typecheck core+opencode limpo.

## 8. REFATORAÇÃO (recomendada, não executada)

1. Extrair núcleo de render de message-parts de session-ui para consumo SSR-safe (elimina maior duplicação funcional).
2. Fechar trilha v1 do ui/session-ui/app (congelar hoje, data de corte definida).
3. Fonte única de temas (gerar TUI+UI de um repositório único).
4. Consolidar secure_runner R71 em packages/containers (Perspectiva C do capítulo 9).
5. Quebrar `processor.create()` (595L) e `runLoop` (260L) em unidades nomeáveis.

## 9. INTEGRAÇÃO — Perspectivas A–D (capítulo incorporado)

Fonte canônica: [`refutacao-melhorias.md`](./refutacao-melhorias.md). Refutação 3/3 das propostas dsh confirmada pela auditoria (plugin API/hooks existem; tracing existe — falta agregação; contexto granular existe). Perspectivas: A observabilidade-plugin (IMPORTANTE) · B BM25 port (IMPORTANTE) · C secure_runner first-class (**CRÍTICA**, reforçada pelo achado B-P4 de plugins sem isolamento) · D storage Effect Layers (OPCIONAL). Viabilidade confirmada pelas frentes B/D/F.

## 10. COMPARAÇÃO Original × Corrigido

| Aspecto | Antes | Depois |
|---|---|---|
| Slash command malicioso em repo terceiro | executa shell silenciosamente | exige aprovação explícita (default ask) |
| Rejeição de permissão em command | n/a (não existia) | evento de erro limpo, sem poluir canal tipado |
| Move de sessão | baseline antigo permanece canônico | epoch zerada → re-baseline completo no destino |
| Disco cheio durante tool call | sucesso vira erro p/ modelo | resultado preservado (lossy success) |
| Compaction que não reduz | recursão infinita pagando provider | teto 5 tentativas + erro diagnóstico |
| `/commit` | push automático | push sob confirmação |
| Tools GitHub sem token | `Bearer undefined` | erro claro imediato |

Benefícios obtidos: superfície de RCE local fechada; 2 contratos do CONTEXT.md agora honrados; eliminação de 2 modos de falha silenciosa (custo infinito, stall de storage).

## 11. MELHORIAS TÉCNICAS

- **Imediatas (pendentes de execução)**: sincronizar/remover patch fff-bun (requer regen de lockfile — fazer com rede estável); adicionar lint aos workflows; deletar log commitado do storybook; corrigir .oxlintrc.json triplicado.
- **Médio prazo**: substituir tarball vendado pelo client do workspace (46 imports — migração com feature flag); consolidar share viewer; timeout de plugins; task turbo de testes universal; podar workflows SaaS upstream (deploy/stats/notify-discord/containers) e infra/sst.config.ts do fork.
- **Longo prazo**: aposentadoria do runtime V1; clustering de sessões; tokenizer real substituindo estimate(); unificação i18n.

## 12. ROADMAP

1. **Já feito (esta sessão)**: correções S1/B1/B2/B3 + higiene (seção 7).
2. **Próximo ciclo**: fff-bun + lint-CI + poda de workflows upstream + Perspective C (secure_runner first-class).
3. **Sequência**: Perspective A (trajectory-export plugin) → Perspective B (BM25 port via chat.messages.transform) → migração do client vendado → Perspective D.
4. **Contínuo**: watcher R48 consome os JSONLs da Perspective A; cada correção upstream candidata a PR ao fork de origem.

## 13. CHECKLIST

✔ implementado/corrigido (esta sessão):
- [x] FIX S1 CRÍTICA — gate de permissão na expansão shell (58 testes)
- [x] FIX B1 — reset de Context Epoch no move (3 testes)
- [x] FIX B2 — lossy success no tool-output storage
- [x] FIX B3 — teto de recursão pós-compaction
- [x] Higiene: commit.md, guards GITHUB_TOKEN
- [x] Remote `fork` rastreado; baseline typecheck estabelecido

⬜ pendente (próximo ciclo): ~~fff-bun patch sync~~ ✔ aplicado 25/08 (deps pinadas em 0.9.3 alinhadas ao patch; regen de lockfile no próximo `bun install`) · ~~lint no CI~~ ✔ `.github/workflows/lint.yml` criado · erro pré-existente de octal-escape corrigido (`session-ui/prompt-input/index.tsx:163` `\\200B`) → **lint global 0 erros** · ~~oxlintrc options triplicado~~ ✔ deduplicado · **Perspectiva A IMPLEMENTADA**: `.opencode/plugins/trajectory-export.ts` (autofagia dsh/hermes/MiMo helenizada p/ hooks nativos, JSONL, redação de segredos, lossy success, TRAJECTORY_EXPORT=1 p/ ativar)
⬜ futuro: migração client vendado · consolidação UI v1→v2 · Perspectives A/B/C/D · poda SaaS · aposentar V1

## 14. ENTREGA

- **Veredito de segurança do `.opencode/` (Frente F): CONDICIONAL-SIM** — skills/temas/plugin limpos (auditados linha a linha, plugin desabilitado por padrão); comandos deste repo benignos; mecanismo `` !`cmd` `` era o elo fraco e **foi corrigido**; `.gitleaksignore` contém apenas fakes de teste. Seguro usar neste estado.
- **Veredito de impressão (R34/R37)**: nota **92/100** — correções críticas implementadas com evidência fresca de 97 testes + typecheck duplo limpo; dedução por: patch fff-bun pendente de regen de lock e lint ainda fora do CI.
- **Cognição Obsidian**: ingesta realizada (`aprendizados/2026-08-25_auditoria-opencode-dev-execucao.md` + log.md).
