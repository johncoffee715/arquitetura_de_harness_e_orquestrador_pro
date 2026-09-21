---
regra: R74
titulo: "MODELO DE IMPLEMENTAÇÃO DE FEATURES GERAIS (Hefesto)"
fonte: AGENTS.md (linha 875)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R74 — MODELO DE IMPLEMENTAÇÃO DE FEATURES GERAIS (Hefesto) — promulgado 2026-08-28 ═══

**Regra**: TODA criação de feature nova (hook, plugin, skill, subagent, MCP, LSP, script, watcher — seja qual for) DEVE seguir o modelo de implementação validado em 2026-08-28 (criação do hook `stack-health-check.py`). O Hefesto é o executor padrão; o Gran-Mestre supervisiona.

## Pipeline obrigatório (8 passos)

1. **VERIFICAR ESTADO ATUAL** — antes de criar, inspecionar o que já existe (hooks registrados, formato do opencode.jsonc, bindings de agentes, catálogo R8). Nunca criar sobre o que já existe.
2. **DELEGAR AO HEFESTO com spec integral** — packet com: deliverable (path exato), requirements numerados (comportamento, fail-open, timeout, idempotência), verification commands obrigatórios (py_compile + testes reais com stdin JSON), return contract (confirmação + output dos testes + JSON final).
3. **SE O BINDING FALHAR → CORRIGIR REFERÊNCIAS (R27)** — erro "Model not found: X" = binding desatualizado nos .md dos agentes/skills. Corrigir `model:` para o ID real (ex.: `local-forge/qwen3.8-4b` → `local-forge/qwen3.8-4b-distill`) em TODOS os arquivos, depois retry.
4. **RETRY com subagente alternativo se necessário** — se o hefesto falhar 2× por binding/runtime, usar `general` com a MESMA spec (não perder o contrato).
5. **REGISTRAR no opencode.jsonc** — hooks → `hooks.session.start`; skills → objeto `{}` (NUNCA array — erro de schema "Expected object | undefined"); agents → lista. Validar JSON com parser real.
6. **VALIDAR JSON final + teste completo** — parse com node (strip comments preservando URLs), health da stack, teste real do hook (matar porta → hook revive).
7. **GARANTIR QUE O SYNC PRESERVA** — sync-llm-stack.py usa `deepcopy(current)` e preserva skills/hooks/permission; rodar `--apply` e confirmar "inalterado" nos campos críticos.
8. **REGISTRAR LIÇÃO/REGRAS** — lição no decision-log + vault Obsidian; regras novas no AGENTS.md (R71-R74).

## Contrato de qualidade (R28/R34)
- Feature entregue = arquivo criado + compile OK + teste real passando (não só sintaxe) + registro no config + JSON válido.
- Fail-open obrigatório em hooks (nunca bloquear session.start).
- Idempotência obrigatória (não duplicar processos/registros).
- Logging em `/tmp/opencode/` (nunca /var/log ou path inexistente).
- Formato skills = OBJETO `{}` (o array quebra o opencode: "Expected object | undefined, got [...] skills").

## Exemplo canônico (2026-08-28)
- Feature: hook `stack-health-check.py` (auto-revive da stack no session.start)
- Fluxo: verificação → delegação hefesto (spec 10 requisitos) → binding falhou → corrigido R27 (3 arquivos) → retry general → hook criado + testado (REVIVED real) → registrado no opencode.jsonc (4º hook) → JSON validado → sync --apply preservou → lição registrada.


---

## Extensão universal — Hefesto para cumprimento e aperfeiçoamento de regras

> Upgrade R74 (2026-09-18): o Hefesto não serve só à criação — serve à manutenção contínua do corpo normativo.

**Mandato**: o Hefesto (dispatcher DECOMPILAÇÃO → AUTOFAGIA → HELENIZAÇÃO → FORJA) DEVE ser usado SEMPRE também para aperfeiçoamento e cumprimento das regras — não apenas para criação de features novas. O Gran-Mestre supervisiona, como no pipeline original.

**Escopo estendido**: o objeto de trabalho expande de "features" para **regras + ecossistema + mente coletiva da biblioteca no Obsidian**. Onde houver drift, gap ou upgrade pendente no corpo normativo, aplica-se R74.

**Automação (R101)**: ao detectar drift/gap/upgrade de regra (via ingestão por upgrade do setor de regras), rotear ao Hefesto com spec curta (regra alvo + delta desejado + comando de verificação); registrar a lição no vault; REUSAR o pipeline de 8 passos existente — nunca criar fluxo paralelo novo.

**Otimização**: visa automatizar, otimizar espaço/tempo, ganhar t/s e aperfeiçoar o ecossistema. Absorve os ângulos de R14 (autofagia + helenização), R44 (refinamento contínuo), R47 (inventário→grafo) e R101 (setor de regras) SEM duplicá-las — R8 anti-reinvenção: catálogo primeiro, construir só o gap.

**Guardrail (R94)**: o Hefesto NUNCA deleta regra permanente. Regra obsoleta → QUARENTENA (mover para setor de arquivo, não remover) + LOG REVERSÍVEL (path original, data, motivo, diff). Reversão sempre possível; o Bibliotecário audita.
