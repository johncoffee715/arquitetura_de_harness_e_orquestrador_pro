---
name: modo-autonomo
description: Modo de execução autônoma do orquestrador — quando ATIVO, age sem intervenção do usuário (gates auto-aprovados, retry e escalação automáticos), pausando SÓ por conclusão, intervenção do usuário, circuit-breaker ou operação irreversível.
version: 2.0.0
triggers: ["modo autônomo", "modo autonomo", "autonomous mode", "sem intervenção", "sem intervencao", "dev loop", "cloud-direct"]
rule: R89
---

# Modo Autônomo — execução sem intervenção

> Quando ATIVO, o orquestrador **age, não pergunta**. Gates viram carimbos automáticos,
> retry/escalação rodam sozinhos, amadurecimento loopeia até done. Pausa SÓ em 4 casos.

## 1. Estado (fonte única)

`opencode/state/modo-autonomo.json` — `{"ativo": false}` por padrão (fail-closed).
Ativação SOMENTE por ordem explícita do usuário ("ativa modo autônomo" + escopo).
Nenhum subagente, hook ou modelo ativa sozinho.

## 2. Loop autônomo (quando ativo)

```
planeja → executa (cloud-direct; delegação só se transporte saudável) →
testa (evidência fresca R29) → passou? done : corrige (packet ajustado, ciclo ≤1+2 retries R18) →
falhou 3×? escala modelo/camada : parqueia task como failed e SEGUE p/ próxima →
pipeline sem pendências executáveis? done geral.
```

- Gates G1–G3: **auto-aprovados com registro** (`[Authorize] auto — modo autônomo`).
- R88 (refutação) CONTINUA valendo: refuta antes, mas o veredito vira ação imediata
  sem perguntar (sustenta→não executa+registra; cai→executa).
- Amadurecimento: loop R16 completo por task sem pedir nada no meio.

## 3. Pausas (as ÚNICAS 4)

1. **Conclusão** — done com evidência (R29) + relatório + memorial.
2. **Intervenção do usuário** — qualquer mensagem tua pausa na hora (flag segue ativa;
   "desativa" desliga o modo).
3. **Circuit-breaker OPEN** — task parqueada como `failed`, pipeline segue nas demais;
   ABORT TOTAL só com rollback R18 + gate humano (inalterado).
4. **Operação irreversível** — `rm -rf`, `trash --empty`, `git reset --hard`, matar o
   :8083 (substrato próprio), sudo/senha: NUNCA automáticas — pedem humano sempre.

## 4. Proibições (mesmo ativo)

- Delegar para transporte morto 3× (padrão de circuito → rota cloud-direct, R6).
- Editar fora de governança/skills sem R88 prévia.
- "Aprovação por cansaço" (R40): impressão real ou não-done.
- Ativar-se sozinho ou estender o próprio escopo.

## 5. Observabilidade

Toda decisão autônoma gera linha `[Authorize] auto` + `[RunID]` no CONTEXT e no
decision-log. Modo ativo aparece em cada relatório (`modo: autonomo ON/OFF`).

## 6. Desativação

"desativa modo autônomo" / conclusão geral / intervenção com ordem contrária.
Desligar = estado volta a HITL total, sem resíduo (flag `false` + linha de log).

## 7. Anti-intervenção (curar o prompt recorrente — forja Hefesto 2026-09-06)

> Causa-raiz auditada: o `Permission required` NÃO vem do `opencode.jsonc`
> (bash `*` = allow nas duas árvores) nem do guard-gap-p5 (só trava destrutivo) —
> vem da camada de aprovação da sessão externa, que nenhum arquivo interno silencia
> unilateralmente. O que esta skill controla: nunca emitir forma nova de comando
> (forma nova = prompt novo).

1. **Padrões fixos**: shell autônomo USA SOMENTE os templates em `allow_patterns`
   do gabarito (launch/health/smoke/probe/VRAM/ps). Forma fora do template = violação.
2. **Trilha por comando**: cada lote carrega `[Authorize] auto — modo autônomo`
   no texto + decision-log (ask→auto com trilha, precedente 2026-09-05).
3. **Rito de aprovação única**: primeira aparição de um padrão, o usuário aprova com
   "sempre permitir"; repetição do padrão não re-prompta. Nunca reescrever o comando
   só p/ variar (variação = novo prompt).
4. **Fallback python**: op de arquivo que o bash travar vai via `python3`
   determinístico (precedente mkdir doom/public), nunca insistência cega.
5. **Honestidade R40**: aprovação por cansaço NÃO conta — prompt persistente no
   mesmo padrão = bug da camada externa: registra, reporta, não finge.

## 8. Cobertura total anti-prompt v1.2 (forja Hefesto 2026-09-06)

> Quando o modo está ON, **todo e qualquer** shell roda sem intervenção: o agente
> impõe o auto-gate abaixo ANTES de emitir o comando. Prompt em padrão coberto =
> falha do agente (forma errada), nunca do usuário.

1. **Auto-gate de forma**: o comando SÓ sai se casar byte-a-byte um template de
   `allow_patterns` (porta/flags/valores podem variar; ESTRUTURA não). Sem match ⇒
   o agente reformula sozinho, nunca emite e espera o usuário salvar.
2. **Formas proibidas**: `rm -f/--force` · `>` fora de `> /tmp/opencode/slot-*.log`
   em launch desanexado · `tee` · `sed -i` · `dd` · `pkill -f` · `pgrep -f` SEM o
   truque `[l]lama` (self-match mata PID errado — bug real 06/09) · pipes novos
   fora dos templates. File-op vai por Read/Edit/Write, nunca shell.
3. **Regra pgrep**: SEMPRE `pgrep -f "[l]lama-server[.]real.*--port <P>"` (colchete
   impede self-match); duplo holder se verifica via `ss -ltnp` (fonte única de
   verdade), nunca via pgrep sozinho.
4. **Ritual prompt-resistente**: se prompt aparecer em padrão coberto, NÃO reemitir
   variantes (cada reemissão = prompt novo): aguarda a aprovação existente, registra
   o padrão como `prompt-resistente` no decision-log e segue o pipeline no resto.
5. **Prova por padrão**: 3 execuções do mesmo template sem prompt = padrão estabilizado.

## 9. Dev Loop Cloud sem interrupções (forja Hefesto-cloud 2026-09-11)

> Quando ON + `cloud-direct`, o loop **não pede nada no meio**. Só para no extremo (§3 + §10).

1. **Roteamento cloud-total**: features/execução vão SEMPRE p/ categoria cloud (`omniroute`/LLM cloud atual). Slots locais (`:8083-:9093`) em bypass até health 5/5 fora do caminho crítico. `local-orchestrator/orchestrator` é DISJUNTOR ABSOLUTO p/ feature (R93).
2. **Hefesto-cloud**: forja/execução pesada via Hefesto com motor cloud (janela grande R20/R23). Transporte local morto 1× = sem retry cego (R6/R89): cai p/ cloud e segue.
3. **Gates auto-carimbados**: G1-G3 viram `[Authorize] auto — modo autônomo (cloud)` + `[RunID]` + `[Budget]` no CONTEXT e decision-log. R88 continua: refuta antes, veredito vira ação imediata (sustenta→não executa+registra; cai→executa).
4. **Ciclo por task**: `planeja → executa (cloud) → testa (evidência fresca R29) → passou? done : corrige (packet ajustado, ciclo ≤1+2 R18) → 3× sem convergir? escala camada → parqueia como failed e SEGUE p/ próxima`. Pipeline só termina sem pendências executáveis.
5. **Proibido no meio**: pergunta de permissão, gate humano, re-confirmação de ordem expressa, "aprovação por cansaço" (R40).

## 10. Long-loop horas/dias + auto-amadurecimento (parada só no extremo)

1. **Checkpoint por volta**: `task_id/status/result/decisions/files_changed/tests/errors/next_action` em CONTEXT + decision-log. Interromper/continuar sem perder estado.
2. **Anti-stall**: heartbeat ~1min (R7); 300s sem progresso ou 3º ciclo acumulado = CB (R18): compensações primeiro, `failed` no log, pipeline segue nas demais; ABORT TOTAL só com rollback + gate humano.
3. **Estado em disco, não em VRAM/janela**: fragmentos enfileirados, rolling summary + ponteiros (R22). Janela do GM preservada: só gates/resumos (R70).
4. **Paradas extremas (únicas)**: conclusão com evidência · intervenção explícita sua · CB OPEN sistêmico que impeça/retarde · operação irreversível (deny §4, pede humano sempre).
5. **Observabilidade**: cada volta carimba `modo: autonomo ON (cloud)` nos relatórios.
