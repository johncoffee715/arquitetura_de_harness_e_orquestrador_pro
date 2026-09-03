# Conceito & Persona (Ontology)
---
name: memory-recall
description: |
  Memory recall skill for the stack. Retrieves and synthesizes context from the stack's health and observations.
  Uses RWKV7 sensorial model to condense massive context into executable summaries.
category: runtime
role: memory-recall
type: skill
version: 1.0.0
creation_date: 2026-08-31
author: local-orchestrator

# Helenization metadata (R77 - 3 layers)
# 1. Ontology & persona (system prompt imutável)
# 2. Gabarito/firewall (constraints & safety)
# 3. Mecânica de ignição (execution & validation)

# R75 bindings by category:
#   provider: local-orchestrator
#   category: runtime
#   model: local-lora/memory-recall

# R8 catalog-first:
#   - catalog: memory-recall
#     path: /mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/memory-recall/SKILL.md
#     version: 1.0.0

# R2 global:
#   - skill: memory-recall
#     binding: runtime
#     category: runtime


# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R75 bindings by category:
#   provider: local-orchestrator
#   category: runtime
#   model: local-lora/memory-recall

# R28 categórico veredito:
#   Capacidades: sensorial (ingestor 1M ctx), debilidade: raciocínio profundo, possibilidades: draft se tokenizer compatível
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + runtime check

# Note: This skill follows R44 (helenização global) and R45 (context window) guidelines.
# It is helenizado com R77 (3 camadas) e R75 (bindings por categoria).