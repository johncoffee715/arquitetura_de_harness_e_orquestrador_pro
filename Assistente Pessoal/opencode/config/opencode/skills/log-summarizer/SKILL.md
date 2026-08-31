---
name: log-summarizer
description: "Sumarizador heurístico DETERMINÍSTICO de logs de ferramentas (pytest, go test, jest, grep, stack traces) — conta erros/warnings/PASSED/FAILED, captura primeiro erro/falha, comprime output verboso em resumo compacto (tail + assinatura + truncamento). ZERO chamada LLM — complementa o RWKV7 cortex para tool output rotineiro. Use para compactar logs de teste antes de injetar no contexto, ou quando precisar de resumo determinístico sem gastar inferência."
mode: skill
tags: "log, sumarizador, deterministico, pytest, go-test, jest, compressor, heuristica, sem-llm"
origin: helenizado:atomic-agent (log-summarizer.ts + result-compressor.ts)
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-08-31
  author: Gran-Mestre
  motor: nenhum (determinístico)
---

# LOG-SUMMARIZER — O Contador

Sumarização **heurística determinística** de logs de ferramentas — sem LLM, sem custo de inferência. Complementa o RWKV7 cortex (que é para contexto massivo 1M).

## Pipeline

1. **Input**: output de tool (stdin ou arquivo).
2. **`summarise_log()`**: conta totalLines, errorLines, warningLines, passCount, failCount; captura firstError/firstFailure (200 chars).
3. **`compress_result()`**: tail N linhas (12) + assinatura + truncamento (400 chars).
4. **Saída JSON** determinística (mesma entrada → mesma saída).

## Padrões reconhecidos

- pytest: `PASSED` / `FAILED`
- go test: `ok` / `FAIL`
- jest: `PASS` / `FAIL`
- Genérico: `error|exception` (erro), `warn(ing)?` (warning)

## Motor

- **NENHUM** — determinístico, Python stdlib puro (refutação R75: tool output rotineiro não justifica LLM; RWKV7 é para 1M ctx).
- **Sampling**: temp 0.0 (não aplicável — sem inferência).

## Uso

```bash
# Via stdin
cat test-output.log | python3 scripts/log_summarizer.py --summarise

# Via arquivo
python3 scripts/log_summarizer.py --compress test-output.log

# Saída JSON
python3 scripts/log_summarizer.py --summarise < test-output.log --json
```

## Output contract

```yaml
log_summarizer:
  totalLines: n
  errorLines: n
  warningLines: n
  passCount: n
  failCount: n
  firstError: "..." | null
  firstFailure: "..." | null
  compressed: {summary, truncated}
```

## Anti-padrões

- Chamar LLM para sumarizar (custo desnecessário).
- Inventar resumo (só conta o que existe).
- Processar binário.
- Interpretação semântica (isso é do LLM/cortex).