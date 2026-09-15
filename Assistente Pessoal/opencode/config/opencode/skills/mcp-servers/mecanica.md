# mcp-servers — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (catálogo + config JSON, precisão)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: config exige exatidão de paths/env — aceito
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

1. Validar gabarito (deny) antes de qualquer ação — sem `need` não há pick
2. Resolver motor via inventário (R75)
3. Mapear need → server do catálogo (7 ativos; arquivados só sob aviso)
4. Gate categórico (R28): pick + client_config com secrets só em env; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(need: str) -> dict:
    """Mapeia necessidade → server + client_config segura. Retorna dict."""
    return escolher_server(need)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Secrets fora de `env` = deny.
