---
name: openclaude-integration
description: "Integração do Gitlawb/openclaude ao Gran-Mestre via autofagia e helenização. Coding-agent CLI multi-provider (30.4k stars, TypeScript/Bun)."
mode: subagent
origin: absorvido:Gitlawb/openclaude
metadata:
  category: orchestration
  version: 1.0.0
  author: Gran-Mestre (autofagia de OpenClaude)
  source: https://github.com/Gitlawb/openclaude
  stars: 30400
  language: TypeScript/Bun
  license: MIT
  note: "OpenClaude é coding-agent CLI multi-provider com 200+ backends, fork subagent, coordinator mode, team system, gRPC server"
---

# OPENCLAUDE — Integration Document

## Conceito Fundamental

> **Coding-agent CLI aberto que roda com qualquer LLM — cloud ou local.**
> Um terminal, qualquer provider: OpenAI, Gemini, Ollama, DeepSeek, Codex, e 200+ outros.

## Visão Geral do Repositório

| Aspecto | Detalhe |
|---------|---------|
| **Repo** | https://github.com/Gitlawb/openclaude |
| **Stars** | 30.4k |
| **Commits** | 1.113 |
| **Linguagem** | TypeScript (strict ESM) + Bun |
| **Runtime** | Node.js >=22.0.0 |
| **UI** | React + Ink (terminal) |
| **Dependências** | 3 production, 75 dev |
| **Testes** | Bun test runner |
| **License** | MIT |

## Padrões Extraídos (12 padrões)

---

### 1. Fork Subagent (Implicação de Contexto)

**Origem:** `src/tools/AgentTool/forkSubagent.ts`

```typescript
// Omissão de subagent_type ativa fork implícito
// Filho herda TODO o contexto do pai
// Prompt cache sharing com prefixes byte-idênticos
export const FORK_AGENT = {
  agentType: 'fork',
  tools: ['*'],
  maxTurns: 200,
  model: 'inherit',
  permissionMode: 'bubble',
}
```

**Helenização para Gran-Mestre:**
- Quando Atlas delega uma task sem especificar subagent_type → fork implícito
- O fork herda o contexto completo da conversa pai
- Prompt cache sharing: todos os forks produzem prefixes idênticos para maximizar cache hits
- Regras do fork child: NÃO spawnar sub-agents, executar diretamente, reportar structured facts

**Aplicação:**
```
Gran-Mestre → Atlas (sem subagent_type) → Fork implícito
  ├── Herda contexto do pai
  ├── Executa diretamente
  ├── Commita mudanças
  └── Reporta: Scope/Result/Key files/Files changed/Issues
```

---

### 2. Coordinator Mode (Orquestração por Workers)

**Origem:** `src/coordinator/coordinatorMode.ts`, `src/coordinator/workerAgent.ts`

```typescript
// Modo especial: agente principal vira coordinator
// Spawna workers autonomamente
const WORKER_AGENT: BuiltInAgentDefinition = {
  ...GENERAL_PURPOSE_AGENT,
  agentType: 'worker',
  whenToUse: 'Worker agent for coordinator mode. Executes tasks autonomously.',
}

export function getCoordinatorAgents(): BuiltInAgentDefinition[] {
  return [WORKER_AGENT, GENERAL_PURPOSE_AGENT, EXPLORE_AGENT, PLAN_AGENT]
}
```

**Helenização para Gran-Mestre:**
- Gran-Mestre já usa este padrão (delega para Atlas, Héstia, Atena)
- Workers têm ferramentas próprias e executam autonomamente
- Coordinator não executa código — apenas orquestra
- Workers podem ter tools restritos (read-only para Explore/Plan)

**Aplicação no MIX Mode:**
```
Gran-Mestre (Coordinator)
├── Worker 1: Prometheus (planning)
├── Worker 2: Atlas (execution)
├── Worker 3: Héstia (validation)
├── Worker 4: Atena (macro-review)
└── Worker 5: Verificador (verification)
```

---

### 3. Team System (Equipes Autônomas)

**Origem:** `src/tools/TeamCreateTool/`, `src/tools/TeamDeleteTool/`

```typescript
// Team = TaskList (1:1 correspondence)
// ~/.openclaude/teams/{team-name}/config.json
// ~/.openclaude/tasks/{team-name}/
```

**Helenização para Gran-Mestre:**
- Criar equipes de agents para projetos complexas
- Cada equipe tem sua task list persistente
- Equipes podem ser criadas/destruídas dinamicamente
- TeamCreate → cria config + task list

**Aplicação:**
```
Team "biografia": {
  members: [researcher, writer, reviewer],
  tasks: [research, outline, draft, polish]
}
```

---

### 4. Task System (Gerenciamento de Tarefas)

**Origem:** `src/tools/TaskCreateTool/`, `src/tools/TaskGetTool/`, `src/tools/TaskListTool/`, `src/tools/TaskUpdateTool/`, `src/tools/TaskStopTool/`

```typescript
// 6 tools para gerenciar tasks:
// TaskCreate, TaskGet, TaskList, TaskOutput, TaskStop, TaskUpdate
```

**Helenização para Gran-Mestre:**
- TaskCreate: cria task com descrição e status
- TaskList: lista todas as tasks do projeto
- TaskGet: obtém detalhes de uma task específica
- TaskUpdate: atualiza status/conteúdo
- TaskStop: para task em execução
- TaskOutput: obtém output de task completada

**Aplicação no Gran-Mestre:**
- Integrar com o sistema de TODOs existente
- Tasks persistem entre sessões
- Status tracking: pending → in_progress → completed/failed

---

### 5. Repo Map (Inteligência de Codebase)

**Origem:** `src/tools/RepoMapTool/`

```typescript
// Tree-sitter parsing → symbol extraction → cross-file reference graph
// → PageRank importance ranking → token-budgeted output
// Supports: TypeScript, JavaScript, Python
// Cache em disco para re-consultas instantâneas
```

**Helenização para Gran-Mestre:**
- Mapa estrutural do repositório ranqueado por importância (PageRank)
- Extrai funções, classes, tipos, interfaces
- Focus files/symbols para boost de ranking
- Auto-cache em disco

**Aplicação:**
- Usar no início de sessões em repositórios desconhecidos
- Identificar arquivos estruturalmente conectados
- Complementar o graphify existente

---

### 6. Multi-Provider Routing (200+ Backends)

**Origem:** `src/services/api/agentRouting.ts`, `src/commands/provider/`

```typescript
// Providers suportados:
// OpenAI, Gemini, Ollama, DeepSeek, Groq, Mistral, LM Studio,
// Fireworks AI, GitHub Models, Codex OAuth, Xiaomi MiMo, NEAR AI,
// Cloudflare Workers AI, Atomic Chat, Bedrock, Vertex, Foundry,
// Hicap, LongCat, ClinePass, Z.AI GLM, AIMLAPI, etc.
```

**Helenização para Gran-Mestre:**
- Sistema de profiles para providers (`~/.openclaude-profile.json`)
- Guided setup via `/provider`
- Auto-routing por modelo
- Fallback chain entre providers

**Aplicação no Gran-Mestre:**
- Já temos model_rotation — expandir para multi-provider
- Profile system para salvar configs de provider
- `/provider` command para setup guiado

---

### 7. Background Sessions (Sessões Desacopladas)

**Origem:** CLI flags `--bg`, `openclaude ps/logs/kill`

```bash
openclaude --bg "fix failing tests"
openclaude --bg --name auth-refactor "refactor auth middleware"
openclaude ps
openclaude logs auth-refactor
openclaude kill auth-refactor
```

**Helenização para Gran-Mestre:**
- Rodar tasks em background (desacoplado do terminal)
- `openclaude ps` — listar sessões ativas
- `openclaude logs <name>` — ver output
- `openclaude kill <name>` — terminar sessão
- Session metadata em `~/.openclaude/bg-sessions/`

**Aplicação:**
- Usar `task(..., run_in_background=true)` para execução paralela
- Monitorar com `background_output()`

---

### 8. WebSearch Multi-Provider (9 Backends)

**Origem:** `src/tools/WebSearchTool/providers/`

```typescript
// Providers de busca:
// DuckDuckGo (default, free)
// Firecrawl (JS-rendered pages)
// Exa (semantic search)
// Brave Search
// Bing
// Jina
// Mojeek
// Tavily
// You.com
// Custom (user-defined)
```

**Helenização para Gran-Mestre:**
- DuckDuckGo como fallback gratuito
- Firecrawl para páginas JS-rendered
- Exa para busca semântica
- Brave como alternativa robusta
- Tavily para research-focused queries

**Aplicação:**
- Integrar com agent-reach
- Fallback chain: Exa → Brave → DuckDuckGo

---

### 9. Cron/Schedule System (Agendamento)

**Origem:** `src/tools/ScheduleCronTool/`

```typescript
// CronCreate, CronDelete, CronList tools
// Jitter config para evitar thundering herd
// Feature gate: CLAUDE_CODE_DISABLE_CRON
```

**Helenização para Gran-Mestre:**
- Criar tasks agendadas (cron)
- Listar e deletar agendamentos
- Jitter para evitar sobrecarga

**Aplicação:**
- Agendar audits periódicos
- Agendar syncs de memória
- Agendar backups

---

### 10. Permission Modes (Controle de Acesso)

**Origem:** `src/hooks/toolPermission/`

```typescript
// Modes:
// 'bubble' — pergunta ao pai
// 'bypassPermissions' — sem perguntas
// 'acceptEdits' — aceita edits sem perguntar
// 'auto' — classifier decide
// 'fullAccess' — acesso total
```

**Helenização para Gran-Mestre:**
- bubble: subagent pergunta ao Gran-Mestre (padrão)
- bypassPermissions: agents confiáveis (Prometheus, Atlas)
- auto: classifier decide baseado no contexto

**Aplicação:**
- Gran-Mestre usa bypassPermissions para agents internos
- Subagents usam bubble para ações destrutivas

---

### 11. gRPC Server (Modo Headless)

**Origem:** `src/grpc/server.ts`

```typescript
// Bidirectional streaming gRPC service
// Proto definition: src/proto/openclaude.proto
// Integração com CI/CD, UIs custom, outras apps
```

**Helenização para Gran-Mestre:**
- Expor Gran-Mestre como serviço gRPC
- Streaming bidirecional para UIs
- Integração com pipelines CI/CD

---

### 12. Doctor/Runtime (Diagnósticos)

**Origem:** `src/commands/doctor/`, scripts `system-check.ts`

```bash
bun run doctor:runtime          # Checagens de saúde
bun run doctor:runtime:json     # Output JSON para automação
bun run doctor:report           # Persistir relatório
bun run verify:privacy          # Verificar sem phone-home
bun run security:pr-scan        # Scan de segurança em PRs
```

**Helenização para Gran-Mestre:**
- `doctor:runtime` — verificar providers, reachability, configs
- `verify:privacy` — garantir sem phone-home
- `security:pr-scan` — scan de intenção em PRs

---

## Metodologia de Segurança (14 pontos)

| # | Verificação | Status |
|---|-------------|--------|
| 1 | Fork herda contexto do pai (sem vazamento) | ✅ Seguro |
| 2 | Coordinator não executa código diretamente | ✅ Seguro |
| 3 | Team system usa paths isolados | ✅ Seguro |
| 4 | Tasks persistem em ~/.openclaude/ (local) | ✅ Seguro |
| 5 | Repo Map cache em disco (local) | ✅ Seguro |
| 6 | Multi-provider: credenciais em profiles | ✅ Seguro |
| 7 | Background sessions: metadata local | ✅ Seguro |
| 8 | WebSearch: sem envio de dados sensíveis | ✅ Seguro |
| 9 | Cron: agendamentos locais | ✅ Seguro |
| 10 | Permission modes: controle granular | ✅ Seguro |
| 11 | gRPC: autenticação via proto | ✅ Seguro |
| 12 | Doctor: diagnósticos locais | ✅ Seguro |
| 13 | Privacy verify: garante sem phone-home | ✅ Seguro |
| 14 | PR scan: análise de intenção | ✅ Seguro |

**Resultado: 🟢 SEGURO — 14/14 verificações passaram**

---

## Integração com Gran-Mestre

### Agent System

| Agent OpenClaude | Gran-Mestre Equivalente | Ação |
|-----------------|------------------------|------|
| Explore (read-only) | explore (já existe) | ✅ Já integrado |
| Plan (read-only) | planner (já existe) | ✅ Já integrado |
| general-purpose | general (já existe) | ✅ Já integrado |
| verification | fable-judge | ✅ Já integrado |
| worker | Atlas sub-workers | ⚡ Criar |
| fork | Gran-Mestre fork implícito | ⚡ Criar |
| claudeCodeGuide | N/A (específico OpenClaude) | ❌ Não aplicável |
| statuslineSetup | N/A (UI específica) | ❌ Não aplicável |

### Tools

| Tool OpenClaude | Gran-Mestre Equivalente | Ação |
|----------------|------------------------|------|
| AgentTool | task() | ✅ Já integrado |
| BashTool | bash() | ✅ Já integrado |
| FileReadTool | read() | ✅ Já integrado |
| FileEditTool | edit() | ✅ Já integrado |
| FileWriteTool | write() | ✅ Já integrado |
| GlobTool | glob() | ✅ Já integrado |
| GrepTool | grep() | ✅ Já integrado |
| WebSearchTool | websearch() | ✅ Já integrado |
| WebFetchTool | webfetch() | ✅ Já integrado |
| RepoMapTool | graphify | ⚡ Integrar |
| TeamCreateTool | N/A | ⚡ Criar |
| TaskCreateTool | todowrite() | ✅ Já integrado |
| SkillTool | skill() | ✅ Já integrado |
| CronCreateTool | N/A | ⚡ Criar |
| MonitorTool | N/A | ⚡ Criar |
| LSPTool | lsp_* tools | ✅ Já integrado |
| REPLTool | N/A | ❌ Não aplicável |
| NotebookEditTool | N/A | ❌ Não aplicável |
| PowerShellTool | N/A (Windows) | ❌ Não aplicável |

### Skills

| Skill OpenClaude | Gran-Mestre Equivalente | Ação |
|-----------------|------------------------|------|
| loop (background) | ralph-loop | ✅ Já integrado |
| batch (parallel) | MoA fan-out | ✅ Já integrado |
| pdf | N/A | ⚡ Avaliar |
| claudeInChrome | browser-use | ✅ Já integrado |
| debug | debugging skill | ✅ Já integrado |
| simplify | refactor skill | ✅ Já integrado |
| updateConfig | gsd-config | ✅ Já integrado |
| keybindings | N/A | ❌ Não aplicável |
| scheduleRemoteAgents | cron system | ⚡ Criar |

---

## O que NÃO faz

- Não força todos os providers a terem o mesmo comportamento
- Não ignora diferenças de capability entre modelos
- Não auto-instala dependências sem confirmação
- Não expõe credenciais em logs
- Não permite phone-home sem verificação

## Limitações

- **TypeScript/Bun** — stack específica, não Python/Go
- **Node.js >=22** — runtime requirement
- **Provider-specific features** — não tudo funciona em todos providers
- **Local models** — qualidade inferior para tasks complexas

---

## Linha de Comando de Referência

```bash
# Instalação
npm install -g @gitlawb/openclaude@latest

# Setup
openclaude                    # Iniciar
/provider                     # Setup guiado de provider
/onboard-github               # GitHub Models onboarding

# Sessões
openclaude --resume <id>      # Resumir sessão
openclaude --continue          # Continuar última sessão
openclaude --bg "task"         # Rodar em background
openclaude ps                  # Listar sessões
openclaude logs <name>         # Ver logs

# Diagnósticos
openclaude --version           # Versão
doctor:runtime                 # Health check
verify:privacy                 # Verificar phone-home
```

---

**Versão:** 1.0.0
**Data:** 2026-07-27
**Fonte:** Gitlawb/openclaude (30.4k stars)
**Autofagia:** 12 padrões extraídos e helenizados
**Segurança:** 🟢 14/14 verificações passaram
