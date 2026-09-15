# TEMPLATE PADRÃO — Construção de Skills, Tools e Agents
## Gran-Mestre Engineering Standard v3.0

**Atualizado:** 2026-07-25 | **Autofagia:** Templates canônicos do Gran-Mestre
**Templates individuais:** `templates/TEMPLATE-agent.md`, `templates/TEMPLATE-subagent.md`, `templates/TEMPLATE-skill.md`, `templates/TEMPLATE-tool.md`, `templates/TEMPLATE-mcp.md`

---

## 1. FILOSOFIA DE CONSTRUÇÃO

### Princípios Fundamentais

1. **Precisão** — Cada linha deve ter propósito claro
2. **Incisividade** — Sem ambiguidade, sem "pode ser que"
3. **Pragmatismo** — Funcionalidade real, não teórica
4. **Conformidade** — 100% alinhado com a demanda do projeto
5. **Antropofagia** — Absorver criticamente, nunca copiar cegamente
6. **Helenização** — Converter sempre para o padrão OpenCode

### Processo de Autofagia + Helenização

A **autofagia** é o processo de absorver criticamente tecnologias externas. A **helenização** é a etapa de conversão para o padrão OpenCode. Juntas, formam o ciclo completo:

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTOFAGIA + HELENIZAÇÃO                   │
├─────────────────────────────────────────────────────────────┤
│  1. IDENTIFICAR    — Encontrar tecnologia útil externa      │
│  2. ANALISAR       — Avaliar o que é útil vs inútil         │
│  3. ABSORVER       — Autoplagiar o que funciona             │
│  4. HELENIZAR      — Converter para padrão OpenCode         │
│  5. INTEGRAR       — Incorporar ao workflow Gran-Mestre      │
│  6. VALIDAR        — Testar adversarialmente                │
└─────────────────────────────────────────────────────────────┘
```

### O que é "94% rejeição do Superpowers"

O Superpowers tem uma cultura de **qualidade extrema** onde:
- 94% dos PRs de agentes são rejeitados
- Cada PR deve ter evidência de envolvimento humano
- Skills são "código que molda comportamento", não prosa
- Mudanças requerem eval antes/depois

**Para o Gran-Mestre:** Isso significa que cada skill, tool e agent deve ser:
- Testado adversarialmente
- Documentado com evidência
- Validado contra o projeto real
- Rejeitado se não atingir o padrão
- **Helenizado** se veio de outro harness

---

## 2. TEMPLATE DE AGENT

### Estrutura Obrigatória

```markdown
---
name: <nome-do-agent>
description: "<descrição precisa em 1-2 linhas>"
model: <modelo-específico-do-harness>
mode: <agent|subagent|tool|skill|mcp>
origin: <gran-mestre-original|oh-my-openagent|superpowers|fable-method>
metadata:
  category: <orchestration|execution|validation|review|research>
  not_from: <framework-que-não-criou>
  note: "<explicação curta da origem>"
  version: "<semver>"
  author: "<criador>"
---

# <Nome> — <Papel em 3-5 palavras>

<1 parágrafo definindo o que é e o que faz>

## Quando você é chamado

<Lista numerada com fase, contexto e ação>

## Comandos

```
/comando <args>    - Descrição
```

## O que você avalia

<Lista de critérios específicos do projeto>

## Regras

<Lista numerada de regras inflexíveis>

## O que você NÃO faz

<Lista do que é proibido>

## Modo de Operação

<Autônomo ou interativo, com regras claras>

## Segurança

<Permissões e restrições>
```

### 2.1 Capability Manifest (Novo Padrão)

Além dos campos obrigatórios, todo componente agora DEVE declarar suas **capacidades** e **modelo com fallback**:

```yaml
# NOVO: Capability Manifest — usado pelo CapabilityIndex (greedy cover)
capabilities:
  - <capability-1>
  - <capability-2>
complexity_range: [MEDIUM, COMPLEX]   # TRIVIAL, SIMPLE, MEDIUM, COMPLEX, CRITICAL, FEATURE
cost: medium                          # light | medium | heavy
requires: []                          # MCPs/dependências externas

# NOVO: Model Rotation — primário + cadeia de fallback
model:
  primary: <modelo-principal-do-harness>
  fallback_chain:
    - <modelo-alternativo-1>
    - <modelo-alternativo-2>
    - cloud:<provider/modelo>
```

**Regras do Capability Manifest:**
- `capabilities`: Lista de capacidades funcionais — cada uma DEVE ser verificável no código/skill
- `complexity_range`: Intervalo de complexidade que o componente atende
- `cost`: Custo relativo de execução (light = nano, medium = gpt-5.5, heavy = opus)
- `requires`: Dependências externas (MCPs, serviços, APIs)

**Regras do Model Rotation:**
- `model.primary`: Modelo principal — DEVE ser específico, nunca "default" ou genérico
- `model.fallback_chain`: Lista ordenada — se o primary falhar, rotaciona nessa ordem
- `cloud:<provider/modelo>`: Último recurso (ex: `cloud:omniroute/kimi-k3`)
- Toda rotação é registrada: `[Model-Fallback] Component: <nome> | Tried: <primary> | Used: <fallback> | Reason: <motivo>`

### 2.2 Provenance Tracking (Rastreamento de Origem)

Para componentes absorvidos via antropofagia, usar `origin` com prefixo `absorvido:`:

```yaml
# Origem nativa
origin: gran-mestre-original

# Origem por antropofagia
origin: absorvido:oh-my-openagent   # absorvido de Oh-My-OpenAgent
origin: absorvido:superpowers        # absorvido de Superpowers
origin: absorvido:fable-method       # absorvido de Fable Method
origin: crossover:superpowers+fable  # crossover entre 2+ frameworks
```

**Seção de Proveniência (dentro do corpo do documento):**

```markdown
## Proveniência (crossover)

<De onde vem cada parte deste componente — nome emprestado de qual
 framework, comportamento inspirado em qual skill, o que é 100%
 original do Gran-Mestre. Responde de cara "isso é nosso ou herdado?"
 sem precisar caçar em 3 repositórios diferentes.>
```

**Campos Obrigatórios**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| name | string | Nome único, lowercase, hífens |
| description | string | 1-2 linhas, precisa |
| model | object | `{primary, fallback_chain}` — ver Model Rotation |
| mode | enum | subagent (preferencial) ou primary (só Gran-Mestre) |
| origin | string | `gran-mestre-orinal` ou `absorvido:<framework>` |
| metadata.category | enum | Categoria funcional |
| metadata.version | string | Semver |
| metadata.author | string | Criador |
| capabilities | list | Capacidades funcionais verificáveis |
| complexity_range | list | Intervalo de complexidade |
| cost | string | light, medium, heavy |
| requires | list | Dependências externas |

---

## 3. TEMPLATE DE SKILL

### Estrutura Obrigatória

```markdown
---
name: <nome-da-skill>
description: "<descrição precisa em 1-2 linhas>"
trigger: /<comando>
model: <modelo-específico-do-harness>
mode: <skill|tool>
origin: <gran-mestre-original|oh-my-openagent|superpowers|fable-method>
metadata:
  category: <orchestration|execution|validation|review|research>
  not_from: <framework-que-não-criou>
  note: "<explicação curta da origem>"
  version: "<semver>"
  author: "<criador>"
---

# <Nome> — <Propósito em 3-5 palavras>

<1 parágrafo definindo o que é e o que faz>

## Quando usar

<Condições específicas de ativação>

## Comandos

```
/comando <args>    - Descrição
```

## Fluxo de Execução

<Passos numerados e claros>

## Critérios de Saída

<Quando o trabalho está "feito">

## O que você NÃO faz

<Lista do que é proibido>

## Segurança

<Permissões e restrições>
```

---

## 4. TEMPLATE DE TOOL

### Estrutura Obrigatória

```markdown
---
name: <nome-da-tool>
description: "<descrição precisa em 1-2 linhas>"
model: <modelo-específico-do-harness>
mode: <tool>
origin: <gran-mestre-original|oh-my-openagent|superpowers|fable-method>
metadata:
  category: <orchestration|execution|validation|review|research>
  not_from: <framework-que-não-criou>
  note: "<explicação curta da origem>"
  version: "<semver>"
  author: "<criador>"
---

# <Nome> — <Função em 3-5 palavras>

<1 parágrafo definindo o que é e o que faz>

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| param1 | string | Sim | Descrição |
| param2 | number | Não | Descrição |

## Uso

```
/tool-name param1=value1 param2=value2
```

## Comportamento

<O que a tool faz em detalhes>

## Erros

| Erro | Causa | Solução |
|------|-------|---------|
| error1 | Causa1 | Solução1 |

## Segurança

<Permissões e restrições>
```

---

## 5. MODELOS DISPONÍVEIS NO HARNESS

### Modelos por Categoria

| Categoria | Modelo | Variante | Uso Recomendado |
|-----------|--------|----------|-----------------|
| **Máximo** | github-copilot/claude-opus-4.7 | max | Agents complexos, orquestração |
| **Alto** | github-copilot/gpt-5.5 | high | Agents de análise, verificação |
| **Médio** | github-copilot/gpt-5.5 | medium | Agents de execução |
| **Baixo** | opencode/gpt-5-nano | - | Agents de exploração |
| **Rápido** | github-copilot/claude-haiku-4.5 | - | Tasks simples |
| **Específico** | opencode/kimi-k2.5 | - | Tasks específicas |
| **Específico** | opencode/glm-5 | - | Tasks específicas |

### Fallback Chains

```yaml
# Para agents críticos (Héstia, Atena)
model:
  primary: github-copilot/claude-opus-4.7
  fallback_chain:
    - opencode/claude-opus-4-7
    - github-copilot/gpt-5.5 (high)
    - cloud:opencode-go/kimi-k3

# Para agents de execução (Atlas, Implementer)
model:
  primary: github-copilot/gpt-5.5 (medium)
  fallback_chain:
    - opencode/gpt-5.5 (medium)
    - opencode/kimi-k2.5
    - cloud:omniroute/kimi-k3

# Para agents de exploração (Explore, Librarian)
model:
  primary: opencode/gpt-5-nano
  fallback_chain:
    - github-copilot/claude-haiku-4.5
    - cloud:deepseek-v4-flash-free
```

### Regras de Model Rotation

1. **Nunca ter apenas 1 modelo sem fallback** — indisponibilidade de UM modelo não quebra o workflow
2. **Rotação em ordem declarada** — se primary falhar (offline, rate-limited, erro de API), vai para o próximo da cadeia
3. **Cloud é último recurso** — `cloud:<provider/modelo>` só após todas as opções locais falharem
4. **Registro obrigatório** — toda rotação é logada: `[Model-Fallback] Component: <nome> | Tried: <modelo> | Used: <fallback> | Reason: <motivo>`
5. **O mesmo princípio do escalonamento CRITICAL → nuvem**: o modelo primário pode ser local (Mi50 16GB), e se ele falha, a cadeia escala para nuvem sem interromper o pipeline
6. **Nunca hardcodar string única** — sempre structured: `model.primary` + `model.fallback_chain`

---

## 6. REGRAS DE CONSTRUÇÃO

### Para Agents

1. **Metadata completa** — Todos os campos obrigatórios preenchidos (incluindo capability manifest)
2. **Modelo específico com fallback** — `model.primary` + `model.fallback_chain`, nunca string única
3. **Modo definido** — subagent (preferencial) ou primary (só Gran-Mestre)
4. **Origem documentada** — `gran-mestre-original` ou `absorvido:<framework>` ou `crossover:<f1>+<f2>`
5. **Proveniência explícita** — Seção "Proveniência (crossover)" no corpo do documento
6. **Capacidades verificáveis** — `capabilities` listadas no manifest, cada uma demonstrável no código
7. **Regras claras** — O que faz E o que NÃO faz
8. **Máximo de ciclos** — Limite de tentativas definido
9. **Modo de operação** — Autônomo ou interativo

### Para Skills

1. **Trigger definido** — Comando que ativa a skill
2. **Fluxo claro** — Passos numerados e precisos
3. **Critérios de saída** — Quando o trabalho está "feito"
4. **Anti-patterns** — O que evitar
5. **Segurança** — Permissões e restrições

### Para Tools

1. **Parâmetros definidos** — Tipo, obrigatório, descrição
2. **Comportamento claro** — O que faz em detalhes
3. **Tratamento de erros** — Erros conhecidos e soluções
4. **Segurança** — Permissões e restrições

---

## 7. VALIDAÇÃO DE CONSTRUÇÃO

### Checklist de Validação

- [ ] Metadata completa (name, description, model, mode, origin)
- [ ] Model rotation definido (`model.primary` + `model.fallback_chain`)
- [ ] Modo definido (subagent preferencial, primary só Gran-Mestre)
- [ ] Origem documentada (`gran-mestre-original`, `absorvido:<f>`, `crossover:<f1>+<f2>`)
- [ ] Proveniência explícita (seção "Proveniência (crossover)" no corpo)
- [ ] Capability manifest presente (capabilities, complexity_range, cost, requires)
- [ ] Capacidades são verificáveis no código/skill
- [ ] Regras claras (o que faz + o que NÃO faz)
- [ ] Máximo de ciclos definido (para agents de validação)
- [ ] Modo de operação definido (autônomo ou interativo)
- [ ] Comandos documentados (para skills)
- [ ] Parâmetros definidos (para tools)
- [ ] Segurança documentada (permissões e restrições)

### Padrões de Qualidade

1. **Precisão** — Cada linha tem propósito claro
2. **Incisividade** — Sem ambiguidade
3. **Pragmatismo** — Funcionalidade real
4. **Conformidade** — Alinhado com o projeto
5. **Testabilidade** — Pode ser validado adversarialmente

---

## 8. EXEMPLO DE APLICAÇÃO

### Agent Héstia (v3 - Padrão)

```markdown
---
name: hestia
description: "Agente de validação do Gran-Mestre. Valida specs, planos e entregas contra o pedido original — nunca escreve ou revisa código, só audita conformidade."
model: github-copilot/claude-opus-4.7
mode: subagent
origin: gran-mestre-original
metadata:
  category: validation
  not_from: oh-my-openagent
  note: "Héstia NÃO existe no OmO — é invenção documentada do Gran-Mestre."
  version: 3.0.0
  author: Gran-Mestre
---

# Héstia — Guardiã da Conformidade

<Héstia description here>
```

---

## 9. REFERÊNCIAS

- **Superpowers:** 94% rejeição = qualidade extrema
- **Fable Method:** Verificação adversarial
- **OmO:** Infraestrutura madura
- **Gran-Mestre:** Meta-orquestrador

---

## 10. HELENIZAÇÃO — Conversão de Harness para OpenCode

### Definição

**Helenização** é o processo de converter tools, skills, agents ou MCPs de outros harnesses (Claude Code, Cursor, Codex, etc.) para o padrão OpenCode. O nome vem da adaptação cultural — absorver o que é útil e transformar na identidade OpenCode.

### Relação com Autofagia

A helenização é a **etapa 4** do processo de autofagia:

```
AUTOFAGIA (absorver) → HELENIZAÇÃO (converter) → INTEGRAR (usar)
```

Sem helenização, a autofagia produz código incompatível. Sem autofagia, a helenização não tem o que converter.

### Regra de Helenização

Ao absorver qualquer componente de outro harness, **SEMPRE** helenizar para o padrão OpenCode. Nunca copiar cegamente — sempre adaptar.

### Tabela de Helenização

| Harness Original | Helenização OpenCode |
|------------------|---------------------|
| Claude Code skill | OpenCode SKILL.md com metadata YAML |
| Claude Code agent | OpenCode agent .md com YAML frontmatter |
| Cursor rule | OpenCode skill ou AGENTS.md |
| Codex plugin | OpenCode MCP ou skill |
| Generic script | OpenCode tool com parâmetros definidos |

### Campos Obrigatórios na Helenização

1. **name** — Nome único em lowercase com hífens
2. **description** — Descrição precisa em 1-2 linhas
3. **model** — Modelo específico do harness OpenCode (não genérico)
4. **mode** — agent, subagent, tool, skill ou mcp
5. **origin** — Origem documentada (ex: claude-code-helenizado)
6. **metadata** — category, version, author

### Exemplo de Helenização

**Claude Code (original):**
```markdown
# My Skill
Description of skill
```

**OpenCode (helenizado):**
```markdown
---
name: my-skill
description: "Description of skill"
model: github-copilot/claude-opus-4.7
mode: skill
origin: claude-code-helenizado
metadata:
  category: utility
  version: 1.0.0
  author: Gran-Mestre (helenizado de Claude Code)
---

# My Skill
Description of skill
```

### pxpipe — Exemplo Real de Helenização

**Original:** https://github.com/teamchong/pxpipe (Node.js proxy)

**Helenizado:** ~/.opencode/skills/pxpipe/SKILL.md (OpenCode skill)

---

**Versão:** 2.0.0
**Data:** 2026-07-25
**Autor:** Gran-Mestre
**Helenização:** Conversão de harness para OpenCode (acoplada à autofagia)

<!--
UPDATES v2.0.0:
- Added Capability Manifest (section 2.1) — capabilities, complexity_range, cost, requires
- Added Model Rotation (section 2.1) — model.primary + model.fallback_chain
- Added Provenance Tracking (section 2.2) — origin prefix absorvido:/crossover:
- Updated Campos Obrigatórios table with new fields
- Updated Fallback Chains to structured model objects
- Added Regras de Model Rotation (section 5)
- Updated Regras de Construção (section 6) with provenance + capabilities
- Updated Checklist de Validação (section 7) with new items
-->