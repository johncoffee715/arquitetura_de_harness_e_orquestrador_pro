# identity-authz-apl — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (regras + decisão, determinismo)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: authz exige decisão bounded+explicável — aceito
- **Fallback**: cloud-direct (modo autônomo §9) se local offline

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

## 3. Sequência de ignição

1. Validar gabarito (deny) antes de qualquer ação — sem `rules`+`attrs` não há decisão
2. Resolver motor via inventário (R75)
3. Avaliar por salience (deny → permit → default), parar na 1ª decisão
4. Gate categórico (R28): decision + fired + explain; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(rules: list, attrs: dict) -> dict:
    """Avalia rules por salience até decisão. Retorna dict."""
    return decidir(rules, attrs)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Lógica arbitrária em condição = deny.
