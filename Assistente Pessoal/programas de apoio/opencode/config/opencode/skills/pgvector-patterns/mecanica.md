# pgvector-patterns — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor

- **Categoria alvo**: `contrato-plano` · **Slot**: `:9088` · **Fallback**: cloud-direct
- Refutação: escolha de índice exige tradeoff explícito — aceito

## 2. Parâmetros

```json
{"temp": 0.0, "top_k": 10, "top_p": 0.9, "repeat_penalty": 1.0, "max_tokens": 512}
```

## 3. Sequência

1. Validar gabarito (deny) — sem `need` não há pick
2. Resolver motor (R75) · 3. Operador + índice · 4. Gate (R28)

## 4. Função

```python
def ignicao(need: str) -> dict:
    return escolher(need)  # recall→HNSW, build→IVFFlat
```

## 5. Enforcement

- Deny em violação do gabarito; sampling travado (R62/R66); extensão como dependência = deny.
