# SPEC — Ecossistema do Harness (Gran-Mestre / OpenCode Local-First)

- **Data**: 2026-08-18 · **Autor**: Gran-Mestre (ornith-1.0-9B, :8083)
- **Escopo**: visão integrada do ecossistema completo — regras, hardware, stack, agentes, skills, hooks, memória, pipeline
- **Estado**: vigente; mudanças estruturais → atualizar este SPEC (R51: catalogar na biblioteca)

---

## 1. Objetivo

Harness híbrido local-first de orquestração de IA: o **Gran-Mestre** (único agente primário,
R39) orquestra subagentes descartáveis, com regras constitucionais (R1-R51), stack de LLMs
locais (GPU+CPU), memória cerebral Obsidian e pipeline de 6 fases com gates humanos.

## 2. Hardware

| Recurso | Especificação |
|---|---|
| CPU | X99 (C612), 36 threads (18 físicos + HT), DDR4 quad-channel |
| RAM | 31 GiB (swap 31 GiB) |
| GPU | AMD MI50 16 GiB (gfx906, HSA_OVERRIDE_GFX_VERSION=9.0.6, backend Vulkan) |
| Disco | /mnt/dados 120 GB (NVMe; 32 GB livres em 2026-08-18) |

## 3. Regras (biblioteca em `/mnt/dados/opencode/config/rules/` — R51)

| Arquivo | Conteúdo |
|---|---|
| `AGENTS.md` | Bootstrapper global R1-R51 (essência, 156 linhas) — carregado em TODA sessão |
| `global-rules.md` | Índice agregador (tabela regras→módulos) |
| `modules/01-constituicao-nucleo.md` | R1-R14: orquestração, delegação, catálogo, saúde, VRAM |
| `modules/02-orquestracao-workflow.md` | R16-R20: workflow contínuo, bipolar, circuit-breaker, stack on/off, fallback nuvem |
| `modules/03-rota-janela-vram.md` | R21-R23: VRAM ativa, fragmentação, roteamento por janela |
| `modules/04-workflow-6-fases.md` | R25-R28: F1-F6+G1-G4, memória Obsidian, sync 5 pontos, trânsito categórico |
| `modules/05-metricas-validacao.md` | R34-R42: métrica 0-100, visão, autofagia, A2A, refutação incansável |
| `modules/06-governanca-scaffolding.md` | R43-R51: autonomia, scaffolding global, benchmarks, dissecação, watcher, catalogação |
| `modules/legado/` | Regras antigas R45-R51 (não vigentes, histórico) |
| `CLAUDE.md` / `vault-AGENTS.md` | Preferências do usuário / regras do vault |
| `README.md` | Índice + procedimento R51 |

## 4. Stack de LLMs (ctx-catalog — R27)

| Modelo | Local | Porta | Ctx | Papel |
|---|---|---|---|---|
| ornith-1.0-9B Q4_K_M (5,4 GB) | GPU | 8083 | 262K | **Gran-Mestre** (R39) — ~77 t/s |
| Bonsai-27B 1-bit (3,6 GB) | CPU | 9083 | 16K | Fase 1 criativa — ~6 t/s |
| qwen3.5-0.8B (0,5 GB) | CPU | 9084 | 262K | Nível 1 generalista — ~211 t/s |
| jamba-reasoning-3b (1,8 GB) | CPU | 9085 | 262K | Fases 3-4 plano/exec — ~7 t/s |
| LFM2.5-230M (0,14 GB) | CPU | 9086 | 128K | Refutação R42 — ~824 t/s |
| granite-4.1-3b (2,0 GB) | CPU | 9087 | 131K | Nível 2 código/tools |
| MiniCPM5-1B (0,66 GB) | CPU | 9088 | 131K | Nível 1.5 tools |
| Ollama :11434 | — | — | — | qwen3.5:0.8b (visão), nomic-embed, qwen2.5-coder:7b |

**5 pontos de verdade (R27)**: `harness/ctx-catalog.json` · `opencode.json` · `oh-my-openagent.json` · `start/stop-all-models.sh` · `llama_budget.py` (+ AGENTS.md §13)

## 5. Modelos em avaliação (bateria de testes 2026-08-18)

| Modelo | Tamanho | GPU 100% (MI50) | Veredito |
|---|---|---|---|
| Qwen3.8-27B Q4_K_M | 16 GB | OOM (não cabe) | híbrido -ngl 50 = 3,13 t/s |
| Qwen3.8-27B UD-IQ3_XXS | 12 GB | ✅ 16,5 t/s | estável, boa |
| **Qwen3.8-27B Ridge 3.7bpw** | 12,6 GB | ✅ **19,5 t/s** (decode 25) | **melhor quant 27B** (arquitecture-aware, Empero) |
| Qwen3.8-27B UD-IQ2_XXS | 9 GB | 9,9 t/s — **LOOP** | ❌ reprovada (2,06 bpw) |
| Qwen3.8-9B Distilled Q4_K_M | 5,8 GB | em teste | candidata vs LLM Orquestrador (ornith-1.0-9B) |
| Qwen3.8-4B Distilled Q4_K_M | 2,5 GB | em teste | laptop-class |
| CPU puro (Q4_K_M 27B) | — | — | 1,18-1,25 t/s (teto banda) |

## 6. Pipeline Gran-Mestre (6 fases — R25)

F1 Descoberta → G1 · F2 Contrato → G2 · F3 Plano (+SHA) → G3 · F4 Execução (TDD, commits atômicos, sem gates) · F5 Revisão Macro · F6 Entrega (evidência fresca + memória cerebral) → G4

## 7. Subagentes (61+ descartáveis — R1/R17)

Pipeline (prometheus, hestia, atlas, atena, atreus, code-reviewer) · Crossover (oh-my-openagents, superpowers, fable-method) · GSD (35) · OpenCode (memory-keeper, reverser, general) · Externos (agent-evaluator, build-error-resolver, contextscout, hookify) · A2A/R40 (refutação incansável entre modelos)

## 8. Skills (catálogo global — R36)

`~/.config/opencode/skills/` + `/mnt/dados/opencode/skills/` — 100+ helenizadas: gran-mestre, hestia, athena, fable-judge, silverhawk (visão), memory-recall, professional-decompilation, security-research, caveman, context-compaction, omniroute, dev-loop, threejs-game-harness, **self-scaffold-guard (nova 2026-08-18)**, etc.

## 9. Hooks (lifecycle — R33/R48)

session.start (stack-auto-start, memory_inject, auto-sync-models) · helenize-* (40+) · prepare-commit-msg (sensitive-data) · gsd-* (workflow-guard, prompt-guard) · watcher vigilante (R48)

## 10. Memória Cerebral (R26 — vault Obsidian)

`/mnt/dados/cerebro com IA/` — raw/ (imutável) · wiki/ (summaries, concepts, entities, evidence, log.md) · aprendizados/ · decisoes/ (R50, R51 registradas) · pipeline/ · cerebral.db

## 11. Regras de ouro operacionais

- **R1**: orquestrador nunca executa trabalho bruto (delega sempre que há recurso)
- **R18**: circuit-breaker (3 falhas/300s → rollback máx 1 → gate humano)
- **R19**: stack on/off via scripts (nunca pkill solto)
- **R28**: trânsito categórico (PASSOU_CATEGORICO / NAO_PASSOU + evidência)
- **R50**: dúvida no escopo → MIX (≥2 rodadas multi-idioma) + vault em paralelo
- **R51**: regra nova → biblioteca rules/ (≤200 linhas, frontmatter tema/categoria/setor/escopo)

## 12. Pendências abertas (2026-08-18)

1. Testes pendentes: Ridge qualidade (rodado — ler), Qwen3.8-9B/4B Distilled (baixando), re-teste IQ2_XXS sozinho (contaminação anterior)
2. 3 transcrições YouTube (429): Y8g4NMB-3Mg, mYx-bhBcwrU, AZTvioP2snU
3. Skill self-scaffold-guard — validar empiricamente (R14)
4. Decidir integração do Ridge na stack oficial (R27: 5 pontos de verdade + hot-swap R21)

## 13. Padrão de temperatura de orquestração (2026-08-18)

- **0,2-0,3** em TODOS os payloads de delegação/orquestração (sintaxe estrita do harness, grafos, JSON — determinismo)
- Aplicado: bench_kv.py, verify_tput.py (0.7 → 0.3); validação de saúde 0.1; agentes OpenCode herdam config
- Exceções: Fase 1 criativa (bonsai) pode usar 0,7+; refutação A2A (R40) pode variar

## 14. Padrão de requisição de orquestração (2026-08-18)

- **thinking OFF por padrão**: `"chat_template_kwargs": {"enable_thinking": false}` em TODOS os
  payloads para a família Qwen3/3.5/3.8 (LLM Orquestrador, bonsai, qwen-0.8B, 2B, 1.7B, 9B, 4B, Ridge).
  Sem isso: content vazio + reasoning_content (quebra parsing de ferramentas/JSON).
- Exceção: quando raciocínio explícito for desejado (Fase 1 criativa, refutação profunda),
  ligar thinking e extrair content (cortar reasoning_content).
- Temperatura 0,2-0,3 (determinismo) — ver §13.
