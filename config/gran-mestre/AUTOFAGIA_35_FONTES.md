---
name: autofagia-35-fontes
description: "Autofagia massiva de 35+ fontes externas (vídeos, repositórios, documentações). Pipeline MIX com 8 librarian agents paralelos. Helenização de padrões para o Gran-Mestre."
mode: skill
origin: autofagia:35-fontes
metadata:
  category: meta-integration
  version: 1.0.0
  author: Gran-Mestre (pipeline MIX — 8 librarian workers paralelos)
  sources: 35+
  patterns: 86
  purpose: "Self-learning massivo — absorver padrões de 10 ecossistemas distintos"
---

# AUTOFAGIA — 35+ Fontes

## Visão Geral

| # | Área | Fontes | Padrões | Status |
|---|------|--------|---------|--------|
| 1 | MCP Ecosystem | 3+ (servers, SDKs, OpenAPI→MCP) | 9 | ✅ |
| 2 | OpenTelemetry GenAI | 2+ (spec, docs) | 8 | ✅ |
| 3 | A2A Protocol | 2+ (spec, SDK, APL) | 8 | ✅ |
| 4 | pgvector | 1+ (repo + architecture) | 8 | ✅ |
| 5 | Temporal + Redis + Inngest | 5+ (repos + docs) | 8 | ✅ |
| 6 | ADK + CrewAI + LangGraph + OpenAI SDK | 4+ (repos) | 10 | ✅ |
| 7 | Langfuse + TestSprite + BMad Method | 3+ (repos + docs) | 7 | ✅ |
| 8 | OpenSpec + AgentSkills + SpecKit | 5+ (repos + docs) | 10 | ✅ |
| 9 | PostgreSQL Core | 1+ (repo + internals) | 10 | ✅ |
| 10 | Pinecone | 2+ (repo + docs) | 8 | ✅ |

**Total: 86 padrões extraídos de 35+ fontes**

---

## 1. MCP ECOSYSTEM — Servidores, SDKs, OpenAPI→MCP

### Fontes
- https://github.com/modelcontextprotocol/servers (89k★)
- https://mcpservers.org/ (9.800+ servidores catalogados)
- OpenAPI→MCP bridge tools

### Padrões Extraídos (9)

| # | Padrão | Descrição | Helenização para Gran-Mestre |
|---|--------|-----------|------------------------------|
| 1.1 | **Stateless Protocol** | MCP é stateless — toda requisição carrega `_meta` com versão + capabilities. Discovery é opcional e cacheável. | Gran-Mestre pode adotar discovery cacheável de sub-agents em vez de registry fixo |
| 1.2 | **Streamable HTTP (2026)** | Novo padrão de transporte. POST + chunked responses. SSE deprecated. | Se Gran-Mestre expor API externa, usar Streamable HTTP |
| 1.3 | **Três Primitivas** | Tools (callables), Resources (data), Prompts (templates) | Separar tools (ações de agente), resources (estado), prompts (templates de task) |
| 1.4 | **Tool Surface Pequena** | 5-10 tools por server v1. Cada tool custa ~200 tokens/turno | Manter número pequeno de rotas de delegação; cada sub-agent expõe toolset limitado |
| 1.5 | **Structured Content + Text** | Sempre retornar ambos: texto pro LLM, JSON pra aplicação | Sub-agents devem retornar resultado natural + structured data |
| 1.6 | **Gateway Pattern** | Gateway centraliza authN/Z, roteamento, rate limiting, OPA policy | Gran-Mestre já é o gateway — formalizar com Policy-as-Code |
| 1.7 | **Stateful Handle** | MCP é stateless no wire, estado via handles explícitos (UUIDv4 com TTL) | Sessions do Gran-Mestre como handles stateful |
| 1.8 | **OpenAPI→MCP Bridge** | 270+ servidores convertem OpenAPI em tools MCP | Gran-Mestre pode importar specs de API como novos sub-agents automaticamente |
| 1.9 | **Tool Naming** | Tool names começam com verbo (list_users ✅, users ❌), descrições de 1 sentença | Padronizar nomes de sub-agents como verbo + domínio |

---

## 2. OPENTELEMETRY GENAI — Tracing, Spans, Métricas

### Fontes
- https://github.com/open-telemetry/semantic-conventions-genai
- Documentação OTel, Greptime blog, Agent MarketCap

### Padrões Extraídos (8)

| # | Padrão | Descrição | Helenização para Gran-Mestre |
|---|--------|-----------|------------------------------|
| 2.1 | **Árvore de Spans** | `invoke_agent → chat/LLM → execute_tool → chat/LLM`. Cada chamada de LLM e tool é span filho | Gran-Mestre: `pipeline → fase → agente → tool_call` como hierarquia de spans |
| 2.2 | **MCP Trace Propagation** | W3C Trace Context entre MCP client e server | Propagar trace_id entre fases do pipeline para debugging cross-fase |
| 2.3 | **Três Modos de Content Capture** | Não capturar (prod), atributos no span (dev), external storage + URL (recomendado) | Usar external storage para prompts/outputs em produção |
| 2.4 | **Métricas Essenciais** | `gen_ai.client.operation.duration`, `token.usage`, `time_to_first_chunk`, `gen_ai.invoke_agent.duration` | Adicionar métricas de duração por fase do pipeline e por sub-agent |
| 2.5 | **Workflow Metrics** | `gen_ai.workflow.duration`, `gen_ai.invoke_agent.inference_calls`, `gen_ai.invoke_agent.tool_calls` | Métricas de quantas chamadas de modelo e tools por pipeline |
| 2.6 | **Agent Attributes** | `gen_ai.agent.name`, `gen_ai.conversation.id`, `gen_ai.tool.name` | Padronizar atributos de observabilidade no CONTEXT.md |
| 2.7 | **GenAI Semconv Registry** | 6 camadas de especificação (spans → agent → MCP → events → metrics → providers) | Structurar observabilidade do Gran-Mestre seguindo as 6 camadas |
| 2.8 | **20+ Providers Registrados** | OpenAI, Anthropic, DeepSeek, Mistral, Groq, Perplexity, xAI, etc. | Suportar múltiplos providers com tracing consistente |

---

## 3. A2A PROTOCOL — Comunicação Inter-Agentes

### Fontes
- https://github.com/a2aproject/A2A (~25k★)
- https://github.com/intuit/identity-authz-apl
- Documentação A2A protocol

### Padrões Extraídos (8)

| # | Padrão | Descrição | Helenização para Gran-Mestre |
|---|--------|-----------|------------------------------|
| 3.1 | **Agente Opaco (Black-Box)** | Agentes não expõem memória interna, ferramentas ou estado. Comunicação via mensagens padronizadas | Sub-agents do Gran-Mestre devem ser opacos — só expõem interface padronizada |
| 3.2 | **Task Stateful com Ciclo de Vida** | Task: submitted → working → input-required → completed/failed/canceled | Pipeline do Gran-Mestre segue o mesmo ciclo de vida de task |
| 3.3 | **Agent Card Discovery** | `/.well-known/agent-card.json` com identidade, capacidades, auth schemes, skills | Cada sub-agent expõe "card" com capacidades e schemas |
| 3.4 | **Três Modos de Interação** | Request/Response (curto), Streaming SSE (incremental), Push Notification (longo) | Gran-Mestre: modo síncrono (request/response) para tasks curtas, modo streaming (eventos) para pipelines longas |
| 3.5 | **A2A + MCP Complementares** | A2A = agente↔agente, MCP = agente↔ferramenta | Gran-Mestre usa A2A para delegar entre sub-agents, MCP para tools |
| 3.6 | **OAuth2 + RBAC para Agentes** | 6 SecuritySchemes: apiKey, http, oauth2, OIDC, mTLS. 3 flows OAuth2 | Gran-Mestre deve suportar autenticação entre sub-agents via OAuth2 client_credentials |
| 3.7 | **Skill-Based Authorization** | OAuth scopes controlam quais skills um agente-cliente pode invocar | Skills do Gran-Mestre (Héstia, Atena) protegidas por scopes |
| 3.8 | **ABAC Policy Language** | Intuit APL: engine RETE ~20μs, <1KB heap, determinístico | Policy-as-Code para gates do pipeline com tempo de execução previsível |

---

## 4. PGVECTOR — Indexação Vetorial, Extensões PG

### Fontes
- https://github.com/pgvector/pgvector (22.4k★, v0.8.5)
- Documentação e DeepWiki

### Padrões Extraídos (8)

| # | Padrão | Descrição | Helenização para Gran-Mestre |
|---|--------|-----------|------------------------------|
| 4.1 | **Extension Pattern + Migration Chain** | SQL incremental migrations (`vector--X.Y.Z--A.B.C.sql`) para versionar capability surface | Capabilities do Gran-Mestre versionadas como migrações atômicas |
| 4.2 | **Plugin Interface via Handler Struct** | HNSW e IVFFlat implementam mesma interface `IndexAmRoutine` | Definir trait Plugin com `init/execute/validate/cleanup` para sub-agents |
| 4.3 | **Dois Níveis de Precisão** | Exato (100% recall, scan linear) vs Aproximado (HNSW, speed tradeoff) | Pipeline tem modo debug/exato e produção/aproximado |
| 4.4 | **Lazy Training vs Instant Index** | IVFFlat precisa de warm-up (k-means), HNSW funciona cold-start | Componentes do Gran-Mestre: cold-start ready vs warm-up needed |
| 4.5 | **Re-Ranking em Duas Etapas** | Coarse (busca barata) → Refine (re-ordenação cara) | Dois estágios de avaliação: filtro rápido → LLM caro |
| 4.6 | **Parallel Build com Shared State** | `HnswShared` com `slock_t`, `ConditionVariable`, `LWLock` para construção paralela | Worker pool com barreira e estado compartilhado |
| 4.7 | **Multi-Tenancy via Partitioning** | List partitioning por tenant para isolar embeddings | Isolar contextos de agente/usuário via partições |
| 4.8 | **Debugging Instrumentado** | Macros condicionais `#ifdef HNSW_BENCH` para tracing em debug, zero overhead em prod | Feature flags para instrumentação, não condicionais de runtime |

---

## 5. TEMPORAL + REDIS + INNGEST — Execução Durável

### Fontes
- https://github.com/temporalio/temporal
- https://github.com/temporal-community/temporal-agent-harness
- https://github.com/inngest/inngest
- https://github.com/redis-developer/langgraph-redis
- https://github.com/redis/redis

### Padrões Extraídos (8)

| # | Padrão | Descrição | Helenização para Gran-Mestre |
|---|--------|-----------|------------------------------|
| 5.1 | **Workflow/Activity Separation** | Código determinístico (orquestração) vs não-determinístico (I/O, LLM). Activities com retry automático | Separar lógica de orquestração (determinística) de execução de sub-agents (não-determinística) |
| 5.2 | **Agent-as-Workflow** | Cada agente = Workflow Temporal. Tools = Activities. Survive crashes, retomada exata | Cada pipeline do Gran-Mestre = workflow durável. SHA antes de executar = checkpoint |
| 5.3 | **Delta State (só persista o que mudou)** | LangGraph DeltaChannel: armazena só sentinel no checkpoint, reconstrói via replay do reducer | Estado do pipeline: só persistir deltas entre fases, não estado completo |
| 5.4 | **Cache Hierarchy para LLM/Tools** | SemanticCache → ToolResultCache → ConversationMemory → SemanticRouter | Cache hierárquico de resultado de sub-agents baseado em metadados |
| 5.5 | **Code Mode** | Tool única que executa script Python com loops, condicionais, `asyncio.gather` | Tool de "modo script" para sub-agents fazerem múltiplas operações em 1 round-trip |
| 5.6 | **Strongly-Typed Agent Interfaces** | Agentes expõem operações tipadas (Pydantic). Composição programática real | Sub-agents do Gran-Mestre com schemas de entrada/saída tipados |
| 5.7 | **Três Camadas de Estado** | Short-term (contexto, não persistido) → Mid-term (sessão, checkpoints) → Long-term (conhecimento, stores vetoriais) | Gran-Mestre: contexto da fase (short), sessão do pipeline (mid), memória compartilhada (long) |
| 5.8 | **Outbox Pattern para Mutations** | Agent escreve intent → Transação → Dispatcher publica. Se crasha, outbox mantém registro | Pipeline escreve intent antes de executar, permite exactly-once |

---

## 6. ADK + CREWAI + LANGGraph + OPENAI SDK — Frameworks de Agentes

### Fontes
- https://github.com/google/adk-python (20.9k★)
- https://github.com/crewaiinc/crewai (56.3k★)
- https://github.com/langchain-ai/langgraph (38.4k★)
- https://github.com/openai/openai-agents-python

### Padrões Extraídos (10)

| # | Padrão | Descrição | Helenização para Gran-Mestre |
|---|--------|-----------|------------------------------|
| 6.1 | **Isolation Scopes** (ADK) | Sub-agents task não veem contexto do coordenador. Scoped-by-FC-id | Sub-agents do Gran-Mestre operam em bolha isolada de estado |
| 6.2 | **Handoff como Ferramenta** (OpenAI SDK) | Agentes como tools. Handoff = tool call que o LLM pode invocar | Formalizar roteamento como Handoff(pattern, handler) |
| 6.3 | **Event-Driven Listeners** (CrewAI) | `@start / @listen / @router + or_()/and_()` para workflows declarativos | Decorators para `@route(type="security")` → hestia.validate() |
| 6.4 | **Durable Checkpointing** (LangGraph) | `BaseCheckpointSaver` + canais (LastValue, Topic, EphemeralValue) para sobreviver a falhas | Checkpointing explícito entre sub-agents com canais de comunicação |
| 6.5 | **Shared State + Reducers** (LangGraph) | `Annotated[list, reducer]` para merge de estado concorrente | Reducers para merge de outputs de múltiplos sub-agents paralelos |
| 6.6 | **Dynamic Nodes + Static Graph** (ADK) | Arestas fixas + `ctx.run_node()` dinâmico. Workflow previsível mas flexível | Pipeline do Gran-Mestre: esqueleto fixo (análise→plano→execução→revisão) com slots dinâmicos |
| 6.7 | **Event Compaction** (ADK) | Sliding-window para manter sessões de tamanho controlado | Compactar eventos de sessão do pipeline para evitar crescimento infinito |
| 6.8 | **Processos Hierárquico e Sequencial** (CrewAI) | Sequential (previsível) vs Hierarchical (manager delega e valida) | Gran-Mestre já faz routing hierárquico — formalizar dois modos de operação |
| 6.9 | **Guardrails em Paralelo** (OpenAI SDK) | Guardrails rodam concorrentemente com agente, fail-fast | Executar Héstia (validação) em paralelo com execução principal |
| 6.10 | **Finishing Tool** (ADK) | Tool `finish_task` que sinaliza conclusão com resultado validado | Sub-agents reportam resultados estruturados com schema de saída |

---

## 7. LANGFUSE + TESTSPRITE + BMAD METHOD — Observabilidade e Testes

### Fontes
- https://github.com/langfuse/langfuse (32k★)
- https://github.com/TestSprite/testsprite-cli (2.7k★)
- https://github.com/bmad-code-org/BMAD-METHOD (51.2k★)

### Padrões Extraídos (7)

| # | Padrão | Descrição | Helenização para Gran-Mestre |
|---|--------|-----------|------------------------------|
| 7.1 | **Tracing Hierárquico 3 Níveis** | Trace (raiz) → Span (sub-operação) → Generation (LLM call) | Pipeline do Gran-Mestre: trace da requisição, spans das fases, generations das chamadas de modelo |
| 7.2 | **Prompt como Config (não como código)** | Prompts versionados com labels (production, canary), cache agressivo, compilação em runtime | Templates de tasks separados do código, versionados, com deploy sem mudança de código |
| 7.3 | **LLM-as-Judge Pipeline** | Avaliador automático roda em background sobre traces de produção | Avaliação automática de outputs do pipeline em background |
| 7.4 | **Cadeia de Avaliação** | LLM-as-Judge → User Feedback → Datasets → Experiments em CI/CD | Ciclo de melhoria contínua: produção → dataset → experimento → novo template |
| 7.5 | **Teste Autônomo (Agentic Testing)** | TestSprite: PRD → Feature Map → Test Plan → Test Code → Execução → Feedback Loop | Testes autônomos de cada fase do pipeline |
| 7.6 | **Documentação como Fonte Única** (BMad) | PRDs, specs de arquitetura e histórias de usuário são artefato primário; código é derivado | SKILL.md como fonte única de verdade; execução como artefato derivado |
| 7.7 | **CI/CD com Evals** | GitHub Action que roda experimento com prompt novo vs dataset antes de deploy | CI/CD do Gran-Mestre: validar template novo contra dataset de regressão |

---

## 8. OPENSPEC + AGENTSKILLS + SPECKIT — Especificações e Skills

### Fontes
- https://github.com/Fission-AI/OpenSpec (63k★)
- https://github.com/tech-leads-club/agent-skills (5k★)
- https://github.com/github/spec-kit (124k★)
- https://github.com/hysnsec/awesome-policy-as-code (210★)
- RBAC in GitHub Actions

### Padrões Extraídos (10)

| # | Padrão | Descrição | Helenização para Gran-Mestre |
|---|--------|-----------|------------------------------|
| 8.1 | **Delta Specs** (OpenSpec) | ADDED/MODIFIED/REMOVED em vez de reescrever specs inteiras | Mudanças no pipeline como deltas, não reescrita completa |
| 8.2 | **Changes como Unidades de Trabalho** | Uma pasta por feature: proposal → specs → design → tasks | Cada pipeline do Gran-Mestre é uma "change" com artefatos encadeados |
| 8.3 | **Archive Folds** | Archive mescla deltas nas specs principais e move change para archive | Ao completar pipeline, arquivar deltas nas specs principais |
| 8.4 | **SKILL.md + Templates** (AgentSkills) | YAML frontmatter (name, description, use_when, do_not_use_for) + markdown body + scripts/templates/references | SKILL.md do Gran-Mestre já segue este formato — evoluir frontmatter com `do_not_use_for` |
| 8.5 | **Lockfile de Integridade** | `.agents/.skill-lock.json` com hashes SHA-256 | Lockfile das skills do Gran-Mestre para garantir integridade |
| 8.6 | **Constitution Enforcement** (SpecKit) | 9 artigos de desenvolvimento (Library-First, Test-First, Simplicity Gate, Anti-Abstraction, Integration-First) | Constituição do Gran-Mestre: princípios imutáveis que governam o pipeline |
| 8.7 | **NEEDS CLARIFICATION** (SpecKit) | Marcadores obrigatórios em pontos ambíguos da spec | Quando task do pipeline é ambígua, inserir marcador de clarificação |
| 8.8 | **Policy-as-Code 3 Camadas** | Pipeline (RBAC GH Actions) → Infra (OPA/Gatekeeper) → Código (Constitutional gates) | Gates do pipeline como Policy-as-Code com motor OPA |
| 8.9 | **Skill-Based Scoping** | OAuth scopes controlam quais skills um agente-cliente pode invocar | Skills do Gran-Mestre protegidas por scopes de permissão |
| 8.10 | **Progressive Disclosure via MCP** | search → list → read → fetch. Usuário descobre skills gradualmente | Sub-agents: descoberta progressiva em vez de lista fixa |

---

## 9. POSTGRESQL CORE — WAL, MVCC, 2PC, Extensões

### Fontes
- https://github.com/postgres/postgres (21.6k★, PG 18.4)
- Documentação interna e arquitetura

### Padrões Extraídos (10)

| # | Padrão | Descrição | Helenização para Gran-Mestre |
|---|--------|-----------|------------------------------|
| 9.1 | **WAL (Write-Ahead Log)** | Mudanças escritas no log ANTES de serem aplicadas. Permite recovery e replay | Pipeline: cada decisão/ação logada antes de executar. Replay após crash |
| 9.2 | **MVCC (Multiversion Concurrency Control)** | Cada transação vê snapshot consistente. Leituras não bloqueiam escritas | Estado do pipeline como versões imutáveis. Conflitos detectados no commit |
| 9.3 | **Two-Phase Commit (2PC)** | PREPARE (garantir que todos podem commitar) → COMMIT (executar) | Workflows multi-fase: prepare (validar) → commit (executar). Rollback se falha |
| 9.4 | **Checkpoint + Recovery** | Periódicamente forçar estado ao disco. Recovery = aplicar WAL a partir do último checkpoint | Snapshot periódico do estado do orquestrador. Restore do último snapshot + replay |
| 9.5 | **Hook System (Function-Pointer)** | `planner_hook`, `ExecutorStart_hook`, etc. Padrão save-and-chain para extensibilidade | Plugins do Gran-Mestre como hooks com save-and-chain |
| 9.6 | **Three-Level Lock Manager** | Spinlocks (curto) → LWLocks (médio) → Heavyweight (objeto) | Sistema de locks em 3 níveis para coordenar acesso a recursos compartilhados |
| 9.7 | **Background Workers** | Processos registrados que rodam no postmaster. `RegisterBackgroundWorker()` | Workers de background do Gran-Mestre (ex: avaliação assíncrona) |
| 9.8 | **Custom Scan/Index AM** | Handler struct com callbacks. pgvector implementa HNSW como Index AM | Plugins de capability do Gran-Mestre como handler struct |
| 9.9 | **Memory Context System** | Alocação hierárquica: cada subsistema tem seu memory context. Reset atômico | Contextos de memória isolados por sub-agent. Reset ao final da fase |
| 9.10 | **Extended Query Protocol** | Parse → Bind → Execute → Close. Prepared statements com parâmetros | Pipeline: planejar (parse+bind) → executar (execute) → finalizar (close) |

---

## 10. PINECONE — Vector DB, Memória de Longo Prazo

### Fontes
- https://github.com/pinecone-io (Pinecone SDK)
- Documentação oficial, MCP server, blog

### Padrões Extraídos (8)

| # | Padrão | Descrição | Helenização para Gran-Mestre |
|---|--------|-----------|------------------------------|
| 10.1 | **Separação Read/Write** | Leituras e escritas escalam independentemente. Queries nunca bloqueiam writes | Pipeline: escalar leitura (consulta de estado) e escrita (log) independentemente |
| 10.2 | **4 Modalidades de Busca** | Full-text (BM25), Semantic (dense), Sparse-vector, Hybrid | Memória do Gran-Mestre: busca híbrida (semântica + lexical) para recall máximo |
| 10.3 | **Serverless-First** | Sem provisionamento, escala automática, cobrança por uso (RU/WU) | Deploy do Gran-Mestre: serverless por default, pod-based para latência previsível |
| 10.4 | **Namespaces para Multi-Tenancy** | 1 namespace por tenant/agente. Isolamento lógico sem custo extra | 1 namespace por usuário/pipeline no estado compartilhado |
| 10.5 | **Schema Imutável** | Fields não podem ser adicionados/removidos após criação. Planejar antes | Schema de pipeline: planejar campos antes de iniciar; imutável durante execução |
| 10.6 | **Reranking Essencial em Produção** | Embeddings perdem precisão em queries ambíguas. Rerank com modelos especializados | Two-stage retrieval: busca inicial + rerank com LLM para precisão |
| 10.7 | **MCP Memory Server** | Agent ganha tools: armazenar, buscar, rerank memórias via MCP commands | Memória do Gran-Mestre exposta como tools MCP para agentes |
| 10.8 | **Tiered Memory Architecture** | Core (contexto) → Working (sumários) → Long-Term (vector DB) → Archival (snapshots) | 4 camadas de memória no pipeline: contexto da fase → sessão → conhecimento → archive |

---

## PADRÕES TRANSVERSAIS (Cross-Cutting)

Padrões que apareceram em múltiplas fontes e merecem destaque especial:

| # | Padrão | Frequência | Fontes |
|---|--------|-----------|--------|
| T1 | **Execução Durável (WAL/Journal)** | 7/10 | Temporal, PostgreSQL, ADK, LangGraph, MCP, Pinecone, A2A |
| T2 | **State Isolation (Scopes/Namespaces)** | 6/10 | ADK, A2A, pgvector, Pinecone, LangGraph, CrewAI |
| T3 | **Two-Stage Processing (Coarse→Refine)** | 5/10 | pgvector (HNSW), Pinecone (rerank), Pipeline (gate→execute), SpecKit (spec→plan→impl) |
| T4 | **Plugin/Hook Architecture** | 5/10 | PostgreSQL (hooks), MCP (servers), AgentSkills (skills), pgvector (handler), ADK (tools) |
| T5 | **Event-Driven Communication** | 5/10 | CrewAI (listeners), A2A (tasks), Inngest (events), OTel (spans), MCP (notifications) |
| T6 | **Constitutional Gates** | 4/10 | SpecKit (9 articles), OpenSpec (delta), BMad (documentation-first), Gran-Mestre (phases) |
| T7 | **Observabilidade em 3 Camadas** | 4/10 | OTel (traces/metrics/logs), Langfuse (trace/span/generation), Pinecone (RU/WU), PostgreSQL (WAL/MVCC/checkpoint) |
| T8 | **Versionamento de Schema/Interface** | 4/10 | pgvector (migrations), OpenSpec (delta), Langfuse (prompts), MCP (protocol version) |

---

## AÇÕES IMEDIATAS PARA O GRAN-MESTRE

### Prioridade Alta (implementar agora)

1. **Adicionar `do_not_use_for` no frontmatter do SKILL.md** — define casos onde o Gran-Mestre NÃO deve ser usado
2. **Formalizar Pipeline como Workflow Durável** — log WAL-like antes de cada ação; replay após crash
3. **Adicionar métricas de observabilidade por fase** — duração, tokens, calls, erros (inspirado OTel GenAI)
4. **Implementar Delta State entre fases** — persistir só deltas, não estado completo

### Prioridade Média (próximo ciclo)

5. **SKILL.md com schemas de entrada/saída tipados** — sub-agents com schemas Pydantic
6. **Isolation scopes para sub-agents** — cada sub-agent não vê contexto do coordenador
7. **Cache hierárquico** — SemanticCache + ToolResultCache + ConversationMemory
8. **Constitution enforcement** — gates de pré-execução baseados em princípios imutáveis

### Prioridade Baixa (visão)

9. **Memory MCP Server** — expor memória do pipeline como tools MCP
10. **Parallel guardrails** — executar Héstia em paralelo com execução
11. **CI/CD com evals** — validar templates contra dataset de regressão antes de deploy
12. **Agent Card discovery** — cada sub-agent expõe `/.well-known/agent-card.json`

---

## RESUMO

| Métrica | Valor |
|---------|-------|
| Total de fontes | 35+ |
| Total de padrões extraídos | 86 |
| Padrões transversais | 8 |
| Áreas de conhecimento | 10 |
| Ações imediatas (alta prioridade) | 4 |
| Ações médio prazo | 4 |
| Visão de longo prazo | 4 |
| Workers librarian utilizados | 8 |
| Duração total da autofagia | ~3 minutos |

**Próximos passos:**
1. Aplicar as 4 ações de alta prioridade no SKILL.md
2. Rodar `/gran-mestre validate` para verificar integridade
3. Iniciar pipeline de upgrade do Gran-Mestre para v7.0
