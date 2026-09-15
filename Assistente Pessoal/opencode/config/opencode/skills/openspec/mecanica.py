"""
Mecânica de Ignição (Execution & Validation) — openspec.
Ciclo explore/propose/apply/archive com 4 artefatos + cenários WHEN/THEN.
Helenizado de Fission-AI/OpenSpec — só lifecycle; sem cópia literal.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


REQUIRED_ARTIFACTS = ("proposal", "specs", "design", "tasks")


class OpenSpecInput(BaseModel):
    """Input schema: change name + artifacts present."""
    change_name: str
    artifacts: Dict[str, Any]


class OpenSpecOutput(BaseModel):
    """Schema for the output."""
    change_name: str
    artifacts: List[str]
    archived: bool
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_openspec_input(input_data: Dict[str, Any]) -> OpenSpecInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = OpenSpecInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.change_name or not input_obj.change_name.strip():
        raise ValueError("Invalid input: 'change_name' must be non-empty")
    if not isinstance(input_obj.artifacts, dict):
        raise ValueError("Invalid input: 'artifacts' must be a dict")
    return input_obj


def validar_ciclo(change_name: str, artifacts: Dict[str, Any]) -> Dict[str, Any]:
    """Valida o ciclo: 4 artefatos + specs com cenário WHEN/THEN."""
    validated = validate_openspec_input({"change_name": change_name, "artifacts": artifacts})
    missing = [a for a in REQUIRED_ARTIFACTS if a not in validated.artifacts]
    specs_text = str(validated.artifacts.get("specs", ""))
    has_scenario = "WHEN" in specs_text and "THEN" in specs_text
    problems: List[str] = []
    if missing:
        problems.append(f"artefatos ausentes: {missing}")
    if not has_scenario:
        problems.append("specs sem cenário WHEN/THEN concreto")
    ok = not problems
    out = OpenSpecOutput(
        change_name=validated.change_name,
        artifacts=sorted(validated.artifacts.keys()),
        archived=bool(validated.artifacts.get("archived", False)),
        validated_at=datetime.now(timezone.utc),
        status="success" if ok else "failure",
        validation_details={"schema_check": True, "problems": problems,
                            "telemetry": "opt-out exigido"},
    )
    return out.model_dump(mode="json")


def ignicao(change_name: str, artifacts: Dict[str, Any]) -> Dict[str, Any]:
    """Função principal: valida → ciclo → dict."""
    return validar_ciclo(change_name, artifacts)


if __name__ == "__main__":
    import json

    good = {"proposal": "why", "specs": "WHEN click THEN dark + persists", "design": "css vars",
            "tasks": ["1.1 ctx", "2.1 vars"]}
    r1 = ignicao("add-dark-mode", good)
    assert r1["status"] == "success" and r1["artifacts"] == ["design", "proposal", "specs", "tasks"], r1
    r2 = ignicao("add-dark-mode", {"proposal": "why"})
    assert r2["status"] == "failure" and r2["validation_details"]["problems"], r2
    try:
        ignicao("   ", {})
        raise SystemExit("FAIL: nome vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
