# SPEC — Estratégia de Compactação Global (Global Context Compaction)

> Feature transversal do Gran-Mestre Hybrid Harness. Rota MIX + Dev Loop N3.
> Estado: contrato canônico. Home das regras: `harness/global-rules.md`.

## Problema
O orquestrador (e todo loop de contexto) acumula janela de tokens a cada fase. Sem gestão, ao atingir a capacidade do modelo o histórico é descartado perdendo raciocínio, ou hard-fail por estouro de contexto.

## Os 4 requisitos inegociáveis (do usuário)
1. **Limiar de Disparo** — iniciar compactação ao usar **75%–85%** da capacidade máxima de tokens do modelo.
   - `trigger_ratio_min = 0.75`, `trigger_ratio_max = 0.85`. Abaixo do min → no-op. Em `[min, max)` → normal. `>= max` → **critical** (forçado).
2. **Preservação de Estado** — nunca apagar tudo; gerar **resumo estruturado** com **intenção da tarefa / progresso atual / próximos passos**, que encabeça o novo prompt ativo.
3. **Offload (Descarregamento)** — salvar o **histórico cru** em `/conversation_history/{thread_id}.md` (persistente) **antes** de limpar a memória de trabalho; janelas por append, nunca destrói janelas anteriores. Fallback se o caminho primário não for gravável → `<project>/harness/conversation_history/`.
4. **Retenção Recente** — manter os **últimos 10%–20%** de tokens intactos no prompt ativo após o resumo (`retain_ratio_min=0.10`, `retain_ratio_max=0.20`, efetivo `0.15`).

## Escopo global
- Uma implementação no núcleo do harness, aplicada a **toda fase, loop e modelo**.
- **Tamanho de contexto por modelo** (config): `gran_mestre`=262144, `heavy_execution`=262144, `filter_medium`=32768; demais → default `8192`.

## Superfície do módulo — `harness/context/compaction.py`
- `CompactionPlan` (dataclass): thread_id, model, used_tokens, max_tokens, ratio, trigger(`none|normal|critical`), reason, retained_tokens.
- `CompactionResult` (dataclass): ..., ratio_before, ratio_after, trigger, dropped_tokens, retained_tokens, summary_tokens, new_prompt, offload_path, summary, created_at.
- `ContextCompactor`:
  - `estimate_tokens(text)->int` (determinístico, chars//4+1; monotônico)
  - `model_max_context(model_id)->int`
  - `check(thread_id, model, used_tokens)->Optional[CompactionPlan]` (decisão, registra evento `track`)
  - `compact(...)->CompactionResult` (ordem estrita: resumo → offload → retenção → novo prompt)
  - `offload_history(...)`, `load_history(...)`, `render_prompt(...)`, `events(...)`, `status()`, `selfcheck()`
  - CLI (`--check|--status|--selfcheck|--compact-demo`)
- **Eventos observáveis**: `harness/metrics/compaction-events.jsonl` (`track|compact|error`), thread-safe.
- **Complementar** ao `CollectiveMemory` (RAG SQLite estruturado): o compactor é dono do offload cru + decisão + sumário.

## Critérios de aceite (testável)
- 0.749→none · 0.75→normal · 0.85→critical · 0.90→critical.
- `model_max_context(filter_medium)==32768`; desconhecido→8192.
- `estimate_tokens("")==0`; monotônico.
- compact a 78%: arquivo offload existe, contém `## Window`, resumo presente, prompt começa com resumo, cauda ~15%, conteúdo dropado ausente do prompt mas presente no offload.
- idempotência: 2 compacts → 2 janelas, sem truncar.
- fallback: caminho primário não gravável → usa `<project>/harness/conversation_history/`.
- invariantes do prompt: começa com `# Compaction Summary`, contém header de retenção, resumo não duplicado.
- config ausente → defaults, sem exceção.
- `load_history` roundtrip.

## Integrações (ancoragem)
1. `harness-config.json` → bloco `harness.context_compaction`.
2. `harness/core/harness.py` → `_compaction_check(phase, task)` ao fim de cada fase + CLI `compact`.
3. `harness/dev_loop/dev_loop.py` → hook opcional `reconcile_context` (compactor=None mantém comportamento atual).
4. Documentação: `.planning/gc/PLAN.md`, `harness/global-rules.md`.

## Anexo — Guardas Globais (R8/R9/R10) + Brainstorm (correção estrutural)
- `harness/models/model_inheritance.py` — herança de submodelo por recurso/categoria, health-probe, `guarded_resolve()` fail-fast (StallGuardError <2s), `stall_audit()`.
- `harness/safety/stall_watchdog.py` — watchdog R6/R7 (re-sonda, recusa preventiva, histórico JSONL).
- `harness/safety/self_heal.py` — R10: redflag silenciosa (predição/prevenção/correção) + recovery da stack local (híbrido local+nuvem; omniroute cobre enquanto locals sobem).
- `harness/a2a/brainstorm.py` — transporte de brainstorm inter-recurso (board A2A, rodadas, transcript).
- Invariante inegociável: NENHUMA delegação parte para backend não confirmado vivo (guard em `_run_wave`).
- Config: `harness.model_inheritance` (backends :8081-:8084 + omniroute; defaults por categoria).
- Testes: `test_global_guards.py` (stall-guard, brainstorm, self_heal).
