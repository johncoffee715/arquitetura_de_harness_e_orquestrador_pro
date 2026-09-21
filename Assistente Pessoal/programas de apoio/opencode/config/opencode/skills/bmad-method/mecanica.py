"""
Mecânica de Ignição (Execution & Validation) — bmad-method.
Roteador right-sized: clarify/plan/build/learn + rationale.
Helenizado de bmad-code-org/BMAD-METHOD — só o loop; sem cópia literal.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


VALID_SIZES = ("vague", "big", "small")
ROUTES = {"vague": "clarify", "big": "plan", "small": "build"}


class BmadInput(BaseModel):
    """Input schema: change + size class."""
    change: str
    size: str


class BmadOutput(BaseModel):
    """Schema for the output."""
    route: str
    rationale: str
    routed_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_bmad_input(input_data: Dict[str, Any]) -> BmadInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = BmadInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.change or not input_obj.change.strip():
        raise ValueError("Invalid input: 'change' must be non-empty")
    if input_obj.size not in VALID_SIZES:
        raise ValueError(f"Invalid size: must be one of {VALID_SIZES}")
    return input_obj


def rotear(change: str, size: str) -> Dict[str, Any]:
    """Roteia pelo tamanho: vague→clarify, big→plan, small→build."""
    validated = validate_bmad_input({"change": change, "size": size})
    route = ROUTES[validated.size]
    rationales = {
        "clarify": "noção vaga: explicitar antes de planejar",
        "plan": "ideia grande e clara: profundidade proporcional + contexto durável",
        "build": "mudança pequena: direto ao build+verify, sem cerimônia",
    }
    out = BmadOutput(
        route=route,
        rationale=rationales[route],
        routed_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "learn_back": "Learn alimenta o próximo Plan"},
    )
    return out.model_dump(mode="json")


def ignicao(change: str, size: str) -> Dict[str, Any]:
    """Função principal: valida → roteia → dict."""
    return rotear(change, size)


if __name__ == "__main__":
    import json

    r1 = ignicao("typo no README", "small")
    assert r1["status"] == "success" and r1["route"] == "build", r1
    r2 = ignicao("novo módulo de billing", "big")
    assert r2["route"] == "plan", r2
    r3 = ignicao("melhorar onboarding?", "vague")
    assert r3["route"] == "clarify", r3
    try:
        ignicao("", "small")
        raise SystemExit("FAIL: change vazio deveria rejeitar")
    except ValueError:
        pass
    try:
        ignicao("x", "gigante")
        raise SystemExit("FAIL: size inválido deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 5}, ensure_ascii=False))
