---
name: openagentscontrol
description: Plan-first agent framework pattern — approval-gated execution with automatic testing, review and validation (multi-language).
category: skill
model: local-forge/proposer
---

# openagentscontrol

Padrão plan-first com gates de aprovação: plano proposto → aprovado → executado
com testes, review e validação automáticos. Multi-linguagem. Helenizado de
`darrenhinde/openagentscontrol` (origem: https://github.com/darrenhinde/openagentscontrol).

> Nativo-primeiro: só o padrão (plan→approve→execute+validate). Nunca o framework como dependência.

## Quando usar

- Feature que merece plano revisável antes de qualquer escrita
- Execução que exige validação automática (testes + review + build)
- Quando precisar de gates humanos explícitos no loop

## Como usar

1. **Propor**: plano com escopo, arquivos e critérios de verificação
2. **Aprovar**: humano aprova (gate obrigatório, nunca auto-executa)
3. **Executar**: incremental, com testes + review + validação por etapa

## Princípio

Nenhuma escrita antes da aprovação. Nenhuma etapa sem verificação.
