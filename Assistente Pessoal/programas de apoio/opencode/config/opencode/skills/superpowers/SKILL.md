---
name: superpowers
description: Mandatory skill-check dev loop — brainstorm→worktree→plan→subagent-review→TDD→review→finish, with two-stage subagent review.
category: skill
model: local-forge/proposer
---

# superpowers

Metodologia dev em skills mandatórias: brainstorm antes do código, worktree isolada,
planos bite-sized, subagent-driven com review em 2 estágios (spec, depois qualidade),
TDD RED-GREEN de verdade, review entre tasks, finish com decisão merge/PR.
Helenizado de `obra/superpowers` (origem: https://github.com/obra/superpowers).

> Irmãs: `openspec`/`bmad-method` (planejamento), `andrej-karpathy-skills` (gates de
> diff), `fable-judge` (verificação). Aqui o FOCO é a checagem mandatória de skill
> antes de qualquer task + review duplo de subagents.

## Quando usar

- Antes de QUALQUER task (checar skills relevantes primeiro — mandatório, não sugestão)
- Execução via subagents com review spec→qualidade
- TDD estrito, worktrees paralelas, finish limpo

## Como usar

1. **Check**: skills relevantes antes da task (sempre)
2. **Brainstorm→Plan**: design em seções legíveis → plano bite-sized (2–5min/task, paths exatos)
3. **Execute**: subagent por task + review duplo; TDD RED-GREEN (código pré-teste é deletado)
4. **Review→Finish**: review por severidade (crítico bloqueia) → testes → merge/PR/discard + cleanup

## Princípio

Evidência sobre alegação: verificar antes de declarar done. Telemetria do original opt-out via env.
