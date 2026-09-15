---
name: ecc
description: Harness-optimization patterns — instincts, research-first dev, memory discipline, AgentShield-style config scanning (patterns only).
category: skill
model: local-forge/proposer
---

# ecc

Padrões de otimização de harness: instincts reutilizáveis, desenvolvimento
research-first, disciplina de memória e varredura de segurança em configs
(prompts, hooks, MCP, permissões, segredos). Helenizado de `affaan-m/ecc`
(origem: https://github.com/affaan-m/ecc).

> Nativo-primeiro: só padrões. Os 68 agents / 292 skills do original NÃO são
> copiados — o catálogo próprio já cobre skills; aqui entram instincts,
> research-first e AgentShield.

## Quando usar

- Transformar vitória repetida em instinct reutilizável
- Antes de codar contra API nova (research-first: docs oficiais primeiro)
- Auditar prompts/hooks/MCP/permissões/segredos (AgentShield pattern)
- Decidir o que lembrar (memória com disciplina, não dump)

## Como usar

1. **Research-first**: docs oficiais → padrões → só então código
2. **Instincts**: vitória repetida 2×+ vira regra versionada
3. **AgentShield**: scan de prompts, hooks, MCP configs, permissões, segredos
4. **Memória**: lembrar o que muda decisão futura; resto é ruído

## Princípio

Otimizar a janela: persistir todo o resto (vault), nunca inflar o contexto.
