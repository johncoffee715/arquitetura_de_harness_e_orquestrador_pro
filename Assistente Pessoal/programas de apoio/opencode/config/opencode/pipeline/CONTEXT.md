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
- [RunID] e783e368-c374-4125-9e17-0898c792c3cd AUT-W2-agentic-awesome-skills done dur_ms=35000 — agentic-awesome-skills 6/6 GBNF travado (correção loop)
- [RunID] 63b22091-6424-492b-816b-3a61885dbcd3 AUT-W2-agent-reach done dur_ms=35000 — agent-reach 6/6
- [RunID] 1388dd1f-d241-4545-ad1b-7fb0abb1db02 AUT-W2-ai-agent-book done dur_ms=35000 — ai-agent-book 6/6
- [RunID] a8da2f63-372c-4125-a4b5-9274c5ba823e AUT-W2-anthropics-skills done dur_ms=35000 — anthropics-skills 6/6
- [RunID] f1671138-0e59-4e0e-b49e-30c93f001318 AUT-W2-archify done dur_ms=35000 — archify 6/6
- [RunID] baf91086-95d5-4ea3-a157-3ec7191d3114 AUT-W2-athena done dur_ms=35000 — athena 6/6 GBNF travado
- [RunID] fd7813e1-df74-4e7e-9d39-ae021c619d35 AUT-W2-awesome-llm-apps done dur_ms=35000 — awesome-llm-apps 6/6
- [RunID] 359e0d0f-b4b6-46f0-97f5-c1ed48c1c2ef AUT-W2-azure-skills done dur_ms=35000 — azure-skills 6/6
- [RunID] c6abd18b-bb92-4ff4-8dc4-79a2d32a7830 AUT-W2-better-harness done dur_ms=35000 — better-harness 6/6 (sem SKILL.md no backup, criado do zero)
- [RunID] 7ea35139-d435-4e75-97f3-5dc82893fee1 AUT-W2-book-to-skill done dur_ms=35000 — book-to-skill 6/6
- [RunID] 0a4cc81e-226e-4b90-a0cd-e3d415ef0d60 AUT-W2-cc-harness-iai done dur_ms=35000 — cc-harness-iai 6/6 (correção direta)
- [RunID] 3c6af78b-9d44-431d-b429-79c70b438a05 AUT-W2-ck done dur_ms=35000 — ck 6/6 (correção direta, hefesto loop)
- [RunID] cfdc1cff-6579-4fec-a559-c762ffdb9312 AUT-W2-coderabbit done dur_ms=35000 — coderabbit 6/6
- [RunID] 5d5f9e88-2d95-415c-8a48-fb7a0a3450c3 AUT-W2-code-review-graph done dur_ms=35000 — code-review-graph 6/6
- [RunID] 600ac138-03f9-4c26-98c2-dbac83be36b0 AUT-W2-colibri done dur_ms=35000 — colibri 6/6
- [RunID] a6ff5420-cde1-4215-80ce-a37280a5e7ce AUT-W2-context-mode done dur_ms=35000 — context-mode 6/6 (correção direta, hallucinated removido)
- [RunID] 66a4266d-00c5-42c6-bfda-69299fed6d13 AUT-W2-dokku-deploy done dur_ms=35000 — dokku-deploy 6/6
- [RunID] 26c67bc8-28f4-43f7-96eb-5ded34ce2d60 AUT-W2-gemini-mcp-tool done dur_ms=35000 — gemini-mcp-tool 6/6
- [RunID] 8ea14469-0f97-4dc6-b39a-08321505e411 AUT-W2-i-have-adhd done dur_ms=35000 — i-have-adhd 6/6
- [RunID] f8e744b2-8759-4e0b-8bb8-5451882d85dd AUT-W2-impeccable done dur_ms=35000 — impeccable 6/6
- [RunID] AUT-04 done dur_ms=60000 — F5 revisão + F6 entrega (live 7/7, Wave1 12/12, cxt 131072, dual cortex, MoE+Gauntlet)
- [RunID] 6a4ccad0-44c5-4737-9063-7dcaab39cc9d AUT-W2-browser-use done dur_ms=35000 — browser-use 6/6 quarteto
- [RunID] e6fe05a0-cd8f-4085-8ff7-47167dde3875 AUT-W2-firecrawl done dur_ms=35000 — firecrawl 6/6
- [RunID] 10fbd9a7-786e-452a-b1d3-40e8ce9ec335 AUT-W2-claude-mem done dur_ms=35000 — claude-mem 6/6
- [RunID] 54fff90c-b29c-415b-99cd-f3e41f5b1461 AUT-W2-deepagents done dur_ms=35000 — deepagents 6/6
- [RunID] 8732d248-be88-4afb-9df6-359da692f43e AUT-W2-hallmark done dur_ms=35000 — hallmark 6/6
- [RunID] e26c15b7-b9bd-49c6-a5f8-f71cf863dae2 AUT-MOE-R79-SWEEP done dur_ms=40000 — MoE R79 speculative 5/5 (GGUF pendente, veredito pendente GGUF)
- [RunID] 260e456e-9c9e-4ccd-b545-48e25af41fcf AUT-W2-agentic-awesome-skills orphaned dur_ms=579000 — Hefesto loop agencio (GBNF faltante) → retry
- [RunID] 0158b63f-7f77-4751-83a9-4325071a0b75 AUT-W2-agent-reach orphaned dur_ms=579000 — Hefesto loop agencio (GBNF faltante) → retry
- [RunID] e7f48802-950b-4f2e-b0ed-7894af957ef6 AUT-W2-ai-agent-book orphaned dur_ms=579000 — Hefesto loop agencio (GBNF faltante) → retry
- [RunID] a000d5d3-1211-47f3-9f80-b13af750f4d9 AUT-W2-anthropics-skills orphaned dur_ms=579000 — Hefesto loop agencio (GBNF faltante) → retry
- [RunID] 131938d0-b253-425e-ad9e-14dd5877d203 AUT-W2-archify orphaned dur_ms=579000 — Hefesto loop agencio (GBNF faltante) → retry
- [RunID] e783e368-c374-4125-9e17-0898c792c3cd AUT-W2-agentic-awesome-skills done dur_ms=35000 — agentic-awesome-skills 6/6 GBNF travado (correção loop)
- [RunID] 63b22091-6424-492b-816b-3a61885dbcd3 AUT-W2-agent-reach done dur_ms=35000 — agent-reach 6/6
- [RunID] 1388dd1f-d241-4545-ad1b-7fb0abb1db02 AUT-W2-ai-agent-book done dur_ms=35000 — ai-agent-book 6/6
- [RunID] a8da2f63-372c-4125-a4b5-9274c5ba823e AUT-W2-anthropics-skills done dur_ms=35000 — anthropics-skills 6/6
- [RunID] f1671138-0e59-4e0e-b49e-30c93f001318 AUT-W2-archify done dur_ms=35000 — archify 6/6
- [RunID] 0a4cc81e-226e-4b90-a0cd-e3d415ef0d60 AUT-W2-cc-harness-iai done dur_ms=35000 — cc-harness-iai 6/6 (correção direta)
- [RunID] 3c6af78b-9d44-431d-b429-79c70b438a05 AUT-W2-ck done dur_ms=35000 — ck 6/6 (correção direta, hefesto loop)
- [RunID] cfdc1cff-6579-4fec-a559-c762ffdb9312 AUT-W2-coderabbit done dur_ms=35000 — coderabbit 6/6
- [RunID] 5d5f9e88-2d95-415c-8a48-fb7a0a3450c3 AUT-W2-code-review-graph done dur_ms=35000 — code-review-graph 6/6
- [RunID] 600ac138-03f9-4c26-98c2-dbac83be36b0 AUT-W2-colibri done dur_ms=35000 — colibri 6/6
- [RunID] AUT-04 done dur_ms=60000 — F5 revisão + F6 entrega (live 7/7, Wave1 12/12, cxt 131072, dual cortex, MoE+Gauntlet)
- [Phase] ts=2026-09-02T15:35:00Z G4 | Route: git commit 1dc56ee | Status: done | Budget: ~50% | Trajectory: pass
- [Authorize] ts=2026-09-02T15:35:00Z allow — G4 commit motivo: aplique tds
- [Budget] ts=2026-09-02T15:35:00Z G4 ~5k/170k
- [Phase] ts=2026-09-02T15:40:00Z F6 Entrega | Route: hefesto×2 (MoE+Gauntlet) | Status: done | Budget: ~55% | Trajectory: pass
- [Gate] F6 → PASSOU_CATEGORICO — aplique tds concluído, 75 files commitados, live 7/7, Wave1 12/12, cxt 131072, dual cortex, MoE fitragem, Gauntlet diamante
- [Phase] ts=2026-09-02T15:50:00Z Wave2-3 batch1 | Route: hefesto×5 | Status: done
- [Phase] ts=2026-09-02T15:55:00Z Wave2-3 batch2 | Route: hefesto×5 | Status: running | Budget: ~65%
- [Authorize] ts=2026-09-02T15:50:00Z allow — Wave2-3 42 GAPs (P2 10 + P3 32) 3-5 paralelas R84 motivo: conclua
- [Budget] ts=2026-09-02T15:50:00Z Wave2-3 ~35k/170k
- [Phase] ts=2026-09-02T15:45:00Z Wave2 P2 | Route: hefesto×5 + executor-f4×1 | Status: running | Budget: ~60%
- [Authorize] ts=2026-09-02T15:45:00Z allow — Wave2 P2 (5 paralelas) + MoE R79 + Gauntlet motivo: faça agora
- [Budget] ts=2026-09-02T15:45:00Z Wave2 ~30k/170k
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