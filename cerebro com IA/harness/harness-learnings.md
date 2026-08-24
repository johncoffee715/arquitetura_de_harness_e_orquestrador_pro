# Harness Learnings

## Pipeline: Global Harness Refactoring (2026-07-30)

### Key Learnings

1. **MIX Mode + Dev Loop = Effective for Architectural Refactoring**
   - MIX mode (COMPLEX + CRITICAL + FEATURE) enables full 6-phase cascade with all registry resources
   - Dev Loop N3 (Human Loop) is the right level for architectural decisions
   - Automatic escalation from N1 (ReAct) → N2 (Mini Loop) → N3 (Human Loop) works well

2. **Hybrid Model Architecture is Viable on Local Hardware**
   - MI50 16GB HBM2 can run Ornith-1.0 (5.5GB) + Bonsai 27B (3.9GB) + LFM/Nanbeige (2.5GB) + KV Cache (4.1GB)
   - 1-bit quantization for Bonsai enables 4 parallel slots without VRAM overflow
   - Cloud MoE as fallback for Phase 5/6 architectural audit is effective

3. **Safety Protocol is Critical**
   - SHA checkpoint before Phase 4 prevents data loss
   - Automatic rollback on failure preserves repo integrity
   - `git diff --quiet` check before cloud offloading prevents partial state

4. **Gran-Mestre Orchestrator Design**
   - ContextAnalyzer complexity routing (TRIVIAL → MIX) works well
   - Dynamic registry-based delegation avoids hardcoded resource binding
   - Model Provider hot-swap enables seamless local/cloud transitions

5. **Integration Ecosystem**
   - 87 skills, 88 agents, 103 commands discoverable via integration manager
   - 12 GitHub repos integrated (oh-my-opencode-slim, pi, RuView, etc.)
   - Obsidian MCP integration provides persistent cognitive memory

6. **GBNF Grammar Enforcement**
   - Prevents syntax errors from 1-bit quantization
   - JSON grammar + code grammar covers most output types
   - Complements auto-correction loop for reliability

7. **Auto-Correction Loop Design**
   - Bonsai 1-bit generates in one slot, Ornith validates in parallel
   - Deterministic monitoring catches logic errors before propagation
   - Cloud MoE fallback after 3 consecutive Bonsai failures is effective safety net