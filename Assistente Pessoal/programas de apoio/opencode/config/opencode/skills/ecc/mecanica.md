# ecc — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (research + regras, julgamento)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: otimização exige síntese, não velocidade — aceito
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

1. Validar gabarito (deny) antes de qualquer ação — sem `topic`+`configs` não há ciclo
2. Resolver motor via inventário (R75)
3. `research_brief` (docs oficiais) + `shield_report` (scan de configs) + regra de instinct/memory
4. Gate categórico (R28): brief + shield; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(topic: str, configs: dict) -> dict:
    """Research-first + shield scan. Retorna dict."""
    return otimizar(topic, configs)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Segredo em config = fail imediato no shield.
