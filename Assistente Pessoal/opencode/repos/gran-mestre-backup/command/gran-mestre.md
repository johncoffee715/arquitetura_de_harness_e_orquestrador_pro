---
description: Run the Gran-Mestre full pipeline — plan, validate, execute, review with automatic delegation between agents.
agent: gran-mestre
subtask: true
---

# Gran-Mestre Pipeline

Execute the full Gran-Mestre pipeline for the following task:

## Argument Validation (REQUIRED FIRST)

Before ANY execution, validate arguments:

```
IF $ARGUMENTS is empty or whitespace-only:
  RESPOND: "❌ Uso: /gran-mestre <descrição da tarefa>
  
  Exemplos:
    /gran-mestre adicionar validação de email
    /gran-mestre refatorar módulo de autenticação
    /gran-mestre corrigir bug no login"
  
  STOP — do not proceed with pipeline.

IF $ARGUMENTS starts with -- and is NOT --plan-only, --execute-only, --review-only:
  RESPOND: "❌ Flag inválida: {flag}
  Flags válidas: --plan-only, --execute-only, --review-only"
  
  STOP — do not proceed with pipeline.
```

## User Task
$ARGUMENTS

## Pipeline Instructions

1. **Assess Complexity**: Classify as TRIVIAL/SIMPLE/MEDIUM/COMPLEX/CRITICAL

2. **TRIVIAL**: Execute directly. No delegation. Skip to Report.

3. **SIMPLE**: Write mini-plano in CONTEXT.md (3-5 lines). Delegate to Atlas. Skip to Report.

4. **MEDIUM+**:
   a. **Plan** (Prometheus): Create PLAN.md in `.omo/plans/gran-mestre-{slug}.md`
   b. **Validate** (Superpowers): If MEDIUM+, validate before executing (max 3 cycles)
   c. **Execute** (Atlas): Follow PLAN.md, atomic commits, escalate if needed (max 2 cycles)
   d. **Review** (Hephaestus): COMPLEX/CRITICAL only — run tests first, then deep review

5. **Report**: Summary of what was done, files changed, test status, warnings

## Context

Original task: $ARGUMENTS
Pipeline: Gran-Mestre → [Prometheus → Superpowers →] Atlas → [Hephaestus]
