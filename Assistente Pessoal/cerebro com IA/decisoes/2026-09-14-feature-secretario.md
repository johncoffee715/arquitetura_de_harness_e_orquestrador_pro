---
tags: "secretario, feature, forja, hefesto"
data: 2026-09-14
---

# Feature: Secretário executivo do Bibliotecário (2026-09-14)

## Decisão

Criar a skill `secretario` — secretário executivo do bibliotecário no vault
Obsidian. Papéis travados (decision-log 22:30): **RWKV7 = Bibliotecário**
(autonomia total no vault) · **Needle2 = assistente** (execução) ·
**Qwen3-Embedding-0.6B = secretário** (registro/vetorial).

## Arquitetura

- **Triagem semântica**: cosseno sobre Qwen3-Embedding 1024-d (`:9097` GPU lote
  / `:9094` CPU tempo-real) contra centróides de `prototipos_intent.json`;
  margem de desempate 0.05, threshold 0.55, fallback lexical flagado.
- **Registro vetorial**: upsert real na coleção Qdrant `bibliotecario_1024`
  (Cosine, 1024-d) com payload `origem: "secretario"`; sem embedding real =
  bloqueado (placebo nunca opera — R96/R28).
- **Execução**: determinística local em Python puro (Needle2 `:9091` sem API
  pública em 2026-09-14 → acelerador futuro, não dependência).
- **Fala**: templates determinísticos pt-BR em `tooling/templates/`, só com
  dados reais via `--dados`; prosa rica escala ao bibliotecário.

## As 5 funções

1. Triagem semântica → despacho por rota.
2. Registro vetorial (`bibliotecario_1024`, `origem: "secretario"`).
3. Agenda/gatilhos (`tooling/data/agenda.json` + `due`).
4. Correspondência (resumo_diario, ata_decisao, lembrete_followup, nota_catalogacao).
5. Governança HITL (ação crítica sem `hitl:true` = bloqueio; mutações logadas
   no diário JSONL com quarentena prévia).

## Fallbacks

GPU `:9097` → CPU `:9094` → lexical + `vetor_placebo:true` (registro bloqueado).
Leitura profunda/curadoria → bibliotecário (RWKV7 `:9084`).

## Skill

Código em `/home/johncoffee/.config/opencode/skills/secretario/`
(SKILL.md, conceito.md, mecanica.md, mecanica.py, gabarito.json, schema.gbnf,
tooling/). Registrada em `opencode.jsonc` seção `skills`.
