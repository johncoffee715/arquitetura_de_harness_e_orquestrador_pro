---
name: gran-mestre-architecture
description: "Arquitetura do Gran-Mestre — único agent primário e meta-orquestrador. Todo o resto é subagent."
mode: primary
origin: gran-mestre-original
metadata:
  category: architecture
  version: 1.0.0
  author: Gran-Mestre
  decision: "2026-07-27 — Gran-Mestre é o ÚNICO agent primário"
---

# ARQUITETURA — Gran-Mestre como Único Agent Primário

## Decisão Fundamental

> **O Gran-Mestre é o único agent primário e meta-orquestrador.**
> **Todo o resto é subagent disponível para orquestração.**

## Hierarquia

```
┌─────────────────────────────────────────────────────────────┐
│                    GRAN-MESTRE (primário)                    │
│              Meta-orquestrador — ponto de entrada único      │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PIPELINE    │    │  CROSSOVER   │    │   EXTERNAL   │
│  SUBAGENTS   │    │  SUBAGENTS   │    │   SUBAGENTS  │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Subagents por Categoria

### 1. Pipeline Gran-Mestre (6)

| Subagent | Função | Quando |
|----------|--------|--------|
| prometheus | Planejamento | Fase 3 |
| hestia | Validação rastreabilidade | Fases 2, 3, 6 |
| atlas | Execução (alias Sisyphus+git-master) | Fase 4 |
| atena | Revisão macro (composição Oracle) | Fase 5 |
| atreus | Entrega | Fase 6 |
| code-reviewer | Code review | Fase 4 |

### 2. Crossover Absorvido (16)

| Subagent | Origem | Função |
|----------|--------|--------|
| explore | oh-my-openagents | Busca rápida |
| librarian | oh-my-openagents | Documentação |
| oracle | oh-my-openagents | Arquitetura/debug |
| prometheus+metis | oh-my-openagents | Planejamento modo entrevista |
| sisyphus | oh-my-openagents | Orquestrador principal |
| hepheastus | oh-my-openagents | Executor autônomo |
| fable-method | fable-method | Classificação |
| fable-loop | fable-method | Orquestração completa |
| fable-judge | fable-method | Verificação adversarial |
| brainstorming | superpowers | Socratic ideation |
| writing-plans | superpowers | Planos TDD |
| subagent-driven-dev | superpowers | Execução delegada |
| verification | superpowers | Verificação antes de completar |
| executing-plans | superpowers | Execução de planos |
| requesting-code-review | superpowers | Solicitar review |
| receiving-code-review | superpowers | Receber review |

### 3. GSD Legacy (35)

| Subagent | Função |
|----------|--------|
| gsd-planner | Criar planos |
| gsd-executor | Executar planos |
| gsd-code-reviewer | Revisar código |
| gsd-debugger | Debugar |
| gsd-verifier | Verificar |
| gsd-doc-writer | Documentar |
| ... | (30 mais) |

### 4. OpenCode/ECC (3)

| Subagent | Função |
|----------|--------|
| memory-keeper | Memória persistente |
| reverser | Engenharia reversa |
| general | Uso geral |

### 5. External (absorção futura)

| Subagent | Origem | Função |
|----------|--------|--------|
| agent-evaluator | ECC | Avaliação 5 eixos |
| build-error-resolver | ECC | Fix build errors |
| contextscout | OpenAgentsControl | Descoberta de contexto |
| hookify | ECC | Auto-gerar hooks |

## Regras de Orquestração

### Regra 1: Gran-Mestre Nunca Executa Direto

```
Usuário → Gran-Mestre → [classifica] → [delega para subagent] → [coleta resultado]
```

O Gran-Mestre NUNCA faz:
- Write/Edit de código de produção
- Bash execution direta
- Debugging manual
- Research manual

O Gran-Mestre SEMPRE:
- Classifica a tarefa
- Roteia para o subagent correto
- Coleta e sintetiza resultados
- Reporta ao usuário

### Regra 2: Subagents São Descartáveis

Cada subagent:
- Tem contexto isolado
- Pode ser destruído e recriado
- Não mantém estado entre invocações
- Herda apenas o que o Gran-Mestre passar

### Regra 3: Hierarquia de Roteamento

```
1. Rota exata (subagent nomeado) → encaminha direto
2. Rota por tipo (skill declarada) → Héstia valida
3. Rota por classificação → Prometheus analisa
4. Fallback → pergunta ao usuário
5. Rejeição → "não sei fazer isso"
```

### Regra 4: Safety Protocol Sempre Ativo

```
Antes de qualquer execução:
1. SHA salvo
2. Héstia valida plano
3. Atena revisa diff
4. Fable Judge verifica
5. Rollback se falhar
```

## Modelo de Invocação

```
/gran-mestre <tarefa>
  │
  ├─ fable-method Step 0: classificar
  │   ├─ trivial → micro-loop
  │   ├─ pergunta → responder
  │   ├─ task → Pipeline Padrão
  │   └─ escopo aberto → Pipeline Cascata
  │
  ├─ Pipeline:
  │   ├─ Fase 1: Explore + Librarian + Brainstorming
  │   ├─ Fase 2: Spec Writer + Héstia
  │   ├─ Fase 3: Prometheus + Metis + Fable Loop
  │   ├─ Fase 4: Sisyphus + Hephaestus + Code Reviewer
  │   ├─ Fase 5: Oracle + Fable Judge
  │   └─ Fase 6: Verification + Héstia + Fable Judge
  │
  └─ Output: relatório + backup
```

## Contagem Total

| Categoria | Quantidade |
|-----------|-----------|
| Agent primário | 1 (gran-mestre) |
| Pipeline subagents | 6 |
| Crossover subagents | 16 |
| GSD subagents | 35 |
| OpenCode subagents | 3 |
| **Total** | **61 subagents** |

---

**Versão:** 1.0.0
**Data:** 2026-07-27
**Decisão:** Gran-Mestre = único agent primário
**Subagents:** 61 disponíveis para orquestração
