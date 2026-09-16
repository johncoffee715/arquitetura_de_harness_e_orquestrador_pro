"""TDD do loop vivo vault -> SNN -> trio -> vault (Wave 2).

Mocks (dry-run, sem rede) + 1 E2E REAL contra :9084/:9091/:9094 com
probe-note criada e REMOVIDA em try/finally (mesmo em falha).
"""

from __future__ import annotations

import json
import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from live_loop import LiveLoop
from parser import parse_csv_to_csr

SNN_DIR = os.path.dirname(os.path.abspath(__file__))
MINI = os.path.join(SNN_DIR, "mini_edges.csv")
PROBE = os.path.abspath(os.path.join(
    SNN_DIR, "..", "cerebro com IA", "pipeline", "w2-probe-note.md"))
STATE = os.path.join(SNN_DIR, "data", "live_state.json")


def _mini_loop(**kw):
    row_ptr, col_idx, weight = parse_csv_to_csr(MINI)
    csr = type("C", (), {"row_ptr": row_ptr, "col_idx": col_idx,
                         "weight": weight, "n": len(row_ptr) - 1})()
    return LiveLoop(csr=csr, **kw)


def _fake_post(url, payload, timeout):
    if "9084" in url:
        return 200, {"choices": [{"message": {"content": "ler"}}]}
    if "9091" in url:
        return 200, {"function_calls": []}
    if "9094" in url:
        return 200, {"data": [{"embedding": [0.1, 0.2]}]}
    raise AssertionError(url)


def test_simulate_topk_regions(tmp_path):
    loop = _mini_loop()
    act = loop.simulate("nota probe", steps=4)
    assert act["total_spikes"] > 0
    assert act["topk"] and act["regions"]
    assert sum(act["regions"].values()) >= 0


def test_classify_decisao():
    assert LiveLoop.classify("  AGIR agora") == "agir"
    assert LiveLoop.classify("ler isso") == "ler"
    assert LiveLoop.classify("???") == "ignorar"


def test_classify_prolixo_w7():
    # W7: RWKV7 curioso responde prolixo; 'ler' tolerante, 'agir' estrito.
    assert LiveLoop.classify("Vou ler a nota com calma...") == "ler"
    assert LiveLoop.classify("Acho melhor ler a nota") == "ler"
    assert LiveLoop.classify("Faça uma leitura do conteúdo") == "ler"
    assert LiveLoop.classify("nota interessante, sem mais") == "ignorar"
    # prolixo sem 'agir' explicito NUNCA vira 'agir'
    assert LiveLoop.classify("Vou ler a nota com calma...") != "agir"
    assert LiveLoop.classify("Acho melhor ler a nota") != "agir"
    assert LiveLoop.classify("Faça uma leitura do conteúdo") != "agir"
    assert LiveLoop.classify("nota interessante, sem mais") != "agir"


def test_run_mock_ler_registra_needle_e_snapshot(tmp_path):
    st = str(tmp_path / "live_state.json")
    note = tmp_path / "n.md"
    note.write_text("# t\ncorpo")
    loop = _mini_loop(state_path=st)
    with patch("live_loop._post_json", side_effect=_fake_post):
        out = loop.run(str(note))
    assert out["exit_status"] == "ok"
    assert out["decision"] == "ler"
    assert out["needle"]["http"] == 200
    assert out["embedding_dim"] == 2
    assert json.loads(open(st).read())["decision"] == "ler"


def test_run_mock_ignorar_pula_needle(tmp_path):
    st = str(tmp_path / "live_state.json")
    note = tmp_path / "n.md"
    note.write_text("x")
    loop = _mini_loop(state_path=st)
    def fake(url, payload, timeout):
        if "9084" in url:
            return 200, {"choices": [{"message": {"content": "ignorar"}}]}
        raise AssertionError("needle/embed nao deveriam ser chamados"
                             if "9091" in url else url)
    with patch("live_loop._post_json", side_effect=fake):
        out = loop.run(str(note))
    assert out["exit_status"] == "ok" and out["needle"] is None


def test_falha_endpoint_nao_finge(tmp_path):
    note = tmp_path / "n.md"
    note.write_text("x")
    loop = _mini_loop(state_path=str(tmp_path / "s.json"))
    with patch("live_loop._post_json",
               side_effect=RuntimeError("POST ... falhou: timeout")):
        out = loop.run(str(note))
    assert out["exit_status"] == "failed" and "error" in out


def _rwkv_up() -> bool:
    """Probe curto do :9084 — e2e real so roda com a stack viva (skip-limpo)."""
    try:
        import urllib.request
        with urllib.request.urlopen("http://127.0.0.1:9084/v1/models",
                                    timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


def test_e2e_real_vault_trio_vault():
    if not _rwkv_up():
        pytest.skip("9084 down — e2e real exige stack viva")
    """E2E REAL: probe-note -> slice CSR real -> :9084/:9091/:9094."""
    probe_body = ("---\ntipo: probe-w2\n---\n# probe w2\n"
                  "Loop vivo vault-trio-vault: verificar decisão curta.\n")
    with open(PROBE, "w", encoding="utf-8") as fh:
        fh.write(probe_body)
    try:
        loop = LiveLoop.from_feather(limit_rows=5000)
        out = loop.run(PROBE, steps=6)
        assert out["exit_status"] == "ok", f"falha bruta: {out.get('error')}"
        assert isinstance(out["decision_raw"], str) and out["decision_raw"].strip()
        assert out["rwkv_http"] == 200
        assert os.path.exists(STATE)
        st = json.loads(open(STATE, encoding="utf-8").read())
        assert st["decision"] in ("ignorar", "ler", "agir")
        print(f"\nE2E rwkv_http={out['rwkv_http']} "
              f"decisao={out['decision_raw'][:80]!r}")
    finally:
        if os.path.exists(PROBE):
            os.remove(PROBE)
    assert not os.path.exists(PROBE), "probe-note NAO foi removida"


def test_classify_chatty_com_decisao():
    """B4: resposta chatty COM palavra de decisao no meio -> classifica."""
    assert LiveLoop.classify("Okay, let's see... vou ler a nota") == "ler"


def test_classify_chatty_sem_decisao():
    """B4: chatty SEM palavra nenhuma -> ignorar (default seguro)."""
    assert LiveLoop.classify("Okay, let's see") == "ignorar"


def test_classify_agir_so_explicito():
    """B4: 'agir' so como palavra unica; nunca inferido de substring."""
    assert LiveLoop.classify("agir") == "agir"
    assert LiveLoop.classify("Vamos gerir o agiramento") == "ignorar"


def test_classify_acentos_pontuacao():
    """B4: normalizacao — acentos e pontuacao nao bloqueiam o match."""
    assert LiveLoop.classify("Ler, com certeza!") == "ler"
    assert LiveLoop.classify("Ignorar.") == "ignorar"
