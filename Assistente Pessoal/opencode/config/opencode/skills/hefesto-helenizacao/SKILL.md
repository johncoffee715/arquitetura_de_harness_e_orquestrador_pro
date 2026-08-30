---
name: hefesto-helenizacao
description: "Fase 3 do Hefesto — HELENIZAÇÃO COMPLETA DO ECOSSISTEMA. Reconstruir o código purificado traduzindo-o integralmente para a cultura idiomática do ecossistema de destino (tipagem estrita, modularidade nativa, padrões de performance); frontmatter YAML completo, instalação GLOBAL (R2/R44), provenance. Restrição rigorosa anti-linha-preguiçosa (R71). Use quando o Hefesto (dispatcher) rotear para a fase de helenização."
mode: skill
tags: "helenizacao, hefesto, traducao, ecossistema, normatizacao, frontmatter, global, tradutor"
origin: helenizado:hefesto-v1
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-08-30
  author: Gran-Mestre
  motor: contrato-plano
---

# HEFESTO-HELENIZACAO — O Tradutor

Fase 3 do pipeline Hefesto. Converter a essência ao padrão estrito do ecossistema de destino. Nunca copiar cegamente — SEMPRE adaptar.

## Restrição rigorosa de prompt (R71)

- PROIBIDO atalhos preguiçosos (linhas de código q4_k_m preguiçosas, comentários vagos, "etc.", implementação pela metade).
- Todo código reescrito deve ser completo, idiomático e funcional de ponta a ponta.
- Zero comentários vagos; zero código morto; zero dependência do framework original.

## Alvo por tipo de recurso

| Tipo | Quando forjar | Forma helenizada |
|---|---|---|
| **skill** | metodologia/procedimento reutilizável | `<global>/skills/<nome>/SKILL.md` + frontmatter YAML |
| **subagent** | execução isolada descartável | agent `.md` com frontmatter (`mode: subagent`) |
| **hook** | reação automática a evento | script idempotente registrado em hooks/ |
| **plugin** | comportamento transversal programático | plugin OpenCode nativo |
| **MCP** | integração com serviço externo | MCP server traversal-safe + fail-fast |
| **LSP** | linguagem com análise estática valiosa | config LSP global |
| **feature** | capacidade nova fim-a-fim | scaffolding resolutivo global (R44) |

## Campos obrigatórios (todo recurso helenizado)

`name` (lowercase-hífens) · `description` (1-2 linhas precisas) · `mode` · `origin` (prefixo `absorvido:`/`crossover:`/`helenizado:`) · `metadata` (category, version, date, source hash).

## Registro global (R2/R44)

Instalar em `/mnt/dados/Assistente Pessoal/opencode/config/opencode/` — invocável de QUALQUER instância. Proibido deixar em sessão isolada, /tmp ou projeto local.

## Motor

- **Categoria**: `contrato-plano` (:9088 Qwen3.8-4B — capacidade de programação para código limpo ponta-a-ponta).
- **Sampling**: temp 0.2 · top_k 20 · top_p 0.95 (R61/R77).
- **Refutação do catálogo**: se a reconstrução exigir mais profundidade, refutar → `orquestrador` (:8083).

## Gate G-H

Recurso parseável + funcional + instalado no path global + campos obrigatórios completos + provenance documentada. Falhou → não avança.

## Output contract

```yaml
helenization:
  targets: [{type, path}]
  fields_complete: bool
  provenance: {origin, source_hash}
  registry_updated: bool
  anti_lazy_check: bool
```

## Anti-padrões

- Copiar implementação literal.
- Comentários vagos / atalhos preguiçosos (R71).
- Path local/sessão isolada — tudo global (R2/R44).
- Recurso novo quando equivalente existe no catálogo (R8).