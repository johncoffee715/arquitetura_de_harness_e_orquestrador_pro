# andrej-karpathy-skills — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (review estruturado de diff, janela média)
- **Slot esperado**: `:9088` (janela p/ diff + contexto)
- **Refutação do catálogo**: review exige precisão, não velocidade — aceito
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

1. Validar gabarito (deny) antes de qualquer ação — sem diff/task o input é inválido
2. Resolver motor via inventário (R75)
3. Checar os 4 gates em ordem (assumptions → simplicity → scope → goals), cada violação com evidência de linha
4. Gate categórico (R28): veredito + lista de violações; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(diff_lines: list, task: str) -> dict:
    """Aplica os 4 gates ao diff. Retorna veredito + violações."""
    return aplicar_gates(diff_lines, task)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Trivialidades (typo, one-liner) dispensam o rigor total — julgamento registrado.
