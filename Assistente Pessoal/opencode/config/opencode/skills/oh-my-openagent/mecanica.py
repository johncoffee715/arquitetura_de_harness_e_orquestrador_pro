"""
Mecânica de Ignição (Execution & Validation) — oh-my-openagent.
Categoria→modelo + edit hash-ancorado (rejeita mismatch).
Helenizado de code-yeongyu/oh-my-openagent — só padrões.
"""

import hashlib
from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


CATEGORIES = ("visual-engineering", "deep", "quick", "ultrabrain")


class OmoInput(BaseModel):
    """Input schema: work + line + anchor."""
    work: str
    line: str
    anchor: str


class OmoOutput(BaseModel):
    """Schema for the output."""
    category_pick: str
    anchored_edit: Dict[str, Any]
    validated_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_omo_input(input_data: Dict[str, Any]) -> OmoInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = OmoInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.work or not input_obj.work.strip():
        raise ValueError("Invalid input: 'work' must be non-empty")
    return input_obj


def rotear_e_ancorar(work: str, line: str, anchor: str) -> Dict[str, Any]:
    """Categoria por keyword + âncora hash da linha."""
    v = validate_omo_input({"work": work, "line": line, "anchor": anchor})
    low = v.work.lower()
    if any(k in low for k in ("visual", "ui", "frontend")):
        cat = "visual-engineering"
    elif any(k in low for k in ("arch", "logic", "hard")):
        cat = "ultrabrain"
    elif any(k in low for k in ("typo", "one-line", "single")):
        cat = "quick"
    else:
        cat = "deep"
    digest = "sha:" + hashlib.sha256(v.line.encode()).hexdigest()[:6]
    match = (digest == v.anchor)
    out = OmoOutput(
        category_pick=cat,
        anchored_edit={"line": v.line, "expected": v.anchor, "computed": digest,
                       "accepted": match},
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "anchor_match": match},
    )
    return out.model_dump(mode="json")


def ignicao(work: str, line: str, anchor: str) -> Dict[str, Any]:
    """Função principal: valida → roteia+ancora → dict."""
    return rotear_e_ancorar(work, line, anchor)


if __name__ == "__main__":
    import json

    line = "  return 'world';"
    good = "sha:" + hashlib.sha256(line.encode()).hexdigest()[:6]
    r1 = ignicao("fix typo", line, good)
    assert r1["category_pick"] == "quick" and r1["anchored_edit"]["accepted"] is True, r1
    r2 = ignicao("redesign dashboard", line, "sha:deadbe")
    assert r2["anchored_edit"]["accepted"] is False, r2
    try:
        ignicao("   ", "", "")
        raise SystemExit("FAIL: work vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
