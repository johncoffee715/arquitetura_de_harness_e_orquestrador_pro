"""
Mecânica de Ignição — postgres-patterns. WAL-first + MVCC (offline).
Helenizado de postgres/postgres — só conceitos.
"""
from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class In(BaseModel):
    write: str
    durable: bool = False


class Out(BaseModel):
    durability_check: str
    checked_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def ignicao(write: str, durable: bool = False) -> Dict[str, Any]:
    """Ack só se durável (WAL primeiro); senão hold."""
    try:
        v = In(write=write, durable=durable)
    except ValidationError as e:
        raise ValueError(f"Invalid input: {e}")
    if not v.write.strip():
        raise ValueError("Invalid input: 'write' must be non-empty")
    verdict = "ack" if v.durable else "hold: durar antes de confirmar (WAL-first)"
    return Out(durability_check=verdict, checked_at=datetime.now(timezone.utc),
               status="success",
               validation_details={"schema_check": True, "mvcc": "readers-never-block"}
               ).model_dump(mode="json")


if __name__ == "__main__":
    import json
    assert ignicao("w1", True)["durability_check"] == "ack"
    assert ignicao("w1", False)["durability_check"].startswith("hold")
    try:
        ignicao("   "); raise SystemExit("FAIL")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
