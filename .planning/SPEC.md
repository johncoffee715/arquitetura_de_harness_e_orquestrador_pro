# SPEC: Global Harness Architecture

## Project: Global Harness Refactoring

## Version: 0.1.0

## Status: Draft

---

## 1. Purpose & Scope

### 1.1 Purpose

This specification defines the architecture for a global refactoring of the OpenCode harness to implement a hybrid AI orchestration system. The system manages models locally (MI50 16GB HBM2) and in the cloud, following the Gran-Mestre 6-phase pipeline architecture with Dev Loop methodology.

### 1.2 Scope

**In Scope:**
- Gran-Mestre meta-orchestrator with 6-phase pipeline
- Model Provider layer (local/cloud hot-swap)
- VRAM allocation manager for MI50
- Safety protocol (SHA checkpointing, rollback)
- Observability layer (OpenTelemetry, MELT)
- Policy engine (Policy-as-Code, RBAC/ABAC)
- Tool registry (MCP servers, OpenAPI specs)
- Obsidian memory integration via MCP
- Dev Loop integration (N1/N2/N3)
- GBNF grammar enforcement
- Auto-correction loop
- Integration with oh-my-opencode-slim and referenced repos

**Out of Scope:**
- Training new models
- Real-time inference serving
- Full cloud deployment

---

## 2. Architecture Overview

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER REQUEST                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                GRAN-MESTRE (Ornith-1.0 9B)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ContextAnalyzer — Classifies Complexity            │  │
│  │  TRIVIAL | SIMPLE | MEDIUM | COMPLEX/CRITICAL        │  │
│  │  FEATURE | MIX                                       │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              MODEL PROVIDER (Hot-Swap Layer)                │
├─────────────────────────────────────────────────────────────┤
│  Local: Ornith-1.0 9B  │  Bonsai 27B 1-bit  │  LFM/Nanbeige │
│  Cloud: MoE (fallback only)                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              6-PHASE PIPELINE (LangGraph)                   │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: Discovery   │  Phase 2: Contract  │  Phase 3: Plan │
│  Phase 4: Execution   │  Phase 5: Review    │  Phase 6: Delivery │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│            OBSIDIAN MEMORY (via MCP Server)                 │
│  Persistent cognitive memory across sessions                │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Model Allocation & VRAM Budget

| Model | Size | VRAM | Role | Phase Usage |
|-------|------|------|------|-------------|
| Ornith-1.0 9B | Q4_K_M | ~5.5GB | Gran-Mestre | All phases (control) |
| Bonsai 27B 1-bit | 1-bit | ~3.9GB | Heavy execution | Phase 2, 3, 4 |
| Nanbeige 3B | 4-bit | ~1.4GB | Filter/validation | Phases 1-3, 4-5 |
| LFM 2.5-1.6B | FP8 | ~1.1GB | Instant checks | Phases 1-2, 4 |
| MoE (Cloud) | Varies | N/A | Architectural audit | Phase 5, 6 (fallback) |

**Total model VRAM:** ~11.9GB
**KV Cache reserve:** ~4.1GB
**Total:** ~16GB (MI50 capacity)

### 2.3 Safety Protocol Flow

```
Phase 3 (Plan) → Save SHA to CONTEXT.md
                │
                ▼
Phase 4 (Execution) → Check git diff --quiet
                      │
                      ▼
                    Execute tasks
                      │
                      ▼
                Any failure? → Rollback to SHA
                      │
                      ▼
                Phase 5 (Review) → Cloud MoE audit
                      │
                      ▼
                Phase 6 (Delivery) → Final verification
```

---

## 3. Component Specifications

### 3.1 Gran-Mestre Meta-Orchestrator

**Role:** Single entry point for all user requests. Classifies complexity and delegates.

**Responsibilities:**
- Classify requests by complexity (TRIVIAL/SIMPLE/MEDIUM/COMPLEX/CRITICAL/FEATURE/MIX)
- Route to appropriate pipeline
- Manage 6-phase workflow
- Save SHA checkpoint before Phase 4
- Implement rollback on failure
- Log metrics to CONTEXT.md after each phase
- Delegate to subagents/skills from global registry

**Implementation:**
- Language: TypeScript
- Framework: LangGraph (event-driven state management)
- Runtime: Node.js
- Tools: bash, Python, file system
- Memory: Obsidian via MCP server
- Persistence: langgraph-checkpoint-postgres

**Complexity Routing Table:**

| Route | Pipeline | Agentes | Model |
|-------|----------|---------|-------|
| TRIVIAL | Execução direta | 1 | LFM 2.5 |
| SIMPLE | Mini-plano | 1-2 | Nanbeige 3B |
| MEDIUM | 3 agentes | 3 | Bonsai 27B 1-bit |
| COMPLEX/CRITICAL | 5 agentes | 5 | Bonsai + Ornith |
| FEATURE | Cascata (6 fases) | 6+ | Ornith + Bonsai |
| MIX | Cascata (6 fases) | arsenal global | Ornith + Bonsai + MoE |

### 3.2 Model Provider (Hot-Swap Layer)

**Role:** Abstract model access, support local/cloud hot-swap.

**Responsibilities:**
- Support local models (Ornith, Bonsai, Nanbeige, LFM)
- Support cloud models (MoE fallback)
- Hot-swap between models without downtime
- Route-based model selection
- Asynchronous layer offloading

**Implementation:**
- Language: TypeScript
- Interface: OpenAI-compatible API
- Local backend: llama.cpp with --tool-call-parser qwen3_xml
- Cloud backend: Model Provider abstraction
- Configuration: YAML/JSON model configs

**API Contract:**
```typescript
interface ModelProvider {
  getModel(route: ComplexityRoute): ModelInstance;
  hotSwap(oldModel: string, newModel: string): Promise<void>;
  getVRAMUsage(): VRAMInfo;
  checkAvailability(model: string): boolean;
}
```

### 3.3 VRAM Allocation Manager

**Role:** Manage VRAM on MI50 16GB HBM2.

**Responsibilities:**
- Allocate ~11.9GB for model weights
- Reserve ~4.1GB for KV Cache
- Prevent CPU offloading (n_gpu_layers = total)
- Support multiple parallel slots
- Monitor and log VRAM usage

**Implementation:**
- Language: Python (for llama.cpp integration)
- Backend: llama.cpp with parallel slots (-np)
- Monitoring: GPU-Z, rocm-smi
- Logging: CONTEXT.md metrics

**VRAM Allocation Strategy:**
- Ornith-1.0 9B: 5.5GB (static)
- Bonsai 27B 1-bit: 3.9GB (static, multiple slots)
- Nanbeige/LFM: 2.5GB (static, instant check)
- KV Cache: 4.1GB (dynamic)

### 3.4 6-Phase Pipeline

#### Phase 1: Discovery
**Goal:** Light decomposition, context gathering.

**Activities:**
- Decompose request into sub-tasks
- Gather context from codebase, docs, research
- Apply scope filtering
- Present direction for Gate 1 approval

**Model:** Ornith-1.0 9B (Gran-Mestre)
**Filters:** LFM 2.5, Nanbeige 3B

**Acceptance Criteria:**
- [ ] Request decomposed
- [ ] Context gathered
- [ ] Direction presented for approval

#### Phase 2: Contract
**Goal:** Transform direction into design doc/spec.

**Activities:**
- Generate design doc/SPEC.md
- Validate spec against original request
- Audit result against quality criteria
- Present spec for Gate 2 approval

**Model:** Bonsai 27B 1-bit (generation), Ornith-1.0 9B (validation)
**Filters:** Nanbeige 3B

**Acceptance Criteria:**
- [ ] SPEC.md created
- [ ] Spec validated
- [ ] Spec approved at Gate 2

#### Phase 3: Plan
**Goal:** Create TDD tasks, atomic commits, safety checkpoint.

**Activities:**
- TDD tasks with test-first approach
- Bite-sized atomic tasks
- Complete code for each task
- Validate test coverage and verifiability
- Save SHA checkpoint (Safety Protocol)
- Present plan for Gate 3 approval

**Model:** Bonsai 27B 1-bit (planning), Ornith-1.0 9B (validation)
**Filters:** LFM 2.5, Nanbeige 3B

**Safety Protocol:** SHA saved here. Phases 1-3 don't touch production code.

**Acceptance Criteria:**
- [ ] PLAN.md created with atomic tasks
- [ ] TDD tests defined
- [ ] SHA checkpoint saved
- [ ] Plan approved at Gate 3

#### Phase 4: Execution
**Goal:** Execute tasks with atomic commits, manage subagent lifecycle.

**Activities:**
- Supervised task execution
- Atomic git commits per task
- Fresh subagent per task
- TDD loop per task
- Verification evidence per task
- Micro-review per task
- Progress reporting to Gran-Mestre

**Model:** Bonsai 27B 1-bit (execution), Ornith-1.0 9B (supervision)
**Filters:** LFM 2.5 (commit validation), Nanbeige 3B (micro-review)

**Note:** No gates — commits atomic, progress visible.

**Acceptance Criteria:**
- [ ] All tasks executed
- [ ] Atomic commits per task
- [ ] Tests passing
- [ ] No partial state

#### Phase 5: Macro Review
**Goal:** Holistic review, cross-task coherence, cloud audit.

**Activities:**
- Review total diff for coherence
- Check cross-task coupling
- Audit against quality criteria
- Validate architecture alignment with contract
- Cloud MoE audit for architectural abstraction

**Model:** Ornith-1.0 9B (local review), MoE (cloud audit)
**Filters:** Nanbeige 3B

**Acceptance Criteria:**
- [ ] Total diff reviewed
- [ ] Cross-task coherence verified
- [ ] Architecture aligned with contract
- [ ] Cloud audit complete

#### Phase 6: Delivery
**Goal:** Final verification, safety validation, cerebral memory archive.

**Activities:**
- Fresh iron evidence verification
- Final validation against original request
- Audit iron evidence, emit final compliance verdict
- Archive to cerebral memory (Obsidian)
- Present final report at Gate 4

**Model:** Ornith-1.0 9B (verification), MoE (final verdict)
**Filters:** LFM 2.5

**Acceptance Criteria:**
- [ ] Iron evidence verified
- [ ] Final validation passed
- [ ] Compliance verdict emitted
- [ ] Cerebral memory archived
- [ ] Final report presented

### 3.5 Safety Protocol

**Role:** Ensure no partial state, enable rollback.

**Components:**
- SHA checkpoint (Phase 3)
- Git diff --quiet check (before Phase 4)
- Rollback on failure
- Local validator (Hestia) intercepts cloud responses
- Never leave repo in partial state

**Implementation:**
```bash
# Save SHA
git rev-parse HEAD > .git_harness_sha

# Check before execution
git diff --quiet

# Rollback on failure
git reset --hard $(cat .git_harness_sha)
```

### 3.6 Observability Layer

**Role:** Track metrics, events, logs, traces across pipeline.

**Components:**
- Metrics logging to CONTEXT.md after each phase
- OpenTelemetry integration
- MELT data (Metrics, Events, Logs, Traces)
- Semantic conventions for GenAI

**Metrics Format:**
```markdown
[Metrics] Phase: {discover|contract|plan|execute|review|deliver}
[Metrics] Route: {TRIVIAL|SIMPLE|MEDIUM|COMPLEX|CRITICAL|FEATURE|MIX}
[Metrics] Status: {success|escalated|failed}
```

### 3.7 Policy Engine

**Role:** Apply security, compliance, and cost policies.

**Components:**
- Policy-as-code (single source of truth)
- RBAC (Role-Based Access Control)
- ABAC (Attribute-Based Access Control)
- Human-in-the-loop gates (HITL/HOTL)

### 3.8 Tool Registry

**Role:** Catalog of APIs and tools agents can use.

**Components:**
- MCP Servers (discovery via tools/list)
- OpenAPI specs
- JSON Schema validation
- Tool access control

### 3.9 Obsidian Memory Integration

**Role:** Persistent cognitive memory across sessions.

**Components:**
- MCP server for Obsidian vault access
- search_vault/append_note tools
- Cognitive memory persists across sessions
- Not inflated in Gran-Mestre context
- LangGraph checkpoint persistence via PostgreSQL

### 3.10 Dev Loop Integration

**Role:** 3-level development iteration with automatic escalation.

**Components:**
- N1: ReAct (Think → Act → Observe → Repeat) for trivial tasks
- N2: Mini Loop (Spec → TDD → Commit → Merge) for features
- N3: Human Loop (Decide → Metrics → Triage → Plan → PR → Decide) for architectural decisions
- Automatic escalation between levels
- Metrics logging for each iteration

### 3.11 GBNF Grammar Enforcement

**Role:** Ensure JSON/code output validity from 1-bit models.

**Components:**
- GBNF grammar for JSON outputs
- GBNF grammar for code outputs
- Grammar validation before output acceptance
- Prevent syntax errors from quantization

### 3.12 Auto-Correction Loop

**Role:** Correct 1-bit model errors using parallel validation slots.

**Components:**
- Bonsai 1-bit generates code/contract in one slot
- Parallel slot validates for logical contradictions
- Ornith-1.0 corrects Bonsai errors via Code Repair
- Deterministic Monitoring for error detection
- Cloud MoE fallback after 3 consecutive failures

---

## 4. Integration Points

### 4.1 oh-my-opencode-slim
- Analyze existing harness structure
- Apply Gran-Mestre 6-phase pipeline
- Maintain backward compatibility

### 4.2 Referenced Repositories
- **pi (earendil-works/pi):** AI pipeline integration
- **RuView (ruvnet/RuView):** Review tool integration
- **openship (oblien/openship):** Deployment integration
- **code-review-graph (tirth8205):** Code review graph integration
- **I Have ADHD (ayghri/i-have-adhd):** Attention-focused workflow
- **Orca (stablyai/orca):** Model integration
- **OmniRoute (diegosouzapw/OmniRoute):** Routing integration
- **Skills (mattpocock/skills):** Skill integration
- **WorldMonitor (koala73/worldmonitor):** Monitoring integration
- **AI Agent Book (bojieli/ai-agent-book):** Knowledge integration
- **onp-spec-driven (onovoprogramador/onp-spec-driven):** Spec-driven development

---

## 5. Data Flow

### 5.1 Request Flow
```
User Request → Gran-Mestre (Ornith-1.0 9B)
    → ContextAnalyzer classifies complexity
    → Model Provider selects appropriate model
    → 6-Phase Pipeline executes
    → Obsidian Memory archives results
    → Final Report to User
```

### 5.2 Safety Flow
```
Phase 3 (Plan) → Save SHA to CONTEXT.md
    → Phase 4 (Execution) → Check git diff --quiet
    → Execute tasks with atomic commits
    → Any failure → Rollback to SHA
    → Phase 5 (Review) → Cloud MoE audit
    → Phase 6 (Delivery) → Final verification
```

### 5.3 Memory Flow
```
User Request → Gran-Mestre
    → Obsidian Memory (via MCP) → search_vault
    → Context from past sessions
    → Execute pipeline
    → Success → Obsidian Memory → append_note
    → Cerebral Memory Archive (Gate 4)
```

---

## 6. Non-Functional Requirements

### 6.1 Performance
- Gran-Mestre routing decisions in milliseconds
- Bonsai 1-bit generates multiple slots in parallel
- LFM/Nanbeige instant checks (< 100ms)

### 6.2 Reliability
- Safety protocol prevents partial state
- Rollback on any failure
- Hestia local validator intercepts cloud responses

### 6.3 Scalability
- Hot-swap model provider
- Parallel slots for Bonsai 1-bit
- Cloud MoE for heavy lifting (Phase 5/6 only)

### 6.4 Security
- Zero-trust communication between agents
- ABAC for access control
- Policy-as-code for compliance
- Data lineage tracking

---

## 7. Validation Criteria

### 7.1 Spec Validation (Gate 2)
- [ ] Spec covers all requirements from REQUIREMENTS.md
- [ ] Architecture components are well-defined
- [ ] Safety protocol is complete
- [ ] Integration points are documented
- [ ] Non-functional requirements are addressed

### 7.2 Plan Validation (Gate 3)
- [ ] PLAN.md covers all spec components
- [ ] TDD tests are defined for each task
- [ ] Dependency graph is correct
- [ ] SHA checkpoint is saved
- [ ] Test coverage is validated

---

## 8. Open Questions

1. Should the harness support GPU passthrough for Docker containers?
2. How to handle model version conflicts between local and cloud?
3. What is the failover strategy if both local and cloud models are unavailable?
4. How to handle VRAM fragmentation with multiple parallel slots?

---

## 9. References

1. `engenharia de harness.md` — Hardware hybrid harness architecture
2. `Orquestrador de IA de Forma Profissional.md` — Professional AI orchestrator architecture
3. `executar autofagia e helenizaçao.md` — Autofagia and helenization execution plan
4. `gran-mestre/SKILL.md` — Gran-Mestre meta-orchestrator skill
5. `dev-loop/SKILL.md` — Dev Loop methodology
6. `fable-judge/SKILL.md` — Adversarial verification
7. `hestia/SKILL.md` — Validation agent
8. Various GitHub repositories referenced in document 3