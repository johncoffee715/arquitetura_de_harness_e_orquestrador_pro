---
name: azure-skills
description: >-
  Suite de skills MS Azure: ai, diagnostics, observability — referência de deployment e diagnóstico de agentes em nuvem gerenciada. (absorvido de microsoft/github-copilot-for-azure)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/microsoft/github-copilot-for-azure
helenized: true
r84: true
r77_triple: true
---
# azure-skills — skills Azure

Helenizado de [`https://github.com/microsoft/github-copilot-for-azure`](https://github.com/microsoft/github-copilot-for-azure) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Suite de skills MS Azure: ai, diagnostics, observability — referência de deployment e diagnóstico de agentes em nuvem gerenciada. (absorvido de microsoft/github-copilot-for-azure)

## Padrões absorvidos
- cloud skills: Azure, cloud, infra
- Origem: https://github.com/microsoft/github-copilot-for-azure
- Domínio: skills Azure

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `azure-skills` (tags: Azure, cloud).
2. `skill(name="azure-skills")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/microsoft/github-copilot-for-azure
