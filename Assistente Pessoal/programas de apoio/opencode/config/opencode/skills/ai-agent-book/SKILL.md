---
name: ai-agent-book
description: >-
  《深入理解 AI Agent：设计原理与工程实践》开源主仓库: 全书正文、PDF 与按章配套代码. (absorvido de bojieli/ai-agent-book)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/bojieli/ai-agent-book
helenized: true
r84: true
r77_triple: true
---
# ai-agent-book — livro de padrões de agentes

Helenizado de [`https://github.com/bojieli/ai-agent-book`](https://github.com/bojieli/ai-agent-book) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
《深入理解 AI Agent：设计原理与工程实践》开源主仓库: 全书正文、PDF 与按章配套代码. (absorvido de bojieli/ai-agent-book)

## Padrões absorvidos
- educação agentic: padrões de agente, arquitetura, tool calling
- Origem: https://github.com/bojieli/ai-agent-book
- Domínio: livro de padrões de agentes

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `ai-agent-book` (tags: padrões de agente, arquitetura).
2. `skill(name="ai-agent-book")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/bojieli/ai-agent-book
