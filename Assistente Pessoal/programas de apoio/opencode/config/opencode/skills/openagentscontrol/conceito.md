# Conceito & Persona (Ontology)
---
name: openagentscontrol
description: |
  Plan-first execution pattern: propose plan, require human approval, execute
  incrementally with automatic testing, review and validation. Multi-language.
category: skill
role: openagentscontrol
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
#   - varredura: openspec/spec-kit (specs) + andrej-karpathy-skills (gates de diff)
#     cobrem plano e review; NADA cobre o gate de aprovação PRÉ-execução + validação
#     automática por etapa
#   - gap: CONFIRMED (estreito) — approval-gate + validação automática incremental

# R2 global:
#   - skill: openagentscontrol
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: gates + validação, debilidade: latência humana no gate,
#   possibilidades: auto-aprovação p/ mudanças triviais whitelistadas
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:darrenhinde/openagentscontrol
#   source: https://github.com/darrenhinde/openagentscontrol
#   licenses: MIT (verificar) — sem cópia literal (só padrão plan→approve→execute)
