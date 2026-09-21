# BIBLIOTECARIO — Mecânica de Ignição

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `talamus-cortex` (RWKV7-G1d-0.4B, :9084 — janela 1.048.576, prefill 2448.65 t/s, decode 143.29, state fixo linear O(N)).
- **Refutação do catálogo**: RWKV7 0.4B é ideal para varrer/indexar/injetar (prefill domina); NÃO usar para raciocínio profundo (densidade 0.4B insuficiente — "lost in the middle" em 1M). Se a query exigir síntese profunda → escalar `contrato-plano` (:9088) ou `orquestrador` (:8083).
- **Fallback**: `contrato-plano` (:9088) para síntese; busca lexical pura (grep/glob) se RWKV offline.

## 2. Parâmetros de ignição

```json
{
  "temp": 0.1,
  "top_k": 10,
  "top_p": 0.9,
  "repeat_penalty": 1.1,
  "max_tokens": 1024
}
```

- **Ganchos de backend**: llama.cpp Vulkan (FA on, KV q4/q4 — R76); prefill massivo 2448 t/s para ingestão de blocos grandes; decode curto (respostas com referências).

## 3. Sequência de ignição

1. Validar gabarito (deny) — nenhuma ação antes.
2. Resolver motor via inventário (R75) — categoria `talamus-cortex` (:9084).
3. **Busca lexical**: glob/grep no Vault por termos da query → top-N arquivos com paths reais.
4. **Busca semântica (Qdrant)**: POST /collections/gran_mestre_docs/points/search (se populado) → reforça ranking.
5. **Prefill RWKV7**: POST /v1/chat/completions com system prompt restritivo + trechos recuperados (com paths) + query.
6. **Veredito**: resposta com referências exatas + gate R28 (PASSOU_CATEGORICO se 100% paths reais).

## 4. Funções focadas (Python 30-60 linhas por bloco)

```python
def recuperar(query: str, vault: str, top_n: int = 5) -> list[dict]:
    """Busca lexical no Vault + reforço Qdrant. Retorna trechos com paths reais."""
    import subprocess, json
    # 1. lexical: grep -ril termos no vault
    termos = query.lower().split()[:4]
    hits = set()
    for t in termos:
        r = subprocess.run(["grep", "-ril", t, vault], capture_output=True, text=True)
        hits.update(r.stdout.splitlines())
    # 2. Qdrant (opcional, graceful)
    try:
        import urllib.request
        body = json.dumps({"vector": [0.0]*4, "limit": top_n}).encode()
        req = urllib.request.Request("http://localhost:6333/collections/gran_mestre_docs/points/search",
                                     data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=2) as resp:
            qd = json.loads(resp.read())
        hits.update(p["payload"].get("path", "") for p in qd.get("result", []) if p.get("payload"))
    except Exception:
        pass  # Qdrant é reforço, nunca bloqueio
    return [{"path": p} for p in sorted(hits)[:top_n] if p.startswith(vault)]
```

## 5. Enforcement

- Motor recusa ignição se ação violar deny do gabarito (camada 2 é lei).
- Alteração de sampling sem novo crivo = proibida (R62/R66).