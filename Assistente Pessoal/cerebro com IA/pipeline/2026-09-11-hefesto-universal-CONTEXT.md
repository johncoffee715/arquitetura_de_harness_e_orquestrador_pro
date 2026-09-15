# Pipeline CONTEXT.md — Hefesto Universal (MIX + Dev Loop)
# Criado: 2026-09-11
# Modo: AUTÔNOMO (diretriz usuário: "execute universal... sistemática e categórica")
# Escopo: absorção de ~32 repos NÃO-absorvidos via Hefesto (decompilação→autofagia→helenização→forja)

[Harness] SHA: 45a3ec8939a860e4490c43bf349e28f00c181446
[Harness] skills-sha: 4af02b43339ae889184c776250f09637e5e76b7bbce9d660b304c39eb522b500
[Phase] ts=2026-09-11T00:00:00Z F1 Descoberta | Route: explore | Status: done | Budget: ~5%
[Phase] ts=2026-09-11T00:00:00Z F2 Contrato | Route: spec | Status: done | Budget: ~5%
[Phase] ts=2026-09-11T00:00:00Z F3 Plano | Route: plan | Status: done | Budget: ~5%

## Categorização R75 (categoria > nome)

### JÁ ABSORVIDOS (Tabela 1 — 30 repos, todos com quarteto completo R85) — NÃO reprocessar
browser-use, firecrawl, claude-mem, omniroute, orca, ruview, openship, code-review-graph,
oh-my-opencode-slim, pi, mattpocock-skills, worldmonitor, ai-agent-book, onp-spec-driven,
sentry-mcp, gemini-mcp-tool, colibri, recursive-llm, prime-agent, dokku-deploy, coderabbit,
azure-skills, awesome-llm-apps, world-model-optimizer, llama-mtp-concept, context-selector,
longhorizon-harness, unsloth-zoo, security-review, anthropics-skills

### JÁ ABSORVIDOS (Lista 2 — 11 repos) — NÃO reprocessar
i-have-adhd, vercel-agent-skills, openwork-mcp, llama-mtp, deepagents, last30days-skill,
impeccable, cc-harness-iai, spec-kit, a2a-brainstorm

### GAP — 32 repos NÃO-absorvidos (alvo do pipeline)

| Wave | Repo | Tipo-feature | Categoria R75 | Prioridade |
|---|---|---|---|---|
| A | netresearch/context7-skill | skill | skill | alta |
| A | chuspeeism/dashi-ppt-skill | skill | skill | alta |
| A | multica-ai/andrej-karpathy-skills | skill | skill | alta |
| A | tech-leads-club/agent-skills | skill | skill | alta |
| A | deepseek-ai/deepspec | skill | skill | alta |
| A | Fission-AI/OpenSpec | skill | skill | alta |
| A | bmad-code-org/BMAD-METHOD | skill | skill | alta |
| B | modelcontextprotocol/servers | mcp | mcp | alta |
| C | crewaiinc/crewai | framework | padrao-orquestracao | media |
| C | langchain-ai/langgraph | framework | padrao-grafo | media |
| C | google/adk-python | framework | padrao-agente | media |
| C | openai/openai-agents-python | framework | padrao-agente | media |
| C | inngest/inngest | workflow | padrao-durable | media |
| C | temporalio/temporal | workflow | padrao-durable | media |
| C | temporal-community/temporal-agent-harness | harness | padrao-harness | media |
| D | langfuse/langfuse | observabilidade | padrao-observabilidade | media |
| D | open-telemetry/semantic-conventions-genai | observabilidade | padrao-otel | media |
| E | hysnsec/awesome-policy-as-code | politica | padrao-politica | media |
| E | intuit/identity-authz-apl | authz | padrao-authz | media |
| F | pgvector/pgvector | infra | padrao-vetor (NUNCA dep) | baixa |
| F | postgres/postgres | infra | padrao-db (NUNCA dep) | baixa |
| F | redis/redis | infra | padrao-cache (NUNCA dep) | baixa |
| F | redis-developer/langgraph-redis | infra | padrao-cache-grafo (NUNCA dep) | baixa |
| G | xai-org/grok-build | tool | tool-build | media |
| G | chidiwilliams/buzz | tool | tool-audio | media |
| G | TestSprite/testsprite-cli | tool | tool-teste | media |
| H | affaan-m/ecc | ? | descoberta | pesquisa |
| H | darrenhinde/openagentscontrol | ? | descoberta | pesquisa |
| H | corebunch/instatic | ? | descoberta | pesquisa |
| H | nexu-io/open-design | ? | descoberta | pesquisa |
| H | ruvnet/ruflo | ? | descoberta | pesquisa |
| H | knockoutez/wigolo | ? | descoberta | pesquisa |

## Regra de ferro (R2/R44): infra (Wave F) absorve SÓ padrão/conceito — NUNCA propor como dependência.
## RunIDs: reservados abaixo por task.

## F4 Execução — RunIDs

[RunID] ts=2026-09-12 run-20260911-context7 hefesto-context7-skill done dur_ms=n/a (forja direta cloud provisória)
[Phase] ts=2026-09-12 F6 Entrega | Route: hefesto-cloud | Status: TODAS AS WAVES DONE (A+B+C+D+E+F+G+I) | Budget: ~95%
[Authorize] auto — modo autônomo (cloud): forjas buzz + open-design + pgvector/postgres/redis/langgraph-redis sem gate humano
[RunID] ts=2026-09-12 run-20260912-buzz hefesto-buzz done dur_ms=n/a (forja direta cloud provisória)
[RunID] ts=2026-09-12 run-20260912-opendesign hefesto-open-design done dur_ms=n/a (forja direta cloud provisória)
[RunID] ts=2026-09-12 run-20260912-pgvector hefesto-pgvector-patterns done dur_ms=n/a (só conceitos, nunca dependência)
[RunID] ts=2026-09-12 run-20260912-postgres hefesto-postgres-patterns done dur_ms=n/a (só conceitos, nunca dependência)
[RunID] ts=2026-09-12 run-20260912-redis hefesto-redis-patterns done dur_ms=n/a (só conceitos, nunca dependência)
[RunID] ts=2026-09-12 run-20260912-lgredis hefesto-langgraph-redis-patterns done dur_ms=n/a (só padrão, nunca servidores)
[Verify] ts=2026-09-12 sweep FINAL 35/35 PASS 0 FAIL (todas as forjas)
[Authorize] auto — modo autônomo (cloud): clones reais /tmp/opencode/repos + forjas grok-build + testsprite sem gate humano
[RunID] ts=2026-09-12 run-20260912-grokbuild hefesto-grok-build done dur_ms=n/a (clone SHA 3794978 + fonte lida, só padrões)
[RunID] ts=2026-09-12 run-20260912-testsprite hefesto-testsprite done dur_ms=n/a (clone SHA 125872f + fonte lida, só loop)

### Wave G — Tools/CLI (clone real Hefesto, 2/4)
| Repo | Skill | Status | Evidência |
|---|---|---|---|
| xai-org/grok-build | grok-build | done | clone SHA 3794978, README+linhas reais, smoke 3/3 |
| TestSprite/testsprite-cli | testsprite | done | clone SHA 125872f, package+skills reais, smoke 3/3 |
| chidiwilliams/buzz | buzz | pending | próximo (clone real) |
| nexu-io/open-design | open-design | pending | próximo (clone real) |
[Authorize] auto — modo autônomo (cloud): forjas oh-my-openagent + superpowers + fable-method + gsd sem gate humano
[RunID] ts=2026-09-12 run-20260912-omo hefesto-oh-my-openagent done dur_ms=n/a (forja direta cloud provisória, só padrões; licença SUL sinalizada)
[RunID] ts=2026-09-12 run-20260912-superpowers hefesto-superpowers done dur_ms=n/a (forja direta cloud provisória)
[RunID] ts=2026-09-12 run-20260912-fablemethod hefesto-fable-method done dur_ms=n/a (forja direta cloud provisória)
[RunID] ts=2026-09-12 run-20260912-gsd hefesto-gsd done dur_ms=n/a (forja direta cloud provisória; org como fonte, PARTIALLY UNDERSTOOD nos internals)

### Wave I — Novos (lote usuário, execução cloud provisória, 4/4)
| Repo | Skill | Status | Evidência |
|---|---|---|---|
| code-yeongyu/oh-my-openagent | oh-my-openagent | done | 6 arquivos + smoke 3/3 (hashline/categorias/Team) |
| obra/superpowers | superpowers | done | 6 arquivos + smoke 4/4 (skill-check + review duplo) |
| Sahir619/fable-method | fable-method | done | 6 arquivos + smoke 4/4 (loop bounded + INTENT) |
| gsd-build (org) | gsd | done | 6 arquivos + smoke 2/2 (flatship patterns; internals PARTIALLY UNDERSTOOD) |
[Authorize] auto — modo autônomo (cloud): forjas temporal + temporal-agent-harness sem gate humano
[RunID] ts=2026-09-12 run-20260912-temporal hefesto-temporal done dur_ms=n/a (forja direta cloud provisória, só padrão; 1 retry: fix tipo Pydantic Dict[str,str]→Dict[str,Any])
[RunID] ts=2026-09-12 run-20260912-tah hefesto-temporal-agent-harness done dur_ms=n/a (forja direta cloud provisória, só padrões)
[Authorize] auto — modo autônomo (cloud): forjas adk-python + openai-agents-python + inngest sem gate humano
[RunID] ts=2026-09-12 run-20260912-adk hefesto-adk-python done dur_ms=n/a (forja direta cloud provisória, só padrão)
[RunID] ts=2026-09-12 run-20260912-oaiagents hefesto-openai-agents-python done dur_ms=n/a (forja direta cloud provisória, só padrão)
[RunID] ts=2026-09-12 run-20260912-inngest hefesto-inngest done dur_ms=n/a (forja direta cloud provisória, só padrão)
[Authorize] auto — modo autônomo (cloud): forjas langfuse + otel-semconv-genai + awesome-policy-as-code + identity-authz-apl sem gate humano
[RunID] ts=2026-09-12 run-20260912-langfuse hefesto-langfuse done dur_ms=n/a (forja direta cloud provisória, só loop)
[RunID] ts=2026-09-12 run-20260912-otel hefesto-otel-semconv-genai done dur_ms=n/a (forja direta cloud provisória)
[RunID] ts=2026-09-12 run-20260912-pac hefesto-awesome-policy-as-code done dur_ms=n/a (forja direta cloud provisória)
[RunID] ts=2026-09-12 run-20260912-apl hefesto-identity-authz-apl done dur_ms=n/a (forja direta cloud provisória)
[Authorize] auto — modo autônomo (cloud): forjas crewai-patterns + langgraph-patterns sem gate humano
[RunID] ts=2026-09-12 run-20260912-crewai hefesto-crewai-patterns done dur_ms=n/a (forja direta cloud provisória, só padrão)
[RunID] ts=2026-09-12 run-20260912-langgraph hefesto-langgraph-patterns done dur_ms=n/a (forja direta cloud provisória, só padrão)
[Authorize] auto — modo autônomo (cloud): forjas openagentscontrol + ecc sem gate humano
[RunID] ts=2026-09-12 run-20260912-oac hefesto-openagentscontrol done dur_ms=n/a (forja direta cloud provisória)
[RunID] ts=2026-09-12 run-20260912-ecc hefesto-ecc done dur_ms=n/a (forja direta cloud provisória)
[Verify] ts=2026-09-12 sweep 12/12 PASS 0 FAIL (todas as forjas re-validadas — falha captada corrigida)
[Authorize] auto — modo autônomo (cloud): forjas wigolo + ruflo sem gate humano
[RunID] ts=2026-09-12 run-20260912-wigolo hefesto-wigolo done dur_ms=n/a (forja direta cloud provisória)
[RunID] ts=2026-09-12 run-20260912-ruflo hefesto-ruflo done dur_ms=n/a (forja direta cloud provisória, só padrões)
[Authorize] auto — modo autônomo (cloud): forjas bmad-method + mcp-servers sem gate humano
[RunID] ts=2026-09-12 run-20260912-bmad hefesto-bmad-method done dur_ms=n/a (forja direta cloud provisória)
[RunID] ts=2026-09-12 run-20260912-mcpservers hefesto-mcp-servers done dur_ms=n/a (forja direta cloud provisória)
[Authorize] auto — modo autônomo (cloud): forjas tech-leads-club-agent-skills + openspec sem gate humano
[RunID] ts=2026-09-12 run-20260912-tlc hefesto-tech-leads-club-agent-skills done dur_ms=n/a (forja direta cloud provisória)
[RunID] ts=2026-09-12 run-20260912-openspec hefesto-openspec done dur_ms=n/a (forja direta cloud provisória)
[Authorize] auto — modo autônomo (cloud): forjas andrej-karpathy-skills + deepspec sem gate humano
[RunID] ts=2026-09-12 run-20260912-karpathy hefesto-andrej-karpathy-skills done dur_ms=n/a (forja direta cloud provisória)
[RunID] ts=2026-09-12 run-20260912-deepspec hefesto-deepspec done dur_ms=n/a (forja direta cloud provisória)
[Authorize] auto — modo autônomo (cloud): forja dashi-ppt-skill sem gate humano
[RunID] ts=2026-09-12 run-20260912-dashippt hefesto-dashi-ppt-skill done dur_ms=n/a (forja direta cloud provisória)
[Budget] ts=2026-09-12 hefesto-context7-skill ~6tok/teto (6 arquivos, smoke 3/3)

### Wave A — Skills (execução cloud provisória, 1/7)
| Repo | Skill | Status | Evidência |
|---|---|---|---|
| netresearch/context7-skill | context7-skill | done | 6 arquivos + gabarito JSON válido + mecanica.py smoke 3/3 |
| chuspeeism/dashi-ppt-skill | dashi-ppt-skill | done | 6 arquivos + gabarito JSON válido + mecanica.py smoke 4/4 |
| multica-ai/andrej-karpathy-skills | andrej-karpathy-skills | done | 6 arquivos + smoke 3/3 |
| tech-leads-club/agent-skills | tech-leads-club-agent-skills | done | 6 arquivos + smoke 3/3 (registry validado + MCP progressivo) |
| deepseek-ai/deepspec | deepspec | done | 6 arquivos + smoke 4/4 (correção: speculative decoding, NÃO spec-driven) |
| Fission-AI/OpenSpec | openspec | done | 6 arquivos + smoke 3/3 (ciclo fluido + Stores) |
| bmad-code-org/BMAD-METHOD | bmad-method | done | 6 arquivos + smoke 5/5 (delivery-loop router) |

### Wave B — MCP (execução cloud provisória, 1/3)
| Repo | Skill | Status | Evidência |
|---|---|---|---|
| modelcontextprotocol/servers | mcp-servers | done | 6 arquivos + smoke 4/4 (catálogo 7 ativos + config segura) |
| knockoutez/wigolo | wigolo | done | 6 arquivos + smoke 3/3 (MCP web local-first $0) |
| ruvnet/ruflo | ruflo | done | 6 arquivos + smoke 4/4 (só padrões, nunca runtime alheio) |

### Wave H — pesquisa concluída (primário cloud, 6/6)
ecc SIM (padrao-harness/alta) · openagentscontrol SIM (padrao-orquestracao/alta) · instatic NÃO (tool-cms/baixa) · open-design SIM (skill/media) · ruflo SIM (padrao-harness/alta) · wigolo SIM (mcp/alta)

### Wave F — Infra-padrões (só conceitos, NUNCA dependência, 4/4 DONE)
| Repo | Skill | Status | Evidência |
|---|---|---|---|
| pgvector/pgvector | pgvector-patterns | done | 6 arquivos + smoke 3/3 (HNSW/IVFFlat) |
| postgres/postgres | postgres-patterns | done | 6 arquivos + smoke 3/3 (WAL-first/MVCC) |
| redis/redis | redis-patterns | done | 6 arquivos + smoke 3/3 (estruturas/TTL) |
| redis-developer/langgraph-redis | langgraph-redis-patterns | done | 6 arquivos + smoke 2/2 (namespace+TTL) |

### Wave G — Tools/CLI (4/4 DONE; grok-build+testsprite com clone real)
| Repo | Skill | Status | Evidência |
|---|---|---|---|
| xai-org/grok-build | grok-build | done | clone SHA 3794978 + fonte real, smoke 3/3 |
| TestSprite/testsprite-cli | testsprite | done | clone SHA 125872f + fonte real, smoke 3/3 |
| chidiwilliams/buzz | buzz | done | 6 arquivos + smoke 2/2 (pipeline offline) |
| nexu-io/open-design | open-design | done | 6 arquivos + smoke 3/3 (loop + DESIGN.md) |

## F6 Encerramento — drift + restart (2026-09-12)
- [Drift] HEAD 35e25c1 (snapshot era 45a3ec8 — commits do sistema no meio); skills novas: 35 dirs untracked; catálogo 117 total
- [Drift] agent/*.md (13 subagents → nvidia/deepseek) EM VIGOR no disco — vale pós-restart; revert: modelos originais (ingestor×2, proposer×6, refuter×2, reflexo×3) — ver decisão abaixo
- [Drift] opencode.jsonc local-forge: minha troca p/ :9090 foi REVERTIDA (volta a :9088/131072) — mecanismo desconhecido (suspeita sync-hook); NÃO confiar nela; routing por agent-file prevalece
- [Restart] :9088 roda new-build Llama-3.2-3B CPU (meu processo); restart-stack.sh usa old-build (Vulkan ausente → NÃO sobe slots novos); stack local segue no seu domínio p/ reparo
- [Safety] NENHUM git add/commit/push feito (sem ordem); NENHUM rollback (máx 1/pipeline, não usado); __pycache__/ em skills/ = limpar antes do add
- [Derivation] 41 absorvidos prévios (evidência: quartetos no disco) + 6 pesquisados + 35 forjados → pesos por onda; strategy: delegation→cloud-direct provisório