---
name: openspec
description: Fluid spec-driven loop for AI coding — explore/propose/apply/archive change folders + cross-repo Stores (brownfield-first).
category: skill
model: local-forge/proposer
---

# openspec

Spec layer leve sobre o coding agent: cada mudança ganha pasta própria
(`proposal.md` + `specs/` + `design.md` + `tasks.md`), evolui fluida e arquiva.
Para features cross-repo, Stores compartilham specs via git. Helenizado de
`Fission-AI/OpenSpec` (origem: https://github.com/Fission-AI/OpenSpec).

> Irmãs no catálogo: `spec-kit` (rigoroso, phase-gates) e `onp-spec-driven`.
> OpenSpec = o polo fluido/iterativo/brownfield (sem gates rígidos).

## Quando usar

- Feature nova ou mudança brownfield que merece plano revisável antes do código
- Mudança cross-repo (API + web + lib): planejar num Store compartilhado
- Quando spec-kit parecer cerimônia demais (fluido > rígido)

## Como usar

1. `/opsx:explore` — pensar junto, sem compromisso
2. `/opsx:propose <ideia>` → `openspec/changes/<nome>/` (proposal + specs WHEN/THEN + design + tasks)
3. `/opsx:apply` — implementar tasks; `/opsx:archive` — arquivar e atualizar specs
4. Cross-repo: Store próprio (`openspec/` + `git push`), referenciado read-only

## Princípio

Specs em Markdown puro, sem sintaxe especial. Iterar qualquer artefato a qualquer hora.
