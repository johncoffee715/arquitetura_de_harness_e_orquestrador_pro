---
name: context-selector
description: "Context engineering layer: seleciona tools/skills por turno via BM25 + disclosure progressivo — corta tokens e recupera acurácia perdida por tool-overload (sem vector DB). (absorvido de ratel-ai/ratel)"
---
# Context Selector

Helenizado de [`ratel-ai/ratel`](https://github.com/ratel-ai/ratel).

## Propósito
Camada de context engineering: indexa tools/skills num catalogo pesquisavel e injeta por turno so o que o modelo precisa — corta tokens pagos por chamada e recupera acurácia perdida por tool-overload.

## Padrões absorvidos (núcleo canônico do repo)
- searchable_text: indexar so tokens semanticos (nome, descricao, valores enum) — pular type/required/braces/aspas via projecao deterministica (serde preserve_order)
- BM25 como ranker default (model-free, nunca falha), k1=0.9 b=0.4 (descricoes curtas); semantic/hybrid opt-in com RRF
- replace-vs-suggest: interceptar a lista de tools antes do modelo e substituir por top-K (replace default = economia direta e atribuivel)
- Skills first-class {id,name,description,tags,tools,metadata,body}: tags indexadas, skills nunca esfomeadas por tool-matches; gateway e o unico loader (host nao auto-scaneia)
- search_capabilities(query, topKTools, topKSkills) -> buckets independentes + invoke_tool + get_skill_content: disclosure progressivo por turno
- Adaptive usage ranking: par impression/click dos traces do proprio uso (busca x tool invocada) vira relevancia confirmada pelo usuario (ADR-0014)

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="context-selector")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/ratel-ai/ratel
