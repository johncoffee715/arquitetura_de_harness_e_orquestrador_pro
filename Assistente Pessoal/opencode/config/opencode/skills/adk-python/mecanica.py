"""
Mecânica de Ignição (Execution & Validation) — adk-python.
Spec Agent/Workflow: simples → Agent; orquestração → Workflow + Task API.
Helenizado de google/adk-python — só padrão; framework nunca como dependência.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class AdkInput(BaseModel):
    """Input schema: agent spec + orchestration flag."""
    name: str
    instruction: str
    orchestrate: bool = False


class AdkOutput(BaseModel):
    """Schema for the output."""
    agent_spec: Dict[str, str]
    workflow_spec: Dict[str, Any]
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_adk_input(input_data: Dict[str, Any]) -> AdkInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = AdkInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.name or not input_obj.name.strip():
        raise ValueError("Invalid input: 'name' must be non-empty")
    if not input_obj.instruction or not input_obj.instruction.strip():
        raise ValueError("Invalid input: 'instruction' must be non-empty")
    return input_obj


def especificar(name: str, instruction: str, orchestrate: bool = False) -> Dict[str, Any]:
    """Monta spec: sempre Agent; Workflow só se orquestração."""
    v = validate_adk_input({"name": name, "instruction": instruction, "orchestrate": orchestrate})
    wf: Dict[str, Any] = {"edges": [], "task_api": "multi-turn", "confirm": True}
    if v.orchestrate:
        wf = {"edges": [["START", v.name, v.name + "-helper"]], "task_api": "multi-turn",
              "confirm": True, "evalset": True}
    out = AdkOutput(
        agent_spec={"name": v.name, "instruction": v.instruction},
        workflow_spec=wf,
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "orchestrated": v.orchestrate},
    )
    return out.model_dump(mode="json")


def ignicao(name: str, instruction: str, orchestrate: bool = False) -> Dict[str, Any]:
    """Função principal: valida → especifica → dict."""
    return especificar(name, instruction, orchestrate)


if __name__ == "__main__":
    import json

    r1 = ignicao("greeting_agent", "Greet warmly.")
    assert r1["status"] == "success" and r1["workflow_spec"]["edges"] == [], r1
    r2 = ignicao("root_agent", "Coordinate.", orchestrate=True)
    assert r2["workflow_spec"]["evalset"] is True, r2
    try:
        ignicao("", "")
        raise SystemExit("FAIL: vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
