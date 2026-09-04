---
tipo: aprendizado
data: 2026-08-28
autor: Gran-Mestre
pipeline: hefesto
tema: captura contexto bruto pre-LLM
---

# Hooks NÃO capturam contexto via session.start — correção talâmica real

## Causa raiz (CONFIRMED)
- `session.start` (hook shell) NÃO expõe `messages`/`prompt` — os hooks Python
  `kronjob-talamus-filter.py` e `sdd-talamus-filter.py` registrados ali capturavam NADA
  (apenas estado de sessão vazio). Evidência: API plugin 1.18.23 (index.d.ts) — o único
  gancho que recebe mensagens pré-LLM é o plugin `experimental.chat.messages.transform`.
- `opencode.jsonc` sem chave `plugin` → diretório `plugins/` é órfão; apenas `plugin/`
  é auto-load (tracer.js prova viva).

## Correção (helenização)
- `plugin/talamus-preflight.ts`: plugin nativo com `experimental.chat.messages.transform`
  → loga JSONL em `state/watcher/talamus-preflight.jsonl` (ts, sessionID, nº msgs,
  tokens estimados, roles, intent, ação), fail-open, conservador; condensação real
  apenas com `TALAMUS_CONDENSE=1`.
- Fix adicional: `IndentationError` pré-existente em `kronjob-talamus-filter.py:179`
  (edição R71 quebrada) — hook NÃO compilava.
- Testes: 6/6 passed (test_talamus_preflight.py) + smoke `--preflight` real.

## Lição (R43/R44)
- Captura pré-LLM = plugin `experimental.chat.messages.transform`, NUNCA session.start.
- Auto-load = pasta `plugin/`; `plugins/` exige registro manual.
- Bug latente: API transform usa `{info:{role}}` aninhado — mesmo defeito no context-bm25.ts.
