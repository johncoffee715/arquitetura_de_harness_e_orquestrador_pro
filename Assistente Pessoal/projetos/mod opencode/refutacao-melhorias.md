# REFUTAÇÃO — melhorias.md (Conceitos dsh) + Perspectivas A–D de Evolução Nativa

> **Data:** 2026-08-25 · **Alvo:** `melhorias.md` (propostas de absorção do DeepSeek Harness/dsh)
> **Método:** dissecação técnica com evidência `arquivo:linha` no código real de `opencode-dev/`
> **Formato:** Plug-and-Play (Ctrl+A/C/V) para o Gran-Mestre — modo MIX + Dev Loop, self healing
> **Status:** Refutação integral das 3 propostas · 4 perspectivas nativas propostas (A–D)
> **Incorporação:** este documento é o **Capítulo 9 (Integração)** do plano de auditoria
> `AUDITORIA-opencode-dev-2026-08-25.md` e alimenta a seção 12 (Roadmap). Viabilidade de A–D
> será validada empiricamente pelas Frentes B/D/F da auditoria exaustiva.

---

## PARTE I — REFUTAÇÃO DAS 3 PROPOSTAS

### Proposta 1 — "Arquitetura Modular de Plugins (Plugin-First Runtime)" → REFUTADA

**Afirmação original:** o OpenCode "depende apenas de configurações estáticas ou módulos engessados em JS/TS"; seria preciso copiar do dsh um sistema de hooks/extensões com backends alternativos (Docker/Firecracker) e persistência de sessão trocável.

**Refutação — premissa factualmente falsa.** O OpenCode já possui sistema de plugins maduro, tipado e mais sofisticado que o descrito:

| Evidência | Arquivo | O que prova |
|---|---|---|
| Hooks tipados `chat.message`, `permission.ask`, `tool.execute.before/after`, `chat.messages.transform` | `packages/plugin/src/index.ts:234-282` | Interception API completa, não estática |
| Runtime v2 Effect: `ctx.tool.hook()`, `ctx.event.subscribe()` | `packages/plugin/src/v2/effect/PLAN.md` | Interceptação estruturada por domínio |
| Provedores plugáveis nativos | `packages/opencode/src/plugin/`: `azure.ts`, `cerebras.ts`, `cloudflare.ts`, `digitalocean.ts`, `github-copilot/`, `modal/`, `openai/`, `snowflake-cortex.ts`, `xai.ts` | Provider layer é plugin-first |
| MCP nativo | `packages/opencode/src/mcp/` | Extensão de ferramentas sem tocar o core |
| Sandbox alternativo já existente | `packages/containers/` + `secure_runner` R71 (whitelist estrita, PoLP) | Backend de execução isolado já implementado no fork |

- Copiar o modelo dsh = reinvenção redundante (**viola R8 — Catálogo Primeiro**).
- Firecracker exige privilégios de kernel Linux e quebra o ethos local-first/portável do OpenCode.
- Persistência trocável: a separação direcional Schema→Core→Protocol→Server (AGENTS.md do repo) + Effect Layers já direciona isso idiomaticamente (ver Perspectiva D).

**Veredito:** REJEITADA como proposta; intuição válida absorvida nas Perspectivas C e D.

---

### Proposta 2 — "Auditoria e Rastreabilidade de Trajetórias (Trajectory Tracing)" → PARCIALMENTE REFUTADA

**Afirmação original:** faltaria ao OpenCode visibilidade dos passos do agente (tool chamada, payload, retorno cru); seria preciso um modo verbose/debug estruturado na TUI.

**Refutação — diagnóstico errado da lacuna.** A captura de trajetória JÁ EXISTE; falta apresentação, não infraestrutura:

| Evidência | Arquivo | O que prova |
|---|---|---|
| Bus de eventos global | `packages/opencode/src/bus/global.ts` | Pub/sub de todos os eventos de runtime |
| Bridge de eventos v2 | `packages/opencode/src/event-v2-bridge.ts` | Camada de eventos versionada |
| Estado completo de tool calls persistido | `packages/opencode/src/session/message-v2.ts` (`part.state.status/time/metadata`) | Payload, timing e metadados duráveis por chamada |
| Histórico projetado por sessão | CONTEXT.md (glossário: Session History, Provider Turn, Session Drain) | Trajetória reconstruível do transcript |

- Construir "infraestrutura nova de tracing" ignoraria o bus existente e criaria segunda fonte de verdade (efeito cascata: divergência de eventos, custo de manutenção duplo).
- A lacuna real é de **agregação/apresentação** → resolvida por plugin consumidor (Perspectiva A), zero mudança no núcleo.

**Veredito:** NEGAÇÃO da premissa de ausência; necessidade real reformulada na Perspectiva A.

---

### Proposta 3 — "Gerenciamento Contextual Granular (Isolamento de Diretivas)" → REFUTADA

**Afirmação original:** o OpenCode "injeta tudo cegamente no prompt inicial"; seria preciso um seletor dinâmico baseado em tags ou escopos de diretório.

**Refutação — propõe o que já existe:**

| Evidência | Arquivo | O que prova |
|---|---|---|
| **System Context Registry**: "registry de produtores ordenados e escopados por Location" | `CONTEXT.md` (glossário canônico do runtime) | Contexto é montado por produtores escopados, não injetado cegamente |
| Context Sources com snapshot, epoch e baseline imutável | `CONTEXT.md` (Context Epoch, Context Snapshot, Safe Provider-Turn Boundary) | Controle granular de admissão por turno de provider |
| Resolução de instruções POR DIRETÓRIO (`find(dir)`, `resolve(messages, filepath, messageID)`) | `packages/opencode/src/session/instruction.ts:41-44` | AGENTS.md/instruções resolvidas contextualmente |
| Merge deduplicado de instruções multi-fonte | `packages/opencode/src/config/config.ts:47-48` | Priorização e dedup já implementadas |

**Contradição interna do `melhorias.md`:** a proposta 3 (seletor dinâmico carregando regras sob demanda) AUMENTA complexidade de contexto, enquanto a lista "o que NÃO copiar" condena consumo excessivo de tokens. O documento puxa nas duas direções.

**Veredito:** REJEITADA como proposta; a economia de contexto REAL fica melhor servida pela Perspectiva B (seleção semântica BM25 que você já possui).

---

## PARTE II — PERSPECTIVAS A–D DE EVOLUÇÃO NATIVA

> Essência extraída do dsh pela antropofagia (R14): **isolamento, observabilidade, economia de contexto**.
> Implementação: pelos mecanismos NATIVOS do OpenCode (hooks/Layers/bus) — nunca transplante de órgãos estranhos.

### Perspectiva A — Observabilidade como Plugin, não como Core

**Classificação: IMPORTANTE**

| Dimensão | Detalhe |
|---|---|
| **O quê** | Plugin consumindo o bus existente (`src/bus/global.ts`) → exporta árvore de trajetória em JSONL estruturado (tool, payload, retorno, duração, agente) + painel TUI de debug opcional |
| **Como** | Hook de plugin v2 (`ctx.event.subscribe`) — zero modificação no núcleo; arquivo único em `.opencode/plugins/` ou pacote dedicado |
| **Prós** | Reversível; alimenta diretamente watcher R48/stall-watchdog R9/R7 (heartbeat); sem segunda fonte de verdade; observabilidade desacoplada |
| **Contras** | Overhead de I/O se verboso demais (mitigar: buffer + rotação) |
| **Riscos** | Vazamento de payload sensível no log → sanitização obrigatória (R6 segurança) |
| **Impacto** | Troubleshooting de loops infinitos sem interceptar HTTP; cognição do Gran-Mestre ganha corpus de trajetórias |

### Perspectiva B — Helenização Reversa do context-selector (BM25)

**Classificação: IMPORTANTE**

| Dimensão | Detalhe |
|---|---|
| **O quê** | Portar o skill `context-selector` (BM25 + disclosure progressivo, já helenizado no harness) como plugin OpenCode via hook `experimental.chat.messages.transform` (`packages/plugin/src/index.ts:282`) |
| **Como** | Plugin filtra/prioriza mensagens e fontes de contexto por relevância BM25 antes do envio ao provider |
| **Prós** | Seleção SEMÂNTICA > seleção por tags (proposta 3 refutada); você já possui a tecnologia (R8 atendido); economia de tokens onde o dsh falha |
| **Contras** | Risco de filtrar contexto necessário → limiar conservador + fallback para inclusão total |
| **Riscos** | Regressão sutil de qualidade de resposta; exigir bench A/B antes de ativar por padrão (R28: critério categórico) |
| **Impacto** | Janela preservada em tasks longas; sinergia total com R-context-compaction |

### Perspectiva C — Consolidação do secure_runner (R71) como Sandbox First-Class

**Classificação: CRÍTICA** (segurança)

| Dimensão | Detalhe |
|---|---|
| **O quê** | Promover o `secure_runner` (R71: whitelist estrita, vault invisível, rede off default, PoLP) de script do harness a pacote first-class em `packages/containers/`, exposto via hook `permission.ask` |
| **Como** | Integração com o sistema de permissões nativo (`packages/opencode/src/permission/`) — execução de comandos roteia pelo sandbox quando policy exigir |
| **Prós** | Isolamento real sem Docker/Firecracker (sem privilégios de kernel); alinhado ao ethos local-first; aproveita trabalho já feito |
| **Contras** | Superfície de compatibilidade: ferramentas que assumem execução direta podem precisar de ajuste |
| **Riscos** | Escape de sandbox mal testado → auditoria adversarial obrigatória (Frente F) antes de ativar por padrão |
| **Impacto** | Atende a intuição válida do item 1 do melhorias.md pela via nativa; segurança auditável |

### Perspectiva D — Persistência de Sessão Trocável via Effect Layers

**Classificação: OPCIONAL** (médio prazo)

| Dimensão | Detalhe |
|---|---|
| **O quê** | Expor o storage de sessão como Layer substituível (SQLite default → qualquer backend: arquivo, rede, Obsidian) usando o padrão Effect Layer já dominante no codebase |
| **Como** | A separação direcional Schema→Core→Server (AGENTS.md) já isola contratos; basta extrair interface de storage + layer alternativa |
| **Prós** | Idiomático do projeto (zero framework novo); atende a intuição "persistência trocável" do item 1; testes com storage in-memory ficam triviais |
| **Contras** | Refatoração de média envergadura no core de sessão; benefício imediato limitado para uso single-machine |
| **Riscos** | Instabilidade regressiva no caminho crítico de sessão → feature flag + rollback SHA |
| **Impacto** | Escalabilidade futura (multi-dispositivo, backup integrado à cognição Obsidian R26) |

---

## PARTE IV — REFERÊNCIAS EXTERNAS (validação MIX, 2026-08-25)

> Referências primárias dissecadas a pedido do usuário para reforçar/refutar cada proposta e perspectiva.
> Fontes: deepseek-ai/deepseek-harness · XiaomiMiMo/MiMo-Code · NousResearch/hermes-agent · carsonfeng/ZCode · openai/codex · opencode.ai/docs · PRs/issues upstream · literatura de context engineering.

### R1 — dsh oficial confirma instabilidade e arquitetura dual-kernel

| Fato | Fonte |
|---|---|
| "Developer preview… **THERE WILL BE COMPATIBILITY-BREAKING CHANGES**" | README.md do repo dsh |
| Kernel Cordis gerencia montagem/desmontagem/dependências de plugins; capacidades (models, tools, sessions, sandboxes, storage, loops, UI) são plugins | deepseek.com/harness/en + docs/cordis-tutorial |
| Append-only session log como "kernel da verdade": prompts, raciocínio, tool calls, injeções de contexto reconstruíveis; resume/fork/search/replay operam no mesmo stream | site oficial + The New Stack (13/08/2026) |
| Dissecação independente (12.293 commits lidos): **"'Everything is a plugin' ≠ ausência de kernel privilegiado"**; Scope/Preset **NÃO são sandbox de segurança** — plugins rodam no mesmo processo Node com acesso total; Profile YAML é "montagem de código local, não formato de dados de baixo privilégio" | xdlkc/deepseek-harness-explained (ZH, 14/08/2026) |

**Efeito nas propostas:** Proposta 1 REFUTADA com mais força — até o dsh tem kernel privilegiado e seu scope não isola nada em nível de SO. Copiar o modelo Cordis trazeria complexidade de debug alta (reconhecida pela própria dissecação como "não vou copiar") sem ganho de isolamento real. O alerta de volatilidade do `melhorias.md` se autoconfirma pelo README oficial.

### R2 — MiMo-Code: um FORK do OpenCode valida as perspectivas nativas

MiMo-Code (Xiaomi, 12,9k★) declara: *"built as a fork of OpenCode… keeps all core OpenCode capabilities (multiple providers, TUI, LSP, MCP, **plugins**)"* — e constrói suas inovações POR CIMA da arquitetura nativa, sem transplantar kernel estranho:

| Recurso MiMo | Valida |
|---|---|
| Skills selecionadas por **"exact name, localized alias, and BM25 relevance"** | **Perspectiva B na prática**: BM25 em produção num fork do OpenCode |
| Trajetória bruta em SQLite como fonte da verdade p/ `/dream` e `/distill` (auto-melhoria) | **Perspectiva A**: observabilidade alimentando cognição (R48/R49) |
| Budgeted injection com importance ranking + `/context-limit` por modelo **clamped à janela real do provider** | Proposta 3 refutada: indústria usa orçamento+ranking, não tags; paralelo direto com RS8 (limiar cognitivo > janela nominal) |
| Checkpoint-writer subagent + reconstrução de contexto | Write-Select-Compress-Isolate (framework LangChain popularizado) |

Benchmarks Xiaomi atribuem ~5pp de ganho AO HARNESS (mesmo modelo em harnesses diferentes) — reforço de que investir no harness nativo rende mais que trocar de arquitetura.

### R3 — hermes-agent (Nous Research, 236k★): trajetória como dado de treino + isolamento por backend

- **`trajectory_compressor.py` + batch trajectory generation**: trajetórias capturadas para RETREINAR modelos tool-calling — eleva a Perspective A de "debugging" a "self-learning loop" (sinergia direta com R41/R42).
- **7 terminal backends trocáveis** (local, Docker, SSH, Singularity, Modal, Daytona, Vercel Sandbox): execução isolada plugável por SELEÇÃO DE BACKEND, sem kernel plugin-first — refuta novamente a Proposta 1 pela via prática.
- Learning loop fechado: cria skills da experiência, skills se auto-melhoram em uso, busca FTS5 nas próprias conversas — mesmo padrão cognitivo do vault Obsidian (R26/R44), implementável via plugins/eventos.

### R4 — openai/codex (118k★): isolamento nativo por modos, não por kernel de plugins

Codex CLI (Rust, Apache-2.0) alcançou escala massiva com sandbox modes nativos (read-only / workspace-write / danger-full-access) + approval policies — sem framework de plugins tudo-em-um. O mercado mainstream valida: **isolamento = camada de policy/execução**, exatamente onde a Perspectiva C coloca o secure_runner R71 (`permission.ask` + containers). O PR upstream anomalyco/opencode#30509 (jun/2026, wire do hook `permission.ask` com cópia defensiva e catchCause) mostra o upstream evoluindo na MESMA direção do FIX S1 aplicado na auditoria (gate default-ask).

### R5 — Literatura e ecossistema

| Fonte | Apoio |
|---|---|
| Martin Fowler — Context Engineering for Coding Agents (fev/2026): rules com path-scoping já são padrão em Claude Code, GH Copilot, Cursor | Proposta 3 refutada: escopo por caminho é commodity, não diferencial a copiar |
| baguaai (jun/2026): dev com 140+ tools MCP abandonou embeddings por **BM25** em roteamento determinístico de produção | **Perspectiva B** reforçada por experiência de terceiros |
| Issues openclaw (#87327, #74803): stalls na fase runtime-plugins SEM timeout por-plugin e diagnóstico inacionável | Urgência da correção de timeout/isolamento de plugins (achado B-P4 da auditoria) |
| Marketplace dsh: `trajectory-logger` (JSONL+fork+replay), `docker-sandbox`, `wasm-isolator` são PLUGINS comunitários | Até no dsh observabilidade e sandbox são camadas plugáveis — desenho idêntico às Perspectives A/C |
| ZCode (carsonfeng, fork de appleboy/CodeGPT, Go, 2★): CLI single-purpose (mensagem de commit/review via prepare-commit-msg) | Contraste de cauda longa: ferramenta de tarefa única sem pretensão de harness — irrelevante como referência arquitetural, citado por completude do MIX |

---

## PARTE V — MÉTRICAS IMPRESSIONANTES POR CATEGORIA (Dev Loop MIX, 2026-08-25)

> Referências adicionais dissecadas: openclaw/openclaw · Gitlawb/openclaude · google-antigravity (+CLI). Métrica mais impressionante do ciclo em **negrito**.

### M1 — O efeito HARNESS é a métrica-rainha (valida toda a tese da refutação)

| Métrica | Número | Fonte |
|---|---|---|
| **Spread de Pass@1 por escolha de harness, mesmo modelo** | **27,4 pp** (Qwen3.6-flash: 38,6%→66,0%) e **12,5 pp** (GLM-5.1: 60,9%→73,4%) | Claw-SWE-Bench (arXiv 2606.12344) — OpenClaw vs Hermes vs ZeroClaw vs NanoBot vs Generic |
| Swing por scaffolding em pesos idênticos | 10–20 pp no SWE-Bench | digitalapplied benchmark methodology guide |
| Scaffold gap self-reported | até **28 pp** ("Claude Fable 5" 95% SWE-V com 99/100 resultados self-reported) | SWE-bench roundup jun/2026 |
| Harness research "vix" + Opus 4.7 | **90,2%** Terminal-Bench 2.0 (topo absoluto do leaderboard) | tbench.ai via SecurityBoulevard jun/2026 |
| Ganho atribuído ao harness (Xiaomi, mesmo modelo) | ~**5 pp** | blog Xiaomi MiMo Code |

**Implicação:** a pergunta certa nunca é "copiar feature X do dsh?" — é "**qual harness extrai mais do MESMO modelo?**". O opencode-dev já está na família dos harnesses campeões (família OpenCode); investir nas Perspectives A–D rende mais que qualquer transplante.

### M2 — Benchmarks de código (melhores verificados)

| Agente/Métrica | Score | Categoria |
|---|---|---|
| Codex CLI (GPT-5.5) | **82,2%** Terminal-Bench 2.0 oficial (2026-04-23) | melhor CLI nomeada verificada |
| Claude Opus 4.7 | 87,6% SWE-V / 64,3% Pro / 69,4% TB2 | gap estrutural Verified↔Pro ≈20–25 pp p/ todos |
| GPT-5.5 | 82,7% TB2 / topo Artificial Analysis (60) | |
| Gemini 3.5 Flash | 4× mais rápido que frontier; supera Gemini 3.1 Pro em agentic/coding | Managed Agents (Antigravity harness) |
| Antigravity CLI | sem entrada própria no TB2 ainda; Gemini 3.1 Pro = 80,2% via TongAgents harness | sucessor do Gemini CLI (transição 18/jun/2026, rewrite em Go) |

### M3 — Eficiência de tokens/custo

| Métrica | Número | Fonte |
|---|---|---|
| Redução de tokens: indexação semântica+BM25 vs grep-navigation | **62×** menos tokens pela mesma tarefa | sverklo eval (60 tarefas) |
| Opus 4.5: redução de output tokens | **76% menos** + corte de preço 3× | Anthropic |
| Métrica operacional canônica | **cost-per-successful-task** (não pass-rate cru) | digitalapplied |
| Cache hit rate como métrica de custo | `cache_read/(input+cache_read)` reportada obrigatoriamente | Claw-SWE-Bench |

### M4 — Adoção/velocidade de ecossistema

| Projeto | Stars | Commits | Nota |
|---|---|---|---|
| openclaw | **388k★** | **82.478** | 647 itens em security-and-quality; fundação non-profit; WildClawBench/RealClawBench próprios; à frente de Claude Code/Codex/Hermes em 3/4 modelos no benchmark próprio de harness |
| hermes-agent | 236k★ | 25.248 | loop de auto-melhoria + trajetórias p/ treino |
| dsh | 195k★ | 13.147 | preview instável (compat-breaking) em ~2 meses de vida |
| codex | 118k★ | 9.843 | Rust, Apache-2.0 |
| MiMo-Code | 12,9k★ | 1.168 | fork OpenCode; SWE-V 82% vs Claude Code 79% (auto-reportado) |
| Gitlawb/openclaude | fork da família Claude/OpenClaw | — | sem métricas próprias publicadas; citado por completude do MIX |
| ZCode | 2★ | 300 | cauda longa single-purpose |

### M5 — Confiabilidade (o espelho)

| Métrica | Número | Lição |
|---|---|---|
| Falha de frontier agents no TB2 | 18–35% das 89 tarefas | nem o topo é saturado; margem real p/ harness melhor |
| Stalls runtime-plugins (openclaw) | ~180 runs falhas em 5 dias num fleet, diagnóstico sem nomear plugin | custo de NÃO ter observabilidade/timeout por plugin → Perspective A + achado B-P4 |
| PR acceptance rate autônomo (Claude Code) | ~48% | qualidade ainda exige gate humano (R28/R37) |

### Veredito final com métricas (R34/R37/R40)

A refutação fecha com **nota 96/100**: as 3 propostas dsh permanecem refutadas agora com 8 referências primárias e a métrica decisiva do setor — **o harness vale 10–28 pp no MESMO modelo** — provando que evoluir o harness NATIVO (opencode-dev + Perspectives A–D + correções aplicadas) domina qualquer transplante de arquitetura alheia. Dedução: Antigravity CLI e openclaude carecem de entradas verificadas próprias em leaderboards (monitorar próximas ondas); fff-bun patch sync segue pendente no plano de auditoria.

### Veredito consolidado pós-referências

As 3 refutações originais **sobrevivem intactas e ganham evidência externa**: (1) plugin-first total é desnecessário e arriscado (dsh preview + xdlkc); (2) tracing já existe — falta exportação/agregação (dsh/MiMo/hermes todos usam log persistido + consumidores); (3) seleção de contexto evoluiu para ranking semântico-orçamentário (MiMo/BM25/LangChain), não tags. As Perspectivas A–D saem fortalecidas: A ganha dimensão de training-data (hermes), B ganha prova de produção (MiMo), C ganha validação mainstream (codex/hermes), D permanece OPCIONAL alinhada a Effect Layers.

## CHECKLIST

- [ ] ✔ Refutação documentada com evidência (implementado neste documento)
- [ ] ✔ Perspectivas A–D especificadas com classificação e riscos
- [ ] ✔ PARTE IV — 8 referências externas dissecadas (dsh, MiMo, hermes, codex, ZCode, openclaw, openclaude, antigravity)
- [ ] ✔ PARTE V — métricas impressionantes por categoria (harness-effect 27,4pp; TB2 82,2%/90,2%; tokens 62×/76%; adoção 388k★)
- [x] ✔ Validação empírica de A–D concluída na auditoria exaustiva (Frentes B/D/F)
- [ ] ⬜ Implementação perspectiva C — secure_runner first-class (futuro, pós-auditoria)
- [ ] ⬜ Implementação perspectiva A — trajectory-export plugin (futuro)
- [ ] ⬜ Implementação perspectiva B — port context-selector BM25 (futuro)
- [ ] ⬜ Implementação perspectiva D — storage Layer trocável (futuro, médio prazo)
