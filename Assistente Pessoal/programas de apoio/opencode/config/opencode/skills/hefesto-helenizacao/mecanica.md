# HEFESTO-HELENIZACAO — Mecânica de Ignição

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (Qwen3.8-4B, :9088 — capacidade de programação ponta-a-ponta).
- **Refutação do catálogo**: se a reconstrução exigir raciocínio profundo (arquitetura complexa), refutar → `orquestrador` (:8083, 35B). Se for reescrita mecânica, manter contrato-plano.
- **Fallback**: `orquestrador` (:8083).

## 2. Parâmetros de ignição

```json
{
  "temp": 0.2,
  "top_k": 20,
  "top_p": 0.95,
  "repeat_penalty": 1.1,
  "max_tokens": 8192
}
```

- **Ganchos de backend**: llama.cpp Vulkan (FA on, KV q4/q4 — R76).

## 3. Sequência de ignição

1. Validar gabarito (deny) — nenhuma ação antes.
2. Resolver motor via inventário (R75) — categoria `contrato-plano`.
3. Receber essência da autofagia (rolling summary, nunca bruto — R22).
4. Reescrever idiomático para o ecossistema alvo (anti-lazy R71).
5. Preencher frontmatter + provenance + instalar GLOBAL (R2/R44).
6. Gate G-H categórico (R28) + nota R34 com bugs concretos.

## 4. Funções focadas

```python
def frontmatter(nome: str, desc: str, origin: str) -> str:
    """Gera frontmatter YAML completo para recurso helenizado."""
    return f"""---
name: {nome}
description: "{desc}"
mode: skill
origin: {origin}
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-08-30
  author: Gran-Mestre
---"""
```

## 5. Enforcement

- Motor recusa ignição se ação violar deny do gabarito (camada 2 é lei).
- Alteração de sampling sem novo crivo = proibida (R62/R66).