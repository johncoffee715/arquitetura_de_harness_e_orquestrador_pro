---
name: unlazy
description: "Disciplina de conclusao para trabalho substancial de agentes: ledger de gates escritos ANTES da execucao, checks aprovados e executaveis, re-verificacao independente e relatorio so com evidencia. Use em tasks longas/multi-partes, trabalho que voltou pela metade, builds/auditorias exaustivas, folhas paralelas, ou triggers /unlazy, 'tree N', 'gates', 'nao pare ate terminar'. Helenizado de Leonxlnx/unlazy (MIT) - motor zero-dependencia Node 16+ preservado byte-a-byte; adaptacao OpenCode (R77 triplice, R75 categoria, R28 gates categoricos)."
mode: skill
tags: "unlazy, gates, ledger, conclusao, evidencia, re-verificacao, anti-falso-completo, orquestracao, paralelismo, leases, dispatch"
origin: "helenizado:Leonxlnx/unlazy@1667149 (MIT) - decompilacao 2026-09-09, 188 testes verdes, smoke checker/dispatch/reverify aprovado"
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-09-09
  author: Gran-Mestre (Hefesto forja)
  source_repo: https://github.com/Leonxlnx/unlazy
  source_commit: 16671491f6679ad9378f52604d3bc2415b4120c7
  license: MIT
  r77_triple: true
  r75_category: "metodologia"
---

# Unlazy - Disciplina de Conclusao com Gates Executaveis (helenizado)

Tornar trabalho incompleto VISIVEL e conclusao TESTAVEL. Provar resultados contra um ledger em vez de confiar num "done" confiante. Converge com: gate de entrega do Gran-Mestre (R28), fable-judge (re-execucao adversarial), anti-lixo gate (escrita real vs afirmacao).

## Escreva os gates ANTES do trabalho real

Para trabalho solo, crie `GATES.md` a partir de `templates/gates-leaf.md` antes de implementar. Um resultado observavel por gate. Todo gate executavel recebe `CHECK:` e `EXPECT:` indentados; gate manual so quando nenhum comando decide o resultado.

`CHECK:` e CODIGO. Antes de executar um ledger herdado, parseie sem rodar nada e leia cada comando e script chamado:

```text
node <skill-dir>/scripts/gate-check.mjs --status GATES.md
```

Aprove so comandos que voce escreveu ou entende, entao execute explicitamente:

```text
node <skill-dir>/scripts/gate-check.mjs --approve GATES.md
```

Aprovacoes vivem em `~/.unlazy/approved` e vinculam ledger, gate, comando, expectativa, CWD resolvido, shell, timeout, limites de output/regex, plataforma e PATH herdado completo. Mudou qualquer entrada vinculada -> aprova de novo. Leia `SECURITY.md` do repo-fonte antes de rodar checks de repositorio nao-confiavel.

Um gate executavel so conta como cumprido quando: processo sai com zero, `EXPECT:` casa com o output combinado, e a evidencia automatica carrega o digest da definicao versionada. Evidencia ausente/pendente/antiga/desalinhada = NAO cumprido ate a definicao atual passar.

Gate impossivel NUNCA e removido silenciosamente: `ABANDON: <id> <motivo>` - abandono e terminal mas NUNCA conclusao bem-sucedida (checker sai 1 com `HANDOFF REQUIRED`).

## Escolha o menor modo que serve

- **Solo**: um `GATES.md` para task focada de uma sessao.
- **Orquestrado**: para build/revisao profunda, leia `references/method.md`, `references/orchestration.md`, `references/dispatch.md`. Contrato e arvore ANTES do fan-out. Ledger proprio por folha e por ramo.
- **Paralelo**: antes de despachar folhas concorrentes, leia `references/parallel.md`. Reconcilie igualdade de conjuntos entre `Owns` do PLAN e `OWNS:` do ledger antes de `READY` e de novo antes de claim. Waves de dispatch; lease da folha liberada so apos verificacao do pai.

## Construa a Arvore de Profundidade

1. Releia o pedido original e emendas. Inventarie todo resultado independentemente omitivel em `PLAN.md` antes de dividir.
2. Divida em fronteiras naturais de task. Profundidade so enquanto cada folha permanece entregavel coerente.
3. Cada folha: contrato estreito, ownership exato de arquivos, ledger proprio.
4. Cada ramo: gates de integracao (verificacao dos filhos, compatibilidade de interface, comportamento end-to-end, regressoes).
5. Despache so folhas com dependencias verificadas e ownership claimado. Wave aberta -> todos os launches -> wave selada -> so entao espere resultado.
6. Re-execute os gates de cada folha retornada com `--reverify`; `--status` NAO e re-verificacao.

Dispatch rolling: folha verificada e lease liberada destrava a proxima -> abra e lance a proxima wave sem esperar trabalho nao-relacionado em voo.

## Trabalhe cada folha em 4 passadas

1. Implemente o entregavel completo. Sem placeholders, sem resto adiado.
2. Releia como especialista do dominio e substitua a versao barata de cada parte.
3. Cace defeitos de correcao, integracao, portabilidade, performance e evidencia. Corrija o que achar.
4. Aplique polimento de baixo custo; repita ate uma passada completa nao achar nada.

Folha so termina com passada limpa e todo gate cumprido com evidencia.

## Gates que podem falhar honestamente

O checker prova so o oraculo declarado - nao infere se o titulo descreve o que o comando mede.

- Token de sucesso decisivo; exija zero-exit E `EXPECT:`.
- Exercite check negativo contra controle positivo conhecido antes de confiar em ausencia.
- Meca numeros independentemente; nao copie numero fornecido para dentro do `EXPECT:` como propria prova.
- Prefira scripts Node portateis (nao assuma `grep`/`tail` no Windows).
- Re-execute com o mesmo shell e toolchain declarados. Ambiente diferente = verificacao falha, nao evidencia.
- Linte o ledger antes de trabalhar:

```text
node <skill-dir>/scripts/gate-lint.mjs GATES.md
```

## Audite o relatorio final

Releia o pedido atual, reconcilie contra o inventario do PLAN, re-meca todo numero e claim de conclusao imediatamente antes de reportar. Use ids qualificados (`leaf-1.2.1:G3`). Reporte contagens medidas de met/unmet/abandoned e surface todo abandono. NAO componha relatorio "done" com gate obrigatorio unmet/abandoned/deferred.

## Integracao com o harness (helenizacao)

- **Gate de entrega R28**: um pipeline pode usar unlazy como mecanismo estrutural do gate - o ledger E o acceptance_criteria executavel.
- **fable-judge**: `--reverify` e a re-execucao adversarial; unlazy a torna deterministica e barata.
- **Stop hook**: o hook original e Claude Code-specific (`decision: "block"`). No OpenCode, o equivalente e o gate de entrega do orquestrador + fable-judge - NAO instale o hook Claude (scripts/install-hooks.mjs e stop-hook.mjs ficam fora desta skill de proposito).
- **Dispatch**: `dispatch-check.mjs` registra waves; o launch nativo no OpenCode e a tool `task` (subagentes frescos por folha, R17). Registre o task_id retornado como `--handle`.
- **Leases**: `OWNS:` + `--claim`/`--release` coordenam folhas paralelas - complementa o zero-trust/downscope do Task Packet (nao substitui: lease e coordenacao, nao sandbox).

## Gaste atencao onde composta

Briefing de folha = contrato + um ledger. Append de status em vez de reescrever historia. Marque `Tier` no PLAN: `judgment` quando o artefato da folha precisa de design/revisao; `mechanical` so quando padrao e gates ja fixos. Tier e metadata de planejamento, nao garantia de roteamento.

NAO crie gates para edit trivial ou resposta factual. Use esta disciplina quando o custo do incompleto silencioso justifica o ledger.

## Triplice R77 (referencia)

- **conceito.md** - ontologia/persona (o que a feature E e REJEITA ser).
- **gabarito.json** - firewall (allow/deny; fonte unica p/ Pydantic/GBNF).
- **mecanica.md** - ignicao (sequencia, sampling, enforcement).

## Licenca e provenance

MIT (c) Leonxlnx (LICENSE incluido). Motor (`scripts/`) preservado do upstream commit `1667149` - zero dependencias, Node 16+. Adaptacao pt-BR + integracao harness: Gran-Mestre, 2026-09-09.
