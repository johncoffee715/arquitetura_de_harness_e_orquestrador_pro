---
name: code-review-graph
description: >-
  Local-first code intelligence graph for MCP and CLI. Persistent map of codebase so AI tools read only what matters. (absorvido de tirth8205/code-review-graph)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/tirth8205/code-review-graph
helenized: true
r84: true
r77_triple: true
---
# code-review-graph — grafo de review

Helenizado de [`https://github.com/tirth8205/code-review-graph`](https://github.com/tirth8205/code-review-graph) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Local-first code intelligence graph for MCP and CLI. Persistent map of codebase so AI tools read only what matters. (absorvido de tirth8205/code-review-graph)

## Padrões absorvidos
- análise grafo: grafo, dependência, review
- Origem: https://github.com/tirth8205/code-review-graph
- Domínio: grafo de review

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `code-review-graph` (tags: grafo, dependência).
2. `skill(name="code-review-graph")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/tirth8205/code-review-graph
