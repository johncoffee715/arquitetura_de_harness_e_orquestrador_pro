# Hefesto — Novo Familiar + Doutrina Unificada (autofagia · helenização · decompilação)

**Data:** 2026-08-26
**Origem:** `hefesto_creationist_v6.zip` (criação autoral do usuário, noite de 2026-08-25/26)
**SHA256 do artefato original:** `0057067d732eb4c1704fb3160a809d50375dfab8d84af4d50470e626c85ae793`

## O que aconteceu

1. **Artefato externo analisado** (Hefesto v6 "O Ferreiro Criacionista"): manifesto md + contrato json + engine py. 4 pilares: autofagia arquitetural, decompilação, helenização, forja; Panteão com 4 validadores (escala 0–100, convergência >95), self-learning/scaffold/healing, freeze 30s com fallback automático.
2. **Falha crítica encontrada no original:** `_evaluate_pillar` retornava score default **96.5 sem evidência** → auto-aprovação fraudulenta (sempre passava o gate). Corrigido na helenização: validador sem evidência → `UNKNOWN` + nota piso (antifraude).
3. **Ruído descartado:** porta :9090/Ternary-Bonsai-8B inexistentes, scan dirs `/var/run/opencode/models` e `/etc/opencode/llm_sockets` alheios ao harness, log em `/var/log/opencode`.
4. **Unificação:** os 3 temas (antes esparsos em professional-decompilation SKILL.md, .planning/autofagia/, seção 10 do TEMPLATE.md do Gran-Mestre) → **UM arquivo**: `config/opencode/skills/hefesto/SKILL.md` (doutrina completa: pipeline G-D→G-A→G-H→G-F, tabela proteína×ruído, helenização por tipo de recurso hook/plugin/skill/subagent/MCP/LSP/feature, Panteão R28/R34/R37/R40, output contract).
5. **Familiar criado:** `config/opencode/agent/hefesto.md` — subagent executor direto (R17), model `local-general/qwen3-8b`, temperature 0.0 (forja determinística).
6. **Órfãos descartados:** `arquitetura_harness_pro/skills/professional-decompilation/` (git rm, commit ad788db) e `gran-mestre-backup/.planning/autofagia/` (untracked, removido físico).

## Lições

- **Validador nunca tem default alto** — todo score exige evidência; senão é fraude estrutural.
- **Geometria declarada ≠ realidade local** (confirma RS6): paths/portas do artefato externo eram ficção — helenização mapeou para inventário real.
- Unificar doutrinas fragmentadas em 1 skill canônica elimina drift entre cópias (fonte única de regras, mesmo princípio do AGENTS.md).

## Artefatos globais criados

| Recurso | Path |
|---|---|
| Skill (doutrina única) | `/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/hefesto/SKILL.md` |
| Familiar (subagent) | `/mnt/dados/Assistente Pessoal/opencode/config/opencode/agent/hefesto.md` |

Cópia do original preservada fora do vault: zip em `~/Downloads/` (imutável).
