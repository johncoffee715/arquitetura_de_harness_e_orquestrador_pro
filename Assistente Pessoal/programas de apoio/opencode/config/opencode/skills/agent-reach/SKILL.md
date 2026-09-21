---
name: agent-reach
description: >-
  > MUST USE when user wants to 调研/research/搜索/search/查/找/look up anything on the internet — e.g. 全网调研 X / 帮我调研一下 X / 查一下 X / 搜搜 X / 看看大家怎么评价 X / X 上有什么讨论 / research this topic。 Also MUST USE when user mentions any platform or shares any URL/链接: 小红书/xiaohongshu/xhs, Twitter/推特/X, B站/bilibili, Reddit, 
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/agent-reach
helenized: true
r84: true
r77_triple: true
---
# agent-reach — roteador multi-plataforma

Helenizado de [`https://github.com/agent-reach`](https://github.com/agent-reach) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
> MUST USE when user wants to 调研/research/搜索/search/查/找/look up anything on the internet — e.g. 全网调研 X / 帮我调研一下 X / 查一下 X / 搜搜 X / 看看大家怎么评价 X / X 上有什么讨论 / research this topic。 Also MUST USE when user mentions any platform or shares any URL/链接: 小红书/xiaohongshu/xhs, Twitter/推特/X, B站/bilibili, Reddit, 

## Padrões absorvidos
- roteamento internet: multi-backend routing, 15 plataformas, doctor --json
- Origem: https://github.com/agent-reach
- Domínio: roteador multi-plataforma

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `agent-reach` (tags: multi-backend routing, 15 plataformas).
2. `skill(name="agent-reach")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/agent-reach
