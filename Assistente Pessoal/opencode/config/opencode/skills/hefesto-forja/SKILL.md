---
name: hefesto-forja
description: "Fase 4 do Hefesto — FORJA DO NOVO SOFTWARE & VALIDAÇÃO (Tool Calling). Empacotar a saída final, validar esquemas estritos de dados (byte-level), estruturar JSONs de configuração do projeto e disparar tool calling para persistir o artefato no filesystem ou no Vault do Obsidian; sanity check definitivo com 100% de conformidade de dados. Use quando o Hefesto (dispatcher) rotear para a fase de forja."
mode: skill
tags: "forja, hefesto, validacao, schema, tool-calling, persistencia, obsidian, selador, needle"
origin: helenizado:hefesto-v1
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-08-30
  author: Gran-Mestre
  motor: forja
---

# HEFESTO-FORJA — O Selador

Fase 4 do pipeline Hefesto. Síntese determinística com precisão cirúrgica (temperature 0.0). TDD obrigatório: RED→GREEN→REFACTOR. Cobertura ≥80%.

## Função operacional

1. **Empacotar** a saída final (artefato + metadados + manifest).
2. **Validar esquemas estritos** de dados — `validate_schema` byte-level (100% conformidade).
3. **Estruturar JSONs** de configuração do projeto.
4. **Tool calling** para persistir: `write_artifact` (filesystem) / `upsert_vault` (Obsidian).
5. **Sanity check definitivo** — payload perfeitamente formatado para consumo automatizado.

## Motor

- **Categoria**: `forja` (:9091 Needle 2 — 26M params, tool calling nativo, extração estruturada com 100% de conformidade de dados, extrator de nível de byte).
- **Fallback**: `judge` (:9085 LLMJudge-3B, temp 0.15) se forja offline.
- **Sampling**: temp 0.0 (determinístico) · max_tokens 4096.

## Panteão — validação categórica (R28/R34/R37/R40)

- 4 validadores independentes (um por pilar: decomposição, digestão, normatização, síntese).
- Escala **0.0000001–100** (R34); nota SEMPRE acompanhada de bugs concretos apontados.
- Convergência: **média > 95.0 encerra o dev loop**.
- Abaixo de 95 → refutação incansável (R40): loop A2A até impressão real (≥90 + elogios concretos + bugs corrigidos).
- Validador sem evidência → `UNKNOWN` + nota piso (NUNCA default alto).
- 3 rodadas sem convergência → escalar camada superior (R18).

## Gate G-F (saída)

Evidência fresca de execução real (R29) + veredito de impressão + memória cerebral alimentada (R26: aprendizados/ + log.md) + lição arquivada. Falhou → não entrega.

## Output contract

```yaml
forging:
  artifact: {name, sha256, origin}
  schema_validated: bool
  persisted: [{target: fs|vault, path}]
  manifest: {...}
  validators_scores: {D: x, A: x, H: x, F: x}
  average: x.x
  converged: bool
  memory: {vault_entries: [...], lessons: [...]}
```

## Anti-padrões

- Saída não-validada (schema frouxo).
- Persistir sem validação.
- Score default alto, aprovação burocrática ("ok", "passou"), impressão simulada.
- Declarar done sem evidência fresca (R29).