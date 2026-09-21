"""
Mecânica de Ignição (Execution & Validation) — dashi-ppt-skill.
Spec de deck temático: páginas como (layout + copy fields + console), export HTML/PDF/PPTX.
Helenizado de chuspeeism/dashi-ppt-skill — só o padrão; engine proprietária nunca copiada.
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


VALID_EXPORTS = ("html", "pdf", "pptx")
VALID_ROLES = (
    "cover", "toc", "metrics", "trend", "compare", "flow",
    "risk", "chart", "cards", "closing",
)


class DeckPage(BaseModel):
    """Uma página: layout + campos de copy + console de edição."""
    layout: str
    role: str
    copy_fields: Dict[str, str]
    console: Dict[str, Any] = {}


class DeckSpecInput(BaseModel):
    """Input schema for the dashi-ppt-skill."""
    theme: str
    pages: List[DeckPage]
    export: str = "html"


class DeckSpecOutput(BaseModel):
    """Schema for the output of the dashi-ppt-skill."""
    theme: str
    pages: List[DeckPage]
    export: str
    validated_at: datetime
    status: str  # "success" or "failure"
    validation_details: Dict[str, Any] = {}


def validate_deck_input(input_data: Dict[str, Any]) -> DeckSpecInput:
    """Validates deck spec. Raises ValueError on invalid input."""
    try:
        input_obj = DeckSpecInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.theme or not input_obj.theme.strip():
        raise ValueError("Invalid input: 'theme' must be non-empty")
    if not input_obj.pages:
        raise ValueError("Invalid input: 'pages' must have ≥1 page")
    if input_obj.export not in VALID_EXPORTS:
        raise ValueError(f"Invalid export: must be one of {VALID_EXPORTS}")
    for p in input_obj.pages:
        if not p.layout or not p.copy_fields:
            raise ValueError("Invalid page: 'layout' + 'copy_fields' required")
    return input_obj


def montar_spec(brief: str, theme: str, pages: List[Dict[str, Any]], export: str = "html") -> DeckSpecOutput:
    """Monta e valida o spec do deck (determinístico, offline)."""
    validated = validate_deck_input({"theme": theme, "pages": pages, "export": export})
    details = {
        "schema_check": True,
        "page_count": len(validated.pages),
        "brief_chars": len(brief),
        "roles": sorted({p.role for p in validated.pages}),
        "local_only": True,
    }
    return DeckSpecOutput(
        theme=validated.theme,
        pages=validated.pages,
        export=validated.export,
        validated_at=datetime.now(timezone.utc),
        status="success",
        validation_details=details,
    )


def validar_export(spec: DeckSpecOutput) -> Dict[str, Any]:
    """Gate de export: PPTX/PDF exigem Chrome local (contrato, não execução)."""
    needs_chrome = spec.export in ("pdf", "pptx")
    out = spec.model_dump(mode="json")
    out["validation_details"]["needs_local_chrome"] = needs_chrome
    return out


def ignicao(brief: str, theme: str, pages: List[Dict[str, Any]], export: str = "html") -> Dict[str, Any]:
    """Função principal: valida → monta spec → gate de export → dict."""
    return validar_export(montar_spec(brief, theme, pages, export))


if __name__ == "__main__":
    import json

    pages = [
        {"layout": "cover-hero", "role": "cover", "copy_fields": {"title": "Q3 Review"},
         "console": {"palette": "dark-gold", "animations": True}},
        {"layout": "metrics-grid", "role": "metrics", "copy_fields": {"kpi1": "+18%"},
         "console": {"modules": 4}},
    ]
    r1 = ignicao("Q3 business review, 2 pages", "theme08", pages, "html")
    assert r1["status"] == "success" and len(r1["pages"]) == 2, r1
    assert r1["validation_details"]["needs_local_chrome"] is False, r1
    r2 = ignicao("Board deck", "theme09", pages, "pptx")
    assert r2["validation_details"]["needs_local_chrome"] is True, r2
    try:
        ignicao("x", "", [], "html")
        raise SystemExit("FAIL: spec vazio deveria rejeitar")
    except ValueError:
        pass
    try:
        ignicao("x", "theme01", pages, "keynote")
        raise SystemExit("FAIL: export inválido deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 4}, ensure_ascii=False))
