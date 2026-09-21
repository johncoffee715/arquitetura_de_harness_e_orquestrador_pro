---
name: <slug-da-skill>
description: >
  <uma frase objetiva: o que esta skill cobre e quando o agente deve
   lê-la. É isso que aparece na listagem de skills disponíveis>
triggers:
  - <palavra-chave-1>
  - <palavra-chave-2>
  - "<frase de gatilho entre aspas, se tiver espaço>"
metadata:
  origin: gran-mestre-original
  # ou: absorvido:<projeto-fonte> -- rastreia proveniência (antropofagia)
  category: <categoria -- ex: orchestration, security, testing>
  version: "1.0"
scripts_associados:
  - <caminho-relativo-do-script-1, se houver>
  - <caminho-relativo-do-script-2, se houver>
# IMPORTANTE: liste aqui TODO script .sh/.py/.js/.ts na mesma pasta,
# mesmo que pareça auxiliar/opcional. A auditoria de segurança de
# 84 skills que fizemos só cobriu SKILL.md e nunca tocou scripts —
# foi assim que 453 linhas de bash do ecc-autofagia passaram sem
# revisão. Se este campo ficar vazio mas existir script na pasta,
# está desatualizado, não é "skill puramente declarativa".
---

# <Nome da Skill>

## Quando usar
<Critério concreto de acionamento — não "quando fizer sentido".>

## Como funciona
<Passo a passo do que a skill instrui o agente a fazer.>

## Scripts associados e o que fazem
<Para cada script listado em scripts_associados: o que ele faz e
por que precisa existir fora do SKILL.md. Rode skill-security-audit.sh
contra qualquer script novo antes de habilitar esta skill.>

## O que NÃO faz
- <proibição 1>
- <proibição 2>
