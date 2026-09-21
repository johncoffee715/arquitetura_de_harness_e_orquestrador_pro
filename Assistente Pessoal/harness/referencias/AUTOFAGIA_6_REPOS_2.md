---
name: autofagia-6-repos-2
description: "Autofagia de 6 repositórios via pipeline MIX. Extração de padrões, helenização para o Gran-Mestre."
mode: skill
origin: autofagia:6-repos-2
metadata:
  category: meta-integration
  version: 1.0.0
  author: Gran-Mestre (pipeline MIX)
  repos: 6
  patterns: 35
  purpose: "Self-learning — absorver padrões de 6 ecossistemas distintos"
---

# AUTOFAGIA — 6 Repositórios (Lote 2)

## Visão Geral

| # | Repo | Tipo | Padrões Extraídos |
|---|------|------|-------------------|
| 1 | multica-ai/andrej-karpathy-skills | Behavioral guidelines | 5 |
| 2 | deepseek-ai/DeepSpec | Speculative decoding | 4 |
| 3 | CoreBunch/Instatic | CMS self-hosted | 6 |
| 4 | nexu-io/open-design | Design platform (164 skills) | 8 |
| 5 | ruvnet/ruflo | Agent federation (314 MCP tools) | 7 |
| 6 | KnockOutEZ/wigolo | Web intelligence MCP | 5 |

**Total: 35 padrões extraídos**

---

## 1. MULTICA-AI/ANDREJ-KARPATHY-SKILLS

### Padrões Extraídos (5)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 1 | **Think Before Coding** | State assumptions, surface tradeoffs, ask when unclear | Gran-Mestre sempre declara suposições antes de agir |
| 2 | **Simplicity First** | Minimum code, no speculative features, no overcomplication | Anti-padrão: 200 linhas quando 50 bastam |
| 3 | **Surgical Changes** | Touch only what must, clean up only your own mess | Subagents editam apenas escopo declarado |
| 4 | **Goal-Driven Execution** | Define success criteria, loop until verified | Cada task tem critério de sucesso verificável |
| 5 | **Push Back** | When simpler approach exists, say so. When unclear, stop | Subagents podem questionar o Gran-Mestre |

### Princípios Karpathy (helenizados)

```
1. Não assumir — declarar suposições explicitamente
2. Não esconder confusão — nomear o que é confuso
3. Não complicar — código mínimo que resolve o problema
4. Não tocar o que não deve — mudanças cirúrgicas
5. Definir sucesso — critérios verificáveis antes de executar
```

---

## 2. DEEPSEEK-AI/DEEPSPEC

### Padrões Extraídos (4)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 6 | **Speculative Decoding** | Draft model + target model para acelerar inferência | Gran-Mestre pode usar drafts rápidos + verificação final |
| 7 | **Multi-Model Evaluation** | 9 benchmarks (gsm8k, math500, humaneval, etc.) | Avaliar subagentes em múltiplos benchmarks |
| 8 | **Pipeline de 3 estágios** | Data Prep → Training → Evaluation | Pipeline Gran-Mestre: Discovery → Execution → Validation |
| 9 | **Custom JSON Encoder** | Serialização customizada para tipos complexos | Gran-Mestre pode usar JSON custom para outputs |

### Arquitetura DeepSpec

```
deepspec/
├── modeling/     # DSpark, Eagle3 (draft models)
├── trainer/      # base, dspark, eagle3 trainers
├── eval/         # Evaluators por modelo
├── data/         # Data preparation
└── utils/        # Utilities
```

---

## 3. COREBUNCH/INSTATIC

### Padrões Extraídos (6)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 10 | **Agent Rule Book** | CLAUDE.md como regra absoluta para agents | Gran-Mestre tem ARCHITECTURE.md como regra |
| 11 | **PR Conventions** | Branch naming, conventional commits, draft PRs | Subagents seguem convenções de PR |
| 12 | **No Agent-Branded Branches** | Nunca `codex/...` ou `claude/...` | Branches genéricos, não agent-specific |
| 13 | **Protected Main** | Nunca push direto para main | Safety protocol impede push direto |
| 14 | **Smoke Tests Locais** | Seed data local, nunca propagar para prod | Testes com dados locais isolados |
| 15 | **Architecture Docs** | docs/architecture.md como referência | Gran-Mestre tem ARCHITECTURE.md |

### Convenções Instatic (helenizadas)

```
Branches: feat/..., fix/..., refactor/..., chore/..., docs/..., test/...
PR titles: <type>(<scope>): <summary>
Draft PRs: padrão (não ready-for-review)
Escopo: coerente, não misturar cleanup com feature
```

---

## 4. NEXU-IO/OPEN-DESIGN

### Padrões Extraídos (8)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 16 | **164 Skills** | Maior catálogo de skills conhecido | Referência para criação de skills |
| 17 | **Skills vs Design Templates** | Split: functional skills vs renderable templates | Gran-Mestre separa skills de templates |
| 18 | **Daemon Plumbing** | `/api/skills` endpoint, lazy scanner | Skills discoverable via API |
| 19 | **User-Imported Skills Shadow** | Skills do usuário sobrescrevem built-in | Hierarquia: user > built-in |
| 20 | **Curated Catalogue** | Skills de `awesome-agent-skills` como stubs | Catálogo curado de skills externas |
| 21 | **Multi-App Architecture** | apps/web, apps/daemon, apps/desktop, apps/packaged | Arquitetura multi-app |
| 22 | **Craft Rules** | Universal brand-agnostic craft rules | Regras de craft compartilháveis |
| 23 | **Mock CLIs** | Mocks para opencode/claude/codex/gemini/etc. | Testes com mocks de CLIs |

### Skills Catalogue (164 skills)

```
8-bit-orbit-video-template, ad-creative, after-hours-editorial-template,
agent-browser, ai-music-album, algorithmic-art, apple-hig,
article-magazine, artifacts-builder, ...
```

---

## 5. RUVNET/RUFLO

### Padrões Extraídos (7)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 24 | **Agent Federation** | 16 agent roles + custom types | Gran-Mestre tem 61 subagents |
| 25 | **314 MCP Tools** | Maior catálogo de MCP tools conhecido | Referência para MCP tools |
| 26 | **19 AgentDB Controllers** | Controllers por domínio | Controllers por domínio de subagent |
| 27 | **21 Native Plugins** | Plugins nativos | Plugins para Gran-Mestre |
| 28 | **LEDGER Pattern** | claude-flow = LEDGER (state, memory, coordination) | Gran-Mestre como ledger de estado |
| 29 | **EXECUTOR Pattern** | Codex = EXECUTOR (code, commands, files) | Subagents como executors |
| 30 | **Memory Search First** | ALWAYS search memory BEFORE starting | Gran-Mestre busca memória antes de agir |

### Arquitetura Ruflo

```
ruflo/
├── crates/ruflo-federation-peer/  # Federation peer
├── bin/cli.js                     # CLI entry
├── agentdb.rvf                    # Agent database
└── CLAUDE.md                      # Agent rules
```

---

## 6. KNOCKOUTEZ/WIGOLO

### Padrões Extraídos (5)

| # | Padrão | Descrição | Helenização |
|---|--------|-----------|-------------|
| 31 | **Local-First Web Intelligence** | No keys, no cloud, no metered bill | Gran-Mestre: local-first, sem dependências externas |
| 32 | **MCP Server** | Servidor MCP para web intelligence | MCP server para Gran-Mestre |
| 33 | **Multi-Agent Compat** | Claude Code, Cursor, Codex, Gemini, VS Code, etc. | Gran-Mestre compatível com todos |
| 34 | **11 Skills Modular** | wigolo, wigolo-agent, wigolo-cache, etc. | Skills modulares por função |
| 35 | **REST API + MCP** | Dual interface: REST + MCP | Gran-Mestre: REST + MCP |

### Skills Wigolo

```
wigolo           # Core web intelligence
wigolo-agent     # Agent integration
wigolo-cache     # Caching layer
wigolo-crawl     # Web crawling
wigolo-diff      # Diff detection
wigolo-extract   # Content extraction
wigolo-fetch     # Fetching
wigolo-find-similar  # Similarity search
wigolo-research  # Research
wigolo-search    # Search
wigolo-watch     # Watching
```

---

## Resumo: 35 Padrões por Categoria

| Categoria | Padrões | Exemplos |
|-----------|---------|----------|
| **Behavioral** | 5 | Think Before Coding, Simplicity First, Surgical Changes |
| **Architecture** | 8 | Agent Federation, Multi-App, LEDGER/EXECUTOR |
| **Skills** | 7 | 164 skills catalogue, Skills vs Templates, Curated |
| **Pipeline** | 4 | Speculative Decoding, 3-stage pipeline, Memory First |
| **Conventions** | 6 | PR Conventions, Protected Main, No Agent-Branded |
| **Tools** | 5 | 314 MCP Tools, REST + MCP, Mock CLIs |
| **Total** | **35** | |

---

## Top 5 para Implementação Imediata

| # | Padrão | Repo | Ação |
|---|--------|------|------|
| 1 | Think Before Coding | karpathy | Integrar como regra global do Gran-Mestre |
| 2 | Memory Search First | ruflo | Gran-Mestre busca memória antes de agir |
| 3 | PR Conventions | Instatic | Subagents seguem convenções de PR |
| 4 | Skills vs Templates | open-design | Separar skills de templates |
| 5 | Local-First | wigolo | Gran-Mestre: local-first, sem dependências |

---

**Versão:** 1.0.0
**Data:** 2026-07-27
**Repos:** 6
**Padrões:** 35
**Pipeline:** MIX
