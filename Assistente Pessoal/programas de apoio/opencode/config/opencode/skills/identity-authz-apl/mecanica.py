"""
Mecânica de Ignição (Execution & Validation) — identity-authz-apl.
Avaliação ABAC: rules when/then por salience (deny > permit > default), para na decisão.
Helenizado de intuit/identity-authz-apl — só padrão; sem engine Java.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


SAL_ORDER = {"deny": 3, "permit": 2, "default": 1}


class AplRule(BaseModel):
    """Uma regra: nome, tipo, salience, conds (attrs esperados), decisão."""
    name: str
    kind: str  # deny | permit | default
    salience: int = 0
    match: Dict[str, str] = {}
    decision: str = ""


class AplInput(BaseModel):
    """Input schema: rules + attrs."""
    rules: List[AplRule]
    attrs: Dict[str, str]


class AplOutput(BaseModel):
    """Schema for the output."""
    decision: str
    fired_rules: List[str]
    evaluated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_apl_input(input_data: Dict[str, Any]) -> AplInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = AplInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.rules:
        raise ValueError("Invalid input: 'rules' must have ≥1 rule")
    kinds = [r.kind for r in input_obj.rules]
    if any(k not in SAL_ORDER for k in kinds):
        raise ValueError("Invalid rule kind: must be deny|permit|default")
    if kinds.count("default") > 1:
        raise ValueError("Invalid: only one default rule allowed")
    return input_obj


def decidir(rules: List[Dict[str, Any]], attrs: Dict[str, str]) -> Dict[str, Any]:
    """Avalia por salience (deny > permit > default); para na 1ª decisão."""
    v = validate_apl_input({"rules": rules, "attrs": attrs})
    ordered = sorted(v.rules, key=lambda r: (SAL_ORDER[r.kind], r.salience), reverse=True)
    fired: List[str] = []
    decision = "deny"
    for r in ordered:
        if all(attrs.get(k) == val for k, val in r.match.items()):
            fired.append(r.name)
            decision = r.decision or ("deny" if r.kind == "deny" else "permit")
            break
    if not fired:
        decision = "deny"
    out = AplOutput(
        decision=decision,
        fired_rules=fired,
        evaluated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "evaluated": len(ordered),
                            "explain": f"fired={fired or 'none→default-deny'}"},
    )
    return out.model_dump(mode="json")


def ignicao(rules: List[Dict[str, Any]], attrs: Dict[str, str]) -> Dict[str, Any]:
    """Função principal: valida → decide → dict."""
    return decidir(rules, attrs)


if __name__ == "__main__":
    import json

    rules = [
        {"name": "r-deny-basic", "kind": "deny", "salience": 2,
         "match": {"sku": "BASIC"}, "decision": "deny"},
        {"name": "r-permit-plus", "kind": "permit", "salience": 1,
         "match": {"sku": "PLUS", "role": "admin"}, "decision": "permit"},
    ]
    r1 = ignicao(rules, {"sku": "PLUS", "role": "admin"})
    assert r1["decision"] == "permit" and r1["fired_rules"] == ["r-permit-plus"], r1
    r2 = ignicao(rules, {"sku": "BASIC", "role": "admin"})
    assert r2["decision"] == "deny", r2
    try:
        ignicao([], {})
        raise SystemExit("FAIL: rules vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
