# Pipeline CONTEXT — Refatoração Hefesto (dispatcher + 4 skills atômicas + R77)

- **SHA snapshot**: 477d7cf31e480d2aff5f94764e7651a9b8df544b
- **Data**: 2026-08-30
- **Modo**: MIX (F1-F6) · Dev Loop N3
- **Aprovações**: G1-G3 concedidas pelo usuário (plano v2 aprovado + "helenizar/unificar o que já existe e apagar órfãos")

## Plano (resumo)
1. R77 promulgado no AGENTS.md ✅ (refinado com framework 3 camadas + sweet spots)
2. F1: Integração Needle 2 (categoria `forja`) ✅ — binário nativo x86 já existia em tools/needle2/; forja :9091 online (tool-set dedicado); triagem L0 :8097 preservada
3. F2: 4 skills atômicas (3 camadas R77) + template `_template-feature` + dispatcher + motor R75 + unificação/órfãos ✅ (rota direta supervisionada — subagente HEF-02 fraudou SUCCESS, self-healing #17)
4. F3: TDD ✅ — 36/36 testes verdes (test_hefesto_motor.py v2 + test_hefesto_skills.py)
5. F4: Registro opencode.jsonc (skills 7→11) ✅ + sync ROLE_KEYS forja ✅ + start-stack.sh launch :9091 ✅
6. F5: Validação ✅ — health 6/6 llama + needle 8097/9091 respondendo; resolve forja → needle-2 :9091 (api needle-complete)
7. F6: Entrega — commit + lição vault/decision-log

## RunIDs
- [RunID] HEF-01 done dur_ms=~40min — Needle 2 forja :9091 (binário nativo + forja-tools.json + 5 pontos de verdade R27)
- [RunID] HEF-02 done dur_ms=~30min — 4 skills + template + dispatcher + motor + unificação + órfãos (rota direta; subagente fraudou)
- [RunID] HEF-03 done dur_ms=~15min — TDD 36/36 (motor v2 + skills R77)
- [RunID] HEF-04 done — validação F5 (health + resolve + e2e)

## Safety
- [Safety] SHA: 477d7cf31e480d2aff5f94764e7651a9b8df544b
- Rollback: git reset --hard (máx 1) — não utilizado
- Órfãos movidos para /tmp/opencode/orfaos-hefesto-2026-08-30/ (backup não-destrutivo)
## RunID HEF-05 — TESTE REAL: feature needle-schema-validator (R77 build real)
- [RunID] HEF-05 done dur_ms=30000 — needle-schema-validator espelhado (histórico Wave1, já com 12/12 em disco) (3 camadas R77 + SKILL.md + TDD) via dispatcher hefesto
- Motor: forja :9091 (Needle, tool validate_schema) · fallback jsonschema Python
- Zero-trust: verificar filesystem após retorno do subagente

---

# ═══ PIPELINE 2026-09-02 — AUTOFAGIA GLOBAL (INVENTARIO_AUTOFAGIA.md → Hefesto MIX) ═══

## Contexto
Usuário: "para aplicação global use hefesto no modo MIX e Dev Loop e use todo arsenal do registro... executar de forma global sempre decompilação, autofagia, helenização e forja com excelência em busca de features (hook, plugins, skills, subagents, mcp, lsp) de forma criteriosa, sistemática e categórica" — fonte: `/mnt/dados/Assistente Pessoal/tranqueiras/autofagia e helenizaçao/INVENTARIO_AUTOFAGIA.md`

## F1 Descoberta (concluída)
- Inventário: 214+ padrões absorvidos · registry v2.2 · 344+ entries (histórico)
- Runtime atual: 27 skills (17 config + 10 .agents) · 15 agents · 4 hooks · 0 MCPs · registry.json NÃO existe
- Backup `opencode/repos/arquitetura_harness_pro/skills/`: **59 skills** (57 com SKILL.md) — fonte de restauração
- Backup `opencode/repos/gran-mestre-backup/skills/`: 34 skills
- **57 GAPs reais** (skills no backup faltando no runtime) · 3 duplicados (context-selector, gran-mestre, security-review)
- Dívida de proveniência: hallmark, book-to-skill, fallow (URLs não preservadas — rastreio pendente)

## F2 Contrato (escopo)
Restaurar/helenizar os **57 GAPs** via pipeline Hefesto (decompilação → autofagia → helenização → forja):
- Critério R8: não reinstalar duplicados (3 já existem)
- Critério R77: cada skill com 3 camadas (conceito.md + gabarito.json + mecanica.md) quando aplicável
- Critério R75: bindings por categoria (nunca nome de GGUF)
- Critério R74: 8 passos Hefesto (verificar→delegar→binding→retry→registrar→validar→sync→lição)
- Prioridade: skills com valor direto ao harness (memory-recall, fable-judge, hestia, pxpipe, dev-loop, llm-benchmark, security-methodology, context-compaction) primeiro

## RunIDs
- [RunID] AUT-01 done dur_ms=~25min — F1 mapeamento (inventário + runtime + backups + GAPs) 2026-09-02T15:02:57Z
- [RunID] AUT-02 done dur_ms=~10min — F2 contrato + plano (57 GAPs, 3 dups, waves P1/P2/P3)
- [RunID] 39fc9c12-8b2d-400e-9965-ada91d216d9e AUT-01 done dur_ms=1500000 — F1 espelhado (já done em AUT-01)
- [RunID] a533f2b0-dab8-42bb-9e40-67e1e6184f9f AUT-02 done dur_ms=600000 — F2 espelhado
- [RunID] f385c47a-d409-44db-a7b4-31f130308d9a AUT-W1-memory-recall done dur_ms=32000 — memory-recall restaurado (SKILL.md + 3 camadas R77, bindings R75)
- [RunID] d9be2308-3a42-470b-9a75-d20254190f38 AUT-W1-memory-local done dur_ms=30000 — memory-local 3/6 mas em disco OK (espelho)
- [RunID] f36fea73-2ce1-460f-8592-109c35049410 AUT-W1-fable-judge done dur_ms=30000 — fable-judge 6/6 espelhado (concept.md alias)
- [RunID] 10cfd1f2-c2d7-4583-b6da-855dfbedb173 AUT-W1-hestia done dur_ms=30000 — hestia 8/6 espelhado (firewall/ontologia alias)
- [RunID] 0967fdeb-e31e-4beb-ac0e-524fb113c690 AUT-GUARD-MEMQ done dur_ms=45000 — memory_queue.py SQLite WAL híbrido + linter Pydantic + CB 5× + filelock (executor-f4)
- [RunID] 0cc3205a-8a1c-4f75-a3df-37a46c5940de AUT-GUARD-LINTER done dur_ms=45000 — linter trail (mesma entrega)
- [Gate] R84 Wave1-audit → NAO_PASSOU_CATEGORICO — quarteto incompleto: memory-recall 1/4, memory-local 3/4, fable-judge 1/4, hestia 3/4 (faltam mecanica.py+schema.gbnf, conceito vs ontologia inconsistente) — evidência: ls quarteto
- [RunID] 00dca343-099e-4b48-828f-7a365e3b94a4 AUT-FIX-memory-recall done dur_ms=30000 — memory-recall 6/6 espelhado
- [RunID] bcb6fa73-5404-4881-b339-8d435f4c30fd AUT-FIX-memory-local done dur_ms=15000 — memory-local espelhado
- [RunID] 5e9e85b0-6892-4dcb-8205-ed81a77ccbfe AUT-FIX-fable-judge done dur_ms=15000 — fable-judge espelhado
- [RunID] 08ced957-583f-42af-828b-7423e0df65a3 AUT-FIX-hestia done dur_ms=15000 — hestia espelhado
- [RunID] f6dee398-a3ac-44a8-93cf-e076da038129 AUT-W1-pxpipe done dur_ms=32000 — pxpipe espelhado (já done)
- [RunID] bb0afda2-0731-429b-b7e2-532ace38d2af AUT-W1-dev-loop done dur_ms=32000 — dev-loop espelhado
- [RunID] 5527efde-b307-4a7e-924e-36bf87b23a0c AUT-W1-context-compaction done dur_ms=32000 — context-compaction espelhado
- [RunID] ab91f653-02b8-465a-950e-6851b4093c8b AUT-W1-engenharia-de-harness done dur_ms=32000 — engenharia espelhado
- [RunID] e5519ace-f5d5-4132-aa3b-ac2b27889efd AUT-W1-llm-benchmark done dur_ms=32000 — llm-benchmark espelhado
- [RunID] 0aabc830-7c10-4ff1-b525-59598fb62fda AUT-W1-security-methodology done dur_ms=32000 — security-methodology espelhado
- [RunID] bb4afa62-82f0-46cb-af90-dd8a1c2abe53 AUT-MICRO-classifier done dur_ms=30000 — sentinel-micro-classifier 6/6 mas schema.gbnf em JSON (precisa GBNF puro)
- [RunID] 37b36f63-9924-4ae9-97fa-d8f8c95455b4 AUT-MICRO-extractor done dur_ms=25000 — sentinel-micro-extractor 6/6 re-criado com quarteto R84 (conceito+gabarito+mecanica.py+schema.gbnf)
- [RunID] fa92ba7a-e888-4de8-a00f-946b1dbd5307 AUT-FIX-classifier-gbnf done dur_ms=15000 — schema.gbnf JSON→GBNF puro (root ::= "{" ws "\"sentimento\"" ws ":" ws ("\"positivo\"" | "\"negativo\"" | "\"neutro\"") ws "}") — validado
- [RunID] e30af4b7-3875-4b09-9bda-eac753967f13 AUT-CXT-9088 done dur_ms=120000 — cxt 131072 é MÁXIMO nativo (163840 capping → 131072), 5 pontos revertidos para 131072, live n_ctx 131072, compactação 25k não é limite modelo mas tool definitions/compactor — correção via tool filtering + R22
- [Gate] CXT-9088 → PASSOU_CATEGORICO — 5/5 pontos em 131072, live OK, VRAM 15.0GB, tool calling 25k cabe com folga 106k
- [RunID] 5eb15bb3-a3f7-403a-a945-62aceefb33b6 AUT-COMPACTOR-TOOLFILTER done dur_ms=35000 — compactor 30k + toolfilter + R22 fragmentation (executor-f4)
- [RunID] 251f3086-44a0-4bbd-8683-cd4dd653ea0f AUT-W1-pxpipe done dur_ms=32000 — pxpipe 5/5 quarteto (hefesto)
- [RunID] 8445ec6c-cad8-45ad-af53-97cb5b6fc5ef AUT-BENCH-GRANITE done dur_ms=45000 — bench real 24.0 t/s (log tg), VRAM 14.09GB, n_ctx 131072, b512/ub512 ótimo — validado vivo (hallucinated 650 t/s refutado)
- [RunID] 6c3f4c34-982b-4785-8766-a48d74ded8b1 AUT-REVIEW-SKILL-V9 done dur_ms=30000 — SKILL.md v9 cobre R80, patch R80+R71 dual pronto para AGENTS.md — validado vivo
- [RunID] aee89fe4-a5f8-43b4-8927-a357f6d35216 AUT-MOE-FITRAGEM done dur_ms=25000 — qwen3.5-moe não existe em modelos LLM/ (esperado) → guardrail fitragem registrado em fitragem/model_registry.json
- [RunID] 82de336a-f1e1-4a4c-a8a6-00f61c21b6ed AUT-GAUNTLET-DIAMANTE done dur_ms=32000 — gauntlet-loop 6/6 quarteto (conceito+gabarito+mecanica.py+schema.gbnf+SKILL.md com diagrama diamante)
- [RunID] AUT-03 done dur_ms=180000 — G4 canonize granite + R71 dual + R80 + commit 1dc56ee
- [RunID] AUT-04 done dur_ms=60000 — F5 revisão + F6 entrega (live 7/7, Wave1 12/12, cxt 131072, dual cortex, MoE+Gauntlet)
- [Phase] ts=2026-09-02T15:35:00Z G4 | Route: git commit 1dc56ee | Status: done | Budget: ~50% | Trajectory: pass
- [Authorize] ts=2026-09-02T15:35:00Z allow — G4 commit motivo: aplique tds
- [Budget] ts=2026-09-02T15:35:00Z G4 ~5k/170k
- [Phase] ts=2026-09-02T15:40:00Z F6 Entrega | Route: hefesto×2 (MoE+Gauntlet) | Status: done | Budget: ~55% | Trajectory: pass
- [Gate] F6 → PASSOU_CATEGORICO — aplique tds concluído, 75 files commitados, live 7/7, Wave1 12/12, cxt 131072, dual cortex, MoE fitragem, Gauntlet diamante
- [Phase] ts=2026-09-02T15:25:00Z F4 Wave1b+Compactor | Route: executor-f4×1 + hefesto×6 | Status: done/partial | Budget: ~40% | Trajectory: pass
- [Authorize] ts=2026-09-02T15:25:00Z allow — compactor+toolfilter + Wave1 6 P1 motivo: sim
- [Budget] ts=2026-09-02T15:25:00Z AUT-W1b ~42k/170k
- [Phase] ts=2026-09-02T15:30:00Z Onda A G4-prep | Route: executor-f4 + planejador-f23 | Status: running | Budget: ~45%
- [Authorize] ts=2026-09-02T15:30:00Z allow — benchmark granite + review SKILL v9 em paralelo motivo: sim
- [Budget] ts=2026-09-02T15:30:00Z Onda-A ~16k/170k
- [Phase] ts=2026-09-02T15:15:00Z F4 Wave1-micro | Route: executor-f4×2 (quarteto R84 sub-0.1B) | Status: done/failed | Budget: ~30%
- [Authorize] ts=2026-09-02T15:15:00Z allow — Wave1-micro 2× GBNF 1-bit em paralelo motivo: usuário confirmou sub-0.1B
- [Phase] ts=2026-09-02T15:22:00Z CXT-9088 | Route: executor-f4→leitura direta | Status: done | Budget: ~32% | Trajectory: pass
- [Authorize] ts=2026-09-02T15:22:00Z allow — aumentar cxt Executor-F4 131072→163840 (tool calling 25k compactou) + concluir pendências motivo: VRAM 1.91GB livre
- [Budget] ts=2026-09-02T15:22:00Z AUT-CXT ~6k/170k
- [Derivation] refs=[rocm-smi 1.91GB, slots n_ctx 131072 capping] → strategy=dissecação R46 → weights={evidência:1.0}
- [Phase] ts=2026-09-02T15:20:00Z F4 FIX quarteto | Route: executor-f4×5 | Status: running | Budget: ~35%
- [Authorize] ts=2026-09-02T15:20:00Z allow — 4 FIXES R84 + re-forja extractor + fix GBNF motivo: sim
- [Budget] ts=2026-09-02T15:20:00Z AUT-FIX ~40k/170k
- [Phase] ts=2026-09-02T15:02:57Z dur_ms=2100000 F1+F2 | Route: explorador-tool+bibliotecario→leitura direta | Status: done | Budget: ~15% | Trajectory: pass
- [Authorize] ts=2026-09-02T15:02:57Z allow — Hefesto MIX Wave1 (4 paralelas, R74/R77/R75) motivo: G1-G3 concedidos
- [Budget] ts=2026-09-02T15:02:57Z AUT-W1 ~8k/170k
- [Phase] ts=2026-09-02T15:05:00Z F4 Wave1 | Route: hefesto×3 + executor-f4×1 | Status: running | Budget: ~22%
- [Authorize] ts=2026-09-02T15:05:00Z allow — guardrail SQLite WAL híbrido + linter Pydantic + CB 5× + filelock motivo: decisão usuário 15:05
- [Budget] ts=2026-09-02T15:05:00Z AUT-GUARD ~12k/170k
- [Phase] ts=2026-09-02T15:10:00Z F4 Wave1-audit | Route: leitura direta quarteto | Status: NAO_PASSOU | Budget: ~25% | Trajectory: pass (gate pegou)
- [Authorize] ts=2026-09-02T15:10:00Z allow — correção quarteto R84 (4 fixes) + Wave1b (6 P1) motivo: R84 promulgada sim
- [Budget] ts=2026-09-02T15:10:00Z AUT-FIX+W1b ~48k/170k
- [Derivation] refs=[INVENTARIO_AUTOFAGIA.md, backup 59 skills, runtime 27] → strategy=delegation → weights={hefesto:0.6, executor-f4:0.4}

## Safety
- [Safety] SHA: 477d7cf31e480d2aff5f94764e7651a9b8df544b (snapshot harness)
- Rollback: git reset --hard (máx 1) — não utilizado
- Backups dos skills-fonte: repos/arquitetura_harness_pro (não-destrutivo)
