---
name: i-have-adhd
description: >-
  A skill to stop your coding agent from burying the answer. ADHD-friendly output. (absorvido de ayghri/i-have-adhd)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/ayghri/i-have-adhd
helenized: true
r84: true
r77_triple: true
---
# i-have-adhd — acessibilidade ADHD

Helenizado de [`https://github.com/ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
A skill to stop your coding agent from burying the answer. ADHD-friendly output. (absorvido de ayghri/i-have-adhd)

## Padrões absorvidos
- acessibilidade: ADHD, foco, acessibilidade
- Origem: https://github.com/ayghri/i-have-adhd
- Domínio: acessibilidade ADHD

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `i-have-adhd` (tags: ADHD, foco).
2. `skill(name="i-have-adhd")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/ayghri/i-have-adhd
