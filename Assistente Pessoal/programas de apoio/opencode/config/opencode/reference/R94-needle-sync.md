# R94 — Sync Permanente Needle 2 ↔ LLMs Canonizados (promulgada 2026-09-07)

> Status: FORJADA (ordem do usuário: "sempre sincronizar") · incorporação no
> AGENTS.md pendente. Vale desde o registro no decision-log.

## Regra

Sempre que a stack mudar (slot adicionado/removido/device/ctx/modelo trocado),
o GM re-verifica a sincronia Needle↔LLMs (probes read-only + log; seguro em autônomo):

1. **Liveness**: `:8097` (triagem) e `:9091` (forja) respondem `/complete`.
2. **E2E canônico**: amostra TDD (`tests/router.py:42 AssertionError expected 200
   got 500`) → `needle_pytest_filter.py --json` (localização+assinatura+delta,
   ≤256tok) → `:9091` responde com sucesso.
3. **Matriz slot→contrato**: refresh no decision-log (qual papel usa qual
   caminho needle). Novo slot só entra em produção com linha na matriz.

## Camada viva (verificado 2026-09-07)

- :8097 triage_route (235 t/s) · :9091 forja validate_schema/write_artifact/
  upsert_vault/emit_manifest (108-198 t/s) · binário
  `opencode/tools/needle2/needle` · schemas/ · scripts em
  `opencode/config/opencode/scripts/` (filter + roteador — o find com espaço
  no path já deu falso-negativo uma vez: usar glob, nunca find cru).
- Needle é slot-agnóstico por design: o sync é por CONTRATO (tool-call JSON,
  TDD-failure, manifest), não por réplica por slot.

## Matriz vigente

| Slot | Contrato needle | Status |
|---|---|---|
| 8083 orquestrador | tool-call JSON + consome E2E TDD | OK (E2E hoje) |
| 9084 ingestor | logs → filter → needle | OK (mecanismo) |
| 9086/9088/9090/9092/9093 | GBNF → validate_schema | OK (:9091 vivo) |
| reservas (OLMoE, Qwen1.5-MoE) | re-verify na promoção (trigger) | pendente-trigger |
