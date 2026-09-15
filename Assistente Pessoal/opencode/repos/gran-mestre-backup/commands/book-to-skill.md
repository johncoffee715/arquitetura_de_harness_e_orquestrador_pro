# Book-to-Skill

Converte PDFs em skills estruturadas para consulta RAG.

## Script

`/mnt/dados/Assistente Pessoal/scripts/book_to_skill.py`

## Como Funciona

1. Extrai texto do PDF
2. Usa LLM local (qwen2.5-coder:14b) para estruturar em:
   - `SKILL.md` — visão geral + frameworks
   - `cheatsheet.md` — comandos e fórmulas essenciais
   - `glossary.md` — glossário de termos
   - `patterns.md` — padrões e anti-padrões
   - `chapters/` — capítulos detalhados

## Uso

```bash
python3 /mnt/dados/Assistente\ Pessoal/scripts/book_to_skill.py <caminho/do/pdf> [slug]
```

O resultado vai para `$KNOWLEDGE/skills/<slug>/`.

## Listar Skills

```bash
python3 /mnt/dados/Assistente\ Pessoal/scripts/book_to_skill.py --list
```

## Consultar Skill

```bash
python3 /mnt/dados/Assistente\ Pessoal/scripts/book_to_skill.py --ask <slug> "sua pergunta"
```
