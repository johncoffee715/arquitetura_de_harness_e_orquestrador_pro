# Grafo F0–F6 × Roster — mapeamento e gaps (helenização 2026-09-07)

> Fonte: doc do usuário (grafo 0–6 fases, loop externo, auto-ameliorativo via Hefesto)
> + R25 (6 fases) + R71/R42 (córtex/reflexo) + roteador-hibrido (Fase 0).
> Hardware: Xeon E5-2699v3 · X99 · 4x8GB DDR4 · MI50 16GB · SSD 128GB.

## Mapeamento fase→papel→ocupante

| Fase | Função do "mais veloz" no doc | Ocupante atual | Status |
|---|---|---|---|
| F0 ingestão/filtro | filtrar prompt+ctx+logs, pacote limpo | RWKV7 :9084 (L0.5) + Smol :9093 (micro) | OK |
| F1 brainstorm | consolidar/limpar refutações rejeitadas | GM (caro!) | **GAP** → DeepSeek-aux? |
| F2 contrato | cache semântico do spec | NINGUÉM | **GAP** → OLMoE? |
| F3 plano | compressão de tokens/history-cap | reflexo + GM (parcial) | **PARCIAL** → DeepSeek? |
| F4 execução | roteamento de ferro (schemas p/ executor) | NINGUÉM explícito | **GAP** → OLMoE-GBNF? |
| F5 revisão | agregador de diff (desvios de contrato) | Atena (skill, sem slot próprio) | **GAP** → DeepSeek? |
| F6 entrega/self | telemetria + scaffold write | GM + Hefesto | OK (juízo fica no GM) |

## Política híbrida Local/GPU × Nuvem (produção)

- **Local (latência/loop)**: F4 TDD, reflexo R42, micro, extração GBNF, filtros F0,
  drafts, crivos. Motivo: loop fechado sem custo/token nem round-trip.
- **Nuvem (profundidade)**: prosa F1 pesada, síntese F2, arbitragem final, overflow
  do GM (R20/R23), refutação-árbitro. Custo de referência: ~$0,20/1M (Muse Spark).
- **Regra de trânsito**: subiu p/ nuvem com resumo destilado (R22 rolling-summary),
  desceu com veredito+IDs. Nunca contexto bruto (janela e custo).

## Candidatos reavaliados (substituição → feature nova)

- **DeepSeek-MoE-Q3** (lógica ✓, PT fraco, 4K, 8.6G): F1-consolidador / F5-agregador
  (rajadas analíticas curtas; PT fraco irrelevante; ctx 4K basta p/ bursts).
- **OLMoE-Q4** (GBNF 5/5, CPU 27, 3.9G): F2-cache / F4-schema-router (GBNF é o trilho).
- **Qwen2.5-0.5B-Q3** (S1 ok CPU, GPU corrompe dígito): F0-classificador de intent
  (labels, não números) — caso fraco; só se F0 saturar.
- Todos excluídos do disco (R95); re-download ~15min sob ordem de criação.
