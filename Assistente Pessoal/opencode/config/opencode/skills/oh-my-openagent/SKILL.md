---
name: oh-my-openagent
description: Multi-model harness patterns — category-routed models, hash-anchored edits, skill-embedded MCPs, Team Mode crews (patterns only).
category: skill
model: local-forge/proposer
---

# oh-my-openagent

Padrões do harness multi-model OmO: roteamento por categoria (não por modelo),
edits hash-ancorados (zero stale-line), MCPs embutidas em skills (on-demand),
Team Mode (lead + membros paralelos), IntentGate + Todo Enforcer.
Helenizado de `code-yeongyu/oh-my-openagent`
(origem: https://github.com/code-yeongyu/oh-my-openagent).

> Licença SUL-1.0 (source-available, NÃO OSI): aqui só padrões, nunca código.
> Irmã `oh-my-opencode-slim` já cobre o slim — aqui o delta (hashline/categorias/Team).

## Quando usar

- Delegar por categoria de trabalho (visual/deep/quick/ultrabrain), não por modelo
- Edits cirúrgicos sem stale-line (hash da linha como âncora)
- MCPs sem inchar contexto (embarcada na skill, sobe sob demanda, morre depois)
- Crew paralela com ferramentas dedicadas (create/send/status)

## Como usar

1. **Categoria**: dizer o TIPO do trabalho; o harness mapeia p/ o modelo
2. **Hashline**: ler (linhas vêm com `#ID`) → editar referenciando `#ID`; mismatch rejeita antes de corromper
3. **Skills+MCP**: skill carrega seu MCP; escopo da task; descarrega ao fim
4. **Team**: lead + até 8 membros paralelos; hyperplan (5 críticos) p/ planos

## Princípio

`ultrawork`: uma palavra, todos os agentes, até done — com disciplina (planner entrevista antes).
