#!/usr/bin/env python3
"""
Testes TDD para o Roteador Híbrido L0/L0.5 (RWKV7 + Needle 2).

Cobre: parse de intent (GBNF), roteamento direto/complexo, coexistência,
gabarito R77.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts")

from roteador_hibrido import parse_intent, rotear, ROTAS_DIRETAS, ROTAS_COMPLEXAS


class TestParseIntent:
    def test_parse_valido(self):
        v = parse_intent('{"intent":"operacional","tipo":"hook","confianca":0.9,"resumo":"x"}')
        assert v["intent"] == "operacional"
        assert v["tipo"] == "hook"

    def test_parse_ruidoso(self):
        v = parse_intent('texto {"intent":"complexo","tipo":"brainstorm","confianca":0.7} fim')
        assert v["intent"] == "complexo"
        assert v["tipo"] == "brainstorm"

    def test_parse_invalido_default(self):
        v = parse_intent("lixo")
        assert v["intent"] == "complexo"
        assert v["tipo"] == "outro"


class TestRotas:
    def test_rotas_diretas(self):
        assert ROTAS_DIRETAS == {"mcp", "hook", "cli", "git"}

    def test_rotas_complexas(self):
        assert ROTAS_COMPLEXAS == {"brainstorm", "codigo", "rag"}


class TestRoteamento:
    def test_operacional_vai_needle(self):
        """Comando operacional → rota direto (Needle)."""
        r = rotear("Execute o hook stack-health-check")
        assert r["rota"] == "direto"

    def test_brainstorm_vai_denso(self):
        """Raciocínio complexo → LLMs densos."""
        r = rotear("Preciso brainstorm da arquitetura")
        assert r["rota"] == "complexo"
        assert "llm-densos" in r["destino"]

    def test_resultado_estrutura(self):
        """Resultado tem rota/destino/intento/payload."""
        r = rotear("teste")
        for k in ("rota", "destino", "intento", "payload"):
            assert k in r


class TestGabarito:
    def test_skill_tres_camadas(self):
        d = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/roteador-hibrido")
        assert (d / "conceito.md").exists()
        assert (d / "gabarito.json").exists()
        assert (d / "mecanica.md").exists()
        assert (d / "SKILL.md").exists()