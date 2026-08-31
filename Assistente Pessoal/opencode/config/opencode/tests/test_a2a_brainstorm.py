#!/usr/bin/env python3
"""
Testes TDD para o A2A Brainstorm (R40/R34/R18/R77).

Cobre: tríade fixa, parse do árbitro, regras de engajamento (max iterações,
convergência, escalação), gabarito, 3 camadas R77.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts")

from a2a_brainstorm import (
    TRIADE, MAX_ROUNDS, CONVERGENCIA, IMPRESSAO,
    parse_arbitro, chamar_slot,
)


class TestTriade:
    def test_quatro_papeis(self):
        """Tríade + escalação = 4 papéis fixos."""
        assert set(TRIADE.keys()) == {"propositor", "refutador", "arbitro", "escalacao"}

    def test_papeis_em_slots_distintos(self):
        """Cada papel em slot distinto (diversidade de pesos)."""
        ports = [v["port"] for v in TRIADE.values()]
        assert len(set(ports)) == 4, "papéis devem estar em slots distintos"

    def test_slots_reais(self):
        """Slots devem bater com o inventário R75."""
        assert TRIADE["propositor"]["port"] == 9088
        assert TRIADE["refutador"]["port"] == 9090
        assert TRIADE["arbitro"]["port"] == 9085
        assert TRIADE["escalacao"]["port"] == 8083

    def test_sampling_por_papel(self):
        """Sampling por papel (R61): árbitro temp baixo, refutador temp alto."""
        assert TRIADE["arbitro"]["temp"] <= 0.15
        assert TRIADE["refutador"]["temp"] >= 0.8
        assert TRIADE["propositor"]["temp"] == 0.6


class TestRegrasEngajamento:
    def test_max_rounds(self):
        """Max 3 rodadas (R18) antes de escalar."""
        assert MAX_ROUNDS == 3

    def test_convergencia(self):
        """Convergência média > 95 (R34)."""
        assert CONVERGENCIA == 95.0

    def test_impressao(self):
        """Impressão ≥ 90 (R40)."""
        assert IMPRESSAO == 90.0


class TestParseArbitro:
    def test_parse_valido(self):
        """JSON válido do árbitro é parseado."""
        raw = '{"nota": 92.5, "bugs": ["bug1"], "elogios": ["e1"], "procede_refutacao": false, "veredito": "PASSOU_CATEGORICO"}'
        v = parse_arbitro(raw)
        assert v["nota"] == 92.5
        assert v["veredito"] == "PASSOU_CATEGORICO"

    def test_parse_ruidoso(self):
        """JSON com ruído ao redor é extraído."""
        raw = 'Texto antes {"nota": 88.0, "bugs": ["x"], "elogios": [], "procede_refutacao": true, "veredito": "REESCREVER"} texto depois'
        v = parse_arbitro(raw)
        assert v["nota"] == 88.0
        assert v["veredito"] == "REESCREVER"

    def test_parse_invalido_piso(self):
        """JSON inválido → piso R34 (0.0000001) + REESCREVER."""
        v = parse_arbitro("resposta sem json")
        assert v["nota"] == 0.0000001
        assert v["veredito"] == "REESCREVER"


class TestChamarSlot:
    def test_slot_offline_graceful(self):
        """Slot offline → ok=False (graceful, não quebra)."""
        r = chamar_slot("propositor", [{"role": "user", "content": "teste"}])
        assert isinstance(r, dict)
        assert "ok" in r


class TestGabarito:
    def test_gabarito_valido(self):
        """Gabarito JSON válido com allow/deny."""
        gp = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/a2a-brainstorm/gabarito.json")
        g = json.loads(gp.read_text(encoding="utf-8"))
        assert g["feature"] == "a2a-brainstorm"
        assert any("concordância preguiçosa" in b for b in g["deny"]["behaviors"])
        assert "loop infinito de discordância" in g["deny"]["behaviors"]

    def test_tres_camadas(self):
        """Skill com 3 camadas R77."""
        d = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/a2a-brainstorm")
        assert (d / "conceito.md").exists()
        assert (d / "gabarito.json").exists()
        assert (d / "mecanica.md").exists()
        assert (d / "SKILL.md").exists()