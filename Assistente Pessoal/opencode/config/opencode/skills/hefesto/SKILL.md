---
name: hefesto
description: "Doutrina unificada de absorção tecnológica — DISPATCHER. Pipeline DECOMPILAÇÃO → AUTOFAGIA → HELENIZAÇÃO → FORJA, invocando a skill atômica certa por fase (hefesto-decompilacao, hefesto-autofagia, hefesto-helenizacao, hefesto-forja) conforme o artefato e o motor ideal por categoria (R75). Use ao absorver qualquer framework/agente/skill/plugin externo (zip, repo, binário, doc), ao criar hooks/plugins/skills/subagents/MCPs/LSPs/features a partir de fontes externas, ou quando 'autofagia', 'helenização', 'decompilação' ou 'antropofagia' forem mencionados."
mode: skill
tags: "autofagia, helenizacao, decompilacao, absorcao, forja, skill, plugin, hook, subagent, mcp, lsp, dispatcher"
origin: helenizado:hefesto-v1
metadata:
  category: methodology
  version: 2.0.0
  date: 2026-08-30
  author: Gran-Mestre
  replaces: [hefesto-v1-monolito]
---

# HEFESTO — Dispatcher (Decompile. Digerir. Helenize. Forge.)

Pipeline único e obrigatório para transformar artefatos externos (código, binário, zip, framework, agente, doc) em recursos nativos globais do harness (R2). **O Hefesto é o dispatcher: invoca a skill atômica certa para cada fase.**

```text
[ARTEFATO EXTERNO] → 1.DECOMPILAÇÃO → 2.AUTOFAGIA → 3.HELENIZAÇÃO → 4.FORJA → [RECURSO GLOBAL]
                        gate G-D         gate G-A        gate G-H        gate G-F
                        skill:           skill:          skill:          skill:
                        hefesto-         hefesto-        hefesto-        hefesto-
                        decompilacao     autofagia       helenizacao     forja
```

## Regra de dispatch

**Carregue a skill `<hefesto-X>` via skill-tool para a fase N.** Cada skill atômica contém seu pipeline, motor (categoria R75), gabarito (R77) e gate.

| Fase | Skill a carregar | Motor (categoria) | Gate |
|---|---|---|---|
| 1. Decompilação | `hefesto-decompilacao` | `contrato-plano` (:9088) | G-D |
| 2. Autofagia | `hefesto-autofagia` | `refutacao` (:9090) | G-A |
| 3. Helenização | `hefesto-helenizacao` | `contrato-plano` (:9088) | G-H |
| 4. Forja | `hefesto-forja` | `forja` (:9091, fb judge) | G-F |

## Seleção de skill por tipo de artefato

- **Binário/dump/código legado** → começar em `hefesto-decompilacao`.
- **Framework/doc/zip já estruturado** → começar em `hefesto-autofagia`.
- **Código a traduzir para o ecossistema** → `hefesto-helenizacao`.
- **Payload a validar/persistir** → `hefesto-forja`.

## Motor executável

```bash
python3 scripts/hefesto_motor.py --list-cpu          # inventário real (R35)
python3 scripts/hefesto_motor.py --resolve decompilacao   # categoria → slot (R75)
python3 scripts/hefesto_motor.py --execute '{"artifact":"...","phase":"forja"}'
```

O motor resolve categoria→slot via `harness/llm-inventory.json` (R75) e valida gabarito antes de ignição (R77 camada 2).

## Ferramental da Tríplice (.md/.py/.json/.gbnf) — tooling/

O Hefesto usa a tríplice estruturada como base na construção de novas features, integrando o llama.cpp como motor de inferência:

| Arquivo | Função |
|---|---|
| `tooling/llama_cpp_config.json` | Contrato de dados (schema) — Single Source of Truth dos parâmetros |
| `tooling/hefesto_llama_bridge.py` | Bridge unificado: compila flags + autodescoberta + webhook |
| `tooling/hefesto_feature.gbnf` | Gramática GBNF para features (JSON estrito) |
| `tooling/hefesto_deep_spec.gbnf` | Gramática GBNF para especificação profunda (types/defaults) |
| `tooling/llama_cpp_spec.md` | Spec Markdown gerada/atualizada pelo pipeline |

**Fluxo automático (webhook/agendamento):**
1. **Gatilho**: llama.cpp atualiza → GitHub Actions/CRON → POST no webhook (:8098).
2. **Descoberta**: `hefesto_llama_bridge.py --discover` detecta flags novas → injeta `"nova-flag": "PENDING_GBNF_VAL"` no JSON.
3. **Enriquecimento**: LLM preenche detalhes técnicos (types/defaults) com gramática `hefesto_deep_spec.gbnf`.
4. **Consolidação**: Python substitui valores pendentes e atualiza `llama_cpp_spec.md`.

```bash
# Compilar flags do config em comando executável
python3 skills/hefesto/tooling/hefesto_llama_bridge.py --compile

# Descobrir novas flags do llama.cpp e injetar no JSON
python3 skills/hefesto/tooling/hefesto_llama_bridge.py --discover

# Subir webhook de gatilho (GitHub Actions/CRON)
python3 skills/hefesto/tooling/hefesto_llama_bridge.py --webhook 8098
```

## Pré-requisitos herdados

**Self-Learning** (minerar conhecimento tácito) · **Self-Scaffold** (parsers/ganchos como subproduto) · **Self-Healing** (refutar input inválido, nunca aceitar acriticamente).

## R74 — Features gerais (modelo de 8 passos)

TODA criação de feature nova (hook, plugin, skill, subagent, MCP, LSP, script, watcher) segue o modelo validado 2026-08-28 (hook `stack-health-check.py`): verificar estado atual → spec integral → binding R27 → retry alternativo → registrar no opencode.jsonc (skills = OBJETO, nunca array) → validar JSON + teste real → sync preserva (deepcopy) → lição registrada. Contrato de qualidade: arquivo criado + compile OK + teste real passando + registro + JSON válido; fail-open em hooks; idempotência; logging em /tmp/opencode/.

## Anti-padrões (proibidos)

- Copiar implementação literal ou criar dependência do framework original.
- Declarar fato sem evidência (fase 1) ou validar sem evidência (fase 4).
- Score default alto, aprovação burocrática ("ok", "passou"), impressão simulada.
- Recurso novo quando equivalente já existe no catálogo (R8).
- Scaffolding local/temporário — tudo global (R2/R44).

## Output contract (obrigatório ao fim)

```yaml
artifact: {name, sha256, origin}
decompilation: {structure_map, evidence_total, confirmed: n, unknown: n}
autophagy: {essence: [...], discarded_noise: [...], flaws_found_in_original: [...], gap_confirmed: bool}
helenization: {targets: [{type, path}], registry_updated: bool}
forging: {validators_scores: {D: x, A: x, H: x, F: x}, average: x.x, converged: bool}
memory: {vault_entries: [...], lessons: [...]}
```