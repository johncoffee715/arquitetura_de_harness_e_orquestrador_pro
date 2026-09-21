# context7-skill — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `talamus-cortex` (retrieval focal, janela longa p/ docs)
- **Slot esperado**: `:9084` (ingestor, 1M ctx, prefill veloz)
- **Refutação do catálogo**: janela do ingestor cobre docs longas? tps de prefill sustenta? vocação é retrieval (sim) — aceito
- **Fallback**: `contrato-plano` (`:9088`) se `:9084` offline; `relay` (`:9092`) em último caso

## 2. Parâmetros de ignição (samplers & setup)

```json
{
  "temp": 0.0,
  "top_k": 10,
  "top_p": 0.9,
  "repeat_penalty": 1.0,
  "max_tokens": 1024
}
```

- **Ganchos de backend**: REST via `curl` + `jq`; `CONTEXT7_API_KEY` opcional via env (nunca no prompt); timeout 30s por chamada; 1 retry com backoff

## 3. Sequência de ignição

1. Validar gabarito (deny) antes de qualquer ação — sem `library` o input é inválido
2. Resolver motor via inventário (R75) — talamus-cortex primeiro
3. `search(library)` → `library_id`; `docs(library_id, topic)` → excerto focal
4. Gate categórico (R28): excerto cita `library_id` + `topic`; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(library: str, topic: str = "") -> dict:
    """Resolve library ID e busca docs focais. Retorna dict validado."""
    lib_id = resolver_library_id(library)
    return buscar_docs(lib_id, topic)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Nenhum segredo em prompt/log — `CONTEXT7_API_KEY` só via env.
