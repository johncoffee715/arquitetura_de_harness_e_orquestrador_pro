---
name: gran-mestre-pipeline-modes
description: "Inventário completo dos 6 modos de pipeline do Gran-Mestre: agentes, skills, MCPs, gates e rotação de modelos por modo."
version: 7.0.0
date: 2026-07-25
status: REFERENCIA
---

# PIPELINE MODES — Inventário Completo do Gran-Mestre

## Visão Geral

O Gran-Mestre classifica toda requisição em **6 níveis de complexidade** usando o `ContextAnalyzer` (método regex-determinístico). Cada nível roteia para um pipeline diferente com agentes, gates e modelos próprios.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CONTEXT ANALYZER (regex-deterministic)            │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────────┤
│ TRIVIAL  │ SIMPLE   │ MEDIUM   │ COMPLEX  │ CRITICAL │ FEATURE      │
│ 1 agent  │ 1 agent  │ 3 agents │ 4 agents │ 5 agents │ 6 fases      │
│ 0 gates  │ 0 gates  │ 0 gates  │ 0 gates  │ 0 gates  │ 4 gates      │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────────┘
```

---

## MODO 1 — TRIVIAL

> Tarefas de 1 arquivo, <10 linhas, sem novo comportamento. Execução direta sem orquestração.

### Agentes Envolvidos

| Agente | Tipo | Função | Modelo Primário |
|--------|------|--------|-----------------|
| **Sisyphus** | subagent | Execução trivial (edição simples, correção rápida) | `opencode/gpt-5-nano` |

### Skills

Nenhuma skill é carregada.

### MCPs

Nenhum MCP necessário.

### Gates

**0 gates** — execução direta sem aprovação.

### Modelo de Rotação

```yaml
agent: sisyphus
category: EXPLORATION
primary: opencode/gpt-5-nano
fallback:
  - github-copilot/claude-haiku-4.5
  - opencode/glm-5
  - opencode/big-pickle
max_retries_per_model: 1
escalate_on_failure: true
continue_after_escalate: true
restart_cycle_on_exhaust: true
restart_order: free_first
```

### Restrições

- **Escopo máximo:** 1 arquivo, <10 linhas
- **Não delega** para subagents
- **Não usa** skills externas
- **Não toca** múltiplos arquivos

### Fluxo

```
Usuário → Gran-Mestre → ContextAnalyzer (classifica: TRIVIAL)
                              ↓
                        Sisyphus (executa diretamente)
                              ↓
                        ✅ Concluído (sem gates)
```

---

## MODO 2 — SIMPLE

> Tarefas simples que podem ser executadas com mini-plano. Atlas direto sem decomposição prévia.

### Agentes Envolvidos

| Agente | Tipo | Função | Modelo Primário |
|--------|------|--------|-----------------|
| **Atlas** | subagent | Execução direta com mini-plano | `github-copilot/claude-sonnet-4.6` |

### Skills

| Skill | Quando Usada |
|-------|-------------|
| **skill-pxpipe** | Disponível para redução de tokens se necessário |

### MCPs

Nenhum MCP necessário.

### Gates

**0 gates** — execução sem aprovação formal.

### Modelo de Rotação

```yaml
agent: atlas
category: EXECUTION
primary: github-copilot/claude-sonnet-4.6
fallback:
  - opencode/claude-sonnet-4-6
  - github-copilot/gpt-5.5
  - opencode/gpt-5.5
  - opencode/kimi-k2.5
max_retries_per_model: 1
escalate_on_failure: true
continue_after_escalate: true
restart_cycle_on_exhaust: true
restart_order: free_first
```

### Restrições

- **TDD obrigatório** para Atlas
- **Safety SHA** antes de executar
- Atlas pode escrever código neste modo (diferente da cascata)

### Fluxo

```
Usuário → Gran-Mestre → ContextAnalyzer (classifica: SIMPLE)
                              ↓
                        Atlas (mini-plano + execução TDD)
                              ↓
                        ✅ Concluído (sem gates)
```

---

## MODO 3 — MEDIUM

> Tarefas que precisam de decomposição, validação e execução. Pipeline de 3 agentes sem gates.

### Agentes Envolvidos

| Agente | Tipo | Função | Modelo Primário | Ordem |
|--------|------|--------|-----------------|-------|
| **Prometheus** | subagent | Decomposição de requisitos em plano | `github-copilot/claude-opus-4.7` | 1º |
| **Héstia** | subagent | Validação do plano contra pedido original | `github-copilot/claude-opus-4.7` | 2º |
| **Atlas** | subagent | Execução do plano validado | `github-copilot/claude-sonnet-4.6` | 3º |

### Skills

| Skill | Agente que Usa | Função |
|-------|---------------|--------|
| **skill-hestia** | Héstia | Critérios e comandos de validação |

### MCPs

Nenhum MCP necessário.

### Gates

**0 gates** — Héstia atua como filtro interno, mas não há gate formal de aprovação do usuário.

### Modelo de Rotação por Agente

#### Prometheus (CRITICAL)
```yaml
primary: github-copilot/claude-opus-4.7
fallback:
  - opencode/claude-opus-4-7
  - github-copilot/gpt-5.5
  - opencode/gpt-5.5
  - github-copilot/gemini-3.1-pro-preview
  - opencode/gemini-3.1-pro
```

#### Héstia (CRITICAL)
```yaml
primary: github-copilot/claude-opus-4.7
fallback:
  - opencode/claude-opus-4-7
  - github-copilot/gpt-5.5
  - opencode/gpt-5.5
  - github-copilot/claude-sonnet-4.6
  - opencode/claude-sonnet-4-6
  - opencode/kimi-k2.5
  - opencode/gpt-5-nano
  - github-copilot/claude-haiku-4.5
  - opencode/glm-5
  - opencode/big-pickle
```

#### Atlas (EXECUTION)
```yaml
primary: github-copilot/claude-sonnet-4.6
fallback:
  - opencode/claude-sonnet-4-6
  - github-copilot/gpt-5.5
  - opencode/gpt-5.5
  - opencode/kimi-k2.5
```

### Fluxo

```
Usuário → Gran-Mestre → ContextAnalyzer (classifica: MEDIUM)
                              ↓
                        Prometheus (decompõe requisitos em plano)
                              ↓
                        Héstia (valida plano vs pedido original)
                              ↓
                        Atlas (executa plano com TDD)
                              ↓
                        ✅ Concluído (sem gates)
```

---

## MODO 4 — COMPLEX

> Tarefas que além de decomposição e validação, precisam de revisão macro. Pipeline de 4 agentes.

### Agentes Envolvidos

| Agente | Tipo | Função | Modelo Primário | Ordem |
|--------|------|--------|-----------------|-------|
| **Prometheus** | subagent | Decomposição de requisitos | `github-copilot/claude-opus-4.7` | 1º |
| **Héstia** | subagent | Validação do plano | `github-copilot/claude-opus-4.7` | 2º |
| **Atlas** | subagent | Execução do plano | `github-copilot/claude-sonnet-4.6` | 3º |
| **Atena** | subagent | Revisão macro do diff total | `github-copilot/claude-opus-4.7` | 4º |

### Skills

| Skill | Agente que Usa | Função |
|-------|---------------|--------|
| **skill-hestia** | Héstia | Critérios e comandos de validação |
| **skill-athena** | Atena | Checklists de revisão macro (5 dimensões) |
| **skill-pxpipe** | Disponível | Redução de tokens |

### MCPs

Nenhum MCP necessário (revisão é interna, não escreve memória persistente).

### Gates

**0 gates** — Atena revisa, mas não há gate formal. Veredicto: `APPROVED` / `APPROVED_WITH_CAVEATS` / `CHANGES_REQUIRED`.

### Modelo de Rotação por Agente

#### Prometheus (CRITICAL)
```yaml
primary: github-copilot/claude-opus-4.7
fallback: [opencode/claude-opus-4-7, gpt-5.5, gemini-3.1-pro-preview]
```

#### Héstia (CRITICAL)
```yaml
primary: github-copilot/claude-opus-4.7
fallback: [opencode/claude-opus-4-7, gpt-5.5, claude-sonnet-4.6, kimi-k2.5]
```

#### Atlas (EXECUTION)
```yaml
primary: github-copilot/claude-sonnet-4.6
fallback: [opencode/claude-sonnet-4-6, gpt-5.5, kimi-k2.5]
```

#### Atena (CRITICAL)
```yaml
primary: github-copilot/claude-opus-4.7
fallback:
  - opencode/claude-opus-4-7
  - github-copilot/gpt-5.5
  - opencode/gpt-5.5
  - github-copilot/claude-sonnet-4.6
  - opencode/claude-sonnet-4-6
  - opencode/kimi-k2.5
  - opencode/gpt-5-nano
  - github-copilot/claude-haiku-4.5
  - opencode/glm-5
  - opencode/big-pickle
```

### Dimensões de Revisão da Atena

1. **Coerência cross-task** — Tasks se conectam logicamente?
2. **Acoplamento** — Componentes estão adequadamente desacoplados?
3. **Arquitetura** — Padrões e convenções são seguidos?
4. **Segurança** — Não há superfície de ataque exposta?
5. **Veredicto** — APPROVED / APPROVED_WITH_CAVEATS / CHANGES_REQUIRED

### Fluxo

```
Usuário → Gran-Mestre → ContextAnalyzer (classifica: COMPLEX)
                              ↓
                        Prometheus (decompõe requisitos)
                              ↓
                        Héstia (valida plano vs pedido)
                              ↓
                        Atlas (executa plano com TDD)
                              ↓
                        Atena (revisão macro: 5 dimensões)
                              ↓
                        ✅ Concluído (sem gates formais)
```

---

## MODO 5 — CRITICAL

> Tarefas de alto risco com revisão reforçada. Pipeline de 5 agentes com reviewers paralelos.

### Agentes Envolvidos

| Agente | Tipo | Função | Modelo Primário | Ordem |
|--------|------|--------|-----------------|-------|
| **Prometheus** | subagent | Decomposição de requisitos | `github-copilot/claude-opus-4.7` | 1º |
| **Héstia** | subagent | Validação do plano | `github-copilot/claude-opus-4.7` | 2º |
| **Atlas** | subagent | Execução do plano | `github-copilot/claude-sonnet-4.6` | 3º |
| **Atena** | subagent | Revisão macro do diff total | `github-copilot/claude-opus-4.7` | 4º |
| **+reviewers-paralelos** | agents externos | Revisão adicional paralela | Varia | 5º |

### Skills

| Skill | Agente que Usa | Função |
|-------|---------------|--------|
| **skill-hestia** | Héstia | Critérios e comandos de validação |
| **skill-athena** | Atena | Checklists de revisão macro |
| **skill-pxpipe** | Disponível | Redução de tokens |
| **skill-gran-mestre** | Gran-Mestre | Pipeline definition + safety protocol |

### MCPs

| MCP | Quando Usado | Função |
|-----|-------------|--------|
| **mcp-obsidian-vault** | Opcional neste modo | Memória persistente (arquivamento) |

### Gates

**0 gates formais**, mas **requer aprovação humana** para:
- Rotas CRITICAL
- Mudanças em arquivos de config core

### Modelo de Rotação por Agente

Todos os agentes CRITICAL usam a mesma chain de fallback:

```yaml
category: CRITICAL
primary: github-copilot/claude-opus-4.7
fallback_chain:
  1. opencode/claude-opus-4-7
  2. github-copilot/gpt-5.5
  3. opencode/gpt-5.5
  4. github-copilot/gemini-3.1-pro-preview
  5. opencode/gemini-3.1-pro
  6. github-copilot/claude-sonnet-4.6
  7. opencode/claude-sonnet-4-6
  8. opencode/kimi-k2.5
  9. opencode/gpt-5-nano
 10. github-copilot/claude-haiku-4.5
 11. opencode/glm-5
 12. opencode/big-pickle
```

Atlas mantém a chain de EXECUTION:

```yaml
category: EXECUTION
primary: github-copilot/claude-sonnet-4.6
fallback: [opencode/claude-sonnet-4-6, gpt-5.5, kimi-k2.5]
```

### Hooks de Segurança (Este Modo)

| Hook | Função |
|------|--------|
| `safety-sha` | Hash antes de qualquer alteração de estado |
| `attestation-gate` | Verificação de attestação |
| `completion-gate` | Validação de conclusão |
| `2-action-rule` | Limite de 2 ações por iteração |
| `3-strike-protocol` | 3 falhas → escala ao usuário |

### Fluxo

```
Usuário → Gran-Mestre → ContextAnalyzer (classifica: CRITICAL)
                              ↓
                        Prometheus (decompõe requisitos)
                              ↓
                        Héstia (valida plano — máx 3 ciclos)
                              ↓
                        Atlas (executa com TDD + safety SHA)
                              ↓
                        Atena (revisão macro reforçada)
                              ↓
                        +reviewers-paralelos (revisão adicional)
                              ↓
                        ⚠️ Requer aprovação humana
                        ✅ Concluído (sem gates formais, mas com hooks)
```

---

## MODO 6 — FEATURE (Cascata)

> Pipeline completo de 6 fases com 4 gates de aprovação. Usado para features significativas que justificam o ciclo completo de descoberta → contrato → plano → execução → revisão → entrega.

### Visão Geral das Fases

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FEATURE PIPELINE — 6 Fases, 4 Gates              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FASE 1: DESCOBERTA         [3 componentes]                        │
│  Prometheus → Fable Method → Brainstorming                         │
│  ⏸️ GATE 1: usuário aprova direção                                  │
│                                                                     │
│  FASE 2: CONTRATO           [3 componentes]                        │
│  Spec Writer → Héstia → Fable Judge                                │
│  ⏸️ GATE 2: usuário aprova spec                                     │
│                                                                     │
│  FASE 3: PLANO              [3 componentes]                        │
│  Plan Writer → Fable Loop → Héstia                                 │
│  ⏸️ GATE 3: usuário aprova plano                                    │
│  💾 Safety: SHA salvo aqui                                          │
│                                                                     │
│  FASE 4: EXECUÇÃO           [4 componentes]                        │
│  Atlas → Fable Loop → Implementer → Code Reviewer                   │
│  ⚡ sem gates — commits atômicos                                    │
│                                                                     │
│  FASE 5: REVISÃO MACRO     [2 componentes]                        │
│  Atena → Fable Judge                                                │
│                                                                     │
│  FASE 6: ENTREGA           [3 componentes]                        │
│  Verification → Héstia → Fable Judge                               │
│  ⏸️ GATE 4: relatório → cerebral memory                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Detalhamento por Fase

---

#### FASE 1 — DESCOBERTA

| Componente | Tipo | Função | Modelo |
|------------|------|--------|--------|
| **Prometheus** | subagent | Decomposição leve do contexto | `github-copilot/claude-opus-4.7` |
| **Fable Method** | skill | Loop em 1 pedido (filtro 1) | N/A (skill) |
| **Brainstorming** | skill | Dialoga livremente, propõe 2-3 abordagens (filtro 2) | N/A (skill) |

**Gate 1:** Usuário aprova a direção (modo interativo) ou Héstia proxy (modo autônomo).

---

#### FASE 2 — CONTRATO

| Componente | Tipo | Função | Modelo |
|------------|------|--------|--------|
| **Spec Writer** (superpowers-spec-writer) | subagent | Transforma direção em design doc | `local/qwen3.5-27b` |
| **Héstia** | subagent | Valida spec contra pedido original (filtro 1) | `github-copilot/claude-opus-4.7` |
| **Fable Judge** | skill | Audita resultado pronto (filtro 2) | N/A (skill) |

**Gate 2:** Usuário aprova o spec.

---

#### FASE 3 — PLANO

| Componente | Tipo | Função | Modelo |
|------------|------|--------|--------|
| **Plan Writer** (superpowers-plan-writer) | subagent | TDD, tasks bite-sized, código completo | `local/qwen3.5-27b` |
| **Fable Loop** | skill | Decompõe em sub-tasks e sub-agentes (filtro 1) | N/A (skill) |
| **Héstia** | subagent | Valida cobertura, contratos, verificabilidade (filtro 2) | `github-copilot/claude-opus-4.7` |

**Gate 3:** Usuário aprova o plano.
**Safety:** SHA do git salvo aqui (fases 1-3 não tocam código).

---

#### FASE 4 — EXECUÇÃO

| Componente | Tipo | Função | Modelo |
|------------|------|--------|--------|
| **Atlas** | subagent | Supervisor: sequencia tasks, gerencia git | `github-copilot/claude-sonnet-4.6` |
| **Fable Loop** | skill | Cria subagentes frescos por task (filtro 1.5) | N/A (skill) |
| **Implementer** (superpowers-implementer) | subagent | Operário: loop TDD por task (filtro 2) | `omniroute/auto/coding` |
| **Code Reviewer** (superpowers-code-reviewer) | subagent | Revisão micro por task (filtro 3) | varia |

**Sem gates** — commits atômicos, progresso visível.
**Regra:** Atlas NUNCA escreve código na cascata (só gerencia).

---

#### FASE 5 — REVISÃO MACRO

| Componente | Tipo | Função | Modelo |
|------------|------|--------|--------|
| **Atena** | subagent | Revisão holística do diff total (filtro 1 macro) | `github-copilot/claude-opus-4.7` |
| **Fable Judge** | skill | Audita qualidade, arquitetura, contrato (filtro 2 macro) | N/A (skill) |

**Veredicto:** `APPROVED` / `APPROVED_WITH_CAVEATS` / `CHANGES_REQUIRED`.

---

#### FASE 6 — ENTREGA

| Componente | Tipo | Função | Modelo |
|------------|------|--------|--------|
| **Verification** | subagent | Evidência fresca de ferro (filtro 2) | varia |
| **Héstia** | subagent | Validação final contra pedido original (filtro 1) | `github-copilot/claude-opus-4.7` |
| **Fable Judge** | skill | Audita evidência, emite veredito final (filtro 3) | N/A (skill) |

**Gate 4:** Relatório do Gran-Mestre → cerebral memory (Shared Brain).

### Todos os Gates do Modo FEATURE

| Gate | Fase | Quem Aprova | Modo Interativo | Modo Autônomo |
|------|------|-------------|-----------------|---------------|
| GATE 1 | Fase 1 | Usuário | Aprova direção | Héstia proxy |
| GATE 2 | Fase 2 | Usuário | Aprova spec | Héstia proxy |
| GATE 3 | Fase 3 | Usuário | Aprova plano | Héstia proxy |
| GATE 4 | Fase 6 | Gran-Mestre | Gera relatório | Auto |

### Skills Completas Usadas no Modo FEATURE

| Skill | Fase(s) | Função |
|-------|---------|--------|
| **skill-gran-mestre** | Todas | Pipeline definition + safety protocol |
| **skill-hestia** | 2, 3, 6 | Validação de spec, cobertura, entrega |
| **skill-athena** | 5 | Revisão macro (5 dimensões) |
| **skill-pxpipe** | Todas | Redução de tokens (quando necessário) |
| **Fable Method** | 1 | Loop em 1 pedido |
| **Fable Judge** | 1, 2, 5, 6 | Auditoria adversarial |
| **Fable Loop** | 3, 4 | Decomposição em sub-tasks |
| **Brainstorming** | 1 | Proposição de abordagens |

### MCPs Necessários

| MCP | Fase | Função |
|-----|------|--------|
| **mcp-obsidian-vault** | 6 | Memória persistente: ingestão, resumo, entidades, conceitos |

### Hooks de Segurança (Modo FEATURE)

| Hook | Fase | Função |
|------|------|--------|
| `safety-sha` | 3→4 | SHA checkpoint antes de tocar código |
| `attestation-gate` | Todas | Verificação de attestação |
| `completion-gate` | Todas | Validação de conclusão |
| `2-action-rule` | Todas | Limite de ações por iteração |
| `3-strike-protocol` | Todas | 3 falhas → escala ao usuário |

### Modos de Autonomia

```yaml
cascade:
  phases: 6
  supervisor_worker_split: inegociavel
  autonomy_modes:
    interactive: "4 gates, aprovação do usuário em cada um (default)"
    autonomous: "validador atua como proxy de aprovação, só escala ao usuário se reprovar 2x"
```

### Modelo de Rotação Completo (Cascata)

#### Gran-Mestre (Primary)
```yaml
primary: github-copilot/claude-opus-4.7
fallback: [opencode/claude-opus-4-7, gpt-5.5, gemini-3.1-pro-preview, gemini-3.1-pro]
max_retries_per_model: 1
escalate_on_failure: true
continue_after_escalate: true
restart_cycle_on_exhaust: true
restart_order: free_first
```

#### Agents CRITICAL (Héstia, Atena, Prometheus)
```yaml
primary: github-copilot/claude-opus-4.7
fallback_chain: 12 modelos (T1→T4)
max_retries_per_model: 1
```

#### Agents de EXECUÇÃO (Atlas, Implementer)
```yaml
primary: github-copilot/claude-sonnet-4.6
fallback_chain: 4 modelos
max_retries_per_model: 1
```

#### Spec Writer / Plan Writer
```yaml
primary: local/qwen3.5-27b
```

#### Implementer
```yaml
primary: omniroute/auto/coding
```

### Fluxo Completo

```
Usuário → Gran-Mestre → ContextAnalyzer (classifica: FEATURE)
                              ↓
                   ╔═══════════════════════════════════╗
                   ║  FASE 1: DESCOBERTA               ║
                   ║  Prometheus → Fable Method →      ║
                   ║  Brainstorming                     ║
                   ║  ⏸️ GATE 1: aprova direção         ║
                   ╠═══════════════════════════════════╣
                   ║  FASE 2: CONTRATO                 ║
                   ║  Spec Writer → Héstia →           ║
                   ║  Fable Judge                      ║
                   ║  ⏸️ GATE 2: aprova spec           ║
                   ╠═══════════════════════════════════╣
                   ║  FASE 3: PLANO                    ║
                   ║  Plan Writer → Fable Loop →       ║
                   ║  Héstia                           ║
                   ║  ⏸️ GATE 3: aprova plano          ║
                   ║  💾 SHA salvo                      ║
                   ╠═══════════════════════════════════╣
                   ║  FASE 4: EXECUÇÃO                 ║
                   ║  Atlas → Fable Loop →             ║
                   ║  Implementer → Code Reviewer       ║
                   ║  ⚡ sem gates                      ║
                   ╠═══════════════════════════════════╣
                   ║  FASE 5: REVISÃO MACRO            ║
                   ║  Atena → Fable Judge              ║
                   ╠═══════════════════════════════════╣
                   ║  FASE 6: ENTREGA                  ║
                   ║  Verification → Héstia →          ║
                   ║  Fable Judge                      ║
                   ║  ⏸️ GATE 4: → cerebral memory     ║
                   ╚═══════════════════════════════════╝
```

---

## Tabela Comparativa

| Propriedade | TRIVIAL | SIMPLE | MEDIUM | COMPLEX | CRITICAL | FEATURE |
|-------------|---------|--------|--------|---------|----------|---------|
| **Qtd agentes** | 1 | 1 | 3 | 4 | 5 | 6+ |
| **Qtd gates** | 0 | 0 | 0 | 0 | 0 | 4 |
| **Fases** | 1 | 1 | 1 | 1 | 1 | 6 |
| **TDD obrigatório** | Não | Sim | Sim | Sim | Sim | Sim (Fase 4) |
| **Safety SHA** | Não | Sim | Sim | Sim | Sim | Sim (Fase 3→) |
| **Revisão macro** | Não | Não | Não | Sim (Atena) | Sim (Atena+) | Sim (Fase 5) |
| **Aprovação humana** | Não | Não | Não | Não | Recomendada | Sim (4 gates) |
| **Shared Brain** | Não | Não | Não | Não | Opcional | Sim (Fase 6) |
| **Escalabilidade** | — | — | Héstia valida | +Atena macro | +Reviewers paralelos | Pipeline cascata |
| **Modelo primário** | gpt-5-nano | sonnet-4.6 | opus-4.7+sonnet | opus-4.7×3+sonnet | opus-4.7×4+sonnet+ext | Todos |

---

## Escalabilidade e Registry

O CapabilityIndex (greedy cover) seleciona automaticamente o melhor conjunto de componentes:

```
Registry atual: 12 entries
├── 1 agent (gran-mestre) — orquestra tudo
├── 5 subagents — executam trabalho
├── 1 MCP — memória persistente
├── 4 skills — habilidades empacotadas
└── 1 tool — safety hook
```

Conforme novos componentes são registrados no `agent-registry.json`:
1. O **CapabilityIndex** os descobre automaticamente
2. O **ContextAnalyzer** classifica a complexidade
3. O Gran-Mestre **orquestra** o melhor conjunto
4. **Nenhuma reconfiguração** é necessária

---

## Cloud Escalation

```
trigger: "executor falhou OU validador reprovou N vezes"
chain: [omniroute, opencode-go, opencode-zen]
```

Quando todos os modelos locais falham, o pipeline escala para a nuvem.

---

**Versão:** 7.0.0
**Data:** 2026-07-25
**Fontes:** `WORKFLOW_IMPLEMENTADO.md`, `gran-mestre.md`, `agent-registry.json`, `MODEL_ROTATION.md`, `HESTIA.md`, `ATHENA.md`, `superpowers-*.md`
**Status:** REFERÊNCIA
