"""
Mecânica de Ignição (Execution & Validation) — openagentscontrol.
Gate plan-first: plano + aprovação (ou fast-track trivial) + validação.
Helenizado de darrenhinde/openagentscontrol — só o padrão.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class OACInput(BaseModel):
    """Input schema: plan + approval flag."""
    plan: str
    approved: bool
    trivial: bool = False


class OACOutput(BaseModel):
    """Schema for the output."""
    plan: str
    approved: bool
    gate: str  # "execute" | "blocked" | "fast_track"
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_oac_input(input_data: Dict[str, Any]) -> OACInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = OACInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.plan or not input_obj.plan.strip():
        raise ValueError("Invalid input: 'plan' must be non-empty")
    return input_obj


def aplicar_gate(plan: str, approved: bool, trivial: bool = False) -> Dict[str, Any]:
    """Gate determinístico: aprovado→execute; trivial→fast_track; senão blocked."""
    validated = validate_oac_input({"plan": plan, "approved": approved, "trivial": trivial})
    if validated.approved:
        gate, why = "execute", "plano aprovado: executar com validação por etapa"
    elif validated.trivial:
        gate, why = "fast_track", "trivial whitelistado: via rápida com rationale logado"
    else:
        gate, why = "blocked", "sem aprovação: NENHUMA escrita permitida"
    out = OACOutput(
        plan=validated.plan,
        approved=validated.approved,
        gate=gate,
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "rationale": why},
    )
    return out.model_dump(mode="json")


def ignicao(plan: str, approved: bool, trivial: bool = False) -> Dict[str, Any]:
    """Função principal: valida → gate → dict."""
    return aplicar_gate(plan, approved, trivial)


if __name__ == "__main__":
    import json

    r1 = ignicao("add login endpoint com testes", True)
    assert r1["gate"] == "execute", r1
    r2 = ignicao("qualquer coisa", False)
    assert r2["gate"] == "blocked", r2
    r3 = ignicao("typo no README", False, trivial=True)
    assert r3["gate"] == "fast_track", r3
    try:
        ignicao("   ", False)
        raise SystemExit("FAIL: plano vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 4}, ensure_ascii=False))
