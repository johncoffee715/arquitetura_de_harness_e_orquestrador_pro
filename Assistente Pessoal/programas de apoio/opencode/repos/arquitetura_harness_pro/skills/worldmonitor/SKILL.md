---
name: worldmonitor
description: "Real-time global intelligence dashboard. AI-powered news aggregation, geopolitical monitoring, infrastructure tracking. (absorvido de koala73/worldmonitor)"
---
# Worldmonitor

Helenizado de [`koala73/worldmonitor`](https://github.com/koala73/worldmonitor).

## Propósito
**Real-time global intelligence dashboard** — AI-powered news aggregation, geopolitical monitoring, and infrastructure tracking in a unified situational awareness interface.

## Padrões absorvidos (núcleo canônico do repo)
- 500+ curated news feeds** across 15 categories, AI-synthesized into briefs
- Dual map engine** — 3D globe (globe.gl) and WebGL flat map (deck.gl) with 56 map layer types
- Cross-stream correlation** — military, economic, disaster, and escalation signal convergence
- Country Instability Index (CII)** — server-authoritative CII v8 stress scoring for 31 Tier-1 countries
- Finance radar** — 29 stock exchanges, commodities, crypto, and 7-signal market composite
- Local AI** — run everything with Ollama, no API keys required
- 6 site variants** from a single codebase (world, tech, finance, commodity, happy, energy)
- Native desktop app** (Tauri 2) for macOS, Windows, and Linux

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="worldmonitor")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/koala73/worldmonitor
