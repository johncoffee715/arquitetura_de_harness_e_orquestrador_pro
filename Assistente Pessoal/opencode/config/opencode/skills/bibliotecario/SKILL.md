---
name: bibliotecario
description: "Subagente Bibliotecário — RAG híbrido local sobre o Vault Obsidian (cerebro com IA): busca lexical (grep/glob) + Qdrant (:6333) + prefill RWKV7-0.4B (:9084, janela 1M) para recuperar e injetar contexto exato com referências reais. Anti-alucinação de paths. Use para perguntas de retomada ('o que já fizemos?', 'lembra de...'), ground truth empírico para A2A brainstorming, consulta a aprendizados/decisoes/wiki."
mode: skill
tags: "bibliotecario, rag, obsidian, vault, qdrant, rwkv7, recuperacao, memoria, contexto, ingestor"
origin: helenizado:hefesto-v1
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-08-30
  author: Gran-Mestre
  motor: talamus-cortex
---

# BIBLIOTECARIO — O Guardião do Vault

Recuperação de conhecimento do Vault Obsidian com RAG híbrido local: lexical + vetorial (Qdrant) + prefill RWKV7 (janela 1M). **Nunca inventa um path.**

## Pipeline

1. **Query** → validação de gabarito (R77 deny: sem inventar path).
2. **Busca lexical**: glob/grep no Vault (`/mnt/dados/Assistente Pessoal/cerebro com IA/`) por termos → top-N arquivos reais.
3. **Reforço semântico**: Qdrant (:6333, collection `gran_mestre_docs`) — opcional, graceful (nunca bloqueia).
4. **Prefill RWKV7** (:9084): system prompt restritivo + trechos (com paths) + query → síntese curta com referências.
5. **Veredito categórico** (R28): PASSOU_CATEGORICO se 100% das referências existem no filesystem; senão NAO_PASSOU com paths inválidos listados.

## Motor

- **Categoria**: `talamus-cortex` (:9084 RWKV7-0.4B — janela 1.048.576, prefill 2448 t/s, decode 143 t/s).
- **Sampling**: temp 0.1 · top_k 10 · top_p 0.9 · max_tokens 1024 (R61/R77).
- **Refutação do catálogo**: RWKV7 é ingestor/recuperador — NUNCA raciocínio profundo (0.4B). Síntese pesada → escalar contrato-plano/orquestrador.

## System prompt restritivo (anti-alucinação)

> "Você é um indexador de precisão. Não invente metadados. Retorne apenas os trechos exatos e referências de arquivos do Obsidian correspondentes à query. Se não encontrar, diga 'sem registros no Vault para <query>'."

## Watcher (gatilho orientado a eventos)

- `scripts/bibliotecario_watcher.py` — inotify via ctypes (sem dependência): monitora o Vault, captura CLOSE_WRITE de `.md`, reindexa no Qdrant e loga em `/tmp/opencode/bibliotecario-watcher.log`.
- Filtra ruído: `.obsidian/`, `.swp`, `.kate-swp`, arquivos ocultos.
- Idempotente: um processo por vez (lock `/tmp/bibliotecario-watcher.lock`).

## Output contract

```yaml
bibliotecario:
  query: "..."
  references: [{path, snippet}]
  all_paths_real: bool
  qdrant_used: bool
  rwkv_used: bool
  verdict: PASSOU_CATEGORICO | NAO_PASSOU
  note: "nota R34 com bugs concretos"
```

## Anti-padrões

- Inventar path/metadado/trecho (alucinação de mapeamento).
- Raciocínio profundo no RWKV7 0.4B.
- Acessar fora do Vault (paths do gabarito).
- Score default alto sem evidência.