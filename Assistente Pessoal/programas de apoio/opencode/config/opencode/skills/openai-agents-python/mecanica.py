"""
Mecânica de Ignição (Execution & Validation) — openai-agents-python.
Spec agente + mapa de handoffs com guardrails.
Helenizado de openai/openai-agents-python — só padrão; framework nunca como dependência.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class HandoffInput(BaseModel):
    """Input schema: agent + handoffs."""
    agent: str
    handoffs: List[str]


class HandoffOutput(BaseModel):
    """Schema for the output."""
    agent_spec: Dict[str, str]
    handoff_map: Dict[str, List[str]]
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_handoff_input(input_data: Dict[str, Any]) -> HandoffInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = HandoffInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.agent or not input_obj.agent.strip():
        raise ValueError("Invalid input: 'agent' must be non-empty")
    if not input_obj.handoffs:
        raise ValueError("Invalid input: 'handoffs' must have ≥1 target")
    return input_obj


def especificar_handoff(agent: str, handoffs: List[str]) -> Dict[str, Any]:
    """Monta spec: agente + mapa de handoffs c/ guardrails+sessions+trace."""
    v = validate_handoff_input({"agent": agent, "handoffs": handoffs})
    out = HandoffOutput(
        agent_spec={"name": v.agent, "guardrails": "in+out", "sessions": "auto"},
        handoff_map={v.agent: v.handoffs},
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "tracing": "built-in"},
    )
    return out.model_dump(mode="json")


def ignicao(agent: str, handoffs: List[str]) -> Dict[str, Any]:
    """Função principal: valida → especifica → dict."""
    return especificar_handoff(agent, handoffs)


if __name__ == "__main__":
    import json

    r1 = ignicao("triage", ["billing", "refund"])
    assert r1["status"] == "success" and r1["handoff_map"] == {"triage": ["billing", "refund"]}, r1
    try:
        ignicao("", [])
        raise SystemExit("FAIL: vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 2}, ensure_ascii=False))
