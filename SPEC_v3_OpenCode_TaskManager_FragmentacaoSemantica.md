# SPEC v3.0 — OpenCode Harness: Orquestração de 5 Modelos Locais + Task Manager de Fragmentação Semântica
## Meta-Orquestrador Gran-Mestre com Context Window Task Fragmentation & Sequential Merge Policy
### Agosto 2026
### Status: RASCUNHO → REQUER APROVAÇÃO GATE 1

---

## 1. RESUMO EXECUTIVO

Este documento evolui o SPEC v2.0, incorporando uma **camada fundamental de Task Manager** que opera **antes da seleção do subagente**. A inovação central é a **fragmentação semântica de contexto**: nenhuma tarefa falha por exceder a janela de contexto. O sistema decompõe → enfileira → executa → valida → consolida → continua, preservando estado, dependências e coesão lógica.

A filosofia operacional é o **MIX Dev Loop**: autofagia tecnológica contínua + helenização rigorosa, buscando hooks, plugins, skills, subagents, MCPs, LSPs e features externas para devorar criticamente e converter ao padrão OpenCode.

### Mudanças Principais da v2 → v3:
| v2.0 (Anterior) | v3.0 (Evoluído) | Razão da Evolução |
|-----------------|-------------------|-------------------|
| Sem gerenciamento de contexto excessivo | **Task Manager com Fragmentação Semântica** | Tarefas grandes nunca falham por limitação de janela |
| Merge por concatenação | **Reducer Semântico com Auditoria de Bordas** | Elimina quebras de coesão entre fragmentos |
| Estado propagado de forma ad-hoc | **Rolling Summaries + Vetor de Estado** | Compressão de contexto entre subtasks |
| Autofagia sem motor formal | **Motor de Antropofagia v3.0** | Devoração sistemática de tecnologias externas |
| 6 fases lineares | **6 fases + MIX Dev Loop contínuo** | Feedback loop pós-entrega para evolução constante |

---

## 2. FILOSOFIA OPERACIONAL: MIX DEV LOOP

```
┌─────────────────────────────────────────────────────────────┐
│                    MIX DEV LOOP v3.0                        │
│                                                             │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌────────┐ │
│   │  M      │───►│  I      │───►│  X      │───►│  LOOP  │ │
│   │ Monitor │    │ Ingest  │    │ eXecute │    │ Learn  │ │
│   │         │    │         │    │         │    │        │ │
│   └────┬────┘    └────┬────┘    └────┬────┘    └───┬────┘ │
│        │              │              │             │      │
│        ▼              ▼              ▼             ▼      │
│   Observa        Devora          Aplica        Auto-cura │
│   gaps           tecnologia      helenizada    skills    │
│                  externa         no harness    e memória │
│                                                             │
│   REGRA: Todo ciclo deve gerar pelo menos 1 hook, 1 skill  │
│   ou 1 plugin que capture o aprendizado em código.         │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Autofagia Tecnológica v3.0

**Definição:** Devorar tecnologias alheias criticamente para criar identidade engenhosa genuinamente funcional.

**Pipeline de Antropofagia:**
```
Tecnologia Externa → Análise Crítica → Extração de Essência → Helenização → OpenCode Artifact

Exemplos v3.0:
• Claude Code Hooks → OpenCode Hooks (JSON config + per-tool perms + auto-fragmentação)
• Codex AGENTS.md → OpenCode AGENTS.md (compatível + extensões + context window policy)
• Cursor Cloud Agents → OpenCode Subagents (fresh_per_task + semantic chunking)
• Claude Skills → OpenCode Skills (SKILL.md padrão unificado + self-healing)
• MCP Servers → OpenCode MCP Registry (yaml + auto-validação + state propagation)
• LSPs → OpenCode LSP Bridge (multi-language, auto-detect, semantic boundary analysis)
• Qwen Function Calling → OpenCode Tool Registry (nativo, 201 idiomas, rolling summaries)
• DeepSeek R1 Thinking → OpenCode Audit Layer (chain-of-thought visível + reducer validation)
• GitHub Copilot Chat → OpenCode Chat Loop (MIX Dev Loop integrado)
• Any External Dev Tool → OpenCode Plugin (anthropophagy engine + helenization validator)
```

### 2.2 Motor de Antropofagia v3.0

```python
# plugins/anthropophagy/engine.py (v3.0)
class AnthropophagyEngine:
    def __init__(self):
        self.analyzer = ModelRouter("qwen-3.5-0.8b-q4")
        self.synthesizer = ModelRouter("bonsai-27b-1bit")
        self.validator = ModelRouter("ornith-1.0-9b-q4km")
        self.logic_auditor = ModelRouter("deepseek-r1-1.5b-q4")
        self.fragmenter = TaskFragmenter()

    def devour(self, technology: ExternalTech) -> OpenCodeArtifact:
        raw = self._ingest(technology)

        analysis = self.analyzer.analyze(
            raw,
            dimensions=["security", "performance", "maintainability", "scalability", "logic", "fragmentability"],
            output_format="structured_report"
        )

        if analysis.token_count > self.analyzer.context_window * 0.8:
            fragments = self.fragmenter.semantic_chunk(
                content=raw,
                model="qwen-3.5-0.8b-q4",
                overlap_ratio=0.15
            )
            analysis = self._merge_fragment_analyses(fragments)

        essence = self._extract_essence(raw, analysis)
        artifact = self._convert_to_opencode(essence, technology.type)

        arch_validation = self.validator.validate(artifact, criteria=[
            "preserves_functionality", "follows_opencode_standards", "fragmentation_safe"
        ])

        logic_validation = self.logic_auditor.generate(
            prompt=f"Audite a consistência lógica: {artifact}",
            show_thinking=False,
            timeout=15
        )

        cohesion_validation = self.fragmenter.validate_cohesion(artifact)

        if not arch_validation.passed or logic_validation.score < 0.85 or not cohesion_validation.ok:
            raise HelenizationFailed(
                arch_validation.issues + logic_validation.issues + cohesion_validation.gaps
            )

        self._log_assimilation(technology, artifact, analysis)
        return artifact
```

---

## 3. MATRIZ DE MODELOS v3.0

| Modelo | Parâmetros | Contexto | Licença | VRAM Q4 | Papel Primário | Papel Secundário | Quando NÃO Usar |
|--------|-----------|----------|---------|---------|---------------|------------------|-----------------|
| **Ornith 9B** | 9B Dense | 256K | MIT | ~5-6GB | Arquitetura, contratos, revisão macro, **Reducer** | Resolução de conflitos, self-scaffolding | Tasks simples (<30s), fragmentação leve |
| **Qwen 3.5 0.8B** | 0.8B | 262K | Apache 2.0 | ~0.9GB | 80% tasks, **Fatiador Semântico**, embeddings | OCR, tradução, tool calling, JSON mode | Raciocínio profundo multi-step |
| **DeepSeek R1 1.5B** | ~1.5B | 128K | MIT | ~1.0-1.2GB | Validação, auditoria, **Auditor de Bordas** | Análise de falhas, discriminação | Geração de código, tool calling |
| **Bonsai 27B** | 27B (1-bit) | 32K-64K | — | ~4GB | Documentação, **Rolling Summaries**, síntese | Análise de impacto em docs | Tool calling, agentic workflows |
| **Llama 3.2 1B** | 1B | 128K | Llama 3.2 | ~0.6-0.7GB | OCR ultra-rápido, fallback visual | Pré-processamento de gates | Qualquer task de reasoning |

---

## 4. CAMADA FUNDAMENTAL: TASK MANAGER DE FRAGMENTAÇÃO SEMÂNTICA

> **REGRA GLOBAL:** Esta camada opera **antes da seleção do subagente**. Se as tasks não couberem dentro da janela de contexto dos subagentes, o sistema fragmenta a task primária até caber, enfileira cronologicamente, executa, valida, consolida e segue o workflow.

### 4.1 Invariante do Sistema

> **Uma tarefa nunca deve ser descartada por excesso de contexto. Ela deve ser decomposta até que cada unidade seja executável dentro da capacidade do agente, mantendo dependências, estado, validação e ordem de execução; ao final, os resultados devem ser semanticamente consolidados antes da continuação do workflow.**

### 4.2 Arquitetura do Task Manager

```
                    ORCHESTRATOR
                         │
              ┌──────────┴──────────┐
              │                     │
          WORKFLOW              TASK MANAGER  ←── CAMADA FUNDAMENTAL v3.0
              │                     │
              │              ┌──────┴──────┐
              │              │             │
              │         CONTEXT      TASK
              │         MANAGER      DECOMPOSER
              │              │             │
              │              └──────┬──────┘
              │                     │
              │              TASK QUEUE
              │                     │
              │         ┌───────────┴───────────┐
              │         │   CHECKPOINT STORE    │
              │         │   RESULT MERGER       │
              │         │   (Reducer Semântico) │
              │         └───────────┬───────────┘
              │                     │
              └──────────┬──────────┘
                         │
                    SUBAGENTS
```

### 4.3 Os Três Vetores

#### Vetor 1: O Fatiador (Chunking Semântico e Overlapping)

Cortes puramente matemáticos destroem a lógica. O Fatiador implementa:

- **Análise de Fronteiras:** Quebra o input em nós lógicos (AST para código, parágrafos fechados para texto), forçando o corte apenas no fim de blocos estruturais.
- **Sliding Window (Overlapping):** Cada fragmento herda uma "margem de sangria" (últimos 15% do contexto do fragmento anterior).

```python
# plugins/task_manager/fragmenter.py (v3.0)
class SemanticFragmenter:
    def __init__(self):
        self.analyzer = ModelRouter("qwen-3.5-0.8b-q4")
        self.overlap_ratio = 0.15

    def semantic_chunk(self, content: str, model: str, max_tokens: int) -> list[TaskFragment]:
        boundaries = self._detect_logical_boundaries(content)
        chunks = []
        current_chunk = ""

        for boundary in boundaries:
            if self._estimate_tokens(current_chunk + boundary) > max_tokens * (1 - self.overlap_ratio):
                overlap = self._extract_overlap(current_chunk, ratio=self.overlap_ratio)
                chunks.append(TaskFragment(
                    content=current_chunk,
                    overlap_tail=overlap,
                    boundary_type=boundary.type
                ))
                current_chunk = overlap + boundary.content
            else:
                current_chunk += boundary.content

        if current_chunk:
            chunks.append(TaskFragment(content=current_chunk))

        return chunks

    def _detect_logical_boundaries(self, content: str) -> list[Boundary]:
        if self._is_code(content):
            return self._ast_boundaries(content)
        return self._text_boundaries(content)
```

#### Vetor 2: O Motor de Estado (Compressão e Rolling Summaries)

- **Vetor de Estado:** Payload JSON estruturado que viaja com a fila.
- **Ponteiros Lógicos:** O texto bruto fica armazenado à parte. O próximo subagente recebe apenas o Rolling Summary + o pedaço de dados da sua task.

```yaml
# state/tasks/TASK-001/state_vector.yaml (v3.0)
state_vector:
  task_id: TASK-001
  current_fragment: 3
  total_fragments: 7

  completed_goals:
    - "Arquitetura analisada: microserviços aprovados"
    - "Schema de banco validado: PostgreSQL + Redis"

  active_entities:
    - name: "UserService"
      type: "microservice"
      status: "defined"
      dependencies: ["AuthService", "Database"]

  pending_context:
    - "Loop de autenticação iniciado no fragmento 2, condição de parada pendente"

  rolling_summary: |
    Até o momento, a arquitetura foi definida como microserviços
    com PostgreSQL e Redis. O serviço UserService foi estruturado
    e o middleware de autenticação foi parcialmente implementado,
    faltando a condição de parada do loop de validação de token.

  decisions:
    - fragment: 1
      decision: "Usar JWT para autenticação"
      rationale: "Escalabilidade e statelessness"

  artifacts_pointer:
    base_path: "state/tasks/TASK-001/artifacts/"
    files:
      - "001_architecture.md"
      - "002_auth_partial.py"
```

#### Vetor 3: O Consolidador (Reducer Semântico)

A fusão final NÃO é concatenação de strings. O Reducer:

- **Audita Bordas:** Foca nas zonas de emenda, rastreia variáveis órfãs, redundâncias do overlapping e escopos abertos.
- **Passagem de Coesão:** Atua como linker, resolvendo dependências cruzadas entre fragmentos.

```python
# plugins/task_manager/reducer.py (v3.0)
class SemanticReducer:
    def __init__(self):
        self.primary = ModelRouter("ornith-1.0-9b-q4km")
        self.logic_auditor = ModelRouter("deepseek-r1-1.5b-q4")
        self.summarizer = ModelRouter("bonsai-27b-1bit")

    def semantic_merge(self, fragments: list[TaskResult]) -> MergedResult:
        border_issues = []
        for i in range(len(fragments) - 1):
            audit = self.logic_auditor.generate(
                prompt=f"Audite a coesão entre fragmentos {i} e {i+1}: "
                       f"TAIL: {fragments[i].tail} | HEAD: {fragments[i+1].head}",
                show_thinking=True,
                timeout=20
            )
            border_issues.extend(audit.issues)

        consolidation_prompt = self._build_consolidation_prompt(fragments, border_issues)
        consolidated = self.primary.generate(
            prompt=consolidation_prompt,
            temperature=0.2,
            reasoning_mode="explicit",
            max_tokens=16384
        )

        cohesion_check = self.logic_auditor.generate(
            prompt=f"Valide a coesão lógica: {consolidated}",
            show_thinking=False,
            timeout=15
        )

        if cohesion_check.score < 0.90:
            consolidated = self._repair_cohesion(consolidated, cohesion_check.gaps)

        final_summary = self.summarizer.generate(
            prompt=f"Gere rolling summary executivo: {consolidated}",
            max_tokens=2048
        )

        return MergedResult(
            artifact=consolidated,
            summary=final_summary,
            border_issues_resolved=border_issues,
            cohesion_score=cohesion_check.score
        )
```

### 4.4 Protocolo de Execução

```
TASK_PRIMARIA
      │
      ▼
[Estimar tamanho da tarefa]
      │
      ├── Cabe no contexto ─────────────► EXECUTAR diretamente
      │
      └── Não cabe
             │
             ▼
       DECOMPOR TASK (Fatiador Semântico)
             │
             ▼
    TASK_QUEUE cronológica com dependências
             │
             ▼
      ┌───────────────┐
      │ Subtask N     │
      │ contexto OK   │
      └───────┬───────┘
              ▼
      ┌───────────────┐
      │ Task Envelope │
      │ + State Vector│
      └───────┬───────┘
              ▼
          EXECUTAR (subagente)
              │
              ▼
           VALIDAR
              │
              ▼
       CHECKPOINT obrigatório
              │
              ▼
       STATE UPDATE + CONTEXT COMPRESSION
              │
              ▼
      PRÓXIMA SUBTASK (com rolling summary)
              │
             ...
              │
              ▼
      CONSOLIDAR RESULTADOS (Reducer Semântico)
              │
              ▼
       VALIDAR CONSOLIDAÇÃO
              │
              ▼
       RETOMAR WORKFLOW
```

### 4.5 Estados do Task Manager

```text
PENDING      → Task criada, aguardando análise de contexto
QUEUED       → Na fila cronológica, dependências satisfeitas
RUNNING      → Em execução no subagente
BLOCKED      → Aguardando dependência ou refragmentação
COMPLETED    → Execução finalizada
VALIDATED    → Passou na validação automática
FAILED       → Falhou na execução ou validação
RETRYING     → Tentativa de reexecução
MERGED       → Resultado consolidado pelo Reducer
REFRAGMENT   → Task muito grande, requer novo fatiamento
```

### 4.6 Pseudocódigo do Orchestrator v3.0

```python
def execute_task(task, agent):
    capacity = calculate_available_context(agent)

    if estimate_tokens(task) <= capacity:
        return execute(task, agent)

    subtasks = decompose_semantically(task, capacity)
    queue = build_dependency_queue(subtasks)

    state_vector = StateVector(task_id=task.id)
    results = []

    while queue.has_pending():
        subtask = queue.next_ready()

        context = build_minimal_context(
            task=task,
            subtask=subtask,
            state_vector=state_vector,
            previous_results=results
        )

        result = execute(subtask, agent, context)

        if result.context_overflow:
            subtask = refragment(subtask, capacity)
            queue.replace(subtask)
            continue

        validation = validate(result)
        if not validation.ok:
            if validation.retry_possible:
                queue.retry(subtask)
            elif validation.context_insufficient:
                subtask = refragment(subtask, capacity)
                queue.replace(subtask)
            else:
                queue.block(subtask, validation.error)
            continue

        checkpoint(subtask, result, state_vector)
        state_vector.update(result)
        state_vector.compress()

        results.append(result)
        queue.mark_completed(subtask)

    merged = semantic_reducer.merge(results, state_vector)

    final_validation = validate_merge(merged)
    if not final_validation.ok:
        merged = resolve_merge_conflicts(merged, final_validation.conflicts)

    return merged
```

---

## 5. ARQUITETURA DO HARNESS v3.0

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    META ORQUESTRADOR GRAN-MASTRE                        │
│              (Ornith-1.0 9B — Decisão Estratégica Final)                │
├─────────────────────────────────────────────────────────────────────────┤
│  CAMADA FUNDAMENTAL: TASK MANAGER                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Context    │  │  Semantic   │  │   Task      │  │  Semantic   │   │
│  │  Manager    │  │  Fragmenter │  │   Queue     │  │  Reducer    │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │
│  │  Checkpoint │  │   State     │  │   Rolling   │                    │
│  │   Store     │  │   Vector    │  │  Summaries  │                    │
│  └─────────────┘  └─────────────┘  └─────────────┘                    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  FASE 1     │  │  FASE 2     │  │  FASE 3     │  │  FASE 4-6   │  │
│  │ Descoberta  │  │ Contrato    │  │ Plano       │  │ Exec-Rev-   │  │
│  │             │  │             │  │             │  │ Entrega     │  │
│  │ Qwen 0.8B   │  │ Ornith 9B   │  │ Ornith 9B   │  │ Bonsai 27B  │  │
│  │ Llama 1B    │  │ Qwen 0.8B   │  │ Qwen 0.8B   │  │ Qwen 0.8B   │  │
│  │ DeepSeek    │  │ DeepSeek    │  │ DeepSeek    │  │ DeepSeek    │  │
│  │   R1 1.5B   │  │   R1 1.5B   │  │   R1 1.5B   │  │   R1 1.5B   │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│  ARSENAL OPENCODE: Hooks | Plugins | Skills | Subagents | MCP | LSP    │
├─────────────────────────────────────────────────────────────────────────┤
│  COGNIÇÃO NEUROLÓGICA — Obsidian Vault (Memória Cerebral Persistente)   │
│  • Embeddings: Qwen 0.8B (rápido, 201 idiomas, multimodal)              │
│  • GraphRAG: DeepSeek R1 1.5B (raciocínio em links)                     │
│  • Auto-cura: Ornith 9B (self-scaffolding de correções)                 │
│  • Rolling Summaries: Bonsai 27B (compressão de sessões)                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 6. ARSENAL OPENCODE v3.0

### 6.1 Hooks

```yaml
# .opencode/hooks/registry.yaml (v3.0)
hooks:
  pre_fragmentation:
    - name: "context_estimator"
      trigger: "before_task_fragmentation"
      handler: "hooks/pre_fragmentation/estimate_context.py"
      priority: 100

  post_execution:
    - name: "auto_checkpoint"
      trigger: "after_subtask_execution"
      handler: "hooks/post_execution/auto_checkpoint.py"
      priority: 50
    - name: "state_compressor"
      trigger: "after_subtask_execution"
      handler: "hooks/post_execution/compress_state.py"
      priority: 40

  pre_merge:
    - name: "border_auditor"
      trigger: "before_reducer_merge"
      handler: "hooks/pre_merge/audit_borders.py"
      model: "deepseek-r1-1.5b-q4"
      priority: 100

  post_merge:
    - name: "cohesion_validator"
      trigger: "after_reducer_merge"
      handler: "hooks/post_merge/validate_cohesion.py"
      model: "deepseek-r1-1.5b-q4"
      priority: 100

  on_failure:
    - name: "refragment_trigger"
      trigger: "on_context_overflow"
      handler: "hooks/on_failure/refragment.py"
      priority: 100
    - name: "fallback_orchestrator"
      trigger: "on_subagent_failure"
      handler: "hooks/on_failure/fallback.py"
      priority: 50
```

### 6.2 Plugins

```yaml
# .opencode/plugins/registry.yaml (v3.0)
plugins:
  anthropophagy:
    name: "Motor de Antropofagia v3.0"
    entry: "plugins/anthropophagy/engine.py"
    models: ["qwen-3.5-0.8b-q4", "bonsai-27b-1bit", "ornith-1.0-9b-q4km", "deepseek-r1-1.5b-q4"]
    capabilities: ["tech_ingest", "essence_extract", "helenization", "cohesion_validate"]

  task_manager:
    name: "Task Manager de Fragmentação Semântica"
    entry: "plugins/task_manager/orchestrator.py"
    models: ["qwen-3.5-0.8b-q4", "ornith-1.0-9b-q4km", "deepseek-r1-1.5b-q4", "bonsai-27b-1bit"]
    capabilities: ["semantic_chunk", "state_propagation", "rolling_summary", "reducer_merge"]

  git_manager:
    name: "Git Manager com Commits Atômicos"
    entry: "plugins/git_manager/hooks.py"
    models: ["qwen-3.5-0.8b-q4", "ornith-1.0-9b-q4km", "deepseek-r1-1.5b-q4"]
    capabilities: ["atomic_commit", "sequence_audit", "conflict_resolution"]

  obsidian_brain:
    name: "Cognição Neurológica Persistente"
    entry: "plugins/obsidian_brain/encoder.py"
    models: ["qwen-3.5-0.8b-q4", "deepseek-r1-1.5b-q4", "ornith-1.0-9b-q4km"]
    capabilities: ["episodic_memory", "semantic_memory", "procedural_memory", "graphrag"]
```

### 6.3 Skills

```markdown
# skills/semantic_fragmentation/SKILL.md (v3.0)
skill: "SemanticFragmentation"
description: "Fragmenta tasks grandes em unidades executáveis preservando coesão lógica"
version: "3.0.0"
models:
  primary: "qwen-3.5-0.8b-q4"
  validator: "deepseek-r1-1.5b-q4"
  reducer: "ornith-1.0-9b-q4km"

steps:
  1:
    action: "estimate_context"
    description: "Calcula available_context = context_window - system_prompt - agent_prompt - tools - memory - safety_margin"
  2:
    action: "detect_boundaries"
    description: "Identifica nós lógicos (AST para código, parágrafos para texto)"
  3:
    action: "semantic_chunk"
    description: "Fragmenta respeitando fronteiras com overlap de 15%"
  4:
    action: "build_envelopes"
    description: "Cria Task Envelope para cada fragmento com state_vector"
  5:
    action: "enqueue"
    description: "Insere na fila cronológica com dependências explícitas"
  6:
    action: "execute_queue"
    description: "Executa subtasks sequencialmente com state propagation"
  7:
    action: "validate_fragments"
    description: "Valida cada fragmento antes do merge"
  8:
    action: "semantic_merge"
    description: "Reducer consolida resultados com auditoria de bordas"
  9:
    action: "validate_merge"
    description: "Valida coesão do artefato final"

invariants:
  - "Nenhuma task falha por excesso de contexto"
  - "Overlap mínimo de 15% entre fragmentos adjacentes"
  - "Cada fragmento deve ser autossuficiente"
  - "Merge deve ser semântico, não concatenação"
```

### 6.4 Subagents

```yaml
# .opencode/subagents/factory.yaml (v3.0)
subagent_factory:
  strategy: "fresh_per_task"
  context_isolation: true

  model_routing:
    - condition: "task.type == 'architecture'"
      model: "ornith-1.0-9b-q4km"
      reasoning: "explicit"

    - condition: "task.type == 'coding' AND task.complexity > 0.7"
      model: "ornith-1.0-9b-q4km"
      reasoning: "explicit"

    - condition: "task.type == 'coding' AND task.complexity <= 0.7"
      model: "qwen-3.5-0.8b-q4"
      temperature: 0.4
      json_mode: true

    - condition: "task.type == 'docs' OR task.type == 'summary'"
      model: "bonsai-27b-1bit"
      temperature: 0.5

    - condition: "task.type == 'vision' OR task.type == 'ocr'"
      model: "qwen-3.5-0.8b-q4"
      vision: true

    - condition: "task.type == 'ocr_fast'"
      model: "llama-3.2-1b-q4"
      temperature: 0.2

    - condition: "task.type == 'audit' OR task.type == 'validate'"
      model: "deepseek-r1-1.5b-q4"
      show_thinking: true
      timeout: 15

    - condition: "task.type == 'fragmentation'"
      model: "qwen-3.5-0.8b-q4"
      skills: ["semantic_fragmentation"]

    - condition: "task.type == 'reduction'"
      model: "ornith-1.0-9b-q4km"
      skills: ["semantic_reduction"]

    - condition: "default"
      model: "qwen-3.5-0.8b-q4"
      temperature: 0.6
      thinking: true

  output_validation:
    enabled: true
    model: "deepseek-r1-1.5b-q4"
    validate: ["logical_consistency", "contract_compliance", "no_contradictions", "border_cohesion"]
    timeout: 8

  lifecycle:
    - spawn
    - load_context
    - execute
    - validate_output
    - checkpoint_state
    - capture_evidence
    - destroy
```

### 6.5 MCP Servers

```yaml
# .opencode/mcp/registry.yaml (v3.0)
mcps:
  filesystem:
    command: "npx -y @modelcontextprotocol/server-filesystem"
    permissions: ["read", "write", "list"]

  git:
    command: "uvx mcp-server-git"
    permissions: ["log", "diff", "commit", "branch"]

  obsidian:
    command: "python -m mcp_obsidian_bridge"
    permissions: ["read", "write", "search", "link"]

  vision:
    command: "python -m mcp_vision_bridge"
    model: "qwen-3.5-0.8b-q4"
    permissions: ["ocr", "classify", "describe"]

  task_state:
    command: "python -m mcp_task_state_bridge"
    permissions: ["read_state", "write_state", "compress_state"]

  fragmenter:
    command: "python -m mcp_fragmenter_bridge"
    model: "qwen-3.5-0.8b-q4"
    permissions: ["chunk", "merge", "validate_borders"]
```

### 6.6 LSP Bridge

```yaml
# .opencode/lsp/registry.yaml (v3.0)
lsp:
  bridge:
    name: "OpenCode LSP Bridge"
    auto_detect: true
    languages: ["python", "javascript", "typescript", "rust", "go", "java", "cpp", "ruby"]

  capabilities:
    - "semantic_tokens"
    - "document_symbols"
    - "diagnostics"
    - "code_actions"
    - "boundary_analysis"

  fragmentation_support:
    enabled: true
    ast_providers:
      python: "pylsp"
      javascript: "typescript-language-server"
      typescript: "typescript-language-server"
      rust: "rust-analyzer"
```

---

## 7. FASE 1 — DESCOBERTA (com Task Manager)

### 7.1 Ideias (filtro)
**Modelos:** Qwen 0.8B (primário) + Llama 1B (OCR) + DeepSeek R1 1.5B (filtro)

**Integração v3.0:** Se o brainstorming gerar mais de 262K tokens de contexto, o Task Manager ativa fragmentação semântica. Cada ideia é um fragmento autossuficiente com overlap de contexto entre análises.

### 7.2 Definição de Escopo (filtro)
**Modelos:** Qwen 0.8B + Ornith 9B + DeepSeek R1 1.5B

**Integração v3.0:** Escopos extensos são fragmentados por domínio (frontend, backend, infra, segurança). Cada fragmento gera seu próprio state_vector. O Reducer consolida em escopo unificado.

### 7.3 Remover Ambiguidade (filtro)
**Modelos:** Ornith 9B + DeepSeek R1 1.5B

**Integração v3.0:** Ambiguidades complexas são fragmentadas por módulo. O Reducer detecta conflitos cross-módulo na consolidação.

### 7.4 Decomposição Leve (com Fragmentação Automática)
**Modelo:** Qwen 0.8B

**Integração v3.0:** Se a decomposição exceder o contexto, o Task Manager fragmenta por subdomínio e consolida via Reducer.

### 7.5 Brainstorm de Agents (com Reducer)
**Modelos:** Qwen 0.8B (divergência) + Bonsai 27B (síntese) + DeepSeek R1 1.5B (crítica)

**Integração v3.0:** Se o brainstorm exceder 262K tokens, cada iteração é fragmentada. O Reducer consolida as 3 iterações em proposta unificada.

### 7.6 ⏸️ GATE 1: Aprovação da Direção

---

## 8. FASE 2 — CONTRATO (com Estado Persistente)

### 8.1 Design Doc (com Fragmentação de Documentos Grandes)
**Modelos:** Ornith 9B + Qwen 0.8B + DeepSeek R1 1.5B

**Integração v3.0:** Design docs extensos são fragmentados por seção. Cada seção é processada como subtask com state_vector compartilhado.

### 8.2 spec.md (com Auditoria de Completude)
**Modelos:** Ornith 9B + DeepSeek R1 1.5B

**Integração v3.0:** Specs grandes são fragmentados por requisito. DeepSeek R1 audita completude lógica entre fragmentos.

### 8.3 Validação contra Pedido Original (com Rolling Summary)
**Modelos:** Qwen 0.8B + DeepSeek R1 1.5B

**Integração v3.0:** O rolling summary do pedido original é propagado entre fragmentos, garantindo que a intenção do usuário não se perca.

### 8.4 Auditoria em Brainstorm de Agents
**Modelos:** Qwen 0.8B + Ornith 9B + DeepSeek R1 1.5B

### 8.5 Preservar Contexto (com State Vector)
```yaml
# .opencode/memory/obsidian_config.yaml (v3.0)
memory:
  type: "obsidian_graphrag"
  vault_path: "./brain/"

  layers:
    episodic:
      path: "./brain/episodic/"
      format: "session_{timestamp}.md"
      retention: "permanent"
      rolling_summary: true
      summary_model: "bonsai-27b-1bit"

    semantic:
      path: "./brain/semantic/"
      format: "concept_{hash}.md"
      embedding_model: "qwen-3.5-0.8b-q4"

    procedural:
      path: "./brain/procedural/"
      format: "skill_{name}.md"
      auto_update: true

    state_vector:
      path: "./brain/state/"
      format: "state_{task_id}.yaml"
      compression: true
      compression_model: "bonsai-27b-1bit"

  graphrag:
    enabled: true
    resolution_strategy: "conflict_merge"
    decay_factor: 0.01
    link_reasoning:
      enabled: true
      model: "deepseek-r1-1.5b-q4"
      show_thinking: false
```

### 8.6 ⏸️ GATE 2: Aprovação do spec

---

## 9. FASE 3 — PLANO (com Decomposição Inteligente)

### 9.1 TDD e Tasks Bite-Sized
**Modelos:** Ornith 9B + Qwen 0.8B + DeepSeek R1 1.5B

**Integração v3.0:** Planos TDD extensos são fragmentados por camada. O Reducer garante que os testes de integração cobram as interfaces entre as unidades fragmentadas.

### 9.2 Quebrar em Tasks
**Modelo:** Qwen 0.8B

**Integração v3.0:** Task queue com dependências explícitas e state_vector. Se o plano total exceder o contexto, fragmenta por sprint/milestone.

### 9.3 Orquestração e Decomposição
**Modelos:** Ornith 9B + Qwen 0.8B + DeepSeek R1 1.5B

**Integração v3.0:** DeepSeek R1 valida se o grafo de dependências entre tasks fragmentadas é acíclico e se não há deadlocks.

### 9.4 Validação de Cobertura
**Modelos:** Qwen 0.8B + Bonsai 27B + DeepSeek R1 1.5B

### 9.5 ⏸️ GATE 3: Aprovação do Plano

### 9.6 💾 Safety: SHA Salvo

---

## 10. FASE 4 — EXECUÇÃO (com Commits Atômicos por Fragmento)

### 10.1 Supervisão e Sequenciamento
**Modelos:** Qwen 0.8B + Ornith 9B + DeepSeek R1 1.5B

**Integração v3.0:** Cada fragmento executado gera um commit atômico. O Reducer consolida os diffs antes do push final.

### 10.2 Reporte de Progresso
**Modelos:** Qwen 0.8B + Llama 1B

### 10.3 Orquestração de Subagents
**Modelos:** Ornith 9B + Qwen 0.8B + DeepSeek R1 1.5B

### 10.4 Ciclo de Vida de Componentes
**Modelos:** Qwen 0.8B + Ornith 9B + DeepSeek R1 1.5B

### 10.5 TDD por Task em Subagents Frescos
**Modelos:** Qwen 0.8B + Ornith 9B + DeepSeek R1 1.5B

### 10.6 Evidência de Verificação
**Modelos:** Qwen 0.8B + Llama 1B + DeepSeek R1 1.5B

### 10.7 Revisão Micro
**Modelos:** Qwen 0.8B + Ornith 9B + DeepSeek R1 1.5B

### 10.8 ⚡ Commits Atômicos por Fragmento

---

## 11. FASE 5 — REVISÃO MACRO (com Auditoria Cross-Fragment)

### 11.1 Revisão Holística
**Modelos:** Ornith 9B + Bonsai 27B + DeepSeek R1 1.5B

**Integração v3.0:** Se o diff total exceder 256K tokens, fragmenta por módulo. O Reducer audita coerência cross-fragment antes do veredito.

### 11.2 Acoplamento
**Modelos:** Ornith 9B + DeepSeek R1 1.5B

### 11.3 Auditoria de Qualidade
**Modelos:** Qwen 0.8B + Ornith 9B + DeepSeek R1 1.5B

### 11.4 Brainstorm de Arquitetura
**Modelos:** Ornith 9B + Qwen 0.8B + DeepSeek R1 1.5B

---

## 12. FASE 6 — ENTREGA (com Verificação de Ferro)

### 12.1 Verification: Evidência Fresca
**Modelos:** Qwen 0.8B + Ornith 9B + DeepSeek R1 1.5B

**Integração v3.0:** Testes extensos são fragmentados por suite. DeepSeek R1 valida se os testes que passaram realmente provam correção, incluindo testes cross-fragment.

### 12.2 Validação Final
**Modelos:** Qwen 0.8B + Ornith 9B + DeepSeek R1 1.5B

### 12.3 Veredito Final
**Modelos:** Ornith 9B + DeepSeek R1 1.5B

### 12.4 Conformidade e Qualidade
**Modelos:** Qwen 0.8B + DeepSeek R1 1.5B

### 12.5 ⏸️ GATE 4: Memória Cerebral

**Integração v3.0:**
```python
# plugins/obsidian_brain/encoder.py (v3.0)
class ObsidianBrainEncoder:
    def encode_session(self, session: Session) -> list[Note]:
        notes = []

        episodic = Note(
            path=f"episodic/session_{session.id}.md",
            content=self._render_episodic(session),
            tags=["session", "episodic", session.project],
            rolling_summary=self.summarizer.generate(session.raw_content)
        )
        notes.append(episodic)

        for concept in session.concepts:
            semantic = Note(
                path=f"semantic/{concept.hash}.md",
                content=self._render_semantic(concept),
                tags=["concept", "semantic"] + concept.domains
            )
            notes.append(semantic)

        state_note = Note(
            path=f"state/{session.task_id}.yaml",
            content=session.state_vector.to_yaml(),
            tags=["state", "vector"]
        )
        notes.append(state_note)

        conflicts = self._detect_conflicts(notes)
        for conflict in conflicts:
            resolution = self._resolve_conflict(conflict)
            notes.append(resolution)

        if session.has_skill_drift:
            repair_plan = self.ornith.generate_repair_scaffold(session)
            notes.append(repair_plan)

        return notes
```

---

## 13. META ORQUESTRADOR GRAN-MASTRE v3.0

### 13.1 Protocolo de Roteamento (com Task Manager)

```yaml
# .opencode/gran_mastre/protocol.yaml (v3.0)
gran_mastre:
  model: "ornith-1.0-9b-q4km"
  reasoning: "explicit"

  routing_policy:
    - condition: "task.type == 'architecture'"
      target: "ornith-1.0-9b-q4km"
      reasoning: "explicit"

    - condition: "task.type == 'coding' AND task.complexity > 0.7"
      target: "ornith-1.0-9b-q4km"
      reasoning: "explicit"

    - condition: "task.type == 'coding' AND task.complexity <= 0.7"
      target: "qwen-3.5-0.8b-q4"
      temperature: 0.4
      json_mode: true

    - condition: "task.type == 'docs' OR task.type == 'summary'"
      target: "bonsai-27b-1bit"
      temperature: 0.5

    - condition: "task.type == 'vision' OR task.type == 'ocr'"
      target: "qwen-3.5-0.8b-q4"
      vision: true

    - condition: "task.type == 'ocr_fast'"
      target: "llama-3.2-1b-q4"
      temperature: 0.2

    - condition: "task.type == 'audit' OR task.type == 'validate'"
      target: "deepseek-r1-1.5b-q4"
      show_thinking: true
      timeout: 15

    - condition: "task.type == 'fragmentation'"
      target: "qwen-3.5-0.8b-q4"
      skills: ["semantic_fragmentation"]

    - condition: "task.type == 'reduction'"
      target: "ornith-1.0-9b-q4km"
      skills: ["semantic_reduction"]

    - condition: "task.type == 'state_management'"
      target: "bonsai-27b-1bit"
      skills: ["rolling_summary", "state_compression"]

    - condition: "default"
      target: "qwen-3.5-0.8b-q4"
      temperature: 0.6
      thinking: true

  task_manager:
    enabled: true
    fragmentation_threshold: 0.8
    overlap_ratio: 0.15
    max_retries: 3
    checkpoint_interval: 1

    models:
      fragmenter: "qwen-3.5-0.8b-q4"
      reducer: "ornith-1.0-9b-q4km"
      state_compressor: "bonsai-27b-1bit"
      border_auditor: "deepseek-r1-1.5b-q4"
```

---

## 14. COGNIÇÃO NEUROLÓGICA NO OBSIDIAN v3.0

| Camada | Função | Formato | Embedding | Raciocínio | Compressão |
|--------|--------|---------|-----------|------------|------------|
| **Episódica** | Sessões | `session_{timestamp}.md` | Qwen 0.8B | — | Bonsai 27B (rolling) |
| **Semântica** | Conceitos | `concept_{hash}.md` | Qwen 0.8B | DeepSeek R1 (links) | — |
| **Procedural** | Skills | `skill_{name}.md` | — | Ornith 9B (auto-cura) | — |
| **Auditória** | Decisões | `audit_{id}.md` | — | DeepSeek R1 (raciocínio) | — |
| **State Vector** | Estado | `state_{task_id}.yaml` | — | — | Bonsai 27B |

---

## 15. MATRIZ DE SEGURANÇA v3.0

| Modelo | Injeção | Vazamento | Hallucination | Mitigação v3.0 |
|--------|---------|-----------|---------------|----------------|
| **Ornith 9B** | MÉDIO | BAIXO | MÉDIO | Sandbox; timeout 30s; reducer audit |
| **Qwen 0.8B** | BAIXO | BAIXO | MÉDIO | Truncamento ativo >200K; fragmentação automática |
| **DeepSeek R1 1.5B** | BAIXO | BAIXO | BAIXO | Apenas auditoria; timeout 15s; border validation |
| **Bonsai 27B** | BAIXO | BAIXO | ALTO | Sem tool calling; apenas docs e summaries |
| **Llama 3.2 1B** | BAIXO | BAIXO | BAIXO | Apenas OCR/classificação; fallback para Qwen |

### 15.1 Riscos Específicos da v3.0

| Risco | Severidade | Mitigação |
|-------|-----------|-----------|
| Reducer falha silenciosa na consolidação | ALTO | DeepSeek R1 audita bordas; score mínimo 0.90 |
| State vector corrompido entre fragmentos | MÉDIO | Checkpoints obrigatórios; validação de estado |
| Overlap excessivo gera redundância | BAIXO | Overlap fixo em 15%; deduplicação no reducer |
| Latência acumulada com muitos fragmentos | MÉDIO | Paralelização de fragmentos independentes |
| Perda de intenção do usuário na fragmentação | MÉDIO | Rolling summary propagado; validação de intenção |

---

## 16. ROADMAP DE IMPLEMENTAÇÃO v3.0

| Fase | Entregável | Prioridade | Modelo Principal | Tempo Est. |
|------|-----------|------------|------------------|------------|
| 1 | Task Manager Core (Fragmenter + Queue + State Vector) | CRÍTICA | Qwen 0.8B | 6h |
| 2 | Semantic Reducer com Auditoria de Bordas | CRÍTICA | Ornith 9B + DeepSeek R1 | 5h |
| 3 | Rolling Summaries e State Compression | CRÍTICA | Bonsai 27B | 3h |
| 4 | Integração com Fases 1-3 do Harness | CRÍTICA | Ornith 9B | 4h |
| 5 | Hooks de Fragmentação e Merge | CRÍTICA | Qwen 0.8B | 2h |
| 6 | MCP Servers (task_state, fragmenter) | IMPORTANTE | Qwen 0.8B | 2h |
| 7 | LSP Bridge com Boundary Analysis | IMPORTANTE | Qwen 0.8B | 3h |
| 8 | Motor de Antropofagia v3.0 | IMPORTANTE | Todos | 5h |
| 9 | MIX Dev Loop e Auto-cura | FUTURA | Ornith 9B | 4h |
| 10 | Tuning do roteamento por feedback | FUTURA | Qwen 0.8B | 3h |

**Tempo total estimado v3.0:** ~37h

---

## 17. CONCLUSÃO DA EVOLUÇÃO v2.0 → v3.0

O SPEC v3.0 estabelece um sistema híbrido de **5 modelos locais** com uma **camada fundamental de Task Manager** que elimina a limitação de contexto como barreira de execução.

| Métrica | v2.0 | v3.0 | Delta |
|---------|------|------|-------|
| **Limite de contexto** | Restrição rígida | **Fragmentação semântica transparente** | **∞ (teórico)** |
| **Coesão cross-task** | Ad-hoc | **Reducer Semântico + Auditoria de Bordas** | **+80%** |
| **Estado entre tasks** | Propagação manual | **State Vector + Rolling Summaries** | **Automático** |
| **Tarefas descartadas** | Possível | **Impossível (por design)** | **0%** |
| **Arsenal extensível** | Básico | **Hooks + Plugins + Skills + MCP + LSP** | **Completo** |
| **Autofagia** | Motor v2.0 | **Motor v3.0 + Helenização + MIX Loop** | **Contínua** |
| **Tempo de implementação** | ~28.5h | ~37h | **+30% (mais robusto)** |

### Próximo passo: Aprovação do **GATE 1** para iniciar a implementação da Fase 1 com o stack v3.0 completo.

---

**Status do documento:** `RASCUNHO COMPLETO v3.0` → Aguardando `GATE 1: APROVAÇÃO DA DIREÇÃO`

---

*Documento gerado em: 2026-08-09*
*Versão: 3.0.0*
*Sistema: OpenCode Harness + Meta-Orquestrador Gran-Mestre + Task Manager de Fragmentação Semântica*
*Modelos: Ornith 9B | Bonsai 27B | Qwen 3.5 0.8B | Llama 3.2 1B | DeepSeek-R1 1.5B*
*Arsenal: Hooks | Plugins | Skills | Subagents | MCP | LSP | MIX Dev Loop*
