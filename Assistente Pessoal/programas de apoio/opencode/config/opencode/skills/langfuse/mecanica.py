"""
Mecânica de Ignição (Execution & Validation) — langfuse.
Run avaliado: trace + dataset + score com porta de qualidade.
Helenizado de langfuse/langfuse — só o loop; sem plataforma.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class LangfuseInput(BaseModel):
    """Input schema: trace + dataset + score."""
    trace: str
    dataset: str
    score: float


class LangfuseOutput(BaseModel):
    """Schema for the output."""
    trace_spec: str
    dataset_run: str
    eval_report: Dict[str, Any]
    recorded_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_langfuse_input(input_data: Dict[str, Any]) -> LangfuseInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = LangfuseInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.trace or not input_obj.trace.strip():
        raise ValueError("Invalid input: 'trace' must be non-empty")
    if not input_obj.dataset or not input_obj.dataset.strip():
        raise ValueError("Invalid input: 'dataset' must be non-empty")
    if not 0.0 <= input_obj.score <= 1.0:
        raise ValueError("Invalid input: 'score' must be in [0,1]")
    return input_obj


def registrar_run(trace: str, dataset: str, score: float) -> Dict[str, Any]:
    """Registra run com porta de qualidade (>=0.7)."""
    v = validate_langfuse_input({"trace": trace, "dataset": dataset, "score": score})
    passed = v.score >= 0.7
    out = LangfuseOutput(
        trace_spec=v.trace,
        dataset_run=f"{v.dataset}@run",
        eval_report={"score": v.score, "passed": passed},
        recorded_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "comparable": True},
    )
    return out.model_dump(mode="json")


def ignicao(trace: str, dataset: str, score: float) -> Dict[str, Any]:
    """Função principal: valida → registra → dict."""
    return registrar_run(trace, dataset, score)


if __name__ == "__main__":
    import json

    r1 = ignicao("trace-login", "auth-v3", 0.85)
    assert r1["status"] == "success" and r1["eval_report"]["passed"] is True, r1
    r2 = ignicao("trace-login", "auth-v3", 0.4)
    assert r2["eval_report"]["passed"] is False, r2
    try:
        ignicao("", "", 9.9)
        raise SystemExit("FAIL: input inválido deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
