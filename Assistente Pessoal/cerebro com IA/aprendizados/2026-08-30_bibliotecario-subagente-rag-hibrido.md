# 2026-08-30 — Subagente Bibliotecário: RAG Híbrido (Obsidian × Qdrant × RWKV7 1M)

## O que foi feito (build real — teste do pipeline Hefesto refatorado)
- **Skill `bibliotecario`** (3 camadas R77): conceito.md (O Bibliotecário) + gabarito.json (firewall allow/deny) + mecanica.md (ignição) + SKILL.md.
- **Subagente `bibliotecario.md`**: model `local-thalamus/ingestor` (RWKV7 :9084), temp 0.1, anti-alucinação de paths.
- **`bibliotecario_rag.py`**: busca lexical (grep/glob) + reforço Qdrant (:6333, collection `gran_mestre_docs`, 768-d Cosine) + prefill RWKV7 :9084 (janela 1M) → resposta com referências reais.
- **`bibliotecario_watcher.py`**: inotify via ctypes (zero dependência) — CLOSE_WRITE de .md → reindexa Qdrant em tempo real (<2s), filtros de ruído (.obsidian/.swp), lock idempotente.

## Evidência real
- TDD: 10/10 novos (suíte total 46/46 verdes).
- Query real "hefesto refatoração skills" → 3 notas reais do Vault, `rwkv_used: true`, 100% paths reais, PASSOU_CATEGORICO.
- Watcher: CLOSE_WRITE detectado → reindex Qdrant → 200 OK (87 diretórios monitorados).

## Lições
1. **Qdrant já existia** (:6333, collection gran_mestre_docs 768-d) — catálogo-primeiro (R8) evitou criar vector DB novo; o GAP era o subagente + scripts.
2. **AnythingLLM não está instalado** — o Bibliotecário substitui o papel de orquestrador RAG com stack local pura (lexical + Qdrant + RWKV7). Se AnythingLLM for instalado depois, o watcher pode apontar para a API dele (:3001).
3. **RWKV7 0.4B**: prefill 2448 t/s ideal para ingestão; decode 143 t/s com repetição em síntese longa — usar para recuperação/extração, nunca raciocínio profundo (refutação R75 confirmada empiricamente).
4. **Embeddings placeholder (768-d zeros)**: Qdrant aceita, mas recall semântico real exige modelo de embedding dedicado (ex.: nomic-embed-text) — próximo upgrade.

## Estado
- Commit: aac0804b0.
- Registrado: opencode.jsonc (skills 12, agents 15).