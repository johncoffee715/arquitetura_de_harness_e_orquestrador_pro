# Conceito & Persona (Ontology)
---
name: inngest
description: |
  Event-driven durable steps: triggers (event/cron/webhook), auto-retry step.run,
  waitForEvent/cancelOn coordination, keyed flow control (concurrency, throttle,
  debounce, rate-limit, batching). Patterns only — server/platform never as dependency.
category: skill
role: inngest
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
#   - varredura: langgraph-patterns (state-graph) + temporal (durable genérico,
#     pendente) cobrem durabilidade; NADA cobre o modelo event→steps com
#     waitForEvent/cancelOn + flow-control keyed
#   - gap: CONFIRMED — padrão event-steps duráveis (nunca servidor/plataforma)

# R2 global:
#   - skill: inngest
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: steps duráveis, debilidade: servidor SSPL,
#   possibilidades: steps sobre pipeline do harness
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:inngest/inngest
#   source: https://github.com/inngest/inngest
#   licenses: SDKs Apache-2.0; servidor SSPL (NÃO absorvido) — só padrão event→steps
