"""
Mecânica de Ignição (Execution & Validation) — tech-leads-club-agent-skills.
Gate de registry: scan-before-publish + pin de integridade + audit.
Helenizado de tech-leads-club/agent-skills — só disciplina; sem cópia literal.
"""

import hashlib
from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class RegistryReviewInput(BaseModel):
    """Input schema: skill sob avaliação."""
    skill_id: str
    source: str
    has_binary: bool = False


class RegistryReviewOutput(BaseModel):
    """Schema for the output."""
    scan_verdict: str  # "pass" or "fail"
    integrity_pin: str
    reviewed_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_registry_input(input_data: Dict[str, Any]) -> RegistryReviewInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = RegistryReviewInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.skill_id or not input_obj.skill_id.strip():
        raise ValueError("Invalid input: 'skill_id' must be non-empty")
    if not input_obj.source or not input_obj.source.strip():
        raise ValueError("Invalid input: 'source' must be non-empty")
    return input_obj


def validar_skill(skill_id: str, source: str, has_binary: bool = False) -> Dict[str, Any]:
    """Gate determinístico offline: binário = fail; senão pin SHA + pass."""
    validated = validate_registry_input(
        {"skill_id": skill_id, "source": source, "has_binary": has_binary}
    )
    if validated.has_binary:
        verdict, pin, reason = "fail", "none", "binário em skill: deny (100% open source exigido)"
    else:
        pin = "sha256:" + hashlib.sha256(
            f"{validated.skill_id}|{validated.source}".encode()
        ).hexdigest()[:16]
        verdict, reason = "pass", "open-source + pin gerado (scan externo requerido pré-publish)"
    out = RegistryReviewOutput(
        scan_verdict=verdict,
        integrity_pin=pin,
        reviewed_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "reason": reason,
                            "attribution": "Tech Leads Club (CC-BY-4.0)"},
    )
    return out.model_dump(mode="json")


def ignicao(skill_id: str, source: str, has_binary: bool = False) -> Dict[str, Any]:
    """Função principal: valida → gate → dict."""
    return validar_skill(skill_id, source, has_binary)


if __name__ == "__main__":
    import json

    r1 = ignicao("tlc-spec-driven", "https://github.com/tech-leads-club/agent-skills")
    assert r1["status"] == "success" and r1["scan_verdict"] == "pass", r1
    assert r1["integrity_pin"].startswith("sha256:"), r1
    r2 = ignicao("evil-skill", "https://example.com/x", has_binary=True)
    assert r2["scan_verdict"] == "fail" and r2["integrity_pin"] == "none", r2
    try:
        ignicao("", "")
        raise SystemExit("FAIL: input vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
