---
name: onp-spec-driven
description: "Spec-driven development workflow. (absorvido de onovoprogramador/onp-spec-driven)"
---
# Onp Spec Driven

Helenizado de [`onovoprogramador/onp-spec-driven`](https://github.com/onovoprogramador/onp-spec-driven).

## Propósito
**A especificação que continua verdadeira.** Você descreve a feature, o agente

## Padrões absorvidos (núcleo canônico do repo)
- Especificação legível** em `.spec/features/<feature>/` — histórias de
- Plano de execução com paralelismo opcional** — tarefas que não se tocam
- Você sempre sabe o que está rolando** — antes de executar, o agente avisa
- Falhou uma faixa? refaça só ela** — peça *"reexecuta só a faixa 2"* e o
- Gestão de commits e branches feita** — 1 tarefa = 1 commit rastreável,
- A prova** — ao final, a auditoria mecânica: cada critério de aceite tem um

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="onp-spec-driven")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/onovoprogramador/onp-spec-driven
