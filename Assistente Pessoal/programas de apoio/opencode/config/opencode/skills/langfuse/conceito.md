# Conceito & Persona (Ontology)
---
name: langfuse
description: |
  LLM observability loop: instrumented tracing, versioned prompts, datasets with
  comparable runs, evaluations (judge/code/human/custom), playground iteration.
category: skill
role: langfuse
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
#   - varredura: MELT nativo cobre métricas/eventos/logs/traces do harness;
#     NADA cobre o loop trace→dataset→eval→playground p/ apps LLM
#   - gap: CONFIRMED — observability loop (nunca a plataforma como dependência)

# R2 global:
#   - skill: langfuse
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: loop eval, debilidade: self-host pesado,
#   possibilidades: datasets p/ crivos R83
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:langfuse/langfuse
#   source: https://github.com/langfuse/langfuse
#   licenses: MIT (exceto pastas ee/) — sem cópia literal (só o loop)
