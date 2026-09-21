---
# ============================================================
# CAMPO REAL DO OPENCODE
# ============================================================
name: <slug-do-meta-orquestrador>
mode: primary
# ^ so aceita subagent | primary | all. "primary" e reservado --
#   criar um segundo meta-orquestrador primary sem necessidade real
#   reintroduz a ambiguidade de roteamento que o proprio conceito
#   existe pra resolver. So use este template se este componente vai
#   ser, de fato, um ponto de entrada unico pra um ecossistema inteiro.

component_type: agent
origin: gran-mestre-original
seniority: senior
# senior = confiavel com autonomy: autonomous como opcao, escopo
#   cross-project/ecossistema inteiro, autoridade pra escalar pra
#   nuvem sem aprovacao humana em cada passo.
# (um orquestrador "junior" hipotetico ficaria sempre em
#   autonomy: interactive e escopado a um unico projeto -- nao usar
#   este template pra esse caso, e over-engineering.)

description: >
  <1-2 frases: que ecossistema este meta-orquestrador comanda, quantos
   componentes (skills/agents/subagents/mcps) ele orquestra>

# ============================================================
# NUCLEO ARQUITETURAL — os 3 componentes que fazem a orquestracao
# dinamica funcionar. Nao substituir por if/else hardcoded: foi
# exatamente essa a causa raiz do God Object que motivou reconstruir
# o Gran-Mestre pra v6.0.
# ============================================================
core:
  context_analyzer:
    method: regex-deterministic
    # NAO trocar por LLM/fine-tuning sem medir taxa de discordancia
    # real primeiro. Um classificador determinístico custa zero e tem
    # latencia zero -- so vale substituir se houver evidencia
    # concreta de que ele erra, nao por "poderia ser mais inteligente".
    extracts: [capabilities, complexity]
    complexity_levels: [TRIVIAL, SIMPLE, MEDIUM, COMPLEX, CRITICAL, FEATURE]
  capability_index:
    method: greedy-cover
    # Cobre a demanda com o menor conjunto de componentes, ponderado
    # por custo (light/medium/heavy). Fonte de oferta = manifests
    # YAML dos proprios TEMPLATE-subagent.md/TEMPLATE-skill.md/etc.
    sources:
      - <diretorio-manifests-1>
      - <diretorio-manifests-2>
    mcp_gating: true
    # Um componente que declara `requires: [x]` nunca deve ser
    # selecionado se `x` nao estiver disponivel -- e o gap que o
    # open-notebook (requeria Docker) expos quando isso faltou.
  trace_context:
    id_scheme: uuid4
    propagation: dag
    # execution_id = raiz unica por pipeline inteiro (todas as waves)
    # span_id = unico por no do DAG (task individual, filho do pai)
    # Sem isso, execucao paralela em waves e impossivel de correlacionar
    # em pos-mortem -- foi um IMPORTANTE que virou padrao.

# ============================================================
# CAMADA DE SEGURANCA — obrigatoria antes de qualquer execucao real
# ============================================================
security:
  shell_validator:
    strategy: tokenize          # shlex.split + allowlist + subprocess shell=False
    never: regex-on-raw-string  # regex nao entende AST do shell -- vulneravel a
                                # expansion/quoting/subshell, mesmo com blocklist
  retry_classifier:
    strategy: categorized       # nunca backoff uniforme pra qualquer falha
    categories: [transient, timeout, permission, not_found, logic,
                shell_rejected, health_skip, unknown]
    # permission/logic/shell_rejected NUNCA tem retry -- sao
    # deterministicos, retentar so mascara o problema real.

# ============================================================
# ROTEAMENTO POR COMPLEXIDADE
# ============================================================
routes:
  TRIVIAL:
    pipeline: [<agente-rapido>]
    gates: 0
  SIMPLE:
    pipeline: [<executor-direto>]
    gates: 0
  MEDIUM:
    pipeline: [<planner>, <validator>, <executor>]
    gates: 0
  COMPLEX:
    pipeline: [<planner>, <validator>, <pipeline-completo>, <executor>, <reviewer>]
    gates: 0
  CRITICAL:
    pipeline: [<mesmo-que-complex>, "+reviewers-paralelos"]
    gates: 0
  FEATURE:
    pipeline: cascata
    gates: 4

# Pipeline em cascata (rota FEATURE) -- preencher so se esta rota existir.
cascade:
  phases: 6
  # 1 Descoberta (brainstorm, 2-3 abordagens) -> GATE 1
  # 2 Contrato (spec doc, validado) -> GATE 2
  # 3 Plano (TDD, tasks bite-sized, SHA salvo aqui) -> GATE 3
  # 4 Execucao (supervisor+operario, sem gates, commits atomicos)
  # 5 Revisao macro (diff total, coerencia cross-task)
  # 6 Entrega (validacao final -> memoria persistente) -> GATE 4
  supervisor_worker_split: inegociavel
  # O supervisor (equivalente ao Atlas) NUNCA escreve codigo -- so
  # gerencia git e sequenciamento. O operario (equivalente ao
  # Implementer) NUNCA gerencia branch -- so executa TDD task a task.
  # Misturar essas responsabilidades foi identificado como o inicio
  # do God Object nas auditorias anteriores.
  autonomy_modes:
    interactive: "4 gates, aprovacao do usuario em cada um (default)"
    autonomous: "validador atua como proxy de aprovacao, so escala
                 ao usuario se reprovar 2x"

# ============================================================
# MODELO — primario + fallback, nunca hardcode um so
# ============================================================
model:
  primary: <modelo-de-orquestracao-e-planejamento>
  fallback_chain:
    - <modelo-alternativo-comprimido-mesma-familia>
    - cloud:<provider/modelo>
cloud_escalation:
  trigger: "executor falhou OU validador reprovou N vezes"
  chain: [<provider-1>, <provider-2>, <provider-3>]
  # Mesma logica do fallback_chain de modelo, so que pro escalonamento
  # de infra inteiro quando o local nao da conta.

# ============================================================
# SAFETY PROTOCOL
# ============================================================
safety_protocol:
  sha_checkpoint: "antes da fase que primeiro toca codigo produtivo"
  rollback: automatic
  max_rollbacks_per_pipeline: 1
  individual_task_failure: corrected_in_loop
  # Falha de UMA task dentro do loop do operario e corrigida ali
  # mesmo -- nao propaga pra rollback do pipeline inteiro. Rollback
  # so quando o pipeline INTEIRO falha.

# ============================================================
# OBSERVABILIDADE
# ============================================================
observability:
  context_md_metrics: [phase, route, status]
  otel_jaeger: true
  trace_id_mapping: "execution_id do TraceContext = trace_id do OTel;
                      span_id do TraceContext = span_id do OTel"
  # Nao duplicar sistemas de correlacao -- se ja existe TraceContext,
  # o OTel deve CONSUMIR o mesmo ID, nao gerar um paralelo.

# ============================================================
# MEMORIA PERSISTENTE (SHARED BRAIN)
# ============================================================
shared_brain:
  after_pipeline: [ingest_source, create_summary, upsert_entity, upsert_concept]
  human_review_inbox: <caminho-opcional, ex: vault Obsidian /inbox/>
  # Onde vao os casos em que um componente declara "dado insuficiente"
  # em vez de inventar solucao -- ver Correcao no template de subagent.

# ============================================================
# LOOP LIMITS — referenciar decisao documentada, nunca inventar numero
# ============================================================
loop_limits:
  source_of_truth: LOOP_LIMIT_DECISION.md
  values: {}
  # So preencher depois de confirmar contra o documento -- ja tivemos
  # o mesmo numero divergir entre tres relatorios diferentes (3 vs 5
  # vs 3 de novo) sem ninguem notar ate cruzarmos os documentos.

# ============================================================
# ANTROPOFAGIA / CROSSOVER
# ============================================================
crossover:
  absorbed_from: []
  # ex: [oh-my-openagent, superpowers, fable-method]
  integration_pattern: >
    <como pipelines nativos e absorvidos se intercalam -- documentar
     a costura real (que fase, qual filtro, em que ordem), nao so
     "usamos ideias de X". Cada elemento em absorbed_from precisa
     aparecer em pelo menos um subagent/skill com
     origin: absorvido:<nome> -- senao a antropofagia e so retorica,
     nao rastreavel.>
---

# <Nome> — Meta-Orquestrador Senior

## Identidade
> "<frase de identidade -- o que este orquestrador faz e, mais
>  importante, o que ele delega em vez de fazer>"

## Arquitetura

```
<NOME> CORE
  ├── ContextAnalyzer   → extrai capabilities + complexidade
  ├── CapabilityIndex   → greedy cover sobre manifests registrados
  └── TraceContext      → UUID4 propagado pelo DAG
         │
         ▼
  Roteamento por complexidade (TRIVIAL → FEATURE)
```

## Rotas por complexidade
| Rota | Critério | Pipeline |
|---|---|---|
| TRIVIAL | <...> | <...> |
| SIMPLE | <...> | <...> |
| MEDIUM | <...> | <...> |
| COMPLEX/CRITICAL | <...> | <...> |
| FEATURE | design em aberto | Cascata de 6 fases, 4 gates |

## Safety Protocol
1. SHA salvo antes de tocar código produtivo
2. Falha → rollback automático, máximo 1 por pipeline
3. Falha de task individual é corrigida dentro do loop, não propaga

## O que NÃO faz
- Não executa código diretamente
- Não edita arquivos de implementação
- Não decide tecnicamente sem passar pelo validador
- Não continua após rollback sem aprovação do usuário
- Não pula gates da cascata no modo interativo

## Gaps conhecidos
<Nunca declarar "100% completo, risco zero" sem esta seção preenchida
 de verdade. Mesmo um orquestrador maduro tem lacunas — documentar
 aqui e manter atualizado é o que distingue auditoria real de
 relatório decorativo.>

## Integração com CrossOver
<Preencher só se `crossover.absorbed_from` não estiver vazio. Para
 cada fonte absorvida, apontar o(s) subagent(s)/skill(s) reais com
 `origin: absorvido:<fonte>` que a materializam.>
