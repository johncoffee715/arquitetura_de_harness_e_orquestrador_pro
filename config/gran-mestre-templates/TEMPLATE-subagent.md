---
# ============================================================
# CAMPO REAL DO OPENCODE
# ============================================================
name: <slug-do-subagente>
mode: subagent
# ^ so aceita subagent | primary | all. Este e o valor default pra
#   praticamente tudo -- confirmado: todo arquivo em agents/ e
#   subagent, exceto o Gran-Mestre.

# ============================================================
# CATEGORIZACAO DO PROJETO
# ============================================================
component_type: subagent
origin: gran-mestre-original
# gran-mestre-original = criado nativamente
# absorvido:<projeto-fonte> = devorado via antropofagia
#   (ex: absorvido:oh-my-openagent, absorvido:fable-method)

# ============================================================
# CAPABILITY MANIFEST — usado pelo CapabilityIndex (greedy cover)
# ============================================================
capabilities:
  - <capability-1>
  - <capability-2>
complexity_range: [MEDIUM, COMPLEX]
cost: medium                # light | medium | heavy
requires: []                # MCPs/dependencias externas necessarias

# ============================================================
# MODELO
# ============================================================
model:
  primary: <modelo-principal-do-harness>
  fallback_chain:
    - <modelo-alternativo-1>
    - cloud:<provider/modelo>

# ============================================================
# AUTONOMIA E VALIDACAO
# ============================================================
autonomy: interactive        # interactive | autonomous
max_validation_cycles: 3
# Confirme o numero real contra LOOP_LIMIT_DECISION.md -- ja tivemos
# inconsistencia de 3 vs 5 documentada ali antes de copiar um valor.

# ============================================================
# QUANDO E CHAMADO / O QUE AVALIA
# ============================================================
triggered_when: >
  <situação concreta e específica deste projeto -- não "quando
   necessário". Se não dá pra escrever um caso de uso real, o
   subagent provavelmente está mal definido.>
evaluates: >
  <o que especificamente avalia/verifica -- só preencher se for
   validador/revisor. Deixar "" se não avalia nada.>
---

# <Nome do Subagent>

## Regras
- <regra específica 1>
- <regra específica 2>

## O que NÃO faz
- <proibição 1>
- <proibição 2>
