# Conceito & Persona (Ontology)
---
name: temporal
description: |
  Durable-execution triad: resilient Workflows, retrying Activities, Workers,
  crash-to-exact-resume, namespaces, local dev server. Patterns only — the
  server is PROHIBITED as dependency.
category: skill
role: temporal
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
#   - varredura: inngest (event-steps) + langgraph-patterns (state-graph) cobrem
#     durabilidade por eventos/grafo; NADA cobre a tríade Workflow/Activity/Worker
#     code-first com resume exato
#   - gap: CONFIRMED (estreito) — tríade durável (nunca o servidor)

# R2 global:
#   - skill: temporal
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: tríade resiliente, debilidade: servidor pesado (Go+DB),
#   possibilidades: workflows sobre pipeline do harness
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:temporalio/temporal
#   source: https://github.com/temporalio/temporal
#   licenses: MIT — sem cópia literal (só tríade); servidor PROIBIDO como dependência
