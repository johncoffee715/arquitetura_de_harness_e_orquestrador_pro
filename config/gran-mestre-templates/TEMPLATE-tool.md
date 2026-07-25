---
name: <slug-da-tool>
# SEM campo `mode:` -- tool nao e um agente do OpenCode, e um
# utilitario determinístico chamado por agents/subagents.

component_type: tool
origin: gran-mestre-original
# ou: absorvido:<projeto-fonte>

invoked_by:
  - <agent-ou-subagent-que-chama-1>
  - <agent-ou-subagent-que-chama-2>

script: <caminho-real-do-script, se houver>
deterministic: true
# true = mesma entrada sempre produz a mesma saida (ex: validador de
#   shell, hash, parser). false = tem algum grau de nao-determinismo
#   (ex: chama um modelo). Tools deterministicas nao precisam de
#   model/fallback_chain -- se este campo for false, adicione um
#   bloco `model:` como no TEMPLATE-subagent.md.

input_contract: >
  <o que a tool espera receber -- tipo e forma, nao so um exemplo>
output_contract: >
  <o que a tool retorna -- tipo e forma>

requires: []
---

# Tool: <nome>

## O que faz
<Descrição objetiva e estreita -- uma tool faz UMA coisa bem feita.
 Se está descrevendo mais de uma responsabilidade, provavelmente
 deveria ser um subagent, não uma tool.>

## O que NÃO faz
- <proibição 1>
- <proibição 2>

## Notas de segurança
<Se houver script associado, ele precisa passar por
 skill-security-audit.sh (ou revisão manual equivalente) antes de
 ser habilitado -- mesma exigência que vale pra scripts de skill.>
