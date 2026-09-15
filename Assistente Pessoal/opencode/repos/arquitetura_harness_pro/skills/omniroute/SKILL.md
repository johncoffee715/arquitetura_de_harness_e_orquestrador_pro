---
name: omniroute
description: "Never stop coding. Free MIT AI gateway: one endpoint, 290+ providers (90+ free), 500+ models. Quota-aware auto-fallback, RTK+Caveman compression saves 15-95% tokens, MCP/A2A. (absorvido de diegosouzapw/OmniRoute)"
---
# Omniroute

Helenizado de [`diegosouzapw/OmniRoute`](https://github.com/diegosouzapw/OmniRoute).

## Propósito
Never stop coding. Free MIT AI gateway: one endpoint, 290+ providers (90+ free), 500+ models. Works with Claude Code, Codex, Cursor, OpenCode, Cline & Copilot. Quota-aware auto-fallback, RTK+Caveman compression saves 15-95% tokens, MCP/A2A, Desktop/PWA.

## Padrões absorvidos (núcleo canônico do repo)
- 🗜️ Compression hardening** — default-on inflation guard, Caveman packs for DE / FR / JA + Chinese (wényán), RTK filters for Gradle & .NET. → [Compression](docs/compression/COMPRESSION_ENGINES.md)
- 💸 Honest flat-rate cost** — subscription / coding-plan providers read **$0** in cost analytics; budget, quota & routing keep estimating. → [API Reference](docs/reference/API_REFERENCE.md)
- ⚖️ Quota-Share routing** — split a shared account's quota fairly across pooled keys, work-conserving so idle slices are lent out. → [Resilience Guide](docs/architecture/RESILIENCE_GUIDE.md)
- 🤖 One-command CLI/agent setup** — `setup-*` configures 12+ coding tools; `omniroute launch` / `launch-codex` are zero-config. → [CLI Integrations](docs/guides/CLI-INTEGRATIONS.md)
- 🛰️ Remote mode** — drive a remote OmniRoute with scoped tokens (`connect` / `contexts` / `tokens`) + an `antigravity` OAuth helper for VPS installs. → [Remote Mode](docs/guides/REMOTE-MODE.md)
- 🕵️ Transparent MITM decrypt (TPROXY)** — capture CLIs that ignore proxy env vars, with a per-SNI CA + trust-store installer. → [MITM/TPROXY](docs/security/MITM-TPROXY-DECRYPT.md)
- 💸 Cost telemetry everywhere** — `X-OmniRoute-*` cost/usage headers on every endpoint, cache-HIT savings header, per-key USD spend quotas. → [API Reference](docs/reference/API_REFERENCE.md)
- 🧠 Memory you control** — off by default, opt-in int8 vector quantization + typed decay, per-request `x-omniroute-no-memory`. → [Memory](docs/frameworks/MEMORY.md)

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="omniroute")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/diegosouzapw/OmniRoute
