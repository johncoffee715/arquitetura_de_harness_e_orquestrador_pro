---
name: dokku-deploy
description: "Docker-powered mini-Heroku: deploy self-hosted via git push; app.json + plugin-hooks de ciclo de vida com triggers ordenados. (absorvido de dokku/dokku)"
---
# Dokku Deploy

Helenizado de [`dokku/dokku`](https://github.com/dokku/dokku).

## Propósito
PaaS docker minima: deploy de apps via git push com buildpacks/Dockerfile, ciclo de vida versionado em app.json e plugin-hooks de triggers ordenados por prefixo numerico.

## Padrões absorvidos (núcleo canônico do repo)
- Fluxo deploy: dokku apps:create <app> + git push dokku main + dokku ps:rebuild <app> (redeploy) / ps:set skip-deploy true
- app.json: scripts predeploy/postdeploy + healthchecks + formations — contrato de ciclo de vida da app
- Plugin-hooks prefixo numerico (00_dokku-standard, 20_events, app-json...) com triggers de ciclo de vida (pre-deploy, post-deploy...)
- Command API dokku: commands (help) + subcommands/default + subcommands/<cmd> -> dokku <plugin>:<cmd>
- plugin.toml obrigatorio (description+version); arquivos executaveis; adotar set -eo pipefail (dica oficial do dokku)

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="dokku-deploy")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/dokku/dokku
