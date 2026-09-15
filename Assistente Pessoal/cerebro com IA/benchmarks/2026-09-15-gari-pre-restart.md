# Benchmarks — gari pré-restart 2026-09-15 (run e6f5a7b5)

Fonte: P1-full 12/12 (crivo-chat-slots + crivo-emb-needle) + needle-sync 2026-09-15.

## Quantitativas
- Chat vivos: 8/8 (8083 · 9088 · 9090 · 9092 · 9093 · 9095 · 9084 · 9086)
- Emb: :9094 CPU + :9097 GPU, dim 1024 verificada — 14.7k/91k
- Needle: :8097 graph-tools 160.1 tps · :9091 forja-tools 146.6 tps — 140/154
- Topo: 9088 4.0 (C +0.8) · 9092 3.5 · 9090 3.5 · 9093 1.0 (regressão −1.0)

## Qualitativas (R28)
- P2 blocked honesto (R9): sem bypass, sem retry cego
- 8083 INTOCÁVEL (gargalo); coder só supervisionado+grammar
- 9086 thinking-burn: cura = G4 futuro, nunca mid-pipeline
