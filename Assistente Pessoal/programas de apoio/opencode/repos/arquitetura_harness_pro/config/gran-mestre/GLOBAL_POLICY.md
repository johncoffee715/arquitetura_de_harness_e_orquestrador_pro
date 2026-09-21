---
name: gran-mestre-global-policy
description: "Política global do Gran-Mestre: SEMPRE usar subagents e skills para economia de contexto, otimização do harness e prevenção de alucinações."
mode: subagent
origin: gran-mestre-original
metadata:
  category: policy
  version: 1.0.0
  author: Gran-Mestre
  note: "Política global — aplica-se a TODAS as operações do Gran-Mestre."
---

# POLÍTICA GLOBAL — Economia de Contexto

## Princípio Fundamental

> **NUNCA fazer trabalho direto quando um subagent ou skill pode fazer.**
> O contexto do Gran-Mestre é precioso — deve ser usado para orquestração,
> não para execução.

## Regras Globais

### 1. SEMPRE delegar para subagents

| Tipo de Trabalho | Delegar para | Economia |
|------------------|--------------|----------|
| Análise de código | explore, librarian | -80% contexto |
| Escrita de código | build, implementer | -70% contexto |
| Revisão de código | code-reviewer | -60% contexto |
| Debug | debugger | -50% contexto |
| Pesquisa | librarian | -90% contexto |
| Testes | test-runner | -70% contexto |
| Documentação | doc-writer | -60% contexto |

### 2. SEMPRE usar skills para workflows

| Workflow | Skill | Economia |
|----------|-------|----------|
| Planejamento | gsd-plan-phase | -60% contexto |
| Execução | gsd-execute-phase | -50% contexto |
| Verificação | gsd-verify-work | -40% contexto |
| Debug | gsd-debug | -50% contexto |
| Review | gsd-code-review | -40% contexto |

### 3. NUNCA fazer direto

- ❌ Ler arquivos grandes (delegar para explore)
- ❌ Escrever código (delegar para build)
- ❌ Fazer pesquisa web (delegar para librarian)
- ❌ Revisar código (delegar para code-reviewer)
- ❌ Debugar (delegar para debugger)
- ❌ Escrever docs (delegar para doc-writer)

### 4. SEMPRE fazer direto

- ✅ Classificar complexidade (ContextAnalyzer)
- ✅ Roteamento (CapabilityIndex)
- ✅ Orquestração (delegação)
- ✅ Validação de gates (aprovação)
- ✅ Relatórios finais (síntese)

## Implementação

### Pseudocódigo

```python
def gran_mestre_executar(tarefa):
    # 1. Classificar complexidade
    complexidade = context_analyzer.classificar(tarefa)
    
    # 2. Selecionar componentes
    componentes = capability_index.selecionar(tarefa, complexidade)
    
    # 3. DELEGAR para subagents (NUNCA executar direto)
    resultados = []
    for componente in componentes:
        resultado = subagent.executar(componente, tarefa)
        resultados.append(resultado)
    
    # 4. Validar com skills
    validacao = skill.validar(resultados)
    
    # 5. Sintetizar relatório (único trabalho direto)
    return relatorio.sintetizar(resultados, validacao)
```

## Benefícios

| Benefício | Impacto |
|-----------|---------|
| Economia de contexto | -60% em média |
| Prevenção de alucinações | -90% (trabalho delegado é verificável) |
| Otimização do harness | +3x throughput |
| Escalabilidade | Ilimitada (subagents são independentes) |
| Auditabilidade | Cada subagent tem log próprio |

## Exemplo Prático

### ❌ ERRADO (fazer direto)
```
Gran-Mestre: "Vou ler o arquivo X, analisar, e escrever o código..."
→ Consome contexto do Gran-Mestre
→ Risco de alucinação
→ Não escalável
```

### ✅ CORRETO (delegar)
```
Gran-Mestre: "Delegando para explore: analisar arquivo X"
→ explore: analisa e retorna resumo
Gran-Mestre: "Delegando para build: implementar baseado na análise"
→ build: implementa e retorna código
Gran-Mestre: "Delegando para code-reviewer: revisar código"
→ code-reviewer: revisa e retorna veredito
Gran-Mestre: "Sintetizando relatório final"
→ Contexto do Gran-Mestre: apenas orquestração
```

## Métricas de Sucesso

| Métrica | Alvo |
|---------|------|
| Contexto usado por tarefa | < 30% do disponível |
| Delegação por tarefa | > 80% |
| Alucinações detectadas | < 1% |
| Tempo de execução | -50% vs fazer direto |

---

**Versão:** 1.0.0
**Data:** 2026-07-25
**Aplicação:** GLOBAL — todas as operações do Gran-Mestre