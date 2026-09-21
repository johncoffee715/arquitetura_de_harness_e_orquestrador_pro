# AUTOFAGIA COMPLETA — Templates Canônicos v2
## Data: 2026-07-25 | Fonte: /mnt/win1/123 tranqueiras e projetos/Nova pasta/

---

## 1. ARQUIVOS ABSORVIDOS

| Arquivo | Tamanho | Conceito-Chave |
|---------|---------|----------------|
| Template meta orquestrador senior.md | 239 linhas | Meta-orquestrador senior, core architecture, security layer |
| agent-registry.schema.json | 185 linhas | Schema JSON para registry canônico |
| agent-registry.example.json | 140 linhas | Exemplo real de registry |
| README-registry.md | 41 linhas | Como usar o registry |
| TEMPLATE-agent.md | 81 linhas | Template para agent primary |
| TEMPLATE-subagent.md | 67 linhas | Template para subagent |
| TEMPLATE-skill.md | 41 linhas | Template para skill |
| TEMPLATE-tool.md | 44 linhas | Template para tool |
| TEMPLATE-mcp.md | 45 linhas | Template para MCP |

---

## 2. CONCEITOS-CHAVE EXTRAÍDOS

### 2.1 Meta-Orquestrador Senior

**Campos únicos:**
- `seniority: senior` — confiável, autonomous como opção, escopo cross-project
- `core.context_analyzer` — regex-deterministic, extrai capabilities + complexity
- `core.capability_index` — greedy-cover sobre manifests
- `core.trace_context` — UUID4 propagado pelo DAG
- `security.shell_validator` — tokenize (nunca regex-on-raw-string)
- `security.retry_classifier` — categorized (nunca backoff uniforme)
- `cascade.supervisor_worker_split: inegociavel`
- `crossover.absorbed_from` — rastreabilidade de antropofagia

### 2.2 Registry Schema

**Campos obrigatórios por entry:**
- `id` — kebab-case único
- `tipo` — agent|subagent|tool|mcp|skill
- `nome` — nome legível
- `status` — ativo|legado|experimental|descontinuado
- `origem` — interno|framework-externo|fork-adaptado
- `proposito` — 1-2 frases
- `modelo` — primario, fallback, provider, vram
- `regras` — nao_faz (obrigatório, minItems: 1)
- `validacao` — gates, tdd_obrigatorio, fase_pipeline
- `autonomia` — modo_autonomo, condicoes

**Gates válidos:**
- safety-sha
- attestation-gate
- 2-action-rule
- 3-strike-protocol
- completion-gate
- tdd-obrigatorio
- review-por-linguagem
- nenhum

### 2.3 Supervisor/Worker Split (INEGOCIAVEL)

```
Supervisor (Atlas)  → NUNCA escreve código, só gerencia git e sequenciamento
Worker (Implementer) → NUNCA gerencia branch, só executa TDD task a task
```

### 2.4 Security Layer

```
shell_validator:
  strategy: tokenize          # shlex.split + allowlist + subprocess shell=False
  never: regex-on-raw-string  # vulnerável a expansion/quoting/subshell

retry_classifier:
  strategy: categorized       # nunca backoff uniforme
  categories: [transient, timeout, permission, not_found, logic,
               shell_rejected, health_skip, unknown]
  # permission/logic/shell_rejected NUNCA tem retry
```

---

## 3. GAPS IDENTIFICADOS

| Gap | Prioridade | Correção |
|-----|------------|----------|
| Registry não segue schema canônico | 🔴 CRÍTICA | Migrar para agent-registry.schema.json |
| Falta seniority no Gran-Mestre | 🔴 CRÍTICA | Adicionar seniority: senior |
| Falta core architecture | 🔴 CRÍTICA | Adicionar core.context_analyzer, capability_index, trace_context |
| Falta security layer | 🔴 CRÍTICA | Adicionar shell_validator, retry_classifier |
| Falta supervisor_worker_split | 🟡 MÉDIA | Documentar como inegociável |
| Falta crossover.absorbed_from | 🟡 MÉDIA | Rastrear antropofagia |

---

## 4. AÇÕES DE HELENIZAÇÃO

### 4.1 Atualizar Gran-Mestre para v4.0

Absorver TODOS os campos do Template meta orquestrador senior.

### 4.2 Migrar Registry para Schema Canônico

Criar novo agent-registry.json seguindo agent-registry.schema.json.

### 4.3 Atualizar TEMPLATE.md para v4.0

Incluir seção de registry canônico.

---

**Versão:** 1.0.0
**Data:** 2026-07-25
**Fonte:** /mnt/win1/123 tranqueiras e projetos/Nova pasta/