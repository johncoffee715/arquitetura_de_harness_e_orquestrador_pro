# Mecânica — impeccable (R77 + R81 + R82)

## Ignição
- **Modelo**: `local-thalamus/ingestor` (RWKV7 1M ctx, 400 t/s) — Filtro Talâmico R71
- **Sampling**: `temp 0.3`, `top_k 20`, `top_p 0.95` (R61 agentic/coding) — determinístico
- **GBNF**: `schema.gbnf` gerado do `gabarito.json` em runtime (`LlamaGrammar.from_json_schema`)
- **Max retries**: 3 (R82) — 3 falhas = exceção Python + fallback `{"result":""}`, nunca loop no LLM

## Seleção de motor (R75)
- Categoria `skill-tecnica` → `local-thalamus/ingestor` (proposer leve 1M)
- Janela >1M → `omniroute` (R23, janela grande 262k)
- Refutação A2A → `local-refuter/refuter` (ternary 8B) + `local-reflexo/reflexo` (LFM)

## Validação determinística
1. `Pydantic model_validate_json` — `gabarito.json` é fonte única
2. `GBNF barrier` — tokens fora da regra = logit bias -inf antes do softmax (físico)
3. `anti-lixo gate` — rejeita output com `False/True` capital, `PASS|FAIL` não JSON, campos extras

## Anti-loop (R82)
- `stop_tokens`: `["</|eot_id|>","\n\n","```"]`
- `max_tokens`: calculado do schema (trava física)
- `max_retries=3` + `Circuit Breaker 5×` (R18) — queda >5× baseline → restart cirúrgico

## Fluxo
1. Ler `conceito.md` (persona) + `gabarito.json` (schema) → compilar `schema.gbnf`
2. `constrained_generate(prompt, schema)` → JSON byte-level
3. `validate_output(json)` → `Output` Pydantic
4. Em falha, re-injetar erro parseado + retry ≤3, senão fallback

## Evidência
- `mecanica.py` implementa `validate_output` + `constrained_generate` stub
- `schema.gbnf` = GBNF do `gabarito.json` (fonte única R77)
- Teste: `python -m py_compile mecanica.py && python -c "import mecanica; print(mecanica.validate_output)"`
