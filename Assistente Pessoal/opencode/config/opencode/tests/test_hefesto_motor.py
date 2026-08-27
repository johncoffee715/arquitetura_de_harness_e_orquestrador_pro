#!/usr/bin/env python3
"""
Testes TDD para hefesto_motor.py

RED → GREEN → REFACTOR
Cobertura ≥80% obrigatória (R28/R44)
"""

import sys
import json
import subprocess
import tempfile
import os

sys.path.insert(0, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts")

from hefesto_motor import (
    load_inventory,
    list_cpu_slots,
    resolve_slot_for_role,
    execute_workflow,
    _evaluate_pillar,
    setup_logger
)


def run_motor(args: list) -> dict:
    """Executa o motor via CLI e retorna JSON parseado."""
    cmd = [sys.executable, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts/hefesto_motor.py"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        return {"error": result.stderr, "stdout": result.stdout}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "JSON inválido", "stdout": result.stdout}


class TestLoadInventory:
    """Testes para load_inventory()."""
    
    def test_inventory_exists(self):
        """Inventário deve existir e ser válido."""
        inv = load_inventory()
        assert "models" in inv
        assert isinstance(inv["models"], list)
        assert len(inv["models"]) > 0
    
    def test_inventory_schema_version(self):
        """Schema version deve ser 1."""
        inv = load_inventory()
        assert inv.get("schema_version") == 1


class TestListCpuSlots:
    """Testes para list_cpu_slots()."""
    
    def test_returns_list(self):
        """Deve retornar lista."""
        logger = setup_logger("/tmp/test_hefesto.log")
        slots = list_cpu_slots(logger)
        assert isinstance(slots, list)
    
    def test_all_slots_have_required_fields(self):
        """Cada slot deve ter campos obrigatórios."""
        logger = setup_logger("/tmp/test_hefesto.log")
        slots = list_cpu_slots(logger)
        for slot in slots:
            assert "id" in slot
            assert "port" in slot
            assert "params" in slot
            assert "ctx" in slot
            assert "temp" in slot
    
    def test_only_online_cpu_models(self):
        """Apenas modelos CPU online devem aparecer."""
        logger = setup_logger("/tmp/test_hefesto.log")
        slots = list_cpu_slots(logger)
        for slot in slots:
            # Verifica se existe no inventário com status online
            inv = load_inventory()
            found = False
            for m in inv["models"]:
                if m["id"] == slot["id"]:
                    assert m["status"] == "online"
                    assert m["sector"].startswith("CPU")
                    found = True
                    break
            assert found, f"Slot {slot['id']} não encontrado no inventário"


class TestResolveSlotForRole:
    """Testes para resolve_slot_for_role()."""
    
    def test_forja_resolves_ornith(self):
        """Role 'forja' deve resolver ornith (GPU)."""
        logger = setup_logger("/tmp/test_hefesto.log")
        slot = resolve_slot_for_role("forja", logger)
        assert slot is not None
        assert "ornith" in slot["id"].lower()
        assert slot["port"] == "8083"
        assert "baseURL" in slot
    
    def test_judge_resolves_bonsai(self):
        """Role 'judge' deve resolver bonsai/ternary."""
        logger = setup_logger("/tmp/test_hefesto.log")
        slot = resolve_slot_for_role("judge", logger)
        assert slot is not None
        # Pode ser ternary-bonsai-8b ou similar
        assert any(x in slot["id"].lower() for x in ["bonsai", "ternary", "judge"])
    
    def test_unknown_role_returns_none(self):
        """Role desconhecido deve retornar None."""
        logger = setup_logger("/tmp/test_hefesto.log")
        slot = resolve_slot_for_role("role_inexistente", logger)
        assert slot is None


class TestEvaluatePillar:
    """Testes para _evaluate_pillar() (antifraude)."""
    
    def test_with_evidence_returns_score(self):
        """Com evidência deve retornar score real."""
        logger = setup_logger("/tmp/test_hefesto.log")
        data = {"autophagy_score": 96.5}
        result = _evaluate_pillar("autophagy", data, logger)
        assert result["score"] == 96.5
        assert result["status"] == "validated_by_evidence"
    
    def test_without_evidence_returns_unknown(self):
        """Sem evidência deve retornar UNKNOWN + piso R34."""
        logger = setup_logger("/tmp/test_hefesto.log")
        data = {}
        result = _evaluate_pillar("autophagy", data, logger)
        assert result["score"] == 0.0000001  # Piso R34
        assert result["status"] == "UNKNOWN"
        assert "sem evidência" in result.get("note", "")
    
    def test_score_bounds_respected(self):
        """Score deve respeitar bounds 0.0000001–100."""
        logger = setup_logger("/tmp/test_hefesto.log")
        # Score válido
        data = {"autophagy_score": 50.0}
        result = _evaluate_pillar("autophagy", data, logger)
        assert 0.0000001 <= result["score"] <= 100
        
        # Score inválido (fora do range) → UNKNOWN
        data = {"autophagy_score": 150.0}
        result = _evaluate_pillar("autophagy", data, logger)
        assert result["status"] == "UNKNOWN"


class TestExecuteWorkflow:
    """Testes para execute_workflow()."""
    
    def test_with_evidence_terminates_loop(self):
        """Com evidência >95 deve terminar dev loop."""
        logger = setup_logger("/tmp/test_hefesto.log")
        payload = {
            "autophagy_score": 96.0,
            "decompilation_score": 97.0,
            "helenization_score": 95.5,
            "forging_score": 98.0
        }
        result = execute_workflow(payload, logger)
        assert result["average_score"] > 95.0
        assert result["dev_loop_terminated"] is True
        assert result["status"] == "OLYMPIAN_PERFECTION"
    
    def test_without_evidence_does_not_terminate(self):
        """Sem evidência não deve terminar dev loop."""
        logger = setup_logger("/tmp/test_hefesto.log")
        payload = {}
        result = execute_workflow(payload, logger)
        assert result["average_score"] == 0.0
        assert result["dev_loop_terminated"] is False
        assert result["status"] == "FREEZE_PAUSE_REQUIRED"
    
    def test_fallback_flag_logged(self):
        """Flag fallback_automatico deve ser registrada."""
        logger = setup_logger("/tmp/test_hefesto.log")
        payload = {"fallback_automatico": True}
        result = execute_workflow(payload, logger)
        assert result["fallback_triggered"] is True
    
    def test_active_model_included(self):
        """Modelo ativo deve ser incluído no resultado."""
        logger = setup_logger("/tmp/test_hefesto.log")
        payload = {"autophagy_score": 96.0}
        result = execute_workflow(payload, logger)
        assert "active_model" in result
        assert result["active_model"] is not None
        assert "id" in result["active_model"]


class TestCLI:
    """Testes de integração via CLI."""
    
    def test_list_cpu_cli(self):
        """CLI --list-cpu deve retornar JSON válido."""
        result = run_motor(["--list-cpu"])
        assert "error" not in result
        assert isinstance(result, list)
        assert len(result) > 0
    
    def test_resolve_forja_cli(self):
        """CLI --resolve forja deve retornar slot válido."""
        result = run_motor(["--resolve", "forja"])
        assert "error" not in result
        assert result is not None
        assert "ornith" in result["id"].lower()
    
    def test_execute_with_evidence_cli(self):
        """CLI --execute com evidência deve retornar OLYMPIAN_PERFECTION."""
        payload = json.dumps({
            "autophagy_score": 96.0,
            "decompilation_score": 97.0,
            "helenization_score": 95.5,
            "forging_score": 98.0
        })
        result = run_motor(["--execute", payload])
        assert "error" not in result
        assert result["status"] == "OLYMPIAN_PERFECTION"
        assert result["dev_loop_terminated"] is True
    
    def test_execute_without_evidence_cli(self):
        """CLI --execute sem evidência deve retornar FREEZE_PAUSE_REQUIRED."""
        result = run_motor(["--execute", "{}"])
        assert "error" not in result
        assert result["status"] == "FREEZE_PAUSE_REQUIRED"
        assert result["dev_loop_terminated"] is False


class TestAntiFraude:
    """Testes antifraude (herdados da auditoria ao original)."""
    
    def test_no_auto_approval_default_96_5(self):
        """NÃO deve haver auto-aprovação com default 96.5."""
        logger = setup_logger("/tmp/test_hefesto.log")
        # O original tinha base_score = 96.5 hardcoded
        # O helenizado deve exigir evidência explícita
        data = {}  # Sem score
        result = _evaluate_pillar("autophagy", data, logger)
        assert result["score"] == 0.0000001  # Piso, não 96.5
        assert result["status"] == "UNKNOWN"
    
    def test_scoring_range_r34(self):
        """Range de scoring deve ser 0.0000001–100 (R34)."""
        logger = setup_logger("/tmp/test_hefesto.log")
        # Score no piso
        data = {"autophagy_score": 0.0000001}
        result = _evaluate_pillar("autophagy", data, logger)
        assert result["score"] == 0.0000001
        
        # Score no teto
        data = {"autophagy_score": 100.0}
        result = _evaluate_pillar("autophagy", data, logger)
        assert result["score"] == 100.0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "--tb=short"])