# deepspec — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (receita técnica multi-etapas, janela média)
- **Slot esperado**: `:9088` (janela p/ configs + tabelas comparativas)
- **Refutação do catálogo**: metodologia exige precisão numérica (acceptance) — aceito
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

1. Validar gabarito (deny) antes de qualquer ação — sem `accepted`+`proposed`+`benchmark` não há report
2. Resolver motor via inventário (R75)
3. Calcular `acceptance_rate = accepted/proposed` por benchmark; checar setup alinhado
4. Gate categórico (R28): rate + benchmark + warning de custo; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(accepted: int, proposed: int, benchmark: str) -> dict:
    """Calcula acceptance-rate e emite report com warnings."""
    return report_acceptance(accepted, proposed, benchmark)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Treino pesado (8 GPUs/TB cache) nunca é default — sempre com cost warning.
