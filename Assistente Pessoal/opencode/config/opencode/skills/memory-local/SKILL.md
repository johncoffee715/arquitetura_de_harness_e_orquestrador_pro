---
name: memory-local
description: >-
  >- Memória persistente de longo prazo 100% local para agentes, baseada na arquitetura do mem0 (Apache-2.0) helenizada para o harness: extração de memórias em ADD/UPDATE/DELETE/NOOP, embeddings locais via llama.cpp, storage vetorial local (Chroma/Qdrant) e integração com o vault Obsidian. Use quando 
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/memory-local
helenized: true
r84: true
r77_triple: true
---
# memory-local — memória local mem0

Helenizado de [`https://github.com/memory-local`](https://github.com/memory-local) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
>- Memória persistente de longo prazo 100% local para agentes, baseada na arquitetura do mem0 (Apache-2.0) helenizada para o harness: extração de memórias em ADD/UPDATE/DELETE/NOOP, embeddings locais via llama.cpp, storage vetorial local (Chroma/Qdrant) e integração com o vault Obsidian. Use quando 

## Padrões absorvidos
- memória persistente: mem0, ADD/UPDATE/DELETE, vetorial
- Origem: https://github.com/memory-local
- Domínio: memória local mem0

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `memory-local` (tags: mem0, ADD/UPDATE/DELETE).
2. `skill(name="memory-local")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/memory-local
