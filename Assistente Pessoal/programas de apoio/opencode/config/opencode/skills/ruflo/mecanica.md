# ruflo — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (topologia + memória, julgamento estrutural)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: coordenação exige visão de dependências, não velocidade — aceito
- **Fallback**: cloud-direct (modo autônomo §9) se local offline

## 2. Parâmetros de ignição (samplers & setup)

```json
{
  "temp": 0.2,
  "top_k": 20,
  "top_p": 0.95,
  "repeat_penalty": 1.1,
  "max_tokens": 1024
}
```

## 3. Sequência de ignição

1. Validar gabarito (deny) antes de qualquer ação — sem `task`+`agents` não há topologia
2. Resolver motor via inventário (R75)
3. Topologia (hierárquica/mesh/adaptativa) + consenso + namespaces de memória + trust
4. Gate categórico (R28): pick + plano; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(task: str, agents: int) -> dict:
    """Escolhe topologia + plano de memória. Retorna dict."""
    return escolher_topologia(task, agents)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Runtime alheio como dependência = deny (só padrões).
