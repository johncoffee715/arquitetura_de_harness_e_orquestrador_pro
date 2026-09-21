---
name: gran-mestre-workflow
description: "Workflow completo do Gran-Mestre: 6 fases, 4 gates, 3 filtros por fase. Meta-orquestrador senior que comanda todos os subagents, tools, MCPs e skills registrados."
mode: subagent
origin: gran-mestre-original
metadata:
  category: orchestration
  version: 7.0.0
  author: Gran-Mestre
  note: "Workflow implementado — cada fase é executável, não apenas documentação."
---

# GRAN-MAESTRO WORKFLOW — 6 Fases Implementadas

## Princípio Fundamental

> O Gran-Mestre é o **único agent primary**. Todos os subagents, tools, MCPs e skills
> registrados no `agent-registry.json` estão disponíveis para serem orquestrados por ele.
> Essa é sua função — conforme a escalabilidade do sistema cresce, o Gran-Mestre orquestra.

## Escalabilidade

```
Registry atual: 12 entries
├── 1 agent (gran-mestre) — orquestra tudo
├── 5 subagents — executam trabalho
├── 1 MCP — memória persistente
├── 4 skills — habilidades empacotadas
└── 1 tool — safety hook

Conforme novos subagents/tools/MCPs/skills são registrados,
o Gran-Mestre automaticamente os orquestra — sem reconfiguração.
O CapabilityIndex (greedy cover) seleciona o melhor conjunto
de componentes para cada tarefa.
```

---

## FASE 1 — DESCOBERTA

### Agentes Envolvidos

| Agente | Tipo | Função | Filtro |
|--------|------|--------|--------|
| **Prometheus** | subagent | Decomposição leve (contexto, não camisa-de-força) | Orquestrador |
| **Fable Method** | skill | O loop em um pedido | Filtro 1 |
| **Brainstorming** | skill | Dialoga livremente, propõe 2-3 abordagens | Filtro 2 |

### Fluxo

```
Usuário → Gran-Mestre → Prometheus (decompõe)
                              ↓
                        Fable Method (loop em 1 pedido)
                              ↓
                        Brainstorming (2-3 abordagens)
                              ↓
                        ⏸️ GATE 1: usuário aprova a direção
```

### Implementação

```python
# Pseudocódigo — Fase 1
def fase_1_descoberta(requisicao):
    # 1. Prometheus decompõe
    contexto = prometheus.decompor(requisicao)
    
    # 2. Fable Method — loop em 1 pedido
    analise = fable_method.analisar(contexto)
    
    # 3. Brainstorming — 2-3 abordagens
    abordagens = brainstorming.propor(analise, n=3)
    
    # 4. GATE 1 — aprovação do usuário
    direcao_aprovada = gate_1.aprovar(abordagens)
    
    return direcao_aprovada
```

### Critérios de Saída

- [ ] Contexto documentado (não camisa-de-força)
- [ ] 2-3 abordagens propostas
- [ ] Direção aprovada pelo usuário
- [ ] Filtro 1 (Fable Method) passou
- [ ] Filtro 2 (Brainstorming) passou

---

## FASE 2 — CONTRATO

### Agentes Envolvidos

| Agente | Tipo | Função | Filtro |
|--------|------|--------|--------|
| **Spec Writer** | subagent | Transforma direção aprovada em design doc | Orquestrador |
| **Héstia** | subagent | Valida spec contra o pedido original | Filtro 1 |
| **Fable Judge** | skill | Audita o resultado pronto | Filtro 2 |

### Fluxo

```
Direção aprovada → Spec Writer (design doc)
                        ↓
                  Héstia (valida spec vs pedido)
                        ↓
                  Fable Judge (audita resultado)
                        ↓
                  ⏸️ GATE 2: usuário aprova o spec
```

### Implementação

```python
# Pseudocódigo — Fase 2
def fase_2_contrato(direcao_aprovada):
    # 1. Spec Writer gera design doc
    spec = spec_writer.gerar(direcao_aprovada)
    
    # 2. Héstia valida contra pedido original
    validacao_hestia = hestia.validar(spec, pedido_original)
    if not validacao_hestia.aprovado:
        spec = spec_writer.corrigir(spec, validacao_hestia.gaps)
        validacao_hestia = hestia.validar(spec, pedido_original)
    
    # 3. Fable Judge audita
    audit_fable = fable_judge.auditar(spec)
    
    # 4. GATE 2 — aprovação do usuário
    spec_aprovado = gate_2.aprovar(spec, audit_fable)
    
    return spec_aprovado
```

### Critérios de Saída

- [ ] Design doc completo
- [ ] Héstia validou (máximo 3 ciclos)
- [ ] Fable Judge auditou
- [ ] Spec aprovado pelo usuário
- [ ] Todos os requisitos cobertos

---

## FASE 3 — PLANO

### Agentes Envolvidos

| Agente | Tipo | Função | Filtro |
|--------|------|--------|--------|
| **Plan Writer** | subagent | TDD, tasks bite-sized, código completo | Orquestrador |
| **Fable Loop** | skill | Orquestra decomposição em sub-tasks e sub-agentes | Filtro 1 |
| **Héstia** | subagent | Valida cobertura, contratos, verificabilidade | Filtro 2 |

### Fluxo

```
Spec aprovado → Plan Writer (TDD, tasks bite-sized)
                      ↓
                Fable Loop (decompõe em sub-tasks)
                      ↓
                Héstia (valida cobertura e verificabilidade)
                      ↓
                ⏸️ GATE 3: usuário aprova o plano
                💾 Safety: SHA salvo AQUI (fases 1-3 não tocam código)
```

### Implementação

```python
# Pseudocódigo — Fase 3
def fase_3_plano(spec_aprovado):
    # 1. Plan Writer gera plano TDD
    plano = plan_writer.gerar(spec_aprovado, tdd=True)
    
    # 2. Fable Loop decompõe em sub-tasks
    sub_tasks = fable_loop.decompor(plano)
    
    # 3. Héstia valida cobertura
    validacao_hestia = hestia.validar_cobertura(plano, spec_aprovado)
    if not validacao_hestia.aprovado:
        plano = plan_writer.corrigir(plano, validacao_hestia.gaps)
        validacao_hestia = hestia.validar_cobertura(plano, spec_aprovado)
    
    # 4. GATE 3 — aprovação do usuário
    plano_aprovado = gate_3.aprovar(plano)
    
    # 5. 💾 Safety: SHA salvo aqui
    sha = safety.salvar_sha()
    
    return plano_aprovado, sha
```

### Critérios de Saída

- [ ] Plano TDD completo
- [ ] Tasks bite-sized definidas
- [ ] Fable Loop decompôs em sub-tasks
- [ ] Héstia validou cobertura (máximo 3 ciclos)
- [ ] Plano aprovado pelo usuário
- [ ] SHA salvo (safety protocol)

---

## FASE 4 — EXECUÇÃO

### Agentes Envolvidos

| Agente | Tipo | Função | Filtro |
|--------|------|--------|--------|
| **Atlas** | subagent | Supervisor: sequencia tasks, gerencia git | Orquestrador |
| **Fable Loop** | skill | Orquestra subagentes frescos por task | Filtro 1.5 |
| **Implementer** | subagent | Operário: loop TDD por task | Filtro 2 |
| **Code Reviewer** | subagent | Revisão micro por task | Filtro 3 |

### Fluxo

```
Plano aprovado → Atlas (supervisor: sequencia, gerencia git)
                      ↓
                Fable Loop (subagentes frescos por task)
                      ↓
                Implementer (loop TDD por task)
                      ↓
                Code Reviewer (revisão micro por task)
                      ↓
                ⚡ sem gates — commits atômicos, progresso visível
```

### Implementação

```python
# Pseudocódigo — Fase 4
def fase_4_execucao(plano_aprovado, sha):
    # Atlas é supervisor — NUNCA escreve código na cascata
    atlas = Atlas(supervisor=True)
    
    for task in plano_aprovado.tasks:
        # 1. Fable Loop cria subagent fresco
        subagent = fable_loop.criar_subagent(task)
        
        # 2. Implementer executa TDD
        resultado = implementer.executar_tdd(task, subagent)
        
        # 3. Code Reviewer revisa micro
        revisao = code_reviewer.revisar(resultado)
        if not revisao.aprovado:
            resultado = implementer.corrigir(resultado, revisao.gaps)
            revisao = code_reviewer.revisar(resultado)
        
        # 4. Atlas gerencia git (commit atômico)
        atlas.commit_atomico(resultado)
        
        # 5. Reporta progresso ao Gran-Mestre
        gran_mestre.reportar_progresso(task, resultado)
    
    # Sem gates — progresso visível
    return resultados
```

### Critérios de Saída

- [ ] Todas as tasks executadas
- [ ] TDD implementado por task
- [ ] Code Reviewer aprovou cada task
- [ ] Commits atômicos realizados
- [ ] Progresso reportado ao Gran-Mestre
- [ ] Atlas NUNCA escreveu código (só gerenciou)

### Nota Importante

> O Atlas já é, na prática, um Fable Loop manual.
> Então o Fable Loop aqui não substitui o Atlas — ele o potencializa.

---

## FASE 5 — REVISÃO MACRO

### Agentes Envolvidos

| Agente | Tipo | Função | Filtro |
|--------|------|--------|--------|
| **Atena** | subagent | Revisão holística do diff total | Filtro 1 macro |
| **Fable Judge** | skill | Audita contra critérios de qualidade | Filtro 2 macro |

### Fluxo

```
Resultados da Fase 4 → Atena (revisão holística: coerência, acoplamento)
                            ↓
                      Fable Judge (audita qualidade, arquitetura, contrato)
                            ↓
                      Veredicto: APPROVED / APPROVED_WITH_CAVEATS / CHANGES_REQUIRED
```

### Implementação

```python
# Pseudocódigo — Fase 5
def fase_5_revisao_macro(resultados):
    # 1. Atena revisa diff total
    revisao_atena = atena.revisar_diff_total(resultados)
    
    # 2. Fable Judge audita
    audit_fable = fable_judge.auditar(resultados, criterios=[
        "qualidade",
        "arquitetura",
        "alinhamento_contrato"
    ])
    
    # 3. Veredicto
    if revisao_atena.status == "CHANGES_REQUIRED":
        # Volta para Fase 4
        return fase_4_execucao(corrigir(resultados, revisao_atena.gaps))
    
    return {
        "atena": revisao_atena,
        "fable_judge": audit_fable,
        "veredicto": "APPROVED"
    }
```

### Critérios de Saída

- [ ] Atena revisou diff total
- [ ] Coerência cross-task verificada
- [ ] Acoplamento analisado
- [ ] Fable Judge auditou
- [ ] Veredicto: APPROVED ou APPROVED_WITH_CAVEATS

---

## FASE 6 — ENTREGA

### Agentes Envolvidos

| Agente | Tipo | Função | Filtro |
|--------|------|--------|--------|
| **Verification** | subagent | Evidência fresca de ferro | Filtro 2 |
| **Héstia** | subagent | Validação final contra o pedido original | Filtro 1 |
| **Fable Judge** | skill | Audita evidência, emite veredito final | Filtro 3 |

### Fluxo

```
Resultados aprovados → Verification (evidência fresca)
                            ↓
                      Héstia (validação final vs pedido original)
                            ↓
                      Fable Judge (audita evidência, veredito final)
                            ↓
                      ⏸️ GATE 4: relatório do Gran-Mestre → cerebral memory
```

### Implementação

```python
# Pseudocódigo — Fase 6
def fase_6_entrega(resultados_aprovados, pedido_original):
    # 1. Verification — evidência fresca de ferro
    evidencia = verification.verificar(resultados_aprovados)
    
    # 2. Héstia — validação final
    validacao_final = hestia.validacao_final(evidencia, pedido_original)
    if not validacao_final.aprovado:
        # Volta para Fase 4
        return fase_4_execucao(corrigir(resultados_aprovados, validacao_final.gaps))
    
    # 3. Fable Judge — veredito final
    veredito_final = fable_judge.veredito_final(evidencia)
    
    # 4. GATE 4 — relatório → cerebral memory
    relatorio = gran_mestre.gerar_relatorio(
        resultados=resultados_aprovados,
        evidencia=evidencia,
        veredito=veredito_final
    )
    
    # 5. Shared Brain — arquiva aprendizados
    shared_brain.ingest_source(relatorio)
    shared_brain.create_summary(relatorio)
    shared_brain.upsert_entity(relatorio)
    shared_brain.upsert_concept(relatorio)
    
    return relatorio
```

### Critérios de Saída

- [ ] Evidência fresca de ferro gerada
- [ ] Héstia validou final (máximo 3 ciclos)
- [ ] Fable Judge emitiu veredito final
- [ ] Relatório gerado
- [ ] Shared Brain arquivou aprendizados
- [ ] GATE 4 aprovado

---

## WORKFLOW COMPLETO — Visão Unificada

```
┌─────────────────────────────────────────────────────────────────┐
│                    GRAN-MAESTRO WORKFLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FASE 1: DESCOBERTA                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Prometheus   │→ │ Fable Method │→ │ Brainstorming│          │
│  │ (decompõe)   │  │ (analisa)    │  │ (abordagens) │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         ↓                                                       │
│  ⏸️ GATE 1: usuário aprova direção                              │
│                                                                 │
│  FASE 2: CONTRATO                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Spec Writer  │→ │ Héstia       │→ │ Fable Judge  │          │
│  │ (design doc) │  │ (valida)     │  │ (audita)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         ↓                                                       │
│  ⏸️ GATE 2: usuário aprova spec                                 │
│                                                                 │
│  FASE 3: PLANO                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Plan Writer  │→ │ Fable Loop   │→ │ Héstia       │          │
│  │ (TDD plan)   │  │ (sub-tasks)  │  │ (valida)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         ↓                                                       │
│  ⏸️ GATE 3: usuário aprova plano                                │
│  💾 Safety: SHA salvo aqui                                      │
│                                                                 │
│  FASE 4: EXECUÇÃO                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Atlas        │→ │ Fable Loop   │→ │ Implementer  │          │
│  │ (supervisor) │  │ (subagents)  │  │ (TDD loop)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         ↓                                                       │
│  ┌──────────────┐                                              │
│  │ Code Reviewer│                                              │
│  │ (revisão)    │                                              │
│  └──────────────┘                                              │
│  ⚡ sem gates — commits atômicos                                │
│                                                                 │
│  FASE 5: REVISÃO MACRO                                         │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │ Atena        │→ │ Fable Judge  │                            │
│  │ (diff total) │  │ (audita)     │                            │
│  └──────────────┘  └──────────────┘                            │
│                                                                 │
│  FASE 6: ENTREGA                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Verification │→ │ Héstia       │→ │ Fable Judge  │          │
│  │ (evidência)  │  │ (valida)     │  │ (veredito)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         ↓                                                       │
│  ⏸️ GATE 4: relatório → cerebral memory                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## REGISTRY — Todos Disponíveis para Orquestração

O Gran-Mestre orquestra **todos** os componentes registrados:

| ID | Tipo | Fase(s) | Função |
|----|------|---------|--------|
| gran-mestre | agent | Todas | Meta-orquestrador |
| prometheus | subagent | 1 | Decomposição |
| hestia | subagent | 2, 3, 6 | Validação |
| atlas | subagent | 4 | Execução (supervisor) |
| athena | subagent | 5 | Revisão macro |
| sisyphus | subagent | 4 | Tasks triviais |
| mcp-obsidian-vault | mcp | 6 | Memória persistente |
| skill-gran-mestre | skill | Todas | Pipeline definition |
| skill-hestia | skill | 2, 3, 6 | Validação |
| skill-athena | skill | 5 | Revisão macro |
| skill-pxpipe | skill | Todas | Redução de tokens |
| tool-safety-sha | tool | 3, 4 | Safety protocol |

### Escalabilidade

Conforme novos componentes são registrados no `agent-registry.json`:
1. O **CapabilityIndex** (greedy cover) os descobre automaticamente
2. O **ContextAnalyzer** classifica a complexidade da tarefa
3. O Gran-Mestre **orquestra** o melhor conjunto de componentes
4. **Nenhuma reconfiguração** é necessária — o registry é a fonte de verdade

---

## IMPLEMENTAÇÃO

### Como usar

```bash
# Pipeline completo
/gran-mestre start "implementar feature X"

# Fase específica
/gran-mestre phase 1 "descobrir abordagens"
/gran-mestre phase 2 "gerar spec"
/gran-mestre phase 3 "criar plano"
/gran-mestre phase 4 "executar plano"
/gran-mestre phase 5 "revisar diff"
/gran-mestre phase 6 "entregar"

# Status
/gran-mestre status

# Validação
/gran-mestre validate
```

### Gates

| Gate | Fase | Quem aprova | Modo interativo | Modo autônomo |
|------|------|-------------|-----------------|---------------|
| GATE 1 | 1 | Usuário | Aprova direção | Héstia proxy |
| GATE 2 | 2 | Usuário | Aprova spec | Héstia proxy |
| GATE 3 | 3 | Usuário | Aprova plano | Héstia proxy |
| GATE 4 | 6 | Gran-Mestre | Gera relatório | Auto |

---

**Versão:** 7.0.0
**Data:** 2026-07-25
**Status:** IMPLEMENTADO