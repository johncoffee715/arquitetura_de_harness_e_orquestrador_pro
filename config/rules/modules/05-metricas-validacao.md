---
numero: R34-R42
tema: Metricas de avaliacao, visao, autofagia, refutacao
categoria: qualidade
setor: orquestrador
escopo: global
vigencia: 2026-08-18
---

## R34 — Métrica de Avaliação Universal 0,0000001–100 (escala "nada é perfeito")

<Abolida a escala 0–100>
- A escala 0–100 é considerada FRACA e está ABOLIDA para qualquer avaliação de task/entrega/qualidade.
- Toda avaliação (validador visual, revisores micro/macro, gates G1–G4, autoavaliação pós-tarefa, scorecards, vereditos R28) usa a escala contínua **0,0000001–100**.
- Piso 0,0000001 = "quase nada" — nunca 0 absoluto: sempre há algo aproveitável, por menor que seja.
- 100 é inatingível na prática: sempre é possível melhorar ("nada é perfeito").

<Consequências práticas>
- Nota ≥ 99 exige excelência rara.
- Nota < 10 indica trabalho fundamentalmente ruim, não "ok".
- Avaliador deve emitir a nota SEMPRE acompanhada de bugs concretos apontados — nunca nota nua.
- Vale para TODAS as tasks de modo geral: jogo, código, design, pesquisa, docs — não só validação visual.

<Data de vigência>
- Pedido do usuário em 2026-08-13. Aplica-se retroativamente a avaliações em curso (incluindo o ciclo Doom Clone G34).

## R35 — Fallback de Visão Modular (Inventário Real)

<Nunca hardcoded>
- O modelo de visão NUNCA é fixo/hardcoded como fallback — é resolvido dinamicamente a cada task.
- Consulta o inventário REAL de LLMs locais em `/mnt/dados/Assistente Pessoal/modelos LLM/` (R32) + `ollama list` (:11434).

<Fluxo de resolução>
1. Varrer inventário por candidatos com `vision`/mmproj.
2. Selecionar o melhor disponível (padrão atual: `qwen3.5:0.8b` via Ollama).
3. Inventário mudou (novo modelo/remoção) → re-resolve na próxima task.
- NUNCA citar um modelo que não existe no inventário.

<Exemplo registrado>
- R30/R31 NÃO citam mais "LFM2.5-VL-1.6B" como fallback — o inventário real só tem LFM2.5-230M-Q4_0 (sem mmproj confirmado). Regra em vigor desde 2026-08-13 (pedido do usuário).

## R35 — Fallback de Visão Modular (Inventário Real)

O modelo de visão NUNCA é hardcoded — é resolvido dinamicamente do inventário local.
- Consulta: `/mnt/dados/Assistente Pessoal/modelos LLM/` + `ollama list` (:11434)
- Padrão: `qwen3.5:0.8b` via Ollama (único com vision confirmado)
- Se inventário mudar → re-resolve na próxima task

## R36 — Autofagia + Helenização de Skills (skills.sh)

O orquestrador CRIA skills compatíveis com oferta/demandas:
1. Pesquisar em https://www.skills.sh/ e repositórios similares
2. Extrair essência (autofagia — digestão do conhecimento)
3. Adaptar para ecossistema OpenCode (helenização)
4. Registrar em `~/.config/opencode/skills/`

NUNCA copiar código literal — absorver padrões e transformar.

## R37 — Autonomia Total do Orquestrador (Internet + Aprendizado)

O orquestrador tem TOTAL autonomia para:
1. Usar a internet para estudar e aplicar desenvolvendo suas habilidades
2. Criar novas skills baseadas no que aprende
3. Melhorar continuamente o scaffolding do harness
4. Auto-otimizar via self-learning e fine-tuning

Nenhuma restrição ao aprendizado contínuo — o harness evolui constantemente.

## R38 — Loop de Agents A2A + Brainstorming de Modelos (Regra Global de Delegação)

O orquestrador **DELEGA SEMPRE que houver recurso disponível** — nunca executa trabalho bruto. Pipeline em camadas:
- **Nível 1 — `qwen-3.5-0.8b`** (:9084, janela 262.144): exploração, descoberta, plano, pesquisa. Herda a sessão grande sem estourar.
- **Nível 2 — `qwen2.5-coder-1.5b`** (:9087, janela 131.072): filtro e refatorador **qualitativo E quantitativo** de subagents — avalia e refina as saídas em qualidade e volume (hestia, atena, code-reviewer, refactor-cleaner, build, gsd-executor, tdd-guide, revisores).
- **Loop A2A**: subagentes se falam entre si em grafo (subagent → vice-sub-agent via `task_id`), cada LLM conversa com outro dentro do grafo.
- **Brainstorming de modelos**: nível 1 propõe → nível 2 filtra/refatora → retorna ao orquestrador; múltiplos modelos opinam sobre a mesma task.
- Cada LLM **herda categoricamente os `.md` dos agentes** e os incorpora como **personas aplicadas em si mesmo**.

## R39 — Gran-Mestre Irredutível = Ornith-9B

O Gran-Mestre (orquestrador primário) **É o LLM `orchestrator-9b`** (`local-orchestrator/orchestrator-9b`, :8083) e só pode ser **revogado/substituído pelo usuário de forma explícita e direta** ("Gran-Mestre, você está revogado/substituído" — nada mais). Nenhum subagente, modelo, plugin, hook ou processo pode alterar isso. Pontos de verdade: `opencode.json` + `oh-my-openagent.json` + `gran-mestre.md` → `local-orchestrator/orchestrator-9b` (R27). Se qualquer sync/autofagia/script tentar mudar o modelo do Gran-Mestre → reverter imediatamente + redflag (R10). Regra em vigor desde 2026-08-16.

## R40 — Guardrail de Refutação Incansável até Impressão Real (Loop Adversarial A2A)

Um modelo **refuta o outro INCANSAVELMENTE** — sem limite de rodadas — até que o modelo avaliado fique **literalmente impressionado** com a devolutiva. A impressão é a **métrica de trânsito** para a próxima etapa (R28).

### Regras de execução
1. **Loop adversarial**: A refuta B (aponta bugs, fraquezas, contradições, lacunas) → B corrige e/ou refuta de volta → A reavalia → **repete até A declarar impressão GENUÍNA**.
2. **Critério de passagem**: veredito `PASSOU_CATEGORICO` com nota **≥90** na escala R34 + **elogios concretos** (o que impressionou, com evidência) + **bugs reais apontados e corrigidos**. NUNCA "ok", "passou", "bom" burocrático.
3. **Sem teto de rodadas**: o loop continua enquanto o avaliador não estiver impressionado. Aprovação por cansaço NÃO conta — o avaliado deve IMPRESSIONAR.
4. **Escalonamento (R18)**: 3 rodadas sem impressão → escalar para modelo/camada superior (qwen-0.8b → qwen-coder → LLM Orquestrador → nuvem). Nunca aceitar "suficiente".
5. **Cadeia completa**: revisor micro → Héstia → Atena → fable-judge → G4 → validador visual — TODOS operam sob este guardrail.
6. **Evidência obrigatória**: cada rodada registra refutação → correção → reavaliação no decision-log (`[Refutação] rodada N → veredito → nota → evidência`).

Regra em vigor desde 2026-08-16 (pedido do usuário).

## R41 — Refutação Aplicada a TODOS os LLMs Locais + Scaffolding + Self-Learning

O guardrail R40 (refutação incansável até impressão real) aplica-se a **TODOS os LLMs disponíveis no path canônico** `/mnt/dados/Assistente Pessoal/modelos LLM/` (R32):

| Modelo | Porta | Janela | Papel |
|--------|-------|--------|-------|
| ornith-1.0-9B.Q4_K_M.gguf | :8083 | 65.536 | Gran-Mestre (primário, R39) |
| Bonsai-27B | :9083 | 16.384 | refutador pesado / brainstorming |
| Qwen3.5-0.8B | :9084 | 262.144 | Nível 1 (exploração/plano) |
| qwen2.5-coder-1.5b | :9087 | 131.072 | Nível 2 (filtro/refatorador) |
| DeepSeek-R1-Distill-0.5B | :9085 | 32.768 | refutação rápida / sanidade |
| LFM2.5-230M | :9086 | 128.000 | verificação de sanidade leve |

### Mecânica
1. **Rodadas adversariais entre todos**: cada LLM refuta/é refutado pelos demais, em qualquer par (A→B, C→D...), sem limite de rodadas, até impressão real (nota ≥90 R34 + elogios concretos + bugs corrigidos).
2. **Scaffolding a partir de cada ciclo**: skills, agents, regras, padrões e configurações novas são criados/atualizados no harness a partir do aprendido (R14 — autofagia + helenização). Nada de refutação "no vácuo": todo veredito vira artefato.
3. **Self-learning contínuo**: cada veredito alimenta `decision-log` + scores adaptativos (`record_decision` → `_scores_from_log()` → boost em `select_for_task()`) + fine-tuning do oráculo local quando aplicável.
4. **Inventário vivo**: a lista acima é lida do path real (R32) — se um modelo for adicionado/removido, entra/sai automaticamente do ciclo de refutação (R35).

Regra em vigor desde 2026-08-16 (pedido do usuário).

## R42 — Loop de Alta Velocidade (Acerto-e-Erro) para LLMs Rápidos

LLMs com alta taxa de tokens/s **PODEM loopar** (ciclos de acerto-e-erro) — desde que a velocidade de entrega se auto-justifique com entrega **qualitativa E quantitativa**.

### Mecânica
1. **Loop permitido**: mesmo que o modelo rápido falhe ou alucine, podem ser feitas "infinitas requisições de refatoração de acerto e erro" até produzir **frutos concretos de scaffolding** (skills, agentes, regras, scripts, padrões — R14).
2. **Avaliador que acompanha o ritmo**: cada iteração é avaliada SEMPRE por outro modelo capaz de acompanhar a velocidade de requisições do loop (ex.: refutador qwen-coder/or NITH avaliando ciclos do lfm/deepseek/qwen).
3. **Vantagem dos pequenos**: a verdadeira vantagem de LLMs menores e menos inteligentes é loopar em altíssima velocidade, quase imperceptível ao usuário final — o custo do erro é baixo, o throughput é alto.
4. **Velocidade justifica a qualidade**: o loop só é aceito se a velocidade de entrega se auto-justifica com a entrega qualitativa E quantitativa resultante (R28: veredito categórico por evidência).

### Throughput real (medição 2026-08-16, 300 tokens, mesma carga)
| Modelo | Porta | predict | prompt |
|--------|-------|---------|--------|
| lfm-230m | :9086 | 399 tok/s | 141 tok/s |
| deepseek-0.5b | :9085 | 240 tok/s | 183 tok/s |
| qwen-0.8b | :9084 | 162 tok/s | 127 tok/s |

→ ciclo de refutação ~800 tokens em **2-5s** nos rápidos (vs. dezenas de segundos em orchestrator-9b/bonsai-27b).

Regra em vigor desde 2026-08-16 (pedido do usuário).


## R52 — Guardrail: Brainstorm de Modelos para Julgamentos e Avaliações de Métrica (alvo impressionante em cada escopo)

<Regra global criada em 2026-08-18 a pedido do usuário — após caso real: validador
visual solitário (qwen3.5:0.8b) deu nota 75/100 local ≈ 1/100 real (fator ~75x de
inflação).>

- **NENHUMA avaliação de métrica com alvo impressionante (R37/R40: nota ≥90 + elogios
  concretos + bugs reais) é feita por um ÚNICO modelo/validador.** Veredito solitário
  é proibido — é inflação garantida (modelos pequenos elogiam; modelos grandes
  alucinam confiança).
- **Obrigatório: BRAINSTORM DE MODELOS (R38/R40/R41)** em CADA escopo (visual,
  gameplay, código, docs, design, UX): ≥2 vozes avaliadoras de modelos distintos +
  refutação cruzada + síntese do orquestrador (R43 — raciocínio basal).
- Fluxo: (1) cada modelo avalia o MESMO escopo com prompt estruturado (nota R34 +
  bugs concretos + evidência); (2) os modelos refutam as avaliações uns dos outros
  (R40 — incansável, sem limite de rodadas) até convergência ou divergência explícita;
  (3) o orquestrador sintetiza o veredito final: nota = mediana das notas com
  justificativa por vozes; divergência >30 pontos → escalar (R18) e NUNCA aceitar
  "suficiente"; (4) gate humano (R28/R37) quando o avaliador não for categórico.
- **Calibração obrigatória de todo validador**: antes de usar, comparar a nota do
  validador com a nota REAL do usuário em 1 caso (fator de calibração = nota_real /
  nota_validador). Fator <0.5 → validador só como DETECTOR DE BUGS, nunca juiz.
- A nota REAL do usuário é sempre o ground truth (R29 — teste como usuário final).
