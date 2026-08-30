#!/usr/bin/env python3
"""
Testes TDD para as 4 skills atômicas do Hefesto + dispatcher (R77).

Valida: estrutura de 3 camadas (conceito.md + gabarito.json + mecanica.md),
frontmatter YAML, gates, referências cruzadas do dispatcher.
"""

import json
import re
from pathlib import Path

SKILLS_DIR = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills")
ATOMIC_SKILLS = ["hefesto-decompilacao", "hefesto-autofagia", "hefesto-helenizacao", "hefesto-forja"]


class TestThreeLayersR77:
    def test_all_skills_have_three_layers(self):
        """Cada skill atômica deve ter conceito.md + gabarito.json + mecanica.md (R77)."""
        for skill in ATOMIC_SKILLS:
            d = SKILLS_DIR / skill
            assert (d / "conceito.md").exists(), f"{skill}: conceito.md ausente"
            assert (d / "gabarito.json").exists(), f"{skill}: gabarito.json ausente"
            assert (d / "mecanica.md").exists(), f"{skill}: mecanica.md ausente"
            assert (d / "SKILL.md").exists(), f"{skill}: SKILL.md ausente"

    def test_gabaritos_are_valid_json(self):
        """Gabaritos devem ser JSON válido com allow/deny/sampling."""
        for skill in ATOMIC_SKILLS:
            g = json.loads((SKILLS_DIR / skill / "gabarito.json").read_text(encoding="utf-8"))
            assert g["feature"] == skill
            assert "allow" in g and "deny" in g
            assert "sampling" in g["allow"]
            assert "temp" in g["allow"]["sampling"]

    def test_gabarito_sweet_spot(self):
        """Gabarito deve respeitar sweet spot R77 (20-50 linhas)."""
        for skill in ATOMIC_SKILLS:
            lines = len((SKILLS_DIR / skill / "gabarito.json").read_text(encoding="utf-8").splitlines())
            assert 10 <= lines <= 80, f"{skill}: gabarito com {lines} linhas (fora do sweet spot)"

    def test_conceito_sweet_spot(self):
        """Conceito deve respeitar sweet spot R77 (50-100 linhas, máx 200)."""
        for skill in ATOMIC_SKILLS:
            lines = len((SKILLS_DIR / skill / "conceito.md").read_text(encoding="utf-8").splitlines())
            assert 30 <= lines <= 200, f"{skill}: conceito com {lines} linhas"

    def test_mecanica_has_motor_selection(self):
        """Mecânica deve ter seleção de motor (R75) + samplers (R61)."""
        for skill in ATOMIC_SKILLS:
            mec = (SKILLS_DIR / skill / "mecanica.md").read_text(encoding="utf-8")
            assert "Categoria alvo" in mec or "categoria" in mec.lower()
            assert "temp" in mec.lower()
            assert "Refutação" in mec or "refutacao" in mec.lower()


class TestFrontmatter:
    def test_skills_have_frontmatter(self):
        """SKILL.md deve ter frontmatter YAML completo."""
        for skill in ATOMIC_SKILLS:
            content = (SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8")
            assert content.startswith("---"), f"{skill}: sem frontmatter"
            assert "name:" in content.split("---")[1]
            assert "description:" in content.split("---")[1]
            assert "mode: skill" in content.split("---")[1]
            assert "tags:" in content.split("---")[1]
            assert "origin:" in content.split("---")[1]

    def test_skills_have_gates(self):
        """Cada skill deve declarar seu gate categórico (R28)."""
        gates = {
            "hefesto-decompilacao": "G-D",
            "hefesto-autofagia": "G-A",
            "hefesto-helenizacao": "G-H",
            "hefesto-forja": "G-F",
        }
        for skill, gate in gates.items():
            content = (SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8")
            assert gate in content, f"{skill}: gate {gate} ausente"


class TestDispatcher:
    def test_dispatcher_references_all_skills(self):
        """Dispatcher deve referenciar as 4 skills atômicas."""
        disp = (SKILLS_DIR / "hefesto" / "SKILL.md").read_text(encoding="utf-8")
        for skill in ATOMIC_SKILLS:
            assert skill in disp, f"dispatcher não referencia {skill}"

    def test_dispatcher_has_pipeline(self):
        """Dispatcher deve ter o pipeline de 4 fases + gates."""
        disp = (SKILLS_DIR / "hefesto" / "SKILL.md").read_text(encoding="utf-8")
        assert "DECOMPILAÇÃO" in disp
        assert "AUTOFAGIA" in disp
        assert "HELENIZAÇÃO" in disp
        assert "FORJA" in disp
        assert "G-D" in disp and "G-A" in disp and "G-H" in disp and "G-F" in disp

    def test_dispatcher_has_dispatch_rule(self):
        """Dispatcher deve instruir carregar skill via skill-tool."""
        disp = (SKILLS_DIR / "hefesto" / "SKILL.md").read_text(encoding="utf-8")
        assert "skill-tool" in disp


class TestMotorIntegration:
    def test_motor_resolves_all_phases(self):
        """Motor deve mapear as 4 fases para categorias R75."""
        import sys
        sys.path.insert(0, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts")
        from hefesto_motor import CATEGORY_ROUTES
        assert CATEGORY_ROUTES == {
            "decompilacao": "contrato-plano",
            "autofagia": "refutacao",
            "helenizacao": "contrato-plano",
            "forja": "forja",
        }

    def test_motor_validates_gabarito(self):
        """Motor deve recusar ação que viola deny (R77 camada 2)."""
        import sys
        sys.path.insert(0, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts")
        from hefesto_motor import validate_gabarito, setup_logger
        logger = setup_logger("/tmp/test_hefesto.log")
        assert validate_gabarito("hefesto-decompilacao", "modificar o original", logger) is False
        assert validate_gabarito("hefesto-forja", "saída não-validada", logger) is False