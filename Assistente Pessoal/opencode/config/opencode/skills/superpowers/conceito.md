# Conceito & Persona (Ontology)
---
name: superpowers
description: |
  Mandatory skill-check dev loop: brainstorm, isolated worktrees, bite-sized plans,
  two-stage subagent review (spec then quality), true RED-GREEN TDD, severity review,
  clean finish. Skills trigger automatically — mandatory workflows, not suggestions.
category: skill
role: superpowers
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
#   - varredura: openspec/bmad (planos) + karpathy (gates) + fable-judge (verificação)
#     cobrem partes; NADA cobre skill-check mandatório pré-task + review duplo
#     de subagent + worktree-por-design
#   - gap: CONFIRMED — loop mandatório + review em 2 estágios

# R2 global:
#   - skill: superpowers
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: loop completo, debilidade: rigidez p/ triviais,
#   possibilidades: drill-evals próprios
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:obra/superpowers
#   source: https://github.com/obra/superpowers
#   licenses: MIT — sem cópia literal (só loop + review duplo)
