---
name: pi
description: "AI agent toolkit: unified LLM API, agent loop, TUI, coding agent CLI. (absorvido de earendil-works/pi)"
---
# Pi

Helenizado de [`earendil-works/pi`](https://github.com/earendil-works/pi).

## Propósito
This is the home of the Pi agent harness project including our self extensible coding agent.

## Padrões absorvidos (núcleo canônico do repo)
- [@earendil-works/pi-coding-agent](packages/coding-agent)**: Interactive coding agent CLI
- [@earendil-works/pi-agent-core](packages/agent)**: Agent runtime with tool calling and state management
- [@earendil-works/pi-ai](packages/ai)**: Unified multi-provider LLM API (OpenAI, Anthropic, Google, …)
- [Visit pi.dev](https://pi.dev), the project website with demos
- [Read the documentation](https://pi.dev/docs/latest), but you can also ask the agent to explain itself
- Gondolin extension**: keep `pi` and provider auth on the host while routing built-in tools and `!` commands into a local Linux micro-VM.
- Plain Docker**: run the whole `pi` process in a local container for simple isolation.
- OpenShell**: run the whole `pi` process in a policy-controlled sandbox.

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="pi")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/earendil-works/pi
