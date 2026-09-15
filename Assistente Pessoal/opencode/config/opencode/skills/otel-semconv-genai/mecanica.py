"""
Mecânica de Ignição (Execution & Validation) — otel-semconv-genai.
Normaliza eventos p/ convenções genai (spans, custo, authz, linhagem).
Helenizado de open-telemetry/semantic-conventions — só convenções.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


KNOWN_PREFIXES = ("genai.", "cost.", "fga.", "derivation.")


class OtelInput(BaseModel):
    """Input schema: span + attributes."""
    span: str
    attributes: Dict[str, Any]


class OtelOutput(BaseModel):
    """Schema for the output."""
    span: str
    attributes: Dict[str, Any]
    normalized_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_otel_input(input_data: Dict[str, Any]) -> OtelInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = OtelInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.span or not input_obj.span.strip():
        raise ValueError("Invalid input: 'span' must be non-empty")
    return input_obj


def normalizar(span: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Normaliza: só attrs com prefixo conhecido passam; resto vira sugestão."""
    v = validate_otel_input({"span": span, "attributes": attributes})
    ok = {k: val for k, val in v.attributes.items()
          if any(k.startswith(p) for p in KNOWN_PREFIXES)}
    unknown = sorted(set(v.attributes) - set(ok))
    out = OtelOutput(
        span=v.span,
        attributes=ok,
        normalized_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "dropped_unknown": unknown},
    )
    return out.model_dump(mode="json")


def ignicao(span: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Função principal: valida → normaliza → dict."""
    return normalizar(span, attributes)


if __name__ == "__main__":
    import json

    r1 = ignicao("genai.chat", {"genai.request.model": "x", "cost.source": "proxy",
                                "cost.exactness": "estimated", "foo": 1})
    assert r1["status"] == "success", r1
    assert r1["attributes"]["genai.request.model"] == "x", r1
    assert r1["validation_details"]["dropped_unknown"] == ["foo"], r1
    try:
        ignicao("   ", {})
        raise SystemExit("FAIL: span vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 2}, ensure_ascii=False))
