---
name: hefesto-autofagia
description: "Fase 2 do Hefesto — AUTOFAGIA CULTURAL DE CÓDIGO. Desconstruir o código legado, expurgar anti-padrões, dependências obsoletas e gordura sintática; extrair a proteína lógica (conceitos, invariantes, protocolos, métricas) e descartar o ruído; auditoria adversarial de falhas DO ORIGINAL; catálogo-primeiro R8. Use quando o Hefesto (dispatcher) rotear para a fase de autofagia."
mode: skill
tags: "autofagia, hefesto, digestao, purificacao, anti-padrao, estomago, essencia"
origin: helenizado:hefesto-v1
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-08-30
  author: Gran-Mestre
  motor: refutacao
---

# HEFESTO-AUTOFAGIA — O Estômago

Fase 2 do pipeline Hefesto. Extrair a ESSENCIA, nunca a implementação literal. Digestão quantitativa E qualitativa (R38).

## Tabela proteína × ruído

| Extrair (proteína) | Descartar (ruído) |
|---|---|
| Conceitos, invariantes, protocolos | Nomes de marca, cosmética |
| Métricas, gates, critérios de qualidade | Hardcodes de ambiente alheio (portas, paths inexistentes) |
| Padrões arquiteturais replicáveis | Código morto, duplicação |
| Falhas e vulnerabilidades DO ORIGINAL | Configuração acoplada ao ecossistema de origem |

## Auditoria adversarial obrigatória

Caçar bugs/fraudes no artefato original (ex.: validador com score default alto = auto-aprovação → refutar). Toda falha encontrada vira lição registrada no output.

## Catálogo primeiro (R8)

Antes de decidir construir, varrer registry/skills/agents/hooks/MCPs/LSPs existentes. Só o GAP vira trabalho de forja; o resto é mapeamento.

## Motor

- **Categoria**: `refutacao` (:9090 Ternary-8B — BFCL 73.9, excelente para estruturar Markdown/JSON intermediário limpo).
- **Sampling**: temp 0.3 · top_k 20 · top_p 0.95 (R61/R77).
- **Refutação do catálogo**: se o Ternary degradar em tarefas longas de digestão, refutar → `contrato-plano` (:9088) como alternativa.

## Gate G-A

Essência destilada (tabela proteína×ruído preenchida) + auditoria de falhas + GAP confirmado contra catálogo. Falhou → não avança.

## Output contract

```yaml
autophagy:
  essence: [conceitos, invariantes, protocolos, métricas]
  discarded_noise: [marca, cosmética, hardcodes alheios, código morto]
  flaws_found_in_original: [{falha, evidencia, licao}]
  gap_confirmed: bool
  inventory: {markdown: path, json: path}
```

## Anti-padrões

- Copiar implementação literal.
- Manter ruído (gordura sintática, dependências obsoletas).
- Tocar o original.
- Declarar GAP sem varrer o catálogo (R8).