# INVENTÁRIO ARQUITETURAL DO HARNESS
## Data: 2026-07-25 | Auto-gerado

---

## 1. RESUMO EXECUTIVO

| Componente | Total | Status |
|------------|-------|--------|
| OpenCode | v1.18.5 | ✅ Funcional |
| Agents | 44 | ✅ Todos com model_rotation |
| Skills | 10 | ✅ Todos com SKILL.md |
| Hooks | 14 | ✅ Funcionais |
| Registry | 12 entries | ✅ Schema canônico |
| Pipeline | 6 modos | ✅ Documentado |

---

## 2. AGENTS (44 total)

### Primary (1)
| Agent | Modelo | Fallback Chain |
|-------|--------|----------------|
| gran-mestre | claude-opus-4.7 | 5 fallbacks |

### Subagents (43)
| Categoria | Agents | Modelo Primary |
|-----------|--------|----------------|
| Gran-Mestre Pipeline | hestia, athena | claude-opus-4.7 |
| GSD | 34 agents | claude-opus-4.7 |
| Superpowers | 7 agents | claude-opus-4.7 |
| Outros | memory-keeper, reverser | claude-opus-4.7 |

### Model Rotation Status
```
✅ 44/44 agents têm model_rotation configurado
✅ max_retries_per_model: 1 (falha em 1x)
✅ escalate_on_failure: true
✅ continue_after_escalate: true (nunca para)
✅ restart_order: free_first (FREE + PAGOS)
```

---

## 3. SKILLS (10 total)

| Skill | Localização | Status |
|-------|-------------|--------|
| gran-mestre | ~/.opencode/skills/ | ✅ |
| hestia | ~/.opencode/skills/ | ✅ |
| athena | ~/.opencode/skills/ | ✅ |
| pxpipe | ~/.opencode/skills/ | ✅ |
| agent-reach | ~/.opencode/skills/ | ✅ |
| archify | ~/.opencode/skills/ | ✅ |
| browser-use | ~/.opencode/skills/ | ✅ |
| ck | ~/.opencode/skills/ | ✅ |
| fable-judge | ~/.opencode/skills/ | ✅ |
| security-review | ~/.opencode/skills/ | ✅ |

---

## 4. PIPELINE MODOS

| Modo | Agents | Gates | Uso |
|------|--------|-------|-----|
| TRIVIAL | 1 (sisyphus) | 0 | Tasks simples |
| SIMPLE | 1 (atlas) | 0 | Execução direta |
| MEDIUM | 3 (prometheus, hestia, atlas) | 0 | Pipeline básico |
| COMPLEX | 4 (prometheus, hestia, atlas, athena) | 0 | Pipeline completo |
| CRITICAL | 5+ (mesmo + reviewers) | 0 | Alta segurança |
| FEATURE | 6 fases | 4 | Cascata completa |

---

## 5. INTEGRAÇÃO ABSORVIDA

| Framework | Conceito | Status |
|-----------|----------|--------|
| Oh-My-Openagents | Orquestração | ✅ |
| Superpowers | TDD, code review | ✅ |
| Fable Method | Verificação adversarial | ✅ |
| MoA | Parallel + aggregator | ✅ |
| Ponytail | YAGNI ladder | ✅ |
| Improve | Audit→Plan→Execute | ✅ |
| SkillSpector | 68 vulnerability patterns | ✅ |
| DeepSpec | Speculative decoding | ✅ |
| drawio | Diagramming | ✅ |

---

## 6. SEGURANÇA

| Item | Status |
|------|--------|
| shell_validator | ✅ tokenize strategy |
| retry_classifier | ✅ categorized |
| safety_protocol | ✅ SHA + rollback |
| model_rotation | ✅ 44/44 agents |
| mode validation | ✅ primary/subagent only |

---

## 7. SYMLINKS

```
~/.config/opencode → /mnt/dados/opencode/config
~/.opencode → /mnt/dados/opencode
```

---

**Versão:** 1.0.0
**Data:** 2026-07-25
**Auto-gerado:** Gran-Mestre Inventory System