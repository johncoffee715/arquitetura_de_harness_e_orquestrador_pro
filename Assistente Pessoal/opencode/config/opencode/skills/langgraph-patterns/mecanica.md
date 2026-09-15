# langgraph-patterns — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (grafo + estado, precisão)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: resiliência exige completude de checkpoint, não velocidade — aceito
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

1. Validar gabarito (deny) antes de qualquer ação — sem `states`+`nodes` não há grafo
2. Resolver motor via inventário (R75)
3. Schema → nós/arestas → checkpoints por step → interrupts → memórias
4. Gate categórico (R28): grafo + checkpoint plan; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(states: list, nodes: list) -> dict:
    """Monta spec do grafo stateful. Retorna dict."""
    return montar_grafo(states, nodes)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Framework como dependência = deny.
