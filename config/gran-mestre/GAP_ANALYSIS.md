---
name: gap-analysis
description: "Análise de gaps e falhas do Gran-Mestre — verificação MIX completa."
mode: skill
origin: verificacao:mix
metadata:
  category: audit
  version: 1.0.0
  author: Gran-Mestre (pipeline MIX)
  verificacoes: 10
  gaps_criticos: 0
  gaps_medios: 4
  gaps_baixos: 2
  status: "OPERACIONAL COM PENDÊNCIAS"
---

# GAP ANALYSIS — Gran-Mestre

## Data: 2026-07-27 | Pipeline MIX

---

## Resumo Executivo

| Categoria | Quantidade | Status |
|-----------|-----------|--------|
| Verificações executadas | 10 | ✅ |
| Gaps críticos | 0 | 🟢 |
| Gaps médios | 4 | 🟡 |
| Gaps baixos | 2 | 🟢 |
| **Status geral** | **OPERACIONAL** | 🟡 |

---

## Verificações Executadas (10)

| # | Verificação | Status | Detalhe |
|---|-------------|--------|---------|
| 1 | Agents primary vs subagent | ✅ | 1 primary (gran-mestre), 43 subagents |
| 2 | Skills instaladas vs documentadas | ⚠️ | 87 skills, 1 sem SKILL.md |
| 3 | Hooks ativos vs documentados | ✅ | 18 hooks, todos existem |
| 4 | MCPs configurados vs disponíveis | ⚠️ | 1 configurado, 4 documentados |
| 5 | Symlinks e portabilidade | ⚠️ | 6/7 portáveis, 1 não |
| 6 | Backup e integridade | ✅ | 17 commits, SHA verificado |
| 7 | Gaps consolidados | ✅ | 4 médios, 2 baixos |
| 8 | Detalhamento dos gaps | ✅ | Análise completa |
| 9 | Agents reais vs documentados | ⚠️ | 44 reais, 61 documentados |
| 10 | Consolidação final | ✅ | OPERACIONAL COM PENDÊNCIAS |

---

## Gaps Críticos (0)

Nenhum gap crítico encontrado.

---

## Gaps Médios (4)

### Gap 1: security-review skill sem SKILL.md

**Problema:** `~/.opencode/skills/security-review/` existe mas só tem `MANIFEST.yaml`, sem `SKILL.md`.

**Impacto:** Skill não funcional — não pode ser invocada.

**Correção:** Criar `SKILL.md` ou remover a skill.

**Prioridade:** MÉDIA

### Gap 2: MCPs documentados mas não configurados

**Problema:** 4 MCPs estão documentados em `INVENTORY_AUDIT.md` mas não estão em `opencode.json`:
- codegraph
- context7
- grep_app
- lsp

**Impacto:** MCPs não disponíveis para uso.

**Correção:** Adicionar ao `opencode.json` ou remover da documentação.

**Prioridade:** MÉDIA

### Gap 3: 21 agents no REGISTRY sem .md no config

**Problema:** O `REGISTRY_SUBAGENTS.md` documenta 61 subagents, mas apenas 44 têm arquivo `.md` em `config/agents/`.

**Agents faltando (21):**
- Pipeline: atena, atlas, atreus, code-reviewer, prometheus
- Crossover: explore, librarian, oracle, metis, sisyphus, hepheastus, build, general
- Fable: fable-judge, fable-loop, fable-method
- Superpowers: superpowers-brainstorming, superpowers-verification
- GSD: gsd-verifier
- Héstia: hestia (tem skill, não tem agent .md)

**Impacto:** Agents não podem ser invocados por falta de definição.

**Correção:** Criar `.md` para cada agent faltando ou ajustar o REGISTRY.

**Prioridade:** MÉDIA

### Gap 4: ~/.npm symlink não portável

**Problema:** `~/.npm` aponta para `/home/johncoffee/.npm`, não para `/mnt/dados/opencode/npm`.

**Impacto:** Se o disco do sistema for formatado, o cache npm é perdido.

**Correção:** Mover para `/mnt/dados/opencode/npm` e criar symlink.

**Prioridade:** MÉDIA

---

## Gaps Baixos (2)

### Gap 5: user-configs com 5 arquivos

**Problema:** `user-configs/` tem 5 arquivos (correto), mas estava documentado como vazio na verificação inicial.

**Impacto:** Nenhum — informação desatualizada na verificação.

**Correção:** Nenhuma necessária.

**Prioridade:** BAIXA

### Gap 6: oh-my-openagents skills não verificadas

**Problema:** 16 skills do oh-my-openagent não foram verificadas localmente.

**Impacto:** Skills podem estar desatualizadas ou ausentes.

**Correção:** Verificar e sincronizar se necessário.

**Prioridade:** BAIXA

---

## Ações Recomendadas

### Imediatas (corrigir agora)

1. **Criar SKILL.md para security-review** ou remover a skill
2. **Adicionar MCPs ao opencode.json** ou ajustar documentação
3. **Criar .md para os 21 agents faltantes** ou ajustar REGISTRY

### Curto prazo (próxima sessão)

4. **Mover ~/.npm para /mnt/dados** para portabilidade
5. **Verificar oh-my-openagents skills** localmente

### Médio prazo

6. **Sincronizar REGISTRY com config real** — reconciliar 61 vs 44

---

## Conclusão

O sistema está **OPERACIONAL** com **4 gaps médios** e **2 gaps baixos**. Nenhum gap crítico. Os gaps médios são:
- 1 skill sem SKILL.md
- 4 MCPs não configurados
- 21 agents sem arquivo .md
- 1 symlink não portável

**Próxima ação:** Corrigir os 4 gaps médios para alcançar status **OPERACIONAL SEM PENDÊNCIAS**.

---

**Versão:** 1.0.0
**Data:** 2026-07-27
**Verificações:** 10
**Status:** OPERACIONAL COM PENDÊNCIAS
