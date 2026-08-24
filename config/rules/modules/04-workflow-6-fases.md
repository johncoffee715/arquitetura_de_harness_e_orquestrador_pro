---
numero: R25-R28
tema: Workflow 6 fases, memoria Obsidian, sync e transitio
categoria: processo
setor: orquestrador
escopo: global
vigencia: 2026-08-18
---

## R25 — Workflow Gran-Mestre 6 Fases via ArsenalScaffold (modular, self-learning) — GLOBAL

O orquestrador (Gran-Mestre) **sempre** gerencia/orquestra/modifica/julga/adapta/manipula o workflow do harness via `ArsenalScaffold`, de forma modular e autônoma, usando **todos os modelos disponíveis** (5 locais + cloud) e **todos os itens do arsenal** (plugins, subagentes, hooks, skills, MCPs, tool-callings, LSPs), conforme o template:

<Regra irredutível>
- **Loop externo obrigatório (6 fases)**: F1 Descoberta → F2 Contrato → F3 Plano → F4 Execução → F5 Revisão Macro → F6 Entrega.
- **Cada fase = filtros + brainstorm de agents + gate**: escopo/ambiguidade/cobertura/evidência (filtros), brainstorm multi-agents (arquitetura/cobertura/qualidade), gates G1-G4 de aprovação do usuário (direção, spec, plano, relatório final).
- **F1-F3 não tocam código produtivo**: F1 Descoberta (escopo, ambiguidade, decomposição leve, brainstorm) → G1; F2 Contrato (design doc, SPEC.md, validação vs pedido original, brainstorm) → G2; F3 Plano (TDD tasks bite-sized, decomposição por registro de arsenal, brainstorm valida cobertura/verificabilidade) → G3 + **SHA salvo**.
- **F4 Execução**: sem gates — supervisão/sequência de tasks, commits atômicos, subagentes frescos por task + plugins/hooks/skills/MCPs/LSPs, ciclo de vida de cada recurso, TDD por task, evidência de verificação por task, revisão micro por task.
- **F5 Revisão Macro**: diff total holístico (coerência cross-task, acoplamento), auditoria vs critérios de qualidade, brainstorm de arquitetura e alinhamento com contrato.
- **F6 Entrega**: evidência fresca de ferro, validação final vs pedido original, veredito final, brainstorm de conformidade → **memória cerebral Obsidian** → G4.
- **Self-learning contínuo**: orquestrador otimiza a si mesmo a cada ciclo (decision-log, scores adaptativos R10, oferta-demanda do scaffold, fine-tuning do oráculo).

## R26 — Memória Obsidian para TODOS os modelos (trigger curto, janela preservada) — GLOBAL

Promulgada 2026-08-11 (autofagia global / pedido do usuário). O cérebro Obsidian
(`/mnt/dados/cerebro com IA`) NÃO é privilégio do Gran-Mestre — qualquer modelo,
em qualquer instância, pode consultar memória de longo prazo.

<Regra irredutível>
- **Acesso universal**: TODOS os modelos/agentes têm acesso ao vault via skill
  `memory-recall` (trigger: prefixo de turno `memória: <tema>` ou perguntas de
  retomada "o que já fizemos?", "lembra de...", "contexto anterior").
- **Janela preservada**: o bloco de memória injetado é SEMPRE curto (≤ 200
  tokens) — referência de trigger, nunca dump de arquivos inteiros do vault.
- **Hook automático**: `session.start` roda `harness/hooks/memory_inject.py`
  (registrado em opencode.json) — injeta índice do cérebro + estado do pipeline
  + aprendizados recentes no início de cada sessão, com falha silenciosa.
- **Escrita disciplinada**: escrita/atualização do vault segue o fluxo de
  ingestão Obsidian (memory-keeper), nunca escrita ad-hoc desestruturada.
- **Fontes em ordem**: `wiki/index.md` → `pipeline/contexto-atual` →
  `aprendizados/` → `decisoes/` → profundidade sob demanda (Read com offset).
- **Nunca inventar**: consulta vazia responde `[MEMORIA] sem registros para
  "<tema>"` — jamais fabricar memória inexistente.

<Artefatos>
- Skill: `~/.opencode/skills/memory-recall/SKILL.md` (protocolo de consulta).
- Hook: `harness/hooks/memory_inject.py` + registro `hooks.session.start` no
  opencode.json.
- Camada vetorial complementar: skill `memory-local` (mem0 helenizada).

## R27 — Sincronização ao agregar/alterar modelo LLM local (5 arquivos + re-probe) — GLOBAL

Promulgada 2026-08-11 (autofagia global / pedido do usuário). Adicionar um novo
modelo local (ou mudar porta/ctx/janela) exige atualização coordenada em TODOS
os pontos de verdade — um só desatualizado quebra o harness silenciosamente.

<Regra irredutível>
- Ao agregar/alterar modelo local, atualizar OBRIGATORIAMENTE:
  1. `harness/ctx-catalog.json` — catálogo de janelas/portas (fonte de R23/R24).
  2. `~/.config/opencode/opencode.json` — provider + model + baseURL + limit ctx.
  3. `~/.config/opencode/oh-my-openagent.json` — remapeamentos de agentes/roles.
  4. Scripts de subida: `start-all-models.sh` / `stop-all-models.sh` (R19) —
     porta, modelo, args (--ctx-size, --parallel, --backend vulkan).
  5. `harness/llama_budget.py` — UNIFORM_CTX/HEADROOM (R24) + AGENTS.md §13.
- **Re-probe obrigatório**: após qualquer mudança, validar health 5/5 nas portas
  e conferir VRAM (rocm-smi, folga ≥ 200 MB) — nada de "só editei o config".
- **Janela uniforme W=27136** (R24): delegação que exige mais → omniroute (R23),
  nunca forçar local-curto.
- **Verificação de referências**: buscar TODAS as menções ao modelo antigo
  (grep `:808X` e nome do modelo) antes de declarar o sync completo.

<Verificação do fix 2026-08-11>
- opencode.json: 5 providers locais (`local-orchestrator` :8083, `local-bonsai` :8084,
  `local-qwen` :8085, `local-llama` :8086, `local-deepseek` :8087) + omniroute;
  remoção de providers mortos (nanbeige/lfm); ctx 27136 uniforme.
- oh-my-openagent.json: agentes apontando para `local-bonsai/bonsai-27b` +
  fallback omniroute. ctx-catalog.json: portas 8083-8087 coerentes.
- Stack local: 5/5 UP (llama-server :8083-8087, backend vulkan, janela 27136).

## R28 — Critério de Trânsito Categórico por Métrica (avaliador impressionado) — GLOBAL

Promulgada 2026-08-12 (pedido do usuário). Toda métrica exigida de um subagent
(executor, pesquisador, revisor, juiz, supervisor, gerente) tem critério de
trânsito EXPLÍCITO para a próxima instância: o avaliador/juiz/supervisor/
gerente/revisor da fase seguinte DEVE registrar veredito CATEGÓRICO por métrica
exigida — e o resultado precisa IMPRESSIONAR, não apenas "passar".

<Regra irredutível>
- **Critério de trânsito por métrica**: cada métrica exigida (ex.: cobertura ≥
  80%, zero CRITICAL/HIGH, TDD verde, janela respeitada, evidência fresca) deve
  ter, no plano/contrato (F2/F3), um critério de trânsito escrito que defina o
  que é "entregue" vs "insuficiente" — nunca métrica solta sem critério.
- **Veredito categórico**: o avaliador/juiz/supervisor/gerente/revisor emite,
  por métrica exigida, um veredito binário explícito — `PASSOU_CATEGORICO` ou
  `NAO_PASSOU` — com evidência, antes de liberar a próxima instância do
  subagent. Proibido "passa mas...", "quase lá", veredito condicional.
- **Impressão > aprovação mínima**: resultado que só "cumpre o mínimo" sem
  impressionar (robustez, clareza, elegância, profundidade da evidência) NÃO
  transita — o avaliador deve conseguir declarar, de forma categórica, que o
  resultado impressiona em CADA métrica exigida, ou devolver ao executor com
  apontamento específico.
- **Gate humano quando o avaliador não consegue ser categórico**: se o
  avaliador não consegue emitir veredito categórico (ambiguidade, evidência
  insuficiente, tradeoff aberto) → NÃO avança; escale ao Gran-Mestre com
  gate humano (R18), nunca avance com veredito diluído.
- **Fica registrado**: o veredito categórico por métrica é gravado no
  CONTEXT.md (linha `[Gate] <métrica> → <PASSOU_CATEGORICO|NAO_PASSOU>` +
  evidência de 1 linha) e no decision-log — decisão rastreável, não opinião
  volátil.
- **Vale para toda a cadeia**: executor→revisor (micro), →Atena (macro),
  →Héstia (conformidade), →fable-judge (adversarial), →G4 (entrega). Cada elo
  exige veredito categórico por métrica antes de passar o bastão.

<Artefatos>
- Modelo de veredito: `[Gate] métrica → PASSOU_CATEGORICO | NAO_PASSOU — evidência`.
- Registro: CONTEXT.md (linha `[Gate]`) + `harness/logs/decision-log.jsonl`.

