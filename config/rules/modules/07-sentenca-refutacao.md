---
numero: R54
tema: Sentenca de validacao e principios LLM-as-Judge
categoria: harness
setor: orquestrador
escopo: global
vigencia: 2026-08-18
---

# R54 — Sentença F5/F6 + Princípios LLM-as-Judge (pedido do usuário 2026-08-18)

## Sentença (Fases 5 e 6 / R52)

O artefato refinado pelas refutações A2A anteriores é entregue ao **ornith-1.0-9B.Q4_K_M.gguf (GPU)**,
que executa a auditoria final (F5 — revisão macro) e aplica o **selo de qualidade** ou
**rejeita**, com base na **nota de impressão real** (R37/R40: ≥90 + elogios concretos +
bugs reais + evidência). O veredito segue R28 (PASSOU_CATEGORICO/NAO_PASSOU por métrica).
Sem selo → artefato volta ao loop de refutação (R40), nunca avança por aprovação burocrática.

## Guardrails LLM-as-Judge (zylos 2026, helenizado)

1. **Juiz ≥ agente + modelo DIFERENTE**: o juiz deve ser tão ou mais capaz que o agente
   avaliado e, idealmente, um modelo distinto (evita blind spots compartilhados).
2. **Boundaries de julgamento**: julgar antes de output ao usuário, antes de tool call
   irreversível (write/send/deploy) e em escritas de memória persistente — não em todo
   passo intermediário (custo).
3. **Calibração mensal**: recalibrar todo validador contra golden set anotado pelo usuário
   (a calibração deriva: 7/10 hoje pode ser 5/10 em 6 meses). Fator <0.5 → só detector
   de bugs, nunca juiz (R52).
4. **Auto-correção intrínseca NÃO funciona**: "revisar seu próprio trabalho" sem grounding
   externo degrada o desempenho. Refutação LLM só é confiável com **verificação
   determinística + tool use** (testes unitários, execução de código, retrieval, tool-output
   comparison). O juiz real mais forte = test runner.

## Aplicação

- F5: LLM Orquestrador (GPU) audita diff holístico; F6: selo/rejeição com impressão real.
- Refutação A2A: matriz em camadas (R42 rápidos → 1.7B/2B leves → LLM Orquestrador/9B/Ridge altos)
  + calibração obrigatória (R52) + grounding externo sempre que possível.

## Impacto prático no pipeline (segmentação de papéis — pedido do usuário 2026-08-18)

```
GERADORES (lógica)         JUÍZES (crítica/pontuação)         SENTENÇA (assinatura)
LLM Orquestrador/9B/Ridge/2B   →    LFM/0.8B/1.7B/2B/Judge-3B     →    ornith-1.0-9B.Q4_K_M.gguf (GPU)
criam o artefato            avaliam com acurácia 0.88-0.95    assina o manifesto final
                            (R52: ≥2 vozes + calibração)      quando nota > limiar crítico,
                                                              OU refuta e devolve ao loop (R40)
```

- Máxima eficiência: modelos geram; juízes fazem o trabalho pesado de crítica/pontuação;
  LLM Orquestrador apenas **assina** (não reavalia tudo — só o veredito final consolidado).
- Limiar crítico: definido por aplicação (default: nota de impressão ≥90 + evidência, R37/R40).
- Abaixo do limiar → LLM Orquestrador refuta com bugs concretos e devolve ao gerador (loop A2A, R40).
