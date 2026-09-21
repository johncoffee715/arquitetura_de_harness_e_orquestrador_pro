# openai-agents-python — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (specs + handoffs)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: delegação exige mapa explícito, não velocidade — aceito
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

1. Validar gabarito (deny) antes de qualquer ação — sem `agent`+`handoffs` não há spec
2. Resolver motor via inventário (R75)
3. Agent → handoffs c/ contexto → guardrails → sessions+trace
4. Gate categórico (R28): spec + mapa; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(agent: str, handoffs: list) -> dict:
    """Spec agente + handoffs. Retorna dict."""
    return especificar_handoff(agent, handoffs)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Framework como dependência = deny.
