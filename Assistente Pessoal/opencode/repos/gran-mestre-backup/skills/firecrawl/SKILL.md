---
name: firecrawl
description: "A context API to search, scrape, and interact with the web at scale — absorvido criticamente de firecrawl/firecrawl (161k★ AGPL-3.0). Scrape de páginas JS-heavy → Markdown limpo, search de fontes, extração estruturada e turnos de interação para agentes (deep research, RAG, data extraction)."
user-invocable: true
allowed-tools: "Read Write Bash WebFetch WebSearch"
metadata:
  version: "1.0.0"
  origin: "https://github.com/firecrawl/firecrawl (AGPL-3.0)"
  absorbed_at: "2026-08-05"
  antropofagia: "Devorada a API de contexto web (search/scrape/interact) e adaptada para o harness OpenCode: firecrawl vira camada de ingestão web do Gran-Mestre, complementando agent-reach (plataformas) e browser-use (navegador real)."
---

# 🔥 firecrawl — Skill de Ingestão Web em Escala para OpenCode

## Origem (Antropofagia Tecnológica)

Esta skill é o resultado da **antropofagia tecnológica** do repositório
[`firecrawl/firecrawl`](https://github.com/firecrawl/firecrawl) (161.720★, AGPL-3.0):

| Componente Original | O que absorvemos | Como adaptamos |
|--------------------|-----------------|----------------|
| Web Context API | Search + scrape + crawl unificados | Skill de ingestão para o Gran-Mestre |
| `scrape` | JS-heavy pages → clean Markdown | Fluxo de contexto: pages → markdown → LLM |
| `search` | Encontrar fontes na web | Complementa agent-reach / WebSearch |
| `extract` | Dados estruturados (schema JSON) | Data extraction para pipelines |
| `crawl` | Múltiplas páginas em lote | Ingestão massiva p/ research profundo |
| LLM-ready output | Saída limpa e estruturada | Sem proxy, sem HTML bruto |

> "Não copiamos. Devoramos, digerimos e transformamos em algo nosso."

## O Que Esta Skill Faz

Permite que o OpenCode **ingira a web em escala** para qualquer tarefa de pesquisa,
extração de dados ou monitoramento:

- 🌐 **Scrape** — pegar uma URL e devolver conteúdo limpo (markdown)
- 🔎 **Search** — encontrar fontes por consulta de texto
- 🧬 **Extract** — extrair dados estruturados com schemas (JSON)
- 🕸️ **Crawl** — varrer um site inteiro em lote
- 🧠 **Deep Research ready** — entrada direta para o Gran-Mestre/agentes

## Arquitetura (Antropofágica)

```
firecrawl skill (OpenCode)
│
├── SKILL.md              ← Este arquivo (diretrizes + playbook)
│
└── Rotas de uso (escolha conforme a task, não como fontes)
    ├── Home stage (R1/R2): → agent-reach p/ plataformas sociais
    ├── Ingest web (R3/R4): → firecrawl API → markdown → context
    ├── QA de conteúdo: → extraction estruturada de site alvo
    └── Cliente: websearch (mínimo ou ausência de chave)
```

## Pré-requisitos

Você precisa de UMA das opções:

### Opção A — Firecrawl Cloud (recomendada, sem infra)

```bash
# Obtenha chave em https://firecrawl.dev
export FIRECRAWL_API_KEY="fc-..."
```

Uso direto via curl:

```bash
# scrape simples
curl -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://docs.sentry.dev", "formats": ["markdown"]}'
```

### Opção B: Servidor Firecrawl MCP (para integração com agente)

```json
// adicionar ao opencode.json mcpServers
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"]
    }
  }
}
```

## Playbook de Uso

### 1. Scrape (página única → markdown)

```bash
curl -s -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://exemplo.com", "formats": ["markdown"], "onlyMainContent": true}'
```

### 2. Search (achar fontes)

```bash
curl -s -X POST "https://api.firecrawl.dev/v1/search" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "langgraph state machine best practices", "limit": 5}'
```

### 3. Extract (dados estruturados com schema)

```bash
curl -s -X POST "https://api.firecrawl.dev/v1/extract" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://exemplo.com/produtos"], "prompt": "Extraia nome e preço de cada produto"}'
```

### 4. Crawl (site inteiro → lote de markdown)

```bash
curl -s -X POST "https://api.firecrawl.dev/v1/crawl" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://docs.exemplo.com", "maxDepth": 2, "limit": 10}'
```

> **Dica**: sempre use `onlyMainContent: true` quando quiser só o conteúdo (corta navbar/rodapé).

## Integração com o Harness

- **Gran-Mestre / Prometheus**: em F1 (DESCOBERTA), use firecrawl search/extract para coletar
  contexto de documentação e fontes — o output markdown entra direto na análise de demanda.
- **Pesquisa/Ingest**: em tarefas de research (agent de pesquisa), firecrawl supre o fluxo
  "URL → markdown → síntese" — especialmente para sites com JS pesado que WebFetch não renderiza.
- **Sem chave disponível**: degrade para `WebSearch` + `webfetch` (queda funcional, não bloqueio).

## Limitações & Avisos

- **AGPL-3.0**: a skill é documentação de uso; não incorporamos código-fonte do projeto.
  Se for auto/self-host das libs internas, revisar compliance AGPL.
- **Custo/Vinculado a nuvem**: o serviço hosted é SaaS pago; sem chave pode haver rate-limit.
- **JS-heavy**: é exatamente onde firecrawl brilha (rendering de páginas SPA) — priorize aqui
  em vez de webfetch puro.
- **Não substitui agent-reach** para plataformas sociais fechadas (小红书, LinkedIn, logs de app).