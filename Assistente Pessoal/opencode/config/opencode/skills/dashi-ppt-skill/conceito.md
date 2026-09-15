# Conceito & Persona (Ontology)
---
name: dashi-ppt-skill
description: |
  Themed, browser-editable slide decks: pages as (layout + copy fields) with a
  per-page edit console, rendered as HTML first, exported to HTML/PDF/PPTX.
  Local-only generation, zero content upload.
category: skill
role: dashi-ppt-skill
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
#   - varredura: nenhuma skill de deck/PPT no catálogo
#   - gap: CONFIRMED — decks temáticos editáveis no browser com export PPTX

# R2 global:
#   - skill: dashi-ppt-skill
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: layouts temáticos, console por página, export triplo,
#   debilidade: ~100k tok/deck + Chrome local p/ PPTX/PDF, possibilidades: cache de temas
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:chuspeeism/dashi-ppt-skill
#   source: https://github.com/chuspeeism/dashi-ppt-skill
#   licenses: AGPL-3.0 (repo) + export engine proprietário (NÃO absorvido — só contrato de export)
#   restrição: absorvido SOMENTE o padrão (tema/layout/console/export-contrato); engine proprietária nunca copiada
