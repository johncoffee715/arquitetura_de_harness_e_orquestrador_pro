#!/usr/bin/env python3
"""
Testes TDD para hefesto_motor.py v2.0.0 (Dispatcher)

RED → GREEN → REFACTOR · Cobertura ≥80% (R28/R44)
Cobre: inventário R75, roteamento por categoria, fallback, gabarito R77,
Panteão R34, CLI.
"""

import sys
import json
import subprocess
import os

sys.path.insert(0, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts")

from hefesto_motor import (
    load_inventory,
    list_cpu_slots,
    resolve_slot_for_role,
    validate_gabarito,
    execute_workflow,
    _evaluate_pillar,
    setup_logger,
    CATEGORY_ROUTES,
    FALLBACK_ROUTES,
)

MOTOR = "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts/hefesto_motor.py"


def run_motor(args: list) -> dict:
    """Executa o motor via CLI e retorna JSON parseado."""
    cmd = [sys.executable, MOTOR] + args
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if result.returncode != 0:
        return {"error": result.stderr, "stdout": result.stdout}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "JSON inválido", "stdout": result.stdout}


class TestLoadInventory:
    def test_inventory_exists(self):
        inv = load_inventory()
        assert "models" in inv
        assert isinstance(inv["models"], list)
        assert len(inv["models"]) > 0

    def test_inventory_schema_version(self):
        inv = load_inventory()
        assert inv.get("schema_version") == 1


class TestListCpuSlots:
    def test_returns_list(self):
        logger = setup_logger("/tmp/test_hefesto.log")
        slots = list_cpu_slots(logger)
        assert isinstance(slots, list)

    def test_only_online_cpu_models(self):
        logger = setup_logger("/tmp/test_hefesto.log")
        slots = list_cpu_slots(logger)
        inv = load_inventory()
        for slot in slots:
            found = False
            for m in inv["models"]:
                if m["id"] == slot["id"]:
                    assert m["status"] == "online"
                    assert m["sector"].startswith("CPU")
                    found = True
                    break
            assert found, f"Slot {slot['id']} não encontrado no inventário"


class TestResolveSlotForRole:
    def test_decompilacao_resolves_contrato_plano(self):
        """R75: decompilacao → contrato-plano (:9088)."""
        logger = setup_logger("/tmp/test_hefesto.log")
        slot = resolve_slot_for_role("decompilacao", logger)
        assert slot is not None
        assert slot["category"] == "contrato-plano"
        assert slot["port"] == "9088"

    def test_autofagia_resolves_refutacao(self):
        """R75: autofagia → refutacao (:9090)."""
        logger = setup_logger("/tmp/test_hefesto.log")
        slot = resolve_slot_for_role("autofagia", logger)
        assert slot is not None
        assert slot["category"] == "refutacao"
        assert slot["port"] == "9090"

    def test_helenizacao_resolves_contrato_plano(self):
        """R75: helenizacao → contrato-plano (:9088)."""
        logger = setup_logger("/tmp/test_hefesto.log")
        slot = resolve_slot_for_role("helenizacao", logger)
        assert slot is not None
        assert slot["category"] == "contrato-plano"

    def test_forja_resolves_forja_or_fallback_judge(self):
        """R75: forja → forja (:9091); fallback judge (:9085) se offline."""
        logger = setup_logger("/tmp/test_hefesto.log")
        slot = resolve_slot_for_role("forja", logger)
        assert slot is not None
        assert slot["category"] in ("forja", "judge")

    def test_unknown_role_returns_none(self):
        logger = setup_logger("/tmp/test_hefesto.log")
        slot = resolve_slot_for_role("role_inexistente", logger)
        assert slot is None

    def test_category_routes_complete(self):
        """As 4 fases do pipeline devem estar mapeadas (R75)."""
        assert set(CATEGORY_ROUTES.keys()) == {"decompilacao", "autofagia", "helenizacao", "forja"}


class TestValidateGabarito:
    def test_gabarito_violation_denied(self):
        """Ação em deny → recusa ignição (R77 camada 2)."""
        logger = setup_logger("/tmp/test_hefesto.log")
        assert validate_gabarito("hefesto-decompilacao", "modificar o original", logger) is False

    def test_gabarito_allowed_action(self):
        """Ação fora do deny → ignição permitida."""
        logger = setup_logger("/tmp/test_hefesto.log")
        assert validate_gabarito("hefesto-decompilacao", "execute", logger) is True

    def test_gabarito_missing_ignored(self):
        """Gabarito inexistente → validação ignorada (fail-open)."""
        logger = setup_logger("/tmp/test_hefesto.log")
        assert validate_gabarito("skill-inexistente", "execute", logger) is True

    def test_all_four_skills_have_valid_gabaritos(self):
        """As 4 skills atômicas devem ter gabarito.json válido com allow/deny."""
        import json as _json
        from pathlib import Path
        skills_dir = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills")
        for skill in ["hefesto-decompilacao", "hefesto-autofagia", "hefesto-helenizacao", "hefesto-forja"]:
            gp = skills_dir / skill / "gabarito.json"
            assert gp.exists(), f"{skill}/gabarito.json ausente"
            g = _json.loads(gp.read_text(encoding="utf-8"))
            assert "allow" in g and "deny" in g
            assert "sampling" in g["allow"]


class TestEvaluatePillar:
    def test_with_evidence_returns_score(self):
        logger = setup_logger("/tmp/test_hefesto.log")
        data = {"autophagy_score": 96.5, "autophagy_evidence": ["E-001"]}
        result = _evaluate_pillar("autophagy", data, logger)
        assert result["score"] == 96.5
        assert result["status"] == "EVALUATED"

    def test_without_evidence_returns_unknown_piso(self):
        logger = setup_logger("/tmp/test_hefesto.log")
        result = _evaluate_pillar("autophagy", {}, logger)
        assert result["score"] == 0.0000001
        assert result["status"] == "UNKNOWN"
        assert "sem evidência" in result.get("note", "")

    def test_score_bounds_respected(self):
        logger = setup_logger("/tmp/test_hefesto.log")
        data = {"autophagy_score": 150.0, "autophagy_evidence": ["E-001"]}
        result = _evaluate_pillar("autophagy", data, logger)
        assert 0.0000001 <= result["score"] <= 100.0


class TestExecuteWorkflow:
    def test_gabarito_violation_blocks(self):
        """Fase desconhecida/violação → GABARITO_VIOLADO."""
        logger = setup_logger("/tmp/test_hefesto.log")
        result = execute_workflow({"phase": "fase-inexistente", "artifact": "x"}, logger)
        assert result["status"] == "GABARITO_VIOLADO"

    def test_with_evidence_terminates_loop(self):
        logger = setup_logger("/tmp/test_hefesto.log")
        payload = {
            "phase": "forja",
            "artifact": "teste",
            "autophagy_score": 96.0, "autophagy_evidence": ["E-001"],
            "decompilation_score": 97.0, "decompilation_evidence": ["E-002"],
            "helenization_score": 95.5, "helenization_evidence": ["E-003"],
            "forging_score": 98.0, "forging_evidence": ["E-004"],
        }
        result = execute_workflow(payload, logger)
        assert result["average_score"] > 95.0
        assert result["dev_loop_terminated"] is True
        assert result["status"] == "OLYMPIAN_PERFECTION"
        assert result["gabarito_validado"] is True

    def test_without_evidence_does_not_terminate(self):
        logger = setup_logger("/tmp/test_hefesto.log")
        result = execute_workflow({"phase": "forja", "artifact": "teste"}, logger)
        assert result["dev_loop_terminated"] is False
        assert result["status"] == "FREEZE_PAUSE_REQUIRED"

    def test_active_model_included(self):
        logger = setup_logger("/tmp/test_hefesto.log")
        result = execute_workflow({"phase": "forja", "artifact": "teste"}, logger)
        assert "active_model" in result
        assert result["active_model"] is not None


class TestCLI:
    def test_list_cpu_cli(self):
        out = run_motor(["--list-cpu"])
        assert "cpu_slots" in out

    def test_resolve_cli(self):
        out = run_motor(["--resolve", "decompilacao"])
        assert out.get("category") == "contrato-plano"

    def test_execute_cli(self):
        payload = json.dumps({"phase": "forja", "artifact": "cli-test"})
        out = run_motor(["--execute", payload])
        assert "status" in out