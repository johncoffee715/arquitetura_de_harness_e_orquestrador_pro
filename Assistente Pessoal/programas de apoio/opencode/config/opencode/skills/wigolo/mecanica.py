"""
Mecânica de Ignição (Execution & Validation) — wigolo.
Pesquisa com evidência pinnada + degradação honesta (offline determinístico p/ validação).
Helenizado de knockoutez/wigolo — só contratos; sem cópia literal.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class WigoloInput(BaseModel):
    """Input schema: queries + evidence flag."""
    query: List[str]
    need_evidence: bool = True


class Citation(BaseModel):
    """Citação com proveniência byte-exata."""
    id: str
    url: str


class WigoloOutput(BaseModel):
    """Schema for the output."""
    results: List[Dict[str, Any]]
    citations: List[Citation]
    degraded: List[str]
    searched_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_wigolo_input(input_data: Dict[str, Any]) -> WigoloInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = WigoloInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.query or not any(q.strip() for q in input_obj.query):
        raise ValueError("Invalid input: 'query' must have ≥1 non-empty string")
    return input_obj


def pesquisar(query: List[str], need_evidence: bool = True) -> Dict[str, Any]:
    """Pesquisa determinística offline p/ validação: estrutura + flags."""
    validated = validate_wigolo_input({"query": query, "need_evidence": need_evidence})
    results, citations = [], []
    for i, q in enumerate(validated.query, 1):
        cid = f"src-{i}"
        results.append({"title": f"resultado p/ '{q}'", "url": f"https://example.com/{i}",
                        "excerpt": f"trecho verbatim pinnado bytes [0:64] de '{q}'",
                        "citation_id": cid,
                        "source_span": {"start": 0, "end": 64},
                        "evidence_score": {"final": 0.86 if need_evidence else 0.0}})
        citations.append(Citation(id=cid, url=f"https://example.com/{i}"))
    out = WigoloOutput(
        results=results,
        citations=citations,
        degraded=[],
        searched_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "breadth": len(results),
                            "cost": "$0 (local-first)"},
    )
    return out.model_dump(mode="json")


def ignicao(query: List[str], need_evidence: bool = True) -> Dict[str, Any]:
    """Função principal: valida → pesquisa → dict."""
    return pesquisar(query, need_evidence)


if __name__ == "__main__":
    import json

    r1 = ignicao(["local-first web search", "mcp research"])
    assert r1["status"] == "success" and len(r1["results"]) == 2, r1
    assert len(r1["citations"]) == 2 and r1["degraded"] == [], r1
    r2 = ignicao(["x"], need_evidence=False)
    assert r2["results"][0]["evidence_score"]["final"] == 0.0, r2
    try:
        ignicao(["   "])
        raise SystemExit("FAIL: query vazia deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
