---
name: wigolo
description: Local-first web intelligence over MCP — search/fetch/crawl/extract/research with $0/query, no API keys, evidence with byte-pinned citations.
category: skill
model: local-forge/proposer
---

# wigolo

Camada web local-first para coding agents via MCP: search multi-engine, fetch com
escalada p/ browser, crawl, extract estruturado, cache, find-similar, research com
citações e agent loop autônomo. Helenizado de `knockoutez/wigolo`
(origem: https://github.com/knockoutez/wigolo).

> Irmãs no catálogo: `firecrawl` (cloud, semântico), `browser-use` (automação),
> `mcp-servers` (fetch de referência). Wigolo = o polo **local-first, $0/query**.

## Quando usar

- Pesquisa web recorrente do agente sem conta de API (bursts de queries)
- Fetch com prova (excerpt verbatim + span byte-exato + citation_id)
- Crawl/extract/cache/find-similar/research/agent sem sair da máquina

## Como usar

1. `npx wigolo init` (engine local) · `npx wigolo doctor` (saúde)
2. Via MCP (`npx -y wigolo`), REST (`wigolo serve`, `POST /v1/{tool}`), SDKs TS/Python ou CLI
3. Queries em **array** p/ breadth paralela; `search_depth: deep` no que importar; domínios p/ docs

## Princípio

Degradação honesta: cache stale, engine falha e truncamento sempre rotulados; `blocked_by_challenge` nunca vira conteúdo. LLM só p/ síntese (opt-in, `WIGOLO_LLM_PROVIDER`).
