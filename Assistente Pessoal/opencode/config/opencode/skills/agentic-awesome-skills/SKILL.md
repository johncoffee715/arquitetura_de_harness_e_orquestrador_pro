---
name: agentic-awesome-skills
description: >-
  >- Catálogo selecionado de skills agentic do ecossistema (helenizado de agentics-org/agentic-awesome-skills): referência de padrões de skills para memória, segurança, pesquisa e automação. Use ao projetar skills novas no harness (catálogo primeiro, constrói só o GAP — regra R8), ao buscar padrão de 
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/agentic-awesome-skills
helenized: true
r84: true
r77_triple: true
---
# agentic-awesome-skills — catálogo de padrões agentic

Helenizado de [`https://github.com/agentic-awesome-skills`](https://github.com/agentic-awesome-skills) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
>- Catálogo selecionado de skills agentic do ecossistema (helenizado de agentics-org/agentic-awesome-skills): referência de padrões de skills para memória, segurança, pesquisa e automação. Use ao projetar skills novas no harness (catálogo primeiro, constrói só o GAP — regra R8), ao buscar padrão de 

## Padrões absorvidos
- curadoria de padrões: padrões agentic, catálogo primeiro R8, memória
- Origem: https://github.com/agentic-awesome-skills
- Domínio: catálogo de padrões agentic

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `agentic-awesome-skills` (tags: padrões agentic, catálogo primeiro R8).
2. `skill(name="agentic-awesome-skills")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/agentic-awesome-skills
