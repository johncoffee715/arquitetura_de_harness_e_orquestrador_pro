# AUTOFAGIA — Templates Canônicos do Gran-Mestre
## Data: 2026-07-25 | Fonte: /mnt/win1/123 tranqueiras e projetos/Nova pasta/

---

## 1. TEMPLATES ANALISADOS

| Template | Componente | Modo | Linhas |
|----------|------------|------|--------|
| TEMPLATE-agent.md | Agent primary | primary | 81 |
| TEMPLATE-subagent.md | Subagent | subagent | 67 |
| TEMPLATE-skill.md | Skill | N/A | 41 |
| TEMPLATE-tool.md | Tool | N/A | 44 |
| TEMPLATE-mcp.md | MCP | N/A | 45 |

---

## 2. PADRÕES EXTRAÍDOS

### 2.1 TEMPLATE-agent.md (Primary)

**Campos-chave:**
- `mode: primary` — reservado para pontos de entrada reais
- `component_type: agent` — categorização lógica
- `pipeline:` — lista de subagents que o orquestrador comanda
- `safety_protocol:` — SHA, rollback, limites
- `complexity_range: [TRIVIAL..FEATURE]` — cobre TODAS as rotas

**Insight crítico:** "Criar um segundo 'primary' sem necessidade real reintroduz ambiguidade de roteamento"

### 2.2 TEMPLATE-subagent.md

**Campos-chave:**
- `mode: subagent` — padrão para praticamente tudo
- `capabilities:` — capability manifest
- `complexity_range:` — subconjunto de rotas
- `cost: light|medium|heavy` — estimativa de custo
- `requires: []` — MCPs/dependências externas
- `triggered_when:` — situação concreta
- `evaluates:` — o que avalia (se validador)
- `max_validation_cycles: 3` — contra LOOP_LIMIT_DECISION.md

### 2.3 TEMPLATE-skill.md

**Campos-chave:**
- `triggers:` — palavras-chave de ativação
- `metadata.origin:` — proveniência (antropofagia)
- `scripts_associados:` — TODO script .sh/.py/.js/.ts na mesma pasta
- **Insight crítico:** "A auditoria de segurança de 84 skills só cobriu SKILL.md e nunca tocou scripts"

### 2.4 TEMPLATE-tool.md

**Campos-chave:**
- SEM campo `mode:` — tool não é agente
- `component_type: tool`
- `invoked_by:` — quem chama
- `script:` — caminho real do script
- `deterministic: true|false`
- `input_contract:` / `output_contract:` — tipos e formas

### 2.5 TEMPLATE-mcp.md

**Campos-chave:**
- SEM campo `mode:` — MCP não é agente
- `type: remote|local`
- `url:` OU `command:` — um dos dois
- `capabilities_exposed:` — tools que disponibiliza
- `health_check:` — enabled, on_failure
- `requires:` — dependências de infraestrutura

---

## 3. GAPS IDENTIFICADOS NO TEMPLATE.md ATUAL

| Gap | Template Novo | TEMPLATE.md Atual |
|-----|---------------|-------------------|
| `component_type` | ✅ Separado de `mode` | ❌ Não tem |
| `pipeline:` | ✅ Lista de subagents | ❌ Não tem |
| `safety_protocol:` | ✅ Detalhado | ❌ Não tem |
| `cost:` | ✅ light/medium/heavy | ❌ Não tem |
| `requires:` | ✅ Array de deps | ❌ Não tem |
| `triggered_when:` | ✅ Campo separado | ❌ Não tem |
| `evaluates:` | ✅ Campo separado | ❌ Não tem |
| `scripts_associados:` | ✅ Obrigatório em skills | ❌ Não tem |
| `invoked_by:` | ✅ Para tools | ❌ Não tem |
| `deterministic:` | ✅ Para tools | ❌ Não tem |
| `input/output_contract:` | ✅ Para tools | ❌ Não tem |
| `health_check:` | ✅ Para MCPs | ❌ Não tem |
| `capabilities_exposed:` | ✅ Para MCPs | ❌ Não tem |

---

## 4. AÇÕES DE HELENIZAÇÃO

### 4.1 Atualizar TEMPLATE.md v2.0 → v3.0

Absorver TODOS os campos dos 5 templates canônicos.

### 4.2 Criar templates individuais

Copiar os 5 templates para `~/.config/opencode/agents/gran-mestre/templates/`

### 4.3 Atualizar agents existentes

Adicionar campos faltantes (pipeline, safety_protocol, cost, requires, triggered_when, evaluates)

---

**Versão:** 1.0.0
**Data:** 2026-07-25
**Fonte:** /mnt/win1/123 tranqueiras e projetos/Nova pasta/