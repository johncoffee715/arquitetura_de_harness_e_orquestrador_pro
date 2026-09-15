"""Roteador evento→endpoint por categoria — Task 4.2 (ponte inotify→LLM).

Roteia um evento de mudança do vault para o endpoint correto por CATEGORIA
(R75: categoria > nome), SEM chamada real — devolve apenas um descritor
{endpoint, categoria, motivo}.

Endpoints (device-map validado 2026-09-13):
  - Needle  :9091 → validação/retrieval (binário nativo, /complete).
  - RWKV7   :9084 → filtro/síntese (talamus-cortex, GPU Vulkan).
  - Qwen    :8083 → orquestração (35B, híbrido GPU/CPU).

Regras de categoria (por prefixo de path):
  - `regras/`   → síntese (RWKV7 :9084)
  - `pipeline/` → orquestração (Qwen :8083)
  - `spec/`     → orquestração (Qwen :8083)
  - default     → retrieval (Needle :9091)

Sem dependências externas. Sem chamadas a sockets/HTTP.
"""

from __future__ import annotations

from typing import Dict

from watcher import VaultEvent


# Endpoints canônicos (device-map.md)
ENDPOINTS = {
    "retrieval": "http://127.0.0.1:9091",   # Needle
    "sintese": "http://127.0.0.1:9084",     # RWKV7
    "orquestracao": "http://127.0.0.1:8083",  # Qwen
}


def _categoria(path: str) -> str:
    """Classifica um path em categoria (R75: categoria > nome)."""
    p = path.replace("\\", "/")
    if "/regras/" in p or p.startswith("regras/"):
        return "sintese"
    if "/pipeline/" in p or p.startswith("pipeline/"):
        return "orquestracao"
    if "/spec/" in p or p.startswith("spec/"):
        return "orquestracao"
    return "retrieval"


class Router:
    """Roteia eventos do vault para endpoints por categoria (sem chamada real)."""

    def route(self, path: str) -> Dict[str, str]:
        """Devolve descritor {endpoint, categoria, motivo} para `path`."""
        categoria = _categoria(path)
        return {
            "endpoint": ENDPOINTS[categoria],
            "categoria": categoria,
            "motivo": f"path '{path}' classificado como {categoria}",
        }


def route_event(event: VaultEvent) -> Dict[str, str]:
    """Roteia um VaultEvent do watcher (integração watcher→router)."""
    return Router().route(event.path)