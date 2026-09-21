# inngest — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (trigger+steps, precisão)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: durabilidade exige pontos de resume explícitos — aceito
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

1. Validar gabarito (deny) antes de qualquer ação — sem `trigger`+`steps` não há função
2. Resolver motor via inventário (R75)
3. Trigger → steps (run+retry+estado) → wait/cancel → flow-control
4. Gate categórico (R28): trigger + steps com resume; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(trigger: str, steps: list) -> dict:
    """Monta função durável: trigger + steps. Retorna dict."""
    return montar_funcao(trigger, steps)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Servidor/plataforma como dependência = deny.
