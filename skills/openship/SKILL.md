---
name: openship
description: "Self-hosted deployment platform. (absorvido de oblien/openship)"
---
# Openship

Helenizado de [`oblien/openship`](https://github.com/oblien/openship).

## Propósito
Open-source, self-hostable deployment platform with built-in CI/CD.<br>

## Padrões absorvidos (núcleo canônico do repo)
- Desktop app** — full GUI, real-time logs, one-click everything. Best for solo.
- Web dashboard** — the same UI in the browser, built for teams.
- CLI** — scriptable and CI-friendly; also how you install and manage a self-hosted instance.
- Openship Cloud** — managed, auto-scaling, zero setup
- Any VPS** — Hetzner, DigitalOcean, Linode, OVH, and the rest
- Dedicated servers** — bare metal, colo, homelab
- Multi-server** — spread workloads across machines
- Report it here (preferred):** [Report a vulnerability](https://github.com/oblien/openship/security/advisories/new) — a private GitHub advisory, visible only to you and the maintainers.

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="openship")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/oblien/openship
