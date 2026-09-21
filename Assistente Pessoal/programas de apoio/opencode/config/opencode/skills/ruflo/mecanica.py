"""
Mecânica de Ignição (Execution & Validation) — ruflo.
Topologia de swarm + plano de memória (determinístico offline p/ validação).
Helenizado de ruvnet/ruflo — só padrões; sem runtime alheio.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class RufloInput(BaseModel):
    """Input schema: task + agent count."""
    task: str
    agents: int


class RufloOutput(BaseModel):
    """Schema for the output."""
    topology_pick: str  # "hierarchical" | "mesh" | "adaptive"
    memory_plan: Dict[str, Any]
    picked_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_ruflo_input(input_data: Dict[str, Any]) -> RufloInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = RufloInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.task or not input_obj.task.strip():
        raise ValueError("Invalid input: 'task' must be non-empty")
    if input_obj.agents < 1:
        raise ValueError("Invalid input: 'agents' must be >= 1")
    return input_obj


def escolher_topologia(task: str, agents: int) -> Dict[str, Any]:
    """Regra determinística: 1 agente = hierárquica solo; 2-4 = hierárquica;
    5+ = mesh com consenso; ambígua/comando único = adaptativa."""
    validated = validate_ruflo_input({"task": task, "agents": agents})
    n = validated.agents
    low = validated.task.lower()
    if n == 1:
        topo, why = "hierarchical", "1 agente: comando direto, sem overhead de mesh"
    elif any(k in low for k in ("approve", "gate", "comando", "review")):
        topo, why = "hierarchical", "comando/aprovação única exige hierarquia"
    elif n >= 5:
        topo, why = "mesh", "5+ agentes pares: mesh + consenso"
    elif n >= 2:
        topo, why = "hierarchical", "2-4 agentes: líder + workers com consenso"
    else:
        topo, why = "adaptive", "fallback adaptativo"
    out = RufloOutput(
        topology_pick=topo,
        memory_plan={"namespaces": [f"agent-{i+1}" for i in range(n)],
                     "index": "HNSW", "pii_strip": True},
        picked_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "rationale": why},
    )
    return out.model_dump(mode="json")


def ignicao(task: str, agents: int) -> Dict[str, Any]:
    """Função principal: valida → topologia → dict."""
    return escolher_topologia(task, agents)


if __name__ == "__main__":
    import json

    r1 = ignicao("build feature", 1)
    assert r1["topology_pick"] == "hierarchical", r1
    r2 = ignicao("swarm research", 6)
    assert r2["topology_pick"] == "mesh" and len(r2["memory_plan"]["namespaces"]) == 6, r2
    r3 = ignicao("approve release", 3)
    assert r3["topology_pick"] == "hierarchical", r3
    try:
        ignicao("", 0)
        raise SystemExit("FAIL: input inválido deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 4}, ensure_ascii=False))
