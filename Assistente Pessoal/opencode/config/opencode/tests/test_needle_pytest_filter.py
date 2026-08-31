#!/usr/bin/env python3
"""
Testes TDD para o filtro cirúrgico pytest do Needle 2 (R77/R28).

Cobre: extração de Localização/Assinatura/Delta, janela 256 tokens,
determinismo, CLI.
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts")

from needle_pytest_filter import filtrar_pytest

SCRIPT = "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts/needle_pytest_filter.py"

LOG_PADRAO = """tests/test_router.py:42: AssertionError
>   assert response.status_code == 200
E   AssertionError: expected status 200 but got 500
E   assert 500 == 200
_____ test_router.py _____
"""


class TestFiltroPytest:
    def test_localizacao_extraida(self):
        r = filtrar_pytest(LOG_PADRAO)
        assert r["localizacoes"][0]["arquivo"] == "tests/test_router.py"
        assert r["localizacoes"][0]["linha"] == "42"
        assert r["localizacoes"][0]["tipo"] == "AssertionError"

    def test_assinatura_extraida(self):
        r = filtrar_pytest(LOG_PADRAO)
        assert any("expected status 200 but got 500" in a for a in r["assinaturas"])

    def test_delta_extraido(self):
        r = filtrar_pytest(LOG_PADRAO)
        assert any("assert" in d for d in r["deltas"])

    def test_cabe_janela_256(self):
        r = filtrar_pytest(LOG_PADRAO)
        assert r["tokens_estimados"] <= 256
        assert r["cabe_janela_256"] is True

    def test_determinismo(self):
        assert filtrar_pytest(LOG_PADRAO) == filtrar_pytest(LOG_PADRAO)

    def test_log_grande_comprimido(self):
        """Log gigante deve comprimir para densidade pura (janela 256)."""
        log_grande = LOG_PADRAO + "\n".join(f"linha ruído {i}" for i in range(500))
        r = filtrar_pytest(log_grande)
        assert r["total_linhas_originais"] > 500
        assert r["tokens_estimados"] <= 256
        assert r["cabe_janela_256"] is True


class TestCLI:
    def test_cli_json(self):
        r = subprocess.run(
            [sys.executable, SCRIPT, "--json"],
            input=LOG_PADRAO, capture_output=True, text=True, timeout=10,
        )
        assert r.returncode == 0
        d = json.loads(r.stdout)
        assert "localizacoes" in d
        assert "assinaturas" in d
        assert "deltas" in d


class TestGabarito:
    def test_skill_tres_camadas(self):
        d = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/needle-pytest-filter")
        assert (d / "conceito.md").exists()
        assert (d / "gabarito.json").exists()
        assert (d / "mecanica.md").exists()
        assert (d / "SKILL.md").exists()