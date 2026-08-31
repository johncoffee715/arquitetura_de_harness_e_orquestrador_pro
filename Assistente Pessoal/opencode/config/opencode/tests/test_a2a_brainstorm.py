#!/usr/bin/env python3
"""
Testes TDD para o A2A Brainstorm v2 (R40/R34 — refutação incansável, nota retroativa).

Cobre: papéis (sem árbitro no loop), constantes homeopáticas recalibradas,
parse de avaliação GBNF, gabarito, 3 camadas R77.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts")

from a2a_brainstorm import (
    TRIADE, NOTA_INICIAL, LIMIAR_CONVERGENCIA, MAX_ROUNDS, DELTA_ACEITO,
    parse_avaliacao, chamar_slot,
)


class TestPapéis:
    def test_seis_papeis_sem_arbitro(self):
        """Sem árbitro no loop — refutação incansável entre os LLMs (R40)."""
        assert set(TRIADE.keys()) == {"propositor", "refutador", "refutador_agil",
                                      "reflexo", "ingestor", "escalacao"}
        assert "arbitro" not in TRIADE, "árbitro removido do loop (custo alto p/ binário)"

    def test_escalacao_judge_impasse(self):
        """Judge-3B (escalacao) só em impasse — coexistência justificada."""
        assert TRIADE["escalacao"]["port"] == 9085
        assert TRIADE["propositor"]["port"] == 9088
        assert TRIADE["refutador"]["port"] == 9090
        assert TRIADE["refutador_agil"]["port"] == 9092


class TestConstantesHomeopaticas:
    def test_piso_real(self):
        """Piso real R34: 0.0000001 — nada é perfeito."""
        assert NOTA_INICIAL == 0.0000001

    def test_limiar_recalibrado_baixo(self):
        """Limiar recalibrado para BAIXO (era 70 — inflado)."""
        assert LIMIAR_CONVERGENCIA <= 30.0
        assert LIMIAR_CONVERGENCIA < 70

    def test_delta_homeopatico(self):
        """Delta mínimo homeopático (subida lenta, nunca salto)."""
        assert DELTA_ACEITO >= 1.0
        assert DELTA_ACEITO <= 3.0

    def test_max_rounds_teto(self):
        """Teto de segurança anti-loop-infinito (refutação incansável com trava)."""
        assert MAX_ROUNDS >= 5


class TestParseAvaliacao:
    def test_parse_valido(self):
        """JSON estrito do GBNF é parseado."""
        v = parse_avaliacao('{"delta": 2, "impresso": true}')
        assert v["delta"] == 2
        assert v["impresso"] is True

    def test_parse_delta_negativo(self):
        """Delta negativo (regressão) é aceito — nota cai."""
        v = parse_avaliacao('{"delta": -1, "impresso": false}')
        assert v["delta"] == -1

    def test_parse_invalido_default(self):
        """JSON inválido → delta 0, impresso false (fail-safe)."""
        v = parse_avaliacao("lixo")
        assert v["delta"] == 0
        assert v["impresso"] is False


class TestChamarSlot:
    def test_slot_offline_graceful(self):
        """Slot offline → ok=False (graceful)."""
        r = chamar_slot("propositor", [{"role": "user", "content": "teste"}])
        assert isinstance(r, dict)
        assert "ok" in r


class TestGabarito:
    def test_tres_camadas(self):
        """Skill com 3 camadas R77."""
        d = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/a2a-brainstorm")
        assert (d / "conceito.md").exists()
        assert (d / "gabarito.json").exists()
        assert (d / "mecanica.md").exists()
        assert (d / "SKILL.md").exists()

    def test_gabarito_valido(self):
        """Gabarito JSON válido."""
        g = json.loads(Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/a2a-brainstorm/gabarito.json").read_text())
        assert g["feature"] == "a2a-brainstorm"
        assert "concordância preguiçosa" in " ".join(g["deny"]["behaviors"])