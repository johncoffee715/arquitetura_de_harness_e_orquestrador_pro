# Conceito & Persona (Ontology)
---
name: browser-use
description: |
  Browser-use skill for extracting and summarizing web content for task completion.
  Uses RWKV7 sensorial model to condense massive context into executable summaries.
  Category: runtime
  Role: memory-recall (browser context)
  Version: 1.0.0
  creation_date: 2026-09-23
  author: local-orchestrator

# Helenization metadata (R77 - 3 layers)
#   1. Ontology & persona (system prompt immutable)
#   2. Gabarito/firewall (constraints & safety)
#   3. Mecânica de ignição (execution & validation)

# R75 bindings by category:
#   provider: local-orchestrator
#   category: runtime
#   model: local-lora/browser-use

# R28 categórico veredito:
#   Capacidades: browser extraction (ingestor 1M ctx)
#   Debilidade: complex filtering
#   Possibilidades: draft if tokenizer compatible
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + runtime check

# Note: This skill follows R44 (helenização global) and R45 (context window) guidelines.
# It is helenizado com R77 (3 camadas) e R75 (bindings por categoria).
