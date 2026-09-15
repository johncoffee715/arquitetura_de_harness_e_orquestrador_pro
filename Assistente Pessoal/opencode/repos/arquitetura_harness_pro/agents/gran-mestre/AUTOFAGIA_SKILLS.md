# AUTOFAGIA — 3 Repositórios de Skills
## Data: 2026-07-25 | Fonte: awesome-copilot, agent-skills, context-engineering

---

## 1. REPOSITÓRIOS ANALISADOS

| Repositório | Stars | Conceito-Chave |
|-------------|-------|----------------|
| github/awesome-copilot | 37k | Community agents, skills, hooks, plugins |
| addyosmani/agent-skills | 80.4k | Production-grade engineering skills |
| muratcankoylan/agent-skills-for-context-engineering | 17.4k | Context engineering skills |

---

## 2. CONCEITOS EXTRAÍDOS

### 2.1 awesome-copilot (37k ⭐)

**O que é:** Coleção comunitária de agents, instructions, skills, hooks, workflows e plugins para GitHub Copilot.

**Estrutura:**
```
awesome-copilot/
├── agents/          ← Agents especializados
├── instructions/    ← Coding standards por file pattern
├── skills/          ← Skills com instruções + assets
├── plugins/         ← Bundles de agents + skills
├── hooks/           ← Session lifecycle hooks
├── cookbook/         ← Recipes copy-paste
└── extensions/      ← Extensões
```

**Conceitos absorvíveis:**
- Marketplace de plugins (`copilot plugin install <name>@awesome-copilot`)
- Skills como pastas self-contained com instruções + assets
- Hooks para lifecycle de sessão
- Agents como personas especializadas

### 2.2 agent-skills (80.4k ⭐) — Addy Osmani

**O que é:** Skills de engenharia production-grade para AI coding agents. 24 skills cobrindo todo o ciclo de desenvolvimento.

**Ciclo de Desenvolvimento:**
```
DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP
/spec    /plan   /build   /test    /review   /ship
```

**24 Skills:**

| Fase | Skills |
|------|--------|
| **Define** | interview-me, idea-refine, spec-driven-development |
| **Plan** | planning-and-task-breakdown |
| **Build** | incremental-implementation, test-driven-development, context-engineering, source-driven-development, doubt-driven-development, frontend-ui-engineering, api-and-interface-design |
| **Verify** | browser-testing-with-devtools, debugging-and-error-recovery |
| **Review** | code-review-and-quality, code-simplification, security-and-hardening, performance-optimization |
| **Ship** | git-workflow-and-versioning, ci-cd-and-automation, deprecation-and-migration, documentation-and-adrs, observability-and-instrumentation, shipping-and-launch |

**4 Agent Personas:**
- code-reviewer (Senior Staff Engineer)
- test-engineer (QA Specialist)
- security-auditor (Security Engineer)
- web-performance-auditor (Web Performance Engineer)

**Conceitos absorvíveis:**
- Anti-rationalization tables (excuses + rebuttals)
- Verification gates non-negotiable
- Progressive disclosure (SKILL.md → references/)
- Doubt-driven development (adversarial review)
- Definition of Done checklist
- Orchestration patterns (personas don't invoke personas)

### 2.3 context-engineering (17.4k ⭐)

**O que é:** Skills focadas em context engineering e harness engineering para sistemas de agentes.

**17 Skills:**

| Categoria | Skills |
|-----------|--------|
| **Foundational** | context-fundamentals, context-degradation, context-compression |
| **Architectural** | multi-agent-patterns, long-horizon-prompting, memory-systems, tool-design, filesystem-context, hosted-agents |
| **Operational** | context-optimization, latent-briefing, evaluation, advanced-evaluation, harness-engineering, self-improvement-loops |
| **Development** | project-development |
| **Cognitive** | bdi-mental-states |

**Conceitos absorvíveis:**
- Context degradation patterns (lost-in-middle, poisoning, distraction, clash)
- Progressive disclosure (load only names at startup)
- Platform agnosticism
- LLM-as-Judge techniques
- Harness engineering (locked metrics, durable logs, novelty gates, rollback)
- Self-improvement loops
- BDI mental states (beliefs, desires, intentions)

---

## 3. PADRÕES PARA GRAN-MAESTRO

### 3.1 Anti-Rationalization (de agent-skills)

```markdown
## Red Flags

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "The skill is overkill" | Simple things become complex. Use it. |
```

### 3.2 Verification Gates (de agent-skills)

```markdown
## Verification

Every skill ends with evidence requirements:
- Tests passing
- Build output
- Runtime data
- "Seems right" is never sufficient
```

### 3.3 Context Degradation (de context-engineering)

```markdown
## Context Degradation Patterns

1. Lost-in-the-middle — models ignore middle of long context
2. Context poisoning — incorrect info persists across turns
3. Context distraction — irrelevant info pulls attention
4. Context clash — contradictory info causes confusion
```

### 3.4 Progressive Disclosure (de context-engineering)

```markdown
## Progressive Disclosure

At startup: load only skill names and descriptions
When activated: load full content
References: load only when needed
```

### 3.5 Doubt-Driven Development (de agent-skills)

```markdown
## Doubt-Driven Development

CLAIM → EXTRACT → DOUBT → RECONCILE → STOP

Every non-trivial decision gets adversarial review:
- Stakes are high (production, security, irreversible)
- Working in unfamiliar code
- Confident output is cheaper to verify now than debug later
```

### 3.6 Harness Engineering (de context-engineering)

```markdown
## Harness Engineering

Design autonomous agent harnesses with:
- Locked metrics
- Durable logs
- Novelty gates
- Rollback
- Human approval boundaries
```

---

## 4. HELENIZAÇÃO PARA OPENCODE

### Skills a criar

| Skill | Origem | Função |
|-------|--------|--------|
| anti-rationalization | agent-skills | Tabela de desculpas + refutações |
| verification-gates | agent-skills | Gates de verificação non-negotiable |
| context-degradation | context-engineering | Padrões de degradação de contexto |
| doubt-driven-development | agent-skills | Revisão adversarial |
| harness-engineering | context-engineering | Design de harness autônomo |
| definition-of-done | agent-skills | Checklist de definição de pronto |

---

**Versão:** 1.0.0
**Data:** 2026-07-25
**Fontes:** 3 repositórios (134.8k stars total)