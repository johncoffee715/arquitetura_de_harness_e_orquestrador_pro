"""
Mecânica de Ignição (Execution & Validation) — buzz.
Backend por hardware + spec de transcrição (determinístico offline).
Helenizado de chidiwilliams/buzz — só pipeline.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


BACKENDS = {"cuda": "whisper+CUDA", "mps": "whisper Apple Silicon",
            "vulkan": "whisper.cpp Vulkan", "cpu": "whisper.cpp/HF"}


class BuzzInput(BaseModel):
    """Input schema: audio + hardware."""
    audio: str
    hardware: str


class BuzzOutput(BaseModel):
    """Schema for the output."""
    backend_pick: str
    transcript_spec: Dict[str, Any]
    picked_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_buzz_input(input_data: Dict[str, Any]) -> BuzzInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = BuzzInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.audio or not input_obj.audio.strip():
        raise ValueError("Invalid input: 'audio' must be non-empty")
    if input_obj.hardware not in BACKENDS:
        raise ValueError(f"Invalid hardware: must be one of {sorted(BACKENDS)}")
    return input_obj


def especificar(audio: str, hardware: str) -> Dict[str, Any]:
    """Backend por hardware + spec do pipeline."""
    v = validate_buzz_input({"audio": audio, "hardware": hardware})
    out = BuzzOutput(
        backend_pick=BACKENDS[v.hardware],
        transcript_spec={"audio": v.audio, "pipeline": ["separation", "whisper",
                         "diarization", "punctuation"], "exports": ["txt", "srt", "vtt"]},
        picked_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "offline": True},
    )
    return out.model_dump(mode="json")


def ignicao(audio: str, hardware: str) -> Dict[str, Any]:
    """Função principal: valida → especifica → dict."""
    return especificar(audio, hardware)


if __name__ == "__main__":
    import json

    r1 = ignicao("entrevista.mp3", "cuda")
    assert r1["backend_pick"] == "whisper+CUDA", r1
    assert r1["transcript_spec"]["exports"] == ["txt", "srt", "vtt"], r1
    try:
        ignicao("", "tpu")
        raise SystemExit("FAIL: inválido deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 2}, ensure_ascii=False))
