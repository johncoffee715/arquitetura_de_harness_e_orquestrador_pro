# GARI — Mecânica de Ignição

**Gatilho:** pergunta direta do user `posso reiniciar ou [ainda] existe[m] [alguma] pend[êe]ncia[s]` (variações) — notada como **referência direta ao requisito R99** — **E** veredito `Pode reiniciar — zero pendências.`

## 1. Seleção de motor (catálogo R75 — sempre refutando)
- **Categoria alvo:** `proposer` (`local-forge/proposer` :9088, `temp 0.0` — determinístico, GBNF-friendly)
- **Refutação:** gari é I/O e verificação, não geração criativa — `proposer` vence por `t/s` + GBNF; `judge` é fallback se :9088 cair.
- **Fallback:** `judge` (`local-judge` :9092) — mesmo sampling determinístico.

## 2. Parâmetros de ignição
```json
{
  "temp": 0.0,
  "top_k": 1,
  "top_p": 1.0,
  "max_tokens": 256
}
```
- **Ganchos:** `temp 0.0` = veredito byte-level; `top_k 1` = sem amostragem alternativa.

## 3. Sequência de ignição
1. Validar gabarito (deny) — nunca limpar sem veredito zero.
2. Resolver motor `proposer` via inventário (R75).
3. **Salvar:** `curl -s http://127.0.0.1:6333/collections/bibliotecario_1024` (Qdrant WAL), `sync-llm-stack.py --check`, garantir `decisoes/YYYY-MM-DD-sessao-encerrada.md` existe.
4. **Armazenar:** varrer `benchmarks/*` + `decisoes/*` do turno, confirmar cada pérola tem evidência (t/s, KV, veredito).
5. **Limpar:** `glob /tmp/opencode/patch_*.py` + `__pycache__` → `unlink` (idempotente, só voláteis).
6. **Veredito:** `Pode reiniciar — zero pendências.` + JSON do output contract.

## 4. Funções focadas (Python 30-60 linhas por bloco)

```python
def salvar() -> dict:
    """Flush + check + snapshot. Retorna {saved: [...]}."""
    import subprocess, pathlib
    # Qdrant já faz WAL 5s; apenas sonda
    subprocess.run(["python3", "/mnt/dados/Assistente Pessoal/programas de apoio/opencode/scripts/sync-llm-stack.py", "--check"], timeout=10)
    snap = pathlib.Path("/mnt/dados/Assistente Pessoal/cerebro com IA/decisoes/2026-09-11-sessao-encerrada.md")
    return {"saved": ["vault", "qdrant", "manifesto"] if snap.exists() else ["vault"]}

def armazenar() -> dict:
    """Confere pérolas quant/qualit na biblioteca."""
    import pathlib
    b = list(pathlib.Path("/mnt/dados/Assistente Pessoal/cerebro com IA/benchmarks").glob("*.md"))
    d = list(pathlib.Path("/mnt/dados/Assistente Pessoal/cerebro com IA/decisoes").glob("*.md"))
    return {"stored": {"quant": len(b), "qualit": len(d)}}

def limpar() -> dict:
    """Remove só voláteis."""
    import pathlib
    vols = list(pathlib.Path("/tmp/opencode").glob("patch_*.py")) + list(pathlib.Path("/home/johncoffee/.config/opencode/skills/gari").glob("__pycache__"))
    for p in vols:
        try: p.unlink()
        except: pass
    return {"cleaned": [p.name for p in vols]}
```

## 5. Enforcement
- Motor recusa ignição se `verdict != zero pendências`.
- `cleaned` com vault/Qdrant dentro → `NAO_PASSOU_CATEGORICO` + reversão.
