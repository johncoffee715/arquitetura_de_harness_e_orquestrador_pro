---
name: agentic-awesome-skills
description: >-
  Catálogo selecionado de skills agentic do ecossistema (helenizado de
  agentics-org/agentic-awesome-skills): referência de padrões de skills para
  memória, segurança, pesquisa e automação. Use ao projetar skills novas no
  harness (catálogo primeiro, constrói só o GAP — regra R8), ao buscar padrão
  de skill para um problema específico, ou para autofagia seletiva.
---
# Agentic Awesome Skills (catálogo selecionado)

## Origem (antropofagia)
- **agentics-org/agentic-awesome-skills** (MIT) — lista curada de skills
  agentic para Claude Code/Copilot: memória, segurança, web, automação.
  Selecionamos as essências reutilizáveis e as refatoramos para o harness —
  NUNCA cópia literal.

## Skills selecionadas → helenizações no harness

| Skill-fonte | Essência | Helenização (onde vive) |
|-------------|----------|-------------------------|
| **tree-ring-memory** | Memória persistente por árvore de contexto; recall por relevância; compactação incremental | Fundiu em `memory-local` (mem0) + `context-compaction` + Obsidian |
| **security-bluebook-builder** | Gerar "bluebook" de segurança do projeto (ativos, ameaças, mitigação) | Fundiu em `security-methodology` (checklist + ferramentas) |
| **youtube-full** | Baixar transcrição completa de vídeo (yt-dlp) para análise | Padrão documentado no aprendizado Obsidian (vídeo Mano Devin) |
| **rag-web-search** | RAG sobre resultados de busca web | Coberto por `agent-reach` + `firecrawl` existentes |
| **semantic-memory** | Índice semântico por embeddings para recall | Coberto por `memory-local` (storage vetorial) |

## Padrões de design de skills (lições extraídas)
1. **Skill = SKILL.md com frontmatter parseável** (name + description com
   gatilhos explícitos) — validação por fable-judge/Atena (R14).
2. **Determinístico quando possível** — regras de detecção sem LLM (como
   impeccable: 59 regras), LLM só na síntese.
3. **Catálogo primeiro (R8)** — antes de criar skill, varrer o registry
   (`build_registry` + capability-index) e criar só o GAP.
4. **TDD que passa** — toda helenização entrega exemplo funcional verificado.
5. **Commit atômico + frontmatter** — excelência verificável (R14).

## Fluxo de autofagia seletiva
1. Identificar skill-fonte de interesse.
2. Extrair a **essência** (não a implementação literal).
3. Refatorar para SKILL.md nativo + registrar no arsenal (`registry`).
4. Validar com fable-judge antes do done.
5. Documentar origem no frontmatter (rastreabilidade).

## Anti-padrões
- NUNCA copiar implementação literal de skill externa (antropofagia, não clone).
- NUNCA criar skill que duplica capacidade já existente (catálogo primeiro).
