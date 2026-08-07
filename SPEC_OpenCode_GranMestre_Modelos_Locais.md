# SPEC — OpenCode Harness: Orquestração de Modelos Locais com Meta-Orquestrador Gran-Mestre
## v1.0.0 — Agosto 2026
### Autor: Sistema de Especificação Técnica OpenCode
### Status: RASCUNHO → REQUER APROVAÇÃO GATE 1

---

## 1. RESUMO EXECUTIVO

Este documento define a alocação estratégica de quatro modelos de linguagem locais (LLMs) em um workflow de seis fases de desenvolvimento de software assistido por IA, operando dentro do harness **OpenCode**. O objetivo é criar um sistema de **antropofagia tecnológica** — onde tecnologias externas são devoradas criticamente, quantitativamente e qualitativamente — e **helenização** — onde essas tecnologias são convertidas ao padrão OpenCode através de uma metanoia arquitetural.

O **Meta-Orquestrador Gran-Mestre** é o agente único de entrada que orquestra todos os subagentes, plugins, hooks, skills, MCPs, tool callings e LSPs, unificando-os sob uma única interface cognitiva.

A **cognição neurológica no Obsidian** serve como camada de memória cerebral persistente, acoplada ao workflow para auto-aprendizado, auto-cura e rastreabilidade de decisões.

---

## 2. MATRIZ DE MODELOS — PERFIL TÉCNICO COMPLETO

### 2.1 Ornith-1.0 9B (Q4_K_M)
| Atributo | Valor |
|----------|-------|
| **Parâmetros** | 9B Dense |
| **Contexto** | 256K tokens |
| **Licença** | MIT (comercial + research) |
| **Quantização** | Q4_K_M (~5-6GB VRAM) |
| **Base** | Qwen 3.5 / Gemma 4 |
| **SWE-Bench Verified** | 69.4 |
| **Terminal-Bench 2.1** | 43.1 |
| **Ranking Agentic** | #67 de 132 |
| **Ranking Coding** | #75 de 132 |
| **Inovação** | Self-scaffolding: aprende a gerar seus próprios harnesses durante RL |
| **Modo Raciocínio** | Explícito (adiciona latência e tokens) |
| **VRAM Estimada** | ~6GB (Q4_K_M) / ~19GB (bf16) |
| **Latência** | Média-Alta (devido ao raciocínio explícito) |
| **Throughput** | ~50-80 tok/s (GPU) |

**Perfil de Uso:** Coding agentic, geração de scaffolds, orquestração complexa, tarefas que exigem raciocínio multi-step em código.

**Limitações:** Não é o melhor em tool calling puro; o self-scaffolding pode gerar overhead de tokens; latência alta para tarefas simples.

---

### 2.2 Nanbeige 3B (4-bit GGUF/EXL2)
| Atributo | Valor |
|----------|-------|
| **Parâmetros** | 3B |
| **Contexto** | 131K tokens |
| **Quantização** | Q4_0 / Q4_K_M / EXL2 (~2-3GB VRAM) |
| **LiveCodeBench-V6** | 76.9 |
| **AIME 2026** | 87.4 |
| **GPQA** | 83.8 |
| **Arena-Hard-v2** | 73.2 |
| **BFCL-V4 (Tool Use)** | 56.5 |
| **Deep Search** | 69.9 |
| **Tool Chain Sustentada** | 500+ rounds |
| **VRAM Estimada** | ~2-3GB |
| **Latência** | Baixa |
| **Throughput** | ~150-300 tok/s (GPU) / ~30-50 tok/s (CPU) |

**Perfil de Uso:** Raciocínio rápido, tool calling, deep search, agentic workflows leves, edge deployment, tarefas que exigem resposta imediata.

**Limitações:** 3B é limite para tasks muito complexas; pode alucinar em contextos >64K sem gerenciamento ativo; tool calling cai em cadeias >200 rounds sem checkpoint.

---

### 2.3 Bonsai 27B 1-bit
| Atributo | Valor |
|----------|-------|
| **Parâmetros** | 27B |
| **Arquitetura** | BitNet b1.58 (ternária: -1, 0, 1) |
| **Tamanho** | ~3.9-4.0GB |
| **Contexto** | 32K-64K (depende da implementação) |
| **Overall Benchmark** | 76.1 |
| **Math** | 91.7 |
| **Coding** | 81.9 |
| **Tool-calling** | 66.0 (queda de -17.5% vs baseline) |
| **DSpark** | Speculative decoding incluso (+37% speedup em CUDA) |
| **VRAM Estimada** | ~4GB (CPU) / ~6GB (GPU com overhead) |
| **Latência** | Média (11 tok/s em iPhone 17 Pro Max, 44 tok/s em M5 Pro) |
| **Throughput** | ~44 tok/s (Apple M5 Pro) / ~104-144 tok/s (H100 com DSpark) |

**Perfil de Uso:** Geração de texto longo, summarization, análise documental, raciocínio matemático, coding assistido (não agentic complexo), deploy em hardware limitado.

**Limitações:** Tool calling degradado (-17.5%); não ideal para agentic workflows multi-step; precisão numérica reduzida em tasks que exigem exatidão de parâmetros; pode variar em qualidade em gerações longas.

---

### 2.4 LFM 2.5-1.6B (FP8)
| Atributo | Valor |
|----------|-------|
| **Parâmetros** | 1.6B (1.2B backbone + 400M vision encoder) |
| **Contexto** | 32K tokens |
| **Formatos** | GGUF, MLX, ONNX |
| **Quantização** | FP8 / Q4 / Q8 |
| **Modalidades** | Texto + Visão (multimodal) |
| **Resolução Imagem** | 512x512 nativo, tiling para maiores |
| **Idiomas** | EN, AR, ZH, FR, DE, JA, KO, ES |
| **VRAM Estimada** | ~1-2GB |
| **Latência** | Muito Baixa |
| **Throughput** | ~500+ tok/s (GPU) / ~100+ tok/s (CPU) |

**Perfil de Uso:** OCR, compreensão documental, classificação rápida, extração de entidades, respostas imediatas, tasks visuais, fallback universal.

**Limitações:** Não é para knowledge-intensive tasks; contexto limitado a 32K; performance de coding limitada; não é reasoning-heavy.

---

## 3. ARQUITETURA DO HARNESS — VISÃO GERAL

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    META ORQUESTRADOR GRAN-MASTRE                        │
│  (Ornith-1.0 9B — Orquestração, Decisão Estratégica, Contratos)       │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  FASE 1     │  │  FASE 2     │  │  FASE 3     │  │  FASE 4-6   │  │
│  │ Descoberta  │  │ Contrato    │  │ Plano       │  │ Exec-Rev-   │  │
│  │             │  │             │  │             │  │ Entrega     │  │
│  │ Nanbeige 3B │  │ Ornith 9B   │  │ Ornith 9B   │  │ Bonsai 27B  │  │
│  │ LFM 1.6B    │  │ Nanbeige 3B │  │ Nanbeige 3B │  │ Nanbeige 3B │  │
│  │             │  │             │  │             │  │ Ornith 9B   │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│  COGNIÇÃO NEUROLÓGICA — Obsidian Vault (Memória Cerebral Persistente) │
│  • GraphRAG de decisões                                               │
│  • Memória episódica (sessões)                                        │
│  • Memória semântica (conceitos, padrões)                             │
│  • Memória procedural (workflows, skills)                             │
│  • Auto-cura (detecção de drift, correção de skills)                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---
## 4. FASE 1 — DESCOBERTA

### 4.1 >>> Ideias (filtro)
**Modelo Designado:** **Nanbeige 3B** (primário) + **LFM 2.5-1.6B** (secundário/OCR)

**Justificativa Técnica:**
A fase de geração de ideias exige **velocidade**, **divergência criativa** e **baixo custo computacional**. Nanbeige 3B, apesar de compacto, demonstra performance de reasoning superior a modelos 30B+ em benchmarks como Arena-Hard-v2 (73.2 vs 56.0 do Qwen3-32B). Sua capacidade de deep search (69.9) permite explorar domínios desconhecidos rapidamente. O LFM 1.6B atua como scanner de documentos, imagens e referências visuais que alimentam o brainstorm.

**Implementação Prática:**
```yaml
# .opencode/agents/discovery_ideation.yaml
agent:
  name: "DiscoveryIdeator"
  model: "nanbeige-3b-q4"
  temperature: 0.8
  top_p: 0.95
  max_tokens: 4096
  system_prompt: |
    Você é um agente de descoberta de ideias. Sua função é:
    1. Gerar N alternativas de solução para o problema apresentado
    2. Para cada alternativa, listar: viabilidade técnica, riscos, sinergias
    3. Aplicar filtros de negócio: ROI, tempo, complexidade
    4. Nunca propor apenas uma solução — sempre divergir primeiro
    
    Use o formato de saída estruturado (YAML) para cada ideia.
    
  tools:
    - name: "web_search"
      enabled: true
    - name: "document_scan"
      model: "lfm-2.5-1.6b"
      enabled: true
  
  memory:
    type: "obsidian_episodic"
    vault_path: "./brain/discovery/"
```

**Prós:**
- Velocidade de inferência 10x superior a modelos 9B+
- Custo energético mínimo (~0.1 mWh/token)
- Capacidade de 500+ rounds de tool use para exploração profunda

**Contras:**
- Pode alucinar em domínios muito técnicos sem contexto adequado
- Não gera código de produção diretamente

**Riscos:**
- **MÉDIO:** Over-exploration — o modelo pode gerar muitas ideias irrelevantes se o filtro de negócio não for rigoroso
- **BAIXO:** Hallucination em facts — mitigado pelo web_search tool

**Benefícios:**
- Brainstorm em <5 segundos por ideia
- Divergência controlada com filtros automáticos
- Integração com documentos visuais via LFM

**Impacto Técnico:**
- **Modularidade:** ALTA — agente isolado, substituível
- **Escalabilidade:** ALTA — pode rodar N instâncias em paralelo
- **Observabilidade:** ALTA — cada ideia é logada com proveniência

**Classificação:** **CRÍTICA** — Sem descoberta eficiente, todo o pipeline falha.

---

### 4.2 >>> Definição de Escopo (filtro)
**Modelo Designado:** **Nanbeige 3B** (primário) + **Ornith-1.0 9B** (validador)

**Justificativa Técnica:**
A definição de escopo exige **raciocínio estruturado** e **alinhamento com constraints**. Nanbeige 3B mantém coerência em cadeias de raciocínio longas (prova: 87.4 em AIME 2026). Ornith-1.0 9B atua como validador cruzado, aplicando seu modo de raciocínio explícito para verificar se o escopo proposto é tecnicamente viável e se não há ambiguidades ocultas.

**Implementação Prática:**
```python
# plugins/scope_definer.py
class ScopeDefiner:
    def __init__(self):
        self.primary = ModelRouter("nanbeige-3b-q4")
        self.validator = ModelRouter("ornith-1.0-9b-q4km")
        
    def define_scope(self, ideas: list[dict]) -> dict:
        # Fase 1: Nanbeige estrutura o escopo
        scope_draft = self.primary.generate(
            prompt=self._build_scope_prompt(ideas),
            temperature=0.4,  # Baixa para precisão
            tools=["constraint_checker", "dependency_analyzer"]
        )
        
        # Fase 2: Ornith valida com raciocínio explícito
        validation = self.validator.generate(
            prompt=self._build_validation_prompt(scope_draft),
            temperature=0.2,
            reasoning_mode="explicit",  # Ativa self-scaffolding
            max_tokens=8192
        )
        
        # Merge: reconciliação de conflitos
        return self._merge_scope(scope_draft, validation)
```

**Prós:**
- Dupla verificação elimina ambiguidades prematuras
- Ornith detecta edge cases que Nanbeige pode ignorar

**Contras:**
- Latência adicional de ~3-5s pela validação
- Custo de tokens dobrado

**Riscos:**
- **BAIXO:** Divergência entre modelos — mitigado pelo algoritmo de merge
- **MÉDIO:** Ornith pode ser excessivamente conservador em modo explícito

**Classificação:** **CRÍTICA** — Escopo mal definido = retrabalho nas fases 4-6.

---

### 4.3 >>> Remover Ambiguidade (filtro)
**Modelo Designado:** **Ornith-1.0 9B** (primário)

**Justificativa Técnica:**
A remoção de ambiguidade é uma tarefa de **análise profunda** e **raciocínio crítico**. Ornith-1.0 9B, com seu self-scaffolding, é treinado para gerar harnesses que guiam soluções. Isso significa que ele naturalmente decompõe problemas ambíguos em sub-problemas claros, gerando scaffolds de resolução.

**Implementação Prática:**
```yaml
# skills/disambiguation/SKILL.md
# Antropofagia: adaptado de técnicas de prompt engineering do Claude Code

skill: "AmbiguityRemover"
description: "Remove ambiguidades de requisitos usando self-scaffolding"
model: "ornith-1.0-9b-q4km"
steps:
  1:
    action: "generate_harness"
    description: "Ornith gera um harness de análise para o problema"
    output_format: "yaml"
  2:
    action: "apply_harness"
    description: "Aplica o harness para decompor o problema"
    output_format: "structured_questions"
  3:
    action: "validate_clarity"
    description: "Verifica se cada sub-problema tem critério de aceitação mensurável"
    gate: "clarity_score > 0.85"
  4:
    action: "output_spec"
    description: "Gera spec de ambiguidade resolvida"
    format: "markdown"
```

**Prós:**
- Self-scaffolding gera estruturas de análise customizadas por problema
- 256K contexto permite análise de documentos extensos

**Contras:**
- Modo explícito adiciona ~20-30% de tokens
- Pode ser overkill para problemas triviais

**Riscos:**
- **MÉDIO:** Over-engineering do harness — mitigado por timeout de 30s
- **BAIXO:** Latência inaceitável para usuários impacientes

**Classificação:** **IMPORTANTE** — Pode ser substituído por Nanbeige 3B em projetos simples.

---

### 4.4 >>> Decomposição Leve (contexto, não camisa-de-força) (filtro)
**Modelo Designado:** **Nanbeige 3B** (primário)

**Justificativa Técnica:**
Decomposição leve exige **velocidade** e **adaptabilidade**. Nanbeige 3B, com sua capacidade de sustentar 500+ rounds de tool invocations, pode decompor iterativamente sem perder contexto. A "leveza" vem da velocidade — decomposições que levariam 10s com Ornith levam <2s com Nanbeige.

**Implementação Prática:**
```python
# hooks/pre_decomposition.py
@hook("pre_decomposition")
def light_decompose(context: Context) -> Decomposition:
    """
    Decomposição leve: quebra em 3-7 tasks, nunca mais.
    Cada task deve ter: descrição, critério de aceitação, dependências.
    """
    model = ModelRouter("nanbeige-3b-q4")
    
    # Estratégia: decompor em waves
    wave1 = model.decompose(context.scope, max_items=5, depth=1)
    
    # Verificar se há tasks > 8h de trabalho — se sim, decompor mais
    for task in wave1:
        if task.estimated_effort > "8h":
            subtasks = model.decompose(task, max_items=3, depth=1)
            task.subtasks = subtasks
    
    return wave1
```

**Prós:**
- Sub-2s de latência
- Iterativo e adaptativo
- Não impõe arquitetura prematura

**Contras:**
- Pode decompor insuficientemente em domínios desconhecidos
- Requer validação humana para tasks críticas

**Classificação:** **CRÍTICA** — Decomposição é o alicerce do planejamento.

---

### 4.5 >>> O Loop em um Pedido em Brainstorm de Agents (filtro)
**Modelo Designado:** **Nanbeige 3B** (primário) + **Bonsai 27B** (síntese/escrita)

**Justificativa Técnica:**
O loop de brainstorm de agents exige **divergência rápida** (Nanbeige) seguida de **síntese coerente** (Bonsai). Bonsai 27B, apesar da queda em tool calling, mantém excelente performance em geração de texto e summarization. Ele consolida as ideias divergentes em narrativas coesas.

**Implementação Prática:**
```yaml
# .opencode/workflows/brainstorm_loop.yaml
workflow:
  name: "AgentBrainstormLoop"
  iterations: 3
  agents:
    - name: "Diverger"
      model: "nanbeige-3b-q4"
      role: "Gera 5 alternativas por iteração"
      temperature: 0.9
    - name: "Synthesizer"  
      model: "bonsai-27b-1bit"
      role: "Consolida alternativas em proposta unificada"
      temperature: 0.5
    - name: "Critic"
      model: "nanbeige-3b-q4"
      role: "Critica a síntese e propõe gaps"
      temperature: 0.6
  
  convergence_criteria:
    - "Score de coerência > 0.8"
    - "Nenhum gap crítico não endereçado"
    - "Cobertura de requisitos > 95%"
```

**Prós:**
- Loop convergente em 3 iterações
- Nanbeige gera ideias em <1s cada
- Bonsai sintetiza sem perder nuances

**Contras:**
- Bonsai pode ser lento em CPU (~11 tok/s em mobile)
- Requer sincronização entre agentes

**Classificação:** **IMPORTANTE** — Pode ser simplificado para 1 iteração em projetos pequenos.

---

### 4.6 ⏸️ GATE 1: Usuário Aprova a Direção
**Modelo Designado:** **LFM 2.5-1.6B** (pré-processamento) + **Ornith-1.0 9B** (apresentação)

**Justificativa Técnica:**
O Gate 1 é um ponto de decisão humana, mas os modelos preparam o material. LFM 1.6B extrai e resume documentos de referência. Ornith 9B gera a apresentação estruturada com raciocínio explícito, mostrando por que a direção escolhida é a melhor.

**Classificação:** **CRÍTICA** — Gate humano é inegociável.

---
## 5. FASE 2 — CONTRATO

### 5.1 >>> Transforma Direção Aprovada em Design Doc (filtro)
**Modelo Designado:** **Ornith-1.0 9B** (primário) + **Nanbeige 3B** (pesquisa técnica)

**Justificativa Técnica:**
Design doc exige **arquitetura**, **coerência** e **raciocínio estruturado**. Ornith 9B, com seu self-scaffolding, gera documentos de design que incluem: diagramas de arquitetura (em Mermaid), decisões técnicas com trade-offs, e contratos de interface. Nanbeige 3B pesquisa padrões e referências técnicas em paralelo.

**Implementação Prática:**
```markdown
# AGENTS.md — Design Doc Contract
## Design Doc Template (gerado por Ornith-1.0 9B)

### 1. Visão
[Ornith gera em modo explícito, justificando cada decisão]

### 2. Arquitetura
```mermaid
[Diagrama gerado por Ornith com validação de sintaxe]
```

### 3. Decisões Técnicas
| Decisão | Alternativas | Trade-offs | Justificativa |
|---------|-------------|------------|---------------|
| [Auto]  | [Auto]      | [Auto]     | [Ornith]      |

### 4. Contratos de Interface
```yaml
[OpenAPI specs geradas por Nanbeige + validadas por Ornith]
```

### 5. Riscos e Mitigações
[Ornith aplica análise de risco com 256K contexto]
```

**Prós:**
- Documento auto-contido e auditável
- Raciocínio explícito torna decisões reversíveis

**Contras:**
- Design doc pode ficar extenso (>10K tokens)
- Requer revisão humana para decisões de arquitetura

**Riscos:**
- **MÉDIO:** Over-specification — mitigado por template que limita seções
- **BAIXO:** Decisões baseadas em conhecimento desatualizado

**Classificação:** **CRÍTICA** — Contrato é a lei do projeto.

---

### 5.2 >>> Cria Especificação spec.md (filtro)
**Modelo Designado:** **Ornith-1.0 9B** (primário)

**Justificativa Técnica:**
spec.md é o documento mais crítico do projeto. Ornith 9B, com sua capacidade de gerar harnesses, cria specs que são **executáveis** — incluindo: critérios de aceitação mensuráveis, testes de aceitação em Gherkin, e contratos de API. O self-scaffolding garante que o spec seja completo e não omita edge cases.

**Implementação Prática:**
```python
# skills/spec_writer/SKILL.md
class SpecWriter:
    model = "ornith-1.0-9b-q4km"
    
    def write_spec(self, design_doc: dict) -> str:
        harness = self.model.generate_harness(design_doc)
        spec = self.model.apply_harness(harness, design_doc)
        
        # Garantir que cada requisito tem teste de aceitação
        for req in spec.requirements:
            req.acceptance_test = self.model.generate_gherkin(req)
            
        return spec.to_markdown()
```

**Classificação:** **CRÍTICA** — spec.md é o contrato legal do código.

---

### 5.3 >>> Valida spec contra o pedido original (filtro)
**Modelo Designado:** **Nanbeige 3B** (primário)

**Justificativa Técnica:**
Validação exige **comparação**, **raciocínio lógico** e **detecção de gaps**. Nanbeige 3B, com sua performance em alignment (73.2 Arena-Hard-v2), é excelente em detectar quando um spec não atende ao pedido original. Sua velocidade permite validação em <2s.

**Implementação Prática:**
```python
def validate_spec(spec: str, original_request: str) -> ValidationReport:
    model = ModelRouter("nanbeige-3b-q4")
    
    # Comparação semântica
    alignment_score = model.compare_semantic(spec, original_request)
    
    # Detecção de gaps
    gaps = model.detect_gaps(spec, original_request)
    
    # Verificação de critérios mensuráveis
    measurability = model.check_measurability(spec)
    
    return ValidationReport(
        alignment=alignment_score,
        gaps=gaps,
        measurability=measurability,
        pass_threshold=0.9
    )
```

**Classificação:** **CRÍTICA** — Validação falha = retrabalho massivo.

---

### 5.4 >>> Audita o Resultado Pronto em Brainstorm de Agents (filtro)
**Modelo Designado:** **Nanbeige 3B** (primário) + **Ornith-1.0 9B** (auditor de arquitetura)

**Justificativa Técnica:**
Auditoria de contrato requer **múltiplas perspectivas**. Nanbeige verifica alinhamento com requisitos de negócio. Ornith verifica coerência técnica e detecta anti-padrões arquiteturais.

**Classificação:** **IMPORTANTE** — Pode ser simplificado em projetos pequenos.

---

### 5.5 >>> Preservar o Contexto
**Modelo Designado:** **Sistema de Memória** (Obsidian + GraphRAG)

**Justificativa Técnica:**
A preservação de contexto entre fases é crítica. O Obsidian Vault atua como **memória episódica** (sessões), **semântica** (conceitos) e **procedural** (workflows). Cada decisão da Fase 2 é persistida como nota atômica com links bidirecionais.

**Implementação Prática:**
```yaml
# .opencode/memory/obsidian_config.yaml
memory:
  type: "obsidian_graphrag"
  vault_path: "./brain/"
  
  layers:
    episodic:
      path: "./brain/episodic/"
      format: "session_{timestamp}.md"
      retention: "permanent"
    semantic:
      path: "./brain/semantic/"
      format: "concept_{hash}.md"
      embedding_model: "nanbeige-3b-q4"  # Fast embeddings
    procedural:
      path: "./brain/procedural/"
      format: "skill_{name}.md"
      auto_update: true
  
  graphrag:
    enabled: true
    resolution_strategy: "conflict_merge"  # Resolve conflitos entre memórias
    decay_factor: 0.01  # Memórias antigas perdem relevância lentamente
```

**Classificação:** **CRÍTICA** — Sem memória, o sistema é stateless e perde aprendizado.

---

### 5.6 ⏸️ GATE 2: Usuário Aprova o spec
**Modelo Designado:** **Ornith-1.0 9B** (apresentação) + **LFM 1.6B** (OCR de anexos)

**Classificação:** **CRÍTICA** — Gate humano inegociável.

---

## 6. FASE 3 — PLANO

### 6.1 >>> TDD, Tasks Bite-Sized, Código Completo (filtro)
**Modelo Designado:** **Ornith-1.0 9B** (primário) + **Nanbeige 3B** (decomposição de tasks)

**Justificativa Técnica:**
TDD (Test-Driven Development) exige **raciocínio invertido** — escrever o teste antes do código. Ornith 9B, com sua performance em coding (69.4 SWE-Bench Verified), é capaz de gerar testes de aceitação e unitários antes da implementação. Nanbeige 3B decompõe em tasks bite-sized (<30 min cada).

**Implementação Prática:**
```python
# skills/tdd_orchestrator/SKILL.md
class TDDOrchestrator:
    primary = ModelRouter("ornith-1.0-9b-q4km")
    decomposer = ModelRouter("nanbeige-3b-q4")
    
    def plan_tdd(self, spec: Spec) -> TaskPlan:
        # Fase 1: Ornith gera testes de aceitação
        acceptance_tests = self.primary.generate_tests(spec, type="acceptance")
        
        # Fase 2: Nanbeige decompõe em tasks
        tasks = self.decomposer.decompose(spec, max_duration="30min")
        
        # Fase 3: Ornith gera stubs de teste unitário por task
        for task in tasks:
            task.unit_tests = self.primary.generate_tests(task, type="unit")
            task.stub = self.primary.generate_stub(task)
        
        return TaskPlan(tasks=tasks, tests=acceptance_tests)
```

**Classificação:** **CRÍTICA** — TDD é a base da qualidade.

---

### 6.2 >>> Quebrar o Trabalho em Tasks (filtro)
**Modelo Designado:** **Nanbeige 3B** (primário)

**Justificativa Técnica:**
Quebra de tasks exige **velocidade** e **granularidade adequada**. Nanbeige 3B, com sua capacidade de reasoning rápido, pode quebrar um spec em 20-50 tasks em <5 segundos. Cada task é limitada a 30 minutos de trabalho humano-equivalente.

**Classificação:** **CRÍTICA** — Tasks mal dimensionadas causam overhead de orquestração.

---

### 6.3 >>> Planejar, Orquestrar e Implementar Decomposição (filtro)
**Modelo Designado:** **Ornith-1.0 9B** (arquitetura) + **Nanbeige 3B** (orquestração operacional)

**Justificativa Técnica:**
Esta é a fase mais complexa: mapear tasks para **plugins, subagentes, hooks, skills, MCPs, tool callings, LSPs**. Ornith 9B define a arquitetura de orquestração (quem chama quem). Nanbeige 3B gera a configuração operacional (arquivos YAML, JSON, registros).

**Implementação Prática:**
```yaml
# .opencode/orchestration/plan.yaml
orchestration:
  generated_by: "ornith-1.0-9b-q4km"
  validated_by: "nanbeige-3b-q4"
  
  plugins:
    - name: "git_manager"
      type: "builtin"
      hooks: ["pre_commit", "post_commit"]
    - name: "test_runner"
      type: "mcp"
      server: "pytest-mcp"
  
  subagents:
    - name: "FrontendAgent"
      model: "nanbeige-3b-q4"
      skills: ["react", "css", "a11y"]
      max_tasks: 5
    - name: "BackendAgent"
      model: "ornith-1.0-9b-q4km"
      skills: ["api_design", "db_schema", "auth"]
      max_tasks: 3
    - name: "TestAgent"
      model: "nanbeige-3b-q4"
      skills: ["tdd", "mutation_testing"]
      max_tasks: 10
  
  hooks:
    - event: "pre_task"
      action: "context_load"
      from: "obsidian_episodic"
    - event: "post_task"
      action: "evidence_capture"
      to: "obsidian_episodic"
  
  skills:
    - path: "./skills/"
      auto_register: true
      format: "SKILL.md"
  
  mcps:
    - name: "filesystem"
      command: "npx -y @modelcontextprotocol/server-filesystem"
    - name: "git"
      command: "uvx mcp-server-git"
    - name: "obsidian"
      command: "python -m mcp_obsidian_bridge"
  
  lsps:
    - language: "python"
      command: "pylsp"
    - language: "typescript"
      command: "typescript-language-server"
  
  tool_callings:
    registry: "./tools/registry.yaml"
    validation: "strict"  # Rejeita tool calls malformados
```

**Classificação:** **CRÍTICA** — Orquestração mal planejada = caos na execução.

---

### 6.4 >>> Brainstorm de Agents Valida Cobertura, Contratos, Verificabilidade (filtro)
**Modelo Designado:** **Nanbeige 3B** (primário) + **Bonsai 27B** (síntese de relatório)

**Justificativa Técnica:**
Validação de cobertura exige **análise sistemática**. Nanbeige 3B verifica se todos os requisitos do spec estão cobertos por tasks. Bonsai 27B gera o relatório de validação com linguagem clara e estruturada.

**Classificação:** **IMPORTANTE** — Pode ser automatizado após calibração inicial.

---

### 6.5 ⏸️ GATE 3: Usuário Aprova o Plano
**Classificação:** **CRÍTICA** — Gate humano inegociável.

---

### 6.6 💾 Safety: SHA Salvo AQUI (Fases 1-3 Não Tocam Código Produtivo)
**Implementação Prática:**
```bash
# .opencode/safety/pre_execution.sh
#!/bin/bash
set -euo pipefail

# Snapshot do estado antes de qualquer modificação
SHA_PRE=$(git rev-parse HEAD)
echo "SHA_PRE=$SHA_PRE" > .opencode/safety/sha_snapshot.env

# Bloqueio de escrita em branches protegidas
if [[ $(git branch --show-current) == "main" || $(git branch --show-current) == "master" ]]; then
    echo "ERRO: Fases 1-3 não podem modificar main/master"
    exit 1
fi

# Cria branch de trabalho isolada
BRANCH_NAME="opencode-plan-$(date +%s)"
git checkout -b "$BRANCH_NAME"
echo "BRANCH_PLAN=$BRANCH_NAME" >> .opencode/safety/sha_snapshot.env
```

**Classificação:** **CRÍTICA** — Segurança de estado é inegociável.

---
## 7. FASE 4 — EXECUÇÃO

### 7.1 >>> Supervisiona e Sequencia Tasks, Gerencia Git (commits atômicos)
**Modelo Designado:** **Nanbeige 3B** (supervisor operacional) + **Ornith-1.0 9B** (resolução de conflitos)

**Justificativa Técnica:**
Supervisão de execução exige **estado**, **sequenciamento** e **recuperação de erros**. Nanbeige 3B, com sua velocidade, monitora o estado de cada task em tempo real. Quando há conflitos de merge ou dependências circulares, Ornith 9B entra com raciocínio explícito para resolver.

**Implementação Prática:**
```python
# plugins/git_manager/hooks.py
class GitManager:
    def __init__(self):
        self.supervisor = ModelRouter("nanbeige-3b-q4")
        self.conflict_resolver = ModelRouter("ornith-1.0-9b-q4km")
    
    def commit_atomic(self, task: Task) -> Commit:
        # Gera mensagem de commit semanticamente relevante
        diff = self._get_diff()
        message = self.supervisor.generate_commit_message(diff, task)
        
        # Commit atômico: 1 task = 1 commit
        commit = git.commit(message, files=task.affected_files)
        
        # Verifica se o commit quebrou o build
        if not self._build_passes():
            git.revert(commit)
            raise BuildBreakException(task)
        
        return commit
    
    def resolve_conflict(self, branch1: str, branch2: str) -> Merge:
        # Ornith analisa o conflito com contexto completo
        conflict_context = self._get_conflict_context(branch1, branch2)
        resolution = self.conflict_resolver.resolve(conflict_context)
        
        return self._apply_resolution(resolution)
```

**Classificação:** **CRÍTICA** — Git mal gerenciado = histórico inútil.

---

### 7.2 >>> Reporta Progresso ao Orquestrador
**Modelo Designado:** **Nanbeige 3B** (geração de relatórios) + **LFM 1.6B** (OCR de evidências visuais)

**Justificativa Técnica:**
Relatórios de progresso devem ser **concisos** e **acionáveis**. Nanbeige 3B gera relatórios em <1s. LFM 1.6B processa screenshots, logs visuais e documentos escaneados que servem como evidência.

**Classificação:** **IMPORTANTE** — Pode ser substituído por regras simples após estabilização.

---

### 7.3 >>> Orquestra Subagentes Frescos por Task
**Modelo Designado:** **Ornith-1.0 9B** (orquestração estratégica) + **Nanbeige 3B** (subagentes operacionais)

**Justificativa Técnica:**
Cada task recebe um **subagente fresco** — sem contexto acumulado de tasks anteriores, evitando contaminação. Ornith 9B decide qual modelo cada subagente usa. Nanbeige 3B é o workhorse para 80% das tasks. Ornith 9B é reservado para tasks de arquitetura e design.

**Implementação Prática:**
```yaml
# .opencode/subagents/factory.yaml
subagent_factory:
  strategy: "fresh_per_task"
  context_isolation: true
  
  model_routing:
    - condition: "task.type == 'architecture'"
      model: "ornith-1.0-9b-q4km"
      reasoning: "explicit"
    - condition: "task.type == 'design'"
      model: "ornith-1.0-9b-q4km"
      reasoning: "explicit"
    - condition: "task.type == 'test'"
      model: "nanbeige-3b-q4"
      temperature: 0.3
    - condition: "task.type == 'refactor'"
      model: "nanbeige-3b-q4"
      temperature: 0.4
    - condition: "task.type == 'docs'"
      model: "bonsai-27b-1bit"
      temperature: 0.5
    - condition: "task.type == 'ui'"
      model: "nanbeige-3b-q4"
      vision: true  # Se necessário, fallback para LFM
    - condition: "default"
      model: "nanbeige-3b-q4"
      temperature: 0.6
  
  lifecycle:
    - spawn
    - load_context  # Apenas contexto relevante da task
    - execute
    - capture_evidence
    - destroy  # Libera memória
```

**Classificação:** **CRÍTICA** — Subagentes contaminados = código inconsistente.

---

### 7.4 >>> Gerencia Ciclo de Vida de Cada Componente (filtro — operacional)
**Modelo Designado:** **Nanbeige 3B** (gerenciamento operacional) + **Ornith-1.0 9B** (decisões de arquitetura)

**Justificativa Técnica:**
Gerenciamento de ciclo de vida exige **monitoramento contínuo**, **detecção de falhas** e **recuperação automática**. Nanbeige 3B monitora métricas de saúde (latência, erro rate, token usage). Ornith 9B decide quando escalar, substituir ou reconfigurar componentes.

**Implementação Prática:**
```python
# plugins/lifecycle_manager/manager.py
class LifecycleManager:
    def __init__(self):
        self.monitor = ModelRouter("nanbeige-3b-q4")
        self.architect = ModelRouter("ornith-1.0-9b-q4km")
        
    def health_check(self, component: Component) -> HealthStatus:
        metrics = component.get_metrics()
        
        # Nanbeige analisa métricas
        analysis = self.monitor.analyze(metrics)
        
        if analysis.status == "degraded":
            # Ornith decide estratégia de recuperação
            recovery_plan = self.architect.plan_recovery(component, analysis)
            self.execute_recovery(recovery_plan)
        
        return analysis
    
    def auto_heal(self, component: Component) -> bool:
        """
        Self-healing: tenta reiniciar, reconfigurar ou substituir componente.
        """
        strategies = ["restart", "reconfigure", "replace", "escalate"]
        
        for strategy in strategies:
            if self._try_heal(component, strategy):
                # Log no Obsidian para aprendizado
                self._log_healing_event(component, strategy)
                return True
        
        return False
```

**Classificação:** **IMPORTANTE** — Essencial para sistemas de longa duração.

---

### 7.5 >>> Implementar Loop Brainstorm de TDD por Task em Subagentes Frescos
**Modelo Designado:** **Nanbeige 3B** (TDD rápido) + **Ornith-1.0 9B** (TDD complexo)

**Justificativa Técnica:**
TDD por task exige **velocidade** para tasks simples e **profundidade** para tasks complexas. Nanbeige 3B executa TDD para tasks <30 min. Ornith 9B assume tasks que exigem design de API ou arquitetura de testes.

**Classificação:** **CRÍTICA** — TDD é a rede de segurança da execução.

---

### 7.6 >>> Evidência de Verificação por Task (filtro)
**Modelo Designado:** **Nanbeige 3B** (geração de evidência) + **LFM 1.6B** (OCR de evidências visuais)

**Justificativa Técnica:**
Cada task deve produzir **evidência verificável**: testes passando, screenshots, logs, métricas. Nanbeige 3B gera o pacote de evidência. LFM 1.6B extrai texto de screenshots e documentos.

**Implementação Prática:**
```yaml
# .opencode/evidence/template.yaml
evidence_package:
  required:
    - test_results: "pytest_output.xml"
    - coverage_report: "coverage.html"
    - diff: "git_diff.patch"
    - reasoning: "rationale.md"  # Gerado pelo modelo
  optional:
    - screenshot: "ui_test.png"
    - performance: "benchmark.json"
    - security_scan: "bandit.json"
  
  validation:
    - rule: "test_pass_rate == 100%"
      critical: true
    - rule: "coverage >= 80%"
      critical: false
    - rule: "no_security_high"
      critical: true
```

**Classificação:** **CRÍTICA** — Sem evidência, não há verificabilidade.

---

### 7.7 >>> Revisão Micro por Task (filtro)
**Modelo Designado:** **Nanbeige 3B** (revisão rápida) + **Ornith-1.0 9B** (revisão profunda)

**Justificativa Técnica:**
Revisão micro deve ser **rápida** (<5s) para não bloquear o pipeline. Nanbeige 3B faz a primeira passada: estilo, padrões, bugs óbvios. Ornith 9B faz a segunda passada em tasks marcadas como "complexas": arquitetura, segurança, performance.

**Classificação:** **IMPORTANTE** — Pode ser relaxada em hotfixes emergenciais.

---

### 7.8 ⚡ Sem Gates — Commits Atômicos, Progresso Visível
**Implementação Prática:**
```bash
# .opencode/hooks/post_task.sh
#!/bin/bash
# Executado após cada task

# 1. Commit atômico
git add -A
git commit -m "[task-${TASK_ID}] ${TASK_DESCRIPTION}

Model: ${MODEL_USED}
Evidence: ${EVIDENCE_SHA}
Review: ${REVIEW_STATUS}"

# 2. Push para branch de trabalho
git push origin $(git branch --show-current)

# 3. Atualiza progresso no Obsidian
echo "- [x] ${TASK_ID}: ${TASK_DESCRIPTION}" >> ./brain/episodic/session_$(date +%Y%m%d).md
```

**Classificação:** **CRÍTICA** — Transparência de progresso é inegociável.

---

## 8. FASE 5 — REVISÃO MACRO

### 8.1 >>> Revisão Holística do Diff Total — Coerência Cross-Task
**Modelo Designado:** **Ornith-1.0 9B** (primário) + **Bonsai 27B** (análise de impacto)

**Justificativa Técnica:**
Revisão holística exige **contexto massivo** (256K do Ornith) e **análise de padrões**. Ornith 9B lê o diff total do projeto e verifica coerência cross-task. Bonsai 27B analisa o impacto em documentação e READMEs.

**Implementação Prática:**
```python
# skills/macro_reviewer/SKILL.md
class MacroReviewer:
    model = ModelRouter("ornith-1.0-9b-q4km")
    impact_analyzer = ModelRouter("bonsai-27b-1bit")
    
    def review(self, base_sha: str, head_sha: str) -> MacroReview:
        diff = git.diff(base_sha, head_sha)
        
        # Ornith analisa coerência
        coherence = self.model.analyze_coherence(diff, self.context)
        
        # Bonsai analisa impacto em docs
        docs_impact = self.impact_analyzer.analyze_docs_impact(diff)
        
        return MacroReview(
            coherence_score=coherence.score,
            cross_task_issues=coherence.issues,
            docs_updates_required=docs_impact.updates,
            pass_threshold=0.85
        )
```

**Classificação:** **CRÍTICA** — Revisão macro evita débito técnico sistêmico.

---

### 8.2 >>> Acoplamento (filtro macro)
**Modelo Designado:** **Ornith-1.0 9B** (primário)

**Justificativa Técnica:**
Análise de acoplamento exige **raciocínio arquitetural**. Ornith 9B, com seu self-scaffolding, pode gerar diagramas de dependência e detectar violações de arquitetura (ex: camada de infraestrutura chamando camada de domínio).

**Classificação:** **IMPORTANTE** — Pode ser automatizado com ferramentas estáticas.

---

### 8.3 >>> Audita o Resultado Pronto contra Critérios de Qualidade
**Modelo Designado:** **Nanbeige 3B** (auditoria operacional) + **Ornith-1.0 9B** (auditoria arquitetural)

**Justificativa Técnica:**
Auditoria de qualidade exige **múltiplas dimensões**: funcional, performance, segurança, manutenibilidade. Nanbeige 3B verifica critérios operacionais (testes, cobertura, lint). Ornith 9B verifica critérios arquiteturais (padrões, coesão, acoplamento).

**Classificação:** **CRÍTICA** — Auditoria é a última linha de defesa.

---

### 8.4 >>> Brainstorm de Agents Arquitetura e Alinhamento com o Contrato
**Modelo Designado:** **Ornith-1.0 9B** (primário) + **Nanbeige 3B** (pesquisa de padrões)

**Justificativa Técnica:**
Brainstorm arquitetural exige **criatividade estruturada**. Ornith 9B propõe melhorias arquiteturais. Nanbeige 3B pesquisa padrões e referências.

**Classificação:** **OPCIONAL** — Pode ser pulado em releases pequenos.

---

## 9. FASE 6 — ENTREGA

### 9.1 >>> Verification: Evidência Fresca de Ferro (filtro)
**Modelo Designado:** **Nanbeige 3B** (execução de testes) + **Ornith-1.0 9B** (análise de falhas)

**Justificativa Técnica:**
"Evidência de ferro" significa **testes executados na branch de entrega**, não em mocks. Nanbeige 3B executa a suite completa de testes. Ornith 9B analisa falhas com raciocínio explícito, propondo correções.

**Implementação Prática:**
```bash
# .opencode/delivery/iron_evidence.sh
#!/bin/bash
set -euo pipefail

# 1. Checkout da branch de entrega
git checkout "$DELIVERY_BRANCH"

# 2. Instalação limpa
rm -rf node_modules venv && npm ci && pip install -r requirements.txt

# 3. Execução completa de testes
pytest --cov=src --cov-report=xml --cov-report=html
npm test -- --coverage

# 4. Validação de evidência
python -m opencode.validate_evidence \
  --tests pytest_output.xml \
  --coverage coverage.xml \
  --model nanbeige-3b-q4

# 5. Se falhar, Ornith analisa
if [ $? -ne 0 ]; then
  python -m opencode.analyze_failure \
    --model ornith-1.0-9b-q4km \
    --reasoning explicit
fi
```

**Classificação:** **CRÍTICA** — Sem evidência de ferro, não há entrega.

---

### 9.2 >>> Validação Final contra o Pedido Original (filtro)
**Modelo Designado:** **Nanbeige 3B** (comparação semântica) + **Ornith-1.0 9B** (validação de intenção)

**Justificativa Técnica:**
Validação final verifica se o **pedido original** foi atendido, não apenas o spec. Nanbeige 3B faz comparação semântica. Ornith 9B valida se a **intenção** do usuário foi preservada (pode haver gaps entre o que foi pedido e o que foi especificado).

**Classificação:** **CRÍTICA** — Entrega sem validação = insatisfação do usuário.

---

### 9.3 >>> Audita Evidência de Ferro, Emite Veredito Final
**Modelo Designado:** **Ornith-1.0 9B** (primário)

**Justificativa Técnica:**
O veredito final é uma **decisão binária** (pass/fail) com **justificativa completa**. Ornith 9B, com seu raciocínio explícito, emite vereditos que são auditáveis e explicáveis.

**Classificação:** **CRÍTICA** — Veredito é a assinatura de qualidade.

---

### 9.4 >>> Brainstorm de Agents para Conformidade e Qualidade
**Modelo Designado:** **Nanbeige 3B** (primário)

**Justificativa Técnica:**
Brainstorm de conformidade verifica se o projeto atende a: padrões de código, regulamentações (GDPR, LGPD), acessibilidade, i18n. Nanbeige 3B, com sua velocidade, pode verificar dezenas de critérios em paralelo.

**Classificação:** **IMPORTANTE** — Essencial para projetos regulamentados.

---

### 9.5 ⏸️ GATE 4: Relatório do Orquestrador → Memória Cerebral para Cognição Neurológica no Obsidian
**Modelo Designado:** **Sistema de Memória** (Obsidian + GraphRAG)

**Justificativa Técnica:**
O Gate 4 é o **ponto de aprendizado**. Todo o conhecimento gerado na sessão é persistido no Obsidian como **memória cerebral**. Isso inclui: decisões tomadas, erros cometidos, padrões descobertos, skills aprimoradas.

**Implementação Prática:**
```python
# plugins/obsidian_brain/encoder.py
class ObsidianBrainEncoder:
    def encode_session(self, session: Session) -> list[Note]:
        notes = []
        
        # 1. Memória Episódica — o que aconteceu
        episodic = Note(
            path=f"episodic/session_{session.id}.md",
            content=self._render_episodic(session),
            tags=["session", "episodic", session.project]
        )
        notes.append(episodic)
        
        # 2. Memória Semântica — conceitos aprendidos
        for concept in session.concepts:
            semantic = Note(
                path=f"semantic/{concept.hash}.md",
                content=self._render_semantic(concept),
                tags=["concept", "semantic"] + concept.domains
            )
            notes.append(semantic)
        
        # 3. Memória Procedural — skills aprimoradas
        for skill in session.skills_updated:
            procedural = Note(
                path=f"procedural/{skill.name}.md",
                content=self._render_procedural(skill),
                tags=["skill", "procedural"]
            )
            notes.append(procedural)
        
        # 4. Auto-cura: detecta conflitos com memórias anteriores
        conflicts = self._detect_conflicts(notes)
        for conflict in conflicts:
            resolution = self._resolve_conflict(conflict)
            notes.append(resolution)
        
        return notes
    
    def _detect_conflicts(self, new_notes: list[Note]) -> list[Conflict]:
        """
        Detecta quando uma nova memória contradiz uma antiga.
        Ex: 'Usar React' vs 'Migrar para Vue'.
        """
        conflicts = []
        for note in new_notes:
            similar = self.vault.find_similar(note, threshold=0.85)
            for old in similar:
                if self._is_contradictory(note, old):
                    conflicts.append(Conflict(new=note, old=old))
        return conflicts
```

**Classificação:** **CRÍTICA** — Sem memória, o sistema não aprende.

---

## 10. ANTROPOFAGIA TECNOLÓGICA & HELENIZAÇÃO

### 10.1 Conceito

**Antropofagia Tecnológica** é o processo de "devorar" tecnologias alheias — especialmente quando examinadas de forma criteriosa, quantitativa e qualitativa — e absorvê-las criticamente para criar uma identidade engenhosa genuinamente funcional.

**Helenização** é a conversão dessas tecnologias absorvidas ao padrão OpenCode, como uma metanoia onde técnicas, tools, conceitos, LSPs, MCPs, skills, agentes e subagentes se convertem ao harness OpenCode.

### 10.2 Metanoia Arquitetural

```
Tecnologia Externa → Análise Crítica → Extração de Essência → Conversão OpenCode

Exemplos:
• Claude Code Hooks (30 eventos) → OpenCode Hooks (JSON config + per-tool perms)
• Codex AGENTS.md → OpenCode AGENTS.md (compatível + extensões)
• Cursor Cloud Agents → OpenCode Subagents (fresh_per_task)
• Claude Skills (SKILL.md) → OpenCode Skills (SKILL.md padrão unificado)
• MCP Servers → OpenCode MCP Registry (yaml + auto-validação)
• LSPs → OpenCode LSP Bridge (multi-language, auto-detect)
```

### 10.3 Implementação: Motor de Antropofagia

```python
# plugins/anthropophagy/engine.py
class AnthropophagyEngine:
    """
    Motor de antropofagia tecnológica: devora, analisa e heleniza.
    """
    
    def __init__(self):
        self.analyzer = ModelRouter("nanbeige-3b-q4")  # Análise rápida
        self.synthesizer = ModelRouter("bonsai-27b-1bit")  # Síntese de texto
        self.validator = ModelRouter("ornith-1.0-9b-q4km")  # Validação arquitetural
    
    def devour(self, technology: ExternalTech) -> OpenCodeArtifact:
        """
        Fases da antropofagia:
        1. Ingestão: carrega a tecnologia externa
        2. Análise: extrai métricas, padrões, riscos
        3. Digestão: identifica a essência (o que é realmente valioso)
        4. Assimilação: converte ao padrão OpenCode
        5. Validação: garante que a conversão preserva valor
        """
        
        # Fase 1: Ingestão
        raw = self._ingest(technology)
        
        # Fase 2: Análise crítica (Nanbeige)
        analysis = self.analyzer.analyze(
            raw,
            dimensions=["security", "performance", "maintainability", "scalability"],
            output_format="structured_report"
        )
        
        # Fase 3: Digestão — extrai essência
        essence = self._extract_essence(raw, analysis)
        
        # Fase 4: Assimilação — helenização
        artifact = self._convert_to_opencode(essence, technology.type)
        
        # Fase 5: Validação (Ornith)
        validation = self.validator.validate(
            artifact,
            criteria=["preserves_functionality", "follows_opencode_standards", "no_security_regression"]
        )
        
        if not validation.passed:
            raise HelenizationFailed(validation.issues)
        
        # Persiste no Obsidian como memória de antropofagia
        self._log_assimilation(technology, artifact, analysis)
        
        return artifact
    
    def _convert_to_opencode(self, essence: Essence, tech_type: str) -> OpenCodeArtifact:
        converters = {
            "skill": SkillConverter(),
            "mcp": MCPConverter(),
            "hook": HookConverter(),
            "plugin": PluginConverter(),
            "lsp": LSPConverter(),
            "agent": AgentConverter(),
        }
        
        converter = converters.get(tech_type, GenericConverter())
        return converter.convert(essence)
```

**Classificação:** **IMPORTANTE** — Motor de antropofagia é diferencial competitivo.

---

## 11. META ORQUESTRADOR GRAN-MASTRE

### 11.1 Definição

O **Meta Orquestrador Gran-Mestre** é o **único agente de entrada** do sistema. Todos os outros agentes (subagentes, plugins, skills, MCPs) são orquestrados por ele. Ele é implementado como uma camada de abstração sobre o OpenCode, usando Ornith-1.0 9B como modelo de decisão.

### 11.2 Arquitetura

```
┌─────────────────────────────────────────────┐
│           GRAN-MASTRE INTERFACE             │
│  (API REST + WebSocket + CLI TUI)           │
├─────────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐    │
│  │  ORNITH-1.0 9B — NÚCLEO DECISÓRIO  │    │
│  │  • Roteamento de tasks para modelos │    │
│  │  • Decisões de arquitetura          │    │
│  │  • Resolução de conflitos           │    │
│  │  • Validação de contratos           │    │
│  └─────────────────────────────────────┘    │
├─────────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │NANBEIGE │ │ BONSAI  │ │ LFM     │       │
│  │  3B     │ │  27B    │ │ 1.6B    │       │
│  │(opera-  │ │(síntese │ │(OCR/   │       │
│  │ cional) │ │ /docs)  │ │ rápido) │       │
│  └─────────┘ └─────────┘ └─────────┘       │
├─────────────────────────────────────────────┤
│  OBSIDIAN BRAIN — MEMÓRIA PERSISTENTE       │
└─────────────────────────────────────────────┘
```

### 11.3 Protocolo de Roteamento

```yaml
# .opencode/gran_mastre/protocol.yaml
gran_mastre:
  model: "ornith-1.0-9b-q4km"
  reasoning: "explicit"
  
  routing_policy:
    # Regras de roteamento determinísticas + heurísticas
    - condition: "task.type == 'architecture'"
      target: "ornith-1.0-9b-q4km"
      reasoning: "explicit"
    
    - condition: "task.type == 'coding' AND task.complexity > 0.7"
      target: "ornith-1.0-9b-q4km"
      reasoning: "explicit"
    
    - condition: "task.type == 'coding' AND task.complexity <= 0.7"
      target: "nanbeige-3b-q4"
      temperature: 0.4
    
    - condition: "task.type == 'docs' OR task.type == 'summary'"
      target: "bonsai-27b-1bit"
      temperature: 0.5
    
    - condition: "task.type == 'vision' OR task.type == 'ocr'"
      target: "lfm-2.5-1.6b"
      vision: true
    
    - condition: "task.type == 'tool_calling' AND task.chain_length > 50"
      target: "nanbeige-3b-q4"  # Único que sustenta 500+ rounds
    
    - condition: "default"
      target: "nanbeige-3b-q4"
      temperature: 0.6
```

**Classificação:** **CRÍTICA** — Gran-Mestre é o cérebro do sistema.

---

## 12. COGNIÇÃO NEUROLÓGICA NO OBSIDIAN

### 12.1 Arquitetura de Memória

O Obsidian Vault implementa **três camadas neurológicas**:

| Camada | Função | Formato | Modelo de Embedding |
|--------|--------|---------|---------------------|
| **Episódica** | Sessões de trabalho | `session_{timestamp}.md` | Nanbeige 3B (rápido) |
| **Semântica** | Conceitos e padrões | `concept_{hash}.md` | Nanbeige 3B |
| **Procedural** | Skills e workflows | `skill_{name}.md` | — |

### 12.2 GraphRAG e Auto-Cura

```yaml
graphrag:
  enabled: true
  resolution_strategy: "conflict_merge"
  decay_factor: 0.01
  self_healing:
    enabled: true
    drift_detection: true
    skill_repair: true
```

**Classificação:** **CRÍTICA**

---

## 13. MATRIZ DE SEGURANÇA — ANÁLISE DE RISCOS POR MODELO

| Modelo | Risco de Injeção de Prompt | Risco de Vazamento de Dados | Risco de Hallucination | Mitigação |
|--------|---------------------------|----------------------------|------------------------|-----------|
| **Ornith 9B** | MÉDIO — self-scaffolding pode gerar prompts internos não auditáveis | BAIXO — local, sem exfiltração | MÉDIO — modo explícito reduz, mas não elimina | Sandbox de execução; validação de harness |
| **Nanbeige 3B** | BAIXO — modelo pequeno, fácil de auditar | BAIXO — local | MÉDIO — cai em contextos >64K | Checkpoint a cada 100 rounds; truncamento ativo |
| **Bonsai 27B** | BAIXO — 1-bit limita capacidade de injeção complexa | BAIXO — local | ALTO — tool calling degradado (-17.5%) | NÃO usar para tool calling crítico; usar apenas para docs/texto |
| **LFM 1.6B** | BAIXO — modelo muito pequeno | BAIXO — local | BAIXO — capability limitada | Usar apenas para OCR/classificação; nunca para decisões |

**Veredito de Segurança:** ✅ **Seguro para uso no harness OpenCode**, desde que:
1. Bonsai 27B **NUNCA** seja usado para tool calling ou decisões arquiteturais
2. Nanbeige 3B tenha **checkpoint a cada 100 rounds** de tool use
3. Ornith 9B tenha **timeout de 30s** em modo explícito para evitar loop de scaffolding
4. Todos os modelos operem em **sandbox de rede isolada** (no external calls sem proxy auditável)

---

## 14. ROADMAP DE IMPLEMENTAÇÃO

| Fase | Entregável | Prioridade | Modelo Principal | Tempo Estimado |
|------|-----------|------------|------------------|----------------|
| 1 | Configuração do Obsidian Brain | CRÍTICA | Nanbeige 3B | 2h |
| 2 | Setup do Gran-Mastre com roteamento | CRÍTICA | Ornith 9B | 4h |
| 3 | Implementação dos agents de Fase 1 | CRÍTICA | Nanbeige 3B | 3h |
| 4 | Motor de Antropofagia v0.1 | IMPORTANTE | Nanbeige + Bonsai | 6h |
| 5 | Hooks de Git e evidência | CRÍTICA | Nanbeige 3B | 3h |
| 6 | Integração LFM para OCR | OPCIONAL | LFM 1.6B | 2h |
| 7 | Self-healing e auto-cura | FUTURA | Ornith 9B | 8h |
| 8 | Tuning do roteamento por feedback | FUTURA | Nanbeige 3B | 4h |

---

## 15. CONCLUSÃO

Este SPEC estabelece um **sistema híbrido de modelos locais** que maximiza:
- **Velocidade** (Nanbeige 3B para 80% das tasks)
- **Profundidade** (Ornith 9B para arquitetura e decisões críticas)
- **Eficiência de hardware** (Bonsai 27B para docs em ~4GB)
- **Multimodalidade** (LFM 1.6B para OCR e visão)

A arquitetura preserva **compatibilidade incremental** com o projeto OpenCode existente, evitando reescritas. Cada modelo foi selecionado com base em **evidência quantitativa de benchmarks** e **análise de risco de segurança**.

**Próximo passo:** Aprovação do **GATE 1** para iniciar a implementação da Fase 1 (Descoberta).

---

**Status do documento:** `RASCUNHO COMPLETO` → Aguardando `GATE 1: APROVAÇÃO DA DIREÇÃO`

---

*Documento gerado em: 2026-08-07*
*Versão: 1.0.0*
*Sistema: OpenCode Harness + Meta-Orquestrador Gran-Mestre*