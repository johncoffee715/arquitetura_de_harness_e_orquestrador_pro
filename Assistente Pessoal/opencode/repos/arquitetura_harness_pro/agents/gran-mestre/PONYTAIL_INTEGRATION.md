# Ponytail (YAGNI Escada) — Autofagia + Helenização
## Disciplina de Simplicidade para o Gran-Mestre Pipeline

**Data:** 2026-07-25
**Origem:** Absorvido criticamente de Superpowers workflow — "94% rejection rate"
**Status:** Autofagia completa

---

## 1. O QUE É PONYTAIL

**Ponytail** é a disciplina de **não construir o que não é necessário agora**. O nome vem da metáfora "amarrar o cabelo para não atrapalhar" — remover o excesso antes que ele atrapalhe. Não é "fazer menos", é **fazer só o que precisa existir**.

No contexto Gran-Mestre, Ponytail é a **escada YAGNI** (You Aren't Gonna Need It) que todo código gerado pelo pipeline deve passar antes de ser escrito.

```
┌──────────────────────────────────────────────────────────────┐
│                    PONYTAIL / YAGNI ESCADA                     │
├──────────────────────────────────────────────────────────────┤
│  1. Precisa existir?          → não: pular (YAGNI)           │
│  2. Já existe no codebase?    → reutilizar, não reescrever   │
│  3. Stdlib resolve?           → usar stdlib                  │
│  4. Feature nativa da plataforma? → usar nativo              │
│  5. Dependência já instalada? → usar dependência             │
│  6. Cabe em uma linha?        → uma linha                    │
│  7. Só então: o mínimo que funciona                          │
└──────────────────────────────────────────────────────────────┘
```

## 2. CONCEITOS-CHAVE EXTRAÍDOS

### 2.1 YAGNI Escada (Degraus de Decisão)
- **Conceito:** Antes de escrever qualquer código, subir a escada de 7 degraus
- **Benefício:** Elimina código desnecessário antes de ser escrito
- **Regra:** Parar no primeiro degrau que valer — não descer mais

### 2.2 Exceções NUNCA Cortáveis
- **Conceito:** Mesmo no degrau 1 (YAGNI), certas validações são obrigatórias
- **Lista Fixa:**
  - Validação em limites de confiança (trust-boundary)
  - Tratamento de perda de dados
  - Segurança
  - Acessibilidade
- **Regra:** Essas NUNCA são cortadas, independente da escada

### 2.3 94% Rejeição (Superpowers Ethics)
- **Conceito:** Cultura de qualidade extrema onde 94% dos PRs são rejeitados
- **Métrica:** Cada linha deve ser justificável sob a escada
- **Efeito:** Código enxuto, manutenível, sem superconstrução

### 2.4 Antropofagia Aplicada ao Código
- **Conceito:** Não inventar o que já existe — absorver criticamente
- **Regra:** Se uma solução já existe, reutilizar. Só criar se for estritamente necessário.
- **Corolário:** "O melhor código é o código que você nunca escreveu."

---

## 3. COMPARAÇÃO COM GRAN-MESTRE

| Aspecto | Ponytail/Superpowers | Gran-Mestre |
|---------|----------------------|-------------|
| **Foco** | Não superconstruir | Orquestração e entrega |
| **Métrica** | 94% rejeição de PR | Gates de aprovação |
| **Ferramenta** | Escada YAGNI | Pipeline de validação |
| **Validação** | Code Reviewer verifica | Héstia + Fable Judge |
| **Custo** | 54% menos código | Qualidade por gates |
| **Velocidade** | 27% mais rápido | Latência por validações |

## 4. O QUE ABSORVER DO PONYTAIL

### 4.1 Escada YAGNI como Ferramenta de Decisão ✅ ABSORVIDO
```python
# Antes de escrever qualquer código:
def should_write_code(problem):
    # Degrau 1: Precisa existir?
    if not problem.necessary:
        return False, "YAGNI — não precisa existir"
    
    # Degrau 2: Já existe?
    if problem.exists_in_codebase:
        return False, "Reutilizar código existente"
    
    # Degrau 3: Stdlib resolve?
    if problem.solved_by_stdlib:
        return False, f"Usar stdlib: {problem.stdlib_solution}"
    
    # Degrau 4: Feature nativa?
    if problem.native_feature:
        return False, f"Usar feature nativa: {problem.native_feature}"
    
    # Degrau 5: Dependência instalada?
    if problem.installed_dependency:
        return False, f"Usar dependência: {problem.dependency}"
    
    # Degrau 6: Cabe em uma linha?
    if problem.one_liner:
        return True, "Uma linha: implementar inline"
    
    # Degrau 7: Mínimo que funciona
    return True, "Mínimo viável: implementar"
```

### 4.2 Code Review com Lente YAGNI ✅ ABSORVIDO
```markdown
# O Code Reviewer deve verificar na revisão micro:
1. Cada linha nova — qual degrau da escada justifica?
2. Código morto / não utilizado?
3. Supergeneralização desnecessária?
4. Abstração prematura?
5. Dependência nova que poderia ser evitada?
```

### 4.3 Métricas de Código Enxuto ✅ ABSORVIDO
```yaml
# Referência de impacto do Ponytail:
metrics:
  less_code: "~54% menos código (até 94% onde há superconstrução)"
  cost_reduction: "~20% mais barato"
  speed_improvement: "~27% mais rápido"
  safety: "100% — nunca corta validação obrigatória"
```

### 4.4 Regra de Ouro para Agentes 🟡 PARCIAL
```
# Implementer e Plan Writer DEVEM consultar a escada antes de cada task.
# Code Reviewer DEVE verificar a escada na revisão micro.
# Gran-Mestre DEVE citar a escada no relatório quando detectar superconstrução.
```

---

## 5. INTEGRAÇÃO COM GRAN-MESTRE

### 5.1 Fase 3 (Plano) — YAGNI Check
```
Plan Writer:
  1. Gera plano seguindo a escada YAGNI
  2. Cada task justificada contra a escada
  3. Héstia valida: tasks são necessárias?
```

### 5.2 Fase 4 (Execução) — YAGNI Enforcement
```
Implementer:
  1. Antes de cada task, verifica escada YAGNI
  2. Só implementa se passar nos 7 degraus
  
Code Reviewer:
  1. Verifica se implementação seguiu a escada
  2. Se detectar superconstrução → FIX_NEEDED
```

### 5.3 Fase 5 (Revisão Macro) — YAGNI Audit
```
Atena:
  1. Revisa diff total contra escada YAGNI
  2. Detecta padrões de superconstrução
  3. Relatório de aderência YAGNI
```

---

## 6. IMPLEMENTAÇÃO

### 6.1 Configuração Ponytail no Gran-Mestre

```json
{
  "gran-mestre": {
    "ponytail": {
      "enabled": true,
      "ladder_steps": 7,
      "never_cut": [
        "trust_boundary_validation",
        "data_loss_protection",
        "security",
        "accessibility"
      ],
      "check_on_plan": true,
      "check_on_execution": true,
      "check_on_review": true,
      "metrics_tracking": true
    }
  }
}
```

### 6.2 Template de Verificação YAGNI

```markdown
## Verificação YAGNI — Task: <task-name>

| Degrau | Pergunta | Resposta | Ação |
|--------|----------|----------|------|
| 1 | Precisa existir? | Sim/Não | Se não: pular |
| 2 | Já existe no codebase? | Sim/Não | Se sim: reutilizar |
| 3 | Stdlib resolve? | Sim/Não | Se sim: usar stdlib |
| 4 | Feature nativa? | Sim/Não | Se sim: usar nativo |
| 5 | Dependência instalada? | Sim/Não | Se sim: usar dependência |
| 6 | Cabe em 1 linha? | Sim/Não | Se sim: inline |
| 7 | Mínimo que funciona? | Sim | Implementar |

### Exceções Obrigatórias Verificadas
- [ ] Trust-boundary validation
- [ ] Data loss protection  
- [ ] Security
- [ ] Accessibility
```

### 6.3 Relatório de Aderência

```markdown
## Relatório YAGNI — Pipeline <id>

### Tasks Verificadas: <N>
### Tasks com Superconstrução: <N>
### Tasks Rejeitadas por YAGNI: <N>

### Superconstruções Detectadas
| Task | Tipo | Justificativa | Ação Corretiva |
|------|------|---------------|----------------|
| ... | abstração prematura | ... | simplificar |

### Métricas
- Código evitado: ~<X>% (estimado)
- Dependências evitadas: <N>
- Complexidade evitada: <score>
```

---

## 7. BENEFÍCIOS DA INTEGRAÇÃO

| Benefício | Descrição | Impacto Esperado |
|-----------|-----------|------------------|
| **Código Enxuto** | Menos código desnecessário | ~54% menos linhas |
| **Manutenibilidade** | Mais fácil de manter e entender | Redução de débito técnico |
| **Performance** | Menos código = menos latência | ~27% mais rápido |
| **Custo** | Menos tokens gerados | ~20% mais barato |
| **Segurança** | Exceções nunca cortadas | 100% de cobertura em validação crítica |
| **Qualidade** | Cada linha justificada | Padrão Superpowers de 94% rejeição |

## 8. PRÓXIMOS PASSOS

1. **Implementar verificação YAGNI** nos templates do Plan Writer
2. **Adicionar checklist YAGNI** ao Code Reviewer
3. **Métricas de aderência** no relatório do Gran-Mestre
4. **Treinar agentes** para consultar escada antes de cada task

---

## 9. REFERÊNCIAS

- **Superpowers Workflow:** Cultura de 94% rejeição de PR
- **YAGNI Principle:** Extreme Programming (XP) — "You Aren't Gonna Need It"
- **Ponytail Discipline:** Amarrar o excesso para não atrapalhar
- **Gran-Mestre TEMPLATE.md:** Seção 6 — Regras de Construção

---

**Versão:** 1.0.0
**Data:** 2026-07-25
**Autor:** Gran-Mestre (autofagia de Superpowers Ponytail + YAGNI)
**Helenização:** Escada YAGNI convertida para disciplina de pipeline Gran-Mestre
