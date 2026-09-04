# INVENTÁRIO COMPLETO — Ecossistema OpenCode

**Data:** 2026-08-02 | **Versão Registry:** 2.1.0 | **Modo:** MIX

---

## 1. AGENT PRIMÁRIO (1)

| Agent | Mode | Modelo | Função |
|-------|------|--------|--------|
| **gran-mestre** | `primary` | omniroute/auto/best-free | Meta-orquestrador — ponto de entrada único para todas as requisições |

---

## 2. PIPELINE SUBAGENTS (6)

| # | Subagent | Fase | Função |
|---|----------|------|--------|
| 1 | **prometheus** | 3 (DESC) | Planejamento modo entrevista — requisitos e decomposição |
| 2 | **hestia** | 2, 3, 6 | Validação de rastreabilidade requisito↔spec |
| 3 | **atlas** | 4 (EXEC) | Execução orquestrada — coordenação de waves paralelas |
| 4 | **atena** | 5 (REV) | Revisão macro — coerência cross-task, acoplamento, arquitetura |
| 5 | **atreus** | 6 (ENTR) | Entrega — verificação final e handoff |
| 6 | **code-reviewer** | 4 (EXEC) | Code review por linguagem — qualidade, segurança, lint |

---

## 3. CROSSOVER SUBAGENTS — oh-my-openagents (8)

| # | Subagent | Função |
|---|----------|--------|
| 7 | **explore** | Busca rápida de código — grep, pattern, file-discovery |
| 8 | **librarian** | Documentação e referências — APIs, bibliotecas, contexto externo |
| 9 | **oracle** | Arquitetura e debug — raciocínio de alto nível, design |
| 10 | **metis** | Consultor pré-planejamento — análise de ambiguidades e riscos |
| 11 | **sisyphus** | Orquestrador principal — coordenação de workflow geral |
| 12 | **hephaestus** | Executor autônomo — implementação e build |
| 13 | **general** | Uso geral — fallback e catch-all |
| 14 | **build** | Desenvolvimento — coding, implementação, compilação |

---

## 4. CROSSOVER SUBAGENTS — Superpowers (6)

| # | Subagent | Função |
|---|----------|--------|
| 15 | **superpowers-brainstorming** | Ideação socrática — pensamento divergente e exploração |
| 16 | **superpowers-plan-writer** | Planos TDD — tasks bite-sized e decomponíveis |
| 17 | **superpowers-implementer** | Execução delegada — TDD red-green |
| 18 | **superpowers-code-reviewer** | Code review — qualidade e padrões |
| 19 | **superpowers-spec-writer** | Especificações — contratos e critérios de aceite |
| 20 | **superpowers-verification** | Verificação — validação e cobertura de testes |

---

## 5. CROSSOVER SUBAGENTS — Fable Method (3)

| # | Subagent | Função |
|---|----------|--------|
| 21 | **fable-method** | Classificação (Step 0) — triagem e complexidade |
| 22 | **fable-loop** | Orquestração completa — loop iterativo de refinamento |
| 23 | **fable-judge** | Verificação adversarial — detecção de falsos positivos |

---

## 6. GSD SUBAGENTS (35)

### Planejamento e Roadmap (5)

| # | Subagent | Função |
|---|----------|--------|
| 24 | **gsd-planner** | Criar planos de fase — decomposição e milestones |
| 25 | **gsd-roadmapper** | Criar roadmap — timeline e dependências |
| 26 | **gsd-plan-checker** | Verificar plano — análise goal-backward pré-execução |
| 27 | **gsd-assumptions-analyzer** | Analisar suposições — riscos e pré-condições ocultas |
| 28 | **gsd-framework-selector** | Selecionar framework — matriz de decisão e comparação |

### Execução e Código (4)

| # | Subagent | Função |
|---|----------|--------|
| 29 | **gsd-executor** | Executar planos — waves, commits atômicos, estado |
| 30 | **gsd-code-reviewer** | Revisar código — bugs, segurança, padrões |
| 31 | **gsd-code-fixer** | Corrigir código — patches automatizados |
| 32 | **gsd-pattern-mapper** | Mapear padrões — analogias e closest-match |

### Debug e Investigação (2)

| # | Subagent | Função |
|---|----------|--------|
| 33 | **gsd-debugger** | Debugar — hipóteses e root-cause |
| 34 | **gsd-debug-session-manager** | Gerenciar sessões de debug — checkpoints e continuação |

### Documentação (5)

| # | Subagent | Função |
|---|----------|--------|
| 35 | **gsd-doc-writer** | Documentar — README, markdown |
| 36 | **gsd-doc-classifier** | Classificar documentos — ADR, PRD, SPEC |
| 37 | **gsd-doc-synthesizer** | Sintetizar documentos — consolidação e dedup |
| 38 | **gsd-doc-verifier** | Verificar documentos — acurácia factual |
| 39 | **gsd-intel-updater** | Atualizar intel — snapshot do codebase |

### Pesquisa (5)

| # | Subagent | Função |
|---|----------|--------|
| 40 | **gsd-phase-researcher** | Pesquisar fase — estratégia de implementação |
| 41 | **gsd-project-researcher** | Pesquisar projeto — ecossistema e landscape |
| 42 | **gsd-research-synthesizer** | Sintetizar pesquisa — consolidação de achados |
| 43 | **gsd-domain-researcher** | Pesquisar domínio — contexto de negócio |
| 44 | **gsd-ai-researcher** | Pesquisar IA — frameworks e LLMs |

### Avaliação e Auditoria (4)

| # | Subagent | Função |
|---|----------|--------|
| 45 | **gsd-eval-planner** | Planejar avaliação — métricas e rubricas |
| 46 | **gsd-eval-auditor** | Auditar avaliação — cobertura e remediação |
| 47 | **gsd-security-auditor** | Auditar segurança — vulnerabilidades e threat-model |
| 48 | **gsd-nyquist-auditor** | Auditar Nyquist — gaps de validação |

### UI/UX (3)

| # | Subagent | Função |
|---|----------|--------|
| 49 | **gsd-ui-auditor** | Auditar UI — visual, design, a11y, responsividade |
| 50 | **gsd-ui-checker** | Verificar UI — aderência ao spec |
| 51 | **gsd-ui-researcher** | Pesquisar UI — padrões e componentes |

### Integração e Verificação (4)

| # | Subagent | Função |
|---|----------|--------|
| 52 | **gsd-integration-checker** | Verificar integração — conectividade E2E |
| 53 | **gsd-verifier** | Verificar fase — validação e aceite |
| 54 | **gsd-codebase-mapper** | Mapear codebase — arquitetura e dependências |
| 55 | **gsd-mempalace-curator** | Curar MemPalace — diário de sessão e KG temporal |

### Usuário e Perfil (2)

| # | Subagent | Função |
|---|----------|--------|
| 56 | **gsd-user-profiler** | Perfil do usuário — análise comportamental |
| 57 | **gsd-advisor-researcher** | Pesquisar decisões — tradeoffs e comparações |

---

## 7. OPENCODE SUBAGENTS (3)

| # | Subagent | Função |
|---|----------|--------|
| 58 | **memory-keeper** | Memória persistente (Obsidian) — consciência e vault neural |
| 59 | **reverser** | Engenharia reversa (Ghidra) — decompilação e análise de firmware |
| 60 | **general** | Uso geral — fallback omniroute |

---

## 8. SKILLS (13)

### Skills .opencode/skills/ (10)

| Skill | Função | Tags |
|-------|--------|------|
| **gran-mestre** | Meta-orquestração — pipeline 6 fases, 4 gates, Dev Loop 3 níveis | orchestrator, meta, pipeline |
| **hestia** | Validação de conformidade — rastreabilidade requisito↔spec | validation, compliance, audit |
| **athena** | Revisão macro — composição Oracle pós-hoc | review, macro, architecture |
| **pxpipe** | Redução de tokens — contexto volumoso como PNG (economia 59-70%) | optimization, tokens, context |
| **agent-reach** | Pesquisa na internet — 15 plataformas, multi-backend | research, web, search, social |
| **archify** | Diagramas de arquitetura — HTML interativo com SVG | diagrams, architecture, visualization |
| **browser-use** | Automação de navegador — Playwright + Gran-Mestre | browser, automation, scraper |
| **ck** | Memória persistente de projeto — auto-load de contexto | memory, project, context |
| **fable-judge** | Verificação adversarial — re-executa cada verificação afirmada | audit, verification, adversarial |
| **dev-loop** | Loop de desenvolvimento 3 níveis — ReAct, Mini Loop, Human Loop | dev, loop, react, iterative |

### Skills .claude/skills/ (3)

| Skill | Função | Tags |
|-------|--------|------|
| **agent-reach** | (espelho) Pesquisa na internet | research, web, search |
| **ck** | (espelho) Memória persistente de projeto | memory, project, context |
| **ecc-autofagia** | Autofagia (self-digestion) para ECC | autofagia, self-healing, meta |

### Comandos GSD (50+)

| Comando | Função |
|---------|--------|
| `/gsd-plan-phase` | Criar plano detalhado da fase (PLAN.md) |
| `/gsd-execute-phase` | Executar planos com waves paralelas |
| `/gsd-discuss-phase` | Coletar contexto da fase via perguntas adaptativas |
| `/gsd-code-review` | Revisar arquivos alterados na fase |
| `/gsd-debug` | Debug sistemático com estado persistente |
| `/gsd-verify-work` | Validar features via UAT conversacional |
| `/gsd-capture` | Capturar ideias, tasks, notas e seeds |
| `/gsd-explore` | Ideação socrática e roteamento de ideias |
| `/gsd-spike` | Exploração experiencial de ideias |
| `/gsd-sketch` | Sketch de UI com mockups HTML descartáveis |
| `/gsd-stats` | Estatísticas do projeto |
| `/gsd-progress` | Verificar progresso e avançar workflow |
| `/gsd-manager` | Centro de comando interativo para fases |
| `/gsd-autonomous` | Executar fases restantes autonomamente |
| `/gsd-fast` | Executar task trivial inline |
| `/gsd-quick` | Executar task rápida com garantias GSD |
| `/gsd-import` | Ingerir planos externos com detecção de conflitos |
| `/gsd-ingest-docs` | Bootstrap de .planning/ a partir de docs existentes |
| `/gsd-new-project` | Inicializar novo projeto com PROJECT.md |
| `/gsd-new-milestone` | Iniciar novo ciclo de milestone |
| `/gsd-complete-milestone` | Arquivar milestone e preparar próxima versão |
| `/gsd-ship` | Criar PR após verificação passar |
| `/gsd-pr-branch` | Criar branch limpa para PR |
| `/gsd-undo` | Revert seguro via git |
| `/gsd-pause-work` | Criar handoff de contexto ao pausar |
| `/gsd-resume-work` | Retomar trabalho de sessão anterior |
| `/gsd-thread` | Gerenciar threads de contexto persistentes |
| `/gsd-workstreams` | Gerenciar workstreams paralelas |
| `/gsd-workspace` | Gerenciar workspaces isolados |
| `/gsd-config` | Configurar settings do GSD |
| `/gsd-settings` | Configurar toggles e perfil de modelo |
| `/gsd-health` | Diagnosticar saúde do diretório .planning/ |
| `/gsd-help` | Mostrar guia de comandos disponíveis |
| `/gsd-update` | Atualizar GSD para última versão |
| `/gsd-surface` | Alternar skills visíveis |
| `/gsd-profile-user` | Gerar perfil comportamental do dev |
| `/gsd-graphify` | Construir knowledge graph do projeto |
| `/gsd-map-codebase` | Analisar codebase com agents paralelos |
| `/gsd-mempalace-capture` | Arquivar artefato no MemPalace |
| `/gsd-mempalace-recall` | Recuperar decisões do MemPalace |
| `/gsd-add-tests` | Gerar tests para fase concluída |
| `/gsd-validate-phase` | Auditar gaps de validação Nyquist |
| `/gsd-audit-fix` | Pipeline autônomo audit→fix |
| `/gsd-audit-milestone` | Auditar conclusão de milestone |
| `/gsd-audit-uat` | Auditoria cross-phase de UAT |
| `/gsd-eval-review` | Auditar cobertura de avaliação de fase IA |
| `/gsd-ai-integration-phase` | Gerar AI-SPEC.md para fases com IA |
| `/gsd-ui-phase` | Gerar UI-SPEC.md para fases frontend |
| `/gsd-ui-review` | Auditoria visual retroativa de 6 pilares |
| `/gsd-spec-phase` | Clarificar WHAT com ambiguity scoring |
| `/gsd-mvp-phase` | Planejar fase como MVP slice vertical |
| `/gsd-ultraplan-phase` | Offload plano para cloud ultraplan |
| `/gsd-plan-review-convergence` | Convergência cross-AI de planos |
| `/gsd-review` | Peer review cross-AI de planos |
| `/gsd-review-backlog` | Revisar e promover backlog |
| `/gsd-extract-learnings` | Extrair lições de artefatos concluídos |
| `/gsd-milestone-summary` | Gerar resumo completo do milestone |
| `/gsd-forensics` | Investigação post-mortem de falhas |
| `/gsd-docs-update` | Gerar/atualizar documentação |
| `/gsd-cleanup` | Arquivar diretórios de fases acumuladas |
| `/gsd-secure-phase` | Verificar ameaças retroativamente |
| `/gran-mestre` | Pipeline completo Gran-Mestre |

---

## 9. MCPs (2)

| MCP | Função | URL/Config |
|-----|--------|------------|
| **ghidra** | Engenharia reversa — decompilação de binários/firmware/BIOS | `http://127.0.0.1:8080/mcp` (remote) |
| **context7** | Documentação de bibliotecas — APIs atualizadas | Integrado via tool `context7_resolve-library-id` + `context7_query-docs` |

---

## 10. LSPs (4)

| LSP | Linguagens | Função |
|-----|-----------|--------|
| **typescript-language-server** | TypeScript, TSX, JavaScript | Diagnósticos, go-to-definition, find-references, rename |
| **basedpyright** | Python | Type checking avançado, análise estática |
| **rust-analyzer** | Rust | Análise de ownership, lifetimes, borrow checker |
| **gopls** | Go | Análise estática, navegação de código |

---

## 11. HOOKS (20)

### Hooks GSD (.config/opencode/hooks/)

| Hook | Tipo | Função |
|------|------|--------|
| **gsd-check-update.js** | session-start | Verifica atualizações disponíveis do GSD |
| **gsd-check-update-worker.js** | worker | Worker de verificação de updates |
| **gsd-config-reload.js** | config-change | Recarrega configuração ao mudar settings |
| **gsd-context-monitor.js** | context | Monitora uso de contexto e alerta |
| **gsd-cursor-post-tool.js** | post-tool | Hook pós-tool para Cursor |
| **gsd-cursor-session-start.js** | session-start | Inicialização de sessão Cursor |
| **gsd-ensure-canonical-path.js** | pre-read | Garante caminhos canônicos antes de ler |
| **gsd-graphify-update.sh** | post-commit | Atualiza knowledge graph após commits |
| **gsd-phase-boundary.sh** | phase-boundary | Valida transições entre fases |
| **gsd-prompt-guard.js** | pre-prompt | Protege contra injeção de prompts |
| **gsd-read-guard.js** | pre-read | Protege leituras sensíveis |
| **gsd-read-injection-scanner.js** | pre-read | Escaneia injeção em arquivos lidos |
| **gsd-session-state.sh** | session | Gerencia estado de sessão |
| **gsd-statusline.js** | statusline | Atualiza barra de status com progresso |
| **gsd-update-banner.js** | session-start | Mostra banner de atualização |
| **gsd-validate-commit.sh** | pre-commit | Valida mensagens de commit |
| **gsd-workflow-guard.js** | pre-action | Protege contra ações fora de workflow |
| **gsd-worktree-path-guard.js** | pre-action | Valida caminhos de worktree |
| **managed-hooks-registry.cjs** | registry | Registro central de hooks gerenciados |

---

## 12. PLUGINS (2)

| Plugin | Função |
|--------|--------|
| **oh-my-openagent** | Framework de agents — fornece explore, librarian, oracle, metis, sisyphus, hephaestus, build, general, superpowers, prometheus, momus, multimodal-looker |
| **model-guide** | Guia de modelos — sugere modelos ideais por task |

---

## 13. PROVIDERS DE MODELOS (3)

| Provider | Tipo | Modelos Disponíveis |
|----------|------|---------------------|
| **local** (Ollama) | OpenAI-compatible | qwen-coder-30b, qwen2.5-coder:7b, qwen3.5-27b |
| **omniroute** | OpenAI-compatible | auto/best-coding, auto/best-reasoning, auto/best-fast, auto/best-vision, auto/best-chat, auto/pro-coding, auto/pro-reasoning, auto/pro-vision, auto/pro-chat, auto/pro-fast, auto/coding, auto/fast, auto/chat, auto/cheap, auto/offline, auto/smart, auto/claude-opus, auto/claude-sonnet, auto/best-free, auto/coding:fast, auto/coding:cheap, auto/coding:free, auto/coding:pro, auto/coding:reliable, auto/reasoning, auto/reasoning:pro, auto/vision, auto/multimodal, auto/glm, auto/minimax, auto/mimo, auto/zai, auto/gemma |
| **opencode** | OpenAI-compatible | big-pickle, deepseek-v4-flash-free, glm-5.2 (via oh-my-openagent) |

---

## 14. RESUMO NUMÉRICO

| Categoria | Quantidade |
|-----------|------------|
| Agent Primário | 1 |
| Pipeline Subagents | 6 |
| Crossover Subagents (oh-my-openagents) | 8 |
| Crossover Subagents (Superpowers) | 6 |
| Crossover Subagents (Fable Method) | 3 |
| GSD Subagents | 35 |
| OpenCode Subagents | 3 |
| **Total Subagents** | **61** |
| Skills (.opencode) | 10 |
| Skills (.claude) | 3 |
| Comandos (/gsd-*) | 50+ |
| **Total Skills/Comandos** | **63+** |
| MCPs | 2 |
| LSPs | 4 |
| Hooks | 20 |
| Plugins | 2 |
| Providers | 3 |
| Modelos disponíveis | 35+ |

---

## 15. ARQUITETURA DE ORQUESTRAÇÃO

```
GRAN-MESTRE (primário) — ponto de entrada único
  ├── Pipeline Subagents (6): prometheus, hestia, atlas, atena, atreus, code-reviewer
  ├── Crossover Subagents (16): oh-my-openagents, superpowers, fable-method
  ├── GSD Subagents (35): gsd-planner, gsd-executor, gsd-code-reviewer, etc.
  ├── OpenCode Subagents (3): memory-keeper, reverser, general
  └── External Subagents: via oh-my-openagent plugin
  TOTAL: 61 subagents
```

### Hierarquia de Roteamento

```
1. Rota exata (subagent nomeado) → encaminha direto
2. Rota por tipo (skill declarada) → Héstia valida
3. Rota por classificação → Prometheus analisa
4. Fallback → pergunta ao usuário
5. Rejeição → "não sei fazer isso"
```

### Safety Protocol

```
SHA → Héstia → Atena → Fable Judge → Rollback
```

### Pipeline 6 Fases

```
FASE 1: DESCOBERTA     → Prometheus + Fable Loop + Brainstorming
FASE 2: CONTRATO        → Spec Writer + Héstia + Fable Judge
FASE 3: PLANO           → Plan Writer + Fable Loop + Héstia
FASE 4: EXECUÇÃO        → Atlas + Fable Loop + Implementer + Code Reviewer
FASE 5: REVISÃO MACRO   → Atena + Fable Judge
FASE 6: ENTREGA         → Verification + Héstia + Fable Judge
```

### Dev Loop — 3 Níveis

```
Nível 1: ReAct      → Tasks pequenas (1-3 arquivos) — ciclo pensa→age→observa
Nível 2: Mini Loop   → Features locais (1 módulo) — spec→plano→implementa→verifica
Nível 3: Human Loop  → Épicos e ciclos longos — decide→consulta→triagem→planeja→PR
```

### Modos de Execução

| Modo | Uso | Algoritmo |
|------|-----|-----------|
| **FEATURE** | Features com design em aberto | Pipeline 6 fases + 4 gates + consulta registry |
| **COMPLEX** | Tasks que precisam de múltiplos recursos | Consulta registry por tags → ativa todos compatíveis |
| **CRITICAL** | Alta segurança/importância | Consulta registry + Safety Protocol + Fable Judge em cada gate |
| **MIX** | Modo máximo (COMPLEX+CRITICAL+FEATURE) | Pipeline completo + delegação dinâmica + todos recursos compatíveis |

---

**Gran-Mestre = único agent primário.** Todo o resto é subagent descartável com contexto isolado, orquestrado dinamicamente via Registry por tags de capacidade.
