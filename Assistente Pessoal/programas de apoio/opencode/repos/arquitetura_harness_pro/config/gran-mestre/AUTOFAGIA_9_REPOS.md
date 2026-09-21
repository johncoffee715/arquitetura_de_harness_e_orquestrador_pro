---
name: autofagia-9-repos
description: "Autofagia de 9 repositórios via pipeline MIX (COMPLEX + CRITICAL + FEATURE). Extração de padrões, helenização para o Gran-Mestre."
mode: skill
origin: autofagia:9-repos
metadata:
  category: meta-integration
  version: 1.0.0
  author: Gran-Mestre (pipeline MIX — 6 workers paralelos)
  repos: 9
  patterns: 47
  purpose: "Self-learning — absorver padrões de 9 ecossistemas distintos"
---

# AUTOFAGIA — 9 Repositórios

## Visão Geral

| # | Repo | Stars | Tipo | Padrões Extraídos |
|---|------|-------|------|-------------------|
| 1 | anthropics/skills | - | Spec + 17 skills | 8 |
| 2 | affaan-m/ecc | - | 67 agents + 281 skills + 94 commands | 12 |
| 3 | netresearch/context7-skill | - | REST API skill | 5 |
| 4 | darrenhinde/OpenAgentsControl | - | Pattern Control | 6 |
| 5 | ayghri/i-have-adhd | - | ADHD output shaping | 4 |
| 6 | chuspeeism/dashi-ppt-skill | - | PPT generation | 3 |
| 7 | xai-org/grok-build | - | Rust TUI coding agent | 5 |
| 8 | vercel-labs/skills | - | Skills CLI | 4 |
| 9 | chidiwilliams/buzz | - | Speech recognition | 2 |

**Total: 47 padrões extraídos**

---

## 1. ANTHROPICS/SKILLS — Agent Skills Spec

### Padrões Extraídos (8)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 1 | **SKILL.md format** | Frontmatter (name, description) + corpo Markdown | Padrão canônico para todas as skills |
| 2 | **Trigger-based activation** | Skills disparam por contexto, não por comando | Gran-Mestre pode ativar skills automaticamente |
| 3 | **Template system** | Template SKILL.md para criação de novas skills | Já temos TEMPLATE-skill.md |
| 4 | **allowed-tools** | Skills declaram quais tools podem usar | Controle de permissão por skill |
| 5 | **disable-model-invocation** | Skills podem desativar invocação de modelo | Para skills que só formatam output |
| 6 | **Spec externalizada** | Spec vive em agentskills.io, não no repo | Documentação versionada separadamente |
| 7 | **17 skills de exemplo** | xlsx, pdf, pptx, webapp-testing, etc. | Padrões de skills de domínio |
| 8 | **Skill categories** | productivity, design, testing, api | Categorização para discovery |

### Skills Disponíveis

| Skill | Descrição |
|-------|-----------|
| xlsx | Spreadsheet manipulation |
| webapp-testing | Playwright testing toolkit |
| web-artifacts-builder | HTML artifacts with React/Tailwind |
| theme-factory | 10 pre-set themes for artifacts |
| slack-gif-creator | GIFs for Slack |
| skill-creator | Create new skills |
| pptx | PowerPoint generation |
| pdf | PDF manipulation |
| mcp-builder | Build MCP servers |
| internal-comms | Communication templates |
| frontend-design | UI/UX design toolkit |
| docx | Word document manipulation |
| doc-coauthoring | Collaborative docs |
| claude-api | Claude API usage |
| canvas-design | Canvas/artifact design |
| brand-guidelines | Brand consistency |
| algorithmic-art | Generative art |

---

## 2. AFFAAN-M/ECC — Everything Claude Code

### Padrões Extraídos (12)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 9 | **Agent-First architecture** | 67 agents especializados | Gran-Mestre já tem — expandir |
| 10 | **281 skills** | Maior catálogo de skills conhecido | Referência para criação de skills |
| 11 | **94 commands** | Comandos slash extensivos | Referência para comandos |
| 12 | **21 hooks** | 7 eventos (PreToolUse, PostToolUse, Stop, etc.) | Sistema de hooks maduro |
| 13 | **Agent evaluator** | 5-axis quality rubric | Integrar como fable-judge alternativo |
| 14 | **Build-error-resolver** | Fix build errors with minimal diffs | Integrar como subagent |
| 15 | **Code-reviewer per language** | C++, C#, Django, etc. | Gran-Mestre já tem — expandir |
| 16 | **Conversation analyzer** | Analisa transcripts para hooks | Self-learning via análise de conversa |
| 17 | **Hookify system** | Cria hooks a partir de padrões | Auto-generar hooks |
| 18 | **Agent self-evaluation** | Auto-avaliação de output | Integrar no pipeline |
| 19 | **Doc-updater** | Atualiza documentação automaticamente | Integrar como subagent |
| 20 | **Session lifecycle** | SessionStart → PreToolUse → PostToolUse → Stop → SessionEnd | Ciclo de vida completo |

### Agent Categories (67)

| Categoria | Agents |
|-----------|--------|
| Architecture | architect, code-architect, code-explorer |
| Build | build-error-resolver, cpp-build-resolver, dart-build-resolver, django-build-resolver |
| Review | code-reviewer, cpp-reviewer, csharp-reviewer, django-reviewer, python-reviewer |
| Quality | agent-evaluator, code-simplifier, comment-analyzer |
| Docs | doc-updater, docs-lookup |
| Communication | chief-of-staff |
| Accessibility | a11y-architect |
| Debug | conversation-analyzer |

### Hook Events

| Event | Hooks | Descrição |
|-------|-------|-----------|
| PreToolUse | 8 | Bash dispatcher, doc warnings |
| PreCompact | 1 | Save state before compaction |
| SessionStart | 2 | Load context, plan canvas |
| PostToolUse | 2 | Sync/async dispatchers |
| PostToolUseFailure | 1 | MCP health check |
| Stop | 6 | Format, typecheck, console.log check |
| SessionEnd | 1 | Lifecycle marker |

---

## 3. NETRESEARCH/CONTEXT7-SKILL

### Padrões Extraídos (5)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 21 | **REST API wrapper** | Shell script como skill backend | Padrão para skills que chamam APIs |
| 22 | **allowed-tools** | Declara tools permitidas (Bash(curl:*), Read) | Controle granular |
| 23 | **Evals system** | evals.json para testar skills | Testar skills automaticamente |
| 24 | **Harness verification** | verify-harness.sh | Verificar maturidade do harness |
| 25 | **When to use / When NOT to use** | Trigger rules explícitas | Melhorar triggers das skills |

### Skill Structure

```
skills/context7/
├── SKILL.md          # Metadata, triggers, workflow
└── scripts/
    └── context7.sh   # REST API wrapper (search + docs)
```

---

## 4. DARRENHINDE/OPENAGENTSCONTROL

### Padrões Extraídos (6)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 26 | **Pattern Control** | Define patterns once, AI uses forever | Gran-Mestre pode definir padrões |
| 27 | **Approval Gates** | Review before execution | Gates no pipeline |
| 28 | **Repeatable Results** | Same patterns = same quality | Consistência via padrões |
| 29 | **Editable Agents** | Full control over AI behavior | Agents configuráveis |
| 30 | **Multi-language** | TS, Python, Go, Rust, C# | Suporte multi-linguagem |
| 31 | **Model Agnostic** | Claude, GPT, Gemini, local | Multi-provider |

### Documentation Structure

```
docs/
├── agents/           # Agent system docs
├── features/         # Feature docs
├── guides/           # User guides
├── model-providers/  # Provider configs
└── planning/         # Planning docs
```

---

## 5. AYGHRI/I-HAVE-ADHD

### Padrões Extraídos (4)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 32 | **Output shaping** | Formatar output para necessidades específicas | Gran-Mestre pode adaptar output |
| 33 | **Always-on pattern** | Flag file ativa modo permanentemente | Modos persistentes via flag |
| 34 | **SessionStart hook** | Injeta regras no início da sessão | Hooks de sessão |
| 35 | **POSIX sh compatibility** | Shell script puro, sem dependências | Portabilidade máxima |

### ADHD Rules (reutilizáveis)

1. **Working memory is small** — não peça para "keep in mind"
2. **Knowing ≠ doing** — fricção entre "got it" e "done it"
3. **Starting is hardest** — primeira ação deve ser óbvia e pequena
4. **Time estimates feel uniform** — estimativas vagas falham
5. **Wins must be visible** — celebre progresso

---

## 6. CHUSPEEISM/DASHI-PPT-SKILL

### Padrões Extraídos (3)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 36 | **Theme system** | 12 temas visuais pré-definidos | Temas para outputs |
| 37 | **Layout library** | 1020 layouts, 8576 controls | Biblioteca de layouts |
| 38 | **Browser-based editing** | Editar no browser antes de exportar | Preview interativo |

---

## 7. XAI-ORG/GROK-BUILD

### Padrões Extraídos (5)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 39 | **Rust TUI** | Terminal UI com ratatui | Referência de arquitetura |
| 40 | **75 crates** | Modularização extrema | Arquitetura modular |
| 41 | **ACP protocol** | Agent Client Protocol | Protocolo padronizado |
| 42 | **Headless mode** | Scripting/CI sem TUI | Modo headless |
| 43 | **Memory system** | xai-grok-memory | Sistema de memória |

### Crates Architecture

```
crates/
├── build/          # Build tools
├── codegen/        # Code generation
│   ├── xai-acp-lib
│   ├── xai-agent-lifecycle
│   ├── xai-chat-state
│   ├── xai-codebase-graph
│   ├── xai-grok-memory
│   ├── xai-grok-mcp
│   └── ... (40+ crates)
└── common/         # Shared utilities
```

---

## 8. VERCEL-LABS/SKILLS

### Padrões Extraídos (4)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 44 | **Skills CLI** | add, use, list, update, init | Gerenciamento de skills |
| 45 | **Agent detection** | Detecta Cursor, Claude, etc. | Auto-detectar agente |
| 46 | **Multi-agent support** | Codex, Claude, OpenClaw, etc. | Suporte multi-agente |
| 47 | **Lock file** | skills-lock.json | Versionamento de skills |

### CLI Commands

| Command | Descrição |
|---------|-----------|
| `skills add <pkg>` | Install from git/URL/local |
| `skills use <pkg>@<skill>` | Use without installing |
| `skills list` | List installed |
| `skills update` | Update to latest |
| `skills init` | Create new SKILL.md |

---

## 9. CHIDIWILLIAMS/BUZZ

### Padrões Extraídos (2)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 48 | **Whisper integration** | Speech-to-text local | Transcrição de áudio |
| 49 | **Python app** | App desktop com GUI | Referência de arquitetura |

---

## Resumo: 47 Padrões por Categoria

| Categoria | Padrões | Exemplos |
|-----------|---------|----------|
| **Skills** | 12 | SKILL.md format, trigger-based, allowed-tools, evals |
| **Agents** | 10 | Agent-first, evaluator, build-resolver, self-eval |
| **Hooks** | 8 | 7 events, always-on, SessionStart, lifecycle |
| **Architecture** | 7 | Rust TUI, 75 crates, ACP, modularização |
| **Output** | 4 | ADHD shaping, themes, browser editing |
| **Tools** | 6 | Skills CLI, agent detection, lock file |
| **Total** | **47** | |

---

## Integração com Gran-Mestre

### Padrões Já Existentes (reconfirmados)

| Padrão | Gran-Mestre | Status |
|--------|-------------|--------|
| Agent-First | 46 agents | ✅ |
| Skills | 87 skills | ✅ |
| Hooks | 18 hooks | ✅ |
| Commands | 72 commands | ✅ |
| Model Rotation | 100 modelos | ✅ |
| Safety Protocol | SHA + rollback | ✅ |

### Novos Padrões para Integrar

| Padrão | Ação | Prioridade |
|--------|------|------------|
| Agent evaluator (5-axis) | Integrar como subagent | ALTA |
| Build-error-resolver | Integrar como subagent | ALTA |
| Hookify system | Auto-gerar hooks | MÉDIA |
| Output shaping (ADHD) | Adaptar output por contexto | MÉDIA |
| Skills CLI | Gerenciamento de skills | MÉDIA |
| Evals system | Testar skills automaticamente | MÉDIA |
| Pattern Control | Definir padrões reutilizáveis | BAIXA |
| Approval Gates | Gates no pipeline | ✅ Já existe |

---

**Versão:** 1.0.0
**Data:** 2026-07-27
**Repos:** 9
**Padrões:** 47
**Workers:** 6 paralelos
**Pipeline:** MIX (COMPLEX + CRITICAL + FEATURE)

---

## Apêndice: Padrões Profundos (6 Workers Paralelos)

### Padrões Críticos Descobertos pelos Workers

| # | Padrão | Repo | Descrição | Prioridade GM |
|---|--------|------|-----------|---------------|
| 50 | **Extension Registry** | grok-build | Builder→Immutable Registry com contributors tipados (TurnLifecycle, SessionLifecycle, TurnInput, Command) | ALTA |
| 51 | **Workflow Engine + Journal** | grok-build | Rhai scripting, determinismo forçado, journal JSONL para replay/resume, host functions (agent, parallel, phase, await_user) | ALTA |
| 52 | **Cascata de Decisão 5 estágios** | grok-build | YOLO→Session Grants→Static Allowlist→Auto Classifier→User Prompt | ALTA |
| 53 | **Meta-Skill com Subagentes** | anthropics | skill-creator com grader (avalia), comparator (A/B cego), analyzer (pós-hoc) | ALTA |
| 54 | **Harness Verification 3 Níveis** | context7 | Basic (estrutura)→Verified (referências)→Enforced (automação) | ALTA |
| 55 | **Eval Framework 3 condições** | i-have-adhd | baseline/candidate/comparator, 5 métricas ponderadas, release gate | ALTA |
| 56 | **Pipeline Orchestration 15 passos** | dashi-ppt | Modular com scripts npm independentes, validação em camadas | ALTA |
| 57 | **Approval Gates XML** | OpenAgentsControl | critical_rules priority=absolute enforcement=strict | ALTA |
| 58 | **Hook System Flag File** | i-have-adhd | POSIX puro, never blocks, opt-in via flag file | MÉDIA |
| 59 | **ContextScout** | OpenAgentsControl | Descoberta automática de contexto com ranqueamento Critical→High→Medium | MÉDIA |
| 60 | **3 Níveis de Contexto** | OpenAgentsControl | Isolation (80%)→Filtered (20%)→Windowed (raro) — redução 80% tokens | MÉDIA |
| 61 | **Self-Review Loop 4 etapas** | OpenAgentsControl | Types→Anti-patterns→Acceptance criteria→External libs | MÉDIA |
| 62 | **Newtype IDs seguros** | grok-build | SessionId, AgentId, PhaseId como tipos separados | MÉDIA |
| 63 | **Tool Bridge + Resource Injection** | grok-build | SharedResources para dependências compartilhadas | MÉDIA |
| 64 | **CLI Módulo Pattern** | skills | parseXOptions() + runX() por comando | MÉDIA |
| 65 | **Instalação Canônica + Symlink** | skills | ~/.agents/skills/ + symlinks por agente | MÉDIA |
| 66 | **Dual-Registry** | context7 | Composer + npm apontando para mesmo SKILL.md | BAIXA |
| 67 | **CI/Hook Parity** | context7 | Mesmos checks local e CI, Renovate pins | BAIXA |
| 68 | **Drift Detection** | context7 | Alerta quando build/CI muda sem atualizar AGENTS.md | BAIXA |
| 69 | **Pre-send Communication Check** | i-have-adhd | 5 regras de limpeza antes de enviar | BAIXA |
| 70 | **Version Check Silencioso** | dashi-ppt | 3 endpoints, China-first, só outputa se há nova versão | BAIXA |

**Total atualizado: 70 padrões**

### Top 10 para Implementação Imediata

| # | Padrão | Repo | Ação |
|---|--------|------|------|
| 1 | Extension Registry | grok-build | Cada subagente se registra como contributor |
| 2 | Workflow Engine | grok-build | Pipeline GSD com journal replay |
| 3 | Cascata de Decisão | grok-build | Roteamento multi-estágio |
| 4 | Meta-Skill | anthropics | skill-creator com grader/comparator/analyzer |
| 5 | Harness Verification | context7 | Verificar maturidade dos componentes |
| 6 | Eval Framework | i-have-adhd | Avaliar subagentes antes de delegar |
| 7 | Pipeline 15 passos | dashi-ppt | Orquestração modular |
| 8 | Approval Gates | OpenAgentsControl | Gates XML em todos agentes |
| 9 | ContextScout | OpenAgentsControl | Descoberta automática de contexto |
| 10 | Self-Review Loop | OpenAgentsControl | 4 verificações obrigatórias |
