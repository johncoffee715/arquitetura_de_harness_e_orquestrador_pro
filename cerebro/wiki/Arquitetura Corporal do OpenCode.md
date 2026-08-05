---
aliases:
  - "Arquitetura OpenCode"
  - "Corpo do OpenCode"
tags:
  - arquitetura
  - opencode
  - sistema
  - MOC
---

# 🧠🦾🦿 Arquitetetura Corporal do OpenCode

> "OpenCode é a cabeça, Tesseract são os olhos, agents/subagents/skills/MCP são o tronco, braços e pernas."

## Visão Geral

```
┌─────────────────────────────────────────┐
│           🧠 CABEÇA (OpenCode)          │
│    Pensa, planeja, decide, orquestra    │
└──────────────────┬──────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼───┐    ┌────▼────┐   ┌────▼────┐
│👁️👁️    │    │🦴 TRONCO│   │💪 BRAÇOS│
│ OLHOS  │    │ AGENTS  │   │ SKILLS  │
│OCR/Visão│   │Execução │   │Habilidades│
└───┬───┘    └────┬────┘   └────┬────┘
    │              │              │
    └──────────────┼──────────────┘
                   │
            ┌──────▼──────┐
            │🦵 PERNAS    │
            │ MCPs/Externo │
            └─────────────┘
```

## 🧠 Cabeça — OpenCode
- Modelo LLM para raciocínio
- Contexto e memória de curto prazo
- CLAUDE.md como personalidade
- Skills carregadas sob demanda

## 👁️👁️ Olhos — Tesseract OCR + Visão
- **Tesseract 5.5.2** — OCR PT+EN
- **pdftotext** — Extração de PDFs
- **Text Extractor** — Plugin Obsidian
- **webfetch/websearch** — Visão da internet

## 🦴 Tronco — Agents
- **Oracle** — Consultor High-IQ
- **Build** — Desenvolvedor principal
- **Explore** — Explorador de código
- **Librarian** — Busca documentação
- **Reverser** — Engenharia reversa

## 💪 Braços — Skills (100+)
- **shared/programming** — Python, Rust, TS, Go
- **tdd-workflow** — Test-Driven Development
- **security-research** — Caça-falhas
- **electronics-debug** — Hardware debug
- **firmware-reverse** — RE de firmware
- **cerebral-wikia** — Wiki persistente

## 🦵 Pernas — MCPs
- **GhidraMCP** — Engenharia reversa
- **Context7** — Documentação de libs
- **Playwright** — Navegação web
- **Obsidian** — Cérebro compartilhado

## Princípios
1. Olhos antes de agir
2. Cabeça delega, não executa
3. Braços especializados
4. Pernas conectam ao mundo
5. Memória compartilhada

---
*Arquitetura v1.0 — 2026-07-17*
