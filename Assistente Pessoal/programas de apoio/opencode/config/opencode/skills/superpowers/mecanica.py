"""
Mecânica de Ignição (Execution & Validation) — superpowers.
Loop mandatório com review duplo (spec → quality).
Helenizado de obra/superpowers — só o loop; sem cópia literal.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class PowersInput(BaseModel):
    """Input schema: task + review flags."""
    task: str
    spec_ok: bool
    quality_ok: bool


class PowersOutput(BaseModel):
    """Schema for the output."""
    skill_check: bool
    review_1_spec: str
    review_2_quality: str
    finish: str
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_powers_input(input_data: Dict[str, Any]) -> PowersInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = PowersInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.task or not input_obj.task.strip():
        raise ValueError("Invalid input: 'task' must be non-empty")
    return input_obj


def aplicar_loop(task: str, spec_ok: bool, quality_ok: bool) -> Dict[str, Any]:
    """Review duplo: spec primeiro, quality depois; finish só com ambos."""
    v = validate_powers_input({"task": task, "spec_ok": spec_ok, "quality_ok": quality_ok})
    r1 = "pass" if v.spec_ok else "blocked"
    r2 = "pass" if (v.spec_ok and v.quality_ok) else "blocked"
    finish = "ship" if (r1 == "pass" and r2 == "pass") else "hold"
    out = PowersOutput(
        skill_check=True,
        review_1_spec=r1,
        review_2_quality=r2,
        finish=finish,
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "stages": ["check", "r1", "r2", "finish"]},
    )
    return out.model_dump(mode="json")


def ignicao(task: str, spec_ok: bool, quality_ok: bool) -> Dict[str, Any]:
    """Função principal: valida → loop → dict."""
    return aplicar_loop(task, spec_ok, quality_ok)


if __name__ == "__main__":
    import json

    r1 = ignicao("add login", True, True)
    assert r1["finish"] == "ship", r1
    r2 = ignicao("add login", True, False)
    assert r2["finish"] == "hold" and r2["review_2_quality"] == "blocked", r2
    r3 = ignicao("add login", False, True)
    assert r3["review_1_spec"] == "blocked" and r3["finish"] == "hold", r3
    try:
        ignicao("   ", False, False)
        raise SystemExit("FAIL: task vazia deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 4}, ensure_ascii=False))
