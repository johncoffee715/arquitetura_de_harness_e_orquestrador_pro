# Roadmap: Global Harness Refactoring

## Project: Global Harness Refactoring

---

## Phase Overview

| Phase | Name | Goal | Complexity | Gate |
|-------|------|------|------------|------|
| 1 | Discovery | Analyze existing harness, extract requirements, define architecture | MIX | Gate 1: Direction approval |
| 2 | Contract | Create SPEC.md with design doc, validate against requirements | MIX | Gate 2: Spec approval |
| 3 | Plan | Create PLAN.md with TDD tasks, atomic commits, safety checkpoint | MIX | Gate 3: Plan approval |
| 4 | Execution | Implement harness modules with atomic commits | MIX | No gates — atomic commits |
| 5 | Macro Review | Holistic review, cross-task coherence, cloud audit | MIX | No gate — report |
| 6 | Delivery | Final verification, safety validation, cerebral archive | MIX | Gate 4: Final report |

---

## Phase 1: Discovery & Context Analysis

**Goal:** Analyze the existing harness structure, extract all requirements from the three reference documents, and define the target architecture.

**Tasks:**
1. Map existing OpenCode harness structure (skills, agents, commands)
2. Analyze oh-my-opencode-slim repository structure
3. Extract requirements from "engenharia de harness.md"
4. Extract requirements from "Orquestrador de IA de Forma Profissional.md"
5. Extract requirements from "executar autofagia e helenizaçao.md"
6. Define target architecture (Gran-Mestre + 6-phase pipeline)
7. Define model allocation strategy (VRAM budget)
8. Define safety protocol flow
9. Present direction for Gate 1 approval

**Acceptance Criteria:**
- [ ] All three reference documents analyzed
- [ ] Requirements extracted and categorized
- [ ] Target architecture defined
- [ ] Model allocation strategy documented
- [ ] Safety protocol flow defined
- [ ] Direction presented for approval

**Dependencies:** None

---

## Phase 2: Contract & Architecture Spec

**Goal:** Create SPEC.md with detailed architecture specification, model configurations, and integration points.

**Tasks:**
1. Create SPEC.md with architecture overview
2. Define Gran-Mestre orchestrator design
3. Define Model Provider layer (hot-swap)
4. Define VRAM allocation manager
5. Define 6-phase pipeline implementation
6. Define safety protocol (SHA checkpointing, rollback)
7. Define observability layer (OpenTelemetry, MELT)
8. Define policy engine (Policy-as-Code, RBAC/ABAC)
9. Define tool registry (MCP, OpenAPI)
10. Define Obsidian memory integration
11. Define Dev Loop integration (N1/N2/N3)
12. Define GBNF grammar enforcement
13. Define auto-correction loop
14. Validate SPEC against original requirements
15. Present SPEC for Gate 2 approval

**Acceptance Criteria:**
- [ ] SPEC.md created with all architectural details
- [ ] Model configurations specified
- [ ] Safety protocol fully specified
- [ ] Observability layer designed
- [ ] Integration points documented
- [ ] SPEC validated against requirements
- [ ] SPEC approved at Gate 2

**Dependencies:** Phase 1 complete

---

## Phase 3: Plan (TDD)

**Goal:** Create detailed PLAN.md with atomic TDD tasks, dependency analysis, and safety checkpoint.

**Tasks:**
1. Break down SPEC into atomic tasks
2. Create TDD test-first plans for each task
3. Define dependency graph between tasks
4. Define VRAM allocation tests
5. Define safety protocol tests
6. Define observability tests
7. Define integration tests
8. Save SHA checkpoint (Safety Protocol)
9. Validate test coverage and verifiability
10. Present PLAN for Gate 3 approval

**Acceptance Criteria:**
- [ ] PLAN.md with all atomic tasks
- [ ] TDD tests defined for each task
- [ ] Dependency graph created
- [ ] SHA checkpoint saved
- [ ] Test coverage validated
- [ ] PLAN approved at Gate 3

**Dependencies:** Phase 2 complete

---

## Phase 4: Execution (Implementation)

**Goal:** Implement all harness modules with atomic commits, TDD, and continuous verification.

**Tasks:**
1. Implement Gran-Mestre meta-orchestrator
2. Implement Model Provider layer
3. Implement VRAM allocation manager
4. Implement Phase 1: Discovery
5. Implement Phase 2: Contract
6. Implement Phase 3: Plan
7. Implement Phase 4: Execution
8. Implement Phase 5: Macro Review
9. Implement Phase 6: Delivery
10. Implement Safety Protocol
11. Implement Observability layer
12. Implement Policy Engine
13. Implement Tool Registry
14. Implement Obsidian Memory Integration
15. Implement Dev Loop integration
16. Implement GBNF grammar enforcement
17. Implement auto-correction loop
18. Integrate with oh-my-opencode-slim
19. Integrate with referenced repositories
20. Run tests after each task
21. Atomic commits per task

**Acceptance Criteria:**
- [ ] All modules implemented
- [ ] All tests passing
- [ ] Atomic commits per task
- [ ] Safety protocol active
- [ ] Observability metrics logged
- [ ] No partial state

**Dependencies:** Phase 3 complete (SHA checkpoint saved)

---

## Phase 5: Macro Review

**Goal:** Holistic review of total diff, cross-task coherence, and cloud audit.

**Tasks:**
1. Review total diff for coherence
2. Check cross-task coupling
3. Audit against quality criteria
4. Validate architecture alignment with contract
5. Cloud MoE audit for architectural abstraction
6. Generate review report

**Acceptance Criteria:**
- [ ] Total diff reviewed
- [ ] Cross-task coherence verified
- [ ] Quality criteria met
- [ ] Architecture aligned with contract
- [ ] Review report generated

**Dependencies:** Phase 4 complete

---

## Phase 6: Delivery

**Goal:** Final verification, safety validation, and cerebral memory archive.

**Tasks:**
1. Fresh iron evidence verification
2. Final validation against original request
3. Audit iron evidence, emit final compliance verdict
4. Archive to cerebral memory (Obsidian)
5. Present final report at Gate 4

**Acceptance Criteria:**
- [ ] Iron evidence verified
- [ ] Final validation passed
- [ ] Compliance verdict emitted
- [ ] Cerebral memory archived
- [ ] Final report presented

**Dependencies:** Phase 5 complete

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| VRAM overflow on MI50 | Medium | High | Strict allocation limits, CPU offload prevention |
| Cloud MoE latency | Medium | Medium | Local-first, cloud only for Phase 5/6 |
| 1-bit model logic drift | High | Medium | GBNF grammars, auto-correction loop |
| Safety protocol failure | Low | Critical | SHA checkpoint, automatic rollback |
| Integration conflicts | Medium | High | Isolated testing per integration |
| Spec drift | Medium | Medium | Hestia validation after each phase |

## Timeline Estimate

| Phase | Estimated Duration |
|-------|-------------------|
| Phase 1: Discovery | 2-3 hours |
| Phase 2: Contract | 3-4 hours |
| Phase 3: Plan | 2-3 hours |
| Phase 4: Execution | 8-12 hours |
| Phase 5: Macro Review | 2-3 hours |
| Phase 6: Delivery | 1-2 hours |
| **Total** | **18-27 hours** |

## Gate Schedule

| Gate | Phase | Description |
|------|-------|-------------|
| Gate 1 | Phase 1 → 2 | Direction approval |
| Gate 2 | Phase 2 → 3 | Spec approval |
| Gate 3 | Phase 3 → 4 | Plan approval |
| Gate 4 | Phase 6 | Final report |