"""
Mecânica de Ignição (Execution & Validation) — testsprite.
Verificação: claims vs observado (determinístico offline).
Helenizado de TestSprite/testsprite-cli (clone SHA 125872f) — só loop + contrato.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class VerifyInput(BaseModel):
    """Input schema: plan + claims + observed."""
    plan: str
    claims: List[str]
    observed: List[str]


class VerifyOutput(BaseModel):
    """Schema for the output."""
    test_plan: str
    verify_report: Dict[str, Any]
    gate_verdict: str  # "pass" | "fail"
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_verify_input(input_data: Dict[str, Any]) -> VerifyInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = VerifyInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.plan or not input_obj.plan.strip():
        raise ValueError("Invalid input: 'plan' must be non-empty")
    if not input_obj.claims:
        raise ValueError("Invalid input: 'claims' must have ≥1 claim")
    return input_obj


def verificar(plan: str, claims: List[str], observed: List[str]) -> Dict[str, Any]:
    """Cruza claims afirmados vs observados; faltantes = fail."""
    v = validate_verify_input({"plan": plan, "claims": claims, "observed": observed})
    missing = [c for c in v.claims if c not in v.observed]
    verdict = "pass" if not missing else "fail"
    out = VerifyOutput(
        test_plan=v.plan,
        verify_report={"claims": v.claims, "observed": v.observed, "missing": missing},
        gate_verdict=verdict,
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "backend": "presumido (declarado)"},
    )
    return out.model_dump(mode="json")


def ignicao(plan: str, claims: List[str], observed: List[str]) -> Dict[str, Any]:
    """Função principal: valida → verifica → dict."""
    return verificar(plan, claims, observed)


if __name__ == "__main__":
    import json

    r1 = ignicao("plan-v1", ["t1 passa", "t2 passa"], ["t1 passa", "t2 passa"])
    assert r1["gate_verdict"] == "pass", r1
    r2 = ignicao("plan-v1", ["t1 passa", "t2 passa"], ["t1 passa"])
    assert r2["gate_verdict"] == "fail" and r2["verify_report"]["missing"] == ["t2 passa"], r2
    try:
        ignicao("", [], [])
        raise SystemExit("FAIL: vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
