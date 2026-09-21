# R95 — Sem Reservas: substituir ou excluir (promulgada 2026-09-07)

> Status: FORJADA (ordem do usuário) · incorporação no AGENTS.md pendente.
> Vale desde o registro no decision-log. Estende R21 (nada ocioso) ao disco.

## Regra

Quarentena (`filtragem/`) NÃO é estoque. Todo LLM que entra recebe veredito
binário por métricas (R83+R84): **SUBSTITUI** (canoniza no slot imediatamente,
mesma sessão) ou **EXCLUI** (apaga o arquivo na hora, com log). Proibido
"reserva quente/fria", "para depois", "failover parado".

- Vencedor sem slot livre: desloca o perdedor NA HORA (o displaced vai p/
  lixeira, não p/ quarentena) ou o veredito vira EXCLUI para o candidato.
- Failover se resolve com re-download (minutos), não com estoque (GB parados).
- Exceção única: draft ativo e pesos em produção (uso real, não reserva).

## Precedente canônico (06-07/09)

- OLMoE-1B-7B: perde relay p/ Llama-3B (5/5+PT-parcial+27CPU vs 10/10+PT-limpo+129GPU) → EXCLUÍDO (3.9G).
- Qwen1.5-MoE-Q3: sem incumbente a deslocar em seu propósito (refuter-CPU vago;
  criar slot novo = adição, não substituição) → EXCLUÍDO (6.9G).
