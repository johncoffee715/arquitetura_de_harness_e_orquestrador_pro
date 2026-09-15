"""
Mecânica de Ignição — redis-patterns. Estrutura + TTL obrigatório (offline).
Helenizado de redis/redis — só conceitos.
"""
from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


STRUCTS = {"counter": "string", "object": "hash", "queue": "list",
           "unique": "set", "ranking": "zset", "log": "stream"}


class In(BaseModel):
    use: str
    ttl_s: int


class Out(BaseModel):
    structure_pick: str
    ttl_policy: str
    picked_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def ignicao(use: str, ttl_s: int) -> Dict[str, Any]:
    """Estrutura por uso + TTL>0 obrigatório."""
    try:
        v = In(use=use, ttl_s=ttl_s)
    except ValidationError as e:
        raise ValueError(f"Invalid input: {e}")
    if v.use not in STRUCTS:
        raise ValueError(f"Invalid use: must be one of {sorted(STRUCTS)}")
    if v.ttl_s <= 0:
        raise ValueError("Invalid ttl_s: TTL-by-design exige ttl_s > 0")
    return Out(structure_pick=STRUCTS[v.use], ttl_policy=f"EX {v.ttl_s}s",
               picked_at=datetime.now(timezone.utc), status="success",
               validation_details={"schema_check": True}).model_dump(mode="json")


if __name__ == "__main__":
    import json
    assert ignicao("ranking", 300)["structure_pick"] == "zset"
    assert ignicao("queue", 60)["ttl_policy"] == "EX 60s"
    try:
        ignicao("ranking", 0); raise SystemExit("FAIL")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
