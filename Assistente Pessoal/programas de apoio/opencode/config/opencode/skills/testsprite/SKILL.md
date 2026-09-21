---
name: testsprite
description: Agent test-verification loop — verify/onboard skills + plan.schema.json contract for AI-tested code (patterns only).
category: skill
model: local-forge/proposer
---

# testsprite

Loop de verificação de testes p/ agentes: skill verify (confere o que o agente
afirma), skill onboard (prepara o repo), contrato `plan.schema.json` p/ planos de
teste estruturados. Helenizado de `TestSprite/testsprite-cli`
(origem: https://github.com/TestSprite/testsprite-cli, v0.11.0, SHA 125872f).

> Clonado e lido na fonte (`/tmp/opencode/repos/testsprite-cli`: package.json real,
> `skills/*.skill.md`, `schemas/plan.schema.json`). Só padrões — backend presumido.

## Quando usar

- Agente afirma "testes passam" (verificar de verdade antes de aceitar)
- Preparar repo p/ bateria de testes de agente (onboard)
- Planos de teste em contrato estruturado (schema versionado)

## Como usar

1. **Onboard**: prepara repo/ambiente p/ verificação
2. **Plan**: plano contra `plan.schema.json` (contrato)
3. **Verify**: executa, confere afirmações, reporta com evidência
4. **Gate**: done só com verificação observada (nunca auto-declaração)

## Princípio

Irmão do `fable-judge` (adversarial) no polo testes: desconfiar da afirmação, rodar de novo.
