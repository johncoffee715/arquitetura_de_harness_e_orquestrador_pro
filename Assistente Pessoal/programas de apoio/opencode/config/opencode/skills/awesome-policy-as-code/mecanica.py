"""
Mecânica de Ignição (Execution & Validation) — awesome-policy-as-code.
Roteamento camada → família + ferramentas (determinístico offline).
Helenizado de hysnsec/awesome-policy-as-code — só taxonomia (CC0).
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


TAXONOMY = {
    "engine": (["OPA/Rego", "Styra DAS", "OPAL", "Topaz"], "runtime + CI"),
    "admission": (["Gatekeeper", "Kyverno", "MagTape"], "k8s admission"),
    "iac-scan": (["Checkov", "Terrascan", "KICS", "Regula"], "CI pré-deploy"),
    "governance": (["Cloud Custodian"], "cloud contínua"),
    "embedded": (["Sentinel"], "embed HashiCorp"),
}


class PolicyInput(BaseModel):
    """Input schema: enforcement layer."""
    layer: str


class PolicyOutput(BaseModel):
    """Schema for the output."""
    family_pick: str
    tools: List[str]
    pipeline_stage: str
    routed_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_policy_input(input_data: Dict[str, Any]) -> PolicyInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = PolicyInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.layer or not input_obj.layer.strip():
        raise ValueError("Invalid input: 'layer' must be non-empty")
    return input_obj


def rotear_layer(layer: str) -> Dict[str, Any]:
    """Roteia camada → família + tools + estágio."""
    v = validate_policy_input({"layer": layer})
    key = v.layer.strip().lower()
    if key not in TAXONOMY:
        return PolicyOutput(
            family_pick="", tools=[], pipeline_stage="",
            routed_at=datetime.now(timezone.utc), status="failure",
            validation_details={"schema_check": True,
                                "reason": f"camada fora da taxonomia: {sorted(TAXONOMY)}"},
        ).model_dump(mode="json")
    tools, stage = TAXONOMY[key]
    out = PolicyOutput(
        family_pick=key, tools=tools, pipeline_stage=stage,
        routed_at=datetime.now(timezone.utc), status="success",
        validation_details={"schema_check": True},
    )
    return out.model_dump(mode="json")


def ignicao(layer: str) -> Dict[str, Any]:
    """Função principal: valida → roteia → dict."""
    return rotear_layer(layer)


if __name__ == "__main__":
    import json

    r1 = ignicao("iac-scan")
    assert r1["status"] == "success" and "Checkov" in r1["tools"], r1
    r2 = ignicao("admission")
    assert r2["pipeline_stage"] == "k8s admission", r2
    r3 = ignicao("blockchain")
    assert r3["status"] == "failure", r3
    try:
        ignicao("   ")
        raise SystemExit("FAIL: layer vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 4}, ensure_ascii=False))
