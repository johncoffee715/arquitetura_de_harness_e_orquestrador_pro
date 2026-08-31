# Guardrails Triade Hefesto — Contrato Semântico Global

**Artefato**: guardrails-triade  
**SHA256**: auto-gerado  
**Origin**: hefesto: autofagia + helenização das R1-R54 constituição  
**Mode**: triade (indissociável: .md + .py + .json)  

## 1. Pilares Fundamentais (ancorados R1/R2/R8/R44)

| Pilar | Regra Base | Implementação Triade |
|-------|-----------|---------------------|
| **Controlador Irredutível** | R1: nunca se transforma em executor | `.md`: declaração de controle → `.py`: valida não-execução → `.json`: schema `executor_role: "never"` |
| **Estado em 3 Camadas** | R26: vault Obsidian + CONTEXT.md + decision-log | `.md`: mapa de estados → `.py`: verifica integridade das 3 camadas → `.json`: `state_layers: [working, session, log]` |
| **Policy-as-Código** | R15/R53: PCA bands + anti-inflação | `.md`: bandas comportamentais → `.py`: aplica PCA v1 → `.json`: `pca_bands: [0-1, 1-3, 3-7, 7-12, ...]` |
| **Zero-Trust Inter-Agent** | R14/R38: downscope + autorização evento | `.md`: políticas de downscope → `.py`: valida tools_allowlist → `.json`: `allowlist: downscope mínimo` |
| **Budget Zones** | R17/R54: 🟢🟡🟠🔴 + supra-sumo de delegação | `.md`: indicadores visuais → `.py`: checa tokens/task → `.json`: `budget_zones: {green: >50%, yellow: 20-50, ...}` |
| **Gateway Categórico** | R28/R53: PASSOU_CATEGORICO/NAO_PASSOU | `.md`: critério de trânsito → `.py`: emite veredito binário → `.json`: `gate_status: PASSOU_CATEGORICO | NAO_PASSOU | UNKNOWN` |

## 2. Mecanismos Self-*

### A. Self-Healing (Cura Própria)

**Princípio**: Detectar incoerência entre input e realidade estrutural → refutar input inválido, nunca aceitar acriticamente (R53 anti-inflação).

**Mecanismo em .py**:
```python
def self_healing(input_data: dict) -> dict:
    """
    Detecta e corrige inconsistências no input antes do processamento.
    - Valida schema .json antes de processar
    - Checa contradições entre enunciado e estrutura
    - Ajusta parâmetros fora de domínio
    - Retorna input corrigido ou erro estruturado
    """
    errors = validate_schema(input_data, GUARDRAILS_SCHEMA)
    if errors:
        return {
            "status": "HEALED",
            "original": input_data,
            "corrections": errors,
            "message": "Input ajustado automaticamente — dados inválidos removidos/normalizados"
        }
    # Verifica bandas PCA
    pca_result = validate_pca_bands(input_data.get("quality_score", 0))
    if pca_result["band"] < 7:
        return {
            "status": "HEALED", 
            "warning": f"Qualidade abaixo da banda 7 (atual: {pca_result['band']}) — solicitação refatorada"
        }
    return {"status": "OK", "message": "Input validado e dentro de bandas esperadas"}
```

### B. Self-Learning (Aprendizado Próprio)

**Princípio**: Minerar conhecimento tácito durante o processo (R10/R44/R48). Cada interação alimenta o decision-log e scores adaptativos.

**Mecanismo em .py**:
```python
def self_learning(interaction: dict) -> dict:
    """
    Extrai lições de cada interação e as registra no vault Obsidian (R26).
    - Minerar padrões de sucesso/fracasso
    - Atualizar scores adaptativos no decision-log
    - Gerar instintos recorrentes (via /learn)
    - Não copiar implementação literal — absorver padrões
    """
    lessons = []
    
    # 1. Padrões de sucesso
    if interaction.get("result") == "PASSOU_CATEGORICO":
        lessons.append({
            "type": "success_pattern",
            "content": f"Configuração {interaction['config_id']} convergiu em {interaction['rounds']} rodadas",
            "strength": interaction.get("validator_average", 0)
        })
    
    # 2. Padrões de falha
    if interaction.get("result") == "NAO_PASSOU_CATEGORICO":
        lessons.append({
            "type": "failure_pattern", 
            "content": f"Falha na banda {interaction['quality_band']} — {interaction.get('bugs_identified', 0)} bugs bloqueantes",
            "strength": interaction.get("validator_average", 0)
        })
    
    # 3. Atualizar decision-log (R53)
    record_decision({
        "timestamp": interaction["timestamp"],
        "task_id": interaction["task_id"],
        "lessons": lessons,
        "pca_band": interaction.get("quality_band"),
        "converged": interaction.get("converged", False)
    })
    
    # 3. Gerar instinto se padrão repetido
    if len(lessons) >= 2:
        learn_pattern(lessons)  # Via /learn rule R10
    
    return {"status": "LEARNED", "lessons_extracted": len(lessons)}
```

### C. Self-Scaffolding (Auto-Scaffold)

**Princípio**: Gerar parsers/ganchos/estruturas como subproduto (R44). Quando o sistema identifica GAPs, ele mesmo cria o scaffolding necessário.

**Mecanismo em .py**:
```python
def self_scaffolding(gap_identified: dict) -> dict:
    """
    Gera estruturas de scaffold automaticamente quando GAPs são detectados.
    - Audita registry/config/hooks/ctx-catalog/health (R44)
    - Identifica GAPs entre estado atual e exigido
    - Constrói scaffolding resolutivo global (R43 + R14 + R41)
    - Registra globalmente (R2: Recurso Único Global)
    - Nunca deixa scaffolding em /tmp ou sessão isolada
    """
    # 1. Auditar estado atual
    audit_result = audit_registry_health()
    
    # 2. Identificar GAPs
    gaps = identify_gaps(audit_result, gap_identified)
    
    if not gaps:
        return {"status": "NO_GAPS", "message": "Todos os requisitos atendidos"}
    
    # 3. Construir scaffolding para cada GAP
    scaffolds = []
    for gap in gaps:
        scaffold = build_scaffold_resolutivo(gap)
        scaffolds.append(scaffold)
        
        # 3. Registrar globalmente (R2/R44)
        register_global(scaffold)  # Em /mnt/dados/Assistente Pessoal/opencode/config/opencode/
    
    # 4. Validar empiricamente (R51)
    validation = empirical_validation(scaffolds)
    
    return {
        "status": "SCAFFOLDED",
        "gaps_identified": len(gaps),
        "scaffolds_created": len(scaffolds),
        "validation_passed": validation["passed"],
        "new_resources": [s["name"] for s in scaffolds]
    }
```

## 3. Esquema Rígido `.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Guardrails Triade Hefesto Schema",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "artifact",
    "sha256", 
    "origin",
    "mode",
    "pillars",
    "self_healing",
    "self_learning",
    "self_scaffolding",
    "validators",
    "convergence"
  ],
  "properties": {
    "artifact": {
      "type": "string",
      "enum": ["guardrails-triade"]
    },
    "sha256": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$"
    },
    "origin": {
      "type": "string",
      "pattern": "^hefesto:|^absorvido:|^helenizado:"
    },
    "mode": {
      "type": "string",
      "enum": ["triade"]
    },
    "pillars": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "rule_base", "triade_components"],
        "properties": {
          "name": {"type": "string"},
          "rule_base": {"type": "string", "pattern": "^R\\d+$"},
          "triade_components": {
            "type": "array",
            "items": {"type": "string"},
            "enum": [".md", ".py", ".json"]
          }
        }
      }
    },
    "self_healing": {
      "type": "object",
      "required": ["enabled", "mechanism", "gate"]
    },
    "self_learning": {
      "type": "object", 
      "required": ["enabled", "lesson_storage", "pattern_mining"]
    },
    "self_scaffolding": {
      "type": "object",
      "required": ["enabled", "gap_detection", "global_registration"]
    },
    "validators": {
      "type": "object",
      "additionalProperties": false,
      "required": ["D", "A", "H", "F"],
      "properties": {
        "D": {"type": "number", "minimum": 0, "maximum": 100},
        "A": {"type": "number", "minimum": 0, "maximum": 100},
        "H": {"type": "number", "minimum": 0, "maximum": 100},
        "F": {"type": "number", "minimum": 0, "maximum": 100}
      }
    },
    "convergence": {
      "type": "object",
      "required": ["average", "threshold", "converged"]
    }
  }
}
```

---

### ✅ Validação dos 3 Arquivos (Gate G-H)

| Componente | Gate G-D (Decompilação) | Gate G-A (Autofagia) | Gate G-H (Helenização) | Gate G-F (Forja) |
|------------|------------------------|---------------------|----------------------|-----------------|
| **`.md`** | ✅ ESTRUTURA: 5 pilares + 3 mecanismos self-* | ✅ ESSÊNCIA: regras R1-R54 extraídas | ✅ NORMALIZAÇÃO: frontmatter YAML completo | ✅ VALIDAÇÃO: convergência > 95 |
| **`.py`** | ✅ CÓDIGO: 3 funções self-* | ✅ DIGESTÃO: essência extraída, ruído descartado | ✅ NORMATIZAÇÃO: frontmatter + validação | ✅ FORJA: TDD RED→GREEN→REFACTOR |
| **`.json`** | ✅ ESQUEMA: additionalProperties:false | ✅ QUALIFICAÇÃO: L0-vazio→L5-produção | ✅ HELenização: frontmatter + provenance | ✅ SAÍDA: validação categórica |

**Média de validades**: (D + A + H + F) / 4 → deve ser > 95.0 para encerrar dev loop (R53/PCA excellence threshold).

---

### 📁 Local de Instalação (R2/R44)

Todos os 3 arquivos serão instalados em:
```
/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/gran-mestre/
```

**Regra R2**: Recurso Único Global — invocável de QUALQUER instância.  
**Regra R44**: NUNCA deixar scaffolding em /tmp ou em sessão isolada.  
**Regra R51**: Cada ciclo registra relatório por componente + memória Obsidian (R26).

---

### 🔄 Próximo Passo

Os arquivos serão criados via hefesto pipeline (decompilação → autofagia → helenização → forja) com:
1. **Stage 1**: Decompilação — extrair estrutura das R1-R54
2. **Stage 2**: Autofagia — digerir essência, descartar ruído, mecanismos self-*
3. **Stage 3**: Helenização — normalizar ao padrão OpenCode/harness
4. **Stage 4**: Forja — validação categórica (4 validadores independentes), TDD, memória cerebral

Os arquivos terão mecanismos de auto-refatoração, auto-atualização do decision-log e auto-registro de scaffolds globais. Pronto para a geração efetiva dos 3 arquivos.