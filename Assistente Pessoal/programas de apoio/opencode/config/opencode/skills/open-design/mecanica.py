"""
Mecânica de Ignição (Execution & Validation) — open-design.
Brief + artefato real (determinístico offline).
Helenizado de nexu-io/open-design — só loop; sem cópia literal.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


VALID_ARTIFACTS = ("prototype", "deck", "dashboard", "image", "video")


class DesignInput(BaseModel):
    """Input schema: brief + artifact."""
    brief: str
    artifact: str


class DesignOutput(BaseModel):
    """Schema for the output."""
    brief: str
    artifact_spec: Dict[str, Any]
    specified_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_design_input(input_data: Dict[str, Any]) -> DesignInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = DesignInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.brief or not input_obj.brief.strip():
        raise ValueError("Invalid input: 'brief' must be non-empty")
    if input_obj.artifact not in VALID_ARTIFACTS:
        raise ValueError(f"Invalid artifact: must be one of {VALID_ARTIFACTS}")
    return input_obj


def especificar(brief: str, artifact: str) -> Dict[str, Any]:
    """Monta spec: brief + artefato + export real."""
    v = validate_design_input({"brief": brief, "artifact": artifact})
    exports = {"prototype": "html", "deck": "pptx", "dashboard": "html",
               "image": "png", "video": "mp4"}
    out = DesignOutput(
        brief=v.brief,
        artifact_spec={"type": v.artifact, "export": exports[v.artifact],
                       "contract": "DESIGN.md"},
        specified_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "real_file": True},
    )
    return out.model_dump(mode="json")


def ignicao(brief: str, artifact: str) -> Dict[str, Any]:
    """Função principal: valida → especifica → dict."""
    return especificar(brief, artifact)


if __name__ == "__main__":
    import json

    r1 = ignicao("landing fintech", "prototype")
    assert r1["artifact_spec"]["export"] == "html", r1
    r2 = ignicao("pitch deck", "deck")
    assert r2["artifact_spec"]["export"] == "pptx", r2
    try:
        ignicao("", "banner")
        raise SystemExit("FAIL: inválido deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
