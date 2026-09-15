"""TDD do DaemonVault (Wave 5 retake). Sem endpoints: LiveLoop mockado."""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from daemon_vault import DaemonVault


class Clock:
    def __init__(self):
        self.t = 1000.0
        self.slept = 0.0

    def __call__(self):
        return self.t

    def sleep(self, s):
        self.slept += s
        self.t += s

    def advance(self, s):
        self.t += s


def _mk(vault, jsonl, clock, **kw):
    calls = []

    def factory():
        class M:
            def run(self, note):
                calls.append(note)
                return {"decision": "ler", "activity": {"total_spikes": 7},
                        "exit_status": "ok"}
        return M()
    kw.setdefault("min_interval_s", 10.0)
    kw.setdefault("grace_s", 1e9)
    d = DaemonVault(vault_root=str(vault), jsonl_path=str(jsonl),
                    loop_factory=factory, time_fn=clock, sleep_fn=clock.sleep,
                    **kw)
    d.calls = calls
    return d


def _note(vault, name="n1.md", body="probe w5"):
    p = vault / name
    p.write_text(body, encoding="utf-8")
    return str(p)


def test_nova_nota_um_episodio(tmp_path):
    v = tmp_path / "vault"
    v.mkdir()
    j = tmp_path / "ep.jsonl"
    c = Clock()
    d = _mk(v, j, c)
    _note(v)
    assert d.scan_and_run_once() == 1
    assert len(d.calls) == 1
    assert j.exists()


def test_debounce_colapsa_rajada(tmp_path):
    v = tmp_path / "vault"
    v.mkdir()
    j = tmp_path / "ep.jsonl"
    c = Clock()
    d = _mk(v, j, c)
    p = _note(v)
    assert d.scan_and_run_once() == 1
    # edita em rajada dentro da janela 3s -> colapsa, nada novo
    for i in range(3):
        open(p, "a", encoding="utf-8").write(f"\n{i}")
        c.advance(0.5)
    assert d.scan_and_run_once() == 0
    assert len(d.calls) == 1
    # apos janela, o pendente vira 1 episodio so'
    c.advance(5.0)
    open(p, "a", encoding="utf-8").write("\ntarde")
    assert d.scan_and_run_once() == 1
    assert len(d.calls) == 2


def test_fila_max5_descarta_com_log(tmp_path):
    v = tmp_path / "vault"
    v.mkdir()
    j = tmp_path / "ep.jsonl"
    c = Clock()
    d = _mk(v, j, c, max_queue=5)
    d.enqueue([f"n{i}" for i in range(8)])
    assert len(d._queue) == 5
    assert d.dropped == 3
    assert any("descartado" in m for m in d.logs)


def test_once_termina(tmp_path):
    v = tmp_path / "vault"
    v.mkdir()
    j = tmp_path / "ep.jsonl"
    c = Clock()
    d = _mk(v, j, c, min_interval_s=0)
    _note(v, "a.md")
    _note(v, "b.md")
    n = d.scan_and_run_once()  # 1 ciclo, termina sem loop
    assert n == 2 and d._stop is False


def test_sigint_flusha_jsonl_valido(tmp_path):
    v = tmp_path / "vault"
    v.mkdir()
    j = tmp_path / "ep.jsonl"
    c = Clock()
    d = _mk(v, j, c, min_interval_s=0)
    _note(v)
    d.scan_and_run_once()
    d.request_stop(2, None)  # SIGINT
    assert d._stop is True
    lines = j.read_text(encoding="utf-8").strip().splitlines()
    assert lines and all(json.loads(line) for line in lines)


def test_jsonl_contem_campos(tmp_path):
    v = tmp_path / "vault"
    v.mkdir()
    j = tmp_path / "ep.jsonl"
    c = Clock()
    d = _mk(v, j, c, min_interval_s=0)
    _note(v)
    d.scan_and_run_once()
    e = json.loads(j.read_text(encoding="utf-8").strip().splitlines()[-1])
    for k in ("ts", "nota", "decisao", "spikes"):
        assert k in e, f"campo ausente: {k}"
    # idempotencia: 2o run nao duplica
    assert d.scan_and_run_once() == 0
    assert len(j.read_text(encoding="utf-8").strip().splitlines()) == 1
