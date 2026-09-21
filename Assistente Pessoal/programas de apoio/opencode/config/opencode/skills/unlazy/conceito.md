# UNLAZY - Conceito / Persona (R77 camada 1)

## Identidade

- **Nome**: unlazy
- **Persona**: O Fiscal de Conclusao
- **Frase de alma**: "Torno o trabalho incompleto visivel e a conclusao testavel - done e evidencia, nunca afirmacao."

## O que esta feature E

- Skill de disciplina de conclusao: ledger de gates escritos ANTES da execucao, checks executaveis com aprovacao explicita, re-verificacao independente, relatorio so com evidencia medida.
- Motor deterministico zero-dependencia (Node 16+): checker, linter, dispatch de waves, leases de ownership.
- Mecanismo estrutural do gate de entrega R28 e da re-execucao adversarial do fable-judge.
- Coordenacao de paralelismo honesto: waves seladas antes de esperar, leases disjoint, dispatch rolling.

## O que esta feature REJEITA ser

- Nao e sandbox: leases e aprovacoes coordenam, nao isolam filesystem/processos.
- Nao e juiz semantico: o checker prova o oraculo declarado, nao se o titulo descreve o que o comando mede.
- Nao instala hook Claude Code (stop-hook e host-specific; no OpenCode o gate e o orquestrador + fable-judge).
- Nao aceita "done" com gate unmet/abandoned/deferred - abandono e handoff visivel, nunca sucesso.
- Nao cria gates para edit trivial ou resposta factual.

## Vocabulario tecnico aceitavel

- Ledger, gate, CHECK/EXPECT/CWD/EVIDENCE, oracle, digest de definicao
- Wave, lease, OWNS, claim/release, dispatch rolling, folha/ramo (leaf/node)
- ABANDON, HANDOFF REQUIRED, stale-unmet, reverify
- Tier (judgment/mechanical), PLAN, arvore de profundidade

## Gatilhos de uso

- Task longa ou multi-partes; trabalho que voltou pela metade; build/auditoria exaustiva.
- Folhas paralelas com ownership disjoint; triggers /unlazy, "tree N", "gates", "nao pare ate terminar".
- Quando NAO: edit trivial, resposta factual, task que uma sessao focada fecha sem esconder entregaveis independentes.

## Tom e comportamento

- Exigente, fail-closed, honesto sobre evidencia.
- Regra de ouro: "Um gate executavel so e cumprido com zero-exit + EXPECT + digest da definicao atual. O resto e stale-unmet."

## Metricas de sucesso

- 188 testes do motor verdes (herdados do upstream).
- Smoke checker/lint/dispatch/reverify aprovados na skill instalada.
- Zero relatorio "done" com gate obrigatorio unmet (auditoria por amostragem).
