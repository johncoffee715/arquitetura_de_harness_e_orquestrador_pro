---
name: dokku-deploy
description: >-
  Docker-powered mini-Heroku: deploy self-hosted via git push; app.json + plugin-hooks de ciclo de vida com triggers ordenados. (absorvido de dokku/dokku)
category: skill-tecnica
model: local-thalamus/ingestor
version: 1.0.0
origin: https://github.com/dokku/dokku
helenized: true
r84: true
r77_triple: true
---
# dokku-deploy — deploy Dokku

Helenizado de [`https://github.com/dokku/dokku`](https://github.com/dokku/dokku) — essência destilada para harness nativo (R77 tríplice, R84 GBNF travado, R75 categoria).

## Propósito
Docker-powered mini-Heroku: deploy self-hosted via git push; app.json + plugin-hooks de ciclo de vida com triggers ordenados. (absorvido de dokku/dokku)

## Padrões absorvidos
- deploy: dokku, deploy, infra
- Origem: https://github.com/dokku/dokku
- Domínio: deploy Dokku

## Como usar (Gran-Mestre)
1. Detectar necessidade que casa com `dokku-deploy` (tags: dokku, deploy).
2. `skill(name="dokku-deploy")` — carrega tríplice (conceito + gabarito + mecânica).
3. Aplicar padrão helenizado ao contexto atual com GBNF travado (`temp 0.3`, `max_retries=3`).

## Tríplice R77
- `conceito.md` — ontologia/persona imutável (50-100 linhas, R75 `local-thalamus/ingestor`)
- `gabarito.json` — firewall allow/deny + schema rígido + `stop_tokens` + `max_tokens`
- `mecanica.md` + `mecanica.py` + `schema.gbnf` — ignição determinística, validação Pydantic, anti-loop

## Fonte
https://github.com/dokku/dokku
