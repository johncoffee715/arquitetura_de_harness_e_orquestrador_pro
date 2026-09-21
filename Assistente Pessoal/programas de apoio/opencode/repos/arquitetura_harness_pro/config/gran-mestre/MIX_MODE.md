---
name: gran-mestre-mix
description: "Modo MIX — unificação de COMPLEX + CRITICAL + FEATURE. Modo operacional máximo do Gran-Mestre com delegação DINÂMICA via Registry, sem hardcoded agents por fase."
mode: primary
origin: gran-mestre-original (crossover oh-my-openagents × Superpowers × Fable Method × OpenClaude)
metadata:
  category: orchestration
  version: 5.0.0
  author: Gran-Mestre
  crossover: oh-my-openagents(4.19.2) × Superpowers × Fable Method × OpenClaude(0.26.0)
  mix_level: COMPLEX + CRITICAL + FEATURE
  dynamic_delegation: true
  registry_based: true
  dev_loop_levels: 3
  model: omniroute/auto/best-free
  max_validation_cycles: 5
---

# MODO MIX — Manual de Operação (Delegação Dinâmica)

## 1. DEFINIÇÃO

**MIX** é o modo operacional que unifica COMPLEX + CRITICAL + FEATURE com delegação dinâmica:

| Faceta | Origem | O que ativa |
|--------|--------|-------------|
| **COMPLEX** | Gran-Mestre | Todos agents + skills + tools + MCPs compatíveis selecionados dinamicamente |
| **CRITICAL** | Gran-Mestre | Pipeline de segurança + rollback automático + Fable Judge |
| **FEATURE** | Gran-Mestre | Pipeline em Cascata (6 fases, 4 gates) |

**MIX = COMPLEX + CRITICAL + FEATURE** — nenhum recurso fica ocioso, nenhum é hardcoded.

## 2. QUANDO USAR MIX

| Gatilho | Ação |
|---------|------|
| "modo MIX" | Ativar modo MIX |
| Tarefa nova não classificada | Usar MIX (default) |
| Autofagia de repositório externo | Usar MIX obrigatoriamente |
| Feature com design em aberto | Usar MIX |
| Auditoria de segurança | Usar MIX |

## 3. DELEGAÇÃO DINÂMICA vs. HARDCODED

### ANTES (hardcoded — v3.x)
```
Fase 4: Atlas → Fable Loop → Implementer → Code Reviewer
```
### DEPOIS (dinâmico — v5.x)
```
Fase 4 [EXECUÇÃO]:
1. Consulta Registry por tags: execution, implementation, coding, review, git
2. Seleciona subagents: atlas, build, code-reviewer, general
3. Seleciona skills: dev-loop, pxpipe
4. Seleciona MCPs: codegraph
5. Seleciona LSPs: todos da stack
6. Compõe equipe e delega
```

## 4. PIPELINE MIX — 6 Fases

### Despacho Inicial (Pré-Fase-1)
```
pedido do usuário
  │
  ▼
Classificação do Escopo
  ├─ trivial (1 arquivo, <10 linhas) → Dev Loop N1
  ├─ pergunta/avaliação → responder direto
  ├─ requisitos claros → entra na Fase 3 (PLANO)
  └─ escopo aberto → Fase 1 completa (DESCOBERTA)
```

### Fases

Cada fase consulta o Registry dinamicamente por **tags de capacidade**:

| Fase | Tags de Consulta |
|------|-----------------|
| **1. DESCOBERTA** | discovery, research, interview, brainstorming |
| **2. CONTRATO** | spec, contract, design, validation |
| **3. PLANO** | planning, tdd, tasks, verification |
| **4. EXECUÇÃO** | execution, implementation, coding, review |
| **5. REVISÃO** | review, macro, architecture, audit |
| **6. ENTREGA** | delivery, verification, release, memory |

### Gates
| Gate | Fase | Quem Aprova |
|------|------|-------------|
| GATE 1 | Fase 1 | Usuário |
| GATE 2 | Fase 2 | Usuário |
| GATE 3 | Fase 3 | Usuário |
| GATE 4 | Fase 6 | Gran-Mestre → Shared Brain |

## 5. DEV LOOP INTEGRADO

| Nível | Ciclo | Quando |
|-------|-------|--------|
| **N1 — ReAct** | pensa → age → observa → repete | Tasks de 1-3 arquivos |
| **N2 — Mini Loop** | spec → TDD → implementa → merge | Features locais |
| **N3 — Human Loop** | decide → métricas → triagem → planeja → PR | Épicos complexos |

**Escalonamento:** N1 → 3 falhas → N2 → incerteza → N3 → humano decide.

## 6. SEGURANÇA

| Medida | Implementação |
|--------|---------------|
| SHA antes de executar | Safety Protocol |
| Rollback automático | git reset --hard |
| Fable Judge | Verificação adversarial em 3 fases |
| Model rotation | OmniRoute fallback automático |
| Cerebral Memory | Obsidian vault (Shared Brain) |

## 7. O QUE MIX NÃO FAZ

- Não executa sem supervisão (gates exigem aprovação)
- Não modifica o harness fora do repositório de trabalho
- Não envia dados para terceiros (telemetria desligada)
- Não substitui o julgamento humano (gates de aprovação)
- Não força todos os subagents a concordar (cada um é independente)

---

**Versão:** 5.0.0
**Data:** 2026-07-29
**Delegação:** Dinâmica via Registry
**Modo:** MIX (COMPLEX + CRITICAL + FEATURE)
