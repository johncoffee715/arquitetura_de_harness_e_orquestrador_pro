---
tags: [entity, framework]
domain: ai
status: active
source: https://github.com/lfnovo/open-notebook
---
# Open Notebook

## Tipo
Framework de knowledge base com LLM Wiki

## Descrição
Sistema de conhecimento persistente que combina:
- SurrealDB (banco de dados)
- LangChain (orquestração)
- MCP (interface)
- Web UI (Obsidian-like)

## Componentes Devorados

### Notebook/Source/Note Hierarchy
- **Raw sources** — fontes imutáveis
- **Notebook** — container de trabalho
- **Source** — documento fonte
- **Note** — anotações geradas

### Dual Search
- Full-text search (BM25)
- Vetorial (embeddings)

### MCP Interface
- Porta 5055 para integração com agentes
- Busca de notas/contexto

## Sinapses
- [[concepts/antropofagia-tecnologica]] — fonte devorada (hierarquia Notebook/Source/Note)
- [[concepts/delegacao-dinamica]] — MCP interface → delegação por tags
- [[concepts/ppr-cascade]] — dual search (BM25 + vetorial) → cascade retrieval
- [[decisoes/2026-07-29-otimizacao-neural-obsidian]] — otimizações neurais
- [[decisoes/2026-07-25-gran-mestre-v7-obsidian]] — cérebro neural
- [[entities/gran-mestre]] — orquestrador que absorveu os padrões

## Status
- ✅ Clonado: `/home/johncoffee/open-notebook/`
- ✅ Configurado: `.env` com encryption key
- ⏳ Docker: precisa start manual
- ✅ Sinapses: 6 links bidirecionais estabelecidos

## Integração OpenCode
- MCP em `~/.config/opencode/opencode.json`
- Skill: `cerebral-wikia`