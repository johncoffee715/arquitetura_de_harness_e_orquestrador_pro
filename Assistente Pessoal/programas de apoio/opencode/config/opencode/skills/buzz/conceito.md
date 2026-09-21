# Conceito & Persona (Ontology)
---
name: buzz
description: |
  Offline transcription pipeline: audio separation, hardware-matched Whisper
  backend, speaker diarization, punctuation, SRT/VTT/TXT export, watch-folder
  and CLI. Patterns only.
category: skill
role: buzz
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
#   - varredura: NADA cobre transcrição/diarização de áudio no catálogo
#   - gap: CONFIRMED — pipeline offline de transcrição (só padrão)

# R2 global:
#   - skill: buzz
#     binding: skill
#     category: skill

# R77 3-layer helenization:
#   1. Ontology & persona (system prompt imutável)
#   2. Gabarito/firewall (esquema rígido, stop_tokens, GBNF)
#   3. Mecânica de ignição (motor determinístico, validação, anti-loop)

# R28 categórico veredito:
#   Capacidades: pipeline completo, debilidade: deps nativas pesadas (torch/CUDA),
#   possibilidades: transcrever sessões p/ o vault
#   Score: ≥90 (escala R34)
#   Evidência: frontmatter válido + mecanica.py smoke + gabarito JSON válido

# Provenance (helenização):
#   origin: absorvido:chidiwilliams/buzz
#   source: https://github.com/chidiwilliams/buzz
#   licenses: MIT — sem cópia literal (só pipeline)
