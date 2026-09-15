---
name: open-design
description: Agent-driven design artifacts — prototypes/decks/dashboards/images/video as real files (HTML/PDF/PPTX/MP4) via BYOK CLIs + DeepSeek Harness.
category: skill
model: local-forge/proposer
---

# open-design

Design dirigido por agente: brief → artefatos reais (protótipos, decks, dashboards,
imagens, vídeo) em arquivos de verdade (HTML/PDF/PPTX/MP4), via CLIs com BYOK +
DeepSeek Harness nativo. Helenizado de `nexu-io/open-design`
(origem: https://github.com/nexu-io/open-design).

> Irmã `dashi-ppt-skill` cobre decks; aqui o FOCO é o loop design completo
> (protótipo→dashboard→deck→imagem→vídeo) + BYOK multi-CLI.

## Quando usar

- Protótipo navegável a partir de brief (single-file HTML)
- Deck/dashboard/imagem/vídeo com export real
- Design system como contrato de marca (`DESIGN.md`)

## Como usar

1. **Brief**: tipo de artefato + direção (ou extrair de referências p/ `DESIGN.md`)
2. **Gerar**: CLI com BYOK (Claude/Codex/Cursor/DeepSeek/OpenCode…); HyperFrames p/ vídeo
3. **Refinar**: iterar no preview; handoff p/ engenharia em HTML/CSS real
4. **Exportar**: HTML / PDF / PPTX / MP4

## Princípio

Artefato real ou nada: nada de mock estático — HTML/CSS vivo, exportável, versionável.
