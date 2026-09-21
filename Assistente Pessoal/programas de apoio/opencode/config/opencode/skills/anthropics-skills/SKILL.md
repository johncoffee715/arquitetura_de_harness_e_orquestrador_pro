---
name: anthropics-skills
description: >-
  Catálogo oficial de Agent Skills (17): mcp-builder, skill-creator (evals quantitativos), frontend-design, pdf/docx/xlsx/pptx, webapp-testing — habilita o padrão SKILL.md oficial no harness. (absorvido de anthropics/skills)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/anthropics/skills
helenized: true
r84: true
r77_triple: true
---
# anthropics-skills — skills Anthropics

Helenizado de [`https://github.com/anthropics/skills`](https://github.com/anthropics/skills) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Catálogo oficial de Agent Skills (17): mcp-builder, skill-creator (evals quantitativos), frontend-design, pdf/docx/xlsx/pptx, webapp-testing — habilita o padrão SKILL.md oficial no harness. (absorvido de anthropics/skills)

## Padrões absorvidos
- skills oficiais: skills Claude, prompt engineering, tool use
- Origem: https://github.com/anthropics/skills
- Domínio: skills Anthropics

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `anthropics-skills` (tags: skills Claude, prompt engineering).
2. `skill(name="anthropics-skills")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/anthropics/skills
