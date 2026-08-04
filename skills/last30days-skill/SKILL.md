---
name: last30days-skill
description: "Pesquisa/síntese multi-plataforma 30d (Reddit, X, YouTube, HN, Polymarket) com ranking por upvotes — ADAPTADO: só a pipeline de briefing, nunca hook cru (RCE upstream corrigido). (absorvido de mvanhorn/last30days-skill)"
origin: absorvido:mvanhorn/last30days-skill
metadata:
  autofagia: mvanhorn/last30days-skill (2026-08-04)
  prioridade: 17
  linguagem: Python
  topics: research, search, synthesis
  artefatos: skill
  padroes_absorvidos: 1
---
# Last30days Skill

Helenizado de [`mvanhorn/last30days-skill`](https://github.com/mvanhorn/last30days-skill).

## Propósito
Pesquisa/síntese multi-plataforma 30d (Reddit, X, YouTube, HN, Polymarket) com ranking por upvotes — ADAPTADO: só a pipeline de briefing, nunca hook cru (RCE upstream corrigido).

## Padrões absorvidos (núcleo canônico do repo)
- Pesquisa/síntese multi-plataforma 30d (Reddit, X, YouTube, HN, Polymarket) com ranking por upvotes — ADAPTADO: só a pipeline de briefing, nunca hook cru (RCE upstream corrigido).

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="last30days-skill")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/mvanhorn/last30days-skill
