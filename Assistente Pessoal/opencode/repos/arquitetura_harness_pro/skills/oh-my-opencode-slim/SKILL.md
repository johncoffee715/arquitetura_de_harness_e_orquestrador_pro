---
name: oh-my-opencode-slim
description: "Lean, fine-tuned Opencode multi agent suite. Mix any models, auto-delegate tasks. (absorvido de alvinunreal/oh-my-opencode-slim)"
---
# Oh My Opencode Slim

Helenizado de [`alvinunreal/oh-my-opencode-slim`](https://github.com/alvinunreal/oh-my-opencode-slim).

## Propósito
oh-my-opencode-slim is an agent orchestration plugin for OpenCode. It includes a built-in team of specialized agents that can scout a codebase, look up fresh documentation, review architecture, handle UI work, and execute well-scoped implementation tasks under one orchestrator.

## Padrões absorvidos (núcleo canônico do repo)
- [Seven specialized agents](#meet-the-pantheon)** - Orchestrator, Explorer,
- [Background orchestration](docs/background-orchestration.md)** - the
- [Bundled skills](#skills)** - prompt-based workflows like `deepwork`,
- [Council](docs/council.md)** - run multiple models in parallel on the same
- [Companion](docs/companion.md)** - an optional floating desktop window
- [Multiplexer integration](docs/multiplexer-integration.md)** - watch agents
- [Preset switching](docs/preset-switching.md)** - swap the whole team's
- [Code intelligence tools](docs/tools.md)** - LSP tools, AST-aware search

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="oh-my-opencode-slim")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/alvinunreal/oh-my-opencode-slim
