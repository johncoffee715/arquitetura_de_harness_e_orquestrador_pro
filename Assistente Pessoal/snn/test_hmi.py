"""Teste da HMI macro-regiões (Task 5.3) — RED→GREEN.

Valida a estrutura da saída (não pixel): agregação produz ≤ N regiões com soma
de neurônios == N do CSR, e a HMI renderiza sem travar com contagens corretas.

Depende de: snn/aggregate.py (agregação) e snn/hmi.py (render).
Fontes de dados: snn/parser.py (Csr) e snn/event_loop.py (SnnEventLoop).
"""

from __future__ import annotations

import pytest

from aggregate import aggregate_regions, DEFAULT_REGIONS
from hmi import render_hmi
from parser import Csr


def _sample_csr() -> Csr:
    """CSR pequeno e determinístico (N=6) para exercitar a agregação."""
    # row_ptr/col_idx/weight consistentes com a fixture da Wave 1.
    return Csr(
        row_ptr=[0, 2, 3, 5, 5, 6, 6],
        col_idx=[1, 2, 3, 3, 4, 5],
        weight=[5, 1, 4, 2, 1, 7],
    )


def _sample_loop() -> "SnnEventLoop":
    """Event-loop com 6 neurônios LIF e alguns spikes acumulados."""
    from event_loop import SnnEventLoop
    from lif import LifNeuron

    neurons = [LifNeuron() for _ in range(6)]
    loop = SnnEventLoop(
        neurons=neurons,
        row_ptr=[0, 2, 3, 5, 5, 6, 6],
        col_idx=[1, 2, 3, 3, 4, 5],
        weight=[5, 1, 4, 2, 1, 7],
    )
    loop.spikes_this_step = 3
    return loop


def test_aggregate_produces_at_most_n_regions():
    """Agregação produz ≤ N regiões (nunca um nó por neurônio — R22)."""
    csr = _sample_csr()
    regions = aggregate_regions(csr, n_regions=4)
    assert len(regions) <= 4
    assert len(regions) >= 1


def test_aggregate_neuron_sum_equals_n():
    """Soma dos neurônios por região == N do CSR (partição completa)."""
    csr = _sample_csr()
    regions = aggregate_regions(csr, n_regions=4)
    total = sum(r["n_neurons"] for r in regions)
    assert total == csr.n


def test_aggregate_default_regions_named():
    """Default usa as 4 macro-regiões HMI do vault (nomes esperados)."""
    csr = _sample_csr()
    regions = aggregate_regions(csr)
    names = [r["name"] for r in regions]
    assert names == DEFAULT_REGIONS


def test_aggregate_spike_sum_consistent():
    """Soma de spikes por região == total de spikes do event-loop."""
    csr = _sample_csr()
    loop = _sample_loop()
    regions = aggregate_regions(csr, n_regions=4, loop=loop)
    total = sum(r["spikes"] for r in regions)
    assert total == loop.spikes_this_step


def test_hmi_renders_regions_and_counts():
    """HMI renderiza regiões esperadas + contagem correta, sem travar."""
    csr = _sample_csr()
    loop = _sample_loop()
    regions = aggregate_regions(csr, n_regions=4, loop=loop)
    out = render_hmi(regions, total_neurons=csr.n, total_spikes=loop.spikes_this_step)
    assert isinstance(out, str)
    assert len(out) > 0
    # contém os nomes das regiões esperadas
    for name in DEFAULT_REGIONS:
        assert name in out
    # contém a contagem total de neurônios
    assert str(csr.n) in out