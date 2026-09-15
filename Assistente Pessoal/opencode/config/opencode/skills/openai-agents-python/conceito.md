# Conceito & Persona (Ontology)
---
name: openai-agents-python
description: |
  Handoff-first multi-agent pattern: agents-as-tools delegation with context,
  input/output guardrails, automatic session history, built-in tracing.
  Patterns only — the framework is PROHIBITED as dependency.
category: skill
role: openai-agents-python
type: skill
version: 1.0.0
creation_date: 2026-09-12
author: gran-mestre-hefesto

# Helenization metadata (R77 - 3 layers)
# 1. Ontology & persona (system prompt imutável)
# 2. Gabarito/firewall (constraints & safety)
# 3. Mecânica de ignição (execution & validation)

# R75 bindings by category:
#   provider: local-forge
#   category: skill
#   model: local-forge/proposer

# R8 catalog-first:
#   - varredura: crewai-patterns (cards) + adk-python (Task API) cobrem delegação;
#     NADA cobre handoffs c/ contexto + guardrails in/out + sessions + tracing
#   - gap: CONFIRMED (estreito) — bundle handoff/guardrail/session/trace

# R2 global:
#   - skill: openai-agents-python
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: delegação guardada, debilidade: default p/ vendor único,
#   possibilidades: handoffs entre subagents do harness
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:openai/openai-agents-python
#   source: https://github.com/openai/openai-agents-python
#   licenses: MIT — sem cópia literal (só padrão); framework PROIBIDO como dependência
