"""Router VRAM/bandwidth-aware com escada de contexto (T4.4).

MODEL_SCORE (SPEC F2 §2.1): 0.30 cap + 0.25 task + 0.15 ctx + 0.15 res +
0.10 hist + 0.05 verif − 0.10 cost − 0.05 risk.

Recursos escassos (diretriz 2026-08-23): VRAM + bandwidth + latência +
KV + throughput do agente. Escada de ctx 64K→96K→128K→192K — nada acima
sem override. LLM fora da GPU é COLD/WARM, carregado sob demanda.

VRAM por ctx usa CURVAS POR ÂNCORAS MEDIDAS (GMB-1/produção): o KV
quantizado + lazy-alloc crescem SUBLINEAR — extrapolação linear já se
mostrou incoerente (previa ornith@131K≈23GiB; real medido 13.69GiB).
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple

PHYSICAL_VRAM_GIB = 16.0
SYSTEM_RESERVE_GIB = 2.0
REFERENCE_CTX = 32768

# janela consumida antes da task (regras+scaffold); task informa em system_prompt_tokens
DEFAULT_SYSTEM_PROMPT_TOKENS_NOTE = "measured 2026-08-23: ~86k para sessoes com monolito"

CTX_TIERS: List[int] = [65536, 98304, 131072, 196608]

WEIGHTS = {"cap": 0.30, "task": 0.25, "ctx": 0.15, "res": 0.15, "hist": 0.10, "verif": 0.05}
PENALTIES = {"cost": 0.10, "risk": 0.05}

RESIDENCY_FACTOR = {"HOT": 1.0, "WARM": 0.9, "COLD": 0.75}

ROLE_TO_CAP = {
    "orchestrator": "tool_use",
    "planner": "planning",
    "coder": "coding",
    "critic": "analysis",
    "reviewer": "analysis",
    "judge": "reasoning",
}

# curva (ctx, GiB) por fragmento de id — ORDEM IMPORTA (mais específico primeiro);
# ponto único = comportamento plano conservador; sincronizada com profiler.py
_MEASURED_VRAM_CURVES: Dict[str, List[Tuple[int, float]]] = {
    "ornith": [(32768, 14.2), (131072, 13.69)],
    "iq2-xxs": [(32768, 15.7)],
    "-9b-q4": [(32768, 14.9)],
}


def ctx_tier(needed_ctx_tokens: int) -> Optional[int]:
    """Menor tier da escada que comporta a necessidade; None se estourar 192K."""
    for tier in CTX_TIERS:
        if needed_ctx_tokens <= tier:
            return tier
    return None


def _norm(text: str) -> str:
    return (text or "").lower().replace(".", "-").replace("_", "-")


def _curve_for(entry: Dict) -> Optional[List[Tuple[int, float]]]:
    stem = Path(entry.get("path", "")).stem
    norm = _norm(stem)
    for frag, pts in _MEASURED_VRAM_CURVES.items():
        if frag in norm:
            return pts
    return None


def vram_at_ctx_gib(entry: Dict, target_ctx: int) -> Optional[float]:
    """VRAM estimada no ctx alvo: interpolação na curva medida; fallback linear
    a partir da âncora de referência do registry."""
    target = max(int(target_ctx), 1)
    pts = _curve_for(entry)
    if pts:
        if target <= pts[0][0]:
            return pts[0][1]
        for (c0, v0), (c1, v1) in zip(pts, pts[1:]):
            if target <= c1:
                ratio = (target - c0) / (c1 - c0)
                return round(v0 + (v1 - v0) * ratio, 2)
        c_last, v_last = pts[-1]
        if len(pts) >= 2:
            slope_sublinear = ((v_last - pts[-2][1]) / max(c_last - pts[-2][0], 1)) * 0.5
            return round(v_last + slope_sublinear * (target - c_last), 2)
        return v_last
    vram32 = float(entry.get("resources", {}).get("estimated_vram_gib") or 0)
    if vram32 <= 0:
        return None
    weights = float(entry["file"]["size_bytes"]) / 2**30 * 1.05
    kv32 = max(0.0, vram32 - weights)
    return round(weights + kv32 * (target / REFERENCE_CTX), 2)


def safe_load(
    entry: Dict,
    target_ctx: int,
    used_gib: float = 0.0,
    physical_gib: float = PHYSICAL_VRAM_GIB,
    reserve_gib: float = SYSTEM_RESERVE_GIB,
) -> Tuple[bool, Dict]:
    """SAFE_LOAD: necessidade ≤ teto efetivo.

    Curva MEDIDA já embute overhead do sistema no total (rocm-smi) ⇒ compara
    contra física − uso externo, sem subtrair reserva em duplicidade. Apenas
    o fallback de ESTIMATIVA linear aplica a reserva conservadora.
    """
    need = vram_at_ctx_gib(entry, target_ctx)
    if _curve_for(entry):
        available = round(physical_gib - used_gib, 2)
        basis = "measured_curve"
    else:
        available = round(physical_gib - used_gib - reserve_gib, 2)
        basis = "linear_estimate"
    detail = {"need_gib": need, "available_gib": available, "basis": basis}
    return (need is not None and need <= available), detail


def _residency_of(entry: Dict) -> str:
    value = (entry.get("runtime") or {}).get("residency", "COLD")
    return value if value in RESIDENCY_FACTOR else "COLD"


def score_components(entry: Dict, task: Dict) -> Tuple[float, Dict]:
    """Decomposição completa do MODEL_SCORE; todos os termos em [0,1]."""
    role = task.get("role", "")
    caps = entry.get("capabilities", {}).get("estimated", {})
    cap_fit = float(caps.get(ROLE_TO_CAP.get(role, "analysis"), 0.0))
    task_fit = float(entry.get("roles_suitability", {}).get(role, 0.0))

    needed = int(task.get("needed_ctx_tokens", 4096)) + int(task.get("system_prompt_tokens", 0))
    native = int(entry.get("architecture", {}).get("context_length", 0)) or REFERENCE_CTX
    ctx_fit = 1.0 if native >= needed else max(0.0, 1.0 - (needed - native) / max(needed, 1))

    health = entry.get("health", {}).get("status", "GREEN")
    residency = _residency_of(entry)
    base_res = {"GREEN": 1.0, "YELLOW": 0.5}.get(health, 0.0)
    res_fit = round(base_res * RESIDENCY_FACTOR[residency], 3)

    history = entry.get("performance_history") or {}
    hist_raw = history.get("success_rate")
    hist = 0.5 if hist_raw is None else float(hist_raw)
    verif_raw = history.get("verification_pass_rate")
    verif = 0.5 if verif_raw is None else float(verif_raw)

    vram32 = float(entry.get("resources", {}).get("estimated_vram_gib") or PHYSICAL_VRAM_GIB)
    tier = ctx_tier(needed)
    allocated = tier if tier else CTX_TIERS[-1]
    cost = min(
        1.0,
        0.5 * min(1.0, vram32 / PHYSICAL_VRAM_GIB)
        + 0.3 * min(1.0, needed / CTX_TIERS[-1])
        + 0.2 * max(0.0, 1.0 - needed / allocated),
    )
    risk = 1.0 if health == "YELLOW" else 0.0

    raw = (
        WEIGHTS["cap"] * cap_fit
        + WEIGHTS["task"] * task_fit
        + WEIGHTS["ctx"] * ctx_fit
        + WEIGHTS["res"] * res_fit
        + WEIGHTS["hist"] * hist
        + WEIGHTS["verif"] * verif
        - PENALTIES["cost"] * cost
        - PENALTIES["risk"] * risk
    )
    components = {
        "cap_fit": round(cap_fit, 3),
        "task_fit": round(task_fit, 3),
        "ctx_fit": round(ctx_fit, 3),
        "res_fit": res_fit,
        "hist": round(hist, 3),
        "verif": round(verif, 3),
        "cost": round(cost, 3),
        "risk": risk,
        "residency": residency,
    }
    return round(max(0.0, min(1.0, raw)), 4), components


def level_of(score: float) -> str:
    """Escada de fallback (SPEC F2): PRIMARY≥0.8 · SECONDARY≥0.65 · TERTIARY≥0.5."""
    if score >= 0.80:
        return "PRIMARY"
    if score >= 0.65:
        return "SECONDARY"
    if score >= 0.50:
        return "TERTIARY"
    return "DEGRADED"


def route(
    models: Dict[str, Dict],
    task: Dict,
    gpu_used_gib: float = 0.0,
    physical_gib: float = PHYSICAL_VRAM_GIB,
    reserve_gib: float = SYSTEM_RESERVE_GIB,
) -> List[Dict]:
    """Ranka modelos aptos para a task. Task acima de 192K ⇒ UNSCHEDULABLE ([])."""
    needed = int(task.get("needed_ctx_tokens", 4096)) + int(task.get("system_prompt_tokens", 0))
    if ctx_tier(needed) is None:
        return []
    ranked: List[Dict] = []
    for model_id, entry in models.items():
        status = entry.get("status", {})
        if status.get("excluded"):
            continue
        ok, detail = safe_load(entry, needed, gpu_used_gib, physical_gib, reserve_gib)
        if not ok:
            continue
        score, components = score_components(entry, task)
        ranked.append(
            {"model_id": model_id, "score": score, "level": level_of(score),
             "vram_detail": detail, **components}
        )
    ranked.sort(key=lambda item: (-item["score"], item["model_id"]))
    return ranked


def pick(
    models: Dict[str, Dict],
    task: Dict,
    gpu_used_gib: float = 0.0,
    physical_gib: float = PHYSICAL_VRAM_GIB,
    reserve_gib: float = SYSTEM_RESERVE_GIB,
) -> Optional[Dict]:
    ranked = route(models, task, gpu_used_gib, physical_gib, reserve_gib)
    return ranked[0] if ranked else None
