---
numero: VAULT
tema: Regras do vault Obsidian
categoria: config
setor: memoria
escopo: modulo
vigencia: 2026-08-18
---

# Cérebro com IA — Schema de Conhecimento

## Diretrizes Gerais

Este cofre é um **LLM Wiki** — um cérebro persistente gerenciado por agentes de IA.

- **Raw sources** (`/mnt/dados/cerebro com IA/raw/`) = entrada imutável
- **Wiki** (`/mnt/dados/cerebro com IA/wiki/`) = síntese mantida por IA
- **Schema** (este arquivo) = convenções e workflows

## Workflows Obrigatórios

### Ingestão
Quando uma nova fonte chega:
1. Ler o conteúdo com atenção
2. Discutir principais takeaways com o usuário
3. Criar `wiki/summaries/{slug}.md` com resumo
4. Atualizar `wiki/index.md` (catálogo)
5. Criar/atualizar páginas em `wiki/concepts/` e `wiki/entities/`
6. Append em `wiki/log.md` com formato: `## [DATA] ingest | {fonte}`

### Consulta
Quando perguntarem algo:
1. Ler `wiki/index.md` primeiro
2. Ler páginas relevantes
3. Síntese com citações de páginas wiki
4. Arquivar resposta em `wiki/answers/{slug}.md` se útil

### Lint
Periodicamente (semanalmente):
1. Verificar contradições entre páginas
2. Identificar páginas órfãs (grafico do Obsidian ajuda)
3. Flagar gaps de conhecimento
4. Sugerir novas fontes/perguntas

## Convenções de Nome

- Slugs: lowercase, hífens, max 50 chars
- Data formato: `YYYY-MM-DD`
- Tags YAML: `tags: [source/video, domain/ai, status/pending]`

## Estrutura de Páginas

### Summaries
```yaml
---
source: {identificador da fonte}
date: YYYY-MM-DD
type: video/article/podcast
tags: [domain/sigla]
---
# {Título}

## Principais Takeaways
- ...

## Conceitos Extraídos
- ...

## Entidades Mencionadas
- ...
```

### Concepts
```yaml
---
tags: [concept]
related: [[outro-conceito]]
last_updated: YYYY-MM-DD
---
# {Nome do Conceito}

## Definição
...

## Fontes
- [[summaries/fonte1]]
- [[summaries/fonte2]]

## Aplicações
...
```

### Entities
```yaml
---
tags: [entity/agent|framework|projeto]
domain: ai|hardware|software
status: active|archived
---
# {Nome da Entidade}

## Tipo
Agente/Software/Framework

## Descrição
...

## Relacionamentos
- [[conceito-relevante]]

## Sessões Relevantes
- ...
```

## Integração OpenCode

Esta skill é consumida por:
- `/gran-mestre` — passa a ter contexto persistente
- `CONTEXT.md` — archive em `wiki/sessions/`

---
*Maintido por Gran-Mestre v5.0 — Sistema de Inteligência Compartilhada*