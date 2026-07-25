---
name: ecc-autofagia
description: Autofagia (self-digestion) para ECC
---

# ecc-autofagia

## Scripts
| Script | Funcao |
|--------|--------|
| ecc-attest.sh | SHA-256 store/verify/check |
| ecc-complete.sh | Completion gate + stats + list-pending |
| ecc-digest.sh | Engine de digestao |
| ecc-autofagia.sh | Orquestrador do ciclo |

## Hooks
| Hook | Tipo | Funcao |
|------|------|--------|
| ecc-safety-sha.sh | PreToolUse | Salva SHA antes de Write/Edit |
| ecc-2action-rule.sh | PostToolUse | Salva findings a cada 2 research |
| ecc-3strike.sh | PostToolUseFailure | Escala apos 3 falhas |
| ecc-attest.sh | PreToolUse | Verifica integridade de planos |

## Uso Rapido
bash /home/johncoffee/scripts/ecc-autofagia.sh health
bash /home/johncoffee/scripts/ecc-attest.sh verify <plan>
bash /home/johncoffee/scripts/ecc-complete.sh stats <plan>
