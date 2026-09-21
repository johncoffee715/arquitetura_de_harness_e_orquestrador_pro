---
name: coderabbit
description: >-
  CodeRabbit AI code review: awesome list + pipeline de revisão automatizada de PRs (spans, dicas acionáveis) — padrão p/ feature/hook de review contínuo do harness. (absorvido de coderabbitai/awesome-coderabbit)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/coderabbitai/awesome-coderabbit
helenized: true
r84: true
r77_triple: true
---
# coderabbit — code review AI

Helenizado de [`https://github.com/coderabbitai/awesome-coderabbit`](https://github.com/coderabbitai/awesome-coderabbit) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
CodeRabbit AI code review: awesome list + pipeline de revisão automatizada de PRs (spans, dicas acionáveis) — padrão p/ feature/hook de review contínuo do harness. (absorvido de coderabbitai/awesome-coderabbit)

## Padrões absorvidos
- review: review, PR, qualidade
- Origem: https://github.com/coderabbitai/awesome-coderabbit
- Domínio: code review AI

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `coderabbit` (tags: review, PR).
2. `skill(name="coderabbit")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/coderabbitai/awesome-coderabbit
