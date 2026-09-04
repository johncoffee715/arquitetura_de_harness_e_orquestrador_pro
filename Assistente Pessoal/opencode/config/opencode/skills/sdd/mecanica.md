# Mecanica — sdd (R77 + R81 + R82)

## Ignicao
- Modelo: `local-thalamus/ingestor` (400 t/s, 1M ctx)
- Sampling: temp 0.3, top_k 20, top_p 0.95
- GBNF: `schema.gbnf` do `gabarito.json` (`LlamaGrammar.from_json_schema`)
- Max retries: 3 + Circuit Breaker 5x

## Validacao
1. Pydantic model_validate_json
2. GBNF barreira fisica
3. anti-lixo gate (False/True capital, PASS|FAIL)

## Fluxo
1. ler conceito + gabarito → compilar GBNF
2. constrained_generate → JSON byte-level
3. validate_output → Output
4. falha → re-inject + retry ≤3 else fallback
