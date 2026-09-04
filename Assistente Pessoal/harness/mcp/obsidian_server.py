#!/usr/bin/env python3
"""
Obsidian MCP Server — minimal MCP-over-stdio server for the cerebral vault.

Exposes three tools over JSON-RPC 2.0 (Content-Length framing, like LSP):
    list_notes — list markdown notes in the vault
    read_note  — read a note by name
    write_note — write a note (path-traversal safe)

Vault root comes from $OBSIDIAN_VAULT (default: /mnt/dados/Assistente Pessoal/cerebro com IA/).
Run: python3 harness/mcp/obsidian_server.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_VAULT = Path("/mnt/dados/Assistente Pessoal/cerebro com IA")

TOOLS: List[Dict[str, Any]] = [
    {"name": "list_notes", "description": "List markdown notes in the vault.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "read_note", "description": "Read a note by name (without .md).",
     "inputSchema": {"type": "object",
                     "properties": {"name": {"type": "string"}},
                     "required": ["name"]}},
    {"name": "write_note", "description": "Write a note (creates dirs if needed).",
     "inputSchema": {"type": "object",
                     "properties": {"name": {"type": "string"},
                                    "content": {"type": "string"}},
                     "required": ["name", "content"]}},
]


class VaultServer:
    """JSON-RPC handler over an Obsidian vault directory."""

    def __init__(self, vault: Path) -> None:
        self.vault = vault

    def _resolve(self, name: str) -> Path:
        """Resolve `name` inside the vault, refusing traversal escapes."""
        if not name or ".." in Path(name).parts:
            raise ValueError("nome inválido (traversal bloqueado)")
        return (self.vault / name).with_suffix(".md")

    def list_notes(self) -> List[str]:
        if not self.vault.is_dir():
            return []
        return sorted(p.name for p in self.vault.rglob("*.md"))

    def read_note(self, name: str) -> str:
        path = self._resolve(name)
        if not path.exists():
            raise FileNotFoundError(f"nota não encontrada: {name}")
        return path.read_text(encoding="utf-8")

    def write_note(self, name: str, content: str) -> Dict[str, str]:
        path = self._resolve(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return {"written": str(path)}

    def handle(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method", "")
        params = request.get("params") or {}
        result: Dict[str, Any] = {}
        error: Dict[str, Any] | None = None
        try:
            if method == "initialize":
                result = {"protocolVersion": "2025-03-26",
                          "capabilities": {"tools": {}},
                          "serverInfo": {"name": "obsidian",
                                         "version": "1.0.0"}}
            elif method == "tools/list":
                result = {"tools": TOOLS}
            elif method == "tools/call":
                tool = params.get("name", "")
                args = params.get("arguments") or {}
                if tool == "list_notes":
                    out: Any = self.list_notes()
                elif tool == "read_note":
                    out = self.read_note(args["name"])
                elif tool == "write_note":
                    out = self.write_note(args["name"], args["content"])
                else:
                    error = {"code": -32601,
                             "message": f"ferramenta desconhecida: {tool}"}
                    return {"jsonrpc": "2.0", "id": request.get("id"),
                            "error": error}
                result = {"content": [{"type": "text",
                                       "text": json.dumps(out, ensure_ascii=False)}]}
            elif method == "notifications/initialized":
                result = {}
            else:
                error = {"code": -32601, "message": f"método desconhecido: {method}"}
        except KeyError as exc:
            error = {"code": -32602, "message": f"argumento ausente: {exc}"}
        except (ValueError, FileNotFoundError) as exc:
            error = {"code": -32603, "message": str(exc)}
        response: Dict[str, Any] = {"jsonrpc": "2.0", "id": request.get("id")}
        if error is not None:
            response["error"] = error
        else:
            response["result"] = result
        return response


# ---- MCP stdio framing (Content-Length, LSP-style) ----------------------
def _read_message(stream) -> Dict[str, Any] | None:
    headers: Dict[str, str] = {}
    while True:
        line = stream.readline()
        if not line:
            return None
        line = line.decode("utf-8", errors="replace").strip()
        if line == "":
            break
        key, _, value = line.partition(":")
        headers[key.strip().lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    body = stream.read(length)
    return json.loads(body)


def _write_message(stream, message: Dict[str, Any]) -> None:
    payload = json.dumps(message).encode("utf-8")
    stream.write(f"Content-Length: {len(payload)}\r\n\r\n".encode("utf-8"))
    stream.write(payload)
    stream.flush()


def main() -> None:
    vault = Path(os.environ.get("OBSIDIAN_VAULT", DEFAULT_VAULT))
    server = VaultServer(vault)
    stream = sys.stdin.buffer
    out = sys.stdout.buffer
    while True:
        try:
            request = _read_message(stream)
            if request is None:
                break
            # JSON-RPC: notifications (sem id) não recebem resposta.
            if request.get("id") is None:
                continue
            response = server.handle(request)
            _write_message(out, response)
        except (json.JSONDecodeError, ValueError, KeyError):
            break


if __name__ == "__main__":
    main()