# Gran-Mestre Integration Layer

## Visão Geral

Camada de integração que combina Oh-My-Openagents, Superpowers, e Fable Method em um pipeline unificado.

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    GRAN-MAESTRO PIPELINE                     │
├─────────────────────────────────────────────────────────────┤
│  FASE 1: DESCOBERTA                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Prometheus   │→ │ Fable Loop   │→ │ Brainstorming│      │
│  │ (OmO)        │  │ (Fable)      │  │ (Superpowers)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                                                   │
│  ⏸️ GATE 1: Usuário aprova direção                          │
├─────────────────────────────────────────────────────────────┤
│  FASE 2: CONTRATO                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Spec Writer  │→ │ Héstia       │→ │ Fable Judge  │      │
│  │ (Superpowers)│  │ (Gran-Mestre)│  │ (Fable)      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                                                   │
│  ⏸️ GATE 2: Usuário aprova spec                             │
├─────────────────────────────────────────────────────────────┤
│  FASE 3: PLANO                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Plan Writer  │→ │ Fable Loop   │→ │ Héstia       │      │
│  │ (Superpowers)│  │ (Fable)      │  │ (Gran-Mestre)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                                                   │
│  ⏸️ GATE 3: Usuário aprova plano                            │
│  💾 Safety: SHA salvo aqui                                  │
├─────────────────────────────────────────────────────────────┤
│  FASE 4: EXECUÇÃO                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Atlas        │→ │ Fable Loop   │→ │ Implementer  │      │
│  │ (OmO)        │  │ (Fable)      │  │ (Superpowers)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                                                   │
│  ┌──────────────┐                                          │
│  │ Code Reviewer│                                          │
│  │ (Superpowers)│                                          │
│  └──────────────┘                                          │
│  ⚡ Sem gates - commits atômicos                            │
├─────────────────────────────────────────────────────────────┤
│  FASE 5: REVISÃO MACRO                                      │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ Atena        │→ │ Fable Judge  │                        │
│  │ (Gran-Mestre)│  │ (Fable)      │                        │
│  └──────────────┘  └──────────────┘                        │
├─────────────────────────────────────────────────────────────┤
│  FASE 6: ENTREGA                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Verification │→ │ Héstia       │→ │ Fable Judge  │      │
│  │ (Fable)      │  │ (Gran-Mestre)│  │ (Fable)      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                                                   │
│  ⏸️ GATE 4: Relatório → cerebral memory                     │
└─────────────────────────────────────────────────────────────┘
```

## Agent Mapping

| Fase | Agent | Framework | Função |
|------|-------|-----------|--------|
| 1 | Prometheus | OmO | Decomposição leve |
| 1 | Fable Loop | Fable | Orquestração |
| 1 | Brainstorming | Superpowers | Proposta de abordagens |
| 2 | Spec Writer | Superpowers | Transforma direção em spec |
| 2 | Héstia | Gran-Mestre | Valida spec contra pedido |
| 2 | Fable Judge | Fable | Audita resultado |
| 3 | Plan Writer | Superpowers | Cria plano TDD |
| 3 | Fable Loop | Fable | Decomposição em sub-tasks |
| 3 | Héstia | Gran-Mestre | Valida cobertura |
| 4 | Atlas | OmO | Sequencia tasks |
| 4 | Fable Loop | Fable | Orquestra subagentes |
| 4 | Implementer | Superpowers | Loop TDD |
| 4 | Code Reviewer | Superpowers | Revisão micro |
| 5 | Atena | Gran-Mestre | Revisão holística |
| 5 | Fable Judge | Fable | Audita contra contrato |
| 6 | Verification | Fable | Evidência fresca |
| 6 | Héstia | Gran-Mestre | Validação final |
| 6 | Fable Judge | Fable | Veredito final |

## Gate System

### Gate 1: Direction Approval
- **Quando**: Após Fase 1
- **Quem**: Usuário
- **O quê**: Aprova a direção proposta
- **Ação**: Se aprovado, avança para Fase 2

### Gate 2: Spec Approval
- **Quando**: Após Fase 2
- **Quem**: Usuário
- **O quê**: Aprova o spec
- **Ação**: Se aprovado, avança para Fase 3

### Gate 3: Plan Approval
- **Quando**: Após Fase 3
- **Quem**: Usuário
- **O quê**: Aprova o plano
- **Ação**: Se aprovado, salva SHA e avança para Fase 4

### Gate 4: Final Report
- **Quando**: Após Fase 6
- **Quem**: Gran-Mestre
- **O quê**: Gera relatório final
- **Ação**: Envia para cerebral memory

## Pipeline Selection

### Pipeline Padrão
- **Quando usar**: Requisitos claros, escopo definido
- **Características**: Linear, gates explícitos
- **Fluxo**: Fase 1 → 2 → 3 → 4 → 5 → 6

### Pipeline em Cascata
- **Quando usar**: Features novas com design em aberto
- **Características**: Iterativo, refinamento contínuo
- **Fluxo**: Fase 1 ↔ 2 ↔ 3 → 4 → 5 → 6

## Skill Routing

| Skill Category | Framework | Used In |
|----------------|-----------|---------|
| Brainstorming | Superpowers | Fase 1 |
| Writing Plans | Superpowers | Fase 3 |
| TDD | Superpowers | Fase 4 |
| Code Review | Superpowers | Fase 4 |
| Fable Method | Fable | Todas |
| Fable Loop | Fable | Fases 1,3,4 |
| Fable Judge | Fable | Fases 2,5,6 |
| Work With PR | OmO | Fase 4 |
| Security Research | OmO | Todas |

## MCP Coordination

| MCP | Framework | Purpose |
|-----|-----------|---------|
| context7 | Todos | Documentação atual |
| grep_app | OmO | Busca em código |
| codegraph | OmO | Análise de código |
| lsp | OmO | Language Server |
| git_bash | OmO | Operações git |

## Security Model

### Combined Security

1. **OmO Security**: QA obrigatório, evidências, worktrees isolados
2. **Superpowers Security**: 94% rejeição de PRs, review rigoroso
3. **Fable Security**: Verificação adversarial, gates de autorização

### Permission Model

| Agent | Permissions |
|-------|-------------|
| Prometheus | Read, Decompose |
| Atlas | Read, Write, Git |
| Héstia | Read, Validate |
| Atena | Read, Review |
| Fable Loop | Read, Orchestrate |
| Fable Judge | Read, Verify |

## Configuration

```json
{
  "gran-mestre": {
    "pipeline": "standard|cascade",
    "gates": {
      "gate1": "user-approval",
      "gate2": "user-approval",
      "gate3": "user-approval",
      "gate4": "auto-report"
    },
    "agents": {
      "prometheus": { "enabled": true },
      "atlas": { "enabled": true },
      "hestia": { "enabled": true },
      "athena": { "enabled": true }
    },
    "skills": {
      "superpowers": { "enabled": true },
      "fable": { "enabled": true },
      "omo": { "enabled": true }
    }
  }
}
```

## Usage

```
/gran-mestre start <task>        - Inicia pipeline completo
/gran-mestre start --cascade     - Inicia pipeline em cascata
/gran-mestre status              - Mostra status atual
/gran-mestre validate <phase>    - Valida fase específica
/gran-mestre report              - Gera relatório
```