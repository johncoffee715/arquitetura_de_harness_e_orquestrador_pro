"""Testes TDD do Router VRAM-aware (T4.4)."""
from __future__ import annotations

import pytest

from models.router import (
    level_of,
    pick,
    route,
    safe_load,
    score_components,
)


def mk(mid="m1", coding=0.85, planning=0.80, analysis=0.84, reasoning=0.82, tool=0.86,
       native=131072, size_gb=5.0, vram32=None, health="GREEN", excluded=False,
       success=None, verif=None):
    caps = {"reasoning": reasoning, "coding": coding, "planning": planning,
            "tool_use": tool, "analysis": analysis}
    roles = {"planner": planning, "coder": coding, "critic": analysis,
             "reviewer": analysis, "judge": reasoning, "orchestrator": tool}
    resources = {} if excluded else {
        "estimated_vram_gib": vram32 if vram32 is not None else round(size_gb * 1.05 + 1.6, 2)
    }
    entry = {
        "path": f"/x/{mid}.gguf",
        "file": {"size_bytes": int(size_gb * 2**30)},
        "capabilities": {"estimated": caps, "measured": None, "confidence": 0.0},
        "roles_suitability": roles,
        "architecture": {"family": "qwen", "context_length": native},
        "resources": resources,
        "health": {"status": health},
        "status": {"available": not excluded, "excluded": excluded},
        "performance_history": {"success_rate": success, "verification_pass_rate": verif},
    }
    return mid, entry


def test_score_bounds_and_best_for_task():
    a_id, a = mk("a", coding=0.90)
    b_id, b = mk("b", coding=0.70)
    ranked = route({b_id: b, a_id: a}, {"role": "coder", "needed_ctx_tokens": 8192})
    assert [r["model_id"] for r in ranked] == ["a", "b"]
    assert all(0.0 <= r["score"] <= 1.0 for r in ranked)


def test_ctx_deficit_penalized_but_not_fatal():
    small_id, small = mk("small", native=8192)
    big_id, big = mk("big", native=131072)
    task = {"role": "planner", "needed_ctx_tokens": 32000}
    ranked = route({small_id: small, big_id: big}, task)
    scores = {r["model_id"]: r["score"] for r in ranked}
    assert scores["big"] > scores["small"]
    _, comps = score_components(small, task)
    assert 0.0 <= comps["ctx_fit"] < 1.0


def test_yellow_penalized_vs_green():
    g_id, g = mk("g", health="GREEN")
    y_id, y = mk("y", health="YELLOW")
    ranked = route({y_id: y, g_id: g}, {"role": "coder", "needed_ctx_tokens": 4096})
    scores = {r["model_id"]: r["score"] for r in ranked}
    assert scores["g"] > scores["y"]
    assert ranked[0]["model_id"] == "g"


def test_safe_load_extrapolates_from_anchor():
    _, fat = mk("fat", size_gb=5.0, vram32=14.9)
    ok_small, d_small = safe_load(fat, 4096)
    ok_big, d_big = safe_load(fat, 131072)
    assert ok_small and d_small["need_gib"] <= 14.0
    assert not ok_big and d_big["need_gib"] > 14.0


def test_unsafe_model_dropped_from_route():
    _, fat = mk("fat", size_gb=5.0, vram32=14.9)
    assert route({"fat": fat}, {"role": "coder", "needed_ctx_tokens": 131072}) == []
    ok_rank = route({"fat": fat}, {"role": "coder", "needed_ctx_tokens": 4096})
    assert len(ok_rank) == 1


def test_excluded_skipped_and_history_neutral_defaults():
    x_id, x = mk("x", excluded=True)
    n_id, n = mk("n")
    ranked = route({x_id: x, n_id: n}, {"role": "judge", "needed_ctx_tokens": 2048})
    assert [r["model_id"] for r in ranked] == ["n"]
    _, comps = score_components(n, {"role": "judge"})
    assert comps["hist"] == 0.5 and comps["verif"] == 0.5


def test_history_boosts_over_identical_peer():
    h_id, h = mk("h", success=0.95, verif=0.95)
    p_id, p = mk("p")
    ranked = route({p_id: p, h_id: h}, {"role": "coder", "needed_ctx_tokens": 4096})
    assert ranked[0]["model_id"] == "h"


def test_level_thresholds_and_pick_fallbacks():
    assert level_of(0.81) == "PRIMARY"
    assert level_of(0.70) == "SECONDARY"
    assert level_of(0.55) == "TERTIARY"
    assert level_of(0.30) == "DEGRADED"
    strong_id, strong = mk("strong", coding=0.95, tool=0.95, planning=0.90)
    chosen = pick({"strong": strong}, {"role": "coder", "needed_ctx_tokens": 4096})
    assert chosen is not None and chosen["model_id"] == "strong"
    assert chosen["level"] in ("PRIMARY", "SECONDARY")


def test_pick_returns_none_when_nothing_fits():
    _, huge = mk("huge", size_gb=5.0, vram32=14.9)
    assert pick({"huge": huge}, {"role": "coder", "needed_ctx_tokens": 262144}) is None


def test_ctx_tiers_ladder_progressive():
    from models.router import ctx_tier
    assert ctx_tier(1000) == 65536
    assert ctx_tier(65536) == 65536
    assert ctx_tier(70000) == 98304
    assert ctx_tier(100000) == 131072
    assert ctx_tier(150000) == 196608
    assert ctx_tier(200000) is None  # acima da escada: UNSCHEDULABLE


def test_oversize_task_is_unschedulable_without_override():
    _, m = mk("m")
    task = {"role": "coder", "needed_ctx_tokens": 200000}
    assert route({"m": m}, task) == []
    assert pick({"m": m}, {"role": "coder", "needed_ctx_tokens": 262144}) is None


def test_warm_beats_cold_at_equal_merit():
    w_id, warm = mk("w")
    c_id, cold = mk("c")
    warm["runtime"] = {"residency": "WARM"}
    ranked = route({c_id: cold, w_id: warm}, {"role": "coder", "needed_ctx_tokens": 4096})
    assert ranked[0]["model_id"] == "w"
    assert ranked[0]["residency"] == "WARM"


def test_hot_residency_maximizes_resource_term():
    h_id, hot = mk("h")
    hot["runtime"] = {"residency": "HOT"}
    _, comps_hot = score_components(hot, {"role": "coder"})
    _, comps_default = score_components(mk("d")[1], {"role": "coder"})
    assert comps_hot["res_fit"] > comps_default["res_fit"]
    assert comps_default["residency"] == "COLD"


def test_ornith_dual_anchor_interpolates_like_reality():
    # âncoras reais GMB-1/produção: 14.2@32K · 13.69@131K — KV quantizado é sublinear
    _, ornith = mk("ornith", vram32=14.2)
    ornith["path"] = "/mnt/dados/Assistente Pessoal/modelos LLM/Ornith-1.5-9B-Q4_K_M.gguf"
    ok64, d64 = safe_load(ornith, 65536)
    ok128, d128 = safe_load(ornith, 131072)
    assert ok64 and ok128
    assert 13.5 <= d64["need_gib"] <= 14.2
    assert abs(d128["need_gib"] - 13.69) < 0.01


def test_system_prompt_overhead_shrinks_effective_window():
    _, m = mk("m", native=131072)
    base = {"role": "coder", "needed_ctx_tokens": 100000}
    heavy = {"role": "coder", "needed_ctx_tokens": 100000, "system_prompt_tokens": 86000}
    s_base, _ = score_components(m, base)
    s_heavy, c_heavy = score_components(m, heavy)
    assert s_heavy < s_base and c_heavy["ctx_fit"] < 1.0
    assert route({"m": m}, {"role": "coder", "needed_ctx_tokens": 111000}) != []
    over_ladder = {"role": "coder", "needed_ctx_tokens": 111000, "system_prompt_tokens": 86000}
    assert route({"m": m}, over_ladder) == []  # 197k efetivo estoura a escada
