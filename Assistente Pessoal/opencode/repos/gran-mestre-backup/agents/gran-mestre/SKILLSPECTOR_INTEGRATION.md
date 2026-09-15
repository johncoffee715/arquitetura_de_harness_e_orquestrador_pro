# Skillspector (Skill Inspection & Testing) — Autofagia + Helenização
## Inspeção, Validação e Teste de Skills

**Data:** 2026-07-25
**Origem:** Absorvido criticamente de Superpowers skill validation + Fable Judge adversarial testing
**Status:** Autofagia completa

---

## 1. O QUE É SKILLSPECTOR

**Skillspector** é o padrão de **inspeção e validação de skills** no pipeline Gran-Mestre. Não é uma skill específica — é uma **camada de qualidade** que garante que toda skill, tool, agent ou MCP atenda aos critérios antes de ser registrada.

```
┌──────────────────────────────────────────────────────────────┐
│                    SKILLSPECTOR PIPELINE                       │
├──────────────────────────────────────────────────────────────┤
│  Nova skill → Inspeção de estrutura                          │
│                   ↓                                          │
│              Validação de metadata                           │
│                   ↓                                          │
│              Teste adversarial (Fable Judge)                  │
│                   ↓                                          │
│           ┌── Aprovado?                                      │
│           │ Sim → Registrar no capability-index              │
│           │ Não → Feedback + corrigir                        │
│           └───────────────────────                            │
│                   ↓                                          │
│              Monitoramento contínuo                           │
└──────────────────────────────────────────────────────────────┘
```

## 2. CONCEITOS-CHAVE EXTRAÍDOS

### 2.1 Structural Inspection (Inspeção Estrutural)
- **Conceito:** Verificar se a skill segue o template obrigatório do Gran-Mestre
- **Verificações:**
  - YAML frontmatter presente e válido
  - Campos obrigatórios preenchidos (name, description, model, mode, origin)
  - Seções obrigatórias existentes
  - Regras claras e específicas (não genéricas)

### 2.2 Adversarial Testing (Teste Adversarial)
- **Conceito:** Testar a skill em condições adversas (limite, borda, erro)
- **Origem:** Fable Judge — verificação adversarial de trabalho concluído
- **Benefício:** Detecta falsos completos, checks enfraquecidos, promessas vazias

### 2.3 Capability Index Validation (Validação de Capacidades)
- **Conceito:** Verificar se as capacidades declaradas são reais e mensuráveis
- **Verificações:**
  - Capacidade declarada existe no código da skill?
  - Ação prometida é realmente executável?
  - Limitação documentada?

### 2.4 Continuous Monitoring (Monitoramento Contínuo)
- **Conceito:** Skills são monitoradas após registro para detectar degradação
- **Métricas:** Taxa de uso, taxa de sucesso, tempo de execução, erros
- **Ação:** Skill com baixa performance é marcada para revisão

---

## 3. COMPARAÇÃO COM GRAN-MESTRE

| Aspecto | Skillspector (genérico) | Gran-Mestre Skillspector |
|---------|------------------------|--------------------------|
| **Template** | Qualquer formato | TEMPLATE.md obrigatório |
| **Validação** | Genérica | Fable Judge adversarial |
| **Capacidades** | Lista declarativa | Verificação contra código real |
| **Registro** | Catálogo simples | Capability-index + agent-registry |
| **Monitoramento** | Métricas básicas | Pipeline de auditoria 14 passos |
| **Correção** | Manual | Self-healing (Improve) |

## 4. O QUE ABSORVER DO SKILLSPECTOR

### 4.1 Template Validation ✅ ABSORVIDO
```python
def validate_skill_template(skill_path):
    """Valida se skill segue o template Gran-Mestre."""
    errors = []
    
    # 1. Verificar YAML frontmatter
    if not has_yaml_frontmatter(skill_path):
        errors.append("Missing YAML frontmatter")
    
    content = read_skill(skill_path)
    
    # 2. Verificar campos obrigatórios
    required_fields = ['name', 'description', 'model', 'mode', 'origin']
    for field in required_fields:
        if field not in content.metadata:
            errors.append(f"Missing required field: {field}")
    
    # 3. Verificar seções obrigatórias
    required_sections = ['Quando usar', 'Comandos', 'Fluxo de Execução']
    for section in required_sections:
        if section not in content.sections:
            errors.append(f"Missing required section: {section}")
    
    # 4. Verificar regras específicas
    if not has_specific_rules(content):
        errors.append("Rules are too generic — must be project-specific")
    
    return errors
```

### 4.2 Adversarial Skill Testing ✅ ABSORVIDO
```python
def adversarial_skill_test(skill_path):
    """Testa skill adversarialmente (Fable Judge pattern)."""
    content = read_skill(skill_path)
    findings = []
    
    # 1. Afirmações: extrair promessas da skill
    claims = extract_claims(content)
    
    # 2. Verificar cada afirmação
    for claim in claims:
        # Re-executa cada verificação afirmada
        result = verify_claim(claim)
        
        if result == FALSE_COMPLETE:
            findings.append({
                "claim": claim,
                "issue": "Falso completo — promete mas não entrega",
                "severity": "CRITICAL"
            })
        elif result == WEAKENED_CHECK:
            findings.append({
                "claim": claim,
                "issue": "Check enfraquecido — condicional demais",
                "severity": "IMPORTANT"
            })
    
    return findings
```

### 4.3 Capability-Index Validation 🟡 PARCIAL
```yaml
# Verificação de capacidades declaradas
capability_validation:
  checks:
    - capability_declared: <nome>
      exists_in_code: <path/linha>
      action: <descrição da ação>
      verifiable: true/false
      limitation: <se aplicável>
  
  # Regras:
  # 1. Toda capacidade declarada DEVE ser verificável no código
  # 2. Toda ação prometida DEVE ser executável
  # 3. Limitações DEVEM ser documentadas explicitamente
```

### 4.4 Skill Health Check 🟡 PARCIAL
```json
{
  "skill_health": {
    "skill_name": "<nome>",
    "structural_inspection": "PASS/FAIL",
    "adversarial_test": "PASS/FAIL",
    "capability_validation": "PASS/FAIL",
    "metrics": {
      "usage_count": 0,
      "success_rate": 0.0,
      "avg_execution_time": 0.0,
      "error_count": 0
    },
    "last_audit": "<data>",
    "next_audit": "<data>",
    "status": "healthy/degraded/broken"
  }
}
```

---

## 5. INTEGRAÇÃO COM GRAN-MESTRE

### 5.1 Pré-Registro — Skillspector Validation
```
Nova skill criada
  → Skillspector valida template
  → Teste adversarial (Fable Judge)
  → Validação de capacidades
  → Se PASS → registrar no capability-index
  → Se FAIL → feedback + aguardar correção
```

### 5.2 Pós-Registro — Continuous Monitoring
```
Skill registrada
  → Monitoramento contínuo de métricas
  → Auditoria periódica (a cada N pipelines)
  → Se degradação → marcar para revisão
  → Se broken → remover do registry
```

### 5.3 Na Criação de Skills — Template Enforcement
```
Plan Writer / Atlas geram nova skill
  → Skillspector verifica template automaticamente
  → Se faltar campos → auto-preenche com defaults
  → Se violar regras → bloqueia registro
```

---

## 6. IMPLEMENTAÇÃO

### 6.1 Configuração Skillspector no Gran-Mestre

```json
{
  "gran-mestre": {
    "skillspector": {
      "enabled": true,
      "structural_inspection": {
        "required_fields": [
          "name", "description", "model", "mode", "origin"
        ],
        "required_sections": [
          "Quando usar", "Comandos", "Fluxo de Execução",
          "Critérios de Saída", "O que NÃO faz", "Segurança"
        ],
        "yaml_validation": true
      },
      "adversarial_testing": {
        "fable_judge": true,
        "max_cycles": 2,
        "check_false_completes": true,
        "check_weakened_checks": true
      },
      "capability_index": {
        "validate_on_register": true,
        "require_verifiable_capabilities": true
      },
      "monitoring": {
        "enabled": true,
        "audit_frequency_pipelines": 10,
        "metrics_tracking": true,
        "auto_disable_on_degradation": true
      }
    }
  }
}
```

### 6.2 Template de Inspeção de Skill

```markdown
## Relatório Skillspector — Skill: <nome>

### Structural Inspection
- [ ] YAML frontmatter presente
- [ ] Campos obrigatórios preenchidos
- [ ] Seções obrigatórias existem
- [ ] Regras são específicas (não genéricas)
- [ ] Modelo definido (não "default")
- [ ] Origem documentada
- [ ] Modo de operação definido

### Adversarial Test
- [ ] Afirmações verificadas: <N>
- [ ] Falsos completos detectados: <N>
- [ ] Checks enfraquecidos detectados: <N>
- [ ] Veredito: <PASS / FAIL / NEEDS_CORRECTION>

### Capability Validation
- [ ] Capacidades são verificáveis: Sim/Não
- [ ] Ações prometidas são executáveis: Sim/Não
- [ ] Limitações documentadas: Sim/Não
- [ ] Veredito: <PASS / FAIL>

### Overall Verdict
- **Status:** <HEALTHY / DEGRADED / BROKEN>
- **Recomendação:** <Aprovar / Corrigir / Rejeitar>
```

### 6.3 Gatilhos de Inspeção

| Evento | Ação | Automático? |
|--------|------|-------------|
| Nova skill criada | Inspeção estrutural + adversarial | ✅ Sim |
| Skill atualizada | Re-inspeção completa | ✅ Sim |
| Skill degradada | Auditoria 14 passos | ✅ Sim |
| Pipeline falha por skill | Análise de causa + correção | ✅ Sim (2x) |
| N pipelines rodados | Auditoria periódica | ✅ Sim |
| Skill removida | Limpeza de registry | ✅ Sim |

---

## 7. BENEFÍCIOS DA INTEGRAÇÃO

| Benefício | Descrição |
|-----------|-----------|
| **Qualidade** | Toda skill passa por validação rigorosa |
| **Consistência** | Skills seguem o mesmo template padronizado |
| **Confiabilidade** | Teste adversarial detecta falsos completos |
| **Rastreabilidade** | Capacidades são verificáveis |
| **Manutenibilidade** | Skills degradadas são detectadas cedo |
| **Automação** | Inspeção e correção automáticas |

## 8. PRÓXIMOS PASSOS

1. **Implementar script de inspeção automática** para novas skills
2. **Configurar adversarial testing** com Fable Judge em skills existentes
3. **Criar dashboard de monitoramento** de saúde das skills
4. **Automatizar correção** de skills com problemas estruturais

---

## 9. REFERÊNCIAS

- **GRAN_MESTRE.md:** Seção "Agentes do Pipeline — Status de Implementação"
- **TEMPLATE.md:** Seções 2-4 (templates de agent, skill, tool)
- **Fable Judge:** Verificação adversarial de trabalho concluído
- **Capability-Index:** Registry de capacidades por agente/skill

---

**Versão:** 1.0.0
**Data:** 2026-07-25
**Autor:** Gran-Mestre (autofagia de Superpowers validation + Fable Judge testing)
**Helenização:** Skill inspection + adversarial testing convertidos para pipeline Gran-Mestre
