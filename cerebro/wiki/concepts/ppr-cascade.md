---
tags: [concept, retrieval, graph, ppr, cascade]
related: [[entities/gran-mestre]] [[concepts/delegacao-dinamica]] [[concepts/dev-loop]]
last_updated: 2026-07-29
---
# PPR Cascade — Recuperação Neural em 5 Estágios

## Definição
Cascade de recuperação baseada em **Personalized PageRank (Haveliwala 2002)** sobre o grafo de `[[wikilinks]]`. Trunca no primeiro estágio que retorna sinal suficiente — sem custo fixo.

## Os 5 Estágios

### 1. Lex Fast Path
Casamento direto de tokens contra títulos e aliases.
- **Custo:** Grátis, instantâneo
- **Gatilho:** Match exato de nome

### 2. LLM Keyword Generation
LLM propõe 8–12 palavras-chave multilíngue.
- **Custo:** 1 chamada LLM pequena
- **Cobre:** Sinônimos, abreviações, variantes

### 3. Local Substring Scan
Cada keyword é rematchada localmente contra títulos, aliases e trechos.
- **Custo:** Zero chamada LLM
- **Cobre:** Noise-tolerant recall

### 4. LLM KB Fallback
Quando lex + keyword scan retornam fracos, LLM re-semeia top-N candidatos.
- **Custo:** 1 chamada LLM
- **Cobre:** Casos ambíguos

### 5. PPR Graph Expansion
Personalized PageRank sobre o grafo de `[[wikilinks]]` partindo do seed set.

**Implementação:** 3.000 walks aleatórias × 50 passos, regra de dead-end.
**Custo:** O(K × L) independente do número de páginas.
**Resultado:** Contexto multi-hop: "Bill Gates" → "Microsoft" → "competidores".

## Por Que Sem Embeddings
O grafo de `[[wikilinks]]` já contém relações curadas manualmente. Embeddings:
- Fragmentam o conhecimento em chunks
- Perdem a semântica relacional
- Exigem modelo de embedding por provider

**Cada `[[link]]` é uma sinapse — não precisa de vetor.**

## Implementação no Gran-Mestre
```
- Estágio 1: grep direto nos títulos
- Estágio 2: memory-keeper sugere keywords
- Estágio 3: substring match local
- Estágio 4: LLM fallback (oracle)
- Estágio 5: expansão por [[links]] no grafo neural
```

## Sinapses
- [[entities/gran-mestre]] — orquestrador
- [[entities/memory-keeper]] — consciência que ativa a cascade
- [[concepts/delegacao-dinamica]] — recuperação dinâmica

---
*Neurônio criado em: 2026-07-29*
