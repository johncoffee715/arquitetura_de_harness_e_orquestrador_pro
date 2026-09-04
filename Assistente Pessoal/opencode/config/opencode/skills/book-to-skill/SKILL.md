---
name: book-to-skill
description: >-
  Converts books and documents (PDF, EPUB, DOCX, HTML, Markdown, plain text, RTF, MOBI/AZW with Calibre) into structured agent skills, extracting frameworks, mental models, principles, techniques, and anti-patterns. Use when the user wants to study a document through GitHub Copilot CLI, Amp, or Claude
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/book-to-skill
helenized: true
r84: true
r77_triple: true
---
# book-to-skill — livro para skill

Helenizado de [`https://github.com/book-to-skill`](https://github.com/book-to-skill) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Converts books and documents (PDF, EPUB, DOCX, HTML, Markdown, plain text, RTF, MOBI/AZW with Calibre) into structured agent skills, extracting frameworks, mental models, principles, techniques, and anti-patterns. Use when the user wants to study a document through GitHub Copilot CLI, Amp, or Claude

## Padrões absorvidos
- conversão livro: livro→skill, destilação, helenização
- Origem: https://github.com/book-to-skill
- Domínio: livro para skill

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `book-to-skill` (tags: livro→skill, destilação).
2. `skill(name="book-to-skill")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/book-to-skill
