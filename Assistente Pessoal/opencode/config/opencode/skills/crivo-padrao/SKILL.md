---
name: crivo-padrao
description: Crivo padrão do harness (R83/R84/R97/R98) — bateria 6 métricas via endpoint com template + gramática GBNF + captura prefill/decode/KV. Todo teste de LLM candidato USA esta skill; sem ela o placar não é fidedigno.
version: 1.1.0
tags: [crivo, benchmark, quarteto, R83, R84, R97, R98, metrica]
---

# Crivo-Padrão (quarteto R85)

## Regra
Nenhum placar entra na tabela sem: (1) endpoint com template (chat/completions; /completion cru só com justificativa), (2) schema validado contra `schema-probe.gbnf`, (3) prefill+decode de `timings`, (4) KV KB/tok do header GGUF, (5) placar 0–1 por métrica T1/T2/T4/T6/T8/T10.

## Bateria (7 métricas, R34 0.0000001–100 → normalizada 0–1)
- T1 identidade/contaminação · T2 poison 2+2=5 · T4 trens (17:20/20:00/2h40) · T6 schema JSON exato (grammar!) · T8 temporal · T10 needle-registry (anti-fabricação) · T11 tool-call GBNF (`{"tool":"read_file","args":{"path":"/tmp/opencode/probe.txt"}}` byte-exato, temp 0.0)

## Motor
`crivo-padrao.py --port 9096 --out /tmp/opencode/crivo.jsonl [--raw-fallback]` — roda a bateria, valida T6 e T11 contra gramáticas, anexa prefill/decode/timings brutos. Ver `gabarito.json` (firewall) e `mecanica.md` (R78 por papel, disjuntores R65/R84).

## Tabela enriquecida obrigatória (R98)
pesos GB · quant · ctx testado · KV KB/tok (header, efetivo p/ híbridos!) · KV@ctx GB · prefill med t/s · decode med t/s · placar/6 · veredito multi-perspectiva (regra universal 2026-09-10).
