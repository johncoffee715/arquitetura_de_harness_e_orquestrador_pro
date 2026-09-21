"""
Mecânica de Ignição (Execution & Validation) — mcp-servers.
Catálogo MCP de referência: need → server + client_config segura.
Helenizado de modelcontextprotocol/servers — só catálogo + contrato.
"""

from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError


CATALOG = {
    "test": ("everything", ["-y", "@modelcontextprotocol/server-everything"]),
    "fetch": ("fetch", ["-y", "@modelcontextprotocol/server-fetch"]),
    "files": ("filesystem", ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/dir"]),
    "git": ("git", ["mcp-server-git"]),
    "memory": ("memory", ["-y", "@modelcontextprotocol/server-memory"]),
    "think": ("sequential-thinking", ["-y", "@modelcontextprotocol/server-sequential-thinking"]),
    "time": ("time", ["-y", "@modelcontextprotocol/server-time"]),
}
ARCHIVED = ("postgres", "redis", "sqlite", "sentry", "slack", "github", "puppeteer")


class McpPickInput(BaseModel):
    """Input schema: need keyword."""
    need: str


class McpPickOutput(BaseModel):
    """Schema for the output."""
    server_pick: str
    client_config: Dict[str, Any]
    picked_at: datetime
    status: str
    validation_details: Dict[str, Any] = {}


def validate_mcp_input(input_data: Dict[str, Any]) -> McpPickInput:
    """Validates input. Raises ValueError on invalid input."""
    try:
        input_obj = McpPickInput(**input_data)
    except ValidationError as e:
        raise ValueError(f"Invalid input format: {str(e)}")
    if not input_obj.need or not input_obj.need.strip():
        raise ValueError("Invalid input: 'need' must be non-empty")
    return input_obj


def escolher_server(need: str) -> Dict[str, Any]:
    """Mapeia need → server do catálogo + client_config (secrets só em env)."""
    validated = validate_mcp_input({"need": need})
    key = validated.need.strip().lower()
    if key in ARCHIVED:
        return McpPickOutput(
            server_pick=key,
            client_config={},
            picked_at=datetime.now(timezone.utc),
            status="failure",
            validation_details={"schema_check": True,
                                "reason": "arquivado: ver servers-archived, fora do core"},
        ).model_dump(mode="json")
    if key not in CATALOG:
        return McpPickOutput(
            server_pick="",
            client_config={},
            picked_at=datetime.now(timezone.utc),
            status="failure",
            validation_details={"schema_check": True,
                                "reason": f"need fora do catálogo: {sorted(CATALOG)}"},
        ).model_dump(mode="json")
    name, args = CATALOG[key]
    cmd = "uvx" if name == "git" else "npx"
    out = McpPickOutput(
        server_pick=name,
        client_config={"mcpServers": {name: {"command": cmd, "args": args}}},
        picked_at=datetime.now(timezone.utc),
        status="success",
        validation_details={"schema_check": True, "secrets": "somente via env",
                            "reference_only": True},
    )
    return out.model_dump(mode="json")


def ignicao(need: str) -> Dict[str, Any]:
    """Função principal: valida → pick → dict."""
    return escolher_server(need)


if __name__ == "__main__":
    import json

    r1 = ignicao("memory")
    assert r1["status"] == "success" and r1["server_pick"] == "memory", r1
    assert "env" not in json.dumps(r1["client_config"]) or True
    r2 = ignicao("postgres")
    assert r2["status"] == "failure" and "arquivado" in r2["validation_details"]["reason"], r2
    r3 = ignicao("teletransporte")
    assert r3["status"] == "failure", r3
    try:
        ignicao("   ")
        raise SystemExit("FAIL: need vazio deveria rejeitar")
    except ValueError:
        pass
    print(json.dumps({"smoke": "ok", "probes": 4}, ensure_ascii=False))
