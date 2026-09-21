"""TDD caminho de RECUPERACAO MC-externo em live_loop (snn-mc-retrieval).

Sem rede: patch live_loop._post_json.
"""

from __future__ import annotations

import json
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import live_loop
from live_loop import LiveLoop, read_history, history_block, HISTORY_MAX_CHARS
from parser import parse_csv_to_csr

SNN_DIR = os.path.dirname(os.path.abspath(__file__))
MINI = os.path.join(SNN_DIR, "mini_edges.csv")


def _mini_loop(**kw):
    row_ptr, col_idx, weight = parse_csv_to_csr(MINI)
    csr = type("C", (), {"row_ptr": row_ptr, "col_idx": col_idx,
                         "weight": weight, "n": len(row_ptr) - 1})()
    return LiveLoop(csr=csr, **kw)


def _fake_ok(url, payload, timeout):
    if "9084" in url:
        return 200, {"choices": [{"message": {"content": "ler"}}]}
    if "9091" in url:
        return 200, {"function_calls": []}
    if "9094" in url:
        return 200, {"data": [{"embedding": [0.1]}]}
    raise AssertionError(url)


def _write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(r + "\n")


def _ep(nota, decisao="ignorar", spikes=1):
    return json.dumps({"nota": nota, "decisao": decisao, "spikes": spikes})


def test_1_read_history_ultimos_n_compactos(tmp_path):
    p = str(tmp_path / "eps.jsonl")
    rows = [_ep(f"/a/n{i}.md", "ler" if i % 2 else "ignorar", i) for i in range(8)]
    _write_jsonl(p, rows)
    hist = read_history(p, limit=5)
    assert len(hist) == 5
    # cronologico: mais antigo primeiro -> n3..n7
    assert [h["nota"] for h in hist] == [f"n{i}.md" for i in range(3, 8)]
    assert hist[0] == {"nota": "n3.md", "decisao": "ler", "spikes": 3}
    assert set(hist[-1]) == {"nota", "decisao", "spikes"}


def test_2_read_history_fail_closed(tmp_path):
    assert read_history(str(tmp_path / "ausente.jsonl")) == []
    p = str(tmp_path / "ruim.jsonl")
    _write_jsonl(p, ['{"nota": "/x/a.md", "decisao": "ler", "spikes": 2}',
                     "LIXO NAO JSON", "[1,2]", "42"])
    hist = read_history(p)
    assert hist == [{"nota": "a.md", "decisao": "ler", "spikes": 2}]


def test_3_history_block_vazio_e_truncamento():
    assert history_block([]) == ""
    hist = [{"nota": f"n{i}.md", "decisao": "ler", "spikes": i} for i in range(50)]
    blk = history_block(hist)
    assert len(blk) <= HISTORY_MAX_CHARS
    assert "n49.md:ler:49" in blk  # mais recente sobrevive


def test_4_decide_inclui_checkpoint_no_prompt(tmp_path):
    loop = _mini_loop(state_path=str(tmp_path / "s.json"))
    hist = [{"nota": "antiga.md", "decisao": "agir", "spikes": 42},
            {"nota": "outra.md", "decisao": "ler", "spikes": 7}]
    act = {"total_spikes": 10, "topk": [(0, 1)], "regions": {"a": 1}}
    seen = {}
    def fake(url, payload, timeout):
        seen["prompt"] = payload["messages"][0]["content"]
        return 200, {"choices": [{"message": {"content": "ler"}}]}
    with patch("live_loop._post_json", side_effect=fake):
        loop.decide(str(tmp_path / "n.md"), act, history=hist)
    assert "antiga.md:agir:42" in seen["prompt"]
    assert "outra.md:ler:7" in seen["prompt"]


def test_5_decide_sem_history_sem_hist(tmp_path):
    loop = _mini_loop(state_path=str(tmp_path / "s.json"))
    act = {"total_spikes": 10, "topk": [(0, 1)], "regions": {"a": 1}}
    seen = {}
    def fake(url, payload, timeout):
        seen["prompt"] = payload["messages"][0]["content"]
        return 200, {"choices": [{"message": {"content": "ler"}}]}
    with patch("live_loop._post_json", side_effect=fake):
        loop.decide(str(tmp_path / "n.md"), act)
    assert "hist=" not in seen["prompt"]


def test_6_memory_hits_no_prompt_dentro_do_teto(tmp_path):
    loop = _mini_loop(state_path=str(tmp_path / "s.json"))
    act = {"total_spikes": 10, "topk": [(0, 1)], "regions": {"a": 1}}
    seen = {}
    def fake(url, payload, timeout):
        seen["prompt"] = payload["messages"][0]["content"]
        return 200, {"choices": [{"message": {"content": "ler"}}]}
    with patch("live_loop._post_json", side_effect=fake):
        loop.decide(str(tmp_path / "n.md"), act, history=[],
                    memory_hits=["fato-alpha", "fato-beta"])
    assert "mem=fato-alpha;fato-beta" in seen["prompt"]
    assert len("mem=fato-alpha;fato-beta") <= HISTORY_MAX_CHARS


def test_7_run_integra_history_n_e_checkpoint(tmp_path):
    eps = str(tmp_path / "eps.jsonl")
    _write_jsonl(eps, [_ep("/vault/antiga.md", "agir", 42)])
    st = str(tmp_path / "live_state.json")
    note = tmp_path / "n.md"
    note.write_text("# t\ncorpo")
    loop = _mini_loop(state_path=st, episodes_path=eps)
    seen = {}
    def fake(url, payload, timeout):
        if "9084" in url:
            seen["prompt"] = payload["messages"][0]["content"]
            return 200, {"choices": [{"message": {"content": "ignorar"}}]}
        raise AssertionError(url)
    with patch("live_loop._post_json", side_effect=fake):
        out = loop.run(str(note))
    assert out["history_n"] == 1
    assert "antiga.md:agir:42" in seen["prompt"]
    assert out["decision"] == "ignorar"
