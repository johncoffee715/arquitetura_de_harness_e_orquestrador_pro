# Requirements: Global Harness Refactoring

## Version: v0.1.0

## Project: Global Harness Refactoring

---

## 1. Core Orchestration Requirements

### HARNESS-01: Gran-Mestre Meta-Orchestrator
**Priority:** Critical
**Complexity:** COMPLEX
**Description:** Implement the Gran-Mestre meta-orchestrator that serves as the single entry point for all user requests, classifies complexity, and delegates to appropriate subagents/skills.

**Acceptance Criteria:**
- [ ] Classifies requests by complexity (TRIVIAL/SIMPLE/MEDIUM/COMPLEX/CRITICAL/FEATURE/MIX)
- [ ] Routes to appropriate pipeline based on complexity
- [ ] Manages 6-phase workflow (Discovery → Contract → Plan → Execution → Macro Review → Delivery)
- [ ] Saves SHA checkpoint before Phase 4
- [ ] Implements rollback on failure
- [ ] Logs metrics to CONTEXT.md after each phase

### HARNESS-02: Model Provider (Hot-Swap)
**Priority:** Critical
**Complexity:** COMPLEX
**Description:** Implement model provider layer that supports hot-swapping between local and cloud models based on task requirements.

**Acceptance Criteria:**
- [ ] Supports local models (Ornith, Bonsai, Nanbeige, LFM)
- [ ] Supports cloud models (MoE fallback for Phase 5/6)
- [ ] Hot-swap between models without downtime
- [ ] Route-based model selection (TRIVIAL→SIMPLE use light models, COMPLEX/CRITICAL→FEATURE use Bonsai/MoE)
- [ ] Asynchronous layer offloading

### HARNESS-03: VRAM Allocation Manager
**Priority:** High
**Complexity:** MEDIUM
**Description:** Manage VRAM allocation on MI50 16GB HBM2 to prevent overflow and maximize throughput.

**Acceptance Criteria:**
- [ ] Allocate ~11.9GB for model weights (stable)
- [ ] Reserve ~4.1GB for KV Cache (dynamic)
- [ ] Prevent CPU offloading (n_gpu_layers = total for GPU)
- [ ] Support multiple parallel slots for Bonsai 27B 1-bit
- [ ] Monitor and log VRAM usage per phase

---

## 2. Pipeline Phase Requirements

### HARNESS-04: Phase 1 - Discovery
**Priority:** High
**Complexity:** SIMPLE
**Description:** Light decomposition of user request, context gathering.

**Acceptance Criteria:**
- [ ] Decompose request into sub-tasks
- [ ] Gather context from codebase, docs, research
- [ ] Apply scope filtering
- [ ] Present direction for user approval (Gate 1)

### HARNESS-05: Phase 2 - Contract
**Priority:** High
**Complexity:** MEDIUM
**Description:** Transform approved direction into design specification.

**Acceptance Criteria:**
- [ ] Generate design doc/SPEC.md
- [ ] Validate spec against original request (filter)
- [ ] Audit result against quality criteria (filter)
- [ ] Present spec for user approval (Gate 2)

### HARNESS-06: Phase 3 - Plan
**Priority:** High
**Complexity:** MEDIUM
**Description:** Create TDD-based plan with atomic tasks.

**Acceptance Criteria:**
- [ ] TDD tasks with test-first approach
- [ ] Bite-sized atomic tasks
- [ ] Complete code for each task
- [ ] Validate test coverage and verifiability (filter)
- [ ] Save SHA checkpoint (Safety Protocol)
- [ ] Present plan for user approval (Gate 3)

### HARNESS-07: Phase 4 - Execution
**Priority:** Critical
**Complexity:** COMPLEX
**Description:** Execute tasks with atomic commits, manage subagent lifecycle.

**Acceptance Criteria:**
- [ ] Supervised task execution
- [ ] Atomic git commits per task
- [ ] Fresh subagent per task
- [ ] TDD loop per task
- [ ] Verification evidence per task (filter)
- [ ] Micro-review per task (filter)
- [ ] Progress reporting to Gran-Mestre
- [ ] No gates — commits atomic, progress visible

### HARNESS-08: Phase 5 - Macro Review
**Priority:** High
**Complexity:** COMPLEX
**Description:** Holistic review of total diff, cross-task coherence.

**Acceptance Criteria:**
- [ ] Review total diff for coherence
- [ ] Check cross-task coupling (filter macro)
- [ ] Audit against quality criteria (filter macro)
- [ ] Validate architecture alignment with contract (filter macro)
- [ ] Cloud MoE audit for architectural abstraction

### HARNESS-09: Phase 6 - Delivery
**Priority:** High
**Complexity:** MEDIUM
**Description:** Final verification and cerebral memory archive.

**Acceptance Criteria:**
- [ ] Fresh iron evidence verification (filter)
- [ ] Final validation against original request (filter)
- [ ] Audit iron evidence, emit final compliance verdict (filter)
- [ ] Archive to cerebral memory (Obsidian)
- [ ] Present final report (Gate 4)

---

## 3. Safety & Governance Requirements

### HARNESS-10: Safety Protocol
**Priority:** Critical
**Complexity:** MEDIUM
**Description:** Implement comprehensive safety protocol with SHA checkpointing and rollback.

**Acceptance Criteria:**
- [ ] Save SHA before Phase 4 execution
- [ ] Store SHA in CONTEXT.md
- [ ] Never leave repo in partial state
- [ ] Automatic rollback on failure
- [ ] Git diff --quiet check before cloud offloading
- [ ] Local validator (Hestia) intercepts cloud responses

### HARNESS-11: Policy Engine
**Priority:** High
**Complexity:** MEDIUM
**Description:** Implement policy-as-code for security, compliance, and cost control.

**Acceptance Criteria:**
- [ ] Policy-as-code implementation
- [ ] RBAC/ABAC for agent access control
- [ ] Compliance rules as code
- [ ] Cost monitoring and control
- [ ] Human-in-the-loop gates (HITL/HOTL)

### HARNESS-12: Observability
**Priority:** High
**Complexity:** MEDIUM
**Description:** Implement comprehensive observability with MELT and OpenTelemetry.

**Acceptance Criteria:**
- [ ] Metrics logging to CONTEXT.md after each phase
- [ ] OpenTelemetry integration
- [ ] MELT data (Metrics, Events, Logs, Traces)
- [ ] Semantic conventions for GenAI
- [ ] Dashboard for monitoring multi-agent workflows

---

## 4. Integration Requirements

### HARNESS-13: Obsidian Memory Integration
**Priority:** High
**Complexity:** MEDIUM
**Description:** Integrate Obsidian as persistent cognitive memory via MCP server.

**Acceptance Criteria:**
- [ ] MCP server for Obsidian vault access
- [ ] search_vault/append_note tools
- [ ] Cognitive memory persists across sessions
- [ ] Memory not inflated in Gran-Mestre context
- [ ] LangGraph checkpoint persistence via PostgreSQL

### HARNESS-14: Tool Registry
**Priority:** High
**Complexity:** MEDIUM
**Description:** Implement tool registry with MCP servers and OpenAPI specs.

**Acceptance Criteria:**
- [ ] MCP server discovery and registration
- [ ] OpenAPI spec integration
- [ ] Dynamic tool listing
- [ ] JSON Schema validation for tool inputs
- [ ] Tool access control

### HARNESS-15: Dev Loop Integration
**Priority:** High
**Complexity:** COMPLEX
**Description:** Integrate Dev Loop methodology (N1 ReAct, N2 Mini Loop, N3 Human Loop).

**Acceptance Criteria:**
- [ ] N1: ReAct for trivial tasks (1-3 files, 3 iterations max)
- [ ] N2: Mini Loop for features (spec → TDD → commit → merge)
- [ ] N3: Human Loop for architectural decisions (Decide → Metrics → Triage → Plan → PR → Decide)
- [ ] Automatic escalation between levels
- [ ] Metrics logging for each iteration

---

## 5. External Integration Requirements

### HARNESS-16: oh-my-opencode-slim Integration
**Priority:** Medium
**Complexity:** MEDIUM
**Description:** Integrate with oh-my-opencode-slim repository.

**Acceptance Criteria:**
- [ ] Analyze existing harness structure
- [ ] Identify refactoring targets
- [ ] Apply Gran-Mestre 6-phase pipeline
- [ ] Maintain backward compatibility

### HARNESS-17: Referenced Repos Integration
**Priority:** Medium
**Complexity:** MEDIUM
**Description:** Integrate with referenced GitHub repositories.

**Acceptance Criteria:**
- [ ] pi (earendil-works/pi) — AI pipeline integration
- [ ] RuView (ruvnet/RuView) — Review tool integration
- [ ] openship (oblien/openship) — Deployment integration
- [ ] code-review-graph (tirth8205) — Code review graph integration
- [ ] I Have ADHD (ayghri/i-have-adhd) — Attention-focused workflow
- [ ] Orca (stablyai/orca) — Model integration
- [ ] OmniRoute (diegosouzapw/OmniRoute) — Routing integration
- [ ] Skills (mattpocock/skills) — Skill integration
- [ ] WorldMonitor (koala73/worldmonitor) — Monitoring integration
- [ ] AI Agent Book (bojieli/ai-agent-book) — Knowledge integration
- [ ] onp-spec-driven (onovoprogramador/onp-spec-driven) — Spec-driven development integration

---

## 6. Quality Requirements

### HARNESS-18: GBNF Grammar Enforcement
**Priority:** High
**Complexity:** MEDIUM
**Description:** Apply strict GBNF grammars to ensure JSON/code output validity.

**Acceptance Criteria:**
- [ ] GBNF grammar for JSON outputs
- [ ] GBNF grammar for code outputs
- [ ] Prevent syntax errors from 1-bit quantization
- [ ] Grammar validation before output acceptance

### HARNESS-19: Thinking Token Limitation
**Priority:** Medium
**Complexity:** SIMPLE
**Description:** Regulate thinking tokens to prevent logic divergence in 1-bit models.

**Acceptance Criteria:**
- [ ] Limit thinking tokens per phase
- [ ] Configurable thinking depth
- [ ] Prevent logic drift in parallel slots

### HARNESS-20: Auto-Correction Loop
**Priority:** High
**Complexity:** MEDIUM
**Description:** Implement auto-correction for 1-bit model errors using parallel validation slots.

**Acceptance Criteria:**
- [ ] Bonsai 1-bit generates code/contract in one slot
- [ ] Parallel slot validates for logical contradictions
- [ ] Ornith-1.0 corrects Bonsai errors via Code Repair
- [ ] Deterministic Monitoring for error detection
- [ ] Cloud MoE fallback after 3 consecutive failures

---

## Traceability

| Requirement | Phase | Source Document |
|------------|-------|-----------------|
| HARNESS-01 | FASE 1-6 | engenharia de harness.md §1, §3 |
| HARNESS-02 | FASE 4-5 | engenharia de harness.md §4 |
| HARNESS-03 | FASE 4 | engenharia de harness.md §4, §7 |
| HARNESS-04 | FASE 1 | engenharia de harness.md §2, FASE 1 |
| HARNESS-05 | FASE 2 | engenharia de harness.md §2, FASE 2 |
| HARNESS-06 | FASE 3 | engenharia de harness.md §2, FASE 3 |
| HARNESS-07 | FASE 4 | engenharia de harness.md §2, FASE 4 |
| HARNESS-08 | FASE 5 | engenharia de harness.md §2, FASE 5 |
| HARNESS-09 | FASE 6 | engenharia de harness.md §2, FASE 6 |
| HARNESS-10 | FASE 3, 4, 6 | engenharia de harness.md §8, §9 |
| HARNESS-11 | All | Orquestrador de IA §3 |
| HARNESS-12 | All | Orquestrador de IA §3.1 |
| HARNESS-13 | FASE 6 | engenharia de harness.md §1, §4 |
| HARNESS-14 | All | Orquestrador de IA §1, §2 |
| HARNESS-15 | FASE 1-4 | Dev Loop skill |
| HARNESS-16-17 | FASE 1 | executar autofagia e helenizaçao.md |
| HARNESS-18-20 | FASE 4-5 | engenharia de harness.md §4, §7 |

## Definition of Done

All requirements marked as [x] in the acceptance criteria above. All phases execute successfully with passing tests. Safety protocol verified. Observability metrics logged. Cerebral memory archived.