---
source: Rafael Quintanilha - QuantBrasil (YouTube)
date: 2026-07-16
type: video
tags: [source/video, domain/llm-wiki, domain/obsidian]
youtube_id: 2KUF9BB_rh8
---
# Obsidian como Cérebro para Agentes de IA

## Principais Takeaways

1. **Obsidian como Second Brain para IA** — Rafael Quintanilha mostra como usar Obsidian como base de conhecimento persistente que agentes de IA podem consultar via CLI.

2. **Headless Obsidian** — Obsidian roda em um VPS sem GUI, usando `obsidian-cli` para criar, ler, buscar e atualizar notas via terminal.

3. **Separação Repo vs Vault** — GitHub repos são para código e tasks; Obsidian vault é para pensamentos, arquitetura, decisões. O agente lê do vault para ENTENDER e escreve no repo para EXECUTAR.

4. **OpenClaw** — Plataforma multi-agent Rafael criou, roteia respostas do agente para Slack/WhatsApp.

## Componentes Devorados (Refatorado para OpenCode)

### Headless Vault
- **Pattern**: Obsidian roda sem interface gráfica
- **Refatoração OpenCode**: `/mnt/dados/cerebro com IA/` como vault compartilhado
- **Status**: ✅ implementado

### obsidian-cli
- **Pattern**: CLI para manipular notas sem GUI
- **Refatoração OpenCode**: cerebral-wikia skill com comandos `ingestar`, `consultar`, `lintar`
- **Status**: ✅ implementado

### Repo vs Vault Separation
- **Pattern**: Código ≠ Conhecimento
- **Refatoração OpenCode**: raw/ vs wiki/ vs schema (AGENTS.md)
- **Status**: ✅ implementado

### Bidirectional Link Traversal
- **Pattern**: `[[wikilinks]]` conectam páginas
- **Refatoração OpenCode**: Páginas interligadas em `/mnt/dados/cerebro com IA/wiki/`
- **Status**: ✅ implementado

## Entidades Mencionadas

- `#agent/claude-code` — LLM principal usado
- `#agent/openclaw` — multi-agent platform
- `#tool/obsidian-cli` — interface de linha de comando
- `#tool/headless-sync` — plugin Obsidian Sync

## Aplicação no Gran-Mestre

Este vídeo inspirou a **Antropofagia Tecnológica v5.0**:
- Intelecto Compartilhado via `/mnt/dados/cerebro com IA/`
- Skills cerebral-wikia + intelecto-compartilhado
- Refatoração global de outras ferramentas de IA