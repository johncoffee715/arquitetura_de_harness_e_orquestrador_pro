---
name: memory-local
description: >-
  Memória persistente de longo prazo 100% local para agentes, baseada na
  arquitetura do mem0 (Apache-2.0) helenizada para o harness: extração de
  memórias em ADD/UPDATE/DELETE/NOOP, embeddings locais via llama.cpp, storage
  vetorial local (Chroma/Qdrant) e integração com o vault Obsidian. Use quando
  precisar de memória entre sessões, recall de fatos/usuário/projeto, ou
  persistência de conhecimento sem nuvem.
---
# Memory Local (helenizada do mem0)

## Origem (antropofagia)
- **mem0** (v2.0.7, Apache-2.0) — camada de memória para agentes LLM. Essência
  extraída: pipeline de extração/atualização de memórias por classificação
  LLM (ADD/UPDATE/DELETE/NOOP), histórico de memória, storage vetorial
  pluggável. NÃO copiamos a implementação — refatoramos para o stack local.

## Pipeline de memória (núcleo helenizado)

### 1. Extração (a cada interação relevante)
Prompt ao modelo local (LLM Orquestrador/qwen via :8083-8087):
```
Analise a conversa. Retorne NOOP se nada relevante para memorizar.
Senão, retorne uma lista JSON de memórias, cada uma com:
- fact: <fato declarativo, 1a pessoa quando for sobre o usuário>
- type: <ADD | UPDATE | DELETE>
- target: <user | project | agent>
- scope: <global | per-conversa>
```

### 2. Atualização
- **ADD** → novo registro com timestamp.
- **UPDATE** → substitua a memória anterior relacionada (mesma entidade/fato),
  mantendo histórico (campo `history: []`).
- **DELETE** → marca removida (soft-delete) — nunca apaga fisicamente.
- **NOOP** → descarta.

### 3. Storage (local-first)
- **Embeddings locais**: via llama.cpp (endpoint /embedding do llama-server)
  ou fallback hashing lexical — NUNCA depender de API externa.
- **Vetorial**: SQLite + FTS5 (leve) ou Chroma/Qdrant se disponível.
  Schema mínimo: `memory(fact, type, target, scope, ts, history, vector)`.
- **Arquivo**: espelhar em Markdown no vault Obsidian
  (`cerebro com IA/wiki/summaries/memories/`) para leitura humana.

### 4. Recall (injeção contextual)
- Antes de tarefa nova: buscar memórias por similaridade (embedding) +
  filtro `target` → injetar top-3 no contexto como bloco `[MEMORY]`.
- Respeitar janela: cada memória ≤ 1 linha; bloco ≤ 200 tokens.

## Integração com o harness
- **Camada 2 do cérebro**: Obsidian (arquivos) = camada 1; este skill = camada
  vetorial consultável. Memory-keeper agente usa ambos.
- **Gatilho de uso**: início de sessão, início de task, mudança de contexto.
- **Higiene**: `DELETE` em soft-delete; TTL configurável por `scope`.

## Anti-padrões
- NUNCA memorizar segredos/tokens/credenciais (regra global §6).
- NUNCA injetar memórias irrelevantes ao contexto atual (polui a janela).
- NUNCA depender de API de embeddings externa — sempre local.

(End of file - total 61 lines)