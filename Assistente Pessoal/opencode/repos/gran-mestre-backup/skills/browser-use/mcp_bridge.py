"""mcp_bridge.py — Bridge entre browser-use skill e Playwright MCP.

Adaptado da arquitetura Agent+Controller do browser-use/browser-use (MIT).
Aplicação de antropofagia: absorvemos o padrão de agente assíncrono
e adaptamos para o modelo de hooks do OpenCode.
"""

import json
import os
import time
import subprocess
from typing import Optional


class BrowserSession:
    """Sessão de navegador gerenciada via Playwright MCP.

    Abstrai a comunicação com o servidor MCP Playwright,
    permitindo que a skill browser-use controle o navegador.
    """

    def __init__(self, mcp_name: str = "playwright"):
        self.mcp_name = mcp_name
        self.session_id: Optional[str] = None
        self.screenshots_dir = "/tmp/browser-use/screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)

    def navigate(self, url: str) -> dict:
        """Navega para URL."""
        return self._mcp_call("browser_navigate", {"url": url})

    def click(self, selector: str) -> dict:
        """Clica em elemento."""
        return self._mcp_call("browser_click", {"selector": selector})

    def fill(self, selector: str, value: str) -> dict:
        """Preenche campo."""
        return self._mcp_call("browser_fill", {"selector": selector, "value": value})

    def screenshot(self, name: str = "page") -> str:
        """Tira screenshot e salva localmente."""
        result = self._mcp_call("browser_screenshot", {})
        path = os.path.join(self.screenshots_dir, f"{name}-{int(time.time())}.png")
        if result.get("data"):
            import base64
            with open(path, "wb") as f:
                f.write(base64.b64decode(result["data"]))
        return path

    def extract(self, selector: str) -> list[dict]:
        """Extrai dados estruturados de elementos."""
        result = self._mcp_call("browser_extract", {"selector": selector})
        return result.get("elements", [])

    def evaluate(self, script: str) -> dict:
        """Executa JavaScript na página."""
        return self._mcp_call("browser_evaluate", {"script": script})

    def _mcp_call(self, tool: str, args: dict) -> dict:
        """Chama ferramenta MCP Playwright via subprocess.

        NOTA: Em produção, usar MCP client SDK. Esta implementação
        é um bridge simplificado para integração imediata.
        """
        cmd = [
            "npx", "-y", "@playwright/mcp",
            "call", tool,
            "--args", json.dumps(args),
        ]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            return {"error": result.stderr}
        except subprocess.TimeoutExpired:
            return {"error": "Timeout na chamada MCP"}
        except Exception as e:
            return {"error": str(e)}

    def close(self) -> None:
        """Fecha sessão."""
        self._mcp_call("browser_close", {})
        self.session_id = None


# Singleton
_default_session: Optional[BrowserSession] = None


def get_browser() -> BrowserSession:
    """Retorna sessão de navegador (singleton)."""
    global _default_session
    if _default_session is None:
        _default_session = BrowserSession()
    return _default_session


def close_browser() -> None:
    """Fecha sessão de navegador."""
    global _default_session
    if _default_session:
        _default_session.close()
        _default_session = None
