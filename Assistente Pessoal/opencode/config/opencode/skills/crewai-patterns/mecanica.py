"""
Mecânica de Ignição (Execution & Validation) — crewai-patterns.
Cards (role/goal/backstory) + contratos (description/expected_output).
Helenizado de crewaiinc/crewai — só padrão; framework nunca como dependência.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class CrewSpecInput(BaseModel):
    """Input schema: card + contract fields."""
    role: str
    goal: str
    task: str
    expected_output: str
    backstory: str = ""


class CrewSpecOutput(BaseModel):
    """Schema for the output."""
    agent_card: Dict[str, str]
    task_contract: Dict[str, str]
    process: str
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_crew_input(input_data: Dict[str, Any]) -> CrewSpecInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = CrewSpecInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    for f in ("role", "goal", "task", "expected_output"):
        if not getattr(input_obj, f) or not getattr(input_obj, f).strip():
            raise ValueError(f"Invalid input: '{f}' must be non-empty")
    return input_obj


def montar_crew(role: str, goal: str, task: str, expected_output: str,
                backstory: str = "") -> Dict[str, Any]:
    """Monta card + contrato (determinístico offline)."""
    v = validate_crew_input({"role": role, "goal": goal, "task": task,
                             "expected_output": expected_output, "backstory": backstory})
    out = CrewSpecOutput(
        agent_card={"role": v.role, "goal": v.goal, "backstory": v.backstory or "n/a"},
        task_contract={"description": v.task, "expected_output": v.expected_output,
                       "agent": v.role},
        process="sequential",
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "telemetry": "opt-out exigido"},
    )
    return out.model_dump(mode="json")


def ignicao(role: str, goal: str, task: str, expected_output: str) -> Dict[str, Any]:
    """Função principal: valida → monta → dict."""
    return montar_crew(role, goal, task, expected_output)


if __name__ == "__main__":
    import json

    r1 = ignicao("Senior Data Researcher", "uncover developments", "research {topic}",
                 "10 bullet points")
    assert r1["status"] == "success" and r1["process"] == "sequential", r1
    assert r1["task_contract"]["expected_output"] == "10 bullet points", r1
    try:
        ignicao("", "", "", "")
        raise SystemExit("FAIL: campos vazios deveriam rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 2}, ensure_ascii=False))
