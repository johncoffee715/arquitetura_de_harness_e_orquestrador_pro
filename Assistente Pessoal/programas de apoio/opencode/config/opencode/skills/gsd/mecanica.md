# gsd — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (fases + pacotes)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: horizonte longo exige persistência, não velocidade — aceito
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

1. Validar gabarito (deny) antes de qualquer ação — sem `goal`+`phases` não há plano
2. Resolver motor via inventário (R75)
3. Fases (exit criteria) + pacotes (paths) + âncora (1 parágrafo)
4. Gate categórico (R28): plano + pacotes + âncora; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(goal: str, phases: list) -> dict:
    """Plano faseado + âncora. Retorna dict."""
    return planejar(goal, phases)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Fase sem resumo em arquivo = deny.
