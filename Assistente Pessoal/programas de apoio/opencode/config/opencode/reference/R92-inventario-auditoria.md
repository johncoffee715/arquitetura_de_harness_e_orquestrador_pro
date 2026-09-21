# R92 — Guardrail Universal de Inventário para Auditoria (promulgada 2026-09-07)

> Status: FORJADA (ordem do usuário) · incorporação no AGENTS.md pendente
> (AGENTS.md bloqueado p/ escrita nesta sessão). Vale desde o registro no decision-log.

## Regra

Todo inventário de LLMs requisitado pelo usuário para auditoria DEVE vir em tabela
legível com TODAS as colunas: slot · LLM (model_id) · pesos GB · ctx operacional ·
KV/tok → KV@ctx · t/s CPU · t/s GPU · RAM/VRAM (por slot + total com guarda explícita).

- Dado ausente = escreve `a medir`, NUNCA célula vazia ou número inventado.
- Fonte: manifesto_llm.json + medições locais frescas (empírico local prevalece — R45).
- VRAM por slot = delta medido em move (restart) ou `~estimado`; declarar qual.
- Guarda mínima de produção: ≥1GB livre (violar = NAO_PASSOU automático).

## Formato canônico

| Slot · Modelo | Pesos | Ctx | KV/tok → KV@ctx | t/s CPU | t/s GPU | VRAM |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |
| **TOTAL** | **soma pesos** | — | — | — | — | **usada/total (guarda X)** |

## Protocolo `a medir` (update 2026-09-07)

- Token literal obrigatório: **`a medir`** (minúsculo, com crase em doc / sem crase em célula).
- Todo `a medir` carrega entre parênteses o que falta: `a medir (KV exato)`,
  `a medir (solo ≥32tok)`, `a medir (delta em move)`.
- Prazo: nenhum `a medir` atravessa 2 sessões sem ser resolvido ou re-justificado
  no decision-log. Carregar em silêncio = NAO_PASSOU na próxima auditoria.
- Resolução vira número + fonte (`medido <data> <método>`); palpite continua proibido.
