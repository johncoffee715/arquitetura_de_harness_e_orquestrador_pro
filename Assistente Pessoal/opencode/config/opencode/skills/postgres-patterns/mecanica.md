# postgres-patterns — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor

- **Categoria alvo**: `contrato-plano` · **Slot**: `:9088` · **Fallback**: cloud-direct
- Refutação: durabilidade exige ordem WAL→ack — aceito

## 2. Parâmetros

```json
{"temp": 0.0, "top_k": 10, "top_p": 0.9, "repeat_penalty": 1.0, "max_tokens": 512}
```

## 3. Sequência

1. Validar gabarito (deny) — sem `write` não há check
2. Resolver motor (R75) · 3. WAL→ack + MVCC + constraints · 4. Gate (R28)

## 4. Função

```python
def ignicao(write: str, durable: bool) -> dict:
    return checar(write, durable)  # ack só se durable
```

## 5. Enforcement

- Deny em violação do gabarito; sampling travado (R62/R66); DB como dependência = deny.
