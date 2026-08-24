# F2 — CONTRATO / SPEC — Meta-Orquestrador Adaptativo Modular + GMB-1

**Versão:** 2.0-integrada
**Data:** 2026-08-23T16:28
**Fontes:** PRD v1 (2171L) + PRD v2 Refatorado (1960L) + GMB-1 (897L) + F1-discovery.md
**Gates exigidos:** Hestia (validação contrato) + Atena (revisão coerência) + fable-judge (adversarial)

---

## 1. Visão
Construir Harness **model-agnostic + backend-agnostic** que, dado `/mnt/dados/Assistente Pessoal/modelos LLM/` como MODEL_LIBRARY volátil:
- descobre LLMs automaticamente, classifica por capability estimada+medida, roteia por VRAM/contexto/histórico, executa grafo 0-6 condicional, aprende e garante auditabilidade.

`META_ORCHESTRATOR` é papel eleito dinamicamente (Primary/Secondary), não fixo. Hoje `Ornith-1.5-9B Q4` é primary hint, mas elegível a failover.

## 2. Escopo Contratual

### 2.1 In (obrigatório)
- Discovery Engine: scan *.gguf -> GGUF metadata -> checksum -> family priors (qwen 0.82/0.85, bonsai 0.88, ornith 0.85, phi 0.75) -> quant penalty (Q4 0.95, Q3 0.88, Q2 0.75, IQ2_XXS 0.65) -> param scaling log -> context bonus +0.05 >64K -> VRAM estimate -> GPU compat gfx906 -> registry update -> micro-bench 5 prompts opcional -> capability confidence = measured/(measured+10)
- Registry: yaml com models/{id: file, arch, backend, resources, capabilities {estimated/measured/confidence}, roles_suitability, performance_history, health {GREEN/YELLOW/RED}}, hot reload inotify debounce 5s, evento MODEL_REMOVED_DURING_EXECUTION
- Router: `MODEL_SCORE = 0.30 cap_fit + 0.25 task_fit + 0.15 ctx_fit + 0.15 res_fit + 0.10 hist + 0.05 verif -0.10 cost -0.05 risk` (todos [0,1]), VRAM-aware (16GB MI50) = TOTAL - USED - 2GB reserve >= MODEL + KV + 1GB buffer, context-aware (prompt+output+tool+retrieved vs context_length)
- Grafo 0-6 condicional: FAST (low risk+low complexity: 0->4->6, G1/G2 auto), STANDARD (0->1->2->3->4->5->6, G1-4), FULL (0->1 brainstorm multi-agente ->2 audit ->3 refutation ->4 micro-review ->5 macro-refutation ->6 verificação independente, G1-4). Classificador leve lfm2.5-230m.
- Swarm dinâmico por task (Planner/Coder/Critic/Judge), sequencial se VRAM==1, fresh subagent per task com task_contract isolado
- Plugin Registry estratificado: tools/mcps/lsps/skills/hooks com lifecycle manager próprio
- Health Engine: GPU vram<80% GREEN, 80-95 YELLOW, >95% ou temp>85 RED; model latency <1.5x GREEN etc; filesystem >10GB GREEN; git clean GREEN
- Observability: dashboard tempo real (Phase, Node, Model, VRAM, Context, Progress, Task Queue), event log SQLite (90d) + arquivo rotativo, audit trail INPUT->STATE->CANDIDATES->SCORES->DECISION->RESULT
- Memory: SQLite + FAISS/chroma + Obsidian sync bidirecional (`/mnt/dados/cerebro com IA/`), knowledge extraction após cada report
- Self-improvement 3 níveis: L1 observacional (dados), L2 política (pesos router, 3 exec sucessivas, auto-revert), L3 estrutural (aprovação humana ou grafo 0-6 completo, PolicyClassifier independente)
- GMB-1 integrado (Gran Master Benchmark): ver §4

### 2.2 Out (não-objetivos v2 §41)
- Não modificar produção silenciosamente, não alterar mecanismos segurança sem auditoria, não aceitar resposta textual como evidência, não escolher por params, não hardcodear modelos, não swarm tudo, não carregar contexto completo desnecessário, não executar sem contrato quando exigir aprovação, não usar Obsidian como engine, não permitir auto-classificação.

## 3. Requisitos Não-Funcionais
- 1 LLM GPU por vez (MI50 16GB), 6 CPU slots (9083 bonsai 16K, 9084 qwen 131K, 9085 llmjudge 32K, 9086 lfm 128K, 9087 qwen38-2b 262K, 9088 qwen-1.7B 32K, 8083 ornith GPU 131K)
- Fases 0-3 READ-ONLY filesystem/git/shell, F4 READ-WRITE task files + shell declarado, F5-6 READ-ONLY inspeção
- Sandboxing menor privilégio, Meta-Orchestrador sem fs/shell direto (via Tool API)
- Hot reload <30s para novo .gguf sem alteração código

## 4. GMB-1 — Benchmark Gran Master (integrado ao contrato)
**Objetivo:** eleger `GPU_PRIMARY_SLOT` entre 3 candidatos:
1. Ornith-1.5-9B Q4 (5.3G, 131K, VRAM 8.5G, 69t/s) — maturidade agentic
2. Qwen3.8-9B-Distill Q4 (5.4G, 131K, VRAM 10.7G, 97t/s) — reasoning/GB
3. Qwen3.8-27B IQ2_XXS (8.4G, 196K, VRAM 12.6G, 28t/s) — potencial cognitivo

**Isolamento (§2):** system_prompt, user_prompt, tools, skills, MCP, RAG, memory, context, temp, top_p, seed, max_tokens, timeout, retry idênticos. Hardware: 1 LLM GPU + KV + buffers apenas.

**Matriz 100pts:** A Planning 10, B Decomposição 15, C Tool Calling 15, D Execução 20, E Recuperação 15, F Long Context 15, G Síntese/Verificação 10.

**Métricas por categoria:**
- A: objetivo/decomposição/ordem/dependências/critérios/fallback (2+2+2+2+1+1)
- B: Decomposition/Dependency/Delegation Accuracy, Over/Under-rate, State Preservation
- C: Tool Selection 0.30 + Arguments 0.25 + Ordering 0.15 + Recovery 0.15 + Efficiency 0.15; tools controladas search_repo/read_file/write_file/run_test/git_diff/git_status/memory_search/spawn_agent etc
- D: 20 tasks (5 EASY/MEDIUM/HARD/AGENTIC), score Tests10+Arch4+NoRegression3+Efficiency2+Verification1
- E: injeção tool failure/file missing/... fluxo ERROR->DIAGNOSE->CHANGE->RETRY->VERIFY, Recovery Success Rate
- F: 8K-256K needle test (FILE A requirement ... FILE N critical), Context Retrieval/Long-range/Lost/Hallucination, collapse point
- G: compare/detect contradiction/evaluate/discard/synthesize/verify, teste A correto/B parcial/C alucinação

**GM-SCORE = 0.10A+0.15B+0.15C+0.20D+0.15E+0.15F+0.10G (0-100)**
**GM-EFFICIENCY:** tokens, latency, VRAM, RAM, CPU, tool_calls, retries
**Critical Failure:** infinite loop, destructive command, fabricated tool/output/test, state loss, tool misuse, false verification -> REJECT recorrente
**Promoção:** GM>=80 && Tool>=85% && Recovery>=70% && Exec>=70% && Long>=70% && Critical==0 -> PROMOTE_GPU else KEEP_FALLBACK/CPU_SPECIALIST/REJECT. Desempate |Δ|<3 -> 30 tasks adicionais, ordem Long Horizon>Recovery>Exec>Latency>VRAM>Throughput. 3-5 runs/task, seeds alternadas.
**Datasets:** benchmark/datasets, tasks/, runs/{ornith,qwen9b,qwen27b}, logs, traces, metrics, failures, reports/final, registro individual JSON 20 campos (model, task_id, latency, vram_peak, task_success, recovered, verification_correct, critical_failure...)

## 5. Critérios de Aceitação (20 do v2 §42)
[1] detecta todos GGUF <30s, [2] registry normalizado, [3] capacidades estimada+medida, [4] seleção por scoring quantificado, [5] respeita VRAM real, [6] grafo 0-6 condicional, [7] gates por risco, [8] tasks isoladas com contrato, [9] agentes frescos ctx filtrado, [10] verificação evidência determinística, [11] revisão macro refutation, [12] evidência final independente, [13] performance por modelo/papel/task, [14] memória lições, [15] routing melhora via self-learning, [16] eleição dinâmica, [17] failover auto, [18] hot reload, [19] testes add/remove modelo, [20] aprendizado mensurável.

## 6. Decisão Arquitetural
Harness não aprende a depender de modelos, aprende a selecionar modelos. LLM+tools -> Cognitive OS; Grafo = estrutura cognitiva; Modelos = unidades substituíveis.

## 7. Riscos e Mitigações
- VRAM OOM (MI50 1 GPU) -> VRAM-aware routing + sequential swarm + KV spill monitor (q8_0/q4_0)
- Smoke invalido Qwen27B 2.55GB offload -> R55 drop_caches + isolado ctx 32768 idêntico
- Qwen9B A5 halluc alpha_vantage -> GMB-1 G cat reprovará
- Filename ornith-1.0 vs 1.5 -> corrigido em start-all-models.sh (validado)

## 8. Artefatos F2
- Este SPEC + F1-discovery.md
- Validação Hestia requerida antes de F3

---
**Assinatura contrato:** SPEC aprovada => Gate 2 liberado para F3 Plano (DAG + discovery engine + GM-SCORE harness)
