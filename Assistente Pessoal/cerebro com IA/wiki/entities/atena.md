---
tags: [entity, agent, review]
domain: ai/agent-orchestration
status: active
version: 3.3
model: omniroute/auto/best-free
---
# Atena — Revisão Macro

## Tipo
Agente de revisão macro do Gran-Mestre

## Descrição
Revisa o diff TOTAL de uma feature (coerência cross-task, acoplamento, arquitetura). Diferente do code-reviewer (revisão micro por task), Atena é chamada 1x por pipeline na Fase 5.

## Dimensões de Revisão
1. **Coerência cross-task** — Tasks se conectam logicamente?
2. **Acoplamento** — Componentes estão adequadamente desacoplados?
3. **Arquitetura** — Padrões e convenções são seguidos?
4. **Segurança** — Não há superfície de ataque exposta?
5. **Veredicto** — APPROVED / APPROVED_WITH_CAVEATS / CHANGES_REQUIRED

## Tags de Ativação
`review`, `macro`, `architecture`, `audit`, `adversarial`

## Sinapses
- [[entities/gran-mestre]] — orquestrador
- [[concepts/delegacao-dinamica]] — pipeline que a invoca
- [[concepts/antropofagia-tecnologica]] — origem (composição Oracle)

---
*Neurônio criado em: 2026-07-29*
