---
# ============================================================
# CAMPO REAL DO OPENCODE
# ============================================================
name: <slug-do-agente>
mode: primary
# ^ so aceita subagent | primary | all. "primary" e reservado pra
#   pontos de entrada de verdade -- na pratica, so o Gran-Mestre.
#   Criar um segundo "primary" sem necessidade real reintroduz
#   ambiguidade de roteamento (o problema que o Gran-Mestre existe
#   pra resolver). Pense duas vezes antes de usar este template.

# ============================================================
# CATEGORIZACAO DO PROJETO
# ============================================================
component_type: agent
origin: gran-mestre-original
description: >
  <em uma frase: que fluxo este orquestrador comanda e por que
   precisa ser um ponto de entrada proprio, nao um subagent>

# ============================================================
# CAPACIDADES E ROTEAMENTO
# ============================================================
capabilities:
  - orchestration
  - <outras capacidades de orquestracao especificas>
complexity_range: [TRIVIAL, SIMPLE, MEDIUM, COMPLEX, CRITICAL, FEATURE]
# Um primary tipicamente cobre TODAS as rotas -- e o ponto de entrada.

pipeline:
  - <agente/subagent 1, na ordem em que e chamado>
  - <agente/subagent 2>
# Referencia os subagents que este orquestrador comanda. Cada um
# deve ter seu proprio arquivo via TEMPLATE-subagent.md.

# ============================================================
# MODELO
# ============================================================
model:
  primary: <modelo-principal-do-harness>
  fallback_chain:
    - <modelo-alternativo-1>
    - cloud:<provider/modelo>

# ============================================================
# SEGURANCA E VALIDACAO
# ============================================================
safety_protocol: >
  <referencia concreta: SHA salvo antes de que fase, rollback
   automatico em que condicao, quantos rollbacks por pipeline>
autonomy: interactive
max_validation_cycles: 0
# Geralmente 0 aqui -- os limites de ciclo pertencem aos loops que
# este orquestrador comanda (documentar em cada subagent envolvido),
# nao ao orquestrador em si.
---

# <Nome do Agente Primary>

## Rotas de complexidade
| Rota | Pipeline |
|---|---|
| TRIVIAL | <...> |
| SIMPLE | <...> |
| MEDIUM | <...> |
| COMPLEX/CRITICAL | <...> |
| FEATURE | <...> |

## Regras
- <regra 1>
- <regra 2>

## O que NÃO faz
- Não executa código diretamente
- <proibições específicas deste orquestrador>

## Integração com CrossOver
<Se agentes/subagents de fontes externas (oh-my-openagent, Superpowers,
 Fable Method) entram no pipeline deste orquestrador, documentar aqui
 a costura real. Deletar a seção se não aplicável.>
