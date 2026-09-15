"""
Mecânica de Ignição (Execution & Validation) — temporal.
Tríade durável: workflow + activities com retry + resume points.
Helenizado de temporalio/temporal — só padrão; servidor nunca.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class TriadInput(BaseModel):
    """Input schema: workflow + activities."""
    workflow: str
    activities: List[str]


class TriadOutput(BaseModel):
    """Schema for the output."""
    workflow_spec: Dict[str, Any]
    activity_plan: List[Dict[str, Any]]
    resume_points: List[str]
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_triad_input(input_data: Dict[str, Any]) -> TriadInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = TriadInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.workflow or not input_obj.workflow.strip():
        raise ValueError("Invalid input: 'workflow' must be non-empty")
    if not input_obj.activities:
        raise ValueError("Invalid input: 'activities' must have ≥1 activity")
    return input_obj


def montar_triade(workflow: str, activities: List[str]) -> Dict[str, Any]:
    """Monta tríade: workflow + activities (retry) + resume points."""
    v = validate_triad_input({"workflow": workflow, "activities": activities})
    plan = [{"name": a, "retry": True, "resume": f"ckpt:{a}"} for a in v.activities]
    out = TriadOutput(
        workflow_spec={"name": v.workflow, "durable": True},
        activity_plan=plan,
        resume_points=[f"ckpt:{a}" for a in v.activities],
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "namespace": "isolated"},
    )
    return out.model_dump(mode="json")


def ignicao(workflow: str, activities: List[str]) -> Dict[str, Any]:
    """Função principal: valida → monta → dict."""
    return montar_triade(workflow, activities)


if __name__ == "__main__":
    import json

    r1 = ignicao("order-pipeline", ["charge", "ship"])
    assert r1["status"] == "success" and len(r1["resume_points"]) == 2, r1
    assert all(a["retry"] for a in r1["activity_plan"]), r1
    try:
        ignicao("", [])
        raise SystemExit("FAIL: vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 2}, ensure_ascii=False))
