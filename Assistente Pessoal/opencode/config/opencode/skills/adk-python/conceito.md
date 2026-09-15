# Conceito & Persona (Ontology)
---
name: adk-python
description: |
  Code-first agent pattern: Agent/Workflow duality, multi-turn Task API delegation,
  tool-confirmation HITL, versioned eval sets. Patterns only — the framework is
  PROHIBITED as dependency.
category: skill
role: adk-python
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
#   - varredura: crewai-patterns (role-cards) + langgraph-patterns (state-graph)
#     cobrem organização e estado; NADA cobre dualidade Agent/Workflow + Task API
#     + tool-confirmation + evalsets
#   - gap: CONFIRMED (estreito) — padrão Agent/Workflow/Task (nunca o framework)

# R2 global:
#   - skill: adk-python
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: dualidade+delegação, debilidade: pull p/ ecossistema Google,
#   possibilidades: Task API sobre subagents do harness
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:google/adk-python
#   source: https://github.com/google/adk-python
#   licenses: Apache-2.0 — sem cópia literal (só padrão); framework PROIBIDO como dependência
