# HISTÓRICO DE AUTOFAGIA & HELENIZAÇÃO — Conta Fechada

> **Propósito deste documento**: registrar TODAS as rodadas de autofagia (antropofagia tecnológica)
> e helenização (metanoia para o padrão OpenCode/Gran-Mestre) do harness — vencendo o viés do
> metadata `patterns_absorbed: 86` do SKILL.md, que só contava a PRIMEIRA rodada.
>
> Conta auditada e fechada em **2026-08-03**, com base nos docs em
> `/mnt/dados/opencode/config/gran-mestre/`, origins reais dos agents e da SKILL.md.
>
> Referência do método: `prompt de auditoria.md` (14 etapas, imperial/CNPJ,
> Plug-and-Play, autofagia anímala + helenização "metanoia" para o padrão OpenCode).

---

## 1. Definição do Método (o que é autofagia / helenização)

- **Autofagia tecnológica**: devorar a tecnologia alheia (exame criterioso quantitativo/qualitativo)
  e absorvê-la criticamente para criar identidade genuinamente funcional → self-learning, self-healing.
- **Helenização**: trazer tecnologias novas das examinadas pela autofagia e **convertê-las ao padrão
  OpenCode** (metanoia): skills/agentes/subagentes vão para subagents orquestrados por um único
  meta-orquestrador (Gran-Mestre).

---

## 2. RODADAS DE AUTOFAGIA REALIZADAS (padrões absorvidos)

| # | Rodada | Doc-fonte | Fontes | Padrões | Alvo de helenização | Data |
|---|--------|-----------|--------|---------|--------------------|------|
| 1 | **35+ Fontes** | `AUTOFAGIA_35_FONTES.md` | 35+ (MCP, OTel, A2A, pgvector, Temporal/Redis/Inngest, ADK/CrewAI/LangGraph/OpenAI-Agents, LangFuse/TestSprite/BMAD, OpenSpec/AgentSkills/SpecKit, Postgres, Pinecone) | **86** | Gran-Mestre (pipeline MIX, 8 librarians) | 2026-07-29 |
| 2 | **9 Repos** | `AUTOFAGIA_9_REPOS.md` | 9 (anthropics/skills, affaan-m/ecc, context7-skill, OpenAgentsControl, i-have-adhd, dashi-ppt-skill, grok-build, vercel-labs/skills, buzz) | **47** | Gran-Mestre (6 workers) | 2026-07-29 |
| 3 | **6 Repos Lote 2** | `AUTOFAGIA_6_REPOS_2.md` | 6 (karpathy-skills, DeepSpec, Instatic, open-design, ruflo, wigolo) | **35** | Gran-Mestre (MIX) | 2026-07-29 |
| 4 | **OpenClaude** | `OPENCLAUDE_INTEGRATION.md` / `REGISTRY_OPENCLAUDE.md` | Gitlawb/openclaude | ~12 | Integração de padrão do OpenClaude | 2026-07-29 |
| 5 | **Mixture-of-Agents** | `MOA_INTEGRATION.md` | togethercomputer/MoA | ~8 | Composição múltiplas respostas | 2026-07-29 |
| 6 | **Crossover/auditoria** | `AUDIT_METHODOLOGY.md` | auditoria gran-mestre crossover | **12** | Aegis/validação de padrões cross | 2026-07-29 |
| 7 | **Self-learning** | `SELF_LEARNING.md` | auto-inspeção dos padrões do orquestrador | **22 + 12 anti-padrões** | comportamento do orquestrador | 2026-07-29 |

### Subtotal concretizado
**3 rodadas massivas + 4 rodadas parciais** = **≥ 214 padrões documentados**
(86 + 47 + 35 + 12 + 12 + 22), mais **12 anti-padrões** (self-learning) e **MoA sem contagem
declarada** (n/d). Agents orgânicos: **46** (34 gsd-helenizado + 7 superpowers sem origin +
2 oh-my-openagent-helenizado + 3 gran-mestre-original). Skills com proveniência explícita: **6+**.
*A conta real fecha com a soma dos docs, não com o 86 do SKILL.md.*

---

## 3. ESTADO DA HELENIZAÇÃO POR CATEGORIA (origins reais)

### 3.1 Agents (arquivos de definição)
- `gran-mestre-original`: **3** (gran-mestre, hestia, atena)
- `gsd-helenizado`: **34** (todo o ecossistema GSD, subagents orquestrados)
- `oh-my-openagent-helenizado`: **2** (memory-keeper, reverser)
- sem origin (vanilla superpowers): **7** → **NOTA: etiqueta de origem ausente — pendente de etiquetar**
- **Total agents: 46** (44 top-level + 2 subagents gran-mestre dir)

### 3.2 Skills (proveniência explícita)
| Skill | Proveniência |
|-------|--------------|
| `fable-judge` | Sahir619/fable-method (MIT) |
| `browser-use` | browser-use/browser-use (MIT), absorbed_at 2026-07-22 |
| `ck` | sreedhargs89/context-keeper (community) |
| `athena` | composição sobre oracle (oh-my-openagent) |
| `archify` | based_on Cocoon-AI/architecture-diagram-generator (MIT) |
| `pxpipe` | teamchong/pxpipe (source) |

### 3.3 Convenção de origem (aplicada nos templates)
`origin: gran-mestre-original | absorvido:<fonte> | crossover:<f1>+<f2> | gsd-helenizado | oh-my-openagent-helenizado`
→ **Alinhar**: substituir etiquetas mistas por `absorvido:<repo>` (proveniência clara) e aplicar
`origin` aos 7 superpowers sem etiqueta.

---

## 4. RODADA PENDENTE (12 alvos listados, NÃO absorvidos ainda)

Fonte: `executar autofagia e helenizaçao.md` (alvos da próxima onda):

1. alvinunreal/oh-my-opencode-slim
2. earendil-works/pi
3. ruvnet/RuView
4. oblien/openship
5. tirth8205/code-review-graph
6. ayghri/i-have-adhd (parcial: já consta no 9-repos)
7. stablyai/orca
8. diegosouzapw/OmniRoute
9. mattpocock/skills
10. koala73/WorldMonitor
11. bojieli/ai-agent-book
12. onovoprogramador/onp-spec-driven

> **Para fechar a conta de vez**: executar esta rodada (modo MIX + DEV LOOP), registrar
> cada absorção num doc `AUTOFAGIA_<n>_...md`, e somar ao inventário. A conta de fontes
> (35+9+6+12) e padrões (à medida) precisa virar o novo total global.

---

## 5. INCONSISTÊNCIA RAIZ (auto-auditoria)

| # | Divergência | Evidência | Correção |
|---|-------------|-----------|----------|
| 1 | `patterns_absorbed: 86` não soma 47+35+22+12 | SKILL.md metadata | somar à soma real ≥ 214, ou mudar para "≥ 200+ múltiplas rodadas" |
| 2 | Agents sem `origin` (7 superpowers) | escolha | etiquetar com `origin: absorvido:superpowers` |
| 3 | Rodada de 12 alvos não registrada | executar-autofagia.md | executar e documentar, e gerar `AUTOFAGIA_12_ALVOS.md` |

---

## ENTREGA (fecho da conta)

**Conta fechada em:** 2026-08-03
**Documentos auditados:** AUTOFAGIA_35_FONTES, AUTOFAGIA_9_REPOS, AUTOFAGIA_6_REPOS_2,
OPENCLAUDE, MOA, AUDIT_METHODOLOGY, SELF_LEARNING, TEMPLATE_AUTOFAGIA_{V1,V2}, subagents/*,
prompt de auditoria.md, executar autofagia e helenização.md, gran-mestre-source/
**Resultado:** a conta NÃO fechava porque o SKILL só dizia uma rodada (86), mas há ≥ 214 padrões
documentados em 3 rodadas massivas + 4 parciais + agents/RGG integrados.
**Cognição neurológica**: acoplado ao Obsidian (`cerebro com IA/`) conforme prática do harness.
**Ação imediata sugerida:**
 1. Atualizar o SKILL.md `patterns_absorbed` → `patterns_absorbed: 214+ (múltiplas rodadas)`.
 2. Rodada pendente (12 alvos) como próximo passo no pipeline MIX.
 3. Etiquetar `origin` dos 7 superpowers para fechar a métrica de proveniência.

---

## 6. RODADA 8 — 26 ALVOS (2026-08-03)

Fonte: `AUTOFAGIA_26_ALVOS_R8.md` (modo MIX + Dev Loop N3, caça paralela librarian/explore + escalada gh api).

| Alvos | Veredito |
|-------|----------|
| 23 repos/URLs (hallmark, buzz, fallow, openwork, last30days, kaneo, book-to-skill, GeoLibre, bitchat, box3d, awesome-llm-apps, impeccable, quill, unsloth-zoo, Mole, hubble.md, native, dokku, decimen-optical-transfer, OpenSlides, world-model-optimizer, ratel, grill-me) | **ABSORB 5** (hallmark, book-to-skill, openwork→executor-deep, fallow→mcp/lsp-reviewer), **MINE 6** (ratel, world-model-optimizer*, dokku, OpenSlides, awesome-llm-apps, hubble.md, impeccable, buzz, unsloth-zoo, grill-me), **SKIP 12** (quill, Mole, bitchat, native, box3d, GeoLibre, kaneo, decimen*, OpenSlides-parte) |

**Concretizado (instalado + registrado):**
- Skills: `hallmark` (design anti-slop) + `book-to-skill` (meta-skill livro→skill, 15 módulos Python) em `~/.opencode/skills/`
- Subagents: `executor-deep` (openwork) + `fallow-mcp-reviewer` + `fallow-lsp-reviewer` em `~/.config/opencode/agents/`
- Registros: `registry/autofagia-{hallmark,book-to-skill,openwork-executor-deep,fallow}.md`
- Doc: `AUTOFAGIA_26_ALVOS_R8.md` | Safety SHA: `63f356189`

**Anti-padrão registrado:** delegação bruta de fetch a librarian estourou limite do provider (7/7 falhas, sessões corrompidas em 6-10s) → pesquisa externa sempre via `gh api`/raw.githubusercontent contido.
**Segurança:** last30days-skill teve RCE real (SessionStart env) — ADAPT só a pipeline, nunca o hook cru.

**Novo total global estimado:** 214+ (rodadas 1-8, múltiplas fundações).

---

## 7. RODADA 8-B — HELENIZE-DEPLOY + REFATORAÇÃO ECC v2 (2026-08-04)

| Entrega | Detalhe |
|---------|---------|
| **helenize_deploy.py** | spec `alvos.json` 12→14 (hallmark, book-to-skill); 86 artefatos gerados; hooks `helenize-{hallmark,book-to-skill}.sh`, plugins `index.ts`, subagents `.md`, upsert registry (5 padrões cada); SKILL.md ricos preservados via backup/restore |
| **Refatoração ecc-autofagia v2** | Auditoria v1.0-audit aplicada: `lib/{core,crypto}.sh`, `$ECC_HOME` portável, flock/realpath/mask/backoff, registry JSON, event bus JSONL, `deploy` idempotente (hardlink detectado), settings.json fantasma (ecc-attest/ecc-complete) corrigido, SKILL.md v2 |
| **Segurança** | SHA 63f356189; backup `~/.ecc/backup-ecc-v1-20260804-011620/` (7 arquivos); validação bash -n 9/9 + smoke tests (tamper detectado) |

**Próxima rodada (R9) em análise:** ratel runtime (context engineering, BM25 progressive disclosure) + dokku deploy (PaaS plugin-hooks) — MINE de maior retorno.

---

## 8. RODADA R9 — CONTEXT-SELECTOR + DOKKU-DEPLOY (2026-08-04)

| Entrega | Detalhe |
|---------|---------|
| **context-selector** | `ratel-ai/ratel` → skill+subagent (6 padrões: searchable_text, BM25 k1=0.9/b=0.4, replace-vs-suggest, skills first-class, disclosure progressivo, adaptive usage ranking) |
| **dokku-deploy** | `dokku/dokku` → skill+subagent (5 padrões: fluxo git push, app.json, plugin-hooks prefixo numérico + triggers, command API, plugin.toml/pipefail) |
| **helenize_deploy** | spec 14→16 alvos, 98 artefatos (skill/subagent/hook/plugin/registry); guard de SKILL.md rico + MCP derivado da spec + parse JSON robusto (v1.2) |
| **Falha de delegação** | 2 frontes librarian R9 presas 43min → canceladas (5/5 tasks) → **fallback de extração própria via gh api/raw contido** (re-registrar anti-padrão de delegação lenta) |

---

## 9. RODADA R10 — AUTOFAGIA DO HARNESS + REGRA GLOBAL QQQ (2026-08-04)

| Item | Detalhe |
|------|---------|
| **arsenal.py v2** | integrado do usuário (361L, idêntico ao entregue) + fix de normalização int/list (registry pós-`--fresh` é int-based → `--fresh` agora rc=0) |
| **helenize_deploy.py v2+R8** | merge externo (14 vulns HLD: slug regex, shell_escape, flock, atomic, schema, dry-run) **+ fixes R8 preservados** (guard SKILL.md rico, is_mcp derivado da spec, hook JSON via jq). 16 alvos, 82 artefatos, ricos preservados |
| **arsenal_v2.py entregue** | corrompido (4 quebras `\n`, bug HOME) → **rejeitado** pelo QQQ; auditoria do usuário confirmada; versão corrigida APROVADA |
| **Regra global `helenize_import.py` v2** | **QQQ**: quantitativa (score 0-100), qualitativa (py_compile+ast+tokenize+corrupção determinística por tokenize+undefined globals), otimizada (dry-run, ThreadPool, atomic, diff), gera **plano de refatoração** p/ padrões do harness. Autovalidação 90 pts |
| **Hook `helenize-gate.sh`** | dispara a políica (PostToolUse Write/Edit em Downloads/autofagia), nunca bloqueia |
| Aprendizado | scanner de corrupção via tokenize STRING-token (rejeita `\n` real sem aspas triplas) é o detector determinístico — heurística de aspa-ímpar dá falso positivo |

---

## 10. RODADA R10-A — CI + BM25 + ATOMICIDADE (2026-08-04)

| Entrega | Detalhe |
|---------|---------|
| **(a) CI `--validate-only`** | `helenize_import.py` ganhou modo CI: valida TODOS candidatos sem integrar; PASS≥60/FAIL; exit 0/2/0 (aprov/reprov/empty). Rejeita corrompido (score 0), aceita corrigido (79) |
| **(b) BM25 no roteamento** | `integration.py` `select_for_task` ganhou ranker **BM25 lexical puro** (k1=0.9, b=0.4 — padrão ratel/context-selector R9) como boost fino (0..3) sobre o matching por tags/sinônimos. Task de segurança → prioriza code-review-graph/reviewers |
| **(c) Atomicidade `build_fresh()`** | `arsenal.py` agora persiste registry com `tempfile+os.replace+fcntl.flock` (mesmo padrão do helenize_deploy). `--fresh` rc=0 |
| **Bug perdido no cp** | o `cp` do `arsenal_v2.py` do usuário sobrescreveu o fix de normalização int/list → **reaplicado** sobre a entrega (registry int-based pós `--fresh` não quebra mais). Lição: **adotar entrega + re-aplicar fixes locais sobre ela** |
| Safety | backup R10; compila todos; CI PASS; `--fresh`/padrão/`--cat`/`--json` rc=0 |

---

## 11. RODADA R10-B — REGRA DE COMPACTAÇÃO COGNITIVA + BM25/PYTEST (2026-08-04)

| Entrega | Detalhe |
|---------|---------|
| **Regra global de compactação a 50%** | `harness/cognition/compact_context.py` (armazenar→compactar→limpar, preservando git/workspace) + hook `~/.claude/hooks/ecc-compact-gate.sh` (PreCompact) + skill `context-compaction`. Validado: dry-run inócuo, run real grava CONTEXT.md + CONTEXT_COMPACT.md + decisão Obsidian |
| **BM25 no route_to_model** | integrado via `select_for_task` (já ranqueia por BM25 R10-A) — `route_to_model` consome a ordem rankeada; dead code removido (2ª computação BM25 era lixo) |
| **pytest 8 cenários do arsenal** | `harness/tests/test_arsenal.py` — padrão, --cat lazy, --json unicode, --pads, --fresh (subprocess mock), agent-registry ausente, registry corrompido (exit 2), integration.py ausente (exit 1) → **8/8 PASSED** (predição de longo prazo da auditoria R10 materializada) |
| Lição | testes C3/C5: API real do arsenal usa `format_json`/`format_pretty` (estáticos); INTEGRATION_PY é lido no escopo do módulo |

---

## 12. RODADA R10-C — REGRA GLOBAL DE INFERÊNCIA GPU-ONLY + WATCHDOG (2026-08-04)

| Item | Detalhe |
|------|---------|
| **Problema** | Após queda do llama-server, respawn caía em CPU/RAM — GPU ociosa (0% GPU, 18% VRAM) e sem watchdog |
| **Fantasma removido** | `llama-qwen35.service` (systemd user) era órfão: ExecStart `/tmp/opencode/run-llama.sh` inexistente → **disabled+removido** (backup `/tmp/llama-qwen35.service.orphan.bak`) |
| **Watchdog v2** | `harness/autofagia/gpu-watchdog.sh` — respawn assíncrono (setsid+timeout), check `/health`, `on_gpu` (log Vulkan/ngl999), backoff, `ECC_CPU_ALLOWED=1` como exceção explícita (NUNCA CPU por default) |
| **Unit systemd** | `gpu-watchdog.service` (user) — `Restart=always`, `--loop 30`, portas 8081-8084; **enabled + ativo** |
| **Prova de fogo** | GPU ociosa→ watchdog ressuscitou 4 modelos em Vulkan (`-ngl 999 -dev Vulkan0`), portas HTTP 200, **VRAM 94%** (GPU, não CPU/RAM) |
| **Bug de loop corrigido** | `/health` devolve 503 até o modelo carregar → watchdog re-spawnava; mitigado com backoff (respawn em tentativas espaçadas) |

## 13. R10-D — CAUSA-RAIZ DO PANIC: SESSÕES CONCORRENTES (2026-08-04)

**Causa raiz do 'panic'**: duas sessions rodaram `start-all-models.sh` simultaneamente.
Cada uma faz `pkill -9 -x llama-server` — matava os llama-servers que a OUTRA acabou
de subir → loop de mata-levanta → respawn/503.

**Fix**: flock cooperativo (`flock -n`) em `start-all-models.sh` — a 2ª instância desiste
em vez de matar a 1ª. Watchdog (gpu-watchdog.sh v2) já usa backoff.

**Evidência**: 1ª chamada obtém lock, 2ª bloqueada; portas 200×4 estáveis; watchdog vivo.
Resolve sem tocar em CPU (regra GPU-only intacta).

---

## 14. R10-E — REGRA GLOBAL: NENHUMA SESSÃO DELETADA SEM REGISTRO/COMPACTAÇÃO/LIMPEZA (2026-08-04)

| Item | Detalhe |
|------|---------|
| **Regra** | Ao comando de deletar/encerrar sessão, ANTES executa o ciclo: **REGISTRAR (cognitivo) → COMPACTAR → LIMPAR**, só então deleta |
| **Hook** | `~/.claude/hooks/ecc-session-end.sh` — chama `compact_context.py` (armazenar→compactar→limpar), nunca bloqueia (exit 0), idempotente; variável `SESSION_DELETE=1` registra no log quando é deleção explícita |
| **Registro** | `settings.json` → eventos **`Stop`** (fim) e **`SessionEnd`** (deleção), JSON validado |
| **Teste** | Hook acionado com `SESSION_DELETE=1`: ciclo completo rodou (CONTEXT.md + CONTEXT_COMPACT.md + decisão Obsidian + log "DELETED session"), workspace/git intacto (45 sujos = intocado), rc=0 |
| **Cadeia completa** | SessionStart→…→PreCompact (compact-gate) →Stop/SessionEnd (session-end)→ registro+compactação+limpeza ≥ todo release |

## 15. R10-F — REGRA GLOBAL TAMBÉM NO OPENCODE (session.deleted) (2026-08-04)

Extende a regra R10-E (nunca deletar sessão sem registrar→compactar→limpar) ao OpenCode nativo:
- Plugin dedicado `~/.config/opencode/plugins/ecc-session-delete/index.ts` — hook nativo
  `session.deleted` → dispara `ecc-session-end.sh` (ciclo completo via compact_context.py), fire-and-forget.
- Registrado no `opencode.json` array `plugin`: `./plugins/ecc-session-delete` (JSON válido).
- `tsc --noEmit` limpo (0 erros; tipado `$`/`_input`).
- Ja havia: Claude Code `Stop`+`SessionEnd` (R10-E) e `PreCompact` (compact-gate) — agora ambas as plataformas garantem o ciclo antes de deletar encerrar.

## 16. RODADA R11 — 36 FONTES EXTERNAS + MTP LLAMA.CPP (2026-08-04)

Fonte: `AUTOFAGIA_R11_36_FONTES.md` (modo MIX + Dev Loop N2/N3, 5 waves librarian → fallback gh api).

| Frente | Veredito |
|--------|----------|
| 36 fontes (23 repos R8 re-verificados + 13 novas: anthropics/skills, skills.sh ×7, All Time library, deepagents, cc-harness-iai, spec-kit, cleveres-ai MTP, llama.cpp PR#22673, coderabbitai) | **ABSORB novos 9 + 1 feature** (llama-mtp, anthropics-skills, deepagents, last30days-skill, cc-harness-iai, impeccable, spec-kit, vercel-agent-skills, openwork-mcp), **ATUALIZAR 1** (executor-deep→openwork-mcp), **MINE 11**, **SKIP 7**, **ABSORVIDO verificado 8** (hallmark, book-to-skill, context-selector, dokku, mattpocock, fallow, ratel) |

**Destaque — Feature de inferência ★**: **llama.cpp PR #22673 (MTP — Multi-Token Prediction) MERGED** —
speculative decoding integrado (MTP heads), ~75% acceptance de 3 draft tokens, **>2x speedup** sem draft
model separado. Aplicável aos 4 modelos locais Vulkan (`--mtp`/rebuild). Prioridade 20.

**Concretizado (deploy REAL concluído 2026-08-04):**
- Doc: `AUTOFAGIA_R11_36_FONTES.md` | Proposta: `harness/autofagia/alvos_r11_proposta.json` (15 alvos, 15/15 válidos no schema Alvo)
- **Merge**: `alvos.json` 16 → **31 alvos** (16 existentes + 15 novos, zero colisões; backup `.bak.*` preservado)
- **Validação**: `helenize_deploy.py --validate-only` → EXIT=0, "OK 31 alvos válidos"
- **Dry-run**: 36 artefatos previstos, EXIT=0
- **Deploy real**: `helenize_deploy.py` → EXIT=0, **158 artefatos OK** — 15 novos alvos com skill+subagent (SKILL.md + agents/), hooks `helenize-*.sh`, plugins `index.ts`; skills ricas existentes preservadas (hallmark, book-to-skill — guard "rico preservado")
- **Registry**: `agent-registry.json` 28 → **43 entradas** (15 novos registrados: llama-mtp, anthropics-skills, deepagents, last30days-skill, cc-harness-iai, impeccable, spec-kit, vercel-agent-skills, openwork-mcp, world-model-optimizer, azure-skills, awesome-llm-apps, coderabbit, llama-mtp-concept, unsloth-zoo)
- **MTP verificado no build local**: `llama-server --help` → `--spec-type none,draft-simple,draft-eagle3,draft-mtp,...` + `libmtmd.so` presente em `/home/johncoffee/llama.cpp/build/bin/` — feature `llama-mtp` aplicável aos 4 modelos Vulkan
- **MCP openwork ativado** (pós-deploy, usuário aprovou): `opencode/config/opencode.json` ganhou entrada `mcp.openwork` (type=remote, url=`https://api.openworklabs.com/mcp/agent`, enabled=true, oauth={}) — formato oficial do README `different-ai/openwork` — + permissão `mcp_openwork: allow`. JSON validado (parse estrito ok). Agora mcp entries = `[ghidra, openwork]`
- Safety SHA: `2414e03af1b27fb0bf74d9208010bebbf39b6126` (checkpoint pós-merge, antes do deploy)

**Anti-padrão re-registrado (lição R8/R9):** delegação de pesquisa de catálogo amplo a 5 librarian agents
ficou presa 20min+ → cancelada (background_cancel all) → mineração própria contida via `gh api`
(readme/contents/pulls, determinística, ~2min p/ 27 repos + PRs). Pesquisa externa de catálogo grande
SEMPRE via gh api contido.

**Segurança R11:** ecossistema de skills tem risco real de supply-chain (335+ skills maliciosas em ClawHub,
campanha mirando API keys) → política: absorver SOMENTE de fontes oficiais (anthropics, vercel-labs,
microsoft) ou repos com milhares de installs; `allowed-tools`; skill = código não-confiável.
last30days-skill: ADAPT só pipeline, nunca hook cru (RCE histórica upstream).

**Novo total global estimado:** 214+ (rodadas 1-11) + 9 absorções + 1 feature novas (R11).

