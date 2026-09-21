# Conceito & Persona (Ontology)
---
name: deepspec
description: |
  Speculative-decoding draft methodology: DSpark/DFlash/Eagle3 training recipe
  (data-prep, train, eval) plus acceptance-rate benchmarks. Complements llama-mtp
  (inference mechanism) with the training/evaluation side.
category: skill
role: deepspec
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
#   - varredura: llama-mtp (MTP heads) + llama-mtp-concept (conceito) cobrem o MECANISMO;
#     nada cobre a RECEITA de treino/avaliação de drafts
#   - gap: CONFIRMED (estreito) — metodologia DSpark/DFlash/Eagle3 + benchmarks de acceptance

# R2 global:
#   - skill: deepspec
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: receita draft train/eval, debilidade: exige 8 GPUs + TB cache no default,
#   possibilidades: eval de acceptance em drafts locais pequenos
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:deepseek-ai/DeepSpec
#   source: https://github.com/deepseek-ai/DeepSpec
#   licenses: MIT — sem cópia literal (só metodologia + benchmarks)
#   correção: repo é speculative decoding, NÃO spec-driven development
