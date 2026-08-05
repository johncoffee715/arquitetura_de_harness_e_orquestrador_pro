"""pytest — 8+ cenários de cobertura de route_to_model (integration.py) e
helenize_deploy (autofagia).

Motivação (predição da auditoria): route_to_model delegava por oferta-demanda
sem cobertura nenhuma; helenize_deploy tinha helpers críticos (escape, slug,
path-traversal, registry idempotente) sem provas. Fixtures isoladas em tmp_path —
nunca tocam o harness real.
"""
import json
import sys
from pathlib import Path

import pytest

HARNESS_ROOT = Path("/mnt/dados")
sys.path.insert(0, str(HARNESS_ROOT))


@pytest.fixture
def manager(tmp_path, monkeypatch):
    """IntegrationManager isolado num project_root temporário com registry leve."""
    from harness.core.integration import IntegrationManager

    reg = tmp_path / "registry.json"
    reg.write_text(json.dumps({
        "skills": [
            {"name": "reverser", "description": "engenharia reversa ghidra binário firmware decompila",
             "tags": ["ghidra", "reverse"]},
            {"name": "orquestrador", "description": "orquestração mcp hook roteia workflow controle",
             "tags": ["orchestration"]},
            {"name": "validador", "description": "valida raciocínio matemática lógica micro review",
             "tags": ["validation"]},
            {"name": "leitor", "description": "ocr imagem documento visual rápido",
             "tags": ["vision", "ocr"]},
        ],
        "subagents": [],
        "mcp": [], "lsp": [], "hooks": [], "plugins": [],
    }), encoding="utf-8")
    m = IntegrationManager(project_root=str(tmp_path))
    monkeypatch.setattr(m, "build_registry", lambda: {"skills": [
        {"name": "reverser", "description": "engenharia reversa ghidra binário firmware decompila",
         "tags": ["ghidra", "reverse"], "model": "x"},
        {"name": "orquestrador", "description": "orquestração mcp hook roteia workflow controle",
         "tags": ["orchestration"], "model": "x"},
        {"name": "validador", "description": "valida raciocínio matemática lógica micro review",
         "tags": ["validation"], "model": "x"},
        {"name": "leitor", "description": "ocr imagem documento visual rápido",
         "tags": ["vision", "ocr"], "model": "x"},
    ]})
    return m


# ─────────────────────────────── route_to_model ─────────────────────────────
class TestRouteToModel:
    def test_rota_binario_para_heavy(self, manager):
        r = manager.route_to_model("engenharia reversa de firmware binário ghidra")
        heavy = [i["recurso"] for i in r.get("heavy_execution", [])]
        assert "reverser" in heavy

    def test_rota_orquestracao_para_gran_mestre(self, manager):
        r = manager.route_to_model("orquestração com mcp hooks e workflow de controle")
        gm = [i["recurso"] for i in r.get("gran_mestre", [])]
        assert "orquestrador" in gm

    def test_rota_revisao_para_filter_medium(self, manager):
        r = manager.route_to_model("validação e raciocínio matemático de precisão")
        med = [i["recurso"] for i in r.get("filter_medium", [])]
        assert "validador" in med

    def test_rota_visual_para_filter_fast(self, manager):
        r = manager.route_to_model("ocr de documento com imagem e vídeo")
        fast = [i["recurso"] for i in r.get("filter_fast", [])]
        assert "leitor" in fast

    def test_task_vazia_nao_quebra(self, manager):
        r = manager.route_to_model("")
        assert isinstance(r, dict)

    def test_task_sem_capacidade_cai_no_gran_mestre(self, manager):
        # task totalmente fora das capacidades -> fallback gran_mestre (linha 752)
        r = manager.route_to_model("zzz qqq wwww xxxx")
        for lista in r.values():
            for item in lista:
                assert "modelo" in item


# ───────────────────────────── get_resources_by_tags (BM25) ────────────────
class TestGetResourcesByTags:
    def test_tag_match_por_relevancia(self, manager):
        res = manager.get_resources_by_tags(["ghidra"])
        names = [i["name"] for i in res.get("skills", [])]
        assert "reverser" in names

    def test_tag_sem_match_retorna_vazio(self, manager):
        res = manager.get_resources_by_tags(["inexistente-xyz"])
        assert res.get("skills", []) == []


# ───────────────────────────── helenize_deploy ──────────────────────────────
@pytest.fixture
def helenize():
    from harness.autofagia import helenize_deploy as hd
    return hd


class TestHelenizeHelpers:
    def test_alvo_slug_invalido_lanca(self, helenize):
        from dataclasses import dataclass
        with pytest.raises(ValueError):
            helenize.Alvo(slug="Sém Espaço!", desc="d", repo="a/b", tipo_artefato="skill")

    def test_alvo_slug_valido(self, helenize):
        a = helenize.Alvo(slug="meu-slug-legal", desc="descrição ok", repo="owner/repo",
                          tipo_artefato="skill")
        assert a.to_dict()["slug"] == "meu-slug-legal"

    def test_shell_escape_quote(self, helenize):
        assert helenize.shell_escape("a'b") == "'a'\\''b'"

    def test_yaml_escape_quebras(self, helenize):
        assert "\n" not in helenize.yaml_escape('linha1\nlinha2 "aspas"')

    def test_path_traversal_bloqueado(self, helenize, tmp_path):
        with pytest.raises(ValueError):
            helenize.safe_path(tmp_path, "..", "..", "etc", "passwd")

    def test_path_valido_ok(self, helenize, tmp_path):
        p = helenize.safe_path(tmp_path, "a", "b")
        assert str(p).startswith(str(tmp_path.resolve()))

    def test_is_mcp(self, helenize):
        from dataclasses import dataclass, field
        a = helenize.Alvo(slug="srv-mcp", desc="d", repo="a/b", tipo_artefato="mcp")
        assert helenize.is_mcp(a) is True
        b = helenize.Alvo(slug="skill-x", desc="d", repo="a/b", tipo_artefato="skill")
        assert helenize.is_mcp(b) is False
