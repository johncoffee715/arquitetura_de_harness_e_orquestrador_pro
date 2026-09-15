"""Testes TDD do Grafo Cognitivo Condicional (T4.5)."""
from __future__ import annotations

import pytest

from core.graph_engine import (
    CIRCUIT_OPEN,
    ROUTES,
    GraphEngine,
    classify_route,
    gates_for,
)


@pytest.mark.parametrize("cx,risk,amb,expected", [
    ("low", "low", "low", "FAST"),
    ("high", "low", "low", "FULL"),
    ("low", "high", "low", "FULL"),
    ("low", "low", "high", "FULL"),
    ("medium", "low", "low", "STANDARD"),
    ("low", "medium", "medium", "STANDARD"),
    ("medium", "high", "medium", "FULL"),
])
def test_classify_matrix(cx, risk, amb, expected):
    assert classify_route(cx, risk, amb) == expected


def test_fast_skips_contract_phases():
    assert ROUTES["FAST"] == ["F0", "F4", "F6"]
    assert set(ROUTES["FAST"]).isdisjoint({"F1", "F2", "F3", "F5"})


def test_full_has_brainstorm_and_refutation_layers():
    full = ROUTES["FULL"]
    assert len(full) > len(ROUTES["STANDARD"])
    assert any("BRAINSTORM" in n for n in full)
    assert any("REFUTATION" in n for n in full)
    assert full[-1].startswith("F6")


def test_unknown_route_raises():
    with pytest.raises(ValueError):
        GraphEngine("ULTRA")


def test_gate_blocks_entry_until_categorico():
    eng = GraphEngine("STANDARD")
    for _ in range(2):
        node, missing = eng.try_next()
        assert not missing
        eng.complete_node()
    node, missing = eng.try_next()
    assert node == "F2" and missing == ["G1"]
    assert eng.complete_node() is False
    with pytest.raises(ValueError):
        eng.approve_gate("G1", "passou burocrático")
    eng.approve_gate("G1", "PASSOU_CATEGORICO")
    assert eng.pending_gates() == []
    assert eng.complete_node() is True


def test_full_pipeline_walk_with_all_gates():
    eng = GraphEngine("STANDARD")
    gates_seq = {"G1", "G2", "G3", "G4"}
    walked = []
    guard = 0
    while not eng.completed and guard < 50:
        guard += 1
        node, missing = eng.try_next()
        for g in missing:
            eng.approve_gate(g)
        walked.append(node)
        eng.complete_node()
    assert eng.completed
    assert set(walked) == set(ROUTES["STANDARD"])
    assert gates_seq <= set(eng.approved)


def test_circuit_breaker_opens_after_three_failures():
    eng = GraphEngine("FAST", max_retries_per_node=3)
    eng.approve_gate("G3")
    node, _ = eng.try_next()
    assert node == "F0"
    eng.complete_node()
    opened_flags = [eng.report_failure("F4") for _ in range(3)]
    assert opened_flags == [False, False, True]
    node, _ = eng.try_next()
    assert node == CIRCUIT_OPEN
    snap = eng.snapshot()
    assert snap["open"] is True and snap["node"] == "F4"


def test_gates_for_fast_uses_sha_semantics():
    assert gates_for("FAST", "F0") == []
    assert gates_for("FAST", "F4") == ["G3"]
    assert gates_for("FAST", "F6") == ["G4"]
    assert gates_for("STANDARD", "F2") == ["G1"]
