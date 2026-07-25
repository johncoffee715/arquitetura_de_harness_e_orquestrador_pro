# AgentRegistry — Central de Descoberta e Roteamento

**Local:** `~/.config/opencode/registry/`
**Versão:** 1.0.0
**Agentes registrados:** 43
**Capacidades mapeadas:** 24

---

## Arquitetura

```
                    ┌────────────────────────────────────────┐
                    │            AgentRegistry               │
                    │  agent-registry.json (43 agentes)     │
                    │  capability-index.json (24 caps)       │
                    └──────┬──────────────────────┬─────────┘
                           │                      │
              ┌────────────▼──────────┐  ┌───────▼──────────┐
              │   Capability Router   │  │     EventBus      │
              │   Roteia por CAP      │  │   11 tópicos      │
              └────────────┬──────────┘  └───────┬──────────┘
                           │                      │
              ┌────────────▼──────────────────────▼──────────┐
              │           ContextBroker (TraceID)             │
              │  command · agent · hook · mcp                │
              └──────────────────────────────────────────────┘
```

## Componentes

### 1. AgentRegistry (`agent-registry.json`)
Catálogo central de todos os 43 agentes GSD. Cada entrada contém:
- `name` — identificador único
- `description` — o que o agente faz
- `mode` — subagent (todos atualmente)
- `capabilities` — array de capacidades inferidas da descrição
- `spawn_sources` — quem invoca este agente
- `model` — modelo de IA preferido (quando especificado)
- `permissions` — permissões específicas (quando especificadas)

### 2. Capability Index (`capability-index.json`)
Índice invertido: **capacidade → lista de agentes**.
Exemplo:
```json
"planning": ["gsd-planner", "gsd-roadmapper", "superpowers-plan-writer", ...],
"code-analysis": ["gsd-code-reviewer", "gsd-code-fixer", ...]
```

### 3. Capability Router (`capability-router.json`)
109 regras de roteamento dinâmico. Estratégia: round-robin com fallback.
Permite rotear por capacidade em vez de nome fixo.

### 4. EventBus (`event-bus.json`)
11 tópicos para pub/sub entre componentes:
| Tópico | Produtor | Consumidores |
|--------|----------|--------------|
| `agent:registered` | agent-registry | * |
| `workflow:phase:started` | gsd-executor | context-broker, otel, dashboard |
| `workflow:phase:completed` | gsd-executor | context-broker, otel, dashboard, memory |
| `command:invoked` | command-router | context-broker, otel |
| `context:propagated` | context-broker | * |

### 5. ContextBroker (`context-broker.json`)
Contexto unificado com TraceID global (formato ULID, propagação W3C TraceContext).
Rastreia 4 componentes:
- **command** → trace_id, command_name, args, timestamp, duration_ms
- **agent** → trace_id, agent_name, capability, parent_trace_id, timestamp, status
- **hook** → trace_id, hook_id, phase, timestamp, exit_code
- **mcp** → trace_id, server_name, tool_name, timestamp, status

## Como Usar

### Descobrir agente por capacidade
```bash
# Consultar quais agentes fazem planning
cat ~/.config/opencode/registry/capability-index.json | jq '.planning'

# Consultar detalhes de um agente específico
cat ~/.config/opencode/registry/agent-registry.json | jq '.agents[] | select(.name=="gsd-planner")'
```

### Roteamento dinâmico
Em vez de invocar `gsd-executor` por nome, use o Capability Router:
```
ROUTING: capability=execution → gsd-executor | gsd-code-fixer | superpowers-implementer
```

### Rastreamento com TraceID
Todo comando/agente/hook/MCP recebe um `trace_id`:
```json
{
  "trace_id": "01J8X...",
  "component": "agent",
  "agent_name": "gsd-executor",
  "capability": "execution",
  "duration_ms": 4523,
  "status": "completed"
}
```

## Prioridades Futuras

### 🟠 IMPORTANTES
- [ ] Hook Registry (ordem de execução baseada em prioridade)
- [ ] OpenTelemetry Export (OTel Collector + OTLP)
- [ ] DAG Viewer (visualização do grafo de chamadas)
- [ ] Hook Priority (prioridade numérica entre hooks)

### 🔵 OPCIONAIS
- [ ] Dashboard Web (status dos agentes em tempo real)
- [ ] Pipeline Visualizer (DAG interativo)
- [ ] Metrics API (REST para métricas)

### 🟣 FUTURAS
- [ ] Multi-host Agents (agentes distribuídos)
- [ ] Distributed Scheduler (escalonamento cross-host)
- [ ] Auto-healing Agents (reinício automático)
- [ ] Reinforcement Routing (rota aprendida por feedback)
