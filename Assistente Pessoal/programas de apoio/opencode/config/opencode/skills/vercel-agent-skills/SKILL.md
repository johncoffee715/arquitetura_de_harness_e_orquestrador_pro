---
name: vercel-agent-skills
description: >-
  Skills oficiais Vercel: react-best-practices (40+ regras/8 categorias), web-design-guidelines, composition-patterns, vercel-optimize (auditoria custo/perf). (absorvido de vercel-labs/agent-skills)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/vercel-labs/agent-skills
helenized: true
r84: true
r77_triple: true
---
# vercel-agent-skills — Vercel Agent Skills

Helenizado de [`https://github.com/vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Skills oficiais Vercel: react-best-practices (40+ regras/8 categorias), web-design-guidelines, composition-patterns, vercel-optimize (auditoria custo/perf). (absorvido de vercel-labs/agent-skills)

## Padrões absorvidos
- Vercel: Vercel, skills
- Origem: https://github.com/vercel-labs/agent-skills
- Domínio: Vercel Agent Skills

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `vercel-agent-skills` (tags: Vercel, skills).
2. `skill(name="vercel-agent-skills")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/vercel-labs/agent-skills
