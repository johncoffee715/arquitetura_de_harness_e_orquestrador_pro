# HEFESTO-DECOMPILACAO — Mecânica de Ignição

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (Qwen3.8-4B, :9088 — janela longa para mapeamento cruzado).
- **Refutação do catálogo**: verificar ctx_allocated real no inventário; se o volume do artefato exceder → fragmentar R22 (nunca estourar janela). Se mesmo fragmentado não couber → rota nuvem R20/R23.
- **Fallback**: `orquestrador` (:8083, janela 262144) para artefatos massivos.

## 2. Parâmetros de ignição

```json
{
  "temp": 0.2,
  "top_k": 20,
  "top_p": 0.95,
  "repeat_penalty": 1.1,
  "max_tokens": 4096
}
```

- **Ganchos de backend**: llama.cpp Vulkan (FA on, KV q4/q4 — R76); prefill/decode no limite do hardware.

## 3. Sequência de ignição

1. Validar gabarito (deny) — nenhuma ação antes.
2. Resolver motor via inventário (R75) — categoria `contrato-plano`.
3. INTAKE: hash sha256 + cópia de trabalho em /tmp/opencode/.
4. IDENTIFICATION → TRIAGE → ANÁLISE (evidências E-xxx) → CORRELATION.
5. Gate G-D categórico (R28) + nota R34 com bugs concretos.

## 4. Funções focadas

```python
def intake(path: str) -> dict:
    """Hash + cópia de trabalho. Nunca toca o original."""
    import hashlib, shutil
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    work = f"/tmp/opencode/work-{sha[:8]}/"
    shutil.copytree(path, work, dirs_exist_ok=True) if __import__("os").path.isdir(path) else shutil.copy2(path, work)
    return {"sha256": sha, "work": work}
```

## 5. Enforcement

- Motor recusa ignição se ação violar deny do gabarito (camada 2 é lei).
- Alteração de sampling sem novo crivo = proibida (R62/R66).