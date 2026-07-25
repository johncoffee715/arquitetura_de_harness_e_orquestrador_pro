# Improve (Self-Healing Pipeline) — Autofagia + Helenização
## Melhoria Contínua e Correção Automática

**Data:** 2026-07-25
**Origem:** Absorvido criticamente de Superpowers + Fable Method + Gran-Mestre nativo
**Status:** Autofagia completa

---

## 1. O QUE É IMPROVE

**Improve** é a capacidade do pipeline Gran-Mestre de **se auto-corrigir e evoluir** sem intervenção manual. Não é um agente específico — é um **padrão de orquestração** que combina:

1. **Auditoria Sistemática** (14 passos de engenharia reversa)
2. **Self-Healing** (detecção + correção automática)
3. **Loop de Validação** (Héstia + Fable Judge em paralelo)
4. **Melhoria Contínua** (métricas → ajuste → evolução)

```
┌──────────────────────────────────────────────────────────────┐
│                    IMPROVE / SELF-HEALING                      │
├──────────────────────────────────────────────────────────────┤
│  Pipeline falha? → Auditoria (14 passos)                     │
│                        ↓                                     │
│              Análise de Causa Raiz                           │
│                        ↓                                     │
│           ┌─── Correção automática possível?                 │
│           │ Sim → Aplicar correção → Validar                  │
│           │ Não → Escalar ao usuário                         │
│           └───────────────────────                            │
│                        ↓                                     │
│              Extrair aprendizado → Memória                    │
│                        ↓                                     │
│              Ajustar pipeline → Prevenir reincidência        │
└──────────────────────────────────────────────────────────────┘
```

## 2. CONCEITOS-CHAVE EXTRAÍDOS

### 2.1 Metodologia de 14 Passos (Auditoria)
- **Conceito:** Toda análise segue sequência obrigatória de 14 passos
- **Origem:** Template de Auditoria do GRAN_MESTRE.md (Downloads/11)
- **Benefício:** Consistência, profundidade, rastreabilidade

| # | Passo | Descrição |
|---|-------|-----------|
| 1 | Visão Geral da Arquitetura | Estado atual, funcionamento, dependências |
| 2 | Auditoria Técnica | Pontos fortes/fracos, inconsistências, redundâncias |
| 3 | Engenharia Reversa | Reconstrução da arquitetura, lógica, fluxo |
| 4 | Análise de Problemas | Causa raiz, impacto, risco, efeito cascata |
| 5 | Predição | Gargalos futuros, limitações, escalabilidade |
| 6 | Prevenção | Medidas preventivas, boas práticas, validações |
| 7 | Correção | Soluções objetivas com justificativa técnica |
| 8 | Refatoração | Simplificação, modularização, redução de complexidade |
| 9 | Integração | Compatibilidade, impacto, plano de migração |
| 10 | Comparação | Original vs corrigido, benefícios obtidos |
| 11 | Melhorias Técnicas | Imediatas, médio prazo, longo prazo |
| 12 | Roadmap | Próxima evolução recomendada |
| 13 | Checklist | Implementado, corrigido, pendente, futuro |
| 14 | Entrega | Plug-and-Play para execução imediata |

### 2.2 Self-Healing (Auto-Correção)
- **Conceito:** Pipeline detecta falha, analisa causa, aplica correção
- **Regra:** Máximo de 2 tentativas de auto-correção antes de escalar
- **Trigger:** Falha em gate, reprovação de Héstia, erro de execução

### 2.3 Classificação de Recomendações
- **Conceito:** Toda recomendação classificada por prioridade
- **Níveis:**
  - **CRÍTICA** — implementar imediatamente
  - **IMPORTANTE** — implementar em breve
  - **OPCIONAL** — implementar quando conveniente
  - **FUTURA** — planejar para o futuro

### 2.4 Extração de Aprendizado (Learning Loop)
- **Conceito:** Após cada correção, extrair aprendizado para a memória
- **Destino:** Obsidian vault — `aprendizados/` (sucessos, falhas, insights)
- **Benefício:** Pipeline melhora com o tempo sem intervenção manual

---

## 3. COMPARAÇÃO COM GRAN-MESTRE

| Aspecto | Improve (genérico) | Gran-Mestre Improve |
|---------|-------------------|---------------------|
| **Auditoria** | 14 passos padrão | Adaptado ao pipeline (fases, gates, agentes) |
| **Self-healing** | Genérico | Específico: rollback SHA, retry task, fallback |
| **Loop** | Indefinido | 2 tentativas máx + escalonamento |
| **Memória** | Banco de knowlege | Obsidian vault cerebro |
| **Classificação** | Crítica/Importante/Opicional/Futura | + Prioridade por fase do pipeline |
| **Entrega** | Relatório | Plug-and-play (Ctrl+C/V) |

## 4. O QUE ABSORVER DO IMPROVE

### 4.1 Ciclo de Self-Healing ✅ ABSORVIDO
```python
def self_heal(pipeline_phase, error):
    """Tenta auto-corrigir uma fase do pipeline."""
    attempts = 0
    max_attempts = 2
    
    while attempts < max_attempts:
        attempts += 1
        
        # Passo 1: Analisar causa raiz
        root_cause = analyze_root_cause(error)
        
        # Passo 2: Determinar se correção é automática
        if root_cause.is_automatable:
            correction = apply_correction(root_cause)
            
            # Passo 3: Validar correção
            validation = validate_correction(correction)
            if validation.passed:
                log_improvement(pipeline_phase, correction)
                return correction
        else:
            # Passo 2b: Se não automática, escalar
            break
    
    # Passo 4: Escalar ao usuário após 2 falhas
    escalate_to_user(pipeline_phase, error, attempts)
```

### 4.2 Template de Auditoria Plug-and-Play ✅ ABSORVIDO
```markdown
## Auditoria: <tema>

### 1. Visão Geral da Arquitetura
### 2. Auditoria Técnica
### 3. Engenharia Reversa
### 4. Análise de Problemas
...
### 14. Entrega (Plug-and-Play)
```

### 4.3 Classificação de Recomendações com Ação ✅ ABSORVIDO
```yaml
classification:
  CRITICAL:
    action: "implementar imediatamente"
    response_time: "horas"
    escalates_to: "usuário se não resolvido em 1h"
  
  IMPORTANT:
    action: "implementar em breve"
    response_time: "dias"
    escalates_to: "próximo pipeline"
  
  OPTIONAL:
    action: "implementar quando conveniente"
    response_time: "semanas"
    escalates_to: "nunca (backlog)"
  
  FUTURE:
    action: "planejar para o futuro"
    response_time: "meses"
    escalates_to: "próximo milestone"
```

### 4.4 Learning Extraction Pattern 🟡 PARCIAL
```markdown
## Aprendizado Extraído

### Contexto
<O que estava acontecendo quando o problema ocorreu>

### Causa Raiz
<Por que o problema aconteceu>

### Correção Aplicada
<O que foi feito para corrigir>

### Prevenção Futura
<O que mudar no pipeline para evitar reincidência>

### Métricas
- Tempo até detecção: <X> minutos
- Tempo até correção: <Y> minutos
- Resultado: <sucesso / escalado>
```

---

## 5. INTEGRAÇÃO COM GRAN-MESTRE

### 5.1 Fase 4 (Execução) — Self-Healing Loop
```
Atlas detecta erro de execução
  → Analisa causa raiz
  → Tenta correção automática
  → Se falha 2x → escala ao Gran-Mestre
  → Gran-Mestre decide: retry, ajuste, rollback
```

### 5.2 Fase 5 (Revisão) — Improve Check
```
Atena encontra problema no diff
  → Classifica severidade (CRÍTICA/IMPORTANTE/OPCIONAL)
  → Se CRÍTICA → sugere correção + gatilho de self-healing
  → Se IMPORTANTE → documenta para próxima execução
```

### 5.3 Após Pipeline — Learning Extraction
```
Pipeline completo
  → Extrair aprendizados (sucessos, falhas, insights)
  → Classificar recomendações
  → Arquivar no Obsidian vault
  → Atualizar template de auditoria se necessário
```

---

## 6. IMPLEMENTAÇÃO

### 6.1 Configuração Improve no Gran-Mestre

```json
{
  "gran-mestre": {
    "improve": {
      "enabled": true,
      "self_healing": {
        "max_attempts": 2,
        "automatable_errors": [
          "lint_error",
          "test_failure",
          "type_error",
          "import_error"
        ],
        "escalate_on_failure": true
      },
      "audit": {
        "template_steps": 14,
        "classify_recommendations": true,
        "plug_and_play_delivery": true
      },
      "learning": {
        "extract_after_pipeline": true,
        "save_to_obsidian": true,
        "vault_path": "/mnt/dados/cerebro com IA/aprendizados/"
      }
    }
  }
}
```

### 6.2 Triggers de Self-Healing

| Evento | Ação | Automático? |
|--------|------|-------------|
| Lint error | Auto-fix (ruff --fix, biome check --fix) | ✅ Sim |
| Test failure | Debug + corrigir + rodar de novo | ✅ Sim (2x) |
| Type error | Corrigir tipo + verificar | ✅ Sim |
| Import error | Instalar dependência + verificar | ✅ Sim |
| Gate reprovado | Re-analisar com Héstia + ajustar | ✅ Sim (2x) |
| Rollback necessário | git reset --hard SHA + reportar | 🟡 Com validação |
| Falha de API | Retry com backoff + fallback | ✅ Sim |
| Erro desconhecido | Escalar ao usuário | ❌ Não |

### 6.3 Relatório de Melhoria Contínua

```markdown
## Relatório Improve — Pipeline <id>

### Self-Healing
- Tentativas de auto-correção: <N>
- Correções aplicadas: <N>
- Falhas escaladas: <N>

### Recomendações
- CRÍTICAS: <N>
- IMPORTANTES: <N>
- OPCIONAIS: <N>
- FUTURAS: <N>

### Aprendizados Extraídos
- Sucessos: <N>
- Falhas: <N>
- Insights: <N>

### Ações para Próximo Pipeline
- <ação 1>
- <ação 2>
```

---

## 7. BENEFÍCIOS DA INTEGRAÇÃO

| Benefício | Descrição |
|-----------|-----------|
| **Auto-Correção** | Pipeline se recupera de erros comuns sem intervenção |
| **Consistência** | Auditoria sempre segue os mesmos 14 passos rigorosos |
| **Priorização** | Recomendações classificadas por impacto e urgência |
| **Memória** | Pipeline melhora com o tempo (learning loop) |
| **Plug-and-Play** | Toda entrega é imediatamente executável |
| **Resiliência** | Menos falhas escaladas ao usuário |

## 8. PRÓXIMOS PASSOS

1. **Implementar self-healing automático** para erros comuns na Fase 4
2. **Criar template de extração de aprendizado** para pós-pipeline
3. **Configurar classificação automática** de recomendações
4. **Métricas de melhoria contínua** dashboard

---

## 9. REFERÊNCIAS

- **GRAN_MESTRE.md (Downloads/11):** Seções 1-14 da Metodologia de Auditoria
- **Fable Method:** Verificação adversarial para validar correções
- **Obsidian Vault:** Armazenamento de aprendizados (`aprendizados/`)
- **Safety Protocol:** SHA + rollback automático

---

**Versão:** 1.0.0
**Data:** 2026-07-25
**Autor:** Gran-Mestre (autofagia de Superpowers + Fable Method + Auditoria Nativa)
**Helenização:** Self-healing + auditoria 14 passos convertidos para pipeline Gran-Mestre
