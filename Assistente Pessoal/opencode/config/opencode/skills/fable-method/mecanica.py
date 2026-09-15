"""
Mecânica de Ignição (Execution & Validation) — fable-method.
Classify + done_spec com bounds duros (determinístico offline).
Helenizado de Sahir619/fable-method — só o loop; sem cópia literal.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


VALID_SHAPES = ("trivial", "question", "task", "plan-first")


class FableInput(BaseModel):
    """Input schema: ask + shape."""
    ask: str
    shape: str


class FableOutput(BaseModel):
    """Schema for the output."""
    classification: str
    done_spec: str
    bounds: Dict[str, int]
    classified_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_fable_input(input_data: Dict[str, Any]) -> FableInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = FableInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.ask or not input_obj.ask.strip():
        raise ValueError("Invalid input: 'ask' must be non-empty")
    if input_obj.shape not in VALID_SHAPES:
        raise ValueError(f"Invalid shape: must be one of {VALID_SHAPES}")
    return input_obj


DONE_TEMPLATES = {
    "trivial": "do it, run the one obvious check, report in 2 sentences",
    "question": "diagnose only, change nothing, findings + one recommendation",
    "task": "evidence → decide → surgical edits → observed verify (≤3 cycles)",
    "plan-first": "plan artifact with named verifications, STOP for approval",
}


def classificar(ask: str, shape: str) -> Dict[str, Any]:
    """Classifica + done_spec + bounds duros."""
    v = validate_fable_input({"ask": ask, "shape": shape})
    out = FableOutput(
        classification=v.shape,
        done_spec=DONE_TEMPLATES[v.shape],
        bounds={"max_verify_cycles": 3, "max_fruitless_lookups": 2},
        classified_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True},
    )
    return out.model_dump(mode="json")


def ignicao(ask: str, shape: str) -> Dict[str, Any]:
    """Função principal: valida → classifica → dict."""
    return classificar(ask, shape)


if __name__ == "__main__":
    import json

    r1 = ignicao("fix typo", "trivial")
    assert r1["classification"] == "trivial" and "2 sentences" in r1["done_spec"], r1
    r2 = ignicao("add auth", "plan-first")
    assert "STOP for approval" in r2["done_spec"], r2
    assert r2["bounds"] == {"max_verify_cycles": 3, "max_fruitless_lookups": 2}, r2
    try:
        ignicao("", "task")
        raise SystemExit("FAIL: ask vazio deveria rejeitar")
    except ValueError:
        pass
    try:
        ignicao("x", "epic")
        raise SystemExit("FAIL: shape inválido deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 4}, ensure_ascii=False))
