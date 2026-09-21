---
tipo: pipeline-context
feature: cientista
data: 2026-09-17
dono: gran-mestre
---

# Pipeline — Feature "Cientista" (estudo observacional/experimental semanal)

- [Harness] SHA: 206fb37 (dirty working tree: 3992 linhas — baseline declarado)
- [Phase] ts=2026-09-17 F1-brainstorm | CONCLUÍDA (refutação GM + 3 rodadas externas do user + ground truth bibliotecário) | PASSOU
- [Phase] ts=2026-09-17 F2-spec | EM CURSO (planejador-f23 despachado)
- [Safety] SHA: 206fb37

## Decisões G1 (fechadas pelo usuário 2026-09-17)

1. **Arquitetura em camadas**: Cientista = METODOLOGISTA (gera método/relatório/hipóteses); refutação pesada fica no quarteto A2A existente (:9088/:9090/:9092). RECUSADO: coder-3b/Noema-2B solo como refutador.
2. **Crivo primeiro (R103/R104)**: candidatos ao papel L1-triagem entram por `fitragem/` + crivo-padrão A/B. Fila de entrada: Noema-2B.Q4_K_S → qwen2.5-coder-3b-instruct-q4_0 → LFM2.5-1.2B-Thinking-ToMoE. NENHUM canonizado por análise de screenshot.
3. **Gatilho semanal híbrido (3 camadas, fechamento de brechas)**:
   a. `secretario/tooling/agenda.py` registra o due semanal (disparo no check-in);
   b. regra doutrinária estilo R98 (obrigação semanal registrada, executada por sessão);
   c. cron/systemd real disparando wrapper (a criar) — autonomia real fora de sessão.

## Arquitetura aprovada (5 camadas)

- L0 COLETA (existe): R48 watcher + tracer + gari → dados brutos contínuos. Cientista é CONSUMIDOR do GAP-SL1 (relatório R48 sem consumidor), não coletor novo.
- L1 TRIAGEM (needle): modelo pequeno pós-crivo condensa semana → clusters/anomalias. VAGO até crivo.
- L2 MÉTODO (a feature): skill `cientista` — quarteto R85 obrigatório (.md/.json/.py/.gbnf). Mecânica determinística (zero LLM). Escreve em setor novo `experimentos/` do vault. Relatório GBNF-estrito: [Fenômeno][Hipótese][Variável][Protocolo de teste].
- L3 REFUTAÇÃO (existe): hipóteses → a2a_brainstorm.py (:9088 propõe, :9090 refuta, :9092 segunda voz).
- L4 GATE HUMANO (novo): relatório semanal → usuário audita/refuta → aprova → aplica. Nada irreversível sem gate (R18/R88/R89).

## Fronteiras declaradas (anti-colisão)

- R98 kronjob = DIÁRIO, fora→dentro (internet vs biblioteca). Cientista = SEMANAL, dentro→dentro (harness+vault).
- Gari (R99) = pérolas por sessão. Cientista = agregação semanal.
- R104/R103 = protocolo experimental do domínio quant/LLM; Cientista generaliza o MÉTODO.

## Riscos aceitos / declarações

- Autorreferência tóxica: exclusion list obrigatória na mecânica (cientista não estuda os próprios artefatos).
- Fadiga de relatório: métrica de utilidade (hipóteses→ações aprovadas) + critério de morte pré-declarado.
- RAG semântico fraco (Qdrant falhou p/ query conceitual nesta sessão; R96 pendente): v1 opera lexical-determinístico.
- Compressão de logs: já resolvido no catálogo (log-summarizer + RWKV7 :9084 1M). RECUSADO: smollm2-360m pré-compressor (perda de sinal por salto).

## Bloqueios vivos

- [BLOQUEIO] Crivo dos 3 candidatos: quartet A2A DOWN (health 000 em :9086/:9088/:9090/:9092 nesta sessão; só :9084 vivo). Crivo exige slots ⇒ pendente até stack subir.
- [BLOQUEIO] Loop A2A oficial (L3) idem — refutação F1 foi executada manualmente (GM 35B + rodadas externas do usuário).

## Evidências F1

- Ground truth bibliotecário: colisões R98/R48/R44/R104/Gari; lacunas (persona, setor experimentos/, mandato refutar-usuário→invertido em gate, GAP-SL1, índice semântico fraco); refs completas verificadas em filesystem.
- Refutações externas do usuário (3 rodadas): HITL semanal ✅ adotado; experimental exige privilégio→sandbox/fitragem ✅ adotado; escolha de modelo por screenshot ❌ refutada (3 coroações contraditórias em 1 sessão = prova viva do crivo-first).

## RunIDs

- [RunID] F1-bibliotecario-groundtruth done
- [RunID] F2-spec-planejador pending

## Encerramento de sessão 2026-09-18T00:31 (modo autônomo ON — reiterado pelo user; state file live+canônico)

### Waves órfãos/governança (paralelas ao pipeline cientista)
- A1 ✅ a2a_brainstorm.py: fallback default :9084 + check_slots() REDFLAG por papel; SKILL.md a2a-brainstorm v2.1.0. Achado: ~/.config/opencode = SYMLINK da canônica programas de apoio (sem drift físico).
- A2 ✅ decision-log CANÔNICO = vault (cerebro com IA/harness/decision-log.jsonl, Decisão A); legado 424 linhas marcado _deprecated; gabarito.json-raiz = NO-OP (não existe — inventário-fonte estava errado).
- A3 ✅ meta_orchestrator.py EXISTE (9.7KB, 5 arquivos da linha de defesa íntegros, sha idêntico nas 2 árvores) — pendência REFUTADA/encerrada.
- A5 ✅ 3 writers convergidos p/ canônico: auto-amelioracao.py, filtro-veloz.py, guardrails-engine.py (diffs reversíveis documentados).
- A4 ❌ spec Cientista v2 — 2 falhas de TRANSPORTE (SSE timeout + cancel). Ciclo nível TASK: resta 1 retry. → PENDENTE

### PENDÊNCIAS — STATUS FINAL 2026-09-18 (todas CONCLUÍDAS)

1. ✅ F2 spec — escrita in-house pelo GM após 4 falhas SSE em tasks de doc-longo (circuit-breaker por forma): `ideias/2026-09-17-feature-cientista-spec.md` (13 seções).
2. ✅ B2 drift sync — zero drift real (inventário "13 hooks" estava stale — 3º caso/24h); MCP saudável; SKILL_GUIDELINES.md criado; backup jsonc feito.
3. ✅ B1 forja quarteto: cientista/{SKILL.md 94L, gabarito.json, mecanica.py 368L, schema.gbnf 37L} + experimentos/ + template + cientista-weekly.sh + systemd user timer **ATIVO** (próximo: dom 2026-09-20 20:00) + agenda due 2026-09-20. Smoke 8/8 B1b + py_compile/json.load/bash -n OK.
4. ✅ Crivo R104 dos 3 candidatos (CPU-only, 8083 intacta): **coder-3b PASSOU (condicional: strip de fence)** · **Noema-2B PASSOU só com R57 no-think** (com thinking: NAO_PASSOU — content vazio) · **LFM-Thinking NAO_PASSOU (alucina em anti-alucinação)**. Motor-cientista recomendado: Noema-2B c/ `enable_thinking:false` ≥3k budget ou coder-3b c/ fence-strip. Benchmarks 2026-09-18-crivo-*.md.
5. ✅ Decisão "migrar histórico": EXECUTADA como append reversível do legado → canônico (427/427 parse OK).
6. R106 permanece CANDIDATA — ratificação pelo usuário no 1º gate semanal (por design: cientista propõe, usuário dispõe).
