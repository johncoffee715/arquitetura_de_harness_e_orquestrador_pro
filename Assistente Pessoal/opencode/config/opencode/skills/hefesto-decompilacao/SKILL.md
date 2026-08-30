---
name: hefesto-decompilacao
description: "Fase 1 do Hefesto — DECOMPILAÇÃO & MAPEAMENTO ESTRUTURAL. Leitura profunda de bases de código legadas, dumps ou binários descompilados de grande volume; isola a lógica bruta desmembrando funções opacas em blocos rastreáveis de dependência, com evidência rastreável E-xxx e classificação CONFIRMED..UNKNOWN. Use quando o Hefesto (dispatcher) rotear um artefato para a fase de decompilação."
mode: skill
tags: "decompilacao, hefesto, engenharia-reversa, mapeamento-estrutural, evidencia, arqueologo"
origin: helenizado:hefesto-v1
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-08-30
  author: Gran-Mestre
  motor: contrato-plano
---

# HEFESTO-DECOMPILACAO — O Arqueólogo

Fase 1 do pipeline Hefesto. Desconstruir o artefato ao nível factual — vale para binário (RE clássico) OU fonte/doc/zip (análise estrutural).

**Princípio central: nunca transformar hipótese em fato sem evidência.**

## Pipeline da fase

1. **INTAKE**: hash sha256, path, tamanho, método de aquisição. NUNCA modificar o original — cópia de trabalho em /tmp/opencode/.
2. **IDENTIFICATION**: formato, arquitetura, toolchain, dependências, entry points, packing.
3. **TRIAGE**: prioridade = Impact × Evidence Density × Centrality × Unknownness.
4. **ANÁLISE**: fluxo de controle/dados, componentes, interfaces, contratos. Cada descoberta = evidência ID `E-001...` com tipo, observação, reprodutibilidade.
5. **CORRELATION**: conclusão ganha confiança quando múltiplas fontes independentes convergem.

## Classificação obrigatória

`CONFIRMED | HIGH_CONFIDENCE | PROBABLE | POSSIBLE | UNKNOWN | CONTRADICTED`

Rastreio: `CONCLUSÃO → EVIDÊNCIA → MÉTODO → VALIDAÇÃO`. Nunca escrever fato onde há apenas evidência. Nunca preencher lacuna inventando comportamento — marcar `PARTIALLY UNDERSTOOD`.

## Motor

- **Categoria**: `contrato-plano` (:9088 Qwen3.8-4B — janela longa para mapeamento cruzado multi-arquivo).
- **Janela**: ctx_allocated do inventário; se task > janela → fragmentar (R22), nunca estourar.
- **Sampling**: temp 0.2 · top_k 20 · top_p 0.95 (R61/R77).
- **Refutação do catálogo**: se a janela do slot for insuficiente para o volume, refutar → rota nuvem (R20/R23) ou fragmentação R22.

## Gate G-D

Mapa estrutural completo com ≥1 evidência rastreável por afirmação central. Falhou → não avança.

## Output contract

```yaml
decompilation:
  artifact: {name, sha256, origin}
  structure_map: {...}
  evidence_total: n
  classification: {confirmed: n, high_confidence: n, probable: n, unknown: n}
  partially_understood: [lacunas]
```

## Anti-padrões

- Modificar o original.
- Declarar fato sem evidência E-xxx.
- Preencher lacuna com invenção.
- Copiar implementação literal.