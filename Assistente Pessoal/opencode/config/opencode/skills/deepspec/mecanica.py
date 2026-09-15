"""
Mecânica de Ignição (Execution & Validation) — deepspec.
Acceptance-rate de speculative decoding: accepted/proposed por benchmark + warnings.
Helenizado de deepseek-ai/DeepSpec — só metodologia; sem treino pesado por default.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


VALID_BENCHMARKS = (
    "gsm8k", "math500", "aime25", "humaneval", "mbpp",
    "livecodebench", "mt-bench", "alpaca", "arena-hard-v2",
)


class SpecDecEvalInput(BaseModel):
    """Input schema: contagens + benchmark."""
    accepted: int
    proposed: int
    benchmark: str


class SpecDecEvalOutput(BaseModel):
    """Schema for the output."""
    acceptance_rate: float
    benchmark: str
    evaluated_at: datetime
    status: str  # "success" or "failure"
    validation_details: Dict[str, Any] = {}


def validate_deepspec_input(input_data: Dict[str, Any]) -> SpecDecEvalInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = SpecDecEvalInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if input_obj.proposed <= 0:
        raise ValueError("Invalid input: 'proposed' must be > 0")
    if not 0 <= input_obj.accepted <= input_obj.proposed:
        raise ValueError("Invalid input: 0 <= accepted <= proposed required")
    if input_obj.benchmark not in VALID_BENCHMARKS:
        raise ValueError(f"Invalid benchmark: must be one of {VALID_BENCHMARKS}")
    return input_obj


def report_acceptance(accepted: int, proposed: int, benchmark: str) -> Dict[str, Any]:
    """Calcula acceptance-rate e emite report determinístico com warnings."""
    validated = validate_deepspec_input(
        {"accepted": accepted, "proposed": proposed, "benchmark": benchmark}
    )
    rate = validated.accepted / validated.proposed
    out = SpecDecEvalOutput(
        acceptance_rate=round(rate, 4),
        benchmark=validated.benchmark,
        evaluated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={
            "schema_check": True,
            "setup_aligned": True,
            "cost_warning": "comparações só válidas com setup de treino alinhado ao repo",
        },
    )
    return out.model_dump(mode="json")


def ignicao(accepted: int, proposed: int, benchmark: str) -> Dict[str, Any]:
    """Função principal: valida → calcula → dict."""
    return report_acceptance(accepted, proposed, benchmark)


if __name__ == "__main__":
    import json

    r1 = ignicao(750, 1000, "humaneval")
    assert r1["status"] == "success" and r1["acceptance_rate"] == 0.75, r1
    assert r1["benchmark"] == "humaneval", r1
    r2 = ignicao(1000, 1000, "gsm8k")
    assert r2["acceptance_rate"] == 1.0, r2
    try:
        ignicao(5, 0, "gsm8k")
        raise SystemExit("FAIL: proposed=0 deveria rejeitar")
    except ValueError:
        pass
    try:
        ignicao(3, 5, "benchmark-inventado")
        raise SystemExit("FAIL: benchmark inválido deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 4}, ensure_ascii=False))
