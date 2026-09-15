"""
Mecânica de Ignição (Execution & Validation) — langgraph-patterns.
Grafo stateful: schema + nós/arestas + checkpoint plan + interrupts.
Helenizado de langchain-ai/langgraph — só padrão; framework nunca como dependência.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class GraphInput(BaseModel):
    """Input schema: states + nodes."""
    states: List[str]
    nodes: List[str]
    interrupts: List[str] = []


class GraphOutput(BaseModel):
    """Schema for the output."""
    state_schema: List[str]
    graph_spec: Dict[str, Any]
    checkpoint_plan: List[str]
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_graph_input(input_data: Dict[str, Any]) -> GraphInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = GraphInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.states:
        raise ValueError("Invalid input: 'states' must have ≥1 field")
    if not input_obj.nodes:
        raise ValueError("Invalid input: 'nodes' must have ≥1 node")
    return input_obj


def montar_grafo(states: List[str], nodes: List[str],
                 interrupts: List[str] | None = None) -> Dict[str, Any]:
    """Monta spec do grafo: arestas em cadeia + checkpoint por nó + interrupts."""
    v = validate_graph_input({"states": states, "nodes": nodes,
                              "interrupts": interrupts or []})
    edges = [[v.nodes[i], v.nodes[i + 1]] for i in range(len(v.nodes) - 1)]
    out = GraphOutput(
        state_schema=v.states,
        graph_spec={"nodes": v.nodes, "edges": edges, "interrupts": v.interrupts,
                    "memory": {"short": "working", "long": "persistent"}},
        checkpoint_plan=[f"ckpt:{n}" for n in v.nodes],
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "resume": "exato por step"},
    )
    return out.model_dump(mode="json")


def ignicao(states: List[str], nodes: List[str]) -> Dict[str, Any]:
    """Função principal: valida → monta → dict."""
    return montar_grafo(states, nodes)


if __name__ == "__main__":
    import json

    r1 = ignicao(["sentiment", "confidence"], ["fetch", "analyze", "route"])
    assert r1["status"] == "success", r1
    assert r1["graph_spec"]["edges"] == [["fetch", "analyze"], ["analyze", "route"]], r1
    assert r1["checkpoint_plan"] == ["ckpt:fetch", "ckpt:analyze", "ckpt:route"], r1
    try:
        ignicao([], [])
        raise SystemExit("FAIL: vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 2}, ensure_ascii=False))
