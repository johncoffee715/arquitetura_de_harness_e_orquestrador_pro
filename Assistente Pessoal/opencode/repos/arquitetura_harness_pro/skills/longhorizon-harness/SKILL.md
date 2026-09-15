---
name: longhorizon-harness
description: "Harness de execução long-horizon: 3 papéis (Manager/Executor/Auditor), estado verificado durável e contexto-fresco por rodada p/ tarefas de várias horas em desktop+CLI. (absorvido de AMAP-ML/LongHorizon-Harness)"
---
# LongHorizon-Harness

Helenizado de [`AMAP-ML/LongHorizon-Harness`](https://github.com/AMAP-ML/LongHorizon-Harness) (arXiv 2608.01964, #1 HuggingFace Daily Papers semana W32/2026).

## Propósito
Sistema de **execução, gestão de estado e verificação de resultados** para tarefas long-horizon. Não treina nem substitui o agente — roda **por cima** de Codex/Claude Code, permitindo operar o computador inteiro (apps desktop + CLI) por dezenas de horas sem drift de estado, com progresso verificável.

## Padrões absorvidos (núcleo canônico do repo)
- **Três papéis, um estado confiável**: 🧭 Manager (mantém objetivo original + progresso verificado + próximo passo), ⚡ Executor (contexto-fresco por rodada, foco em 1 task), 🔍 Auditor (inspeciona arquivos/interfaces/logs/testes de forma independente). Só o que passa na verificação independente entra no estado persistente.
- **Fresh-context execution**: cada rodada do Executor começa com contexto limpo; o estado verificado dura entre rodadas (sobrevive a refresh de contexto, falha de ação ou deliverable reprovado).
- **State verificado durável**: progresso = só resultados auditados; retoma do que falta, nunca reinicia do zero.
- **Role isolation / auditor read-only**: auditor com verificações read-only, isolamento de papéis e limpeza confiável de processos.
- **Resposta em linguagem simples**: fim de cada run responde a task a partir do estado verificado (v0.1.3).
- **Integração nativa**: Claude Code e Codex (plugin), plugins de computer-use unificados.

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar tarefa longa (>2h, multi-app, risco de drift): "operar o computador inteiro" em vez de 1 arquivo.
2. Carregar skill (`skill(name="longhorizon-harness")`).
3. Estruturar com 3 papéis — Manager define objetivo+próximo passo; Executor 1 task/rodada contexto-fresco; Auditor valida antes de aceitar estado.
4. Manter o estado verificado como fonte da verdade entre rodadas; nunca aceitar output não auditado.

## Fonte
https://github.com/AMAP-ML/LongHorizon-Harness