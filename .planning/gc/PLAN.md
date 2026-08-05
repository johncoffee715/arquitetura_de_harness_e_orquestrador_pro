# PLAN — Implementação da Compactação Global (TDD, atômico)

> Executado sob supervisão do orquestrador (N3), exceção supervisionada por infra de subagentes 5/5 falha.
> Âncora de rollback: SHA `63f356189`. Cada task = 1 commit atômico (conventional).

## Tasks (ordem, test-first)

### T1 — Módulo core `harness/context/` (feat(harness): ContextCompactor global)
- Criar `harness/context/__init__.py` (exports) e `harness/context/compaction.py` (ContextCompactor + dataclasses + CLI + selfcheck).
- Testes: `harness/tests/test_compaction.py` cobrindo critérios de aceite da SPEC.
- Verificação: `python3 -m unittest harness.tests.test_compaction -v` verde; `python3 -m harness.context.compaction --selfcheck` ok.

### T2 — Config `harness-config.json` (feat(harness): config context_compaction)
- Adicionar bloco `harness.context_compaction` (enabled, ratios 0.75/0.85/0.10/0.20/0.15, offload_dir `/conversation_history`, models override max_context).
- Verificação: JSON válido (`json.load`), `"context_compaction" in d["harness"]`.

### T3 — Hook de execução `harness/core/harness.py` (feat(harness): hook _compaction_check + CLI compact)
- Instanciar `self.compactor` (graceful), `_compaction_check(phase, task)` ao fim de cada `_run_phase`, CLI subcomando `compact (--status|--selfcheck|--check --model --used)`.
- Verificação: `python3 -m harness.core.harness compact --status` e `--check` não quebram.

### T4 — Integração DevLoop `harness/dev_loop/dev_loop.py` (feat(dev-loop): hook opcional reconcile_context)
- `LoopState.used_tokens/max_context/compactions`; `reconcile_context(used_tokens)` com compactor=None mantém comportamento atual.
- Verificação: `python3 -c "import harness.dev_loop.dev_loop"` sem erro; testes de regressão do DevLoop (nenhuma quebra).

### T5 — Docs `docs(harness): SPEC+PLAN da compactação global`
- `.planning/gc/SPEC.md` + `.planning/gc/PLAN.md` (este arquivo) refletem implementação real.

## Gates
- Rollback: `git reset --hard 63f356189` se falha catastrófica.
- Commit atômico por task; somente arquivos da feature.

## Anexo — Tasks extras (guardas + brainstorm + self_heal)
- T6 (feat(harness)): model_inheritance + stall_watchdog + brainstorm + test_global_guards + self_heal (R8/R9/R10).
- T7 (feat(harness)): wiring global R9/R10 em _run_wave e __init__; CLI compact; docs.
