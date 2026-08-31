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

Loop A2A estruturado com **todos os LLMs rápidos** na VRAM (R42 — alta velocidade permite mais iterações). O enxame corrige as próprias alucinações antes de entregar ao Orquestrador (Ornith-35B CPU — exclusivo de orquestração, R46).

## Papéis (todos os LLMs rápidos — vocação R46 + debilidades documentadas)

| Papel | Modelo | Slot | Vocação | Debilidade (NÃO usar para) |
|---|---|---|---|---|
| 🛠️ Propositor | Qwen3.8-4B | :9088 | tool calling, sintaxe, velocidade | refatoração limpa profissional (q4_k_m → linhas preguiçosas "# insira seu código") |
| 🧠 Refutador | Ternary-8B | :9090 | profundidade conceitual, BFCL 73.9 | — |
| ⚖️ Árbitro | LLMJudge-3B | :9085 | avaliação emparelhada, pontuação | NUNCA gerar conteúdo original (código/MD/JSON) — só julgar |
| 🏛️ Escalação | LLMJudge-3B | :9085 | Suprema Corte local (rápida) | — |
| ⚡ Reflexo | LFM-1.2B | :9086 | raciocínio verbal rápido, testes acadêmicos | produção/JSON/Python (imaturidade de engenharia) |
| 🧠 Ingestor | RWKV7-0.4B | :9084 | peneira grossa, contexto 1M, prefill 2448 t/s | raciocínio profundo (0.4B) |

**35B (Ornith :8083)**: EXCLUSIVO de orquestração — nunca escalação síncrona (2× 35B em RAM = ~40GB + contenção DDR).

## Regras de engajamento (anti-loop-infinito)

1. **Propositor** propõe (contrato/spec.md no contexto).
2. **Refutador** refuta com evidência (nunca opinião solta).
3. **Árbitro** decide emparelhado (alternância de ordem elimina viés de posição):
   - Proposta vence → nota 70 (PASSOU_CATEGORICO se elogios).
   - Refutação procede → nota 45 (REESCREVER).
4. **Progresso gradativo (homeopatia R34)**: nota deve SUBIR ≥ PROGRESSO_MIN por rodada; estagnou/regrediu → impasse real → escala.
5. **Max iterações**: MAX_ROUNDS = 12 (alta velocidade GPU — R42) OU convergência (nota ≥ 70 + elogios) OU sem progresso → **escalar Judge-3B** (Suprema Corte local, rápida).
6. Veredito registrado no decision-log (`[Refutação] rodada N → veredito → nota → evidência`).

## Motor

- **Script**: `scripts/a2a_brainstorm.py` — loop com papéis via API OpenAI-compatible dos slots.
- **Sampling por papel** (R61/R77): propositor temp 0.6 · refutador temp 0.8 · árbitro/escalação temp 0.15 · reflexo temp 0.8 · ingestor temp 0.1.
- **Refutação do catálogo**: slot caiu (R10) → NÃO reatribuir papel (mata tensão) → redflag + escalar.

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