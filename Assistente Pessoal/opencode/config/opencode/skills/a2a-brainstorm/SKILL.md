---
name: a2a-brainstorm
description: "Loop A2A (Agent-to-Agent) de refutação INCANSÁVEL com nota retroativa (R40/R34): os LLMs se refutam sem árbitro externo no loop, a nota inicial (piso 0.0000001) alimenta retroativamente cada rodada com deltas homeopáticos (+1..+3 por melhoria real). Papéis: Propositor (Qwen-4B :9088), Refutador (Ternary-8B :9090), Refutador Ágil (Gemma-2-2B :9092), Reflexo (LFM :9086), Ingestor (RWKV7 :9084). Judge-3B (escalação) só em impasse final. Use para brainstorm de arquitetura/plano/código com amadurecimento progressivo do produto."
mode: skill
tags: "a2a, brainstorm, refutacao, incansavel, nota-retroativa, homeopatica, r40, r34, tensao-cognitiva"
origin: helenizado:hefesto-v1
metadata:
  category: methodology
  version: 2.0.0
  date: 2026-08-31
  author: Gran-Mestre
  motor: refutação incansável (sem árbitro no loop)
---

# A2A-BRAINSTORM — Refutação Incansável com Nota Retroativa

Loop A2A onde os **próprios LLMs se refutam incansavelmente** (R40), sem árbitro externo caro. A métrica de nota inicial é o **alimento retroativo de aprendizado**: cada rodada recebe a nota atual no prompt e deve justificar a subida.

## Papéis (refutação entre os LLMs — sem árbitro no loop)

| Papel | Modelo | Slot | Função |
|---|---|---|---|
| 🛠️ Propositor | Qwen3.8-4B | :9088 | gera/reescreve a proposta corrigindo refutações |
| 🧠 Refutador | Ternary-8B | :9090 | refuta incansavelmente (falhas/contrato/gargalos) + avalia delta |
| ⚡ Refutador Ágil | Gemma-2-2B | :9092 | 2ª voz crítica (lógica/matemática) |
| 💬 Reflexo | LFM-1.2B | :9086 | opinião verbal rápida (opcional) |
| 🧠 Ingestor | RWKV7-0.4B | :9084 | contexto massivo (1M) |
| 🏛️ Escalação | LLMJudge-3B | :9085 | Suprema Corte — APENAS em impasse final (raro) |

## Notas homeopáticas (R34 — recalibradas 31/08)

- **Piso real**: 0.0000001 (nada é perfeito — nunca 0 absoluto, nunca salto).
- **Delta por rodada**: +1 a +3 por melhoria real (subida LENTA e gradativa), 0 se estagnou, negativo se regrediu.
- **Convergência**: nota ≥ 30.0 (limiar BAIXO — era 70, inflado) **E** impressão real (R40: elogios concretos).
- **Alimento retroativo**: a nota atual entra no prompt de cada rodada ("NOTA ATUAL: X — sua correção deve justificar subir").

## Regras de engajamento

1. Propositor propõe (nota inicial = piso).
2. Refutador (Ternary) ataca — nota no contexto.
3. Refutador Ágil (Gemma) ataca com lógica.
4. Propositor corrige TODOS os pontos.
5. Refutador avalia com GBNF estrito: `{"delta": +1..+3|0|-1..-3, "impresso": bool}`.
6. Nota evolui homeopaticamente → alimenta a próxima rodada.
7. **Convergência**: nota ≥ limiar + impresso → PASSOU_CATEGORICO.
8. **Estagnação** (delta < 1 em 2+ rodadas) → impasse → ESCALA (Judge-3B).
9. **Teto**: max 10 rodadas (refutação incansável com trava anti-loop).

## Motor

- **Script**: `scripts/a2a_brainstorm.py` — loop com GBNF estrito para avaliação.
- **Sampling** (R61/R77): propositor 0.6 · refutador 0.8 · escalação 0.15.
- **Refutação do catálogo**: slot caiu → NÃO reatribuir papel (mata tensão) → redflag + escalar.

## Output contract

```yaml
a2a_brainstorm:
  topic: "..."
  rounds: n
  converged: bool
  nota_final: x.xxxxx      # homeopática (piso 0.0000001 → convergência ~30)
  nota_media: x.xxxxx
  motivo_parada: "convergência | estagnação"
  verdict: PASSOU_CATEGORICO | ESCALADO
  rounds_detail: [{round, delta, nota, impresso}]
  escalation_decision: ... # se escalado
```

## Anti-padrões

- Árbitro externo por rodada (custo alto p/ escolha binária — removido).
- Notas infladas (70/45 — recalibradas para homeopatia real).
- Concordância preguiçosa ("ok", "passou") — R40 proíbe.
- Loop infinito sem trava — teto 10 rodadas.
- Mesmo modelo em 2 papéis — mata tensão.
