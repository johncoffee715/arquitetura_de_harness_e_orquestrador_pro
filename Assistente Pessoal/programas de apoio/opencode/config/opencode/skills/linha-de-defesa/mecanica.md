# Mecânica de Ignição — Linha de Defesa Quadriplice

## 1. Seleção de motor (R75 — sempre refutando)

- **Categoria alvo**: `forja` (:9091 Needle) + `contrato-plano` (:9088 granite) + `orquestrador` (:8083 AD-IQ3)
- **Slot esperado**: 9091 (Needle byte-level) + 8083 (Ornith IQ3)
- **Refutação**: catálogo tem `granite 131K` mas KV Guard mostra `token budget 259k` — janela suficiente, mas t/s 103 vs 3.44 (granite 30× mais rápido para F2). Para F1 criativa, granite vence; para orquestração, Orquestrador vence. Não rebaixar por conveniência.
- **Fallback**: `qwen3-8b-q4_k_m` denso validador (~12 t/s CPU, 4.9G) se IQ3 Δ>5%

## 2. Parâmetros de ignição

```json
{
  "temp": 0.0,
  "top_k": 20,
  "top_p": 0.95,
  "repeat_penalty": 1.1,
  "max_tokens": 300,
  "stop": ["\n\n", "```", "<|eot_id|>"],
  "grammar": "runtime PydanticToGbnf"
}
```
- **Ganchos**: `Vulkan` prefill 15.74 tg32 3.44 (IQ3) vs 9.67/1.55 (IQ4) — batch 2048/512, KV q4_0/q4_0, threads auto

## 3. Sequência de ignição (6 camadas)

1. Validar gabarito (deny) — `tool in allowlist` + `invariants`
2. Resolver motor via inventário R75 — `llm-inventory.py --resolve forja`
3. KV Guard 1.5 — `calculate_budget` → fragmentar se necessário
4. Gerar com GBNF 2 — `PydanticToGbnf(schema).to_gbnf()` + `ConstrainedGenerate` temp0
5. Watchdog 2.5 — `watchdog_check` (n-gram, stall, entropy)
6. Validar 3 — `validate_byte_level` + `Pydantic.model_validate`
7. Gate 4 — `execution_gate` (whitelist, permission, fingerprint)
8. Tool → Result 5 — `result_validator` → COMMIT ou RETRY/FALLBACK/CIRCUIT_BREAKER

## 4. Validação

- `isAllowedWritePath` para `gabarito.json` → `Pydantic` → `GBNF` runtime
- `max_retries=3` + `max_tokens` calculado do schema
- `fallback` para base coerente se agressiva falhar
