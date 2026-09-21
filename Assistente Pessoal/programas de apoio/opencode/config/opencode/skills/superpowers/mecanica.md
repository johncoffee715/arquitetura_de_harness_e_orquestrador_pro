# superpowers — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (loop + reviews)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: loop exige ordem estrita, não velocidade — aceito
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

1. Validar gabarito (deny) antes de qualquer ação — sem `task` não há ciclo
2. Resolver motor via inventário (R75)
3. skill-check → plan → review-1 (spec) → review-2 (quality) → finish
4. Gate categórico (R28): checks + reviews; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(task: str, spec_ok: bool, quality_ok: bool) -> dict:
    """Loop com review duplo. Retorna dict."""
    return aplicar_loop(task, spec_ok, quality_ok)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Pular skill-check ou fundir reviews = deny.
