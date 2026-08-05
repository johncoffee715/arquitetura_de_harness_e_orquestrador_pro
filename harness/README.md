# Gran-Mestre Hybrid Harness

A hybrid AI orchestration system that manages models locally (MI50 16GB HBM2) and in the cloud, following the Gran-Mestre 6-phase pipeline architecture with Dev Loop methodology.

## Architecture

```
┌─────────────────────────────────────────────────┐
│              USER REQUEST                        │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│        GRAN-MESTRE (Ornith-1.0 9B)              │
│  ContextAnalyzer — Classifies Complexity        │
│  TRIVIAL | SIMPLE | MEDIUM | COMPLEX | MIX      │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│         MODEL PROVIDER (Hot-Swap)              │
├─────────────────────────────────────────────────┤
│  Local: Ornith-1.0 9B  │  Bonsai 27B 1-bit      │
│  Local: Nanbeige 3B    │  LFM 2.5-1.6B           │
│  Cloud: MoE (fallback)                         │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│          6-PHASE PIPELINE (LangGraph)            │
├─────────────────────────────────────────────────┤
│  Phase 1: Discovery  │  Phase 2: Contract       │
│  Phase 3: Plan       │  Phase 4: Execution       │
│  Phase 5: Review     │  Phase 6: Delivery       │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│      OBSIDIAN MEMORY (via MCP Server)           │
│  Persistent cognitive memory across sessions    │
└─────────────────────────────────────────────────┘
```

## Hardware Requirements

- **CPU:** Xeon E5-2699v3
- **Motherboard:** jingsh x99-d8 (x99/c612)
- **RAM:** 32GB DDR4 2400MHz
- **GPU:** MI50 16GB HBM2
- **Storage:** SSD 128GB SATA3 (Harness idempotent)

## Model Allocation (VRAM Budget)

| Model | Size | VRAM | Role |
|-------|------|------|------|
| Ornith-1.0 9B | Q4_K_M | ~5.5GB | Gran-Mestre (control) |
| Bonsai 27B 1-bit | 1-bit | ~3.9GB | Heavy execution (4 slots) |
| Nanbeige 3B | 4-bit | ~1.4GB | Filter/validation |
| LFM 2.5-1.6B | FP8 | ~1.1GB | Instant checks |
| MoE (Cloud) | Varies | 0GB | Architectural audit |

**Total:** ~11.9GB models + ~4.1GB KV Cache = 16GB

## Pipeline Phases

### Phase 1: Discovery
- Light decomposition of user request
- Context gathering from codebase, docs, research
- Scope filtering
- **Gate 1:** Direction approval

### Phase 2: Contract
- Transform direction into design doc/SPEC.md
- Validate spec against original request
- Audit against quality criteria
- **Gate 2:** Spec approval

### Phase 3: Plan
- TDD tasks with test-first approach
- Bite-sized atomic tasks
- Validate test coverage and verifiability
- **Safety:** SHA checkpoint saved here
- **Gate 3:** Plan approval

### Phase 4: Execution
- Supervised task execution
- Atomic git commits per task
- Fresh subagent per task
- TDD loop per task
- Micro-review per task
- **No gates** — commits atomic, progress visible

### Phase 5: Macro Review
- Review total diff for coherence
- Check cross-task coupling
- Audit against quality criteria
- Cloud MoE audit for architectural abstraction

### Phase 6: Delivery
- Fresh iron evidence verification
- Final validation against original request
- Audit iron evidence, emit final compliance verdict
- Archive to cerebral memory (Obsidian)
- **Gate 4:** Final report → cerebral memory

## Dev Loop Integration

The harness integrates with the Dev Loop methodology:

- **N1 (ReAct):** Trivial tasks (1-3 files, 3 iterations max)
- **N2 (Mini Loop):** Features (spec → TDD → commit → merge)
- **N3 (Human Loop):** Architectural decisions (Decide → Metrics → Triage → Plan → PR → Decide)

## Safety Protocol

1. **SHA Checkpoint:** Saved at Phase 3 (before Phase 4 execution)
2. **Git Diff Check:** `git diff --quiet` before Phase 4
3. **Rollback:** Automatic rollback on any phase failure
4. **Hestia Validator:** Local validator intercepts cloud responses

## Usage

```bash
# Start the full pipeline
python harness/core/harness.py start --task "Refactor harness globally" --mode MIX

# Run a specific phase
python harness/core/harness.py phase --phase discovery --task "Your task"

# Check model status
python harness/core/harness.py status

# Check VRAM usage
python harness/core/harness.py models

# Build integration registry (v2 — 6 categorias)
python harness/core/integration.py registry

# Seleção automática de recursos por task (orquestrador)
python harness/core/integration.py select --task "engenharia reversa com ghidra" --phase execute --top 3

# Run full integration
python harness/core/integration.py integrate --all
```

## Comando Global (qualquer diretório/instância)

> **Helenizado 2026-08-02**: o Gran-Mestre é global. Instalei o wrapper
> `gran-mestre` em `~/.local/bin` (no PATH) — funciona de qualquer cwd,
> pois delega para os scripts com caminhos absolutos `/mnt/dados/...`.

```bash
gran-mestre start --task "..." --mode MIX    # pipeline completo
gran-mestre phase --phase discovery          # fase isolada
gran-mestre status | models                  # estado/VRAM dos modelos
gran-mestre registry                         # reconstrói registro
gran-mestre select --task "..." [--print]    # recursos por oferta-demanda
gran-mestre route --task "..."               # recurso → submodelo local
gran-mestre decision --task "..." --outcome success|fail   # aprendizado adaptativo
gran-mestre history [--task]                 # histórico de decisões
gran-mestre models-up | validate             # sobe/valida 4 modelos
```

Agente global: `~/.config/opencode/agents/gran-mestre.md` (v7.0.0, mode: primary) —
sincronizar com `~/.opencode/agent/gran-mestre.md` após edições (autofagia).

## Registry v2 — Catalogação Automática (6 Categorias)

O orquestrador (Ornith) consulta o registro global para escolher recursos por task:

| Categoria | Fonte | Exemplo |
|-----------|-------|---------|
| `plugins` | `~/.config/opencode/plugins`, `opencode/plugins` | ecc-hooks, graphify |
| `mcp` | `opencode.json` → `mcp` | ghidra (engenharia reversa) |
| `lsp` | binários instalados + configs | rust-analyzer, clangd |
| `hooks` | `~/.config/opencode/hooks` | gsd-validate-commit |
| `skills` | `~/.config/opencode/skills` + locais | ecc-autofagia, dev-loop |
| `subagents` | `~/.config/opencode/agents` + locais | reverser, gran-mestre |

**Seleção por task**: `IntegrationManager.select_for_task(task, phase, top_k)` — matching por
tags + descrição + nome, com stopwords pt/en e boost por fase do pipeline. O ModelProvider
expõe `select_resources()` para o orquestrador delegar com os recursos certos em cada fase/gate.

### Aprendizado Adaptativo — o orquestrador estuda por task

O orquestrador incorporado no Ornith **estuda conforme cada task** qual a melhor ferramenta:

1. **Seleção**: `select_for_task()` escolhe recursos por matching (tags + descrição + fase).
2. **Registro**: cada escolha vira uma entrada em `harness/decision-log.jsonl`
   (`record_decision(task, phase, selections, outcome, feedback)`).
3. **Feedback**: o orquestrador marca `success` ou `fail` após usar os recursos
   (`--outcome success|fail` na CLI).
4. **Score adaptativo**: scores são **derivados do log** (fonte de verdade idempotente —
   `build_registry()` re-descobre recursos e sobrescreve `registry.json`, então o score
   NÃO vive lá). `+1.0` por sucesso, `-1.0` por falha, aplicado com peso `0.5` na seleção.

```bash
# Selecionar recursos para uma task (sem registrar — dry-run)
python3 harness/core/integration.py select --task "engenharia reversa com ghidra" --phase execute --print

# Selecionar + registrar decisão
python3 harness/core/integration.py select --task "engenharia reversa com ghidra" --phase execute

# Registrar feedback (aprendizado)
python3 harness/core/integration.py decision --task "..." --outcome success --feedback "ok"
python3 harness/core/integration.py decision --task "..." --outcome fail --feedback "ghidra travou"

# Estudar o passado (histórico por task)
python3 harness/core/integration.py history --task "ghidra"
```

### Specs dos Modelos (confirmadas 2026-08-02)

| Modelo | Papel | Contexto máx | Capacidades |
|--------|-------|--------------|-------------|
| Ornith-1.0 9B | Gran-Mestre (meta-orquestrador) | **256K** | agentic coding, gera código + harness/scaffold juntos (RL), tool-calling via MCP, loops de correção de bugs |
| Bonsai 27B 1-bit | Execução pesada (4 slots) | **262K** | 89,5% retenção vs FP16, tool calling, multimodal opcional (mmproj), 4-8GB VRAM |
| Nanbeige 3B | Filtro/validação (micro reviews) | 32K | CoT passo a passo, programação, agente com múltiplas tool calls + deep search |
| LFM 2.5-1.6B | Checks instantâneos | — | multimodal VL (imagens/OCR/documentos), multilíngue, 731MB, edge |

- `start-llama.sh` aplica `--cache-type-k q8_0 --cache-type-v q8_0` para `ornith*` e `nanbeige*`
  (KV cache compactado → janelas longas dentro da VRAM de 16GB).

## Ornith — Orquestrador Gran-Mestre (Self-Scaffolding)

- **Self-scaffolding**: gera seu próprio scaffold + solução (otimiza os dois juntos) — não usa RL com scaffold fixo
- **Raciocínio nativo**: abre com bloco `<think>` → `--reasoning-preserve` no llama-server
- **Tool-calling nativo**: formato OpenAI-style (`/v1/chat/completions` com `tools`) — delegação real para submodelos/recursos
- Lançamento: `start-llama.sh` detecta `ornith*` e adiciona `--reasoning-preserve --jinja` automaticamente

## Directory Structure

```
harness/
├── __init__.py
├── harness-config.json       # Main configuration
├── README.md                 # This file
├── CONTEXT.md                # Runtime context and metrics
├── core/
│   ├── __init__.py
│   ├── harness.py            # Main entry point
│   └── integration.py        # Integration manager
├── safety/
│   ├── __init__.py
│   └── safety-protocol.py    # SHA checkpointing, rollback
├── observability/
│   ├── __init__.py
│   └── observability-layer.py # Metrics, OpenTelemetry
├── dev-loop/
│   ├── __init__.py
│   └── dev-loop.py           # N1/N2/N3 Dev Loop
├── models/
│   ├── __init__.py
│   └── model-provider.py     # Hot-swap model management
├── metrics/                  # Metrics storage
│   └── pipeline-metrics.jsonl
└── integrations/             # GitHub repo integration stubs
    ├── oh-my-opencode-slim.md
    ├── pi.md
    ├── RuView.md
    └── ...
```

## License

MIT