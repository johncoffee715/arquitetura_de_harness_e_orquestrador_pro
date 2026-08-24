# F3 — PLANO — Meta-Orquestrador Adaptativo Modular + GMB-1

**Data:** 2026-08-23T16:35
**Contrato base:** F2-contrato-SPEC.md (PRD v1+v2+GMB-1)
**Descoberta base:** F1-discovery.md (3379 bytes)
**Stack verificado:** CPU 7/7 UP (9083 Bonsai 16K, 9084 Qwen0.8B 131K, 9085 LLMJudge 32K, 9086 LFM230M 128K, 9087 Qwen2B 262K, 9088 Qwen1.7B 32K) + GPU Ornith 1.5-9B 131K 14.9GB UP :8083

---

## 1. DAG do Grafo Cognitivo (F0→F6 condicional)

```mermaid
F0(INTAKE: classificador lfm2.5-230m) --> C{complexity/risk/ambiguity}
C -->|low+low+low| FAST: F0->F4->F6 (G0 auto, G3 SHA, G4)
C -->|medium| STD: F0->F1->F2->F3->F4->F5->F6 (G1-4)
C -->|high| FULL: F0->F1+brainstorm(Primary Qwen9B/Secondary Ornith/Critic Bonsai8B/Judge LLMJudge) ->F2+audit ->F3+refutation ->F4+micro-review ->F5 macro-refutation ->F6 verif independente (G1-4)
```

**Gates:**
- G1 Direção (F1→F2) — Hestia: valida escopo/risco, FAST auto-aprova
- G2 Spec (F2→F3) — Hestia: valida SPEC vs pedido, FAST auto se sintático OK
- G3 Plano+SHA (F3→F4) — Hestia + `git rev-parse HEAD` save, FS 0-3 READ-ONLY enforcement
- G4 Final (F6) — Hestia+Atena+fable-judge: evidência ferro + GM-SCORE

## 2. Registry — Schema Normalizado

```yaml
registry_version: "2026-08-23T16:35Z"
models:
  ornith-1.5-9b-q4km:
    path: "/mnt/dados/Assistente Pessoal/modelos LLM/Ornith-1.5-9B-Q4_K_M.gguf"
    file: {size_bytes: 5300000000, checksum: sha256, last_modified: iso8601}
    architecture: {family: ornith, type: decoder-only, parameters: 9000000000, quantization: Q4_K_M, context_length: 131072, embedding_dim: 4096, vocab_size: 152064}
    backend: {format: gguf, compatible: [llama.cpp], chat_template: jinja+reasoning-preserve}
    resources: {estimated_vram_gb: 8.5, estimated_ram_gb: 5.5, gpu_compatible: {mi50_gfx906: true}}
    capabilities:
      estimated: {reasoning: 0.85, coding: 0.78, planning: 0.84, tool_use: 0.82, analysis: 0.84, speed_tps: 69}
      measured: {reasoning: null, coding: null} # preenchido após GMB-1
      confidence: 0.0 # measured/(measured+10)
    roles_suitability: {planner: 0.88, orchestrator: 0.90, reviewer: 0.82, coder: 0.78, critic: 0.80, judge: 0.70}
    performance_history: {total_tasks: 0, success_rate: 0, avg_latency_ms: 0, verification_pass_rate: 0}
    health: {status: GREEN, last_check: iso8601, consecutive_failures: 0, oom_events: 0}
    status: {available: true, healthy: true, excluded: false}
```

**Exclusion rules:** vram_required > vram_available*0.9, file_corrupted, metadata_unreadable, backend_incompatible, user_blacklisted -> excluded=true (permanece no diretório)

**Hot reload:** inotify/polling debounce 5s -> re-run discovery arquivo afetado -> registry update -> recompute router caches -> se model_in_use removido -> FALLBACK + MODEL_REMOVED_DURING_EXECUTION

## 3. Discovery Engine — Pipeline

```
scan directory /mnt/dados/Assistente Pessoal/modelos LLM/*.gguf
  ↓ extract GGUF metadata (llama.cpp metadata API)
  ↓ validate checksum parcial
  ↓ estimate base capabilities = family_prior * quant_penalty * param_scaling(log) * context_bonus(>64K +0.05)
      family_priors: qwen 0.82/0.85/0.80/0.86, bonsai 0.88/0.65/0.60/0.80, ornith 0.85/0.78/0.82/0.84, phi 0.75/0.70/0.65/0.72
      quant_penalty: Q4 0.95, Q3 0.88, Q2 0.75, IQ2_XXS 0.65
  ↓ estimate VRAM (params*quant + KV ctx*arch) -> check ROCm gfx906 -> update registry
  ↓ [OPCIONAL] micro-bench 5 prompts (reasoning/coding/tool_call/summarization/refutation) 120s max, static verification
  ↓ update confidence
```

**Implementação F4:** `harness/models/discovery.py` + `metadata.py` + `profiler.py` + `benchmark.py::micro` + `cache_manager.py` (VRAM load/offload, LRU preditiva task graph, N=1 MI50)

## 4. VRAM-Aware Routing

**Monitor contínuo:**
```
VRAM_AVAILABLE = 16GB - USED(rocm-smi) - 2GB SYSTEM_RESERVE
MODEL_ESTIMATE = registry.resources.estimated_vram_gb
KV_ESTIMATE = f(prompt+output+tool+retrieved, arch)
SAFE_LOAD = AVAILABLE >= MODEL + KV + 1GB RESERVE
```

**MODEL_SCORE por task:**
```
SCORE = 0.30*capability_fit + 0.25*task_fit + 0.15*context_fit + 0.15*resource_fit + 0.10*historical + 0.05*verification -0.10*cost -0.05*risk
```
Todos [0,1] normalizados. Router escolhe BEST FOR THIS TASK, não BEST ABSOLUTELY. Se SAFE_LOAD false -> escolhe menor que cabe (teoricamente melhor perde p/ menor). Fallback estratificado: PRIMARY (fit>=0.8) -> SECONDARY (fit>=0.8) -> TERTIARY (>=0.6) -> DEGRADED (reduz escopo) -> HUMAN

**Context-aware:** se KV_ESTIMATE > context_length -> seleciona maior context_length OU trunca/compacta OU divide sub-tasks

## 5. GMB-1 Benchmark Harness — Matriz 7 categorias (100pts)

| Cat | Peso | O que mede | Artefato |
|-----|------|-----------|----------|
| A Planning | 10 | objetivo/decomposição/ordem/dependências/critérios/fallback (2+2+2+2+1+1) | design.md/spec.md |
| B Decomp | 15 | Decomposition/Dependency/Delegation Accuracy, Over/Under-rate, State Preservation | task graph |
| C Tool | 15 | Selection 0.30+Args 0.25+Order 0.15+Recovery 0.15+Efficiency 0.15 (tools: search_repo/read_file/write_file/run_test/git_diff/git_status/memory_search/spawn_agent) | traces |
| D Exec | 20 | 20 tasks (5 EASY/MEDIUM/HARD/AGENTIC) Tests10+Arch4+NoRegression3+Eff2+Verif1 | repo real + tests |
| E Recovery | 15 | injeção tool failure/file missing/... fluxo ERROR->DIAGNOSE->CHANGE->RETRY->VERIFY, Recovery Success Rate | failures/ |
| F LongCtx | 15 | 8K-256K needle (FILE A req ... FILE N critical), Retrieval/Long-range/Lost/Halluc, collapse point | long ctx logs |
| G Verify | 10 | compare/detect contradiction/evaluate/discard/synthesize/verify (A correto/B parcial/C alucinação) | reports/ |

**GM-SCORE = 0.10A+0.15B+0.15C+0.20D+0.15E+0.15F+0.10G (0-100)**
**GM-EFFICIENCY:** tokens, latency, VRAM, RAM, CPU, tool_calls, retries

**Promoção GPU_PRIMARY_SLOT:**
```
Critical? -> REJECT
GM<80? -> FALLBACK
Tool<85%? -> FALLBACK
Recovery<70%? -> FALLBACK
Exec<70%? -> FALLBACK
Long<70%? -> FALLBACK
=> PROMOTE_GPU
Desempate |Δ|<3 -> +30 tasks, ordem LongHorizon>Recovery>Exec>Latency>VRAM>Throughput
3-5 runs/task, seeds alternadas, ordem modelos alternada
```

**Candidatos já com dados parciais:**
- Ornith 69t/s 8.5GB 4/5 smoke (A1 fail raw vazio) -> estimativa GM 80-85
- Qwen9B 97t/s 10.7GB 3/5 smoke (A5 critical alpha_vantage) -> GM penalizado
- Qwen27B 28t/s 12.6GB smoke pending (2.55GB offload incoerência) -> refazer isolado R55 drop_caches ctx 32768 idêntico

**Estrutura dados:** benchmark/{datasets,tasks,runs/{ornith,qwen9b,qwen27b},logs,traces,metrics,failures,reports/final}, registro JSON 20 campos, harness skill `llm-benchmark`: bench.py (T1 KV 12k + invariante, T2 JSON coleira, T3 volatile), smoke.py (A1-A5 <30s), throughput.py, ctx-cost.py, R55 drop_caches

## 6. Arsenal — Decompilação/Autofagia/Helenização (categórico)

Inventário base (fatiado do slim): skills 133, subagents 79, hooks 53, MCP 5 (ghidra, openwork, obsidian, siz_delimiter, codegraph), LSP via oh-my-openagent, 86k restaurado.

**F4 helenização MIX+Dev Loop (excelência verificável: frontmatter parseável + TDD passa + registry + commit atômico + fable-judge/Atena):**
- hooks: completar 3 ausentes (VRAM guard já existe, falta: audit trail hook, self-improvement policy hook)
- plugins: tools/mcps/lsps/skills/hooks lifecycle managers (harness/plugins/{tools,mcps,lsps,skills}/)
- skills: gap = skill `model-discovery` + `vram-router` (não existem) -> helenizar de `agent-reach`/`firecrawl` pattern
- subagents: `model-profiler`, `health-monitor` (gap)
- MCP: `obsidian_sync` já existe, gap `health` MCP
- LSP: `diagnostics` gate já em `lsp_gate.py`, gap `completions` LSP
- features: `conditional graph` engine, `election` failover

Todos com TDD: `harness/tests/test_discovery.py` etc, + smoke 5 testes, + fable-judge

## 7. Task Graph F4 (DAG real)

```
T4.1 discovery.py + metadata.py (scan *.gguf, 30s detect) -> evidência: registry.json com 17 modelos
T4.2 profiler.py + family priors (helenizado) -> evidência: capabilities estimated
T4.3 benchmark.py micro 5 prompts (opcional 120s) -> evidência: measured update
T4.4 router.py + VRAM-aware (rocm-smi) + MODEL_SCORE -> evidência: routing unit tests
T4.5 graph_engine.py (DAG, conditional, retries, gates) -> evidência: test_graph fast/standard/full
T4.6 GMB-1 runs isolados R55 (1 GPU por vez, ctx 32768 idêntico, drop_caches) -> evidência: results/*.json + matriz_final.md
  T4.6a Ornith @8083
  T4.6b Qwen9B @8090
  T4.6c Qwen27B @8090 (após kill anterior)
T4.7 CPU fallback t/s ctx 8192 isolado :18083/:18084 (Qwen9B já 3.06t/s, Qwen27B ~1.5t/s) -> evidência: timings
T4.8 helenização hooks/plugins/skills/MCP/LSP (autofagia) -> evidência: frontmatter + registry rebuild
Dependências: T4.1->T4.2->T4.3->T4.4->T4.5->T4.6a/b/c (sequencial GPU) ->T4.7 (paralelo CPU) ->T4.8
Commits atômicos 1 task -> 1 commit, verificação determinística (compiler/test/linter) antes de LLM verifier
```

**Estimativa recursos:** VRAM 14.9GB Ornith, testes 20+10 tasks *3 runs = 90 execuções, ~2h total, RAM 31GB suficiente, CPU 18t

## 8. Gates & Verificação
- F3->F4: Gate 3 Hestia + SHA `git rev-parse HEAD` (FS 0-3 READ-ONLY)
- F4 micro-review por task (complexity>low) -> REVIEWER+REFUTER+FIXER+VERIFIER (determinístico primeiro)
- F5 Atena macro: FULL DIFF PRE_SHA..HEAD, cross-task coherence, coupling, contract audit vs SPEC, macro refutation -> PASS/PASS_WITH_WARNINGS/FAIL->replan
- F6 fable-judge adversarial re-executa testes críticos do zero + verifica GM-SCORE >=80 etc

## 9. Entrega F6
`GMB-1 FINAL REPORT` com GRAN MASTER RANK 1/2/3, GM-SCORE quebra A-G, Long Horizon, Latency, VRAM/RAM, perfil individual, decisão PROMOTE_GPU/KEEP_FALLBACK/CPU_SPECIALIST/REJECT + fluxograma §17, + memória Obsidian (`/mnt/dados/cerebro com IA/` Projects/Models/Benchmarks)

---
**Próximo:** F4 Execução — implementar T4.1-T4.8 com TDD, commits atômicos, evidência ferro, sem tocar código produtivo em F3 (apenas plano)
