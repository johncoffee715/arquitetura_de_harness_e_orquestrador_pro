# HEFESTO-AUTOFAGIA — Mecânica de Ignição

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `refutacao` (Ternary-Bonsai-8B, :9090 — BFCL 73.9, estrutura Markdown/JSON limpa, baixo consumo).
- **Refutação do catálogo**: se a digestão exigir raciocínio mais profundo (artefato complexo), refutar → `contrato-plano` (:9088). Se exigir velocidade, manter refutacao.
- **Fallback**: `contrato-plano` (:9088).

## 2. Parâmetros de ignição

```json
{
  "temp": 0.3,
  "top_k": 20,
  "top_p": 0.95,
  "repeat_penalty": 1.1,
  "max_tokens": 4096
}
```

- **Ganchos de backend**: llama.cpp Vulkan (FA on, KV q4/q4 — R76).

## 3. Sequência de ignição

1. Validar gabarito (deny) — nenhuma ação antes.
2. Resolver motor via inventário (R75) — categoria `refutacao`.
3. Receber mapa estrutural da decompilação (nunca o bruto — R22 rolling summary).
4. Preencher tabela proteína×ruído + auditoria adversarial + varredura de catálogo (R8).
5. Escrever inventário lógico em /tmp/opencode/ (md + json).
6. Gate G-A categórico (R28) + nota R34 com bugs concretos.

## 4. Funções focadas

```python
def destilar(mapa: dict) -> dict:
    """Extrai proteína e descarta ruído do mapa estrutural."""
    proteina = [c for c in mapa.get("conceitos", []) if c.get("essencial")]
    ruido = [c for c in mapa.get("conceitos", []) if not c.get("essencial")]
    return {"essence": proteina, "discarded_noise": ruido}
```

## 5. Enforcement

- Motor recusa ignição se ação violar deny do gabarito (camada 2 é lei).
- Alteração de sampling sem novo crivo = proibida (R62/R66).