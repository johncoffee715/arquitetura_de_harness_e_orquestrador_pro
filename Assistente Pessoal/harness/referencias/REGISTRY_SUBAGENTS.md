# REGISTRY — 61 Subagents do Gran-Mestre
## Data: 2026-07-27 | Decisão: Gran-Mestre = único agent primário

---

## 1. Agent Primário (1)

| Agent | Mode | Modelo | Função |
|-------|------|--------|--------|
| gran-mestre | **primary** | claude-opus-4.7 | Meta-orquestrador — ponto de entrada único |

---

## 2. Pipeline Subagents (6)

| # | Subagent | Fase | Função | Origem |
|---|----------|------|--------|--------|
| 1 | prometheus | 3 | Planejamento modo entrevista | oh-my-openagents |
| 2 | hestia | 2,3,6 | Validação rastreabilidade requisito↔spec | gran-mestre |
| 3 | atlas | 4 | Execução (alias Sisyphus+git-master) | oh-my-openagents |
| 4 | atena | 5 | Revisão macro (composição Oracle) | oh-my-openagents |
| 5 | atreus | 6 | Entrega | gran-mestre |
| 6 | code-reviewer | 4 | Code review por linguagem | oh-my-openagents |

---

## 3. Crossover Subagents — oh-my-openagents (8)

| # | Subagent | Função | Skills |
|---|----------|--------|--------|
| 7 | explore | Busca rápida de código | grep, glob, read |
| 8 | librarian | Documentação e referências | context7, webfetch |
| 9 | oracle | Arquitetura e debug | read, grep, glob |
| 10 | metis | Consultor pré-planejamento | read, grep |
| 11 | sisyphus | Orquestrador principal | all tools |
| 12 | hepheastus | Executor autônomo | all tools |
| 13 | general | Uso geral | all tools |
| 14 | build | Desenvolvimento | all tools |

---

## 4. Crossover Subagents — Superpowers (6)

| # | Subagent | Função | Skill |
|---|----------|--------|-------|
| 15 | superpowers-brainstorming | Socratic ideation | brainstorming |
| 16 | superpowers-plan-writer | Planos TDD | writing-plans |
| 17 | superpowers-implementer | Execução delegada | subagent-driven-dev |
| 18 | superpowers-code-reviewer | Code review | requesting-code-review |
| 19 | superpowers-spec-writer | Especificações | writing-plans |
| 20 | superpowers-verification | Verificação | verification-before-completion |

---

## 5. Crossover Subagents — Fable Method (3)

| # | Subagent | Função | Skill |
|---|----------|--------|-------|
| 21 | fable-method | Classificação (Step 0) | fable-method |
| 22 | fable-loop | Orquestração completa | fable-loop |
| 23 | fable-judge | Verificação adversarial | fable-judge |

---

## 6. GSD Subagents (35)

| # | Subagent | Função |
|---|----------|--------|
| 24 | gsd-planner | Criar planos de fase |
| 25 | gsd-executor | Executar planos |
| 26 | gsd-code-reviewer | Revisar código |
| 27 | gsd-code-fixer | Corrigir código |
| 28 | gsd-debugger | Debugar |
| 29 | gsd-debug-session-manager | Gerenciar sessões de debug |
| 30 | gsd-verifier | Verificar resultados |
| 31 | gsd-doc-writer | Documentar |
| 32 | gsd-doc-classifier | Classificar documentos |
| 33 | gsd-doc-synthesizer | Sintetizar documentos |
| 34 | gsd-doc-verifier | Verificar documentos |
| 35 | gsd-phase-researcher | Pesquisar fase |
| 36 | gsd-project-researcher | Pesquisar projeto |
| 37 | gsd-research-synthesizer | Sintetizar pesquisa |
| 38 | gsd-domain-researcher | Pesquisar domínio |
| 39 | gsd-ai-researcher | Pesquisar IA |
| 40 | gsd-framework-selector | Selecionar framework |
| 41 | gsd-eval-planner | Planejar avaliação |
| 42 | gsd-eval-auditor | Auditar avaliação |
| 43 | gsd-security-auditor | Auditar segurança |
| 44 | gsd-ui-auditor | Auditar UI |
| 45 | gsd-ui-checker | Verificar UI |
| 46 | gsd-ui-researcher | Pesquisar UI |
| 47 | gsd-nyquist-auditor | Auditar Nyquist |
| 48 | gsd-pattern-mapper | Mapear padrões |
| 49 | gsd-codebase-mapper | Mapear codebase |
| 50 | gsd-intel-updater | Atualizar intel |
| 51 | gsd-mempalace-curator | Curar MemPalace |
| 52 | gsd-assumptions-analyzer | Analisar suposições |
| 53 | gsd-integration-checker | Verificar integração |
| 54 | gsd-plan-checker | Verificar plano |
| 55 | gsd-roadmapper | Criar roadmap |
| 56 | gsd-advisor-researcher | Pesquisar decisões |
| 57 | gsd-user-profiler | Perfil do usuário |
| 58 | gsd-verifier | Verificar fase |

---

## 7. OpenCode Subagents (3)

| # | Subagent | Função |
|---|----------|--------|
| 59 | memory-keeper | Memória persistente (Obsidian) |
| 60 | reverser | Engenharia reversa (Ghidra) |
| 61 | general | Uso geral |

---

## 8. Regras de Orquestração

### Regra 1: Gran-Mestre Nunca Executa Direto
```
Usuário → Gran-Mestre → [classifica] → [delega] → [coleta] → [reporta]
```

### Regra 2: Subagents São Descartáveis
- Contexto isolado
- Sem estado entre invocações
- Herdam apenas o que o Gran-Mestre passar

### Regra 3: Hierarquia de Roteamento
```
1. Rota exata (subagent nomeado) → encaminha direto
2. Rota por tipo (skill declarada) → Héstia valida
3. Rota por classificação → Prometheus analisa
4. Fallback → pergunta ao usuário
5. Rejeição → "não sei fazer isso"
```

### Regra 4: Safety Protocol Sempre Ativo
```
SHA → Héstia → Atena → Fable Judge → Rollback
```

---

**Versão:** 1.0.0
**Data:** 2026-07-27
**Total:** 61 subagents
**Agent primário:** gran-mestre (único)
