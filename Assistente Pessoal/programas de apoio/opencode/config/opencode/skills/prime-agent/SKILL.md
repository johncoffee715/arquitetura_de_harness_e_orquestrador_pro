---
name: prime-agent
description: >-
  Agente RLM self-improving: contexto como variável, tools como funções, subagents recursivos, harness contínuo com estado durável, IPython persistente. (absorvido de PrimeIntellect-ai/prime-agent)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/PrimeIntellect-ai/prime-agent
helenized: true
r84: true
r77_triple: true
---
# prime-agent — Prime Agent

Helenizado de [`https://github.com/PrimeIntellect-ai/prime-agent`](https://github.com/PrimeIntellect-ai/prime-agent) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Agente RLM self-improving: contexto como variável, tools como funções, subagents recursivos, harness contínuo com estado durável, IPython persistente. (absorvido de PrimeIntellect-ai/prime-agent)

## Padrões absorvidos
- agente: prime, agente
- Origem: https://github.com/PrimeIntellect-ai/prime-agent
- Domínio: Prime Agent

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `prime-agent` (tags: prime, agente).
2. `skill(name="prime-agent")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/PrimeIntellect-ai/prime-agent
