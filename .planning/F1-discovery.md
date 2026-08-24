# F1 — Descoberta MIX+Vault — Meta-Orquestrador Adaptativo Modular
**Data:** 2026-08-23T16:22
**Fontes:** PRD v1 (2171L) + PRD v2 Refatorado (1960L) + GMB-1 (897L) + Vault + Arsenal

## 1. MIX (2 rodadas multi-idioma) + Vault paralelo
- Buscas: ornith self-scaffolding, model discovery, VRAM routing, helenização, benchmark harness
- Vault recall: `memória: meta-orquestrador` -> 64KB cerebral.db + hot.md (1821 chars = sem contexto relevante)
- Dissecação: família priors Qwen/Bonsai/Ornith/Phi, quant penalty Q4 0.95 -> IQ2_XXS 0.65

## 2. PRD v1 vs v2 — delta
| Dimensão | v1 | v2 Refatorado |
|---|---|---|
| Papel | Modelo≠Papel | Modelo≠Papel≠Fase |
| Eleição | estática (Ornith 9B fixo) | dinâmica Primary/Secondary + failover 30s*3 |
| Grafo | 0-6 linear | FAST(0>4>6)/STANDARD/FULL condicional via classificador lfm2.5-230m |
| Discovery | scan->GGUF->VRAM | + checksum + backend compat + exclusion_rules(vram>0.9, corrupted) |
| Registry | yaml simples | + hot reload inotify debounce5s + MODEL_REMOVED_DURING_EXECUTION |
| Capability | estimated | 2 camadas confidence=measured/(measured+10) + micro-bench 5 prompts |
| Routing | capability_fit | MODEL_SCORE = 0.30cap+0.25task+0.15ctx+0.15res+0.10hist+0.05verif -0.10cost -0.05risk |
| Swarm | fixo | dinâmico por task (planner/coder/critic/judge), sequencial se VRAM=1 |
| Plugins | monolito | estratificado tools/mcps/lsps/skills/hooks + lifecycle |
| Observability | logs | dashboard tempo real + event log SQLite + audit trail INPUT>STATE>CANDIDATES>SCORES>DECISION>RESULT |

## 3. GMB-1 — 3 candidatos GPU_PRIMARY_SLOT (MI50 16GB, 1 LLM GPU only)
- Ornith-1.5-9B Q4 5.3GB ctx131K VRAM8.5GB decode69t/s prefill414t/s — 4/5 smoke (A1 fail raw vazio)
- Qwen3.8-9B Q4 5.4GB ctx131K VRAM10.7GB decode97t/s prefill423t/s — 3/5 smoke (A5 critical halluc alpha_vantage)
- Qwen3.8-27B IQ2_XXS 8.4GB ctx196K VRAM12.6GB decode28t/s — smoke pending (server DOWN antes), CPU 8192: 15.14 prompt / 3.06 decode

Matriz 7 cats 100pts: A10 Planning + B15 Decomp + C15 Tool + D20 Exec + E15 Recovery + F15 LongCtx + G10 Verify
GM-SCORE + GM-EFFICIENCY (tokens/latency/VRAM/RAM/CPU/tool_calls/retries)
Promoção: GM>=80 + Tool>=85% + Recovery>=70% + Exec>=70% + Long>=70% + 0 critical -> PROMOTE_GPU else KEEP_FALLBACK/CPU_SPECIALIST/REJECT
Flow: Critical?->REJECT : GM>=80?->Tool?->Recovery?->Exec?->PROMOTE else FALLBACK
Incoerência detectada: Qwen27B smoke 2.55GB (offload RAM, não GPU) + A1 timeout 90s EXIT124 — refazer isolado R55 drop_caches

## 4. Arsenal inventariado
- Hooks: 53 -> 51 base + silverhawk etc (skill count 133)
- Skills: 133 (llm-benchmark v2 bench.py/smoke.py/throughput.py/ctx-cost.py + 5 fixtures)
- Subagents: 79 (gsd-* + fallow + general) 76 agents no oh-my-openagent.json (local primary + omniroute fallback)
- MCP: 5 (ghidra remote, openwork, obsidian local, siz_delimiter, codegraph)
- LSP: configs via oh-my-openagent (qwen 9084, lfm 9086 etc)
- VRAM: MI50 16GB, GPU Ornith 14.9GB + CPU 6/6 UP (9083-9088), :8083 131072 :8090 ex-Qwen agora morto (realloc p/ Ornith)
- 86k restaurado: global-rules 82.228 + AGENTS-global 41.600 = 123828

## 5. Riscos abertos
- Smoke Qwen27B invalido (server DOWN) -> refazer F4 GMB-1 1/3 Ornith @8083, 2/3 Qwen9B @8090, 3/3 Qwen27B @8090 isolado
- CPU Qwen9B 8192 medido 3.06t/s vs GPU 97t/s = 32x gap -> confirma t18 fisico R56
