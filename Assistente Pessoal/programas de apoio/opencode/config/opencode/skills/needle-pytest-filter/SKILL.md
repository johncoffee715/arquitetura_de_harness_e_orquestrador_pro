---
name: needle-pytest-filter
description: "Filtro cirúrgico de logs pytest para o Needle 2 (janela rígida de 256 tokens) — extrai APENAS Localização (arquivo:linha), Assinatura (tipo de erro) e Delta (expected vs actual), descartando todo o ruído na CPU antes do binário. Determinístico, zero LLM. Use para preparar logs TDD falhos para o Needle 2 (Fase 4), ou qualquer stack trace que precise caber na janela de 256 tokens."
mode: skill
tags: "needle, pytest, filtro, cirurgico, janela-256, tdd, log, extracao, deterministico"
origin: helenizado: Needle 2 ai.md (2026-08-31)
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-08-31
  author: Gran-Mestre
  motor: nenhum (determinístico)
---

# NEEDLE-PYTEST-FILTER — O Cirurgião de Logs

Pré-processamento cirúrgico de logs pytest para o **Needle 2** (janela rígida de 256 tokens — sliding window descarta o início do texto). O log bruto estoura a janela; o filtro entrega **densidade pura**.

## Pipeline

1. **Input**: log pytest (stdin ou arquivo).
2. **📍 Localização**: regex `arquivo.py:linha:Tipo` (ex: `tests/router.py:42: AssertionError`).
3. **🛑 Assinatura**: linhas `E   ...` (mensagem da exceção).
4. **⚖️ Delta**: linhas `>   ...` com assert/expected/actual (o que o contrato exigia vs o que retornou).
5. **Verificação de janela**: tokens estimados ≤ 256 → `cabe_janela_256: true`.
6. **Saída JSON** determinística.

## Âncoras textuais do pytest

| Marcador | Significado |
|---|---|
| `>` | Linha exata do código que falhou |
| `E` | Mensagem da exceção (tipo + intro specção) |
| `arquivo.py:linha: Tipo` | Localização |
| `_____` | Delimitador de escopo |

## Motor

- **NENHUM** — determinístico, Python stdlib (regex). Zero LLM, zero VRAM.
- **Sampling**: temp 0.0 (não aplicável).

## Uso

```bash
# Via arquivo
python3 scripts/needle_pytest_filter.py test-output.log --json

# Via stdin
cat test-output.log | python3 scripts/needle_pytest_filter.py --json
```

## Output contract

```yaml
needle_pytest_filter:
  localizacoes: [{arquivo, linha, tipo}]
  assinaturas: ["AssertionError: expected 200 got 500"]
  deltas: ["assert response.status_code == 200"]
  total_linhas_originais: n
  tokens_estimados: n
  cabe_janela_256: bool
```

## Anti-padrões

- Chamar LLM para extrair (o Needle faz a extração estruturada — o filtro só pré-processa).
- Inventar localização/assinatura/delta.
- Exceder a janela 256 sem avisar.
- Processar binário.