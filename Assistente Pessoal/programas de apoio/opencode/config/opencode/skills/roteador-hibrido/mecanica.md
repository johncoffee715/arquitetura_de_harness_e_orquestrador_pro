# ROTEADOR-HIBRIDO — Mecânica de Ignição

## 1. Seleção de motores (L0.5 + L0 — coexistência, R75)

| Camada | Modelo | Slot | Função |
|---|---|---|---|
| L0.5 | RWKV7-0.4B | :9084 | classificação SEMÂNTICA (1M ctx, RNN O(1), TTFT imediato) |
| L0 | Needle 2 | :9091 | payload JSON ESTRITO (sintaxe 100%) |
| F1/F2 | Qwen/Ornith | :9088/:8083 | raciocínio denso (só complexo) |

**Refutação do catálogo**: RWKV7 NÃO segue JSON sem GBNF (documento L0.5) — grammar obrigatória na chamada. Needle NÃO raciocina (45M) — só sintaxe.

## 2. Parâmetros de ignição

```json
{
  "rwkv": {"temp": 0.1, "max_tokens": 128, "grammar": "GBNF estrito"},
  "needle": {"temp": 0.0, "max_tokens": 256}
}
```

## 3. Sequência de ignição

1. Validar gabarito (deny: sem acordar GPU à toa).
2. **FASE 0**: RWKV7 classifica com GBNF → `{"intent": "operacional"|"complexo"|"saudacao", "tipo": "...", "confianca": n}`.
3. **RoTA**:
   - saudacao → resposta local (early-exit, zero GPU).
   - operacional (mcp/hook/cli/git) → **Needle 2** (payload JSON estrito).
   - complexo (brainstorm/codigo/rag) → **LLMs densos**.
4. **FASE 4**: RWKV7 ingere logs longos (sem perda — causa raiz no topo); Needle valida schema.

## 4. Funções focadas (Python 30-60 linhas por bloco)

```python
def rotear(texto: str) -> dict:
    """RWKV7 classifica (GBNF) → roteia direto/complexo."""
    intento = parse_intent(chamar_rwkv(texto)["choices"][0]["message"]["content"])
    if intento["intent"] == "operacional" and intento["tipo"] in ROTAS_DIRETAS:
        return {"rota": "direto", "destino": f"needle-{intento['tipo']}", "intento": intento,
                "payload": chamar_needle(texto)}
    if intento["intent"] == "saudacao":
        return {"rota": "direto", "destino": "resposta-local", "intento": intento}
    return {"rota": "complexo", "destino": "llm-densos", "intento": intento}
```

## 5. Enforcement

- RWKV7 SEMPRE com GBNF para JSON (deny: sem grammar = recusa).
- GPU só acorda em rota complexa (deny: acordar GPU à toa).