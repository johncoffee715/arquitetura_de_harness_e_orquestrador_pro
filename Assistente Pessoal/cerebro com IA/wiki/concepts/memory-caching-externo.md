---
tags: [concept]
related: [[summaries/memory-caching-rnns-growing-memory]]
last_updated: 2026-09-16
---
# Memory Caching Externo (MC fora do forward pass)

## Definição
Aplicar o padrão do paper *Memory Caching* (segmentar → cachear checkpoint comprimido por segmento → agregar atual+passado na decisão) como **engenharia de memória externa** ao redor de um núcleo recorrente de estado fixo — em vez de dentro do forward pass com gradiente. Segmentos = episódios/notas; checkpoints = snapshots + embeddings; agregação = prompt compacto / retrieval top-k.

## Mapa MC (paper) ↔ harness (já rodando)

| MC (Behrouz et al. 2026) | Harness local |
|---|---|
| Núcleo recorrente estado-fixo | RWKV7-0.4B :9084 (córtex) |
| Segmentação em N blocos | Slices CSR `limit_rows`, episódios `DaemonVault`, notas atômicas |
| Checkpoint `M_L(s)` por segmento | `snn/data/live_state.json` + linhas de `daemon_episodes.jsonl` |
| Agregação `Agg(atual; caches)` | `LiveLoop.run`: top-k + regiões → decisão RWKV → write-back `<!-- snn-episode` |
| Recuperação seletiva (sparse) | Qdrant 1024-d + Needle top-k sobre o vault |

## Ruptura honesta (onde a analogia quebra)
MC é **diferenciável** (gradiente flui pelos checkpoints); o nosso é **engenharia** (arquivos+RAG, sem gradiente). Mesmo problema (amnésia de estado fixo), camadas diferentes. Não afirmar equivalência arquitetural.

## Experimento B — MEDIDO 2026-09-16: PARKED com evidência
Protocolo A/B executado (3 probes sobre daemon_episodes.jsonl real, :9084, max_tokens 64):
recallA=recallB=0 em 3/3 — o 0.4B gasta os 64 tok em preâmbulo e nunca emite o fato,
com ou sem checkpoints. tokB>tokA (bloco não comprime o suficiente p/ este modelo).
Veredito: MC-externo via :9084 NÃO validado. Reabrir com modelo maior como leitor
(árbitro :9090) ou pergunta-resposta extrativa em vez de recall generativo.
**Pergunta:** recall do RWKV :9084 sobre contexto longo do vault melhora com checkpoints cacheados (live_state + Qdrant top-k) vs. contexto cru?
**Protocolo:**
1. 3 probe-notes com perguntas cuja resposta exige cruzar ≥3 docs distantes do vault.
2. Condição A (controle): pergunta + docs crus no prompt. Condição B: pergunta + top-k Qdrant + último `live_state` relevante.
3. Métrica: acerto recall (0/1 por pergunta) + tokens de entrada por condição.
**Acceptance:** B vence recall com ≤50% dos tokens de A em 2/3 probes → MC-externo vale a formalização; senão, parked com evidência.

## Fontes
- [[summaries/memory-caching-rnns-growing-memory]]
- `snn/live_loop.py` (`run`/`simulate`), `snn/daemon_vault.py`, `snn/data/live_state.json`

## Aplicações
- Formalizar o loop SNN→vault como cache de segmentos (segment-id, checkpoint schema, política de evicção).
- Guia de notas atômicas/MOCs como "checkpoints comprimidos" (via A — engenharia do vault).
