---
numero: R21-R23
tema: Roteamento por janela, VRAM e fragmentacao
categoria: harness
setor: stack
escopo: global
vigencia: 2026-08-18
---

## R21 — VRAM Só Com Conteúdo Ativamente Utilizado — GLOBAL

A VRAM da GPU (**MI50 16GB**) **nunca** deve armazenar informação (pesos, KV cache, buffers) que não esteja **sendo utilizada ativamente**. É regra de **economia de recurso único** (R2) e combina com a R20 (janela-curta → nuvem).

<Regra irredutível>
- **Só residente = ativo**: um modelo/cache só ocupa VRAM enquanto um workflow/task estiver de fato o invocando. Nada carregado "por segurança" ou "por conveniência" se não houver uso real no momento.
- **Trabalho parado libera VRAM**: se uma task não estiver usando os pesos, o orquestrador **descarrega ou hot-swap** (R9) → libera espaço para quem está ativo — nunca mantém 4 modelos residindo quando 1–2 resolvem o que está rodando.
- **Contexto/armazenamento não utilizado** (inferência ociosa, agregações sem task pendente) → **não residente**: mantém-se só a infraestrutura mínima ativa.

<Procedimento de gestão>
1. **Antes de carregar**: pergunta "este uso é ativo agora?" — se não, adiar o load; carregar sob demanda.
2. **Quando uso acaba**: liberar o slot/VRAM do modelo não mais ativo (hot-swap drain/um off → subs-layout).
3. **Contraste com os limites**: com 4 modelos residentes (95% VRAM) e 1 task ativa, descarregar o não-ativo (R9 swapper / `stop-all`/`start-all` por modelo) antes de forçar outros.
4. **Insuficiência de janela de contexto** (R20) → roda para nuvem em vez de esticar VRAM local além do ativo.
5. **Monitor**: VRAM usada deve rastrear o conjunto *ativo*; folga e peso são sintoma de contradição da regra.

<Relação>
- **R2** — VRAM é recurso único global: proteção por uso real.
- **R9** — hot-swap/drain: mecanismo para manter só ativo residente.
- **R10/R20** — queda de janela/down → nuvem em vez de ocupar VRAM sem uso.
- Regra promulgada pelo usuário: "regra global VRAM nunca deve armazenar informação que não esteja sendo utilizada ativamente".

## R22 — Context Window Task Fragmentation & Sequential Merge (Task Manager) — GLOBAL

Camada **fundamental do Task Manager**, executada **antes da seleção do subagente**. Nenhuma tarefa deve falhar exclusivamente por exceder a janela de contexto de um subagente: a tarefa primária é **decomposta → enfileirada → executada → validada → consolidada → retomada**. O tamanho da janela do subagente é **restrição de execução, não limitação da tarefa** (`TASK SIZE ≠ CONTEXT WINDOW`).

<Regra irredutível (invariante)>
> Uma tarefa nunca deve ser descartada por excesso de contexto. Ela deve ser decomposta até que cada unidade seja executável dentro da capacidade do agente, mantendo dependências, estado, validação e ordem de execução; ao final, os resultados devem ser semanticamente consolidados antes da continuação do workflow.

<Fluxo obrigatório>
1. **Estimativa de capacidade**: `available_context = window − system_prompt − agent_prompt − tool_definitions − memory − reserved_output_tokens − safety_margin`. Se `task_tokens <= available_context` → EXECUTAR direto. Senão → `TASK_FRAGMENTATION`.
2. **Decomposição semântica (Fatiador)**: cortar **só em fronteiras estruturais** (fim de blocos lógicos — AST para código, parágrafos fechados para texto), **nunca por contagem matemática de tokens**. Fragmentos autossuficientes com `task_id/parent_task/sequence/objective/inputs/constraints/expected_output/validation/state_from_previous_tasks`.
3. **Envelope de task**: cada fragmento carrega envelope mínimo (YAML/JSON) com dependências explícitas, critérios de validação e `output_artifact`.
4. **Fila cronológica com dependências**: scheduler só executa task cujas dependências estejam `COMPLETED + VALIDATED`. Estados: PENDING→QUEUED→RUNNING→BLOCKED→COMPLETED→VALIDATED→FAILED→RETRYING→MERGED.
5. **Motor de Estado (propagação)**: **nunca passar output bruto** de um subagente ao próximo (estoura a janela em cascata). Passar **Rolling Summary + Vetor de Estado (JSON)** — "metas concluídas, entidades globais ativas, contexto pendente" — e **ponteiros lógicos** ao dado bruto. Contexto progressivo: objective + resultados relevantes + decisões + constraints + estado atual (não histórico bruto).
6. **Checkpoint obrigatório** após cada fragmento: `task_id/status/result/decisions/files_changed/tests/errors/unresolved/next_action` — permite interromper/continuar sem perder estado.
7. **Falha de subtask**: RETRY se possível; **REFRAGMENT se contexto insuficiente** (nunca abortar a primária); BLOCK se dependência inválida.
8. **Consolidação (Reducer)**: merge **semântico**, não concatenação — remover duplicações do overlapping, resolver conflitos, preservar decisões, verificar dependências, reconstruir coesão, validar consistência. Conflito detectado → **registrar** (sources/description/resolution/reason), nunca escolher silenciosamente.
9. **Validação final do merge** → se falhar, resolver conflitos → **RETOMAR WORKFLOW** com o resultado consolidado.

<Arquitetura (abaixo do workflow, nível do orquestrador)>
```
ORCHESTRATOR
   ├── WORKFLOW
   └── TASK MANAGER
        ├── CONTEXT MANAGER
        ├── TASK DECOMPOSER
        ├── TASK QUEUE
        ├── CHECKPOINT STORE
        └── RESULT MERGER
```
Qualquer workflow usa a mesma infraestrutura de fragmentação (reuso, R8/R2).

<Overlapping (margem de sangria)>
Task N+1 herda ~15% final do contexto da Task N (sliding window) para garantir escopo imediato das funções/raciocínios em andamento — e o Reducer remove as redundâncias geradas por essa sobreposição na emenda.

<Relação>
- **R20** — janela-curta → nuvem: a fragmentação R22 roda ANTES (decompõe para caber no subagente); se mesmo fragmentada não couber, aí a rota nuvem (R20) se aplica.
- **R21** — VRAM só uso ativo: fragmentos enfileirados não alocam VRAM ociosa; estado vive em disco (`state/tasks/TASK-N/`), não em VRAM.
- **R13/R17** — roteamento por competência: fragmentos podem ser executados por subagentes distintos conforme capacidade; orquestrador supervisa, executor executa.
- Regra promulgada pelo usuário: "regra global camada fundamental do Task Manager, antes da seleção do subagente. se as tasks não couberem dentro da janela de contexto dos subagentes, fragmentar a task primária até caber dentro da janela de contexto dos subagents e enfileirar as tasks cronologicamente até terminar e fundir tudo novamente e seguir workflow".

## R53 — Auditoria Obrigatória a Cada Update de LLM Local
A cada adição/remoção/alteração de LLM local (path canônico, Ollama, stack), gerar auditoria:
(1) custo de contexto por LLM em GB (pesos + KV no ctx nativo e operacional, VRAM e/ou RAM);
(2) ctx max por LLM (n_ctx_train e ctx configurado); (3) t/s GPU solo e CPU solo (bateria
padrão de 5 testes × 192 tok); (4) t/s simultâneo com outros LLMs menores (degradação % +
throughput agregado). Registrar no ctx-catalog (R27) + wiki/evidence/ do vault.

Template obrigatório:

| Modelo | GB contexto | ctx max | GPU solo t/s | CPU solo t/s | Simultâneo t/s (degrad.) |

Regra em vigor desde 2026-08-18 (pedido do usuário).

## R23 — Roteamento por Janela de Contexto: Local CURTO → Omniroute (janela grande) — GLOBAL

Quando uma delegação **precisa de contexto maior que o suportado** pelo backend local destino (**janela real uniforme R24-categórica = 27.136 p/ todos os 5 locais**, medida 2026-08-10 — R23 media 11.776 com matemática FP16; R24 recalibrou com KV quant real q8_0/q4_0 → 27.136, não usar o `max_context` teórico de 262K), o destino **deve ser omniroute** (gateway cloud, janela grande 262.144), **NUNCA** forçar o local-curto — o que estoura a janela e corrompe a delegação (falha recorrente: "request (N tokens) exceeds the available context size (M)").

Cálculo categórico da janela uniforme (frio, folga ≥ 200 MB; MI50 16GiB) — **R24 recalibrado com KV quant q8_0/q4_0 empírico**:
- orçamento 16 GiB − 200 MiB → alvo `used ≤ 15,78 GiB`
- base 5 servers @2048 (KV VRAM) = **14,05 GiB**
- custo combinado/token extra (5 modelos) = 49.152+98.304+18.432+12.288+10.752 = **188.928 B/tok** (R23 assumiu FP16; R24 mediu o custo real quantizado ~13% do FP16 → janela ~2,3× maior)
- R24 empírico: 5/5 @27.136 → VRAM 15,29 GiB, folga real **0,69 GiB**; prefill 21.6K tok sem OOM; sonda 32.768 → folga 0,24 GiB sob prefill → REJEITADA
- verificado R24: 5/5 healthy @27.136 → **W = 27.136** (múltiplo de 128)
- ⚠️ **KV-spill**: se o decode de LLM Orquestrador/bonsai parecer lento, é o KV realocado para RAM do host sob pressão (comportamento llama.cpp).
- Janelas máximas INDIVIDUAIS (1 modelo por vez, KV 100% VRAM; NÃO simultâneas — somam ~41,7 GiB de KV): LLM Orquestrador 205.000 (53,5 t/s) · bonsai 120.000 (23,2 t/s) · qwen 262.144 nativa · llama 131.072 nativa · deepseek 131.072 nativa. A regra uniforme mantém todos **abaixo** do nativo de cada um.

<Regra irredutível>
- **Gatilho**: `task_tokens_estimated` (ou a delegação já montada) **> janela real disponível do backend local** (`-c` alocado, NÃO o `max_context` teórico). O `-c` real é o limite; `max_context=262144` é só o teto teórico/declarado, irrelevante para rota.
- **Destino obrigatório**: janela insuficiente → **`omniroute`** (priority 60, gateway cloud, janela grande 262.144). **Nunca** `local-orchestrator`/`local-bonsai` para delegação que exige mais janela (forçar local = overflow silencioso / falha do pipeline).
- **Não esticar o local**: a fragmentação R22 divide a *task*; se mesmo assim o fragmento exigir mais do que o suportado OU o trabalho for de análise/geração de código longo, a rota é nuvem (R20/R23), não esticar o local.
- **Só local quando cabe**: `LLM Orquestrador`/`bonsai` para delegações que couberem na janela real; micro-checks, fragmentos curtos → local ok.

<Procedimento de roteamento (quem decide onde)>
1. **Estime** `task_tokens` da delegação (compactor.estimate_tokens ou janela real do backend destino).
2. Se `task_tokens <= janela_real_destino` → **local**.
3. Senão → **omniroute**, com redflag registrada (R10) como aprendizado de roteamento (janela-curta → nuvem).
4. Ao concluir a task → **retorna prioridade ao local** (R21: só residente/ativo; local continua disponível p/ delegações que couberem).
5. Se omniroute também estiver indisponível → StallGuardError (R9 fail-fast <2s) → NÃO tentar local com janela insuficiente.

<Fechamento de lacuna no código (patch aplicado 2026-08-10)>
> **✅ FECHADO**: `ModelInheritance.guarded_resolve` agora é **janela-aware** (R23 implementada).
> - `Backend.context_window` = janela real (`-c` medido via `/props`; config em `harness.model_inheritance.backends.*.context_window`; 0 = desconhecido/ilimitado).
> - `guarded_resolve(resource, category, estimated_tokens=0)` e `resolve(...)` filtram candidatos por `tokens <= context_window`; preferido local que NÃO cabe é pulado na cadeia → omniroute (janela 262144) quando couber; nenhum cabível saudável → `StallGuardError` com hint de janelas (fail-fast R9).
> - Sem `estimated_tokens` (default 0) → comportamento health-only preservado (compat retroativa).
> - Prova: `harness/tests/test_window_routing.py` (9 cenários TDD: pequeno→local, grande→omniroute, bonsai-no-meio, gateway down→StallGuard, janela 0 ilimitada, default compat, override nunca força local-curto, resolve soft-path, parsing config).

<Contingência e relação>
- **R20** — janela-curta → nuvem **até concluir**; R23 é a condição/rota explícita de *destino* (omniroute) aplicada **a cada delegação**. Coerentes: ambos proíbem forçar local acima da janela.
- **R22** — fragmentar primeiro (interior da task); **R23** — se ainda exceder, **destino nuvem**. Duas camadas no mesmo caminho, sem contradição.
- **R13/R9** — roteamento por competência + guarded_resolve: R23 adiciona o critério **janela** ao fallback (hoje só health). Complementa, não conflita.
- Regra promulgada pelo usuário: "regra global se uma delegação precisar de contexto maior que o suportado, o destino deve ser omniroute (janela grande), não local-orchestrator".

### Auditoria de regras contraditórias (pedido do usuário)
- ✅ **R22 × R23**: não contradizem — fragmentação intra-janela (R22), depois rota a nuvem se ainda exceder (R23). Etapas sequenciais no fluxo.
- ✅ **R20 × R23**: R20 descreve a sessão/tarefa inteira, R23 o roteamento pontual da delegação — mesmo princípio (janela→nuvem), R23 é mais fino.
- ⚠️ **R19/R21 × R23**: R21 quer descarregar ociosos (bom); mas se descarregar **todos** os locais, R23 perde a opção "local quando couber". **Não é contradição** — R21 mantém o **ativo** que couber; R23 usa nuvem só para o que exceder o ativo. **Eliminação: nenhuma necessária**; manter R21→R23 complementares via "manter ativo que cabe".

