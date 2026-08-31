# HEFESTO-FORJA — Mecânica de Ignição

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `forja` (Needle 2, :9091 — 26M params, tool calling nativo, extração estruturada 100% conformidade, extrator de nível de byte).
- **Refutação do catálogo**: se o Needle estiver offline ou o payload exigir validação semântica profunda, refutar → `judge` (:9085, temp 0.15). Se exigir tool calling complexo, manter forja.
- **Fallback**: `judge` (:9085).

## 2. Parâmetros de ignição

```json
{
  "temp": 0.0,
  "top_k": 1,
  "top_p": 1.0,
  "repeat_penalty": 1.0,
  "max_tokens": 4096
}
```

- **Ganchos de backend**: cactus serve (OpenAI-compatible, :9091) — tool calling nativo; llama.cpp Vulkan para fallback judge.

## 3. Sequência de ignição

1. Validar gabarito (deny) — nenhuma ação antes.
2. Resolver motor via inventário (R75) — categoria `forja` (fallback judge).
3. Receber artefato helenizado (rolling summary + ponteiros — R22).
4. Empacotar + validar schema byte-level (validate_schema).
5. Persistir via tool calling (write_artifact / upsert_vault) + emit_manifest.
   Escopo de escrita = gabarito allow.paths (SPIEGEL com guard-gap-p5): governança (config/opencode,
   vault, state), harness operacional (scripts/tools/tests/bin/templates/data), globais
   (~/.opencode, ~/.config/opencode) e sandbox /tmp/opencode. Código de terceiros (repos/,
   cactus-build/, llama.cpp/, projetos/, cache/) = DENY ABSOLUTO — persistir via delegação/PR.
6. Panteão de validadores (R28/R34) + gate G-F com evidência fresca (R29).

## 4. Funções focadas

```python
def validar_payload(payload: dict, schema: dict) -> dict:
    """Valida payload contra schema estrito (byte-level)."""
    import jsonschema
    try:
        jsonschema.validate(payload, schema)
        return {"valid": True, "errors": []}
    except jsonschema.ValidationError as e:
        return {"valid": False, "errors": [e.message]}
```

## 5. Enforcement

- Motor recusa ignição se ação violar deny do gabarito (camada 2 é lei).
- Alteração de sampling sem novo crivo = proibida (R62/R66).