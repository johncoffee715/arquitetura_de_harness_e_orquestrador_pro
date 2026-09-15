# Conceito & Persona (Ontology)
---
name: context7-skill
description: |
  Up-to-date library documentation lookup via Context7 REST API.
  Resolves a library ID, then fetches focused docs with topic filtering.
  Zero persistent context cost: ~100 tokens on-demand vs ~500-2000 always-on MCP schemas.
category: skill
role: context7-skill
type: skill
version: 1.0.0
creation_date: 2026-09-12
author: gran-mestre-hefesto

# Helenization metadata (R77 - 3 layers)
# 1. Ontology & persona (system prompt imutável)
# 2. Gabarito/firewall (constraints & safety)
# 3. Mecânica de ignição (execution & validation)

# R75 bindings by category:
#   provider: local-thalamus
#   category: skill
#   model: local-thalamus/ingestor

# R8 catalog-first:
#   - varredura: nenhuma skill context7 no catálogo (browser-use/firecrawl cobrem web geral, não docs versionadas)
#   - gap: CONFIRMED — docs de lib up-to-date com topic focus, sem overhead MCP

# R2 global:
#   - skill: context7-skill
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: retrieval focal (resolve+fetch), debilidade: sem cache local, possibilidades: cache + offline fallback
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:netresearch/context7-skill
#   source: https://github.com/netresearch/context7-skill
#   licenses: MIT (code) + CC-BY-SA-4.0 (content) — respeitadas, sem cópia literal
