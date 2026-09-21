# LOG-SUMMARIZER — Mecânica de Ignição

## 1. Seleção de motor (catálogo R75 — refutação)

- **Categoria alvo**: NENHUMA — **determinístico, sem LLM** (refutação do catálogo: RWKV7 cortex é para contexto massivo 1M; tool output rotineiro não justifica inferência).
- **Fallback**: nenhum — se o script falhar, retorna erro explícito (nunca chama LLM).

## 2. Parâmetros de ignição

```json
{
  "max_summary_length": 400,
  "max_tail_lines": 12,
  "temp": 0.0
}
```

- **Ganchos de backend**: nenhum (puro Python stdlib — zero dependência).

## 3. Sequência de ignição

1. Validar gabarito (deny: sem LLM, sem inventar).
2. Receber output (stdin ou arquivo).
3. `summarise_log()`: conta linhas, erros, warnings, PASSED/FAILED; captura primeiro erro/falha.
4. `compress_result()`: tail N linhas + assinatura + truncamento a 400 chars.
5. Saída JSON determinística.

## 4. Funções focadas (Python 30-60 linhas por bloco)

```python
import json, re, sys

def summarise_log(output: str) -> dict:
    """Conta sinais de frameworks de teste (pytest/go/jest) + erros/warnings."""
    lines = output.splitlines()
    err = warn = passed = failed = 0
    first_err = first_fail = None
    for ln in lines:
        if re.search(r"\b(error|exception)\b", ln, re.I):
            err += 1
            first_err = first_err or ln.strip()[:200]
        elif re.search(r"\bwarn(ing)?\b", ln, re.I):
            warn += 1
        if re.search(r"\b(PASSED|PASS|ok)\b", ln):
            passed += 1
        if re.search(r"\b(FAILED|FAIL)\b", ln):
            failed += 1
            first_fail = first_fail or ln.strip()[:200]
    return {"totalLines": len(lines), "errorLines": err, "warningLines": warn,
            "passCount": passed, "failCount": failed,
            "firstError": first_err, "firstFailure": first_fail}
```

## 5. Enforcement

- Motor recusa se ação violar deny (sem LLM, sem inventar).
- Determinismo testado por TDD (mesma entrada → mesma saída).