---
name: gemini-mcp-tool
description: >-
  MCP server que dá ao agente acesso ao Gemini CLI / Antigravity CLI (agy) — janela massiva para análise de arquivos/codebases grandes e brainstorm em 3 vozes. (absorvido de jamubc/gemini-mcp-tool). Aviso: Gemini CLI foi aposentado em 2026-06-18; backend padrão agora é agy.
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/jamubc/gemini-mcp-tool
helenized: true
r84: true
r77_triple: true
---
# gemini-mcp-tool — MCP Gemini

Helenizado de [`https://github.com/jamubc/gemini-mcp-tool`](https://github.com/jamubc/gemini-mcp-tool) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
MCP server que dá ao agente acesso ao Gemini CLI / Antigravity CLI (agy) — janela massiva para análise de arquivos/codebases grandes e brainstorm em 3 vozes. (absorvido de jamubc/gemini-mcp-tool). Aviso: Gemini CLI foi aposentado em 2026-06-18; backend padrão agora é agy.

## Padrões absorvidos
- integração Gemini: MCP, Gemini, tool
- Origem: https://github.com/jamubc/gemini-mcp-tool
- Domínio: MCP Gemini

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `gemini-mcp-tool` (tags: MCP, Gemini).
2. `skill(name="gemini-mcp-tool")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/jamubc/gemini-mcp-tool
