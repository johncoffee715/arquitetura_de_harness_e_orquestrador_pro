"""Discovery Engine — varre o MODEL_LIBRARY e gera o registry normalizado (T4.1/T4.2).

Critérios SPEC F2 §42 cobertos: [1] detecta todos *.gguf <30s · [2] registry
normalizado · exclusões documentadas COM evidência, sem remover arquivos.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, Iterable, Optional, Union

from .metadata import read_gguf_metadata
from .profiler import (
    detect_family,
    detect_quant_tag,
    estimate_capabilities,
    estimate_vram_gib,
    params_billion,
)

MODELS_DIR = Path("/mnt/dados/Assistente Pessoal/modelos LLM")

# ctx de referência para estimativas comparáveis entre modelos (âncora
# empírica GMB-1 @32768); o router extrapola para o ctx alvo (T4.4)
REFERENCE_CTX = 32768

# papel do grafo -> capacidade que o pontua (SPEC F2/F3)
ROLES_FROM_CAPS = {
    "orchestrator": "tool_use",
    "planner": "planning",
    "coder": "coding",
    "critic": "analysis",
    "reviewer": "analysis",
    "judge": "reasoning",
}


def _model_id(path: Path) -> str:
    """Id estável: stem em lowercase com '.' e '_' virando '-'."""
    return path.stem.lower().replace(".", "-").replace("_", "-")


def _base_entry(path: Path) -> Dict:
    """Esqueleto conforme schema da SPEC F2 §2."""
    return {
        "path": str(path),
        "file": {"size_bytes": path.stat().st_size},
        "architecture": {},
        "backend": {"format": "gguf", "compatible": ["llama.cpp"]},
        "capabilities": {"estimated": {}, "measured": None, "confidence": 0.0},
        "roles_suitability": {},
        "performance_history": {
            "total_tasks": 0,
            "success_rate": None,
            "avg_latency_ms": None,
            "verification_pass_rate": None,
        },
        "health": {"status": "GREEN", "last_check": None, "consecutive_failures": 0, "oom_events": 0},
        "status": {"available": True, "excluded": False, "exclusion_reason": None},
    }


def _exclude(entry: Dict, reason: str) -> None:
    entry["status"] = {"available": False, "excluded": True, "exclusion_reason": reason}


def scan_models_dir(
    directory: Union[str, Path] = MODELS_DIR,
    vram_available_gib: float = 14.0,
    vram_physical_gib: float = 16.0,
    blacklist: Iterable[str] = frozenset(),
    vram_estimator: Optional[Callable[[Dict, str, int], float]] = None,
) -> Dict:
    """Varre *.gguf e monta o registry.

    Regras de exclusão (SPEC F2): metadata ilegível · vram_estimada >
    disponível física · blacklist por fragmento do id. O arquivo NUNCA é
    removido; modelos entre 90% e 100% do teto ficam YELLOW (carregam, mas o
    router deve preferir fallback).
    """
    est = vram_estimator or estimate_vram_gib
    black = {str(b).lower() for b in blacklist}
    root = Path(directory)
    models: Dict[str, Dict] = {}
    files = sorted(root.glob("*.gguf")) if root.is_dir() else []
    for p in files:
        gid = _model_id(p)
        entry = _base_entry(p)
        models[gid] = entry
        try:
            meta = read_gguf_metadata(p)
        except Exception as exc:  # arquivo truncado/corrompido — evidencia e segue
            _exclude(entry, f"metadata_unreadable: {exc}")
            continue
        quant = detect_quant_tag(p.name)
        native_ctx = next((int(v) for k, v in meta.items() if k.endswith(".context_length")), 32768)
        caps = estimate_capabilities(meta, p.name)
        params_b = params_billion(meta, meta["file_size_bytes"] / 2**30, quant)
        vram = round(float(est(meta, gid, REFERENCE_CTX)), 2)
        entry["architecture"] = {
            "family": detect_family(
                str(meta.get("general.name") or ""),
                meta.get("general.architecture"),
                filename=p.name,
            ),
            "quantization": quant,
            "context_length": native_ctx,
            "parameters_b": params_b,
        }
        entry["capabilities"]["estimated"] = caps
        entry["roles_suitability"] = {r: caps[c] for r, c in ROLES_FROM_CAPS.items() if c in caps}
        soft_ceiling = round(vram_available_gib * 0.9, 2)
        hard_ceiling = round(vram_physical_gib, 2)
        matched_black = next((b for b in sorted(black, key=len, reverse=True) if b in gid), None)
        if matched_black:
            _exclude(entry, "user_blacklist")
        elif vram > hard_ceiling:
            _exclude(entry, f"vram_insufficient: {vram}GiB estimado > físico {hard_ceiling}GiB")
        else:
            entry["resources"] = {"estimated_vram_gib": vram}
            if vram > soft_ceiling:
                entry["health"]["status"] = "YELLOW"
                entry["resources"]["vram_warning"] = True
                entry["resources"]["note"] = (
                    f"{vram}GiB > soft {soft_ceiling}GiB — router deve priorizar fallback"
                )
    available = [m for m in models.values() if m["status"]["available"]]
    return {
        "registry_version": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_dir": str(root),
        "reference_ctx": REFERENCE_CTX,
        "vram_physical_gib": vram_physical_gib,
        "vram_available_gib": vram_available_gib,
        "vram_soft_ceiling_gib": round(vram_available_gib * 0.9, 2),
        "total_models": len(models),
        "available_models": len(available),
        "excluded_models": len(models) - len(available),
        "models": models,
    }


def write_registry(registry: Dict, out_path: Union[str, Path]) -> Path:
    """Serializa o registry em JSON (utf-8, ascii-safe off). Retorna o caminho."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    return out
