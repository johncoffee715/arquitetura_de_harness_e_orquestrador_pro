---
name: orca
description: "Orca is the ADE for working with a fleet of parallel agents. Run any coding agent with your own subscription. (absorvido de stablyai/orca)"
---
# Orca

Helenizado de [`stablyai/orca`](https://github.com/stablyai/orca).

## Propósito
Orca is the ADE (Agent Development Environment) for working with a fleet of parallel agents. Run any coding agent with your own subscription. Available on desktop, mobile and VPS.

## Padrões absorvidos (núcleo canônico do repo)
- [Quick open](https://www.onorca.dev/docs/model/quick-open)** — Search across worktrees, files, agents, commands, and repo context without leaving your flow.
- [Account switcher &amp; usage tracking](https://www.onorca.dev/docs/agents/usage-tracking)** — See Claude and Codex usage and rate-limit resets, and hot-swap accounts without re-logging in.
- [Rich repo previews](https://www.onorca.dev/docs/editing/markdown)** — Preview Markdown, images, PDFs, and repo docs in the workspace.
- [Computer Use](https://www.onorca.dev/docs/cli/computer-use)** — Let agents operate desktop apps and visible UI when a workflow needs real interaction.
- [Notifications and unread state](https://www.onorca.dev/docs/notifications)** — Know when an agent finishes or needs attention, then mark threads unread to come back later.
- And many, many more** — we ship daily, so this list is perpetually behind. The [changelog](https://github.com/stablyai/orca/releases) is the real feature list.
- [Download from onOrca.dev](https://onorca.dev/download)**
- Running `orca serve` on a headless Linux server? See the [headless Linux server guide](docs/reference/headless-linux-server.md).

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="orca")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/stablyai/orca
