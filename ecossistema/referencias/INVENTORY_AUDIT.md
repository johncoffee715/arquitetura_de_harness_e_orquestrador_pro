# INVENTÁRIO COMPLETO PARA AUDITORIA
## Gran-Mestre Harness — OpenCode
### Data: 2026-07-27 | v4.0.0

---

## RESUMO EXECUTIVO

| Categoria | Total | Status |
|-----------|-------|--------|
| Agents | 46 | ✅ Todos com model_rotation |
| Skills | 87 | ✅ Todos com SKILL.md |
| Hooks | 18 | ✅ Funcionais |
| Commands | 72 | ✅ Registrados |
| MCPs | 5 | ✅ Configurados |
| Providers | 2 (100 modelos) | ✅ Ativos |
| Integrações | 10 | ✅ Absorvidas |
| Pipeline Modes | 6 | ✅ Documentados |
| Symlinks | 7 | ✅ Portáveis |
| Permissões | 6 | ✅ Configuradas |

---

## 1. AGENTS (46 total)

### 1.1 Agent Primário (1)

| Agent | Modelo | Fallback Chain | Descrição |
|-------|--------|----------------|-----------|
| gran-mestre | claude-opus-4.7 | 5 fallbacks | Meta-orquestrador senior. Ponto de entrada único. Analisa complexidade, roteia (TRIVIAL→FEATURE), delega para agents especializados. Gerencia pipeline completo (6 fases) com safety protocol, rollback automático e Shared Brain. |

### 1.2 Gran-Mestre Pipeline (6)

| Agent | Modelo | Fallback | Descrição |
|-------|--------|----------|-----------|
| prometheus | claude-opus-4.7 | 5 fallbacks | Planejador — decomposição de tarefas |
| hestia | claude-opus-4.7 | 5 fallbacks | Validador — valida specs, planos e entregas contra pedido original |
| atlas | claude-opus-4.7 | 5 fallbacks | Executor — implementa conforme plano |
| athena | claude-opus-4.7 | 5 fallbacks | Revisão macro — diff total, coerência cross-task |
| atreus | claude-opus-4.7 | 5 fallbacks | Entrega — relatório final |
| code-reviewer | claude-opus-4.7 | 5 fallbacks | Code review por linguagem |

### 1.3 Superpowers (7)

| Agent | Modelo | Descrição |
|-------|--------|-----------|
| superpowers | claude-opus-4.7 | Orquestrador superpowers |
| superpowers-code-reviewer | claude-opus-4.7 | Revisor de código |
| superpowers-implementer | claude-opus-4.7 | Implementador |
| superpowers-plan-writer | claude-opus-4.7 | Escritor de planos |
| superpowers-plan-writer-alt1 | claude-opus-4.7 | Escritor de planos (alternativa 1) |
| superpowers-plan-writer-alt2 | claude-opus-4.7 | Escritor de planos (alternativa 2) |
| superpowers-spec-writer | claude-opus-4.7 | Escritor de especificações |

### 1.4 GSD Legacy (30)

| Agent | Descrição |
|-------|-----------|
| gsd-advisor-researcher | Researches single gray area decision |
| gsd-ai-researcher | Researches AI frameworks official docs |
| gsd-assumptions-analyzer | Deeply analyzes codebase for assumptions |
| gsd-codebase-mapper | Explores codebase and writes analysis |
| gsd-code-fixer | Applies fixes to code review findings |
| gsd-code-reviewer | Reviews source files for bugs/security |
| gsd-debugger | Investigates bugs using scientific method |
| gsd-debug-session-manager | Manages multi-cycle debug checkpoints |
| gsd-doc-classifier | Classifies planning documents |
| gsd-doc-synthesizer | Synthesizes classified docs |
| gsd-doc-verifier | Verifies factual claims in docs |
| gsd-doc-writer | Writes and updates documentation |
| gsd-domain-researcher | Researches business domain |
| gsd-eval-auditor | Retroactive audit of AI phase evaluation |
| gsd-eval-planner | Designs evaluation strategy |
| gsd-executor | Executes GSD plans with atomic commits |
| gsd-framework-selector | Interactive AI/LLM framework decision |
| gsd-integration-checker | Verifies cross-phase integration |
| gsd-intel-updater | Analyzes codebase for intel files |
| gsd-mempalace-curator | Ship-time MemPalace curation |
| gsd-nyquist-auditor | Fills Nyquist validation gaps |
| gsd-pattern-mapper | Analyzes codebase for patterns |
| gsd-phase-researcher | Researches phase implementation |
| gsd-plan-checker | Verifies plans will achieve goals |
| gsd-planner | Creates executable phase plans |
| gsd-project-researcher | Researches domain ecosystem |
| gsd-research-synthesizer | Synthesizes research outputs |
| gsd-roadmapper | Creates project roadmaps |
| gsd-security-auditor | Verifies threat mitigations |
| gsd-ui-auditor | 6-pillar visual audit |
| gsd-ui-checker | Validates UI-SPEC.md contracts |
| gsd-ui-researcher | Produces UI-SPEC.md design |
| gsd-user-profiler | Analyzes session messages |
| gsd-verifier | Verifies phase goal achievement |

### 1.5 Outros (2)

| Agent | Descrição |
|-------|-----------|
| memory-keeper | Gerencia memória persistente integrada ao Obsidian |
| reverser | Engenharia reversa de binários/firmware/BIOS via GhidraMCP |

---

## 2. SKILLS (87 total)

### 2.1 Gran-Mestre Core (10) — ~/.opencode/skills/

| Skill | Descrição | Status |
|-------|-----------|--------|
| gran-mestre | Meta-orquestrador — ponto de entrada único | ✅ |
| hestia | Validador — valida specs, planos e entregas | ✅ |
| athena | Revisão macro — diff total, coerência | ✅ |
| fable-judge | Verificação adversarial de trabalho concluído | ✅ |
| agent-reach | Pesquisa em 15 plataformas (search/social/career/dev) | ✅ |
| archify | Diagramas de arquitetura como HTML interativo | ✅ |
| browser-use | Automação de navegador via AI Agent | ✅ |
| ck | Memória persistente por projeto | ✅ |
| pxpipe | Proxy local que reduz tokens de entrada (59-70%) | ✅ |
| security-review | Auditoria de segurança de codebase | ✅ |

### 2.2 GSD Core (67) — ~/.config/opencode/skills/

| Skill | Descrição |
|-------|-----------|
| graphify | Knowledge graph com god nodes, community detection |
| gsd-add-tests | Generate tests for completed phase |
| gsd-ai-integration-phase | Generate AI-SPEC.md for AI phases |
| gsd-audit-fix | Autonomous audit-to-fix pipeline |
| gsd-audit-milestone | Audit milestone completion |
| gsd-audit-uat | Cross-phase UAT audit |
| gsd-autonomous | Run all remaining phases autonomously |
| gsd-capture | Capture ideas, tasks, notes |
| gsd-cleanup | Archive phase directories |
| gsd-code-review | Review source files for bugs |
| gsd-complete-milestone | Archive completed milestone |
| gsd-config | Configure GSD settings |
| gsd-debug | Systematic debugging |
| gsd-discuss-phase | Gather phase context |
| gsd-docs-update | Generate/update documentation |
| gsd-eval-review | Audit AI phase evaluation |
| gsd-execute-phase | Execute plans with wave parallelization |
| gsd-explore | Socratic ideation and routing |
| gsd-extract-learnings | Extract decisions and patterns |
| gsd-fast | Execute trivial task inline |
| gsd-forensics | Post-mortem investigation |
| gsd-graphify | Build/query knowledge graph |
| gsd-health | Diagnose planning directory health |
| gsd-help | Show available GSD commands |
| gsd-import | Ingest external plans |
| gsd-inbox | Triage GitHub issues/PRs |
| gsd-ingest-docs | Bootstrap from existing docs |
| gsd-manager | Interactive command center |
| gsd-map-codebase | Analyze codebase with parallel mappers |
| gsd-mempalace-capture | File artifact into MemPalace |
| gsd-mempalace-recall | Recall from MemPalace |
| gsd-milestone-summary | Generate project summary |
| gsd-mvp-phase | Plan phase as MVP slice |
| gsd-new-milestone | Start new milestone cycle |
| gsd-new-project | Initialize new project |
| gsd-ns-context | Codebase intel |
| gsd-ns-ideate | Exploration capture |
| gsd-ns-manage | Config workspace |
| gsd-ns-project | Project lifecycle |
| gsd-ns-review | Quality gates |
| gsd-ns-workflow | Workflow management |
| gsd-pause-work | Create context handoff |
| gsd-phase | CRUD for phases |
| gsd-plan-phase | Create detailed phase plan |
| gsd-plan-review-convergence | Cross-AI plan convergence |
| gsd-pr-branch | Create clean PR branch |
| gsd-profile-user | Generate developer profile |
| gsd-progress | Check progress, advance workflow |
| gsd-quick | Execute quick task |
| gsd-resume-work | Resume from previous session |
| gsd-review | Request cross-AI peer review |
| gsd-review-backlog | Review and promote backlog |
| gsd-secure-phase | Verify threat mitigations |
| gsd-settings | Configure workflow toggles |
| gsd-ship | Create PR, run review |
| gsd-sketch | Sketch UI/design ideas |
| gsd-spec-phase | Clarify WHAT a phase delivers |
| gsd-spike | Spike an idea |
| gsd-stats | Display project statistics |
| gsd-surface | Toggle surfaced skills |
| gsd-thread | Manage persistent context threads |
| gsd-ui-phase | Generate UI design contract |
| gsd-ui-review | 6-pillar visual audit |
| gsd-ultraplan-phase | Offload plan to ultraplan cloud |
| gsd-undo | Safe git revert |
| gsd-update | Update GSD to latest |
| gsd-validate-phase | Audit Nyquist validation gaps |
| gsd-verify-work | Validate through UAT |
| gsd-workspace | Manage workspaces |
| gsd-workstreams | Manage parallel workstreams |

### 2.3 Superpowers (6) — ~/.config/opencode/skills/

| Skill | Descrição |
|-------|-----------|
| superpowers-brainstorming | Socratic ideation before design |
| superpowers-executing-plans | Carrying out approved plans |
| superpowers-subagent-driven-development | Execution with delegated tasks |
| superpowers-using-superpowers | Skill usage discipline |
| superpowers-verification-before-completion | Verification before claims |
| superpowers-writing-plans | Writing implementation plans |

### 2.4 OpenClaude Absorvido (3) — REGISTRY_OPENCLAUDE.md

| Skill | Descrição |
|-------|-----------|
| oc-background-sessions | Sessões desacopladas (--bg) |
| oc-provider-profiles | Sistema de profiles para 200+ providers |
| oc-doctor-runtime | Diagnósticos e privacy verification |

---

## 3. HOOKS (18 total)

| Hook | Tipo | Descrição |
|------|------|-----------|
| gsd-check-update.js | JS | Verifica atualizações do GSD |
| gsd-check-update-worker.js | JS | Worker de verificação de updates |
| gsd-config-reload.js | JS | Recarrega configuração |
| gsd-context-monitor.js | JS | Monitora contexto da sessão |
| gsd-cursor-post-tool.js | JS | Pós-execução de tool no Cursor |
| gsd-cursor-session-start.js | JS | Início de sessão no Cursor |
| gsd-ensure-canonical-path.js | JS | Garante path canônico |
| gsd-graphify-update.sh | Shell | Atualiza knowledge graph |
| gsd-phase-boundary.sh | Shell | Boundary entre fases |
| gsd-prompt-guard.js | JS | Guard de prompts |
| gsd-read-guard.js | JS | Guard de leitura |
| gsd-read-injection-scanner.js | JS | Scanner de injeção em reads |
| gsd-session-state.sh | Shell | Estado da sessão |
| gsd-statusline.js | JS | Status line da UI |
| gsd-update-banner.js | JS | Banner de atualização |
| gsd-validate-commit.sh | Shell | Validação de commits |
| gsd-workflow-guard.js | JS | Guard de workflow |
| gsd-worktree-path-guard.js | JS | Guard de path de worktree |

---

## 4. COMMANDS (72 total)

### 4.1 Gran-Mestre (1)

| Comando | Descrição |
|---------|-----------|
| /gran-mestre | Pipeline completo do Gran-Mestre |

### 4.2 GSD Core (70)

| Comando | Descrição |
|---------|-----------|
| /gsd-add-tests | Generate tests for phase |
| /gsd-ai-integration-phase | Generate AI-SPEC.md |
| /gsd-audit-fix | Autonomous audit-to-fix |
| /gsd-audit-milestone | Audit milestone |
| /gsd-audit-uat | Cross-phase UAT audit |
| /gsd-autonomous | Run all phases autonomously |
| /gsd-capture | Capture ideas/tasks |
| /gsd-cleanup | Archive phase dirs |
| /gsd-code-review | Review source files |
| /gsd-complete-milestone | Archive milestone |
| /gsd-config | Configure GSD |
| /gsd-debug | Systematic debugging |
| /gsd-discuss-phase | Gather phase context |
| /gsd-docs-update | Update documentation |
| /gsd-eval-review | Audit AI evaluation |
| /gsd-execute-phase | Execute plans |
| /gsd-explore | Socratic ideation |
| /gsd-extract-learnings | Extract patterns |
| /gsd-fast | Execute trivial task |
| /gsd-forensics | Post-mortem |
| /gsd-graphify | Knowledge graph |
| /gsd-health | Diagnose health |
| /gsd-help | Show commands |
| /gsd-import | Ingest plans |
| /gsd-inbox | Triage issues/PRs |
| /gsd-ingest-docs | Bootstrap from docs |
| /gsd-manager | Command center |
| /gsd-map-codebase | Analyze codebase |
| /gsd-mempalace-capture | File to MemPalace |
| /gsd-mempalace-recall | Recall from MemPalace |
| /gsd-milestone-summary | Project summary |
| /gsd-mvp-phase | MVP slice |
| /gsd-new-milestone | New milestone |
| /gsd-new-project | Initialize project |
| /gsd-ns-context | Codebase intel |
| /gsd-ns-ideate | Exploration |
| /gsd-ns-manage | Config workspace |
| /gsd-ns-project | Project lifecycle |
| /gsd-ns-review | Quality gates |
| /gsd-ns-workflow | Workflow |
| /gsd-pause-work | Context handoff |
| /gsd-phase | CRUD phases |
| /gsd-plan-phase | Phase plan |
| /gsd-plan-review-convergence | Plan convergence |
| /gsd-pr-branch | Clean PR branch |
| /gsd-profile-user | Developer profile |
| /gsd-progress | Check progress |
| /gsd-quick | Quick task |
| /gsd-resume-work | Resume session |
| /gsd-review | Peer review |
| /gsd-review-backlog | Review backlog |
| /gsd-secure-phase | Verify threats |
| /gsd-settings | Configure toggles |
| /gsd-ship | Create PR |
| /gsd-sketch | Sketch UI |
| /gsd-spec-phase | Clarify deliverables |
| /gsd-spike | Spike idea |
| /gsd-stats | Project stats |
| /gsd-surface | Toggle skills |
| /gsd-thread | Context threads |
| /gsd-ui-phase | UI design contract |
| /gsd-ui-review | Visual audit |
| /gsd-ultraplan-phase | Ultraplan cloud |
| /gsd-undo | Git revert |
| /gsd-update | Update GSD |
| /gsd-validate-phase | Nyquist gaps |
| /gsd-verify-work | UAT validation |
| /gsd-workspace | Manage workspaces |
| /gsd-workstreams | Parallel workstreams |

### 4.3 Outros (1)

| Comando | Descrição |
|---------|-----------|
| /registry-sync | Sincroniza AgentRegistry |

---

## 5. MCPs (5 total)

| MCP | Tipo | Endpoint | Status |
|-----|------|----------|--------|
| ghidra | remote | http://127.0.0.1:8080/mcp | ✅ Ativo |
| codegraph | stdio | codegraph serve --mcp | ✅ Disponível |
| context7 | url | mcp.context7.com | ✅ Disponível |
| grep_app | url | mcp.grep.app | ✅ Disponível |
| lsp | stdio | lsp-daemon | ✅ Disponível |

---

## 6. PROVIDERS (2 total, 100 modelos)

### 6.1 Local — Ollama (AMD ROCm)

| Modelo | Context | Output | Tool Call | Reasoning |
|--------|---------|--------|-----------|-----------|
| qwen-coder-30b | 8192 | 4096 | ✅ | ❌ |
| qwen2.5-coder:7b | 32768 | 4096 | ✅ | ❌ |
| qwen3.5-27b | 4096 | 2048 | ✅ | ✅ |

### 6.2 OmniRoute (97 modelos)

| Modelo | Context | Output | Tool Call | Reasoning |
|--------|---------|--------|-----------|-----------|
| auto/best-coding | 1M | 512K | ✅ | ✅ |
| auto/best-reasoning | 1M | 512K | ✅ | ✅ |
| auto/best-fast | 1M | 512K | ✅ | ✅ |
| auto/best-vision | 1M | 512K | ✅ | ✅ |
| auto/pro-coding | 1M | 512K | ✅ | ✅ |
| auto/claude-opus | 1M | 512K | ✅ | ✅ |
| auto/claude-sonnet | 1M | 512K | ✅ | ✅ |
| auto/mimo | 1M | 128K | ✅ | ✅ |
| auto/gemini | 1M | 65K | ✅ | ✅ |
| ... | ... | ... | ... | ... |

---

## 7. INTEGRAÇÕES ABSORVIDAS (10 total)

| Framework | Origem | Padrões | Status | Arquivo |
|-----------|--------|---------|--------|---------|
| oh-my-openagents | v4.19.2 | 8 | ✅ | MIX_MODE.md |
| Superpowers | github.com | 6 | ✅ | MIX_MODE.md |
| Fable Method | github.com | 8 | ✅ | MIX_MODE.md |
| OpenClaude | v0.26.0 (30.4k⭐) | 12 | ✅ | OPENCLAUDE_INTEGRATION.md |
| MoA | togethercomputer/moa (29.3k⭐) | 5 | ✅ | MOA_INTEGRATION.md |
| Ponytail | github.com | 1 | ✅ | MIX_MODE.md |
| Improve | github.com | 1 | ✅ | MIX_MODE.md |
| SkillSpector | github.com | 1 | ✅ | MIX_MODE.md |
| DeepSpec | github.com | 1 | ✅ | MIX_MODE.md |
| drawio | github.com | 1 | ✅ | MIX_MODE.md |

---

## 8. PIPELINE MODES (6 total)

| Modo | Agents | Gates | Uso |
|------|--------|-------|-----|
| TRIVIAL | 1 (sisyphus) | 0 | Tasks simples (1 arquivo, <10 linhas) |
| SIMPLE | 1 (atlas) | 0 | Execução direta com mini-plano |
| MEDIUM | 3 (prometheus, hestia, atlas) | 0 | Pipeline básico |
| COMPLEX | 4 (prometheus, hestia, atlas, athena) | 0 | Pipeline completo |
| CRITICAL | 5+ (mesmo + reviewers) | 0 | Alta segurança + rollback |
| FEATURE | 6 fases | 4 | Cascata completa |

---

## 9. PERMISSÕES (6 total)

| Permissão | Valor | Descrição |
|-----------|-------|-----------|
| bash | allow | Execução de comandos bash |
| read | allow | Leitura de arquivos |
| edit | allow | Edição de arquivos |
| webfetch | allow | Fetch de URLs |
| websearch | allow | Pesquisa web |
| mcp_ghidra | allow | Acesso ao Ghidra MCP |

---

## 10. SYMLINKS PORTÁVEIS (7 total)

| Symlink | Target | Status |
|---------|--------|--------|
| ~/.opencode | /mnt/dados/opencode | ✅ |
| ~/.config/opencode | /mnt/dados/opencode/config | ✅ |
| ~/.claude | /mnt/dados/opencode/claude | ✅ |
| ~/.omo | /mnt/dados/opencode/omo | ✅ |
| ~/.bun | /mnt/dados/opencode/bun | ✅ |
| ~/.local/share/opencode | /mnt/dados/opencode/share-data | ✅ |
| ~/.npm | /home/johncoffee/.npm | ✅ |

---

## 11. BACKUP

| Item | Detalhe |
|------|---------|
| Repositório | https://github.com/johncoffee715/gran-mestre-backup (PRIVATE) |
| Branch | master |
| Commits | 3 |
| Último | 1fca257 — Autofagia OpenClaude |
| Binário | /mnt/dados/opencode/bin/opencode.bin (171MB) |
| Configs | /mnt/dados/opencode/user-configs/ |
| fstab | /mnt/dados/opencode/system-backup/fstab |

---

## 12. SEGURANÇA

### 12.1 Auditoria de Frameworks

| Framework | Status | Verificações |
|-----------|--------|--------------|
| oh-my-openagents | 🟢 SEGURO | Plugin maduro, telemetria opt-out |
| Superpowers | 🟢 SEGURO | Skills processuais, sem IO externo |
| Fable Method | 🟢 SEGURO | Verificação adversarial, sem backdoors |
| OpenClaude | 🟢 SEGURO | 30.4k stars, MIT, privacy verified |
| MoA | 🟢 SEGURO | Paper acadêmico, código aberto |

### 12.2 Regras de Segurança

| Regra | Status |
|-------|--------|
| Safety SHA antes de execução | ✅ |
| Rollback automático em falha | ✅ |
| Model rotation com fallback | ✅ |
| Permissões granulares | ✅ |
| Hooks de validação | ✅ |
| Privacy verification | ✅ |

---

## 13. ARQUIVOS DE CONFIGURAÇÃO

| Arquivo | Tamanho | Descrição |
|---------|---------|-----------|
| MIX_MODE.md | 26KB | Modo MIX — 4 reinos, 6 fases, 4 pipelines |
| OPENCLAUDE_INTEGRATION.md | 14KB | Autofagia OpenClaude — 12 padrões |
| REGISTRY_OPENCLAUDE.md | 13KB | Registry dos componentes OpenClaude |
| PIPELINE_MODES.md | 25KB | 6 modos de pipeline documentados |
| MOA_INTEGRATION.md | 9KB | Autofagia MoA — 5 padrões |
| GLOBAL_POLICY.md | 4.6KB | Política global de execução |
| OBSIDIAN_COGNITIVE_BRAIN.md | 4.9KB | Integração Obsidian |
| INVENTORY.md | 3.1KB | Inventário resumido |

---

## 14. TEMPLATES

| Template | Descrição |
|----------|-----------|
| TEMPLATE-agent.md | Template para criar agents |
| TEMPLATE-subagent.md | Template para criar subagents |
| TEMPLATE-skill.md | Template para criar skills |
| TEMPLATE-tool.md | Template para criar tools |
| TEMPLATE-mcp.md | Template para criar MCPs |
| agent-registry.schema.json | Schema do registry |
| agent-registry.example.json | Exemplo de registry |

---

## 15. REGISTRY FILES

| Arquivo | Descrição |
|---------|-----------|
| agent-registry.json | Registry de agents |
| capability-index.json | Índice de capabilities |
| capability-router.json | Router de capabilities |
| context-broker.json | Broker de contexto |
| event-bus.json | Event bus |
| GRAN_MESTRE.md | Documentação do Gran-Mestre |
| REGISTRY.md | Registry geral |
| MODELOS.md | Modelos disponíveis |

---

**Versão:** 4.0.0
**Data:** 2026-07-27
**Total de componentes:** 231
**Status:** ✅ Todos auditados e registrados
**Backup:** https://github.com/johncoffee715/gran-mestre-backup
