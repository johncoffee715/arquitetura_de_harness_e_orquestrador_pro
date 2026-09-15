# wigolo — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (pesquisa multi-fonte com síntese)
- **Slot esperado**: `:9088`
- **Refutação do catálogo**: pesquisa exige amplitude + julgamento de evidência — aceito
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

- **Ganchos de backend**: engine local (`npx wigolo`, `~/.wigolo/`); `WIGOLO_LLM_PROVIDER` opt-in p/ síntese

## 3. Sequência de ignição

1. Validar gabarito (deny) antes de qualquer ação — sem `query` não há pesquisa
2. Resolver motor via inventário (R75)
3. `search` (array p/ breadth) → `fetch`/`extract` → checar degradação → sintetizar com citações
4. Gate categórico (R28): resultados + citations + flags; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(query: list, need_evidence: bool = True) -> dict:
    """Pesquisa com evidência pinnada + flags de degradação. Retorna dict."""
    return pesquisar(query, need_evidence)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Excerpt sem span/citation = evidência inválida.
