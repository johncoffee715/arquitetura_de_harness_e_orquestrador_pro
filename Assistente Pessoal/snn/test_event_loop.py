"""Teste de integração LIF + event-loop (Task 3.3).

Valida que um spike propaga de A→B com latência esperada, usando a fixture
`mini_edges.csv` local (parser CSR — fonte única `snn/parser.py`). Latência
determinística: delay axonal fixo por neurônio, sem aleatoriedade.
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lif import LifNeuron
from event_loop import SnnEventLoop, run_simulation
from parser import parse_csv_to_csr


def _mini_edges_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "mini_edges.csv")


def test_lif_fires_above_threshold_and_resets():
    """LIF dispara acima do threshold e reseta abaixo (Task 3.1)."""
    n = LifNeuron(v=0.0, threshold=1.0, reset=0.0, leak=0.0, delay=1)
    assert not n.receive(0)          # v=0 < 1 → não dispara
    assert n.receive(2)              # v=2 >= 1 → dispara
    assert n.v == 0.0                # reset pós-disparo


def test_spike_propagates_a_to_b_with_expected_latency():
    """Integração: spike A→B com latência esperada (Task 3.3).

    Fixture mini_edges.csv topologia: 0→1(w2), 0→2(w1), 1→2(w3), 2→0(w1), 2→3(w4).
    A = neurônio 0, B = neurônio 1. A dispara ao receber peso 2 (threshold 1.0)
    e propaga a B com delay=1 timestep → latência determinística = 1.
    """
    row_ptr, col_idx, weight = parse_csv_to_csr(_mini_edges_path())

    # delay axonal uniforme = 1 timestep → latência determinística
    neurons = [LifNeuron(v=0.0, threshold=1.0, reset=0.0, leak=0.0, delay=1)
               for _ in range(len(row_ptr) - 1)]

    loop = SnnEventLoop(neurons, row_ptr, col_idx, weight)

    # injeta spike externo em A (neurônio 0) com peso 2 → dispara no passo 1
    loop.inject(0, 2)

    # passo 1: A recebe spike, dispara, agenda spikes p/ vizinhos (1 e 2)
    delivered = loop.step()
    assert delivered == 1, f"passo 1 deve entregar 1 spike, entregou {delivered}"
    assert neurons[0].v == 0.0, "A deve ter disparado e resetado"

    # passo 2: B (neurônio 1) recebe o spike propagado de A (latência = delay = 1)
    delivered = loop.step()
    # A tem 2 arestas de saída (0→1 e 0→2) → 2 spikes entregues no passo 2
    assert delivered == 2, f"passo 2 deve entregar 2 spikes (A→B e A→C), entregou {delivered}"

    # B acumulou o peso da aresta 0→1 (=2) → disparou e resetou
    assert neurons[1].v == 0.0, f"B deve ter disparado e resetado, v={neurons[1].v}"


def test_run_simulation_async_returns_spike_count():
    """Event-loop assíncrono processa N passos sem deadlock, ordem determinística."""
    row_ptr, col_idx, weight = parse_csv_to_csr(_mini_edges_path())
    neurons = [LifNeuron(v=0.0, threshold=1.0, reset=0.0, leak=0.0, delay=1)
               for _ in range(len(row_ptr) - 1)]
    loop = SnnEventLoop(neurons, row_ptr, col_idx, weight)
    loop.inject(0, 2)

    total = asyncio.run(run_simulation(loop, steps=3))
    # passo1: 1 spike (A dispara), passo2: 2 spikes (A→B, A→C), passo3: 3 spikes
    # (B→2, C→0, C→3) — cadeia determinística da topologia da fixture.
    assert total == 6, f"total de spikes entregues deve ser 6, foi {total}"