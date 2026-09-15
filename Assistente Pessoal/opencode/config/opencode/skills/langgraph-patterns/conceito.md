# Conceito & Persona (Ontology)
---
name: langgraph-patterns
description: |
  Stateful graph pattern: typed state schema, nodes, edges, per-step checkpointing
  with exact resume, human interrupts at any point, short-term working memory plus
  long-term persistent memory. Patterns only — the framework is PROHIBITED as dependency.
category: skill
role: langgraph-patterns
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
#   - varredura: NADA cobre grafo stateful + checkpoint/resume + interrupts +
#     memória curta/longa (temporal cobre durable genérico; ruflo cobre swarm)
#   - gap: CONFIRMED — padrão state-graph resiliente (nunca o framework)

# R2 global:
#   - skill: langgraph-patterns
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: grafo resiliente, debilidade: cerimônia p/ fluxos triviais,
#   possibilidades: checkpoints no decision-log
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:langchain-ai/langgraph
#   source: https://github.com/langchain-ai/langgraph
#   licenses: MIT — sem cópia literal (só padrão); framework PROIBIDO como dependência
