"""pytest — 8 cenários do arsenal v2 (predição da auditoria R10, materializada).

Cobre os fluxos de R10: normalização int/list, exit codes 1/2/3, lazy --cat,
--pads, --json, --fresh (subprocess), agent-registry ausente, registry corrompido.
Fixtures isoladas em tmp_path — nunca tocam o harness real.
"""
import json
import sys
from pathlib import Path

import pytest

HARNESS_AUTOFAGIA = Path("/mnt/dados/harness/autofagia")
sys.path.insert(0, str(HARNESS_AUTOFAGIA))

import arsenal  # noqa: E402


@pytest.fixture
def env(tmp_path, monkeypatch):
    """Ambiente mínimo: registry E agent-registry escritos em tmp_path."""
    reg = tmp_path / "registry.json"
    agent = tmp_path / "agent-registry.json"
    reg.write_text(json.dumps({
        "plugins": ["p1"], "mcp": 1, "lsp": 2,
        "hooks": ["h1", "h2"], "skills": 3, "subagents": ["s1"]
    }), encoding="utf-8")
    agent.write_text(json.dumps({
        "entries": [
            {"id": "a1", "origem": {"tipo_origem": "framework-externo", "framework": "f/x"},
             "numero_padraes": 5, "formato_orquestravel": {"skill": True,
             "subagent": True, "hook": True, "plugin": False, "mcp": False, "lsp": False},
             "tags": ["t1"], "status": "ativo"},
            {"id": "sem-padrao", "origem": {"tipo_origem": "framework-externo", "framework": "g/y"},
             "numero_padraes": 0, "formato_orquestravel": {}, "tags": [], "status": "ativo"},
            {"id": "interno", "origem": {"tipo_origem": "interno"},
             "numero_padraes": 0, "formato_orquestravel": {}, "tags": [], "status": "ativo"},
        ]
    }), encoding="utf-8")
    monkeypatch.setattr(arsenal, "REGISTRY_PATH", reg)
    monkeypatch.setattr(arsenal, "AGENT_REGISTRY_PATH", agent)
    return tmp_path


def test_cenario1_modo_padrao(env):
    """Cenário 1 — modo padrão: resumo global funciona e mostra total."""
    loader = arsenal.RegistryLoader(arsenal.REGISTRY_PATH, arsenal.AGENT_REGISTRY_PATH)
    summ = arsenal.Summarizer(loader.load(), loader.load_agent_meta()).summarize()
    assert summ.meta["total_artefatos_globais"] == 1 + 1 + 2 + 2 + 3 + 1
    assert summ.meta["total_helenizados"] == 2  # só os 2 framework-externo


def test_cenario2_cat_lazy(env):
    """Cenário 2 — --cat hooks: só a categoria filtrada aparece (lazy)."""
    loader = arsenal.RegistryLoader(arsenal.REGISTRY_PATH, arsenal.AGENT_REGISTRY_PATH)
    summ = arsenal.Summarizer(loader.load(), loader.load_agent_meta()).summarize(cat_filter="hooks")
    assert list(summ.categories.keys()) == ["hooks"]
    assert summ.categories["hooks"]["total"] == 2


def test_cenario3_json_unicode(env, capsys):
    """Cenário 3 — --json: output parseável com ensure_ascii=False (Unicode ok)."""
    loader = arsenal.RegistryLoader(arsenal.REGISTRY_PATH, arsenal.AGENT_REGISTRY_PATH)
    summ = arsenal.Summarizer(loader.load(), loader.load_agent_meta()).summarize()
    out = arsenal.Formatter.format_json(summ)
    parsed = json.loads(out)
    assert "helenizados" in parsed
    assert "\\u" not in out


def test_cenario4_pads_exclui_sem_padrao(env):
    """Cenário 4 — --pads: exclui helenizados com numero_padraes == 0."""
    loader = arsenal.RegistryLoader(arsenal.REGISTRY_PATH, arsenal.AGENT_REGISTRY_PATH)
    summ = arsenal.Summarizer(loader.load(), loader.load_agent_meta()).summarize(only_with_pads=True)
    assert all(h.padroes > 0 for h in summ.helenizados)
    assert len(summ.helenizados) == 1  # 'sem-padrao' filtrado


def test_cenario5_fresh_subprocess(env, monkeypatch):
    """Cenário 5 — --fresh: subprocess validado (rc/stdout/JSON) e registry reescrito."""
    import subprocess as sp

    class FakeResult:
        returncode = 0
        stdout = json.dumps({"plugins": 9})
        stderr = ""

    monkeypatch.setattr(sp, "run", lambda *a, **k: FakeResult())
    monkeypatch.setattr(arsenal, "INTEGRATION_PY", Path("/mnt/dados/harness/core/integration.py"))
    loader = arsenal.RegistryLoader(arsenal.REGISTRY_PATH, arsenal.AGENT_REGISTRY_PATH)
    data = loader.build_fresh()
    assert data == {"plugins": 9}
    assert json.loads(arsenal.REGISTRY_PATH.read_text()) == {"plugins": 9}


def test_cenario6_agent_registry_ausente(env, monkeypatch, capsys):
    """Cenário 6 — agent-registry ausente: avisa e segue, exit 0."""
    monkeypatch.setattr(arsenal, "AGENT_REGISTRY_PATH", env / "nao-existe.json")
    loader = arsenal.RegistryLoader(arsenal.REGISTRY_PATH, arsenal.AGENT_REGISTRY_PATH)
    summ = arsenal.Summarizer(loader.load(), loader.load_agent_meta()).summarize()
    assert summ.helenizados == []
    assert summ.meta["total_helenizados"] == 0


def test_cenario7_registry_corrompido(env, monkeypatch):
    """Cenário 7 — registry corrompido: exit 2 (dados inválidos)."""
    bad = env / "registry-bad.json"
    bad.write_text("{not-json", encoding="utf-8")
    monkeypatch.setattr(arsenal, "REGISTRY_PATH", bad)
    monkeypatch.setattr(arsenal, "AGENT_REGISTRY_PATH", env / "agent-registry.json")
    loader = arsenal.RegistryLoader(arsenal.REGISTRY_PATH, arsenal.AGENT_REGISTRY_PATH)
    with pytest.raises(RuntimeError):
        loader.load()


def test_cenario8_integration_py_ausente(env, monkeypatch):
    """Cenário 8 — integration.py ausente: exit 1 (FileNotFoundError)."""
    monkeypatch.setattr(arsenal, "INTEGRATION_PY", env / "nao-existe.py")
    loader = arsenal.RegistryLoader(env / "registry-ausente.json", env / "agent-registry.json")
    with pytest.raises(FileNotFoundError):
        loader.build_fresh()
