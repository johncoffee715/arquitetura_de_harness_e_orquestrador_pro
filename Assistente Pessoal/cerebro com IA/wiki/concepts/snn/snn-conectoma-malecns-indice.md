---
tags: [concept, snn, conectoma, drosophila, hmi]
related: [[concepts/snn/snn-mb-corpos-cogumelo]] [[concepts/snn/snn-cx-complexo-central]] [[concepts/snn/snn-ppl101-dopamina]]
last_updated: 2026-09-13
source: male-cns-v1.0
---

# SNN Conectoma Drosophila — MaleCNS v1.0 (HMI Macro-Regiões)

## Propósito
Human-Machine Interface (HMI) em Obsidian para mapear macro-regiões do conectoma do
cérebro de *Drosophila melanogaster* macho (MaleCNS v1.0) como ground-truth estrutural
para um event-loop SNN user-space. NÃO é simulação completa — é mapa de referência.

## Fonte (ground truth, evidência rastreável)

- **MaleCNS v1.0**: conectoma completo do SNC masculino (cérebro + cordão nervoso ventral).
  - **166K neurônios, 312M sinapses** (químicas apenas — sem gap junctions/neuromoduladores).
  - Imagem FIB-SEM + segmentação flood-filling network + proofreading manual.
  - Consórcio: Janelia Research Campus + University of Cambridge + MRC LMB + Google.
  - Preprint: Berg et al. 2025, "Sexual dimorphism in the complete connectome of the
    Drosophila male central nervous system", bioRxiv `10.1101/2025.10.09.680999`.
  - URL referência: https://en.wikipedia.org/wiki/Drosophila_connectome
- **Corpos Cogumelo**: https://en.wikipedia.org/wiki/Mushroom_body
- **Não verificado (conceito, NÃO fato)**: DOOMFLY / Alex Wormuth — marcado UNKNOWN.

## Macro-regiões HMI (clusters)

| Cluster | Nota | Papel funcional |
|---|---|---|
| PPL101 | [[concepts/snn/snn-ppl101-dopamina]] | modulação dopaminérgica (recompensa/punição) |
| Complexo Central (CX) | [[concepts/snn/snn-cx-complexo-central]] | navegação, integração sensorimotora |
| Corpos Cogumelo (MB) | [[concepts/snn/snn-mb-corpos-cogumelo]] | aprendizado/memória olfativa associativa |

## Invariantes estruturais (proteína extraída)

1. **Sinapse poliádica**: 1 T-bar pré-sináptico → múltiplos PSD pós-sinápticos.
   → grafo dirigido multiedge: `(pre → {post_1..n})`, peso = contagem de sinapses.
2. **Conectoma = grafo dirigido**: neurônio = nó, sinapse = aresta ponderada.
3. **Só sinapses químicas** no dataset — neuromodulação e gap junction FORA do grafo.
4. **Dimorfismo sexual** é o foco analítico primário do MaleCNS.

## Limitações (adversarial — NÃO simular além do dado)

- Sem gap junctions, neuromoduladores, hormônios, dinâmica de receptor, glia.
- Uma simulação comportamental completa exigiria esses dados (fora do escopo do event-loop).
- Contagens variam entre indivíduos; pesos de conexão variam dentro/across animais.

## Estado vivo (motor SNN 2026-09-14)
Ver [[concepts/snn/snn-motor-indice]] — esta nota entra no loop como topologia:
`feather_to_csr.py` fornece a slice CSR que o `live_loop.py` estimula a cada episódio.