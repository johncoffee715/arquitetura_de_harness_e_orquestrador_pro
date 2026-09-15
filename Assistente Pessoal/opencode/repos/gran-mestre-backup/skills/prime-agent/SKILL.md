---
name: prime-agent
description: "Agente RLM self-improving: contexto como variável, tools como funções, subagents recursivos, harness contínuo com estado durável, IPython persistente. (absorvido de PrimeIntellect-ai/prime-agent)"
origin: absorvido:PrimeIntellect-ai/prime-agent
metadata:
  autofagia: PrimeIntellect-ai/prime-agent (2026-08-10)
  prioridade: 8
  linguagem: TypeScript
  topics: rlm, recursive-language-model, continual-harness, ipython, self-improving, coding-agent
  artefatos: skill
  padroes_absorvidos: 8
---
# Prime Agent

Helenizado de [`PrimeIntellect-ai/prime-agent`](https://github.com/PrimeIntellect-ai/prime-agent) (docs: primeintellect.ai/blog/prime-agent + RLM: primeintellect.ai/blog/rlm + Continual Harness: arXiv 2605.09998).

## Propósito
Agente de código e pesquisa **open-source, self-improving**, para trabalho geral e long-running. Estruturado em duas abstrações: **RLM** (Recursive Language Model — contexto como variável, `prompt-as-a-variable`) e **Continual Harness** (estado durável com prompts suplementares, memórias, descrições de skills e specs de subagentes refináveis com updates pequenos e baseados em evidência).

## Padrões absorvidos (núcleo canônico do repo)
- **Contexto como variável (RLM)**: o contexto vive em REPL persistente (IPython), não no prompt — o modelo inspeciona só o que precisa.
- **Tudo programático**: IPython persistente é a tool embutida; operações de arquivo, shell, tools, subagents e gestão de contexto via código.
- **Subagents recursivos nativos**: `rlm(...)` spawna agentes filhos reais (paralelo/background) e retorna resultados programaticamente.
- **Harness que melhora**: `/refine` revisa a trajetória e aplica updates pequenos baseados em evidência ao estado suplementar; nunca reescreve o base system prompt (imutável) e snapshots permitem rollback.
- **Skills como pacotes importáveis**: skills são pacotes Python; skill creator embutido converte workflows recorrentes em skills de projeto/pessoais.
- **Daemon-backed**: sessões continuam em background com terminal desconectado, reatacháveis.
- **Compaction automática + persistência**: goals persistentes, heartbeats, schedules, modo autônomo, subagents retidos — progresso preservado entre turns e terminais.
- **Separação de processos**: worker/kernel em processos separados para isolamento de lifecycle/falha (não sandbox de segurança — mesmas permissões).

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar tarefa longa/autônoma que precisa sobreviver a turns e sessões (mixed coding+research).
2. Carregar skill (`skill(name="prime-agent")`).
3. Aplicar: contexto em REPL/variável (não prompt), subagentes via chamada recursiva, harness durável com refine baseado em evidência, skills como código importável.
4. Para melhoria contínua: `/refine` com updates pequenos + snapshot p/ rollback; nunca editar o system prompt base.

## Fonte
https://github.com/PrimeIntellect-ai/prime-agent