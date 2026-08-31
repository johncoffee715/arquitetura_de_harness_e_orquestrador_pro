# A2A-BRAINSTORM — Mecânica de Ignição

## 1. Seleção de motores (catálogo R75 — tríade fixa na VRAM)

| Papel | Categoria | Slot | Por quê |
|---|---|---|---|
| 🛠️ Propositor | `contrato-plano` | :9088 Qwen3.8-4B | tool calling, velocidade, precisão de sintaxe |
| 🧠 Refutador | `refutacao` | :9090 Ternary-8B | 8B de profundidade conceitual, BFCL 73.9 |
| ⚖️ Árbitro | `judge` | :9085 LLMJudge-3B | treinado para pontuação emparelhada, temp 0.15 |
| 🏛️ Escalação | `orquestrador` | :8083 Ornith-35B CPU | Suprema Corte — decisão final em impasse |

**Refutação do catálogo**: se um slot da tríade cair (R10), o loop NÃO reatribui papel (mata tensão) — registra redflag e escala direto ao 35B.

## 2. Parâmetros de ignição (samplers por papel — R61/R77)

```json
{
  "propositor": {"temp": 0.6, "top_k": 20, "top_p": 0.95, "max_tokens": 2048},
  "refutador": {"temp": 0.8, "top_k": 20, "top_p": 0.95, "max_tokens": 2048},
  "arbitro": {"temp": 0.15, "top_k": 10, "top_p": 0.9, "max_tokens": 1024},
  "escalacao": {"temp": 0.3, "top_k": 20, "top_p": 0.95, "max_tokens": 4096}
}
```

- **Ganchos de backend**: llama.cpp Vulkan (FA on, KV q4/q4 — R76); tríade na GPU >60 t/s; escalação na CPU.

## 3. Sequência de ignição (loop A2A)

1. Validar gabarito (deny) — nenhuma ação antes.
2. **Propositor** gera proposta v1 (plano/código/extração) com contrato (spec.md) no contexto.
3. **Refutador** inspeciona: falhas lógicas, desvios de contrato, gargalos → refutação com evidência.
4. **Árbitro** avalia: refutação procede? → nota R34 (0.0000001-100) + bugs concretos.
   - Nota < 90 → Propositor reescreve (loop).
   - Nota ≥ 90 com elogios concretos → **PASSOU_CATEGORICO** (R28/R40).
5. **Max iterações**: convergência média > 95.0 (R34) OU 3 rodadas sem impressão → **escalar 35B** (R18).
6. Veredito final + registro no decision-log.

## 4. Funções focadas (Python 30-60 linhas por bloco)

```python
def chamar_slot(port: int, papel: str, messages: list, sampling: dict) -> dict:
    """Chama um slot llama.cpp via API OpenAI-compatible."""
    import json, urllib.request
    payload = {"messages": messages, "temperature": sampling["temp"],
               "max_tokens": sampling.get("max_tokens", 2048)}
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/v1/chat/completions",
        data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())
```

## 5. Enforcement

- Motor recusa ignição se ação violar deny do gabarito (camada 2 é lei).
- Alteração de sampling sem novo crivo = proibida (R62/R66).