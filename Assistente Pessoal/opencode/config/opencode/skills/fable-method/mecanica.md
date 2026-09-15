# fable-method — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (loop + classificação)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: loop exige ordem + bounds, não velocidade — aceito
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

1. Validar gabarito (deny) antes de qualquer ação — sem `ask` não há ciclo
2. Resolver motor via inventário (R75)
3. Classify (trivial→saída rápida) → done_spec → INTENT → act → verify (bounded) → report
4. Gate categórico (R28): classification + done + bounds respeitados; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(ask: str, shape: str) -> dict:
    """Classifica + define done. Retorna dict."""
    return classificar(ask, shape)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Verify além de 3 falhas ou lookup além de 2 infrutíferos = stop + hand back.
