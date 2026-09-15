"""TDD Wave 4 retry: reinforce com eligibility trace (sem rede/LLM)."""

from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from live_loop import LiveLoop
from parser import parse_csv_to_csr

SNN_DIR = os.path.dirname(os.path.abspath(__file__))
MINI = os.path.join(SNN_DIR, "mini_edges.csv")


def _mini_loop(state_path=None, **kw):
    row_ptr, col_idx, weight = parse_csv_to_csr(MINI)
    csr = type("C", (), {"row_ptr": row_ptr, "col_idx": col_idx,
                         "weight": weight, "n": len(row_ptr) - 1})()
    if state_path is not None:
        return LiveLoop(csr=csr, state_path=str(state_path), **kw)
    return LiveLoop(csr=csr, **kw)


def test_reforco_sobe_desce_rota_ativa(tmp_path):
    loop = _mini_loop(state_path=str(tmp_path / "s.json"))
    loop.simulate("probe-a")
    assert loop._active_routes, "simulate deve marcar rotas ativas"
    up = loop.reinforce(+1)
    assert up, "reinforce imediato nao pode expirar"
    rota = sorted(up)[0]
    assert loop.efficacies[rota] > 1.0
    before = dict(loop.efficacies)
    down = loop.reinforce(-1)
    assert down
    assert loop.efficacies[rota] < before[rota]


def test_bounds_respeitados(tmp_path):
    loop = _mini_loop(state_path=str(tmp_path / "s.json"))
    loop.simulate("probe-b")
    for _ in range(30):
        loop.reinforce(+1)
    assert loop.efficacies
    assert all(v <= 2.0 for v in loop.efficacies.values())
    loop._last_active_ts = time.monotonic()
    for _ in range(40):
        loop.reinforce(-1)
    assert all(v >= 0.1 for v in loop.efficacies.values())


def test_persistencia_roundtrip(tmp_path):
    st = str(tmp_path / "s.json")
    loop = _mini_loop(state_path=st)
    loop.simulate("probe-c")
    loop.reinforce(+1)
    assert os.path.exists(st)
    body = json.loads(open(st, encoding="utf-8").read())
    assert "efficacies" in body and isinstance(body["efficacies"], dict)
    loop2 = _mini_loop(state_path=st)
    assert loop2.efficacies == loop.efficacies


def test_rotas_inativas_inalteradas(tmp_path):
    loop = _mini_loop(state_path=str(tmp_path / "s.json"))
    loop.simulate("probe-d")
    loop._active_routes = {"r0"}
    loop.efficacies = {"r0": 1.0, "r1": 1.0}
    out = loop.reinforce(+1)
    assert out
    assert loop.efficacies["r0"] > 1.0
    assert loop.efficacies["r1"] == 1.0
