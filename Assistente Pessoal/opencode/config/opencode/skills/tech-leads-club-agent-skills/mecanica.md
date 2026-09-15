# tech-leads-club-agent-skills — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (validação estruturada + catálogo)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: validação exige determinismo, não velocidade — aceito
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

1. Validar gabarito (deny) antes de qualquer ação — sem `skill_id`+`source` não há veredito
2. Resolver motor via inventário (R75)
3. `scan` (open-source? estática? pré-publish?) → `pin` (lockfile+hash) → `record` (audit)
4. Gate categórico (R28): veredito + pin; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(skill_id: str, source: str, has_binary: bool) -> dict:
    """Valida skill de terceiros: scan → pin → dict."""
    return validar_skill(skill_id, source, has_binary)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Binário em skill = deny imediato.
