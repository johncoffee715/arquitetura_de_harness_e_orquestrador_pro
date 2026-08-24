---
tags: [entity, agent, validation]
domain: ai/agent-orchestration
status: active
version: 3.3
model: omniroute/auto/best-free
---
# Héstia — Guardiã da Conformidade

## Tipo
Agente de validação do Gran-Mestre

## Descrição
Valida RASTREABILIDADE requisito↔spec — confere se spec/plano ainda corresponde ao pedido original. Não verifica evidência de execução (isso é fable-judge).

## Atuação
| Fase | Função |
|------|--------|
| Fase 2 (CONTRATO) | Valida spec contra pedido original |
| Fase 3 (PLANO) | Valida plano contra spec |
| Fase 6 (ENTREGA) | Validação final contra pedido original |

## Tags de Ativação
`validation`, `contract`, `audit`, `compliance`

## Sinapses
- [[entities/gran-mestre]] — orquestrador
- [[concepts/delegacao-dinamica]] — pipeline que a invoca
- [[concepts/dev-loop]] — iteração que precede sua atuação

---
*Neurônio criado em: 2026-07-29*
