---
tags: [concept, snn, conectoma, drosophila, mushroom-body]
related: [[concepts/snn/snn-conectoma-malecns-indice]]
last_updated: 2026-09-13
source: male-cns-v1.0
---

# Corpos Cogumelo (Mushroom Bodies — MB)

## Definição
Par de neuropilos do cérebro de insetos (corpora pedunculata) — centro de aprendizado
e memória olfativa associativa. Nome vem do cálice hemisférico (calyx) ligado ao resto do
cérebro por um pedúnculo (peduncle).

## Estrutura (Drosophila)

- **Kenyon cells (KC)**: neurônios intrínsecos do MB (~2.500 em Drosophila).
- **Lobos** (três classes de KC, expressão gênica distinta): α/β, α'/β', γ.
- **Calyx**: recebe input olfativo via projection neurons (PNs) do antennal lobe.
- **MBONs** (mushroom body output neurons): saída — poucos MBONs recebem convergência
  densa de milhares de KCs (fonte de stereotypy de resposta apesar de conexão aleatória).

## Papel funcional

- Aprendizado/memória olfativa (ablação destrói a função).
- Coincidence detector: integra input olfativo (CS) + valência (US, dopamina/octopamina).
- Traços de memória: curta (α'/β'), intermediária, longa (α/β entre 9–24h; γ entre 18–24h).

## Bioquímica da plasticidade (proteína p/ modelo SNN)

- **cAMP** elevado por dopamina (aversiva) ou octopamina (apetitiva) → sinal de valência.
- **rutabaga (rut)** adenylyl cyclase = coincidence detector: sensível a Ca²⁺ (CS) + G-proteína (US).
- **PKA** ativada por cAMP; **dunce (dnc)** PDE restringe especificidade espacial (lobo α).

## Invariante p/ event-loop SNN

- Convergência densa KC → MBON (muitos-para-poucos) = pooling esparso.
- Valência é sinal modulador separado do sinal sensorial (padrão CS/US → aprendizado).
- Plasticidade dependente de coincidência temporal (Ca²⁺ + neuromodulador).

## Fontes
- https://en.wikipedia.org/wiki/Mushroom_body
- https://en.wikipedia.org/wiki/Drosophila_connectome (refs Takemura 2017, Mittal 2020, Caron 2013)

## Classificação de evidência
- Estrutura/lobos/contagem KC: CONFIRMED (Wikipedia + literatura primária).
- Dinâmica exata de receptor no MaleCNS: UNKNOWN (não no grafo de sinapses químicas).

## Estado vivo (motor SNN 2026-09-14)
Ver [[concepts/snn/snn-motor-indice]] — esta região entra no loop como KC/memória:
convergência KC→MBON como referência de pooling para o resumo de atividade do `live_loop.py`.