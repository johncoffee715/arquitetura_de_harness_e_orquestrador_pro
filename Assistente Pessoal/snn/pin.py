"""Pin de threads condicional (Task 6.2).

`pin_if_healthy(health, cpus)` afina SOMENTE o PRÓPRIO processo
(os.sched_setaffinity no PID atual) e SOMENTE se health for válido e
não-ambíguo. Caso contrário, no-op retornando {pinned: False, motivo}.

INVARIANTE DE SEGURANÇA (nao_fazer):
  - NUNCA toca em outros PIDs (sem taskset/pkill em processos externos).
  - NUNCA inicia/para/mata llama-server.
  - Apenas os.sched_setaffinity(0, ...) no processo corrente.
"""

from __future__ import annotations

import os

from health_check import is_healthy


def current_affinity() -> list[int] | None:
    """Lê a afinidade de CPU do processo atual. None se não suportado."""
    try:
        return sorted(os.sched_getaffinity(0))
    except (OSError, AttributeError):
        return None


def pin_if_healthy(health: dict | None, cpus: list[int]) -> dict:
    """Aplica afinidade de CPU ao processo atual SE health válido e não-ambíguo.

    Args:
        health: mapa {slot: {online, device_cpu_gpu, ngl}} de health_check.
        cpus: lista de CPUs (núcleos) para afinar o processo atual.

    Returns:
        {"pinned": bool, "motivo": str} — pinned True só se afinidade aplicada.
    """
    if not is_healthy(health):
        return {"pinned": False, "motivo": "health ausente/ambíguo/offline"}

    if not cpus:
        return {"pinned": False, "motivo": "lista de cpus vazia"}

    try:
        os.sched_setaffinity(0, cpus)
    except (OSError, ValueError) as exc:
        return {"pinned": False, "motivo": f"setaffinity falhou: {exc}"}

    # Verifica que a afinidade foi de fato aplicada.
    after = current_affinity()
    if after is None or not set(after).issubset(set(cpus)):
        return {"pinned": False, "motivo": "afinidade nao confirmada"}

    return {"pinned": True, "motivo": "afinidade aplicada ao processo atual"}