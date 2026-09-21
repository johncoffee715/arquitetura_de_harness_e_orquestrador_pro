"""
Mecânica de Ignição (Execution & Validation) — ecc.
Research-first + AgentShield scan de configs (determinístico offline p/ validação).
Helenizado de affaan-m/ecc — só 4 padrões.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


SECRET_KEYS = ("api_key", "apikey", "secret", "token", "password", "private_key")


class EccInput(BaseModel):
    """Input schema: topic + configs to shield-scan."""
    topic: str
    configs: Dict[str, Any]


class ShieldFinding(BaseModel):
    """Um achado do shield."""
    field: str
    issue: str


class EccOutput(BaseModel):
    """Schema for the output."""
    research_brief: str
    shield_report: List[ShieldFinding]
    shield_pass: bool
    checked_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_ecc_input(input_data: Dict[str, Any]) -> EccInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = EccInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.topic or not input_obj.topic.strip():
        raise ValueError("Invalid input: 'topic' must be non-empty")
    return input_obj


def otimizar(topic: str, configs: Dict[str, Any]) -> Dict[str, Any]:
    """Research-first (brief) + shield scan (segredos em configs)."""
    validated = validate_ecc_input({"topic": topic, "configs": configs})
    findings: List[ShieldFinding] = []
    for k, v in validated.configs.items():
        kl = k.lower()
        if any(s in kl for s in SECRET_KEYS) and str(v).strip() and str(v) != "***":
            findings.append(ShieldFinding(field=k, issue="possível segredo em config (mascarar)"))
    out = EccOutput(
        research_brief=f"research-first p/ '{validated.topic}': docs oficiais → padrões → código",
        shield_report=findings,
        shield_pass=not findings,
        checked_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "findings": len(findings)},
    )
    return out.model_dump(mode="json")


def ignicao(topic: str, configs: Dict[str, Any]) -> Dict[str, Any]:
    """Função principal: valida → otimiza → dict."""
    return otimizar(topic, configs)


if __name__ == "__main__":
    import json

    r1 = ignicao("stripe webhooks", {"env": "prod", "retries": 3})
    assert r1["status"] == "success" and r1["shield_pass"] is True, r1
    r2 = ignicao("stripe webhooks", {"api_key": "sk-live-123"})
    assert r2["shield_pass"] is False and len(r2["shield_report"]) == 1, r2
    try:
        ignicao("   ", {})
        raise SystemExit("FAIL: topic vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
