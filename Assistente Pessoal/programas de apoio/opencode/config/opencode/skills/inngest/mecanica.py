"""
Mecânica de Ignição (Execution & Validation) — inngest.
Função durável: trigger + steps com retry/estado + flow-control.
Helenizado de inngest/inngest — só padrão; servidor/plataforma nunca.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class DurableInput(BaseModel):
    """Input schema: trigger + steps."""
    trigger: str
    steps: List[str]


class DurableOutput(BaseModel):
    """Schema for the output."""
    trigger_spec: Dict[str, str]
    step_plan: List[Dict[str, Any]]
    flow_control: Dict[str, Any]
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_durable_input(input_data: Dict[str, Any]) -> DurableInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = DurableInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.trigger or not input_obj.trigger.strip():
        raise ValueError("Invalid input: 'trigger' must be non-empty")
    if not input_obj.steps:
        raise ValueError("Invalid input: 'steps' must have ≥1 step")
    return input_obj


def montar_funcao(trigger: str, steps: List[str]) -> Dict[str, Any]:
    """Monta função: trigger + steps (run+retry+estado) + flow-control default."""
    v = validate_durable_input({"trigger": trigger, "steps": steps})
    plan = [{"name": s, "retry": True, "persist_state": True} for s in v.steps]
    out = DurableOutput(
        trigger_spec={"on": v.trigger},
        step_plan=plan,
        flow_control={"concurrency": 1, "throttle": None, "debounce": None},
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "resume_points": len(plan)},
    )
    return out.model_dump(mode="json")


def ignicao(trigger: str, steps: List[str]) -> Dict[str, Any]:
    """Função principal: valida → monta → dict."""
    return montar_funcao(trigger, steps)


if __name__ == "__main__":
    import json

    r1 = ignicao("shop/product.imported", ["copy-images-to-s3", "resize-images"])
    assert r1["status"] == "success" and len(r1["step_plan"]) == 2, r1
    assert all(s["retry"] and s["persist_state"] for s in r1["step_plan"]), r1
    try:
        ignicao("", [])
        raise SystemExit("FAIL: vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 2}, ensure_ascii=False))
