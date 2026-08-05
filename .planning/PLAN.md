# PLAN: Global Harness Refactoring

## Project: Global Harness Refactoring

## Phase: 1

## Status: Planning

---

## Phase Goal

Implement a global refactoring of the OpenCode harness to create a hybrid AI orchestration system that manages models locally (MI50 16GB HBM2) and in the cloud, following the Gran-Mestre 6-phase pipeline architecture with Dev Loop methodology (N3 - Human Loop for architectural decisions).

---

## Assumptions

1. The existing OpenCode harness structure in `/mnt/dados/opencode/` provides the base
2. The three reference documents define the target architecture
3. The MI50 16GB HBM2 hardware constraints are real (VRAM budget: ~11.9GB models, ~4.1GB KV Cache)
4. LangGraph is the preferred orchestration framework
5. Obsidian is used for persistent cognitive memory via MCP
6. The Dev Loop N3 (Human Loop) is required for architectural decisions

## Evidence

- `engenharia de harness.md` defines the hybrid architecture, model allocation, and 6-phase pipeline
- `Orquestrador de IA de Forma Profissional.md` defines the 4-pillar architecture, orchestration models, and governance
- `executar autofagia e helenizaçao.md` defines the MIX mode and Dev Loop usage with repository references

---

## Tasks

### Task 1.1: Map Existing Harness Structure
**Description:** Analyze the current OpenCode harness structure to understand what exists and what needs to be refactored.

**Acceptance Criteria:**
- [ ] Map skills directory structure
- [ ] Map agents directory structure
- [ ] Map commands directory structure
- [ ] Map config files (opencode.json, etc.)
- [ ] Identify existing Gran-Mestre implementation
- [ ] Identify integration points with oh-my-opencode-slim

**Subagent:** explore
**Model:** Ornith-1.0 9B (Gran-Mestre)
**TDD:** No (analysis task)

### Task 1.2: Analyze oh-my-opencode-slim Repository
**Description:** Clone and analyze the oh-my-opencode-slim repository to understand its structure and identify refactoring targets.

**Acceptance Criteria:**
- [ ] Clone repository from GitHub
- [ ] Analyze directory structure
- [ ] Identify harness components
- [ ] Map to Gran-Mestre 6-phase pipeline
- [ ] Identify backward compatibility requirements

**Subagent:** librarian
**Model:** Nanbeige 3B
**TDD:** No (analysis task)

### Task 1.3: Extract Requirements from Reference Documents
**Description:** Systematically extract all requirements from the three reference documents and organize them into a structured format.

**Acceptance Criteria:**
- [ ] Requirements from engenharia de harness.md extracted
- [ ] Requirements from Orquestrador de IA.md extracted
- [ ] Requirements from executar autofagia.md extracted
- [ ] Requirements categorized by priority and complexity
- [ ] Requirements traced to source documents

**Subagent:** explore
**Model:** LFM 2.5-1.6B
**TDD:** No (analysis task)

### Task 1.4: Define Target Architecture
**Description:** Define the target architecture for the refactored harness based on the extracted requirements.

**Acceptance Criteria:**
- [ ] Architecture diagram created
- [ ] Component boundaries defined
- [ ] Model allocation strategy documented
- [ ] Safety protocol flow defined
- [ ] Integration points identified
- [ ] Data flow documented

**Subagent:** oracle
**Model:** Bonsai 27B 1-bit
**TDD:** No (design task)

### Task 1.5: Present Direction for Gate 1 Approval
**Description:** Present the discovered architecture and direction for user approval at Gate 1.

**Acceptance Criteria:**
- [ ] Architecture summary presented
- [ ] Model allocation documented
- [ ] Safety protocol documented
- [ ] Gate 1 approval received

**Subagent:** General (human interaction)
**Model:** Ornith-1.0 9B
**TDD:** No (presentation task)

---

## Dependencies

- None (this is the first phase)

---

## Safety Protocol

- SHA checkpoint will be saved at the end of Phase 3 (before Phase 4 execution)
- Phases 1-3 do not touch production code
- Git diff --quiet check before Phase 4

---

## Metrics

```
[Metrics] Phase: discover
[Metrics] Route: MIX
[Metrics] Status: pending
```

---

## Phase 2: Contract

### Task 2.1: Create SPEC.md
**Description:** Create the detailed specification document based on the target architecture.

**Acceptance Criteria:**
- [ ] SPEC.md created with architecture overview
- [ ] All components specified
- [ ] API contracts defined
- [ ] Safety protocol fully specified
- [ ] Integration points documented

### Task 2.2: Validate Spec Against Requirements
**Description:** Validate the SPEC.md against the REQUIREMENTS.md.

**Acceptance Criteria:**
- [ ] All requirements covered in SPEC.md
- [ ] No requirements omitted
- [ ] Traceability matrix created
- [ ] Validation report generated

### Task 2.3: Present Spec for Gate 2 Approval
**Description:** Present the SPEC.md for user approval at Gate 2.

**Acceptance Criteria:**
- [ ] SPEC.md presented
- [ ] Gate 2 approval received

---

## Phase 3: Plan

### Task 3.1: Break Down SPEC into Atomic Tasks
**Description:** Break down the SPEC.md into atomic TDD tasks.

**Acceptance Criteria:**
- [ ] All components broken down into tasks
- [ ] Each task is atomic (1-3 files)
- [ ] Dependency graph created
- [ ] Task prioritization defined

### Task 3.2: Create TDD Tests for Each Task
**Description:** Create test-first plans for each atomic task.

**Acceptance Criteria:**
- [ ] Test files defined for each task
- [ ] Test cases specified
- [ ] Test coverage targets defined
- [ ] Verification criteria documented

### Task 3.3: Save SHA Checkpoint
**Description:** Save the current SHA as a safety checkpoint before Phase 4.

**Acceptance Criteria:**
- [ ] SHA saved to CONTEXT.md
- [ ] Git diff --quiet verified clean
- [ ] Safety protocol active

### Task 3.4: Present Plan for Gate 3 Approval
**Description:** Present the PLAN.md for user approval at Gate 3.

**Acceptance Criteria:**
- [ ] PLAN.md presented
- [ ] Gate 3 approval received

---

## Phase 4: Execution

### Task 4.1: Implement Gran-Mestre Meta-Orchestrator
**Description:** Implement the Gran-Mestre meta-orchestrator with complexity classification and routing.

**Acceptance Criteria:**
- [ ] ContextAnalyzer implemented
- [ ] Complexity routing implemented
- [ ] 6-phase pipeline management
- [ ] SHA checkpoint management
- [ ] Rollback mechanism
- [ ] Metrics logging

### Task 4.2: Implement Model Provider Layer
**Description:** Implement the Model Provider layer for local/cloud hot-swap.

**Acceptance Criteria:**
- [ ] Local model support
- [ ] Cloud model support
- [ ] Hot-swap capability
- [ ] Route-based selection
- [ ] Asynchronous offloading

### Task 4.3: Implement VRAM Allocation Manager
**Description:** Implement VRAM allocation manager for MI50.

**Acceptance Criteria:**
- [ ] VRAM budget management
- [ ] CPU offload prevention
- [ ] Parallel slot support
- [ ] Monitoring and logging

### Task 4.4: Implement Safety Protocol
**Description:** Implement the safety protocol with SHA checkpointing and rollback.

**Acceptance Criteria:**
- [ ] SHA checkpoint saving
- [ ] Git diff check
- [ ] Rollback mechanism
- [ ] Hestia validator integration

### Task 4.5: Implement Observability Layer
**Description:** Implement the observability layer with OpenTelemetry and MELT.

**Acceptance Criteria:**
- [ ] Metrics logging to CONTEXT.md
- [ ] OpenTelemetry integration
- [ ] MELT data tracking
- [ ] Semantic conventions

### Task 4.6: Implement Policy Engine
**Description:** Implement the policy engine with Policy-as-Code and RBAC/ABAC.

**Acceptance Criteria:**
- [ ] Policy-as-code implementation
- [ ] RBAC/ABAC
- [ ] HITL/HOTL gates
- [ ] Compliance rules

### Task 4.7: Implement Tool Registry
**Description:** Implement the tool registry with MCP servers and OpenAPI specs.

**Acceptance Criteria:**
- [ ] MCP server discovery
- [ ] OpenAPI integration
- [ ] JSON Schema validation
- [ ] Access control

### Task 4.8: Implement Obsidian Memory Integration
**Description:** Implement Obsidian memory integration via MCP server.

**Acceptance Criteria:**
- [ ] MCP server for Obsidian
- [ ] search_vault/append_note tools
- [ ] Persistent memory
- [ ] LangGraph checkpoint persistence

### Task 4.9: Implement Dev Loop Integration
**Description:** Implement Dev Loop integration (N1/N2/N3).

**Acceptance Criteria:**
- [ ] N1: ReAct for trivial tasks
- [ ] N2: Mini Loop for features
- [ ] N3: Human Loop for architecture
- [ ] Automatic escalation

### Task 4.10: Implement GBNF Grammar Enforcement
**Description:** Implement GBNF grammar enforcement for 1-bit model outputs.

**Acceptance Criteria:**
- [ ] JSON grammar
- [ ] Code grammar
- [ ] Validation before output

### Task 4.11: Implement Auto-Correction Loop
**Description:** Implement auto-correction loop for 1-bit model errors.

**Acceptance Criteria:**
- [ ] Parallel validation slots
- [ ] Code repair mechanism
- [ ] Deterministic monitoring
- [ ] Cloud MoE fallback

### Task 4.12: Implement 6-Phase Pipeline
**Description:** Implement the 6-phase pipeline execution.

**Acceptance Criteria:**
- [ ] Phase 1: Discovery
- [ ] Phase 2: Contract
- [ ] Phase 3: Plan
- [ ] Phase 4: Execution
- [ ] Phase 5: Macro Review
- [ ] Phase 6: Delivery

### Task 4.13: Integrate with oh-my-opencode-slim
**Description:** Integrate with oh-my-opencode-slim repository.

**Acceptance Criteria:**
- [ ] Backward compatibility maintained
- [ ] Gran-Mestre pipeline applied
- [ ] Integration tests passing

### Task 4.14: Integrate with Referenced Repositories
**Description:** Integrate with all referenced GitHub repositories.

**Acceptance Criteria:**
- [ ] pi integration
- [ ] RuView integration
- [ ] openship integration
- [ ] code-review-graph integration
- [ ] I Have ADHD integration
- [ ] Orca integration
- [ ] OmniRoute integration
- [ ] Skills integration
- [ ] WorldMonitor integration
- [ ] AI Agent Book integration
- [ ] onp-spec-driven integration

---

## Phase 5: Macro Review

### Task 5.1: Review Total Diff
**Description:** Review the total diff for coherence and cross-task coupling.

**Acceptance Criteria:**
- [ ] Total diff reviewed
- [ ] Cross-task coherence verified
- [ ] Architecture aligned with contract
- [ ] Cloud MoE audit complete

---

## Phase 6: Delivery

### Task 6.1: Final Verification
**Description:** Final verification against original requirements.

**Acceptance Criteria:**
- [ ] Iron evidence verified
- [ ] Final validation passed
- [ ] Compliance verdict emitted

### Task 6.2: Cerebral Memory Archive
**Description:** Archive to cerebral memory (Obsidian).

**Acceptance Criteria:**
- [ ] Pipeline context archived
- [ ] Learnings documented
- [ ] Key decisions archived
- [ ] Patterns discovered archived

---

## Verification

### Phase 1 Verification
- [ ] All three reference documents analyzed
- [ ] Requirements extracted and categorized
- [ ] Target architecture defined
- [ ] Model allocation strategy documented
- [ ] Safety protocol flow defined

### Phase 2 Verification
- [ ] SPEC.md created with all architectural details
- [ ] Model configurations specified
- [ ] Safety protocol fully specified
- [ ] Integration points documented

### Phase 3 Verification
- [ ] PLAN.md with all atomic tasks
- [ ] TDD tests defined for each task
- [ ] SHA checkpoint saved
- [ ] Dependency graph created

### Phase 4 Verification
- [ ] All modules implemented
- [ ] All tests passing
- [ ] Atomic commits per task
- [ ] Safety protocol active

### Phase 5 Verification
- [ ] Total diff reviewed
- [ ] Cross-task coherence verified
- [ ] Architecture aligned with contract

### Phase 6 Verification
- [ ] Iron evidence verified
- [ ] Final validation passed
- [ ] Cerebral memory archived
- [ ] Final report presented

---

## Rollback Plan

If any phase fails:
1. Read saved SHA from CONTEXT.md
2. Execute `git reset --hard {sha}`
3. Report failure to user
4. Wait for user decision (retry, revise, cancel)

---

## Notes

- This plan follows the MIX mode (6-phase cascade with global registry)
- Dev Loop N3 (Human Loop) is used for architectural decisions
- Safety protocol is active throughout
- Observability metrics logged after each phase
- Fable Method gates (Fit, Twin Check, Artifact) applied where relevant