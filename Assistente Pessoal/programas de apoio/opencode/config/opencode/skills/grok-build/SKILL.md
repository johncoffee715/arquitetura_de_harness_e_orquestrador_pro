---
name: grok-build
description: TUI-agent construction patterns — composition-root binary, workspace (fs/VCS/exec/checkpoints), headless/leader/stdio modes (patterns only).
category: skill
model: local-forge/proposer
---

# grok-build

Padrões de construção de um coding-agent em TUI: binário composition-root,
workspace (filesystem/VCS/execução/checkpoints), 3 modos de entrada
(headless/leader/stdio), tools próprias + user-guide como docs.
Helenizado de `xai-org/grok-build` (origem: https://github.com/xai-org/grok-build,
SHA 3794978, rev c4ea71cf).

> Clonado e lido na fonte (`/tmp/opencode/repos/grok-build`, 95M, Apache-2.0).
> Só padrões — nunca o runtime Rust como dependência.

## Quando usar

- Desenhar CLI/TUI de agente (composition root + crates por domínio)
- Isolar workspace (fs/VCS/exec/checkpoints) do resto do runtime
- Rodar o mesmo agente interativo, headless (CI) ou embarcado (ACP)

## Como usar

1. **Composition root**: 1 bin crate monta tudo; resto são libs por domínio
2. **Workspace**: fs + VCS + execução + checkpoints num módulo só
3. **Modos**: headless (script/CI), leader (orquestra), stdio (embarcado via ACP)
4. **Docs**: user-guide versionado junto (auth, atalhos, MCP, skills, sandbox)

## Princípio

Notices de terceiros em dia (ports de codex/opencode aqui têm §4(b) explícito).
Contribuições externas fechadas no original — absorver padrão, não o projeto.
