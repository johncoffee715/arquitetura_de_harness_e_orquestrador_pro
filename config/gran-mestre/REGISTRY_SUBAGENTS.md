# REGISTRY — 61 Subagents do Gran-Mestre
## Data: 2026-07-29 | Decisão: Gran-Mestre = único agent primário
## Modo: MIX — Delegação Dinâmica via Registry

---

## 1. Agent Primário (1)

| Agent | Mode | Modelo | Função | Tags |
|-------|------|--------|--------|------|
| gran-mestre | **primary** | omniroute/auto/best-free | Meta-orquestrador — ponto de entrada único | orchestrator, meta, entrypoint |

---

## 2. Pipeline Subagents (6)

| # | Subagent | Fase | Função | Tags |
|--|----------|------|--------|------|
| 1 | prometheus | 3 (DESC) | Planejamento modo entrevista | discovery, planning, interview, socratic, requirements, decomposition |
| 2 | hestia | 2,3,6 | Validação rastreabilidade requisito↔spec | validation, contract, audit, compliance, traceability, gatekeeper |
| 3 | atlas | 4 (EXEC) | Execução orquestrada | execution, orchestration, git, wave, parallel, coordinator |
| 4 | atena | 5 (REV) | Revisão macro (composição Oracle) | review, macro, architecture, coherence, cross-task, coupling |
| 5 | atreus | 6 (ENTR) | Entrega | delivery, verification, release, handoff, closure |
| 6 | code-reviewer | 4 (EXEC) | Code review por linguagem | review, code, quality, security, lint, static-analysis |

---

## 3. Crossover Subagents — oh-my-openagents (8)

| # | Subagent | Função | Tags |
|---|----------|--------|------|
| 7 | explore | Busca rápida de código | search, code, grep, fast, pattern, file-discovery |
| 8 | librarian | Documentação e referências | research, docs, context, discovery, api, library, external |
| 9 | oracle | Arquitetura e debug | architect, debug, reasoning, high-iq, design, troubleshooting |
| 10 | metis | Consultor pré-planejamento | pre-planning, analysis, ambiguity, intent, assumptions, risks |
| 11 | sisyphus | Orquestrador principal | orchestration, execution, general, coordinator, workflow |
| 12 | hepheastus | Executor autônomo | execution, autonomous, build, implementation, agent |
| 13 | general | Uso geral | general, utility, fallback, catch-all |
| 14 | build | Desenvolvimento | development, coding, implementation, compile, build-tool |

---

## 4. Crossover Subagents — Superpowers (6)

| # | Subagent | Função | Tags |
|---|----------|--------|------|
| 15 | superpowers-brainstorming | Socratic ideation | ideation, brainstorming, creative, divergent-thinking, exploration |
| 16 | superpowers-plan-writer | Planos TDD | planning, tdd, tasks, bite-sized, decomposition, estimable |
| 17 | superpowers-implementer | Execução delegada | implementation, coding, tdd, test-first, red-green |
| 18 | superpowers-code-reviewer | Code review | review, code, quality, standards, best-practices |
| 19 | superpowers-spec-writer | Especificações | spec, contract, design, documentation, acceptance-criteria |
| 20 | superpowers-verification | Verificação | verification, validation, testing, assertion, coverage |

---

## 5. Crossover Subagents — Fable Method (3)

| # | Subagent | Função | Tags |
|---|----------|--------|------|
| 21 | fable-method | Classificação (Step 0) | classification, routing, triage, complexity, fit-gate |
| 22 | fable-loop | Orquestração completa | loop, orchestration, decomposition, iterative, refinement |
| 23 | fable-judge | Verificação adversarial | audit, verification, adversarial, gate, anti-pattern, false-positive |

---

## 6. GSD Subagents (35)

| # | Subagent | Função | Tags |
|---|----------|--------|------|
| 24 | gsd-planner | Criar planos de fase | planning, phase, decomposition, tasks, milestones, goal-backward |
| 25 | gsd-executor | Executar planos | execution, plan, implementation, waves, atomic-commit, state |
| 26 | gsd-code-reviewer | Revisar código | review, code, quality, bugs, security, patterns |
| 27 | gsd-code-fixer | Corrigir código | fix, code, remediation, patch, automated-fix |
| 28 | gsd-debugger | Debugar | debug, investigation, troubleshooting, root-cause, hypothesis |
| 29 | gsd-debug-session-manager | Gerenciar sessões de debug | debug, session, management, checkpoint, continuation |
| 30 | gsd-verifier | Verificar resultados | verification, validation, testing, goal-backward, acceptance |
| 31 | gsd-doc-writer | Documentar | docs, documentation, writing, readme, markdown |
| 32 | gsd-doc-classifier | Classificar documentos | docs, classification, analysis, adr, prd, spec |
| 33 | gsd-doc-synthesizer | Sintetizar documentos | docs, synthesis, consolidation, merge, dedup |
| 34 | gsd-doc-verifier | Verificar documentos | docs, verification, accuracy, factual, codebase-crossref |
| 35 | gsd-phase-researcher | Pesquisar fase | research, phase, domain, implementation-strategy |
| 36 | gsd-project-researcher | Pesquisar projeto | research, project, domain, ecosystem, landscape |
| 37 | gsd-research-synthesizer | Sintetizar pesquisa | research, synthesis, consolidation, summary, findings |
| 38 | gsd-domain-researcher | Pesquisar domínio | research, domain, business, context, expert-criteria |
| 39 | gsd-ai-researcher | Pesquisar IA | research, ai, framework, llm, best-practice |
| 40 | gsd-framework-selector | Selecionar framework | selection, framework, decision, matrix, comparison |
| 41 | gsd-eval-planner | Planejar avaliação | evaluation, planning, metrics, rubric, dataset |
| 42 | gsd-eval-auditor | Auditar avaliação | evaluation, audit, metrics, coverage, remediation |
| 43 | gsd-security-auditor | Auditar segurança | security, audit, vulnerabilities, threat-model, mitre |
| 44 | gsd-ui-auditor | Auditar UI | ui, audit, visual, design, a11y, responsive |
| 45 | gsd-ui-checker | Verificar UI | ui, verification, design, spec-adherence |
| 46 | gsd-ui-researcher | Pesquisar UI | ui, research, design, patterns, components |
| 47 | gsd-nyquist-auditor | Auditar Nyquist | validation, audit, coverage, test-gap, remediation |
| 48 | gsd-pattern-mapper | Mapear padrões | patterns, mapping, analysis, analog, closest-match |
| 49 | gsd-codebase-mapper | Mapear codebase | codebase, mapping, architecture, structure, dependency |
| 50 | gsd-intel-updater | Atualizar intel | intel, update, intelligence, codebase-snapshot |
| 51 | gsd-mempalace-curator | Curar MemPalace | memory, curation, knowledge, session-diary, tunnels |
| 52 | gsd-assumptions-analyzer | Analisar suposições | analysis, assumptions, risks, hidden, preconditions |
| 53 | gsd-integration-checker | Verificar integração | integration, verification, connectivity, e2e, phase-links |
| 54 | gsd-plan-checker | Verificar plano | planning, verification, quality, goal-backward, pre-execution |
| 55 | gsd-roadmapper | Criar roadmap | roadmap, planning, milestones, timeline, dependencies |
| 56 | gsd-advisor-researcher | Pesquisar decisões | research, decisions, analysis, comparison, tradeoff |
| 57 | gsd-user-profiler | Perfil do usuário | profile, user, analysis, behavior, preferences |
| 58 | gsd-verifier | Verificar fase | verification, phase, validation, acceptance, closure |

---

## 7. OpenCode Subagents (3)

| # | Subagent | Função | Tags |
|---|----------|--------|------|
| 59 | memory-keeper | Memória persistente (Obsidian) | memory, persistence, obsidian, knowledge, consciousness, vault, neural |
| 60 | reverser | Engenharia reversa (Ghidra) | reverse-engineering, binary, firmware, ghidra, bios, decompile, disassembly |
| 61 | general | Uso geral | general, utility, fallback, catch-all, omniroute |

---

## 8. Skills Registry (10+ skills)

| Skill | Função | Tags |
|-------|--------|------|
| gran-mestre | Meta-orquestração | orchestrator, meta, pipeline |
| hestia | Validação de conformidade | validation, compliance, audit |
| athena | Revisão macro | review, macro, architecture |
| pxpipe | Redução de tokens (PNG) | optimization, tokens, context |
| agent-reach | Pesquisa na internet | research, web, search, social |
| archify | Diagramas de arquitetura | diagrams, architecture, visualization |
| browser-use | Automação de navegador | browser, automation, scraper |
| ck | Memória persistente de projeto | memory, project, context |
| fable-judge | Verificação adversarial | audit, verification, adversarial |
| security-review | Revisão de segurança | security, audit, vulnerabilities |
| dev-loop | Loop de desenvolvimento 3 níveis | dev, loop, react, iterative |

---

## 9. MCPs Registry

| MCP | Função | Tags |
|-----|--------|------|
| context7 | Documentação de bibliotecas | docs, libraries, reference |
| codegraph | Knowledge graph de código | codebase, graph, analysis |

---

## 10. LSPs Registry

| LSP | Linguagens | Tags |
|-----|-----------|------|
| typescript-language-server | TypeScript, TSX, JS | typescript, javascript |
| basedpyright | Python | python, type-checking |
| rust-analyzer | Rust | rust, analysis |
| gopls | Go | go, analysis |

---

## 11. Regras de Orquestração Dinâmica (Modo MIX)

### Regra 1: Gran-Mestre Consulta Registry para Cada Fase
```
Para cada fase do pipeline:
1. Consultar registry por tags relevantes à fase
2. Selecionar subagents, skills, MCPs, LSPs, tools compatíveis
3. Compor equipe dinâmica para a fase
4. Delegar conforme capacidades
5. Coletar resultados
```

### Regra 2: Critérios de Seleção por Fase

| Fase | Tags de Busca no Registry |
|------|--------------------------|
| DESCOBERTA | discovery, research, interview, brainstorming, creative |
| CONTRATO | spec, contract, design, validation, compliance |
| PLANO | planning, tdd, tasks, decomposition, verification |
| EXECUÇÃO | execution, implementation, coding, review, git |
| REVISÃO | review, macro, architecture, audit, adversarial |
| ENTREGA | delivery, verification, release, memory, knowledge |

### Regra 3: Subagents São Descartáveis
- Contexto isolado
- Sem estado entre invocações
- Herdam apenas o que o Gran-Mestre passar

### Regra 4: Hierarquia de Roteamento
```
1. Rota exata (subagent nomeado) → encaminha direto
2. Rota por tipo (skill declarada) → Héstia valida
3. Rota por classificação → Prometheus analisa
4. Fallback → pergunta ao usuário
5. Rejeição → "não sei fazer isso"
```

### Regra 5: Safety Protocol Sempre Ativo
```
SHA → Héstia → Atena → Fable Judge → Rollback
```

---

## 12. Matriz de Compatibilidade Fase x Recurso

| Fase | Subagents Core | Skills Core | MCPs | LSPs | Tools |
|------|---------------|-------------|------|------|-------|
| DESCOBERTA | prometheus, librarian, explore, metis | brainstorming, fable-judge, agent-reach | context7 | - | read, glob, grep, websearch |
| CONTRATO | superpowers-spec-writer, hestia | fable-judge, hestia | context7 | - | read, write |
| PLANO | superpowers-plan-writer, gsd-planner, hestia | fable-loop, fable-judge | context7 | basedpyright, rust-analyzer | read, write, glob |
| EXECUÇÃO | atlas, superpowers-implementer, code-reviewer, build | fable-loop, pxpipe, dev-loop | codegraph | Todos LSPs | read, write, edit, bash, lsp |
| REVISÃO | atena, code-reviewer, oracle | fable-judge, athena, security-review | codegraph | Todos LSPs | read, glob, grep, lsp |
| ENTREGA | atreus, gsd-verifier, memory-keeper, hestia | fable-judge, hestia, ck | context7 | - | read, write, bash |

---

**Versão:** 2.1.0
**Data:** 2026-07-29
**Total:** 61 subagents, 11 skills, 2 MCPs, 4 LSPs
**Agent primário:** gran-mestre (único)
**Modo:** MIX — Delegação Dinâmica via Registry
**Tags granulares:** 35+ tags de capability (orquestração, validação, execução, revisão, memória, pesquisa, segurança, ui, debug, documentação, integração, inteligência, análise, perfil, roadmap, classificação, síntese, verificação, framework, ia, domínio, auditoria, cobertura, padrões, codebase, intel, curadoria, suposições, conectividade, fase, release, binário, firmware, ghidra, obsidian, persistência, conhecimento)
