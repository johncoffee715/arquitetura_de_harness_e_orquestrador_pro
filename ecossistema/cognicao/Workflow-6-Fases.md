# Workflow 6 Fases — Gran-Mestre Crossover

## Conceito
O workflow completo do Gran-Mestre combina os melhores elementos de:
- **Oh-My-Openagents**: Paralelismo (Team Mode), hash-anchored edits, skill-embedded MCPs
- **Superpowers**: TDD enforcement, brainstorming, writing-plans
- **Fable Method**: 7-step loop, fable-judge, domain adapters

## Fluxo Completo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    GRAN-MESTRE WORKFLOW 6 FASES                             │
│                    (Crossover: OmO + Superpowers + Fable)                   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    FASE 1 — DESCOBERTA                              │   │
│  │                                                                     │   │
│  │  Usuário → Gran-Mestre                                              │   │
│  │      ↓                                                              │   │
│  │  Prometheus: decomposição leve (contexto, não camisa-de-força)      │   │
│  │      ↓                                                              │   │
│  │  Fable Method: classifica o pedido (filtro 1)                       │   │
│  │      ↓                                                              │   │
│  │  Brainstorming (Superpowers): dialoga livremente, propõe 2-3       │   │
│  │  abordagens (filtro 2)                                              │   │
│  │      ↓                                                              │   │
│  │  ⏸️ GATE 1: usuário aprova a direção                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    FASE 2 — CONTRATO                                │   │
│  │                                                                     │   │
│  │  Spec Writer: transforma direção aprovada em design doc             │   │
│  │      ↓                                                              │   │
│  │  Héstia: valida spec contra o pedido original (filtro 1)            │   │
│  │      ↓                                                              │   │
│  │  fable-judge: audita o resultado pronto (filtro 2)                  │   │
│  │      ↓                                                              │   │
│  │  ⏸️ GATE 2: usuário aprova o spec                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    FASE 3 — PLANO                                   │   │
│  │                                                                     │   │
│  │  Plan Writer: TDD, tasks bite-sized, código completo                │   │
│  │      ↓                                                              │   │
│  │  Fable Loop: orquestra decomposição em sub-tasks e sub-agentes      │   │
│  │  (filtro 1)                                                         │   │
│  │      ↓                                                              │   │
│  │  Héstia: valida cobertura, contratos, verificabilidade (filtro 2)   │   │
│  │      ↓                                                              │   │
│  │  ⏸️ GATE 3: usuário aprova o plano                                  │   │
│  │  💾 Safety: SHA salvo AQUI (fases 1-3 não tocam código produtivo)   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    FASE 4 — EXECUÇÃO                                │   │
│  │                                                                     │   │
│  │  Atlas (supervisor): sequencia tasks, gerencia git (commits         │   │
│  │  atômicos, estado da branch), reporta progresso ao Gran-Mestre      │   │
│  │      ↓                                                              │   │
│  │  Fable Loop: orquestra subagentes frescos por task, gerencia        │   │
│  │  ciclo de vida de cada subagent (filtro 1.5 — operacional)          │   │
│  │      ↓                                                              │   │
│  │  Implementer (operário): loop TDD por task em subagent fresco,      │   │
│  │  evidência de verificação por task (filtro 2)                       │   │
│  │      ↓                                                              │   │
│  │  Code Reviewer: revisão micro por task (filtro 3)                   │   │
│  │      ↓                                                              │   │
│  │  ⚡ sem gates — commits atômicos, progresso visível                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    FASE 5 — REVISÃO MACRO                          │   │
│  │                                                                     │   │
│  │  Atena: revisão holística do diff total — coerência cross-task,     │   │
│  │  acoplamento (filtro 1 macro)                                       │   │
│  │      ↓                                                              │   │
│  │  fable-judge: audita o resultado pronto contra critérios de         │   │
│  │  qualidade, arquitetura e alinhamento com o contrato (filtro 2)     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    FASE 6 — ENTREGA                                 │   │
│  │                                                                     │   │
│  │  Verification: evidência fresca de ferro (filtro 2)                 │   │
│  │      ↓                                                              │   │
│  │  Héstia: validação final contra o pedido original (filtro 1)        │   │
│  │      ↓                                                              │   │
│  │  fable-judge: audita evidência de ferro, emite veredito final       │   │
│  │  de conformidade e qualidade (filtro 3 — o último)                  │   │
│  │      ↓                                                              │   │
│  │  ⏸️ GATE 4: relatório do Gran-Mestre → cerebral memory              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Detalhamento de Cada Fase

### FASE 1 — DESCOBERTA

**Objetivo**: Entender o que o usuário quer e explorar abordagens.

**Agentes Envolvidos**:
| Agente | Função | Framework |
|--------|--------|-----------|
| **Prometheus** | Decomposição leve | Gran-Mestre |
| **Fable Method** | Classificação do pedido | Fable |
| **Brainstorming** | Exploração de abordagens | Superpowers |

**Fluxo**:
1. Usuário descreve o que quer
2. Prometheus decompõe em contexto (não camisa-de-força)
3. Fable Method classifica: question? task? plan-first?
4. Brainstorming propõe 2-3 abordagens
5. Usuário aprova direção → GATE 1

**Saída**: Direção aprovada pelo usuário

---

### FASE 2 — CONTRATO

**Objetivo**: Transformar direção aprovada em spec verificável.

**Agentes Envolvidos**:
| Agente | Função | Framework |
|--------|--------|-----------|
| **Spec Writer** | Cria design doc | Gran-Mestre |
| **Héstia** | Valida spec contra pedido | Gran-Mestre |
| **fable-judge** | Audita resultado | Fable |

**Fluxo**:
1. Spec Writer transforma direção em design doc
2. Héstia valida spec contra pedido original
3. fable-judge audita resultado pronto
4. Usuário aprova spec → GATE 2

**Saída**: SPEC.md aprovado

---

### FASE 3 — PLANO

**Objetivo**: Criar plano executável com TDD e tasks bite-sized.

**Agentes Envolvidos**:
| Agente | Função | Framework |
|--------|--------|-----------|
| **Plan Writer** | Cria plano com TDD | Superpowers |
| **Fable Loop** | Orquestra decomposição | Fable |
| **Héstia** | Valida cobertura | Gran-Mestre |

**Fluxo**:
1. Plan Writer cria plano com TDD, tasks bite-sized
2. Fable Loop orquestra decomposição em sub-tasks
3. Héstia valida cobertura, contratos, verificabilidade
4. Usuário aprova plano → GATE 3
5. 💾 Safety: SHA salvo aqui

**Saída**: PLAN.md aprovado + SHA de segurança

---

### FASE 4 — EXECUÇÃO

**Objetivo**: Executar plano com paralelismo e TDD.

**Agentes Envolvidos**:
| Agente | Função | Framework |
|--------|--------|-----------|
| **Atlas** | Supervisor de execução | Gran-Mestre |
| **Fable Loop** | Orquestra subagentes | Fable |
| **Implementer** | Loop TDD por task | Superpowers |
| **Code Reviewer** | Revisão micro por task | Gran-Mestre |

**Fluxo**:
1. Atlas sequencia tasks, gerencia git
2. Fable Loop orquestra subagentes frescos por task
3. Implementer executa loop TDD por task
4. Code Reviewer revisa micro por task
5. ⚡ Sem gates — commits atômicos

**Saída**: Código implementado + commits atômicos

**Nota**: O Atlas já é, na prática, um Fable Loop manual. O Fable Loop aqui não substitui o Atlas — ele o potencializa.

---

### FASE 5 — REVISÃO MACRO

**Objetivo**: Revisão holística do diff total.

**Agentes Envolvidos**:
| Agente | Função | Framework |
|--------|--------|-----------|
| **Atena** | Revisão holística | Gran-Mestre |
| **fable-judge** | Audita resultado | Fable |

**Fluxo**:
1. Atena revisa diff total — coerência cross-task, acoplamento
2. fable-judge audita contra critérios de qualidade e arquitetura

**Saída**: Revisão macro aprovada

---

### FASE 6 — ENTREGA

**Objetivo**: Validar entrega final com evidência de ferro.

**Agentes Envolvidos**:
| Agente | Função | Framework |
|--------|--------|-----------|
| **Verification** | Evidência fresca | Gran-Mestre |
| **Héstia** | Validação final | Gran-Mestre |
| **fable-judge** | Veredito final | Fable |

**Fluxo**:
1. Verification coleta evidência fresca de ferro
2. Héstia valida contra pedido original
3. fable-judge audita evidência e emite veredito final
4. ⏸️ GATE 4: relatório → cerebral memory

**Saída**: Relatório final + memória atualizada

---

## Comparação: Original vs Crossover

| Aspecto | Original (Gran-Mestre) | Crossover (OmO + Superpowers + Fable) |
|---------|------------------------|---------------------------------------|
| **Paralelismo** | Sequencial | Team Mode (8 agentes paralelos) |
| **Edits** | String-based | Hash-anchored (LINE#ID) |
| **TDD** | Opcional | Obrigatório (RED-GREEN-REFACTOR) |
| **Verificação** | Confiança | fable-judge (adversarial) |
| **Brainstorming** | Explícito | Integrado (Superpowers) |
| **Domain Adapters** | Não | Sim (Fable) |
| **IntentGate** | Não | Sim (OmO) |
| **Skill-embedded MCPs** | Não | Sim (OmO) |

## Tags
#workflow #6-fases #gran-mestre #crossover #oh-my-openagents #superpowers #fable-method
