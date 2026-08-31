# Crivo Sistêmico R83 + Constrained Decoding R81 — 2026-08-31

## Crivo (scripts/llm_crivo.py — 2 etapas)
- **Etapa A (anti-alucinação)**: ground truth factual + extração com schema Pydantic + não-invenção de arquivo.
- **Etapa B (anti-loop)**: N amostras temp 0.0 → determinismo, repetição n-gram, finish_reason, latência.
- Memorial comparativo: `harness/logs/llm-crivo-memorial.jsonl` (append-only).

## Resultados empíricos (memorial)
| Modelo | Alucinação | Determinismo | Veredito |
|---|---|---|---|
| granite-4.2-3b :9088 | 0.0% | 100% (temp0) | **PASSOU_CATEGORICO** |
| ternary-bonsai-8b :9090 | 0.333 (fence markdown!) | 100% | NAO_PASSOU |
| ornith-35b :8083 | — | — | NAO_PASSOU (35B CPU instável) |

- **Dado-ouro**: ternary não alucinou CONTEÚDO (0 invenções), alucinou SINTAXE (fence ```json) → prova empírica de que o erro de LLM pequeno está no amostrador, não na cognição → GBNF resolve fisicamente.

## Constrained Decoding (R81/R82) — lições técnicas
- **GBNF: aspas são DELIMITADORES** — `"key"` gera `key` sem aspas; JSON exige `"\"" "key" "\""`.
- **Grammar só ativa em `/completion`** (não `/v1/chat`) no llama.cpp server.
- Pydantic → JSON Schema → GBNF runtime (`LlamaGrammar.from_json_schema`/PydanticToGbnf); `.gbnf` manual = legado.
- Anti-loop: max_retries=3 no Python (nunca no LLM) + fallback default + reinjeção do erro.
- FORJA byte-level: valida fence/JSON inválido/campos extra/faltantes + manifest.
- Matriz multi-linguagem: Rust (Candle), Go (go-llama), TS (node-llama-cpp), C# (LLamaSharp) — `skills/hefesto/reference/constrained-decoding-linguagens.md`.

## Stack resultante
- Slot :9088: granite-4.2-3b (BFCL 52.41, decode ~104 tok/s, crivo PASS) — substituiu qwen3.8-4b (alucinava sucesso).
- Gran-Mestre v9.0.0 (R1-R79 + R80-R83), Hefesto v2, anti-lixo gate.
