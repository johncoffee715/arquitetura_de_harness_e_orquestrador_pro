---
name: otel-semconv-genai
description: GenAI semantic conventions — span/attribute standards for LLM telemetry (model, tokens, cost, authz) aligned to the harness MELT.
category: skill
model: local-forge/proposer
---

# otel-semconv-genai

Convenções semânticas p/ telemetria GenAI: nomes de spans e atributos padronizados
(model, tokens in/out, cost source/exactness, authz) p/ traces consistentes.
Helenizado de `open-telemetry/semantic-conventions` (área genai)
(origem: https://github.com/open-telemetry/semantic-conventions).

> O MELT nativo do harness já cita estas convenções (PR #291, issue #287):
> `cost.source`, `cost.exactness`, `fga.authorize`, derivation por spans.

## Quando usar

- Emitir spans de chamada LLM (modelo, tokens, latência, custo)
- Anotar custo com fonte e exatidão (`billed`/`estimated`/`proxy`)
- Auditar autorizações (`fga.authorize`) e linhagem (input_spans/strategy/weight)

## Como usar

1. **Span**: `genai.chat` + attrs (`genai.request.model`, `genai.usage.*`)
2. **Custo**: `cost.source` + `cost.exactness` em todo evento de custo
3. **Authz**: `fga.authorize` em decisões de acesso
4. **Linhagem**: `derivation.{input_spans,strategy,weight,influence}` na síntese

## Princípio

Atributos consistentes ou nada: semântica compartilhada antes de volume.
