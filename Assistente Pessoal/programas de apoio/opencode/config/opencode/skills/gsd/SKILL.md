---
name: gsd
description: Long-horizon context engineering — phased plans, file-based context packets, big-picture retention for autonomous multi-hour runs.
category: skill
model: local-forge/proposer
---

# gsd

Engenharia de contexto p/ runs autônomos longos: planos faseados que sobrevivem a
compactações, pacotes de contexto em arquivo (3 primitivas, zero deps) e retenção
do big picture sem perder o fio. Helenizado da org `gsd-build`
(origem: https://github.com/gsd-build — flagship `get-shit-done`/`gsd-2`, `context-packet`).

> Org (não repo único): absorvidos os padrões flagship. `gsd-browser` (CDP) fica
> com `browser-use`; daemon/cloud fora do escopo local-first do harness.

## Quando usar

- Agente precisa trabalhar horas sem perder o big picture
- Contexto precisa atravessar compactações (arquivo, não janela)
- DAG de workflows com resolução de contexto por arquivo

## Como usar

1. **Fases**: plano em fases com critérios de saída; cada fase fecha com resumo em arquivo
2. **Pacotes**: contexto em arquivos (3 primitivas), resolução por path, zero deps
3. **Big picture**: 1 parágrafo âncora recarregado a cada fase; deriva → re-ancorar

## Princípio

Estado em disco versionado, nunca só na janela: interromper/continuar sem perder nada.
