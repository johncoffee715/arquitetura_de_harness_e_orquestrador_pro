---
name: fable-method
description: Think/act/prove loop — classify, define done with named verification, parallel evidence, one decision, surgical edits, observed verify (bounds enforced).
category: skill
model: local-forge/proposer
---

# fable-method

Loop think/act/prove com limites duros: classificar o ask, definir done com
verificação nomeada, evidência paralela de fontes primárias, UMA decisão,
edits cirúrgicos, verify observado, report outcome-first com caveats honestos.
Helenizado de `Sahir619/fable-method`
(origem: https://github.com/Sahir619/fable-method).

> Irmã `fable-judge` (já no catálogo) = o verificador adversarial. Aqui o FOCO é
> o LOOP completo + INTENT artifact + bounds (3 verify-fails→stop, 2 lookups→stop).

## Quando usar

- Qualquer task não-trivial multi-step (classificar antes de tocar)
- Quando autoridade conflita (spec vs teste: INTENT line decide)
- Runs desacompanhados (bounds impedem loop infinito)

## Como usar

1. **Classify**: trivial? question? task? plan-first? (tie-breaks explícitos)
2. **Define done**: verificação nomeada por shape (sem ela, perguntar)
3. **Evidence**: paralela, fontes primárias, intent antes de mudar
4. **Decide→Act→Verify→Report**: UMA recomendação; surgical; observado+bounded; outcome first

## Princípio

Regras em decision points, não em listas: `INTENT: code faz X / check espera Y / spec diz Z`.
