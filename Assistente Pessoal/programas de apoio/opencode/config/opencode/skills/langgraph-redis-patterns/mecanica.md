# langgraph-redis-patterns — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor

- **Categoria alvo**: `contrato-plano` · **Slot**: `:9088` · **Fallback**: cloud-direct
- Refutação: store exige namespace+TTL — aceito

## 2. Parâmetros

```json
{"temp": 0.0, "top_k": 10, "top_p": 0.9, "repeat_penalty": 1.0, "max_tokens": 512}
```

## 3. Sequência

1. Validar gabarito (deny) — sem `thread` não há namespace
2. Resolver motor (R75) · 3. Namespace + TTL · 4. Gate (R28)

## 4. Função

```python
def ignicao(thread: str, ttl_s: int) -> dict:
    return especificar(thread, ttl_s)
```

## 5. Enforcement

- Deny em violação do gabarito; sampling travado (R62/R66); servidores como dependência = deny.
