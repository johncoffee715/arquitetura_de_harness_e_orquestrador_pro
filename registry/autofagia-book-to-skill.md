# Autofagia: Book-to-Skill

**Data:** 2026-08-03 (Rodada 8 — 26 alvos)
**Fonte:** https://github.com/virgiliojr94/book-to-skill (16k★, MIT)
**Objetivo:** Absorver **meta-skill** que converte livro/documento em skill acionável — extraindo estrutura, não resumo

---

## 1. O que é

Skill que transforma PDF/EPUB/DOCX/HTML/MD/TXT/RTF (e MOBI/AZW via Calibre) em skills de agente: frameworks nomeados, princípios acionáveis, técnicas passo-a-passo, anti-padrões e calibração de voz do autor. Compatível com Copilot CLI, Amp, Claude Code (raízes `~/.claude/skills`, `.agents/skills`, etc.).

## 2. Padrões absorvidos

- **Extract structure, not summaries** — a filosofia: skill não é book report, é toolkit
- **Preserve a precisão do autor** — nomes de frameworks são exatos ("5 Whys" ≠ "perguntar várias vezes")
- **Depth por camadas** — livro simples → skill simples; livro complexo (10+ frameworks) → skill com references + capítulos on-demand
- **Pacote Python `book_to_skill`** — CLI + parsers por formato + sanitização
- **Agent-neutral**: `allowed-tools` omitido de propósito para ser portável entre hosts

## 3. Helenização

- Instalado: `~/.opencode/skills/book-to-skill/` (SKILL.md + `scripts/book_to_skill/` com 16 módulos Python: cli, config, dependencies, exceptions, sanitize, utils + parsers/{pdf,epub,docx,html,rtf,text,calibre})
- Invocação: `python3 -m book_to_skill` (dentro do dir do skill)
- Papel no Gran-Mestre: pipeline de estudo — livro → skill helenizável (sinergia com a coleção `textos-biblioteca-*` já absorvida)

## 4. Aprendizado

Esta skill é o "fabricante de skills" da autofagia: qualquer fonte textual vira skill canônica. Aproveitar para produzir novas skills a partir da biblioteca de textos do Obsidian (`cerebro com IA/`).
