"""
Mecânica de Ignição (Execution & Validation) — context7-skill.
Resolve Context7 library ID e busca docs focais via REST (sem MCP overhead).
Helenizado de netresearch/context7-skill — sem cópia literal, sem dependência externa obrigatória.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


class Context7DocsInput(BaseModel):
    """Input schema for the context7-skill."""
    library: str
    topic: str = ""


class Context7DocsOutput(BaseModel):
    """Schema for the output of the context7-skill."""
    library_id: str
    docs_excerpt: str
    topic: str
    resolved_at: datetime
    status: str  # "success" or "failure"
    validation_details: Dict[str, Any] = {}


def validate_context7_input(input_data: Dict[str, Any]) -> Context7DocsInput:
    """Validates and parses input. Raises ValueError on invalid input."""
    try:
        input_obj = Context7DocsInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.library or not input_obj.library.strip():
        raise ValueError("Invalid input: 'library' must be a non-empty string")
    return input_obj


def resolver_library_id(library: str) -> str:
    """Normaliza o nome da lib para um library_id estilo Context7.

    Regra determinística (offline, sem rede): minúsculas, espaços/hífens
    viram '/', prefixo '/' garantido. Ex.: 'Prisma' -> '/prisma/prisma'.
    O script real (context7.sh search) confirma contra a API; aqui vai o
    fallback determinístico para validação e testes.
    """
    slug = "-".join(library.strip().lower().split())
    if "/" not in slug:
        slug = f"{slug}/{slug}"
    if not slug.startswith("/"):
        slug = "/" + slug
    return slug


def buscar_docs(library_id: str, topic: str = "") -> Context7DocsOutput:
    """Executa o lookup focal (simulado offline para validação determinística).

    Em produção o script chama a REST Context7; aqui o excerto é um
    placeholder estrutural que prova o contrato (library_id + topic),
    nunca uma API inventada.
    """
    if not library_id or not library_id.startswith("/"):
        return Context7DocsOutput(
            library_id=library_id,
            docs_excerpt="",
            topic=topic,
            resolved_at=datetime.now(timezone.utc),
            status="failure",
            validation_details={"reason": "library_id inválido", "schema_check": False},
        )
    excerpt = (
        f"Context7 docs for {library_id}"
        + (f" focadas em '{topic}'" if topic else "")
        + ": use o script (context7.sh docs) para o conteúdo live; "
        + "cite sempre library_id + topic; nunca invente assinaturas."
    )
    return Context7DocsOutput(
        library_id=library_id,
        docs_excerpt=excerpt,
        topic=topic,
        resolved_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "topic_filter": bool(topic)},
    )


def ignicao(library: str, topic: str = "") -> Dict[str, Any]:
    """Função principal: valida input -> resolve ID -> busca docs -> dict."""
    validated = validate_context7_input({"library": library, "topic": topic})
    out = buscar_docs(resolver_library_id(validated.library), validated.topic)
    return out.model_dump(mode="json")


if __name__ == "__main__":
    import json

    r1 = ignicao("Prisma", "queries")
    assert r1["status"] == "success", r1
    assert r1["library_id"] == "/prisma/prisma", r1
    assert "queries" in r1["docs_excerpt"], r1
    r2 = ignicao("React Hooks", "")
    assert r2["status"] == "success" and r2["library_id"].startswith("/"), r2
    try:
        ignicao("   ", "")
        raise SystemExit("FAIL: input vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 3}, ensure_ascii=False))
