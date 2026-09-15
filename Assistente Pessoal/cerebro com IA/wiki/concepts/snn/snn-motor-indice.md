---
tags: [concept, snn, motor]
related: ["[[concepts/snn/snn-conectoma-malecns-indice]]", "[[concepts/snn/snn-mb-corpos-cogumelo]]", "[[concepts/snn/snn-cx-complexo-central]]", "[[concepts/snn/snn-ppl101-dopamina]]"]
last_updated: 2026-09-14
source: male-cns-v1.0
---

# SNN Motor — Índice Vivo (live_loop)

## Propósito
Índice motor que liga as 4 notas de macro-região ao loop vivo
(`snn/live_loop.py`). Não duplica anatomia — só mapeia módulo→região.

## Mapa módulo→região

| Módulo | Região / papel |
|---|---|
| `snn/feather_to_csr.py` | topologia MaleCNS real 1.05GB sha256 e35da783 |
| `snn/live_loop.py` | ciclo sensório→decisão RWKV7 (bibliotecário-autônomo, AUTONOMIA TOTAL)→Needle 2 (assistente que executa)→Embedding (secretário que registra/vetoriza) |
| `snn/data/live_state.json` | memória sináptica durável |

## Ciclo
Evento de vault (.md novo/editado) estimula a slice CSR → resumo de
atividade (top-k + contagem por região) vira prompt compacto p/ decisão
RWKV7 → intenção registrada p/ Needle → snapshot em `live_state.json`.

## Regiões ligadas
- [[concepts/snn/snn-conectoma-malecns-indice]] — topologia
- [[concepts/snn/snn-mb-corpos-cogumelo]] — KC/memória
- [[concepts/snn/snn-cx-complexo-central]] — navegação/decisão
- [[concepts/snn/snn-ppl101-dopamina]] — reforço dopamina

## Classificação de evidência
- Módulos e ciclo: CONFIRMED (código em `snn/`).
- Pesos/região por neurônio no loop: UNKNOWN — não declarar métricas aqui.
