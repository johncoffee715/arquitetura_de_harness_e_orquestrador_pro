---
name: claude-mem
description: "Memória persistente entre sessões: captura o que o agente faz, comprime com IA e injeta contexto relevante de volta. Multi-agente (Claude Code, OpenClaw, Codex, Gemini, OpenCode+). (absorvido de thedotmack/claude-mem)"
---
# Claude-Mem

Helenizado de [`thedotmack/claude-mem`](https://github.com/thedotmack/claude-mem) (v13.4.0, Apache-2.0, Trendshift).

## Propósito
Sistema de **compressão de memória persistente**: captura tudo o que o agente faz durante a sessão, comprime com IA e injeta o contexto relevante de volta em sessões futuras. Funciona com Claude Code, OpenClaw, Codex, Gemini, Copilot e OpenCode.

## Padrões absorvidos (núcleo canônico do repo)
- **Capture-ecomprima**: cada sessão é capturada integralmente; a compressão (LLM-driven) reduz o volume antes do armazenamento de longo prazo — padrão que casa com `harness/context-compaction` (ARMARENAR→COMPACTAR→LIMPAR).
- **Injeção de contexto relevante por busca**: em sessões futuras, só o contexto relevante é injetado (busca sobre memória comprimida, não replay bruto).
- **Stack de armazenamento**: `~/.claude-mem/claude-mem.db` (SQLite) + `~/.claude-mem/chroma/` (embeddings/Chroma) — SQLite p/ metadados, Chroma p/ similaridade.
- **Multi-agente**: um único backend de memória atende vários agentes (Claude Code, OpenClaw, Codex, Gemini, Copilot, OpenCode) — memória como infra compartilhada, não acoplada ao agente.
- **Plugin/mercado**: instalável como plugin (`~/.claude/plugins/marketplaces/thedotmack/`); hooks de cursor (`cursor-hooks/`), integração openclaw (`openclaw/`).
- **Build idiossincrático**: Bun + uv (Python p/ Chroma), auto-instaláveis — baixo atrito de setup.

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade de memória cross-session: trabalho multi-sessão, retomada, contexto disperso.
2. Carregar skill (`skill(name="claude-mem")`).
3. Aplicar o ciclo: capturar sessão completa → comprimir com IA → armazenar (SQLite+embeddings) → injetar apenas o relevante na próxima sessão.
4. Manter memória como infra compartilhada entre agentes (não por-agente).

## Fonte
https://github.com/thedotmack/claude-mem