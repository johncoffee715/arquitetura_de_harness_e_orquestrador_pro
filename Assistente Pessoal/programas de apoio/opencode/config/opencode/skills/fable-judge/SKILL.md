---
name: fable-judge
description: >-
  Verificação adversarial de trabalho concluído. Trata qualquer 'done' como conjunto de afirmações, re-executa cada verificação afirmada, detecta checks enfraquecidos e falsos completos. Use após qualquer agente/modelo afirmar que trabalho está completo.
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/Sahir619/fable-method
helenized: true
r84: true
r77_triple: true
---
# fable-judge — juiz fabular

Helenizado de [`https://github.com/Sahir619/fable-method`](https://github.com/Sahir619/fable-method) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Verificação adversarial de trabalho concluído. Trata qualquer 'done' como conjunto de afirmações, re-executa cada verificação afirmada, detecta checks enfraquecidos e falsos completos. Use após qualquer agente/modelo afirmar que trabalho está completo.

## Padrões absorvidos
- avaliação: julgamento, veredito, R28
- Origem: https://github.com/Sahir619/fable-method
- Domínio: juiz fabular

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `fable-judge` (tags: julgamento, veredito).
2. `skill(name="fable-judge")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/Sahir619/fable-method
