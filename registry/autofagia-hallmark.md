# Autofagia: Hallmark

**Data:** 2026-08-03 (Rodada 8 — 26 alvos)
**Fonte:** https://github.com/nutlope/hallmark (21k★, MIT)
**Objetivo:** Absorver skill de design **anti-AI-slop** — regras opinativas para UIs parecerem "feitas, não geradas"

---

## 1. O que é

Hallmark é uma skill de design para assistentes de IA (compatível Claude Code / Cursor / Codex). Não é "mais um tema": insiste em **variedade estrutural** (dois briefs diferentes não devem compartilhar o mesmo ritmo hero→3-features→CTA→footer), com catálogo de 20 temas nomeados, modo custom (paleta OKLCH + fontes livres), e 3 verbs: `audit`, `redesign`, `study` (extração de DNA de design de URL/screenshot → `design.md` portátil).

## 2. Padrões absorvidos

- **Verbs explícitos** (audit/redesign/study) + fluxo default de design → disparo por intenção
- **6 disciplinas** transversais a todo verb (anti-slop test, estrutura, cor, tipo, espaço)
- **Safety rail de implementação** — nunca apagar rotas/componentes sem aprovação explícita; declarar arquivos antes de editar
- **`design.md` portátil** — DNA de design exportável entre projetos (com camada de recusa para não copiar pixels alheios)

## 3. Helenização

- Instalado: `~/.opencode/skills/hallmark/` (SKILL.md + recipes.md + references/{structure,anti-patterns,color,component-cookbook,custom-theme,study,typography}.md)
- Papel no Gran-Mestre: skill de design/UI (faz par com browser-use e archify)
- Pós-instalação: hook auto via `helenize_deploy.py` (padrão dos demais helenizados)

## 4. Aprendizado

O padrão "anti-slop test" e a variedade estrutural são validáveis na prática com os testes do próprio repo (`site/_tests/*/brief.md`). Reaplicar o conceito nas próximas skills de design (ex.: cross-over com impeccable design language).
