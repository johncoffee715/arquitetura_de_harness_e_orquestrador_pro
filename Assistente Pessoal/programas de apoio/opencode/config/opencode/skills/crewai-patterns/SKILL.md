---
name: crewai-patterns
description: Role-based crew pattern — agent cards (role/goal/backstory), task contracts, sequential/hierarchical processes, event Flows (patterns only, never the framework).
category: skill
model: local-forge/proposer
---

# crewai-patterns

Padrão de crews por papéis + Flows event-driven, sem o framework: agent cards
(role/goal/backstory/tools), contratos de task (description/expected_output/context),
processos sequential/hierarchical e Flows com estado tipado + roteamento.
Helenizado de `crewaiinc/crewai` (origem: https://github.com/crewaiinc/crewai).

> PROIBIDO como dependência (doutrina R2): vault é a memória, catálogo é o registro.
> Aqui só o padrão organizacional.

## Quando usar

- Decompor trabalho em papéis especializados com contratos claros
- Combinar autonomia (crews) com controle determinístico (flows event-driven)
- Precisar de human-in-the-loop e checkpointing no desenho

## Como usar

1. **Cards**: cada agente = role + goal + backstory + tools (+ memória/guardrails se preciso)
2. **Contratos**: cada task = description + expected_output + agent (+ context de tasks anteriores)
3. **Processo**: sequential (cadeia) ou hierarchical (manager delega e valida)
4. **Flows**: estado tipado (Pydantic) + `@start/@listen/@router` p/ branches condicionais

## Princípio

Autonomia onde ajuda, controle explícito onde importa; telemetria sempre opt-out.
