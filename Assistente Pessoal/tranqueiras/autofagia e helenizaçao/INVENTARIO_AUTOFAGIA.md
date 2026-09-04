---
numero: AUTOFAGIA-INVENTARIO
tema: Inventário completo de autofagia e helenização — todas as fontes absorvidas
categoria: registro
setor: gran-mestre
escopo: harness
vigencia: 2026-08-25
fontes-de-dados: HISTORICO_AUTOFAGIA.md · AUTOFAGIA_9_REPOS.md · AUTOFAGIA_6_REPOS_2.md · AUTOFAGIA_26_ALVOS_R8.md · AUTOFAGIA_35_FONTES.md · AUTOFAGIA_R11_36_FONTES.md · proveniência nos SKILL.md instalados
tags: [autofagia, helenizacao, inventario, registry, links]
---

# INVENTÁRIO DE AUTOFAGIA — TODAS AS FONTES ABSORVIDAS

> Consolidado em 2026-08-25 pelo Gran-Mestre. Cada link abaixo tem evidência de
> absorção em pelo menos um registro desta sessão (grep nos relatórios + SKILL.md).
> Métrica de fecho histórica: **214+ padrões absorvidos** · registry v2.2 · 344+ entries.

---

## 1. RODADA INICIAL — 9 REPOSITÓRIOS (`AUTOFAGIA_9_REPOS.md` · 47 padrões)

| # | Fonte | Link | Padrões extraídos |
|---|---|---|---|
| 1 | Agent Skills Spec (Anthropic) | https://github.com/anthropics/skills | 8 |
| 2 | Everything Claude Code (ECC) | https://github.com/affaan-m/ecc | 12 |
| 3 | Context7 Skill | https://github.com/netresearch/context7-skill | 5 |
| 4 | OpenAgents Control | https://github.com/darrenhinde/openagentscontrol | 6 |
| 5 | I Have ADHD | https://github.com/ayghri/i-have-adhd | 4 |
| 6 | Dashi PPT Skill | https://github.com/chuspeeism/dashi-ppt-skill | 3 |
| 7 | Grok Build | https://github.com/xai-org/grok-build | 5 |
| 8 | Vercel Skills | https://github.com/vercel-labs/skills | 4 |
| 9 | Buzz | https://github.com/chidiwilliams/buzz | 2 |

## 2. RODADA 2 — 6 REPOSITÓRIOS (`AUTOFAGIA_6_REPOS_2.md` · 35 padrões)

| # | Fonte | Link | Padrões |
|---|---|---|---|
| 10 | Karpathy Skills | https://github.com/multica-ai/andrej-karpathy-skills | 5 |
| 11 | DeepSpec | https://github.com/deepseek-ai/deepspec | 4 |
| 12 | Instatic | https://github.com/corebunch/instatic | 6 |
| 13 | Open Design | https://github.com/nexu-io/open-design | 8 |
| 14 | Ruflo | https://github.com/ruvnet/ruflo | 7 |
| 15 | Wigolo | https://github.com/knockoutez/wigolo | 5 |

## 3. RODADA R8 — 26 ALVOS AVALIADOS, 4 ABSORVIDOS (`AUTOFAGIA_26_ALVOS_R8.md`)

| Fonte | Link | Virou |
|---|---|---|
| hallmark ⚠️ *URL não preservada* | *(pendente de rastreio)* | skill `hallmark` (design anti-slop) |
| book-to-skill ⚠️ *URL não preservada* | *(pendente de rastreio)* | skill `book-to-skill` (meta-skill) |
| openwork | https://github.com/different-ai/openwork | subagent `executor-deep` + MCP openwork |
| fallow ⚠️ *URL não preservada* | *(pendente de rastreio)* | subagents `fallow-mcp-reviewer` + `fallow-lsp-reviewer` |

## 4. RODADA R11 — 36 FONTES (`AUTOFAGIA_R11_36_FONTES.md`)

| Fonte | Link | Absorção |
|---|---|---|
| llama.cpp MTP | https://github.com/ggml-org/llama.cpp | feature PR #22673 (skill `llama-mtp`) |
| Anthropic Skills (reconf.) | https://github.com/anthropics/skills | catálogo oficial |
| DeepAgents | https://github.com/langchain-ai/deepagents | skill `deepagents` |
| Last30days | https://github.com/mvanhorn/last30days-skill | skill v3 adaptada |
| Impeccable | https://github.com/pbakaus/impeccable | skill + subagent |
| CC-Harness-IAI | https://github.com/elberrd/cc-harness-iai | skill task-master/sequencer |
| Spec Kit | https://github.com/github/spec-kit | skill `spec-kit` |
| Vercel Agent Skills | https://github.com/vercel-labs/agent-skills | react-best-practices etc. |
| Openwork (update) | https://github.com/different-ai/openwork | executor-deep atualizado |

## 5. LOTE "35 FONTES" — INFRA DE AGENTES (`AUTOFAGIA_35_FONTES.md` · 86 padrões helenizados em 10 áreas)

| Área temática | Links |
|---|---|
| Protocolos de agentes | https://github.com/a2aproject/A2A · https://github.com/modelcontextprotocol/servers |
| Orquestração/workflow | https://github.com/langchain-ai/langgraph · https://github.com/crewaiinc/crewai · https://github.com/google/adk-python · https://github.com/openai/openai-agents-python · https://github.com/bmad-code-org/BMAD-METHOD |
| Spec-driven | https://github.com/Fission-AI/OpenSpec · https://github.com/github/spec-kit *(dup R11)* |
| Execução durável | https://github.com/temporalio/temporal · https://github.com/temporal-community/temporal-agent-harness · https://github.com/inngest/inngest |
| Observabilidade | https://github.com/langfuse/langfuse · https://github.com/open-telemetry/semantic-conventions-genai |
| Storage/memória | https://github.com/pgvector/pgvector · https://github.com/redis/redis · https://github.com/redis-developer/langgraph-redis · https://github.com/postgres/postgres |
| Policy/authz | https://github.com/hysnsec/awesome-policy-as-code · https://github.com/intuit/identity-authz-apl |
| Testing/QA | https://github.com/TestSprite/testsprite-cli |
| Catálogos | https://github.com/tech-leads-club/agent-skills |

## 6. SKILLS HELENIZADOS INSTALADOS — PROVENIÊNCIA EXPLÍCITA NOS SKILL.md

| Skill local | Origem absorvida |
|---|---|
| browser-use | https://github.com/browser-use/browser-use |
| firecrawl | https://github.com/firecrawl/firecrawl |
| claude-mem | https://github.com/thedotmack/claude-mem |
| omniroute | https://github.com/diegosouzapw/OmniRoute |
| orca | https://github.com/stablyai/orca |
| ruview | https://github.com/ruvnet/RuView |
| openship | https://github.com/oblien/openship |
| code-review-graph | https://github.com/tirth8205/code-review-graph |
| oh-my-opencode-slim | https://github.com/alvinunreal/oh-my-opencode-slim |
| pi | https://github.com/earendil-works/pi |
| mattpocock-skills | https://github.com/mattpocock/skills |
| worldmonitor | https://github.com/koala73/worldmonitor |
| ai-agent-book | https://github.com/bojieli/ai-agent-book |
| onp-spec-driven | https://github.com/onovoprogramador/onp-spec-driven |
| sentry-mcp | https://github.com/getsentry/sentry-mcp |
| gemini-mcp-tool | https://github.com/jamubc/gemini-mcp-tool |
| colibri | https://github.com/JustVugg/colibri |
| recursive-llm | https://github.com/grishahq/recursive-llm |
| prime-agent | https://github.com/PrimeIntellect-ai/prime-agent |
| dokku-deploy | https://github.com/dokku/dokku |
| coderabbit | https://github.com/coderabbitai/awesome-coderabbit |
| azure-skills | https://github.com/microsoft/github-copilot-for-azure |
| awesome-llm-apps | https://github.com/Shubhamsaboo/awesome-llm-apps |
| world-model-optimizer | https://github.com/experientiallabs/world-model-optimizer |
| llama-mtp-concept | https://github.com/tryigit/cleveres-ai |
| context-selector | https://github.com/ratel-ai/ratel (+ ref. https://github.com/Ratel/Context-Engineering) |
| longhorizon-harness | https://github.com/AMAP-ML/LongHorizon-Harness |
| unsloth-zoo | https://github.com/unslothai/unsloth-zoo |
| security-review | https://github.com/anthropics/skills *(via catálogo oficial)* |

---

## 7. TABELA MESTRA DEDUPLICADA (~70 fontes únicas)

anthropics/skills · affaan-m/ecc · netresearch/context7-skill · darrenhinde/openagentscontrol · ayghri/i-have-adhd · chuspeeism/dashi-ppt-skill · xai-org/grok-build · vercel-labs/skills (= vercel-labs/agent-skills, provável rename) · chidiwilliams/buzz · multica-ai/andrej-karpathy-skills · deepseek-ai/deepspec · corebunch/instatic · nexu-io/open-design · ruvnet/ruflo · knockoutez/wigolo · different-ai/openwork · ggml-org/llama.cpp · langchain-ai/deepagents · mvanhorn/last30days-skill · pbakaus/impeccable · elberrd/cc-harness-iai · github/spec-kit · a2aproject/A2A · bmad-code-org/BMAD-METHOD · crewaiinc/crewai · Fission-AI/OpenSpec · google/adk-python · hysnsec/awesome-policy-as-code · inngest/inngest · intuit/identity-authz-apl · langchain-ai/langgraph · langfuse/langfuse · modelcontextprotocol/servers · openai/openai-agents-python · open-telemetry/semantic-conventions-genai · pgvector/pgvector · postgres/postgres · redis-developer/langgraph-redis · redis/redis · tech-leads-club/agent-skills · temporal-community/temporal-agent-harness · temporalio/temporal · TestSprite/testsprite-cli · browser-use/browser-use · firecrawl/firecrawl · thedotmack/claude-mem · diegosouzapw/OmniRoute · stablyai/orca · ruvnet/RuView · oblien/openship · tirth8205/code-review-graph · alvinunreal/oh-my-opencode-slim · earendil-works/pi · mattpocock/skills · koala73/worldmonitor · bojieli/ai-agent-book · onovoprogramador/onp-spec-driven · getsentry/sentry-mcp · jamubc/gemini-mcp-tool · JustVugg/colibri · grishahq/recursive-llm · PrimeIntellect-ai/prime-agent · dokku/dokku · coderabbitai/awesome-coderabbit · microsoft/github-copilot-for-azure · Shubhamsaboo/awesome-llm-apps · experientiallabs/world-model-optimizer · tryigit/cleveres-ai · ratel-ai/ratel · Ratel/Context-Engineering · AMAP-ML/LongHorizon-Harness · unslothai/unsloth-zoo

## 8. FONTES SEM LINK PRESERVADO (dívida de proveniência)

| Nome registrado | Rodada | Status |
|---|---|---|
| hallmark | R8 | skill ativo; owner/repo original não registrado |
| book-to-skill | R8 | skill ativo; origem não registrada |
| fallow | R8 | subagents ativos; origem não registrada |

**Ação sugerida:** rastreio retroativo dos 3 URLs ausentes para fechar a métrica de proveniência.

## 9. HISTÓRICO DE EXECUÇÃO DAS RODADAS

R-inicial (9 repos) → R2 (6 repos) → R8 (26 alvos, 2026-08-03) → R8-B (helenize_deploy.py + ECC v2, 2026-08-04) → R9 (context-selector + dokku, 2026-08-04) → R10..R10-F (autofagia do próprio harness + regras globais, 2026-08-04) → R11 (36 fontes + MTP llama.cpp, 2026-08-04) → lote 35 fontes (86 padrões).

---

*Método: autofagia = digestão crítica de fontes externas; helenização = transformação (nunca cópia). Sinapses: [[concepts/antropofagia-tecnologica]] · [[entities/gran-mestre]] · [[aprendizados/2026-07-29_autofagia-35-fontes]]*
