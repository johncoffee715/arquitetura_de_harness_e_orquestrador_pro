---
name: last30days-skill
description: >-
  Pesquisa/síntese multi-plataforma 30d (Reddit, X, YouTube, HN, Polymarket) com ranking por upvotes — ADAPTADO: só a pipeline de briefing, nunca hook cru (RCE upstream corrigido). (absorvido de mvanhorn/last30days-skill)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/mvanhorn/last30days-skill
helenized: true
r84: true
r77_triple: true
---
# last30days-skill — pesquisa 30d multi-plataforma

Helenizado de [`https://github.com/mvanhorn/last30days-skill`](https://github.com/mvanhorn/last30days-skill) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Pesquisa/síntese multi-plataforma 30d (Reddit, X, YouTube, HN, Polymarket) com ranking por upvotes — ADAPTADO: só a pipeline de briefing, nunca hook cru (RCE upstream corrigido). (absorvido de mvanhorn/last30days-skill)

## Padrões absorvidos
- pesquisa: Reddit, X, YouTube
- Origem: https://github.com/mvanhorn/last30days-skill
- Domínio: pesquisa 30d multi-plataforma

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `last30days-skill` (tags: Reddit, X).
2. `skill(name="last30days-skill")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/mvanhorn/last30days-skill
