# Conceito & Persona (Ontology)
---
name: temporal-agent-harness
description: |
  Durable agent-harness patterns: agents-as-workflows with mid-turn resume,
  layered tool-approval policies, Code Mode (typed scripts over tools),
  client-side callback tools, typed composable agent interfaces. Patterns only.
category: skill
role: temporal-agent-harness
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
#   - varredura: temporal (tríade) + openai-agents-python (handoffs) + ruflo
#     (swarm) cobrem durabilidade/delegação; NADA cobre agente-como-workflow
#     (resume mid-turn) + Code Mode + callback tools + approval policy engine
#   - gap: CONFIRMED — 4 padrões (nunca harness/servidor alheios)

# R2 global:
#   - skill: temporal-agent-harness
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: 4 padrões, debilidade: original experimental (APIs mudam),
#   possibilidades: approvals sobre tool-calling do harness
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:temporal-community/temporal-agent-harness
#   source: https://github.com/temporal-community/temporal-agent-harness
#   licenses: MIT — sem cópia literal (só 4 padrões); harness/servidor NUNCA como dependência
