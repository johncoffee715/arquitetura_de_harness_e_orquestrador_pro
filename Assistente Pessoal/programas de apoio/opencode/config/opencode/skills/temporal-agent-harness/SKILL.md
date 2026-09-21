---
name: temporal-agent-harness
description: Durable agent harness pattern — agents as workflows (resume mid-turn), approval policy engine, Code Mode, callback tools, typed composable agents (patterns only).
category: skill
model: local-forge/proposer
---

# temporal-agent-harness

Harness de agentes duráveis: cada agente é um workflow (resume mid-turn sem perder
tokens), approvals com policy engine, Code Mode (1 tool que roda script sobre tools),
callback tools (cliente executa), agentes tipados e componíveis. Helenizado de
`temporal-community/temporal-agent-harness`
(origem: https://github.com/temporal-community/temporal-agent-harness).

> Experimental/pre-1.0 no original; aqui só padrões estáveis. Servidor/harness
> NUNCA como dependência.

## Quando usar

- Agente que precisa sobreviver a crash no meio do turn (resume exato, sem re-pagar tokens)
- Tool calls com aprovação humana granular (policy por tool, auto-approve só safe)
- Um turn orquestrando N calls (Code Mode: script tipado sobre tools)
- Tools que rodam no cliente (callback: laptop/celular do usuário)

## Como usar

1. **Agente=workflow**: turn com histórico replayável; crash retoma mid-turn
2. **Approvals**: policy em camadas (allow-lists, auto-approve safe, overrides por sessão)
3. **Code Mode**: `code_mode_tool(tools)` — modelo escreve script tipado, cada host-call é activity durável aprovada
4. **Callback**: contrato tipado; cliente executa; workflow espera (segundos ou dias)
5. **Interfaces tipadas**: `@agent.accepts` sobre pydantic; subagents como toolsets

## Princípio

Pin de versão sempre (pre-1.0 quebra sem aviso); event stream único p/ live + replay.
