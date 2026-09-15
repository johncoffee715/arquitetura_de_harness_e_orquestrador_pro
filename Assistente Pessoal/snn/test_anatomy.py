"""TDD Wave 6: anatomia real + write-back reativo + anti-loop (B2).

Nao altera testes antigos: arquivo novo, fixtures proprias.
"""

from __future__ import annotations

import json
import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import anatomy
from daemon_vault import DaemonVault
from live_loop import LiveLoop
from parser import parse_csv_to_csr

SNN_DIR = os.path.dirname(os.path.abspath(__file__))
MINI = os.path.join(SNN_DIR, "mini_edges.csv")


def _mini_loop(**kw):
    row_ptr, col_idx, weight = parse_csv_to_csr(MINI)
    csr = type("C", (), {"row_ptr": row_ptr, "col_idx": col_idx,
                         "weight": weight, "n": len(row_ptr) - 1})()
    return LiveLoop(csr=csr, **kw)


# -- anatomia --

def test_region_of_ids_conhecidos():
    meta = anatomy.load_annotations()
    assert meta["loaded"] and meta["n_mapped"] > 100_000
    assert anatomy.region_of(10013) == "MB"    # MBON01
    assert anatomy.region_of(11862) == "MB"    # KCab-s
    assert anatomy.region_of(11327) == "MB"    # PPL101
    assert anatomy.region_of(10539) == "CX"    # EPG
    assert anatomy.region_of(999999999) == "outros"


def test_classify_prefixos_puro():
    assert anatomy.classify("KCab-s", "KCab-m", None) == "MB"
    assert anatomy.classify("MBON01", None, None) == "MB"
    assert anatomy.classify("PEN_a(PEN1)", None, None) == "CX"
    assert anatomy.classify("FB6A", None, None) == "CX"
    assert anatomy.classify("Tm3", None, "ol_intrinsic") == "OL"
    assert anatomy.classify("DNg08", None, None) == "VNC"
    assert anatomy.classify(None, None, None) == "outros"


def test_slice_real_tem_mais_de_3_regioes():
    loop = LiveLoop.from_feather(limit_rows=5000)
    act = loop.simulate("nota probe w6", steps=6)
    regs = {k for k, v in act["regions"].items()}
    assert len(regs) > 3, f"regioes distintas insuficientes: {act['regions']}"
    assert "outros" in regs or "MB" in regs or "CX" in regs
    assert "r0" not in regs and "r3" not in regs  # B2: sem i%4


# -- write-back --

def _fake_ler(url, payload, timeout):
    if "9084" in url:
        return 200, {"choices": [{"message": {"content": "ler"}}]}
    if "9091" in url:
        return 200, {"function_calls": []}
    if "9094" in url:
        return 200, {"data": [{"embedding": [0.1]}]}
    raise AssertionError(url)


def test_writeback_so_em_ler_agir_com_marcador(tmp_path):
    note = tmp_path / "n.md"
    note.write_text("# t\ncorpo suficiente p/ hash", encoding="utf-8")
    loop = _mini_loop(state_path=str(tmp_path / "s.json"))
    with patch("live_loop._post_json", side_effect=_fake_ler):
        out = loop.run(str(note))
    assert out["decision"] == "ler"
    body = note.read_text(encoding="utf-8")
    assert "<!-- snn-episode" in body
    assert "body_hash=" in body
    assert "## Cérebro (episódio" in body
    assert out["write_back"]["appended"] is True


def test_writeback_nao_em_ignorar(tmp_path):
    note = tmp_path / "n.md"
    antes = "# t\nnada a fazer"
    note.write_text(antes, encoding="utf-8")
    loop = _mini_loop(state_path=str(tmp_path / "s.json"))

    def fake(url, payload, timeout):
        if "9084" in url:
            return 200, {"choices": [{"message": {"content": "ignorar"}}]}
        if "9094" in url:
            return 200, {"data": [{"embedding": [0.1]}]}
        raise AssertionError(url)
    with patch("live_loop._post_json", side_effect=fake):
        out = loop.run(str(note))
    assert out["decision"] == "ignorar"
    assert out["write_back"] is None
    assert note.read_text(encoding="utf-8") == antes


# -- anti-loop --

def test_daemon_ignora_nota_auto_referente(tmp_path):
    v = tmp_path / "vault"
    v.mkdir()
    j = tmp_path / "ep.jsonl"
    p = v / "auto.md"
    p.write_text("# probe\npedido claro", encoding="utf-8")
    loop = _mini_loop(state_path=str(tmp_path / "s.json"))
    with patch("live_loop._post_json", side_effect=_fake_ler):
        out = loop.run(str(p))  # write-back real anexa bloco+marcador
    assert out["write_back"]["appended"] is True
    calls = []

    def factory():
        class M:
            def run(self, note):
                calls.append(note)
                return {"decision": "x", "activity": {"total_spikes": 1},
                        "exit_status": "ok"}
        return M()
    d = DaemonVault(vault_root=str(v), jsonl_path=str(j),
                    loop_factory=factory, min_interval_s=0, grace_s=1e9)
    d._seen[str(p)] = os.stat(str(p)).st_mtime - 100  # simula run anterior
    assert d.scan() == []  # eco proprio: 0 episodios
    assert calls == []
    # edicao real do usuario apos o bloco => volta a disparar
    with open(str(p), "a", encoding="utf-8") as fh:
        fh.write("\nnota nova do usuario: revisar amanha\n")
    got = d.scan()
    assert got == [str(p)]
