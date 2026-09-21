# NEEDLE-PYTEST-FILTER — Mecânica de Ignição

## 1. Seleção de motor (catálogo R75 — refutação)

- **Categoria alvo**: NENHUMA — **determinístico, sem LLM** (refutação: o Needle 2 tem janela 256; o filtro é pré-processamento na CPU, não inferência).
- **Fallback**: nenhum — se o filtro falhar, retorna erro explícito (nunca chama LLM).

## 2. Parâmetros de ignição

```json
{
  "janela_alvo_tokens": 256,
  "max_chars": 1500,
  "temp": 0.0
}
```

- **Ganchos de backend**: nenhum (Python stdlib — grep/awk-like via regex).

## 3. Sequência de ignição

1. Validar gabarito (deny: sem LLM, sem inventar).
2. Receber log pytest (stdin ou arquivo).
3. Extrair 📍 Localização (regex `arquivo.py:linha:tipo`).
4. Extrair 🛑 Assinatura (linhas `E   ...`).
5. Extrair ⚖️ Delta (linhas `>   ...` com assert/expected/actual).
6. Estimar tokens e verificar janela 256 → saída JSON.

## 4. Funções focadas (Python 30-60 linhas por bloco)

```python
import json, re, sys

RE_LOCATION = re.compile(r"([\w./\\-]+\.py):(\d+):\s*(\w+(?:Error|Exception|Failure)?)")
RE_EXCEPTION = re.compile(r"^E\s+(.+)$", re.MULTILINE)
RE_CODE_LINE = re.compile(r"^>\s+(.+)$", re.MULTILINE)

def filtrar_pytest(log: str) -> dict:
    """Extrai Localização/Assinatura/Delta (densidade pura para janela 256)."""
    locs = [{"arquivo": m.group(1), "linha": m.group(2), "tipo": m.group(3)}
            for m in RE_LOCATION.finditer(log)][:3]
    assinaturas = [m.group(1).strip() for m in RE_EXCEPTION.finditer(log)][:3]
    codigo = [m.group(1).strip() for m in RE_CODE_LINE.finditer(log)][:3]
    deltas = [c for c in codigo if re.search(r"assert|expected|actual|!=|==", c, re.I)][:2]
    payload = json.dumps({"localizacoes": locs, "assinaturas": assinaturas, "deltas": deltas})
    return {"localizacoes": locs, "assinaturas": assinaturas, "deltas": deltas,
            "tokens_estimados": max(1, len(payload) // 4),
            "cabe_janela_256": len(payload) // 4 <= 256}
```

## 5. Enforcement

- Motor recusa se ação violar deny (sem LLM, sem inventar).
- Determinismo testado por TDD (mesma entrada → mesma saída).