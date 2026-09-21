"""
Mecânica de Ignição (Execution & Validation) — grok-build.
Spec CLI/TUI: composition root + workspace + entry modes.
Helenizado de xai-org/grok-build (clone SHA 3794978) — só padrões.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


VALID_MODES = ("headless", "leader", "stdio")


class CliInput(BaseModel):
    """Input schema: binary + entry modes."""
    binary: str
    modes: List[str]


class CliOutput(BaseModel):
    """Schema for the output."""
    cli_spec: Dict[str, Any]
    workspace_spec: Dict[str, Any]
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_cli_input(input_data: Dict[str, Any]) -> CliInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = CliInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.binary or not input_obj.binary.strip():
        raise ValueError("Invalid input: 'binary' must be non-empty")
    if not input_obj.modes:
        raise ValueError("Invalid input: 'modes' must have ≥1 mode")
    bad = [m for m in input_obj.modes if m not in VALID_MODES]
    if bad:
        raise ValueError(f"Invalid modes: {bad} (use {list(VALID_MODES)})")
    return input_obj


def especificar_cli(binary: str, modes: List[str]) -> Dict[str, Any]:
    """Monta spec: composition root + workspace + modos."""
    v = validate_cli_input({"binary": binary, "modes": modes})
    out = CliOutput(
        cli_spec={"binary": v.binary, "composition_root": True, "modes": v.modes},
        workspace_spec={"fs": True, "vcs": True, "exec": True, "checkpoints": True},
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "source_sha": "3794978"},
    )
    return out.model_dump(mode="json")


def ignicao(binary: str, modes: List[str]) -> Dict[str, Any]:
    """Função principal: valida → especifica → dict."""
    return especificar_cli(binary, modes)


if __name__ == "__main__":
    import json

    r1 = ignicao("xai-grok-pager", ["headless", "leader", "stdio"])
    assert r1["status"] == "success" and r1["workspace_spec"]["checkpoints"] is True, r1
    try:
        ignicao("", [])
        raise SystemExit("FAIL: vazio deveria rejeitar")
    except ValueError:
        pass
    try:
        ignicao("x", ["daemon"])
        raise SystemExit("FAIL: modo inválido deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
