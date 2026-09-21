# Findings & Decisions — Autofagia do Gran-Mestre

## Requirements
- Aplicar planning-with-files (PWF) ao Gran-Mestre
- Identificar gaps entre GSD e PWF
- Implementar melhorias prioritárias
- Fechar ciclo de autofagia

## Research Findings

### O que é planning-with-files (PWF)
- Repositório: https://github.com/OthmanAdi/planning-with-files
- Versão: v3.7.0 (Jul 2026)
- Stars: 25.6k, Forks: 2.2k
- Benchmark: 96.7% pass rate
- Licença: MIT
- Autor: OthmanAdi
- Concorrente direto vendido por $2B (Manus → Meta)

### Core Pattern
```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)
→ Anything important gets written to disk.
```

Três arquivos de planejamento:
1. `task_plan.md` — Fases, progresso, decisões
2. `findings.md` — Pesquisa, descobertas, decisões técnicas
3. `progress.md` — Log de sessão, resultados de teste

### Inovações vs GSD

#### 1. UserPromptSubmit Hook (PWF-only)
PWF injeta o plano **a cada prompt do usuário**, não apenas antes de ferramentas. O PreToolUse injeta um resumo menor. O GSD só injeta contexto via CONTEXT.md manualmente.

#### 2. Attestation (SHA-256)
PWF calcula SHA-256 do `task_plan.md` e armazena em `.plan-attestation` (root) ou `.attestation` (scoped). Antes de injetar, verifica se o hash atual corresponde. Se não → **PLAN TAMPERED — injection blocked**.

O GSD tem Safety SHA (salvo antes de executar), mas é para rollback, não para integridade do plano.

#### 3. Completion Gate
PWF tem um `check-complete.sh` que verifica se TODAS as fases estão completas. Se não estiverem, o Stop hook notifica. Em modo `--gated`, o Stop hook bloqueia ativamente.

O GSD não tem nada equivalente — o agente pode simplesmente parar no meio.

#### 4. Session Recovery
PWF tem `session-catchup.py` que verifica se há contexto não sincronizado de sessões anteriores (via timestamps de arquivos, git diff).

O GSD tem `gsd-resume-work` mas depende de session-data salvos.

#### 5. Plan Resolution (múltiplos escopos)
PWF resolve planos em ordem:
1. `$PLAN_ID` (env var) → `.planning/$PLAN_ID/`
2. `.planning/.active_plan` → arquivo com slug
3. `.planning/*/` → diretório mais recente com `task_plan.md`
4. Raiz → `task_plan.md` no diretório atual

O GSD usa `.planning/` direto com fase numerada.

#### 6. Ledger (JSONL)
PWF v3.0+ tem `ledger-append`, `ledger-summary`, `phase-status` — append-only JSONL run ledger.

O GSD usa CONTEXT.md com texto livre.

#### 7. 2-Action Rule
PWF: "After every 2 view/browser/search operations, IMMEDIATELY save key findings to text files."

GSD: Não tem regra equivalente.

#### 8. 3-Strike Error Protocol
PWF formaliza: Attempt 1 (diagnose) → Attempt 2 (alternative) → Attempt 3 (broader rethink) → Escalate.

GSD: Tem retry-classifier com 8 categorias de erro, mas não formaliza o protocolo de 3 tentativas.

#### 9. Templates
PWF tem templates ricos com comentários explicativos (WHAT, WHY, WHEN, EXAMPLE).

GSD: PLAN.md é mais enxuto, sem exemplos inline.

#### 10. Suporte a 60+ agents
PWF instala em 60+ IDEs (Claude Code, Codex CLI, Cursor, Kiro, OpenCode, etc.) via SKILL.md standard.

GSD: Só funciona no ecossistema OpenCode.

### Gap Analysis Summary

| Inovação PWF | GSD Atual | Gap | Prioridade |
|---|---|---|---|
| **SKILL.md** | Skills/gran-mestre/SKILL.md **AUSENTE** | 🔴 CRÍTICO | Alta |
| **Attestation (SHA-256)** | Safety SHA (só rollback) | 🟡 MÉDIO | Alta |
| **Completion Gate** | Não existe | 🟡 MÉDIO | Alta |
| **findings.md** | RESEARCH.md (parcial) | 🟢 BAIXO | Média |
| **Ledger (JSONL)** | CONTEXT.md (texto livre) | 🟢 BAIXO | Média |
| **Session Recovery** | gsd-resume-work (similar) | 🟢 BAIXO | Baixa |
| **Plan Resolution** | .planning/ (simples) | 🟢 BAIXO | Baixa |
| **2-Action Rule** | Não existe | 🟢 BAIXO | Baixa |
| **3-Strike Protocol** | RetryClassifier (parcial) | 🟢 BAIXO | Baixa |
| **UserPromptSubmit Hook** | Não existe | 🟡 MÉDIO | Média |

### Decisão: Incorporar vs Instalar

**Opção A — Instalar PWF como skill:**
- ✅ Acesso imediato a toda infraestrutura PWF
- ❌ Hooks conflitantes com hooks existentes do Gran-Mestre
- ❌ Dois sistemas de planejamento concorrentes

**Opção B — Incorporar ideias seletivamente:**
- ✅ Sem conflito de hooks
- ✅ Evolução natural do GSD
- ❌ Mais trabalho manual
- ✅ SKILL.md precisa ser criado de qualquer forma (gap existente)

**Decisão: Opção B — Incorporar.**

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Incorporar ideias, não instalar PWF | Evita conflito de hooks; SKILL.md já é gap conhecido |
| Priorizar SKILL.md + Attestation + Completion Gate | 3 gaps mais críticos para integridade do pipeline |
| SKILL.md em skills/gran-mestre/ | Localização padrão do OpenCode para skills |
| Attestation via SHA-256 no PLAN.md | Mesmo mecanismo do Safety SHA, mas para integridade do plano |
| Completion Gate no Stop hook | Verifica se fase atual está completa antes de permitir parada |
| findings.md por fase | Em vez de RESEARCH.md global, um findings.md por diretório de fase |
| Ledger JSONL opcional | Pode ser adicionado depois como complemento ao CONTEXT.md |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| Skills/gran-mestre/SKILL.md ausente | Criar como parte da autofagia |
| Hooks.json já tem 30+ hooks | Novo hook de attestation precisa ser não-blocking |
| Completion gate pode conflitar com stop:format-typecheck | Implementar como check não-blocking (modo advisório) |

## Resources
- Repo PWF: https://github.com/OthmanAdi/planning-with-files
- Repo AAS: https://github.com/sickn33/agentic-awesome-skills
- Video: https://www.youtube.com/watch?v=Vg2ypKmtK8M
- SKILL.md standard: https://skill-management.github.io/skill-standard/
- OpenCode docs: ~/.opencode/docs/
- Gran-Mestre agent: ~/.opencode/agent/gran-mestre.md
- Gran-Mestre manifesto: ~/.config/opencode/registry/GRAN_MESTRE.md

## Inovações do AAS (antigravity-awesome-skills)

O AAS (Agentic Awesome Skills) complementa o planning-with-files com:

| Inovação AAS | Descrição | Aplicável ao Gran-Mestre? |
|---|---|---|
| **Agent-First Control Plane** | MCP local para busca/validação de skills | ✅ Sim — para discovery de skills |
| **1,969+ Skills Catalog** | Catálogo completo de skills | ✅ Sim — como referência |
| **AAS Core v15.1.0** | Stack validation, immutable planning | ✅ Sim — conceito transferível |
| **Specialized Plugins** | Plugins por domínio (Security, DevOps, QA) | ✅ Sim — integrar ao Gran-Mestre |
| **Workbench** | Review browser-local de stacks | ❌ Não essencial |
| **Agent Selection** | Agente escolhe skills, não rankings | ✅ Sim — refletir em decisões |

### Decisão sobre AAS

**Integrar conceitos do AAS ao Gran-Mestre:**
- Usar `AAS Core Stack Validation` como modelo para `compose_stack` do Gran-Mestre
- Criar `specialized-plugins.md` no docs/ do Gran-Mestre
- Adicionar `catalog_search` capability ao Gran-Mestre (via MCP local)

**Não instalar AAS como skill separada:**
- Conflito de arquitetura (AAS é control plane, Gran-Mestre é orchestrator)
- Melhor incorporar conceitos seletivamente

## Visual/Browser Findings
- README do PWF mostra 60+ IDEs suportados
- Banner v3: "Manus-style persistent file-based planning"
- 317 commits, 25.6k stars (crescimento explosivo em <24h)
- Benchmark: 2.7x faster recovery vs 6 methods
- Community forks: devis, multi-manus-planning, plan-cascade
