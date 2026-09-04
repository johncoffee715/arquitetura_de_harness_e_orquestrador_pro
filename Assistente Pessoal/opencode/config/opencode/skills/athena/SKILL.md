---
name: athena
description: >-
  Agente de revisão macro do Gran-Mestre. Revisa o diff total de uma feature (coerência cross-task, acoplamento, arquitetura) — diferente do Code Reviewer, que revisa micro (por task)." model: github-copilot/claude-opus-4.7 mode: subagent
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/athena
helenized: true
r84: true
r77_triple: true
---
# athena — revisão arquitetural

Helenizado de [`https://github.com/athena`](https://github.com/athena) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Agente de revisão macro do Gran-Mestre. Revisa o diff total de uma feature (coerência cross-task, acoplamento, arquitetura) — diferente do Code Reviewer, que revisa micro (por task)." model: github-copilot/claude-opus-4.7 mode: subagent

## Padrões absorvidos
- quality gate: revisão macro, contrato, Atena
- Origem: https://github.com/athena
- Domínio: revisão arquitetural

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `athena` (tags: revisão macro, contrato).
2. `skill(name="athena")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/athena
