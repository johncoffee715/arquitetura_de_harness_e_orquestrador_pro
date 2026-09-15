# Conceito & Persona (Ontology)
---
name: otel-semconv-genai
description: |
  GenAI semantic conventions: standard span names and attributes for LLM
  telemetry (model, tokens, cost with source/exactness, authz, lineage),
  aligned to the harness native MELT.
category: skill
role: otel-semconv-genai
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
#   - varredura: MELT nativo emite eventos, mas SEM convenção de atributos
#     compartilhada (cada evento com seu vocabulário)
#   - gap: CONFIRMED — convenções genai p/ spans/atributos do harness

# R2 global:
#   - skill: otel-semconv-genai
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: vocabulário telemetry, debilidade: sem coletor próprio,
#   possibilidades: validar eventos do decision-log
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:open-telemetry/semantic-conventions (área genai)
#   source: https://github.com/open-telemetry/semantic-conventions
#   licenses: Apache-2.0 — sem cópia literal (só convenções aplicadas ao MELT)
