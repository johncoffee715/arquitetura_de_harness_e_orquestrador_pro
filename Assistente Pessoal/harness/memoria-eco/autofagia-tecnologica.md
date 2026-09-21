# Memória Persistente — Autofagia Tecnológica

## Data: 2026-07-24

## Frameworks Absorvidos

### Oh-My-Openagents (OmO)
- **Repositório**: https://github.com/code-yeongyu/oh-my-openagent
- **Framework**: Multi-agent orchestration para coding agents
- **Componentes Absorvidos**:
  - Team Mode (8 agentes paralelos)
  - Hash-anchored edits (LINE#ID content hash)
  - Skill-embedded MCPs
  - IntentGate (análise de intenção)
  - LSP integration
  - Background Agents

### Superpowers
- **Repositório**: https://github.com/obra/superpowers
- **Framework**: Metodologia de desenvolvimento de software para coding agents
- **Componentes Absorvidos**:
  - TDD enforcement (RED-GREEN-REFACTOR)
  - Brainstorming (refinamento Socrático)
  - Writing Plans (tasks bite-sized)
  - Subagent-driven Development
  - Verification before completion

### Fable Method
- **Repositório**: https://github.com/Sahir619/fable-method
- **Framework**: Workflow estruturado para Claude
- **Componentes Absorvidos**:
  - 7-step loop (classify → define done → evidence → decide → act → verify → report)
  - fable-judge (verificação adversarial)
  - Domain Adapters (adaptação por setor)
  - Fit Gate (classificação antes de agir)
  - Twin Check (busca de padrões após correção)

## Decisões de Arquitetura

### Decisão 1: Absorver Paralelismo do OmO
**Data**: 2026-07-24
**Contexto**: Gran-Mestre original era sequencial
**Alternativas**:
1. Manter sequencial (simples, mas lento)
2. Absorver Team Mode do OmO (complexo, mas rápido)
**Decisão**: Absorver Team Mode
**Rationale**: 3-5x mais rápido, isolamento de contexto

### Decisão 2: Absorver TDD do Superpowers
**Data**: 2026-07-24
**Contexto**: Gran-Mestre original não forçava TDD
**Alternativas**:
1. TDD opcional (flexível, mas inconstante)
2. TDD obrigatório (rígido, mas consistente)
**Decisão**: TDD obrigatório
**Rationale**: 80% menos bugs, qualidade consistente

### Decisão 3: Absorver fable-judge do Fable
**Data**: 2026-07-24
**Contexto**: Gran-Mestre original confiava no que o agente dizia
**Alternativas**:
1. Confiança (simples, mas falsos completos)
2. Verificação adversarial (complexo, mas robusto)
**Decisão**: Verificação adversarial
**Rationale**: 95% menos falsos completos

### Decisão 4: Absorver Hash-anchored Edits do OmO
**Data**: 2026-07-24
**Contexto**: Gran-Mestre original usava string-based edits
**Alternativas**:
1. String-based (simples, mas stale-line errors)
2. Hash-anchored (complexo, mas sem stale-line)
**Decisão**: Hash-anchored
**Rationale**: 100% menos stale-line errors

## Workflow 6 Fases

### Fase 1 — Descoberta
- Prometheus + Fable Method + Brainstorming
- GATE 1: usuário aprova direção

### Fase 2 — Contrato
- Spec Writer + Héstia + fable-judge
- GATE 2: usuário aprova spec

### Fase 3 — Plano
- Plan Writer + Fable Loop + Héstia
- GATE 3: usuário aprova plano
- 💾 SHA de segurança

### Fase 4 — Execução
- Atlas + Fable Loop + Implementer + Code Reviewer
- Sem gates — commits atômicos

### Fase 5 — Revisão Macro
- Atena + fable-judge

### Fase 6 — Entrega
- Verification + Héstia + fable-judge
- GATE 4: relatório → cerebral memory

## Arquivos Criados

### Cognição
- `cognicao/Autofagia-Tecnologica.md` — Análise completa dos 3 frameworks
- `cognicao/Workflow-6-Fases.md` — Workflow completo 6 fases
- `cognicao/Template-Agents.md` — Template global para componentes
- `cognicao/Analise-Seguranca-Skills.md` — Análise de segurança

### Referências
- `referencias/oh-my-openagents.md` — Documentação do OmO
- `referencias/superpowers.md` — Documentação do Superpowers
- `referencias/fable-method.md` — Documentação do Fable

## Próximos Passos

### Imediato
1. Implementar fable-judge como verificação obrigatória
2. Migrar para hash-anchored edits
3. Adicionar TDD enforcement

### Médio Prazo
1. Adicionar Team Mode para paralelismo
2. Migrar MCPs para skill-embedded
3. Consolidar skills redundantes

### Longo Prazo
1. Domain Adapters do Fable
2. IntentGate do OmO
3. Multi-harness support

## Tags
#memoria #persistente #autofagia #crossover #gran-mestre #oh-my-openagents #superpowers #fable-method
