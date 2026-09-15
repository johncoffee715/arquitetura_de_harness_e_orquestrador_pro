---
tags: [concept, snn, conectoma, drosophila, dopamina]
related: [[concepts/snn/snn-conectoma-malecns-indice]] [[concepts/snn/snn-mb-corpos-cogumelo]]
last_updated: 2026-09-13
source: male-cns-v1.0
---

# PPL101 — Cluster Dopaminérgico (Protocerebral Posterior Lateral)

## Definição
PPL = neurônios dopaminérgicos protocerebrais posteriores-laterais. O identificador
"PPL101" refere-se a um cluster de células dopaminérgicas no conectoma Drosophila.
Neurônios dopaminérgicos fornecem o sinal de valência (punição/recompensa) que modula
a plasticidade em regiões como os Corpos Cogumelo (via cAMP/rutabaga).

## Papel funcional

- Modulação dopaminérgica: valência aversiva (dopamina) vs apetitiva (octopamina).
- No MB: dopamina ativa PKA seletivamente no lobo vertical (α); octopamina em todos os lobos.
- Recorrência alta: neurônios dopaminérgicos estão entre os tipos com mais conexões
  recorrentes (57% no cérebro larval — referência análoga, Winding 2023).

## Invariante p/ event-loop SNN

- **Sinal de valência** como canal modulador global, separado do fluxo sensorial.
- Feedback recorrente dopaminérgico → loop de recompensa (RL-like).

## Fontes
- Manifesto do usuário (Alura MaleCNS 166k/125M — PPL101 como cluster alvo).
- https://en.wikipedia.org/wiki/Mushroom_body (dopamina/PKA/octopamina)
- https://en.wikipedia.org/wiki/Drosophila_connectome (Winding 2023 — recorrência dopaminérgica)

## Classificação de evidência
- "PPL101" como ID específico de cluster no MaleCNS: HIGH_CONFIDENCE (manifesto usuário),
  NÃO confirmado por fonte primária aberta nesta task.
- Papel dopaminérgico no MB (PKA/cAMP): CONFIRMED (literatura).
- Contagem exata de células PPL101: UNKNOWN — NÃO inventar.

## Estado vivo (motor SNN 2026-09-14)
Ver [[concepts/snn/snn-motor-indice]] — esta região entra no loop como reforço dopamina:
sinal de valência como canal modulador de referência para o ciclo decisão→snapshot do `live_loop.py`.