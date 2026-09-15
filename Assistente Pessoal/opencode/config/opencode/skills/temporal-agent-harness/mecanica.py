"""
Mecânica de Ignição (Execution & Validation) — temporal-agent-harness.
Agente durável: spec + approval policy (safe-by-default) + modos.
Helenizado de temporal-community/temporal-agent-harness — só padrões.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class HarnessInput(BaseModel):
    """Input schema: agent + tools."""
    agent: str
    tools: List[str]


class HarnessOutput(BaseModel):
    """Schema for the output."""
    agent_spec: Dict[str, Any]
    approval_policy: Dict[str, Any]
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_harness_input(input_data: Dict[str, Any]) -> HarnessInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = HarnessInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.agent or not input_obj.agent.strip():
        raise ValueError("Invalid input: 'agent' must be non-empty")
    if not input_obj.tools:
        raise ValueError("Invalid input: 'tools' must have ≥1 tool")
    return input_obj


def especificar_agente(agent: str, tools: List[str]) -> Dict[str, Any]:
    """Spec: agente-como-workflow + policy safe-by-default."""
    v = validate_harness_input({"agent": agent, "tools": tools})
    out = HarnessOutput(
        agent_spec={"name": v.agent, "durable": True, "resume": "mid-turn",
                    "event_stream": "live+replay"},
        approval_policy={"default": "safe-by-default", "allow_lists": [],
                         "overrides": "per-session", "code_mode": True,
                         "tools": v.tools},
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "pin": "versão sempre pinada (pre-1.0)"},
    )
    return out.model_dump(mode="json")


def ignicao(agent: str, tools: List[str]) -> Dict[str, Any]:
    """Função principal: valida → especifica → dict."""
    return especificar_agente(agent, tools)


if __name__ == "__main__":
    import json

    r1 = ignicao("travel", ["search_flights", "book_flight"])
    assert r1["status"] == "success", r1
    assert r1["approval_policy"]["default"] == "safe-by-default", r1
    assert r1["agent_spec"]["resume"] == "mid-turn", r1
    try:
        ignicao("", [])
        raise SystemExit("FAIL: vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 2}, ensure_ascii=False))
