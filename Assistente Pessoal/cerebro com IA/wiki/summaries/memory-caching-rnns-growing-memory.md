---
source: arxiv-2602.24281
date: 2026-09-16
type: article
tags: [domain/ai, memoria-recorrente, long-context]
---
# Memory Caching: RNNs with Growing Memory (Google Research)

> Paper: Behrouz, Li, Deng, Zhong, Razaviyayn, Mirrokni — arXiv:2602.24281 (27/fev/2026), poster ICML 2026.
> https://arxiv.org/abs/2602.24281

## Principais Takeaways
- RNNs comprimem tudo num hidden state fixo → "amnésia" (overflow) em contexto longo; Transformers lembram (memória cresce com L) mas custam O(L²).
- **Memory Caching (MC):** divide a sequência em N segmentos; ao fim de cada um, o estado de memória final é **cacheado como checkpoint comprimido**; cada token consulta o estado atual **+** os checkpoints passados via agregação: `y_t = Agg(M_atual(q_t); {M_cacheados(q_t)})`.
- Complexidade controlável **O(N·L)** — interpola entre RNN O(L) e Transformer O(L²).
- 4 variantes de agregação (incl. gated aggregation e sparse selective); vale p/ linear attention, deep memory modules e RNNs em geral.
- Em recall in-context: Transformers ainda vencem, mas MC fecha o gap e supera RNNs SOTA.
- Linha de trabalhos-irmãos: Infini-attention (Google 2024, memória compressiva), Compressive Transformer, MARCH (ago/2026, "state anchors" com chave por conteúdo), Log-linear attention (hierarquia logarítmica de estados).

## Conceitos Extraídos
- [[concepts/memory-caching-externo]] — MC como memória externa de engenharia (vault+RAG) vs MC arquitetural
- Checkpoint de segmento como resumo comprimido (↔ `live_state.json`, MOCs)
- Agregação atual+passado (↔ prompt compacto do live_loop, retrieval Qdrant)

## Entidades Mencionadas
- RWKV7 (:9084, córtex recorrente de estado fixo — classe exata que o MC mira)
- Qdrant `bibliotecario_1024` (banco de checkpoints consultável)
