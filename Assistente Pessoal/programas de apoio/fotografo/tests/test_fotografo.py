"""Testes OFFLINE da feature Fotógrafo — sem rede, sem ComfyUI, sem LLM."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parent.parent
MCP_DIR = BASE / "mcp"
WF_DIR = BASE / "workflows"
SCHEMA = BASE / "schemas" / "dop_schema.gbnf"


def _carregar_server():
    spec = importlib.util.spec_from_file_location(
        "server_fotografo", str(MCP_DIR / "server_fotografo.py")
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["server_fotografo"] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- workflows
def test_workflows_validos():
    esperados = {
        "draft_sdxl.json": (
            {"CheckpointLoaderSimple", "CLIPTextEncode", "KSampler", "VAEDecode", "SaveImage"},
            ["{{PROMPT}}", "{{NEGATIVE}}", "{{SEED}}", "{{STEPS}}"],
        ),
        "img2img_cn.json": (
            {"CheckpointLoaderSimple", "CLIPTextEncode", "LoadImage", "ControlNetLoader",
             "ControlNetApplyAdvanced", "KSampler", "VAEDecode", "SaveImage"},
            ["{{PROMPT}}", "{{REFERENCE_IMAGE}}", "{{STRENGTH}}", "{{SEED}}"],
        ),
        "svd_xt.json": (
            {"ImageOnlyCheckpointLoader", "LoadImage", "SVD_img2vid_Conditioning",
             "VideoLinearCFGGuidance", "KSampler", "VAEDecode", "SaveAnimatedWEBP"},
            ["{{REFERENCE_IMAGE}}", "{{MOTION_BUCKET_ID}}", "{{FRAMES}}", "{{SEED}}"],
        ),
    }
    for nome, (classes, phs) in esperados.items():
        arq = WF_DIR / nome
        assert arq.exists(), f"ausente: {nome}"
        bruto = arq.read_text(encoding="utf-8")
        dado = json.loads(bruto)  # json válido
        assert isinstance(dado, dict) and dado, nome
        achadas = {n.get("class_type") for n in dado.values()}
        assert classes <= achadas, f"{nome}: faltam {classes - achadas}"
        for ph in phs:
            assert ph in bruto, f"{nome}: placeholder {ph} ausente"
        # pesos exatos
        if nome in ("draft_sdxl.json", "img2img_cn.json"):
            assert "sd_xl_base_1.0.safetensors" in bruto, nome
        if nome == "img2img_cn.json":
            assert "diffusion_pytorch_model_promax.safetensors" in bruto
        if nome == "svd_xt.json":
            assert "svd_xt_1_1.safetensors" in bruto


def test_schema_gbnf():
    assert SCHEMA.exists(), "dop_schema.gbnf ausente"
    txt = SCHEMA.read_text(encoding="utf-8")
    assert txt.lstrip().startswith("root ::="), "GBNF deve começar com root ::="
    for chave in ("camera_angle", "lighting_and_style", "technical_subjects"):
        assert chave in txt, f"chave {chave} ausente na gramática"


# ---------------------------------------------------------------- contrato
def test_contract(monkeypatch):
    srv = _carregar_server()

    class FakeResp:
        def __init__(self, dado):
            self._d = dado

        def raise_for_status(self):
            pass

        def json(self):
            return self._d

    # done com outputs
    hist_done = {"p1": {"status": {"completed": True},
                        "outputs": {"7": {"images": [{"filename": "a.png", "subfolder": "",
                                                     "type": "output"}]}}}}
    monkeypatch.setattr(srv.httpx, "get", lambda *a, **k: FakeResp(hist_done))
    r = srv.status_job.fn("p1") if hasattr(srv.status_job, "fn") else srv.status_job("p1")
    assert r["state"] == "done" and r["outputs"], r

    # queued (prompt_id desconhecido)
    monkeypatch.setattr(srv.httpx, "get", lambda *a, **k: FakeResp({}))
    r = srv.status_job.fn("x") if hasattr(srv.status_job, "fn") else srv.status_job("x")
    assert r["state"] == "queued", r

    # running
    hist_run = {"p2": {"status": {"completed": False}, "outputs": {}}}
    monkeypatch.setattr(srv.httpx, "get", lambda *a, **k: FakeResp(hist_run))
    r = srv.status_job.fn("p2") if hasattr(srv.status_job, "fn") else srv.status_job("p2")
    assert r["state"] == "running", r

    # error
    hist_err = {"p3": {"status": {"status_str": "error", "messages": ["boom"]}, "outputs": {}}}
    monkeypatch.setattr(srv.httpx, "get", lambda *a, **k: FakeResp(hist_err))
    r = srv.status_job.fn("p3") if hasattr(srv.status_job, "fn") else srv.status_job("p3")
    assert r["state"] == "error" and "boom" in r["message"], r


def test_display(monkeypatch, tmp_path):
    srv = _carregar_server()
    monkeypatch.setenv("DISPLAY_CMD", "true")
    srv.DISPLAY_CMD = "true"
    alvo = tmp_path / "img.png"
    alvo.write_bytes(b"\x89PNG fake")
    f = srv.display_locally.fn if hasattr(srv.display_locally, "fn") else srv.display_locally
    r = f(str(alvo))
    assert r["aberto"] is True, r
    r2 = f(str(tmp_path / "inexistente.png"))
    assert r2["aberto"] is False, r2
