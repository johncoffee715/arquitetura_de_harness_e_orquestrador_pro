---
tags: [concept, development, iteration]
related: [[entities/gran-mestre]] [[concepts/delegacao-dinamica]]
last_updated: 2026-07-29
---
# Dev Loop — 3 Níveis de Iteração Neural

## Definição
Sistema de iteração em cascata que imita o ciclo cognitivo humano: pensa → age → observa → repete. Três níveis com escalonamento automático.

## Arquitetura Neural
```
                    ┌─────────────────────────────┐
                    │         TASK ENTRADA        │
                    │   (estímulo sensorial)       │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │     CÓRTEX PRÉ-FRONTAL      │
                    │  (classificador de escopo)  │
                    └──────┬──────────────┬───────┘
                           │              │
                      simples         complexa
                           ▼              ▼
                ┌──────────────────┐  ┌──────────────────┐
                │   N1 — ReAct     │  │   N2 — Mini Loop │
                │  (reflexo)       │  │  (habitual)      │
                └────────┬─────────┘  └────────┬─────────┘
                         │                     │
                    3 falhas?             incerteza?
                         └──────┬──────────────┘
                                │
                                ▼
                   ┌──────────────────────────┐
                   │   N3 — Human Loop         │
                   │  (consciência)            │
                   │  humano decide            │
                   └──────────────────────────┘
```

## Nível 1 — ReAct (Reflexo Neural)
**Ciclo:** pensa → age → observa → repete
**Equivalente:** Arco reflexo da medula espinhal
**Quando:** Tasks de 1-3 arquivos, <5 tool calls
**Morte:** Task completa ou 3 falhas (escala)

## Nível 2 — Mini Loop (Memória Habitual)
**Ciclo:** spec → branch → TDD → implementa → verifica → merge
**Equivalente:** Gânglios da base (hábitos motores)
**Quando:** Features locais, 3-5 tasks, spec clara
**Morte:** Feature mergeada ou incerteza (escala)

## Nível 3 — Human Loop (Consciência)
**Ciclo:** decide → métricas → triagem → planeja → executa → PR → decide
**Equivalente:** Córtex pré-frontal (decisão consciente)
**Quando:** Épicos, incerteza alta, múltiplos módulos
**Morte:** Decisão humana explícita

## Escalonamento Automático
```
ReAct (N1) → 3 falhas → Mini Loop (N2) → incerteza → Human Loop (N3)
                                                                        ↓
                                                                  Humano decide
                                                              ├── CONTINUAR
                                                              ├── AJUSTAR
                                                              └── ENCERRAR
```

## Sinapses
- [[entities/gran-mestre]] — quem invoca o Dev Loop
- [[concepts/delegacao-dinamica]] — pipeline que contém o loop
- [[2026-07-29-gran-mestre-v7-mix-dev-loop]] — decisão arquivada

---
*Neurônio criado em: 2026-07-29*
