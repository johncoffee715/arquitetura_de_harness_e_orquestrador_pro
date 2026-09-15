---
name: inngest
description: Event-driven durable steps — triggers (event/cron/webhook) + step.run auto-retry + waitForEvent/cancelOn + flow control (patterns only).
category: skill
model: local-forge/proposer
---

# inngest

Steps duráveis orientados a eventos: triggers disparam, `step.run` retenta sozinho,
`waitForEvent`/`cancelOn` coordenam, flow-control (concurrency/throttle/debounce/rate-limit)
ordena a fila. Helenizado de `inngest/inngest`
(origem: https://github.com/inngest/inngest).

> Servidor sob SSPL (não-OSI) e SDKs Apache-2.0: aqui só o padrão event→steps.
> Plataforma/servidor NUNCA como dependência.

## Quando usar

- Background jobs que precisam sobreviver a falhas (meses de runtime)
- Coordenação por eventos com espera/cancelamento declarativos
- Fila com fairness + prioridades + batching

## Como usar

1. **Trigger**: event / cron / webhook
2. **Steps**: `step.run("nome", fn)` — cada step retenta e persiste estado
3. **Coordenar**: `waitForEvent` (pausa até evento) / `cancelOn` (cancela por evento)
4. **Controlar fluxo**: concurrency keyed, throttle, debounce, rate-limit, batching

## Princípio

Estado no step, não na memória volátil: cada step é um ponto de resume.
