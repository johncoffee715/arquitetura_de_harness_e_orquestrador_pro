"""
Mecânica de Ignição — langgraph-redis-patterns. Namespace + TTL (offline).
Helenizado de redis-developer/langgraph-redis — só padrão.
"""
from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class In(BaseModel):
    thread: str
    ttl_s: int


class Out(BaseModel):
    store_spec: Dict[str, str]
    namespace: str
    picked_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def ignicao(thread: str, ttl_s: int) -> Dict[str, Any]:
    """Namespace por thread + TTL obrigatório."""
    try:
        v = In(thread=thread, ttl_s=ttl_s)
    except ValidationError as e:
        raise ValueError(f"Invalid input: {e}")
    if not v.thread.strip():
        raise ValueError("Invalid input: 'thread' must be non-empty")
    if v.ttl_s <= 0:
        raise ValueError("Invalid ttl_s: TTL obrigatório > 0")
    ns = f"ckpt:{v.thread}"
    return Out(store_spec={"backend": "key-value", "namespace": ns, "ttl": f"{v.ttl_s}s"},
               namespace=ns, picked_at=datetime.now(timezone.utc), status="success",
               validation_details={"schema_check": True}).model_dump(mode="json")


if __name__ == "__main__":
    import json
    r = ignicao("sessao-7", 3600)
    assert r["namespace"] == "ckpt:sessao-7" and r["status"] == "success", r
    try:
        ignicao("", 0); raise SystemExit("FAIL")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 2}, ensure_ascii=False))
