---
tags: [gran-mestre, decisao, FEATURE]
date: 2026-07-25
pipeline: FEATURE
rota: FEATURE
---

# Decisão: Gran-Mestre v7.0 — Cérebro Cognitivo Obsidian

## Contexto
O Gran-Mestre precisa de um sistema de memória persistente para arquivar decisões, aprendizados e contexto de longo prazo. O Obsidian foi escolhido como cérebro cognitivo.

## Decisão
Usar Obsidian como cérebro cognitivo do Gran-Mestre, com:
- `/decisoes/` — Decisões arquiteturais
- `/aprendizados/` — Lições aprendidas
- `/pipeline/` — Contexto do pipeline

## Rationale
1. **Persistência** — Notas Markdown são persistentes
2. **Busca** — Obsidian tem busca poderosa
3. **Links** — `[[]]` para referenciar notas
4. **Tags** — Para categorização
5. **Cerebral DB** — Para ingestão estruturada

## Implementação
- Criar estrutura de diretórios
- Integrar com pipeline Gran-Mestre
- Arquivar após cada pipeline
- Buscar antes de cada pipeline

## Referências
- [[entities/gran-mestre]] — Pipeline do Gran-Mestre
- [[concepts/antropofagia-tecnologica]] — Metodologia de absorção
- [[GLOBAL_POLICY.md]] — Política global