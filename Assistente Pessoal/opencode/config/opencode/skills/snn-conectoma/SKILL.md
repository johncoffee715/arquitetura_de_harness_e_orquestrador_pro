---
name: snn-conectoma
description: "Recurso nativo do harness para simulação SNN user-space do conectoma Drosophila MaleCNS v1.0 (166K neurônios, 312M sinapses). Contém (a) spec do parser CSR (Compressed Sparse Row) para o grafo de adjacência do conectoma, (b) esqueleto do event-loop SNN (Min-Heap O(log n) / Timing Wheel), (c) HMI de macro-regiões (MB/CX/PPL101). Use ao trabalhar com SNN, conectoma, simulação de spikes ou parsing de grafos esparsos de grande volume."
mode: skill
tags: "snn, conectoma, drosophila, csr, event-loop, spike, spiking-neural-network, malecns"
origin: helenizado:male-cns-v1.0
metadata:
  category: feature
  version: 1.0.0
  date: 2026-09-13
  author: Hefesto (dispatcher snn-hefesto-absorb)
  motor: contrato-plano
---

# SNN-CONECTOMA — Simulação SNN user-space do MaleCNS

Recurso nativo helenizado do conectoma *Drosophila* MaleCNS v1.0. NÃO é o conectoma em si
(não copia dados proprietários) — é o **conjunto de ferramentas** para consumir/processar
um dump de adjacência e executar um event-loop de spikes.

## Arquitetura (3 camadas)

```text
[dump adjacência 166K×166K, 312M sinapses]
        │  (1) PARSER CSR
        ▼
[CSR: row_ptr[], col_idx[], weight[]]
        │  (2) EVENT-LOOP SNN
        ▼
[spikes por timestep → pooling → macro-regiões HMI]
```

## Restrições duras (do packet)

- **user-space only** — zero alteração de kernel CachyOS.
- **Rust ou C++ zero-cost** — sem GC, sem alocação por spike.
- **Min-Heap O(log n) ou Timing Wheel** para agendamento de spikes.
- Threads SNN pinadas em slots CPU: **9086 / 9090 / 9092** (validado via /proc cmdline:
  `-ngl 0` = CPU puro). Não usar 9088 (GPU ngl999) nem 9084 (GPU ngl999).
- Device-map validado nesta task (ver `docs/device-map.md`).

## Ver também

- `spec-parser-csr.md` — spec do parser CSR (formato, invariantes, contrato).
- `esqueleto/event_loop.rs` — esqueleto Rust do event-loop SNN.
- Vault HMI: `cerebro com IA/wiki/concepts/snn/` (macro-regiões MB/CX/PPL101).