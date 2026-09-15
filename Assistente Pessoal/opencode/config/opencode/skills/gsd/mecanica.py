"""
Mecânica de Ignição (Execution & Validation) — gsd.
Plano faseado + âncora de big-picture (determinístico offline).
Helenizado da org gsd-build — só padrões flagship.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class GsdInput(BaseModel):
    """Input schema: goal + phases."""
    goal: str
    phases: List[str]


class GsdOutput(BaseModel):
    """Schema for the output."""
    phase_plan: List[Dict[str, str]]
    anchor: str
    planned_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_gsd_input(input_data: Dict[str, Any]) -> GsdInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = GsdInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.goal or not input_obj.goal.strip():
        raise ValueError("Invalid input: 'goal' must be non-empty")
    if not input_obj.phases:
        raise ValueError("Invalid input: 'phases' must have ≥1 phase")
    return input_obj


def planejar(goal: str, phases: List[str]) -> Dict[str, Any]:
    """Monta plano faseado com exit criteria + âncora de 1 parágrafo."""
    v = validate_gsd_input({"goal": goal, "phases": phases})
    plan = [{"phase": p, "exit": f"{p} resumido em arquivo", " packet": f"ctx/{p}.md"}
            for p in v.phases]
    out = GsdOutput(
        phase_plan=plan,
        anchor=f"Âncora: {v.goal} — recarregar por fase; deriva → re-ancorar.",
        planned_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "phases": len(plan)},
    )
    return out.model_dump(mode="json")


def ignicao(goal: str, phases: List[str]) -> Dict[str, Any]:
    """Função principal: valida → planeja → dict."""
    return planejar(goal, phases)


if __name__ == "__main__":
    import json

    r1 = ignicao("ship auth", ["plan", "build", "verify"])
    assert r1["status"] == "success" and len(r1["phase_plan"]) == 3, r1
    assert "Âncora" in r1["anchor"], r1
    try:
        ignicao("", [])
        raise SystemExit("FAIL: vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 2}, ensure_ascii=False))
