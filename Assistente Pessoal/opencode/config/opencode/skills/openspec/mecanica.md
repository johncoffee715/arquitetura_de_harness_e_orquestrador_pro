# openspec — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (specs multi-artefato, janela média)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: specs exigem coerência longa, não velocidade — aceito
- **Fallback**: cloud-direct (modo autônomo §9) se local offline

## 2. Parâmetros de ignição (samplers & setup)

```json
{
  "temp": 0.0,
  "top_k": 10,
  "top_p": 0.9,
  "repeat_penalty": 1.0,
  "max_tokens": 2048
}
```

## 3. Sequência de ignição

1. Validar gabarito (deny) antes de qualquer ação — sem `change_name` não há ciclo
2. Resolver motor via inventário (R75)
3. `explore` → `propose` (4 artefatos) → `apply` (tasks) → `archive` (specs atualizadas)
4. Gate categórico (R28): 4 artefatos presentes + cenários WHEN/THEN; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(change_name: str, artifacts: dict) -> dict:
    """Valida o ciclo explore→propose→apply→archive. Retorna dict."""
    return validar_ciclo(change_name, artifacts)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Telemetria sempre opt-out.
