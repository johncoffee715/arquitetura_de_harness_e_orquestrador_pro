"""Teste do pin condicional (Task 6.3) — RED→GREEN.

Valida o gate: pin é no-op quando health check está ausente/ambíguo/offline,
e aplica afinidade real no próprio processo de teste com restore garantido.
"""

import os
import pytest

from pin import pin_if_healthy, current_affinity


def _health(online=True, ambiguous=False, device="cpu"):
    """Constrói um mapa de health sintético para os testes."""
    if ambiguous:
        # Divergência: dois slots reportam devices diferentes para o mesmo papel.
        return {
            "9086": {"online": True, "device_cpu_gpu": "cpu", "ngl": 0},
            "9090": {"online": True, "device_cpu_gpu": "gpu", "ngl": 999},
            "9092": {"online": True, "device_cpu_gpu": "cpu", "ngl": 0},
        }
    if not online:
        return {
            "9086": {"online": False, "device_cpu_gpu": None, "ngl": None},
            "9090": {"online": False, "device_cpu_gpu": None, "ngl": None},
            "9092": {"online": False, "device_cpu_gpu": None, "ngl": None},
        }
    return {
        "9086": {"online": True, "device_cpu_gpu": device, "ngl": 0},
        "9090": {"online": True, "device_cpu_gpu": device, "ngl": 0},
        "9092": {"online": True, "device_cpu_gpu": device, "ngl": 0},
    }


def test_pin_noop_sem_health():
    """Pin é no-op quando health está ausente (None)."""
    result = pin_if_healthy(None, cpus=[0, 1])
    assert result["pinned"] is False
    assert "motivo" in result


def test_pin_noop_health_ambiguo():
    """Pin é no-op quando health é ambíguo (devices divergentes)."""
    result = pin_if_healthy(_health(ambiguous=True), cpus=[0, 1])
    assert result["pinned"] is False
    assert "motivo" in result


def test_pin_noop_health_offline():
    """Pin é no-op quando todos os slots estão offline."""
    result = pin_if_healthy(_health(online=False), cpus=[0, 1])
    assert result["pinned"] is False
    assert "motivo" in result


def test_pin_noop_health_vazio():
    """Pin é no-op quando health é um mapa vazio."""
    result = pin_if_healthy({}, cpus=[0, 1])
    assert result["pinned"] is False
    assert "motivo" in result


def test_pin_real_aplicado_com_restore():
    """Pin real aplica afinidade no próprio processo e restaura em finally."""
    original = current_affinity()
    assert original is not None and len(original) > 0

    # Escolhe um subconjunto de CPUs disponíveis (mínimo 1).
    cpus = original[:1] if len(original) >= 1 else original

    try:
        result = pin_if_healthy(_health(), cpus=cpus)
        assert result["pinned"] is True
        # Afinidade atual deve ser subconjunto do pedido.
        after = current_affinity()
        assert set(after).issubset(set(cpus))
    finally:
        # Restore garantido da afinidade original.
        os.sched_setaffinity(0, original)
        restored = current_affinity()
        assert set(restored) == set(original)