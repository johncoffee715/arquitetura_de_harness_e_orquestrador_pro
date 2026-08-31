---
name: a2a-brainstorm
description: "Loop A2A (Agent-to-Agent) de brainstorming com tríade fixa na VRAM: Propositor (Qwen3.8-4B :9088) → Refutador (Ternary-8B :9090) → Árbitro (LLMJudge-3B :9085) → Escalação (Ornith-35B :8083). Tensão cognitiva produtiva com regras de engajamento, max iterações por nota R34 (convergência >95) e escalação R18 após 3 impasses. Use para brainstorm de arquitetura/plano/código, troubleshooting com ground truth, decisões com tradeoff aberto."
mode: skill
tags: "a2a, brainstorm, debate, propositor, refutador, arbitro, tensao-cognitiva, tríade, loop, escalacao"
origin: helenizado:hefesto-v1
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-08-30
  author: Gran-Mestre
  motor: tríade VRAM (contrato-plano + refutacao + judge)
---

# A2A-BRAINSTORM — A Ágora

Loop A2A estruturado com **tríade de papéis** na VRAM. O enxame corrige as próprias alucinações antes de entregar ao Orquestrador (Ornith-35B CPU).

## Tríade (fixa — diversidade de pesos = tensão real)

| Papel | Modelo | Slot | Função |
|---|---|---|---|
| 🛠️ Propositor | Qwen3.8-4B | :9088 | gera 1ª versão (plano/código/extração), pragmático |
| 🧠 Refutador | Ternary-8B | :9090 | inspeciona falhas lógicas, desvios de contrato, gargalos |
| ⚖️ Árbitro | LLMJudge-3B | :9085 | pondera o embate, decide com nota R34 |
| 🏛️ Escalação | Ornith-35B | :8083 CPU | Suprema Corte — decisão final em impasse |

## Regras de engajamento (anti-loop-infinito)

1. **Propositor** propõe (contrato/spec.md no contexto).
2. **Refutador** refuta com evidência (nunca opinião solta).
3. **Árbitro** decide: nota R34 (0.0000001-100) + bugs concretos.
   - Nota < 90 → Propositor reescreve.
   - Nota ≥ 90 + elogios concretos → **PASSOU_CATEGORICO** (R28/R40).
4. **Max iterações**: convergência média > 95.0 (R34) OU 3 rodadas sem impressão → **escalar 35B** (R18).
5. Veredito registrado no decision-log (`[Refutação] rodada N → veredito → nota → evidência`).

## Motor

- **Script**: `scripts/a2a_brainstorm.py` — loop com tríade via API OpenAI-compatible dos slots.
- **Sampling por papel** (R61/R77): propositor temp 0.6 · refutador temp 0.8 · árbitro temp 0.15 · escalação temp 0.3.
- **Refutação do catálogo**: slot da tríade caiu (R10) → NÃO reatribuir papel (mata tensão) → redflag + escalar 35B.

## Output contract

```yaml
a2a_brainstorm:
  topic: "..."
  rounds: n
  proposer: {model, proposal_v1, rewrites: n}
  refuter: {model, refutations: [{round, evidence}]}
  arbiter: {model, scores: [{round, nota, bugs}]}
  converged: bool
  average_score: x.x
  escalated_to_35b: bool
  verdict: PASSOU_CATEGORICO | ESCALADO
  memory: {decision_log: true}
```

## Anti-padrões

- Concordância preguiçosa ("ok", "passou") — R40 proíbe.
- Loop infinito de discordância — max iterações por nota R34.
- Mesmo modelo em 2 papéis — mata a tensão cognitiva.
- Refutar sem evidência; aprovar sem nota; escalar sem 3 impasses.