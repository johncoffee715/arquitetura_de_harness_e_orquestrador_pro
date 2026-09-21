# Conceito & Persona (Ontology)
---
name: testsprite
description: |
  Agent test-verification loop: onboard skill prepares the repo, verify skill
  re-runs claimed checks against a versioned plan.schema.json contract.
  Done only on observed verification. Patterns only.
category: skill
role: testsprite
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
#   - varredura: fable-judge (adversarial genérico) + coderabbit (review) cobrem
#     verificação; NADA cobre loop onboard→plan→verify de TESTES p/ agentes com
#     contrato de schema
#   - gap: CONFIRMED — verificação de testes agentiva (clone real SHA 125872f)

# R2 global:
#   - skill: testsprite
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: loop de verificação, debilidade: backend presumido (PARTIALLY
#   UNDERSTOOD — CLI pode exigir serviço TestSprite),
#   possibilidades: plan.schema próprio
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido
#   + clone SHA 125872f + package.json/skills/schemas reais lidos

# Provenance (helenização):
#   origin: absorvido:TestSprite/testsprite-cli
#   source: https://github.com/TestSprite/testsprite-cli
#   licenses: Apache-2.0 — sem cópia literal (só loop + contrato)
