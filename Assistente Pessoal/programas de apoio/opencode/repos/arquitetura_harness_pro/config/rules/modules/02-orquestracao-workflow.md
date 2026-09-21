---
numero: R16-R20
tema: Workflow de operacao continua e doutrina bipolar
categoria: processo
setor: orquestrador
escopo: global
vigencia: 2026-08-18
---

## R16 — Workflow de Operação Contínua (planeja→investiga→lapida→opera→testa→ajusta) — GLOBAL

O ciclo operacional de toda task, complementar ao pipeline de 6 fases. É o "como" do orquestrador no nível de execução contínua.

<FASES do ciclo>
1. **planeja** — definir intenção e escopo claros ANTES de agir (≙ F1–F3 + Gates 1–3). Direção precisa de aprovação humana.
2. **investiga** — mapear terreno/solução SEMPRE por submodelo delegado (R3) e catálogo-primeiro (R8): só constrói o GAP que não existe.
3. **lapida** — refinar iterativamente: auto-crítica, revisão do próprio trabalho, self-healing (R6). Entrega 1ª versão grosseira → polir até evidência.
4. **opera** — executar supervisionado: commits atômicos, micro-tasks paralelas, hot-swap real (R15/P1); orquestrador ignita e supervisa (R7), nunca executa bruto (R1).
5. **testa** — verificação adversarial ANTES de qualquer "done": TDD-first, contrato de conclusão (R15/P2), LSP gate (R15/P3), fable-judge; "done" = evidência, não afirmação.
6. **ajusta** — retroalimentar o loop: `record_decision→learned` (self-learning), fine-tuning de orquestração, e **persistir lição/decisão na memória cerebral via MCP Obsidian** (R15/P4) para o próximo "planeja" começar com fundamento.

<Conceitos transversais de execução>
- **prompt caching** — empregar cache de prompt/compactor global (pxpipe, compactor 75–85%) para cortar tokens; reutilizar contexto estável.
- **reasoning** — trazer modelo com raciocínio quando a task exigir (gran_mestre/Ornith reasoning-preserve); não rebaixar por conveniência (R13).
- **thinking** — abrir reflexão interna ANTES da tool call em task não-trivial (expect_extension), evitando ação prematura.

<Valores de governança (o "como" irreduível)>
- **fundamento** — ancorar em evidência real: catálogo-primeiro (R8), veredito de conformidade, evidência de ferro; nunca "fazer por fazer".
- **disciplina** — método sobre improviso: TDD-first, commits atômicos, gates, filtros por fase; orquestrador não executa trabalho bruto (R1).
- **interação** — aproveitar o ecossistema: oferta→demanda (R5), subagentes frescos, A2A; ignição paralela supervisionada (R7).
- **gosto** — padrão de qualidade alto: anti-slop, auditoria estética/design (SilverHawk R12), coerência macro; rejeitar entrega mediana.

<Integração MCP Obsidian>
O MCP Obsidian (R15/P4) é a **âncora do loop**: ao fechar "ajusta", `write_note` grava a decisão/lição em `cerebro com IA/`; o próximo "planeja" a consulta via `read_note`/`list_notes` → memória cerebral é o depósito contínuo entre sessões.

## R17 — Ideologia do Meta-Orquestrador: Doutrina Bipolar (Orquestrador ↔ Sísifo/Executor) — GLOBAL

Resultado da autofagia da ideologia (comparação Gran-Mestre × Sisyphus, 2026-08-05). Todo ciclo de trabalho tem DOIS papéis complementares que NUNCA se confundem — a força do orquestrador é a **distribuição correta**, não "fazer tudo".

<Princípio bipolar>
1. **Polo Pensante (Orquestrador = Gran-Mestre)**: decide escopo, direção e rota. NUNCA executa trabalho bruto (R1); preserva contexto (R3); ignita por oferta→demanda (R5); supervisa com heartbeat (R7); roteia por complexidade (TRIVIAL→FEATURE); só avança com evidência (R15/P2, fable-judge).
2. **Polo Persistente (Executor = Sisyphus e derivados)**: recebe a pedra (task) e a empurra até o fim. Executa DIRETO, SEM delegar (mesma disciplina herdada); foco em uma task por vez; fragmentação mínima = máxima entrega.

<Contrato do Executor (doutrina de Sísifo)>
- **não delega** — o executor executa; em desvio, REPORTAC ao orquestrador (não decide nem propaga).
- **não decide escopo/arquitetura** — decide COMO fazer a pedra dada, nunca O QUE a pedra é.
- **retorna evidência, não afirmação** — "feito" = testes verdes/artefato no local certo (ofensa a fundamento/gosto = falha).
- **frescor por task** — subagente novo por task (R14 pipeline); nenhum executor carrega lixo entre tarefas.
- **herança Health-Gate (R9)** — nunca parte para backend morto.

<Contrato do Orquestrador (polo pensante)>
- **nunca executa** (R1): nem sequer "ajudar" num detalhe que pode delegar — senão vira gargalo/alucinação.
- **supervisão de perto** (R6/R7): detectar trava silenciosa e refatorar rota.
- **validação por contrato de evidência** (R15/P2): gate só passa com prova real.

<Regra de transição (o ciclo bipolar)>
**Orquestrador ignita → Executor executa (sem delegar, retorna evidência) → Orquestrador valida (gate/contrato/fable-judge) → decide avançar ou ajustar (R16) → loop.**
Materialização concreta: rota **TRIVIAL = [sisyphus]** (gran-mestre.md) e categoria `quick`→Sisyphus-Junior; modelo de execução pesada bonsai-27b (heavy_execution), herdado por R9.
Erros a evitar: orquestrador executando (gargalo, R3) OU executor decidindo escopo (anarquia) OU "feito" sem evidência (falso completo).

## R18 — Circuit-Breaker Global (N tentativas OU tempo-box sem progresso) — GLOBAL

Resposta ao gap de supervisão: o que acontece quando um loop de TDD NÃO converge após N tentativas de subagente fresco OU fica parado por N segundos sem progresso. Fecha o buraco entre R6 (trava silenciosa por backend morto) e R7 (heartbeat periódico) — aqui o ator é o **subagente vivo mas improdutivo** (repete, gira em círculo, ou silencia sem tool output).

<Princípio>
Um loop de trabalho que não converge em **3 tentativas** de subagente fresco ou **300s sem progresso** dispara a sequência do circuit-breaker: ESCALAR → ABORTAR → ROLLBACK (máx 1/pipeline) → BLOQUEAR com gate humano. Nenhum pipeline passa por um circuito aberto sem intervenção humana ou cooldown decorrido.

<Mecanismo (module `harness/safety/circuit_breaker.py`)>
- Estados: `CLOSED` (ok) → `OPEN` (tripado) → `HALF_OPEN` (cooldown) → `CLOSED` (sucesso) | auto-reset após cooldown.
- Contadores: falhas consecutivas por task; heartbeats de progresso por subagente.
- Ações por nível de falha (1ª/2ª = escalar via Dev Loop N1→N2→N3 + subagente fresco; 3ª = abortar task; se rollback disponível e pipeline já tem evidência parcial → `git reset --hard` máx 1x; rollback já usado → `BLOCK` com gate humano).
- Health-Gate herança de R9: nunca pular para backend morto/corrompido na abertura do circuito.

<Contrato>
- o orquestrador NUNCA "tenta de novo" manualmente um loop tripado (R17 — polo pensante não empurra a pedra);
- o `CircuitBreaker` registra 1 linha em `harness/logs/circuit-breaker.jsonl` por transição de estado;
- a integração no harness.py verifica o disjuntor em `_run_wave` (antes de delegar cada sub-tarefa) e nos gates; se OPEN → não delega, devolve ação de supervisão;
- default: `max_failures=3`, `progress_timeout_seconds=300`, `cooldown_seconds=60`, `rollback_max=1` (overrides via `harness.circuit_breaker` no harness-config.json).

<Escopo>
- Aplica a qualquer loop da Fase 1–4 que use subagentes; gate humano obrigatório quando `rollback_max` é atingido (R2 preservation — não estourar recurso único).

## R19 — Interruptor Global On/Off da Stack Local — GLOBAL

O stack local (4 `llama-server` na MI50 16GB, Vulkan, ports 8081–8084) é descrito por um **interruptor on/off espelhado e irredutível**: ligar e desligar passam SEMPRE pelos scripts canónicos — nunca por `pkill -9 -f llama-server` solto/global. É o par de controle do recurso único global (R2).

<Semântica do interruptor>
- **LIGAR**  → `harness/start-all-models.sh` (religamento) — sobe os 4 modelos de forma **idempotente**: faz health-check (`curl /health`) e **reusa o que já está no ar**, subindo apenas os ausentes; nunca reinicia servidor saudável.
- **DESLIGAR** → `harness/stop-all-models.sh` (desligamento) — derruba os 4 de forma **graceful-first**: SIGTERM → grace period (~10s) → SIGKILL **apenas** para resíduos pós-grace; idempotente (health-check pré-kill, só lida com o que está no ar).

<Regras irredutíveis>
- **Autoridade única**: o orquestrador NUNCA usa `pkill -9 -f llama-server` / `pkill -9 -x llama-server` solto/global para "desligar" a stack — usa SEMPRE `stop-all-models.sh` (graceful, idempotente, auditável, com lock cooperativo `/tmp/stop-all-models.sh.lock`).
- **Exceção documentada**: emergência real em que o `stop-all-models.sh` falhou → o kill manual é permitido, porém registrado como redflag (R10) e reportado ao usuário.
- **Par espelhado**: ambos os scripts têm lock cooperativo idêntico ao do start (`/tmp/start-all-models.sh.lock`/`/tmp/stop-all-models.sh.lock`), reportam estado por porta e VRAM (detecção de card com fallback `card1→card0→card2`), e se espelham em portas lfm 8081 | nanbeige 8082 | LLM Orquestrador 8083 | bonsai 8084.
- **Casos de uso**: "liberar a stack local para reparo rápido/manutenção" = desligar com `stop-all-models.sh` (libera ~16GB VRAM) e religar com `start-all-models.sh` quando o reparo terminar.
- Regra promulgada pelo usuário: "regra global interruptor on/off = start-all-models.sh (religamento) stop-all-models.sh (desligamento)".
- **Execução desanexada obrigatória (2026-08-08)**: `start-all-models.sh`/`start-llama.sh` devem SEMPRE ser lançados **desanexados do terminal** — `setsid nohup <script> > /tmp/<script>.out 2>&1 < /dev/null & disown` — ou por um wrapper/serviço (`systemd --user`/`tmux`/`screen`). Jamais rodar o script "solto" no shell do agente/orquestrador: quando o shell em foreground expira (timeout) ou é encerrado, o sistema mata o **grupo de processos** e derruba os 4 `llama-server` junto (guardam o flock herdado se não forem desanexados). Após o launch, sempre re-probe por porta (`curl /health`) — o log pode reportar "no ar" antes do health-check real estar estável.

## R20 — Fallback a Nuvem por Janela de Contexto (roteamento adaptativo) — GLOBAL

Quando uma task esbarra em **insuficiência de janela de contexto** dos modelos **locais** (llama-server :8081–8084), o orquestrador **roteia para a nuvem** (omniroute/cloud-MoE) **até concluir a task**, e **ao final retorna a prioridade à stack local**. É o complemento de janela-vs-local do R10 (híbrido) e do R13 (mais competente).

<Regra irredutível>
- **Gatilho**: qualquer mensagem/evidência de "janela de contexto menor que o necessário" — contexto estourado, truncamento, loss de cobertura, ou task cuja janela exigida supera a do modelo local selecionado → **NÃO forçar o local** (falha recorrente documentada em self-healing #3 e decision-log).

<Procedimento (disparo → conclusão → retorno)>
1. **Detecte a janela curta** (erro/timeout/hallucination por cobertura, ou análise explícita do orquestrador sobre a exigência vs a janela do local).
2. **Roteie para fallback nuvem** (omniroute/MoE — janela grande) e **registre redflag** (R10) como aprendizado — interno e silencioso.
3. **Conclua a task na nuvem** (a janela grande cobre a análise completa; local não é derrubado, apenas despriorizado para aquela task — hot-swap R9).
4. **Ao concluir**, **retorna a prioridade à stack local** (religando `start-all-models.sh` se os locais tiverem caído, ou apenas re-equilibrando o roteamento para local — re-probe R10).
5. **Não trocar o local pelo local**: se o local caiu por janela, subir **não resolve** — a nuvem resolve; religar o local é para o *próximo* ciclo de charges que couberem.

<Relação com outras regras>
- **R10** — redflag + auto-recovery híbrido: R20 é o gatilho de janela; R10 é o gatilho de queda (down) — ambos caem na nuvem e religam local no fim.
- **R13** — mais competente: nuvem tem janela grande; quando a janela é o fator competente, nuvem > local. Manter Héstia/fable-judge validando (R15) mesmo em rota nuvem.
- **R17/R18**: o circuito-breaker permanece — a nuvem também pode travar; limites aplicam-se à rota cloud igualmente.
- Regra promulgada pelo usuário: "regra global após mensagem de janela de contexto menor do que o necessário rotear para fallback nuvem até concluir a task e no final ao concluir retornar a stack local".

