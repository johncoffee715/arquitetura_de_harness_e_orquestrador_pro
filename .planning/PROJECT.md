# Project: Global Harness Refactoring

## What This Is

A global refactoring of the OpenCode harness to implement a hybrid AI orchestration system that manages models locally (MI50 16GB HBM2) and in the cloud, following the Gran-Mestre 6-phase pipeline architecture with Dev Loop methodology (N3 - Human Loop for architectural decisions).

## Core Value

Create a unified, modular AI orchestration harness that:
1. Routes tasks by complexity (TRIVIAL → SIMPLE → MEDIUM → COMPLEX/CRITICAL → FEATURE → MIX)
2. Manages VRAM allocation across multiple local models (Ornith-1.0 9B, Nanbeige 3B, LFM 2.5-1.6B, Bonsai 27B 1-bit)
3. Executes a 6-phase pipeline (Discovery → Contract → Plan → Execution → Macro Review → Delivery)
4. Implements safety protocols (SHA checkpointing, rollback, validation gates)
5. Integrates observability (metrics logging, OpenTelemetry, MELT)
6. Supports human-in-the-loop governance at critical gates

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Hardware target | MI50 16GB HBM2, Xeon E5-2699v3, 32GB RAM | Local-first with cloud fallback |
| Gran-Mestre model | Ornith-1.0 9B Q4_K_M (~5.5GB VRAM) | Stable control backbone |
| Heavy execution model | Bonsai 27B 1-bit (~3.9GB VRAM) | Multiple parallel slots |
| Filter models | LFM 2.5-1.6B + Nanbeige 3B (~2.5GB VRAM) | Instant binary checks |
| Orchestration framework | LangGraph (event-driven, state management) | Local state, cloud compute |
| Memory system | Obsidian via MCP server | Persistent cognitive memory |
| Dev Loop level | N3 (Human Loop) | Architectural decisions require human approval |
| Workflow mode | MIX | 6-phase cascade with global registry |

## Context

### Hardware Specifications
- CPU: Xeon E5-2699v3
- Motherboard: jingsh x99-d8 (x99/c612)
- RAM: 32GB DDR4 2400MHz
- GPU: MI50 16GB HBM2 / spoof pro VII
- Storage: slave A.I. SSD 128GB SATA3 (Harness idempotent)

### Model Allocation (VRAM Budget: ~11.9GB used, ~4.1GB for KV Cache)
- Ornith-1.0 9B (Q4_K_M): ~5.5GB — Gran-Mestre (local)
- Bonsai 27B 1-bit: ~3.9GB — Heavy execution (local, multiple slots)
- Nanbeige 3B (4-bit): ~1.4GB — Filter/validation (local)
- LFM 2.5-1.6B (FP8): ~1.1GB — Instant checks (local)

### Pipeline Phases
1. **Discovery** — Light decomposition, context gathering
2. **Contract** — Transform direction into design doc/spec
3. **Plan** — TDD tasks, code complete, coverage validation
4. **Execution** — Supervised task execution, atomic commits
5. **Macro Review** — Holistic diff review, cross-task coherence
6. **Delivery** — Final verification, cerebral memory archive

### Safety Protocol
- SHA saved before Phase 4 execution
- Rollback on any phase failure
- Git diff --quiet check before cloud offloading
- Local validator (Hestia) intercepts cloud responses

## Requirements

### Validated
(none yet — building from scratch)

### Active
- [ ] HARNESS-01: Implement Gran-Mestre meta-orchestrator with 6-phase pipeline
- [ ] HARNESS-02: Configure model provider for local/cloud hot-swap
- [ ] HARNESS-03: Implement VRAM allocation manager for MI50
- [ ] HARNESS-04: Create safety protocol (SHA checkpointing, rollback)
- [ ] HARNESS-05: Implement observability (metrics, OpenTelemetry, MELT)
- [ ] HARNESS-06: Integrate Obsidian as persistent memory via MCP
- [ ] HARNESS-07: Implement Dev Loop N3 (Human Loop) for architectural decisions
- [ ] HARNESS-08: Configure LangGraph event-driven workflow engine
- [ ] HARNESS-09: Implement policy engine (Policy-as-Code, RBAC/ABAC)
- [ ] HARNESS-10: Create tool registry (MCP servers, OpenAPI specs)
- [ ] HARNESS-11: Implement human-in-the-loop gates (HITL/HOTL)
- [ ] HARNESS-12: Integrate with existing oh-my-opencode-slim and referenced repos

### Out of Scope
- Full cloud deployment — local-first with cloud fallback only
- Training new models — using existing quantized models
- Real-time inference serving — orchestration layer only

## Evolution

This document evolves at phase transitions and milestone boundaries.

---
*Last updated: 2026-07-30 after initialization*