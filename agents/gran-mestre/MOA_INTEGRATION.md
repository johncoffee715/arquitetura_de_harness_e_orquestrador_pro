# MOA (Mixture of Agents) — Autofagia + Helenização
## Integração com Gran-Mestre Pipeline

**Data:** 2026-07-25
**Fonte:** https://github.com/togethercomputer/moa
**Status:** Autofagia completa + Obsidian cognition coupling + Serial→Parallel fix

---

## 1. O QUE É MOA

**MoA (Mixture of Agents)** é uma arquitetura que usa múltiplos LLMs em camadas para melhorar respostas. Conceito-chave:

```
┌─────────────────────────────────────────────────────────────┐
│                    MOA ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Reference Models (paralelo)                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Model A  │ │ Model B  │ │ Model C  │ │ Model D  │       │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       │
│       └─────────────┼─────────────┼─────────────┘           │
│                     ▼                                        │
│  Layer 2: Aggregator Model (síntese)                        │
│  ┌──────────────────────────────────────────────────┐       │
│  │ Aggregator: sintetiza respostas em output final   │       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## 2. CONCEITOS-CHAVE EXTRAÍDOS

### 2.1 Reference Models (Modelos de Referência)
- **Conceito:** Múltiplos LLMs geram respostas independentes
- **Benefício:** Diversidade de perspectivas
- **Paralelismo:** `asyncio.gather()` para execução concorrente

### 2.2 Aggregator Model (Modelo Agregador)
- **Conceito:** Um LLM sintetiza as respostas em output final
- **Benefício:** Refinamento e consolidação
- **Prompt:** Instrução para sintetizar criticamente

### 2.3 Layers (Camadas)
- **Conceito:** Múltiplas rodadas de refinamento
- **Benefício:** Cada camada melhora a resposta anterior
- **Configuração:** `layers = 3` (2 camadas de referência + 1 agregador)

### 2.4 Rate Limit Handling
- **Conceito:** Retry com backoff exponencial
- **Implementação:** `[1, 2, 4]` segundos entre tentativas
- **Benefício:** Resiliência contra limites de API

---

## 3. COMPARAÇÃO COM GRAN-MAESTRE

| Aspecto | MoA | Gran-Mestre |
|---------|-----|-------------|
| **Agentes** | N reference + 1 aggregator | 4 agents (Prometheus, Héstia, Atlas, Atena) |
| **Camadas** | N layers | 6 phases |
| **Paralelismo** | asyncio.gather | Task delegation |
| **Síntese** | Aggregator model | Atena (macro-review) |
| **Verificação** | Implicit | Fable Judge (adversarial) |
| **Gates** | Nenhum | 4 gates de aprovação |

## 4. O QUE ABSORVER DO MOA

### 4.1 Padrão de Execução Paralela ✅ ABSORVIDO
```python
# MoA pattern
results = await asyncio.gather(*[run_llm(model) for model in reference_models])

# Gran-Mestre adaptation
# Fase 4: Atlas pode delegar tasks em paralelo
```

### 4.2 Padrão de Agregação ✅ ABSORVIDO
```python
# MoA pattern
aggregator_system_prompt = """You have been provided with a set of responses...
Your task is to synthesize these responses into a single, high-quality response."""

# Gran-Mestre adaptation
# Atena: sintetiza revisões de múltiplos agents
```

### 4.3 Padrão Multi-Layer ✅ ABSORVIDO
```python
# MoA pattern
for _ in range(1, layers - 1):
    results = await asyncio.gather(*[run_llm(model, prev_response=results)])

# Gran-Mestre adaptation
# Fases 1-3: refinamento iterativo antes de execução
```

### 4.4 Rate Limit Handling ✅ ABSORVIDO
```python
# MoA pattern
for sleep_time in [1, 2, 4]:
    try:
        response = await async_client.chat.completions.create(...)
        break
    except RateLimitError:
        await asyncio.sleep(sleep_time)

# Gran-Mestre adaptation
# Model rotation: fallback chain com retry
```

---

## 5. INTEGRAÇÃO COM GRAN-MAESTRE

### 5.1 Fase 1 (Descoberta) — MoA Pattern
```
Prometheus → Reference Models (paralelo)
├── Model A: análise técnica
├── Model B: análise de requisitos
├── Model C: análise de riscos
└── Aggregator: síntese das análises
```

### 5.2 Fase 4 (Execução) — MoA Pattern
```
Atlas → Reference Models (paralelo)
├── Task 1: Implementação A
├── Task 2: Implementação B
├── Task 3: Implementação C
└── Aggregator: Atena (macro-review)
```

### 5.3 Fase 5 (Revisão Macro) — MoA Pattern
```
Atena → Reference Models (paralelo)
├── Reviewer 1: coerência
├── Reviewer 2: acoplamento
├── Reviewer 3: arquitetura
└── Aggregator: síntese das revisões
```

---

## 6. IMPLEMENTAÇÃO

### 6.1 Configuração MoA no Gran-Mestre

```json
{
  "gran-mestre": {
    "moa": {
      "enabled": true,
      "layers": 3,
      "reference_models": [
        "github-copilot/claude-opus-4.7",
        "github-copilot/gpt-5.5",
        "opencode/gemini-3.1-pro"
      ],
      "aggregator_model": "github-copilot/claude-opus-4.7",
      "parallel_execution": true,
      "rate_limit_retry": [1, 2, 4]
    }
  }
}
```

### 6.2 Padrão de Execução Paralela

```python
import asyncio

async def run_moa_phase(tasks, models):
    """Executa tasks em paralelo usando padrão MoA."""
    results = await asyncio.gather(*[
        execute_task(task, model) 
        for task, model in zip(tasks, models)
    ])
    return aggregate_results(results)
```

---

## 7. BENEFÍCIOS DA INTEGRAÇÃO

| Benefício | Descrição |
|-----------|-----------|
| **Diversidade** | Múltiplos modelos geram perspectivas diferentes |
| **Qualidade** | Agregação melhora output final |
| **Resiliência** | Fallback entre modelos |
| **Paralelismo** | Execução concorrente eficiente |
| **Refinamento** | Multi-layer para qualidade progressiva |

---

## 8. OBSIDIAN COGNITION COUPLING (Ressalva)

### 8.1 Shared Brain — Mecanismo Atual

O Gran-Mestre arquiva memória em um vault Obsidian em `/mnt/dados/cerebro com IA/`:

```
/mnt/dados/cerebro com IA/
├── wiki/                          # Conhecimento estruturado
│   ├── agentes/                   # Documentação de agentes
│   ├── projetos/                  # Contexto de projetos
│   ├── decisoes/                  # Decisões arquiteturais
│   └── padroes/                   # Padrões descobertos
├── textos, pdf e esquemas/        # Documentos originais
├── diarios/                       # Logs de pipeline (YYYY-MM-DD/)
├── aprendizados/                  # Lições aprendidas
│   ├── sucessos/
│   ├── falhas/
│   └── insights/
└── templates/                     # Templates reutilizáveis
```

A integração entre MoA e Obsidian segue o padrão:

```
Pipeline completo
  → Gran-Mestre sintetiza (MoA aggregator)
  → Extrai decisões e aprendizados
  → Arquiva no vault Obsidian (camada fria)
  → Disponível para consulta humana via Graph View
```

### 8.2 4 Riscos Concretos do Acoplamento Cognitivo

O vault Obsidian é excelente como **camada fria** (arquivamento), mas tem 4 riscos se o pipeline passar a **depender** dele durante a execução:

| # | Risco | Descrição | Mitigação |
|---|-------|-----------|-----------|
| 1 | **Sem lock/transação** | Markdown é arquivo puro — duas execuções paralelas (ou Team Mode) escribendo no mesmo `wiki/` podem colidir | Escrever no vault só após a fase, nunca no meio. Usar arquivos temporários + mv atômico. |
| 2 | **Sem validação de schema** | Frontmatter YAML solto — campo errado ou faltando corrompe consulta Dataview silenciosamente | Script de validação de frontmatter antes de escrever. Template fixo com checklist. |
| 3 | **Desempenho degrada com o vault** | Busca full-text e Dataview ficam mais lentos conforme diarios/ cresce — aceitável para consulta humana, ruim no meio de decisão sob latência | Manter a memória de trabalho (CONTEXT.md, SHA, estado de rota) fora do vault. Obsidian só para pós-pipeline. |
| 4 | **Sync + escrita concorrente** | Obsidian Sync ativo enquanto pipeline escreve = merge collision | Desabilitar sync durante escrita programática, ou usar lock file. |

### 8.3 Fronteira Quente vs Fria (Recomendação)

```
╔═══════════════════════════════════════════════════════════════╗
║              FRONTEIRA DE TEMPERATURA DA MEMÓRIA              ║
╠═══════════════════════════════════════════════════════════════╣
║  MEMÓRIA QUENTE (durante execução)                            ║
║  ├── CONTEXT.md (estado atual)                                ║
║  ├── SHA do repositório (safety)                               ║
║  ├── Decisão de rota (TRIVIAL→FEATURE)                        ║
║  └── Estado dos gates (APPROVED/BLOCKED)                      ║
║  Local: ~/.config/opencode/agents/gran-mestre/                 ║
║  Formato: Markdown + arquivos temporários                      ║
╠═══════════════════════════════════════════════════════════════╣
║  MEMÓRIA FRIA (após pipeline)                                  ║
║  ├── Relatório final                                          ║
║  ├── Decisões arquiteturais                                   ║
║  ├── Aprendizados (sucessos, falhas, insights)                ║
║  ├── Padrões descobertos                                      ║
║  └── Contexto de projeto                                      ║
║  Local: /mnt/dados/cerebro com IA/ (vault Obsidian)            ║
║  Formato: Markdown + YAML frontmatter + Dataview queries       ║
╚═══════════════════════════════════════════════════════════════╝
```

### 8.4 Integração MoA + Obsidian

```
Fase 6 (Entrega) completa
  → Gran-Mestre (MoA aggregator) sintetiza:
  │  ┌──────────────────────────────────┐
  │  │ Héstia: validação final          │
  │  │ Atena: revisão macro             │
  │  │ Fable Judge: veredito adversarial │
  │  └──────────┬───────────────────────┘
  │             ↓ MoA paralelo + síntese
  │   Estado final: DELIVERED/ROLLBACK/ESCALATE
  ↓
Gran-Mestre decide:
  ├── Se DELIVERED → arquivar no Obsidian
  │   ├── diarios/YYYY-MM-DD/pipeline-{id}.md
  │   ├── wiki/decisoes/{feature}.md
  │   └── aprendizados/{categoria}/{feature}.md
  └── Se ROLLBACK/ESCALATE → registrar falha
      └── aprendizados/falhas/{feature}.md
```

---

## 9. SERIAL TO PARALLEL VALIDATION FIX

### 9.1 Problema: Validação Serial

O pipeline original executava validações em série nas fases com múltiplos filtros:

```
Fase 2: Spec → Héstia → (espera) → Fable Judge → (espera) → Gate 2
Fase 5: Diff → Atena → (espera) → Fable Judge → (espera) → Gate pre-Fase 6
Fase 6: Entrega → Verification → (espera) → Héstia → (espera) → Fable Judge → Gate 4
```

**Custo:** 3x o tempo de inferência — cada filtro espera o anterior terminar.

### 9.2 Solução: MoA Parallel Validation

Com MoA, os filtros rodam **em paralelo** e o Gran-Mestre sintetiza:

```
Fase 2: Spec → ┌──────────┐
                │ Héstia   │ (paralelo)
                │ Fable    │ (paralelo)
                └────┬─────┘
                     ↓
              Gran-Mestre (aggregador)
              → Estado: APPROVED / NEEDS_CORRECTION / BLOCKED

Fase 5: Diff → ┌──────────┐
                │ Atena    │ (paralelo)
                │ Fable    │ (paralelo)
                └────┬─────┘
                     ↓
              Gran-Mestre (aggregador)
              → Estado: DELIVERED / ROLLBACK / ESCALATE

Fase 6: Entrega → ┌──────────────┐
                   │ Verification │ (paralelo)
                   │ Héstia       │ (paralelo)
                   │ Fable Judge  │ (paralelo)
                   └──────┬───────┘
                          ↓
                   Gran-Mestre (aggregador)
                   → Estado: DELIVERED / ROLLBACK / ESCALATE
```

### 9.3 Implementação

```python
import asyncio

async def parallel_validation(artifact, filters):
    """Executa filtros em paralelo (MoA) e sintetiza resultado."""
    
    # Passo 1: Rodar filtros em paralelo
    results = await asyncio.gather(*[
        run_filter(f, artifact) for f in filters
    ])
    
    # Passo 2: Gran-Mestre sintetiza (aggregator)
    # Sem custo extra de modelo — é o Gran-Mestre quem já recebe o resultado
    final_state = synthesize_verdicts(results)
    
    return final_state
```

### 9.4 Limitação Real (GPU Única)

O ganho de latência do MoA **só se realiza** quando pelo menos um dos proposers é chamada de nuvem:

| Cenário | Filtros | Ganho Real |
|---------|---------|------------|
| Todos locais (mesma GPU Mi50) | 3x Héstia local | ❌ Mínimo — GPU processa em fila |
| 2 locais + 1 nuvem (OmniRoute) | Héstia + Atena local + Fable Judge nuvem | ✅ ~2x — nuvem roda em paralelo |
| Todos nuvem (modelos diferentes) | 3 APIs diferentes | ✅ ~3x — paralelo real |

### 9.5 Comparação Antes vs Depois

| | Antes (Serial) | Depois (MoA Paralelo) |
|---|---|---|
| **Tempo Fase 2** | 3x latência de inferência | ~1x + síntese barata |
| **Tempo Fase 5** | 2x latência de inferência | ~1x + síntese barata |
| **Tempo Fase 6** | 3x latência de inferência | ~1x + síntese barata |
| **Rigor** | 3 ângulos, 3 origens | Mesmo rigor, menos tempo |
| **Agregador** | Nenhum (resultado parcial) | Gran-Mestre (visão holistic) |
| **Custo de implementação** | Já existia | Padrão sobre OmniRoute, zero novas dependências |

---

## 10. PRÓXIMOS PASSOS

### Implementação Imediata
1. **Aplicar fronteira Obsidian** — garantir que NENHUM agente leia o vault como parte do caminho crítico de decisão. Memória quente (CONTEXT.md, SHA) fora do vault. Obsidian exclusivamente como camada fria pós-pipeline.
2. **Implementar validação paralela (MoA)** nas fases 2, 5 e 6 — substituir chamadas seriais por `asyncio.gather()` com síntese do Gran-Mestre.
3. **Configurar reference models** no omni-route para suportar proposers em nuvem paralelos aos locais.

### Médio Prazo
4. **Medir ganho real de latência** — comparar serial vs MoA com pelo menos 1 proposer em nuvem. A ressalva da GPU única (Mi50) significa que MoA com 3 proposers locais não ganha latência real.
5. **Documentar padrão MoA** no TEMPLATE.md como técnica de orquestração (não dependência) — seção de padrões de execução paralela.
6. **Implementar validação de schema** para frontmatter do vault Obsidian — evitar corrupção silenciosa de consultas Dataview.

### Longo Prazo
7. **Avaliar lock/transação** para escrita concorrente no vault (Team Mode com múltiplos membros paralelos).
8. **Dashboard de métricas** de aceitação MoA por fase (acceptance rate tracking).

---

**Versão:** 2.0.0
**Data:** 2026-07-25
**Autor:** Gran-Mestre (autofagia de MoA + Obsidian Cognition Coupling + Parallel Validation Fix)