# Conceito & Persona (Ontology)
---
name: mcp-servers
description: |
  Official MCP reference catalog: 7 active servers (Everything, Fetch, Filesystem,
  Git, Memory, Sequential-Thinking, Time) plus safe client-config contract.
  Reference/educational — hardening próprio antes de produção.
category: skill
role: mcp-servers
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
#   - varredura: sentry-mcp + gemini-mcp-tool + openwork-mcp + firecrawl existem,
#     mas NENHUM catálogo de referência (filesystem/git/memory/fetch/time/sequential)
#   - gap: CONFIRMED — catálogo MCP de referência + contrato de config segura

# R2 global:
#   - skill: mcp-servers
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: catálogo+config, debilidade: referência≠produção, possibilidades: hardening checklist
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:modelcontextprotocol/servers
#   source: https://github.com/modelcontextprotocol/servers
#   licenses: Apache-2.0 (novo) / MIT (existente) — sem cópia literal (só catálogo + contrato)
