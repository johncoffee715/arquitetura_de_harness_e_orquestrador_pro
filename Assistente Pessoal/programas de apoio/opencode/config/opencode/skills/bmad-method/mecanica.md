# bmad-method — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (roteamento + plano proporcional)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: roteamento exige julgamento de tamanho, não velocidade — aceito
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

1. Validar gabarito (deny) antes de qualquer ação — sem `change` não há rota
2. Resolver motor via inventário (R75)
3. Classificar (vaga→clarify · grande→plan · pequena→build) → profundidade proporcional
4. Gate categórico (R28): rota + rationale; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(change: str, size: str) -> dict:
    """Roteia a mudança: clarify/plan/build + rationale. Retorna dict."""
    return rotear(change, size)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Mudança arquitetural nunca vai direto ao build.
