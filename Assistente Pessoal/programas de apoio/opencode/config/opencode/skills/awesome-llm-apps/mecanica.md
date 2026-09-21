# Template de Feature Cognitiva — Mecânica de Ignição (R77 camada 3)

> Copie para `skills/<sua-feature>/mecanica.md` e preencha.
> Sweet spot: 30–60 linhas por bloco; máx 150–200 por arquivo.

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `<categoria do llm-inventory.json — ex.: contrato-plano, refutacao, forja, judge>`
- **Slot esperado**: `<porta>`
- **Refutação do catálogo**: `<o que questionar no catálogo atual antes de aceitar — ex.: janela insuficiente? tps? vocação?>`
- **Fallback**: `<categoria/slot alternativo se o primário offline>`

## 2. Parâmetros de ignição (samplers & setup)

```json
{
  "temp": 0.2,
  "top_k": 20,
  "top_p": 0.95,
  "repeat_penalty": 1.1,
  "max_tokens": 4096
}
```

- **Ganchos de backend**: `<Vulkan/llama.cpp — prefill/decode no limite do hardware; batch/ubatch; KV q4/q4 (R76)>`

## 3. Sequência de ignição

1. `<passo 1 — validar gabarito (deny) antes de qualquer ação>`
2. `<passo 2 — resolver motor via inventário (R75)>`
3. `<passo 3 — executar função principal>`
4. `<passo 4 — gate categórico (R28) + nota R34 com bugs concretos>`

## 4. Funções focadas (Python 30–60 linhas por bloco)

```python
def ignicao(artefato: str) -> dict:
    """Função principal da feature — 1-2 funções focadas."""
    # validar gabarito → resolver motor → executar → gate
    return {"status": "SUCCESS", "evidencia": []}
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).