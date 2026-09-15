---
tags: [concept, snn, conectoma, drosophila, central-complex]
related: [[concepts/snn/snn-conectoma-malecns-indice]]
last_updated: 2026-09-13
source: male-cns-v1.0
---

# Complexo Central (Central Complex — CX)

## Definição
Conjunto de neuropilos na linha média do cérebro do protocerebrum de insetos —
centro de navegação, integração sensorimotora e controle de orientação espacial.

## Sub-estruturas (neuropilos)

| Estrutura | Papel |
|---|---|
| **Fan-shaped body (FB)** | integração de sinais de vento + direção olfativa; navegação em turbulência |
| **Ellipsoid body (EB)** | representação de heading/orientação (compasso interno) |
| **Protocerebral bridge (PB)** | rotação/ângulo — conexão entre hemisférios |
| **Noduli (NO)** | input/relay |

## Papel funcional

- Navegação: escolha de direção combinando fluxo de ar + movimento de pacotes de odor.
- No conectoma: processamento de direção do vento cruza com detecção de direção olfativa
  no fan-shaped body (refs: Mackenzie 2023, Matheson 2022).

## Invariante p/ event-loop SNN

- **Representação em anel/coluna**: EB + FB codificam ângulo de forma topográfica
  (padrão de "heading" — útil como anel de fases dirigido por spikes).
- Integração de múltiplas modalidades sensoriais em uma única representação espacial.

## Fontes
- https://en.wikipedia.org/wiki/Drosophila_connectome (fan-shaped body, EB/PB citados)
- MaleCNS v1.0 (Berg et al. 2025, bioRxiv 10.1101/2025.10.09.680999)

## Classificação de evidência
- Presença/estrutura FB/EB/PB/NO: CONFIRMED (literatura primária via connectome).
- Números exatos de neurônios por sub-estrutura no MaleCNS: UNKNOWN (não extraído aqui).

## Estado vivo (motor SNN 2026-09-14)
Ver [[concepts/snn/snn-motor-indice]] — esta região entra no loop como navegação/decisão:
anel de heading EB/FB como referência espacial para a decisão curta do `live_loop.py`.