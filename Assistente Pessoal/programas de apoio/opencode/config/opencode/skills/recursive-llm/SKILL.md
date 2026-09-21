---
name: recursive-llm
description: >-
  RLM (Recursive Language Model) p/ contexto longo eficiente: contexto vive em REPL Python, modelo explora/particiona recursivamente — 1M+ tokens com menos tokens de LLM e sem context rot. (absorvido de grishahq/recursive-llm)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/grishahq/recursive-llm
helenized: true
r84: true
r77_triple: true
---
# recursive-llm — LLM recursivo

Helenizado de [`https://github.com/grishahq/recursive-llm`](https://github.com/grishahq/recursive-llm) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
RLM (Recursive Language Model) p/ contexto longo eficiente: contexto vive em REPL Python, modelo explora/particiona recursivamente — 1M+ tokens com menos tokens de LLM e sem context rot. (absorvido de grishahq/recursive-llm)

## Padrões absorvidos
- recursivo: recursão, LLM
- Origem: https://github.com/grishahq/recursive-llm
- Domínio: LLM recursivo

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `recursive-llm` (tags: recursão, LLM).
2. `skill(name="recursive-llm")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/grishahq/recursive-llm
