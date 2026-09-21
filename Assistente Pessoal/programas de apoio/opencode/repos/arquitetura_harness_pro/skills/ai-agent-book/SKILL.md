---
name: ai-agent-book
description: "《深入理解 AI Agent：设计原理与工程实践》开源主仓库: 全书正文、PDF 与按章配套代码. (absorvido de bojieli/ai-agent-book)"
---
# Ai Agent Book

Helenizado de [`bojieli/ai-agent-book`](https://github.com/bojieli/ai-agent-book).

## Propósito
**中文** ← 当前 · [English](docs/en/README.md) · [Español](docs/es/README.md) · [Bahasa Indonesia](docs/id/README.md) · [العربية](docs/ar/README.md) · [繁體中文（台灣）](docs/zh-TW/README.md) · [Русский](docs/ru/README.md) · [Tiếng Việt](docs/vi/README.md) · [தமிழ்](docs/ta/README.md) · [日本語](docs/ja/README.md) · [Türkçe](docs/tr/README.md) · [한국어](docs/ko/README.md) · [Magyar](docs/hu/README.md)

## Padrões absorvidos (núcleo canônico do repo)
- Orquestrar conhecimento de design de agentes de IA: usar o livro como fonte de princípios de engenharia, arquitetura e padrões de design de agentes (capítulos 1-10 disponíveis como markdown)
- Consultar o código de exemplo por capítulo para implementar padrões de agentes (memória, tool calling, planejamento) em projetos reais
- Seguir o fluxo de build do repo (pandoc + xelatex + ElegantBook) para gerar PDFs dos documentos técnicos do projeto

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="ai-agent-book")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/bojieli/ai-agent-book
