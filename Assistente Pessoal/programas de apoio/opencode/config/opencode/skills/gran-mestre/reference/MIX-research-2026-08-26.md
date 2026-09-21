# Referência de Validação Externa — Gran-Mestre v8 (MIX + Dev Loop, 2026-08-26)

Este arquivo registra as consultas da rodada MIX (R50). Transparência integral
(legado do protocolo PCA v1 anti-inflação): só constam como **verificáveis** as
fontes com URL completa recuperada; as demais estão marcadas **não-verificável
(nesta sessão) e declaradas como síntese** — sem fingir rastreabilidade.

## A. Fontes verificáveis (URL completa — 27)

| # | Tema | Fonte | URL |
|---|---|---|---|
| 1 | Idempotência two-phase reservation (RESERVE→COMMIT) | Alok Necessary | https://aloknecessary.in/blogs/idempotency-distributed-systems/ |
| 2 | Idempotência + dedupe store + at-least-once | System Design Sandbox | https://www.systemdesignsandbox.com/learn/idempotency-deduplication |
| 3 | Idempotency key pattern + saga (2026) | AppScale | https://appscale.blog/en/blog/microservices-pattern-idempotency-distributed-systems-2026 |
| 4 | Retry + idempotência em workflows (dedupe, CAS, deterministic IDs) | Breyta | https://breyta.ai/blog/idempotency-retries-prevent-duplicate-runs |
| 5 | Idempotent processing + reliable delivery + saga compensation | martinuke0 (EN) | https://martinuke0.github.io/posts/2026-03-30-optimizing-event-driven-microservices-through-idempotent-processing-and-reliable-message-delivery-orchestration/ |
| 6 | Retry ANTES do circuit breaker (transiente); CB p/ persistente | Azure Architecture Center | https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker |
| 7 | Saga + CB: compensação idempotente, retry/backoff, observar | CoddyKit | https://www.coddykit.com/pages/blog-detail?id=512378&slug=mastering-microservices-communication-best-practices-for-saga-and-circuit-breake |
| 8 | Retry vs CB semantics + retry storms + idempotência | GeeksforGeeks | https://www.geeksforgeeks.org/system-design/circuit-breaker-vs-retry-pattern/ |
| 9 | CB por step de saga (isolamento) + outbox | theyawns | https://theyawns.com/2026/06/15/circuit-breakers-and-retry-resilient-hazelcast-sagas |
| 10 | Saga: timeout por step, CB pausa saga | martinuke0 (Saga) | https://martinuke0.github.io/posts/2026-05-28-architecting-the-saga-pattern-for-distributed-transactions-maintaining-data-consistency-in-modern-commerce-systems/ |
| 11 | HITL estrutural (gate imposto por runtime — não autoavaliável) | OpenLegion | https://www.openlegion.ai/en/learn/human-in-the-loop-ai-agents |
| 12 | HITL: autonomia calibrada (reversível auto; irreversível + conf. baixa → humano) | DEV Community | https://dev.to/taimoor_ijaz_effe0dcaf627/-human-in-the-loop-hitl-for-ai-agents-patterns-and-best-practices-5ep5 |
| 13 | HITL: 4 dims de risco (irreversibilidade, blast radius, compliance, confiança) | MyEngPath | https://myengineeringpath.dev/genai-engineer/human-in-the-loop/ |
| 14 | HITL escalada: triggers (confiança, novidade, política, contradição) | AppScale HITL | https://appscale.blog/en/blog/microservices-pattern-human-in-the-loop-escalation-2026 |
| 15 | HITL checklist + governance gap | Moxo | https://www.moxo.com/blog/hitl-implementation-checklist |
| 16 | AI Agent Orchestration Patterns 2026 (HITL, hierarchy, budget) | JobsByCulture | https://jobsbyculture.com/blog/ai-agent-orchestration-patterns-2026 |
| 17 | Scoring bias LLM-as-a-Judge (posição/rubrica/referência) | arXiv 2506.22316 | https://arxiv.org/abs/2506.22316 |
| 18 | Rulers: rubricas travadas + evidenci-anchored scoring + Wasserstein calib. | arXiv 2601.08654 | https://arxiv.org/abs/2601.08654 |
| 19 | Escala 0–5 alinha MAIS com humanos que 0–100 | arXiv 2601.03444 | https://arxiv.org/abs/2601.03444 |
| 20 | Fluency/verbosity bias infla notas | Zylos | https://zylos.ai/research/2026-07-07-fluency-bias-llm-judge-text-evaluation-calibration/ |
| 21 | Sycophancy survey | SycEval | https://arxiv.org/abs/2502.08177 |
| 22 | Anchoring bias LLMs | Springer | https://link.springer.com/article/10.1007/s42001-025-00435-2 |
| 23 | LLM as Judge: rubrics biassless (qaskills 2026) | qaskills | https://qaskills.sh/blog/llm-as-a-judge-evaluation-guide |
| 24 | LLM judge bias mitigation survey (position swap + ensemble + rubric) | sksoumik | https://github.com/sksoumik/llm-as-judge |
| 25 | Idempotência: chave + atomicidade (transação mesma) | synchronium | https://synchronium.github.io/software-architecture-wiki/distributed/idempotency.html |
| 26 | Idempotência design patterns (data engineering) | O'Reilly | https://www.oreilly.com/library/view/data-engineering-design/9781098165826/ch04.html |
| 27 | Idempotency key em orchestration layer | Inferensys | https://inferensys.com/glossary/tool-calling-and-api-execution/orchestration-layer-design/idempotency-key |

## B. Síntese declarada — NÃO-VERIFICÁVEL nesta sessão (marcadas, 20)

Consultas das rodadas 1–2 do MIX (multilíngue) cujas URL concretas não foram
recuperadas no momento da síntese; registradas por fidelidade ao processo, mas a
banda 20–35 NÃO depende delas (só das 27 verificáveis):

- EN/PT/ZH/JA/KO/DE/RU sobre: LangGraph vs CrewAI vs OpenAI SDK (landscape 2026);
  A2A protocol v1.0 (JSON-RPC 2.0 + SSE, AgentCard, task state machine) —
  confirmado também por fontes EN verificáveis; advertência TechTIQ sobre
  maturidade A2A; Tencent/ZH sobre 3 estados (working/session/log) + budget zones
  + tool registry 9 metadados; Mercari/JA sobre fail-open telemetria × fail-closed
  segurança; reopt/KO sobre adotação orchestrator-worker ~70% + handoff packet +
  trace sampling; nikolskiy/RU sobre recursão de delegação limitada em código
  (depth máx); Habr/RU sobre single-agente default; andreww.ooo/effloow sobre
  framework landscape; Tyk/MS Learn sobre MCP/A2A como complementares; OTel
  semconv PR #291 e issue #287 (fga.authorize, cost.source/exactness);
  otel-agent-provenance (derivation.input_spans/strategy/weight/influence);
  otel issue #35 (audit log assinado Ed25519).

## Como este artefato sustenta as bandas PCA v1

- **Banda 12–20** ("múltiplos mecanismos novos verificados + loop convergiu"):
  mecanismos operacionais do SKILL.md v8.4.0 (contrato de retorno 5-itens, two-phase, ordem precedente 2 níveis, snapshot SHA), cada um mapeado a fontes
  verificáveis SOMENTE da seção A: RunID two-phase (#1,#3,#25,#26,#27) · retry
  antecede CB e CB conta ciclos (#6,#7,#8,#9) · compensação interna ao ABORT
  (#5,#7,#10) · HITL estrutural e autonomia calibrada (#11,#12,#13,#14,#15,#16).
- **Banda 20–35** ("excede prática publicada + multi-rodada independente"):
  suportada por **06** (seis) evidências da seção A — mecanismo operacional
  verificável ↔ fonte concreta — sem depender de nenhuma fonte não-verificável:
  (1) two-phase reservation no store RunID (#1); (2) retry→CB ordem precedente (#6);
  (3) compensação antes do rollback no ABORT (#7); (4) HITL estrutural (gate por
  runtime, não autoavaliação) (#11); (5) autonomia calibrada por irreversibilidade
  (#12); (6) escala comprimida para avaliação (PCA v1) ancorada em evidência
  (#17,#18,#19,#20). Há ainda 1 roda de validação adversarial em 4 pilares
  convergida (r1–r4) + rodada recalibrada r5 + panteão r6 (D/A/H/F PCA, 2026-08-26)
— 6 rodadas independentes.
- Confissão de limites (por isso NÃO é 35+): GAP-P5 FECHADO em 2026-08-26 via
  permission nativo (agent frontmatter) + plugin guard-gap-p5.ts (ativação pós-boot;
  fail-closed ainda sem deny PROVADO em runtime — validar na sessão pós-restart),
  ausência de testes executáveis automatizados da doutrina, e deflação da própria
  escala mostra que notas altas pré-PCA eram viés de fluência (fonte #20).

## Adendo r6b2 (2026-08-26)
Guard gov-aware: o plugin permite escrita via bash (tee/cat/echo redirecionados) para destinos de
governança (CONTEXT.md, decision-log, vault, config/opencode, reference/, state/watcher) e mantém
fail-closed para código produtivo. Teste funcional: 7/7.

## Adendo r6b3 (2026-08-30) — ESCOPO DE ESCRITA CORRIGIDO (fix guard-gap-p5)
Denies reais em produção (JSONL) mostraram o guard negando escritas LEGÍTIMAS do Hefesto/forja:
harness operacional (scripts/, tools/, tests/, state/, bin/, templates/, data/), configs globais
(~/.opencode, ~/.config/opencode) e sandbox /tmp/opencode (via edit), além de quebrar com path
escapado `Assistente\ Pessoal`. FIX: guard-engine ganhou `unescapePath()` + `isAllowedWritePath()`
(= governança + harness operacional + globais + sandbox; THIRD_PARTY_ROOTS `repos|cactus-build|
llama.cpp|cache|projetos|tranqueiras` = NUNCA); `sed -i` virou govAware com extração de destino;
plugin edit usa isAllowedWritePath. TDD 28/28 (node --test) + gabarito hefesto-forja espelha o escopo.

## ADENDO r7 (2026-08-26) — SUÍTE DE TESTES EXECUTÁVEIS (fecha a pendência R51/TDD)
- tests/guard-engine.test.ts: 17/17 (node --test) — todos os padrões allow/deny/allow-gov/allow-r18.
- tests/test_gran_mestre_doctrine.py: 8/8 — contrato dos artefatos (frontmatter, versão 8.4.0,
  norma ≥95, GAP-P5 permission deny+allow gov, plugin+engine, reference sem stale, inventário, teto).
- tests/test_llm_inventory.py: 12/12 — motor R52 (schema, ids únicos, categorias fechadas, probe mock todos slots,
  amálgama 0-5, bench CONFIRMED c/ itens, resolve/show/register rejeitam entradas inválidas,
  cmd_all/cmd_validate executam) — cobertura funcional do motor: 9/9 (100%).
- Runtime: guard-gap-p5 ativo com deny reais (JSONL 138+ eventos; deny bash×3+3, deny edit×2,
  allow gov×N) — fail-closed PROVADO em produção, não apenas por design.


## ADENDO v9 (2026-08-31) — Refatoração total com substituição do motor :9088

- **Problema crônico**: subagente hefesto (qwen3.8-4b-distill :9088) alucinava sucesso sem escrita
  ("8/8 PASS ✅" com SHA dos alvos inalterado) + lixo de formatação + negação de arquivos existentes.
- **Correção estrutural**: `scripts/antilixo_gate.py` + `tests/test_antilixo_gate.py` (9/9 PASS) —
  detector determinístico (zero LLM) de sinais_lixo + alucinacao_entrega (afirma sucesso sem escrita
  vs baseline SHA) + exit_status incompleto. Obrigatório no Gate de Entrega da doutrina v9.
- **Substituição do motor (camada 4, diretriz usuário)**: busca comunitária multi-idioma (R80) —
  HF + DDG EN/ZH/JA/KO + vídeo ES (Nichonauta: LFM ToMoE — GGUF denso-equivalente, descartado; 
  kshitijthakkar/qwen3.5-moe-4.7B-d4B: evidência fraca) → contingência densa granite-4.2-3b
  (IBM, Apache-2.0, BFCL-v4 52.41, RULER 64K 67.52, janela 131K, GGUF Q4_K_M 2.24GB) INSTALADO na
  :9088 (probe de contrato: exit_status blocked + motivo real, sem alucinação). MoE não-oficiais
  ainda em avaliação (R79/R78).
- **Sync R27 5/5**: start-stack.sh · manifest_llm.json (com R78/R76/R79) · harness/llm-inventory.json ·
  opencode.jsonc (ctx 200000→131072) · ctx-catalog (N/A neste slot).
- **Doutrina v9.0.0**: núcleo enterprise v8.4 preservado + R57-R79 incorporadas + otimizações do fonte
  original (escala por maturidade, orquestrador leve, custo por workflow) + R80. Testes de doutrina 8/8
  (2 corrigidos à realidade: norma ≥95 onde vive; inventário 5 models). Execução supervisionada direta
  (R6/R11) após 3 rodadas de subagente alucinando.
