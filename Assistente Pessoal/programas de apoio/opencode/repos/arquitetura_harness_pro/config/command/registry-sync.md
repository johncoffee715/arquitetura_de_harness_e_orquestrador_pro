---
name: registry-sync
description: "Sincroniza o AgentRegistry com skills, agents, commands e MCPs atuais"
argument-hint: "[--watch | --dry-run]"
allowed-tools:
  - Read
  - Bash
---

# /registry-sync — Auto-Registration Agent

Sincroniza o **AgentRegistry** (`~/.config/opencode/registry/`) com o estado atual de:
- `~/.claude/skills/` (skills instaladas)
- `~/.config/opencode/agents/` (agentes GSD)
- `~/.config/opencode/command/` (comandos)
- `~/.config/opencode/opencode.json` (MCPs)

## Como usar

```
/registry-sync         → sync único
/registry-sync --watch → modo observador contínuo
/registry-sync --dry-run → só mostra o que mudaria
```

## O que atualiza

1. `agent-registry.json` — catálogo central com agentes + skills
2. `capability-index.json` — índice de capacidades
3. `capability-router.json` — regras de roteamento
4. `event-bus.json` — tópicos dinâmicos por agente

## Automático

O hook **SessionStart** já executa `registry-sync` automaticamente
no início de cada sessão. Use este comando para forçar uma
sincronização manual a qualquer momento.
