---
name: identity-authz-apl
description: ABAC micro-policy pattern — when/then rules with salience, bounded RETE execution, explain and quota (no arbitrary logic).
category: skill
model: local-forge/proposer
---

# identity-authz-apl

Micro-linguagem ABAC: policies de regras `when` (atributos sub/res/env) → `then`
(decision + obligations), com salience, execução limitada (RETE, para na decisão),
explain e quota. Helenizado de `intuit/identity-authz-apl`
(origem: https://github.com/intuit/identity-authz-apl).

## Quando usar

- Decisão de acesso por atributos (user/resource/env), não por role fixa
- Políticas que precisam responder em microssegundos com heap mínimo
- Auditoria de decisão (explain: quais regras dispararam, com stats)

## Como usar

1. **Regras**: `rule: nome` + `description` + `salience` + `when:` (conds) + `then:` (decision)
2. **Ordem**: deny > permit > default (salience decrescente; 1 default só)
3. **Limites**: quota anti-hog; sem network/DB/computação arbitrária nas conds
4. **Explain**: stats (regras, fired, condições únicas, tempos) + regras inconsistentes

## Princípio

Decisão bounded, determinística e explicável — ou não é policy, é código disfarçado.
