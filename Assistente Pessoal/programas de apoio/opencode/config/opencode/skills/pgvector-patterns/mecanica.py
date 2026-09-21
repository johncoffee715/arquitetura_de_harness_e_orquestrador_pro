"""
Mecânica de Ignição — pgvector-patterns. Operador + índice (offline).
Helenizado de pgvector/pgvector — só conceitos.
"""
from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class In(BaseModel):
    need: str


class Out(BaseModel):
    operator_pick: str
    index_pick: str
    picked_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def ignicao(need: str) -> Dict[str, Any]:
    """Recall/latência→HNSW; build rápido→IVFFlat."""
    try:
        v = In(need=need)
    except ValidationError as e:
        raise ValueError(f"Invalid input: {e}")
    if not v.need.strip():
        raise ValueError("Invalid input: 'need' must be non-empty")
    idx = "HNSW" if any(k in v.need.lower() for k in ("recall", "latency", "query")) else "IVFFlat"
    return Out(operator_pick="cosine/euclidean/inner-product", index_pick=idx,
               picked_at=datetime.now(timezone.utc), status="success",
               validation_details={"schema_check": True}).model_dump(mode="json")


if __name__ == "__main__":
    import json
    assert ignicao("recall latency")["index_pick"] == "HNSW"
    assert ignicao("fast build")["index_pick"] == "IVFFlat"
    try:
        ignicao("   "); raise SystemExit("FAIL")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
