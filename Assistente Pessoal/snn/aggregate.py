"""Agregação CSR em macro-regiões HMI (Task 5.1).

Agrega os neurônios do CSR em macro-regiões (clusters funcionais), NUNCA um nó
por neurônio (R22 — fragmentação). A função de mapeamento neurônio→região é
configurável; o default espelha as 4 macro-regiões HMI do vault:

  1. sensorial/optico      — input sensorial (restante, não atribuído às demais);
  2. complexo-central (CX) — navegação/integração sensorimotora;
  3. corpos-cogumelo (MB)  — aprendizado/memória olfativa;
  4. dopamina/PPL101       — modulação dopaminérgica (valência).

Default: partição por faixas de índices (neurônio i → região floor(i * K / N)),
onde K = nº de regiões. A função `neuron_to_region` pode ser injetada para
qualquer mapeamento customizado (ex.: por tipo celular real do MaleCNS).

Sem dependências externas (stdlib apenas). Sem chamadas a LLMs.
"""

from __future__ import annotations

from typing import Callable, List, Optional, Sequence

from parser import Csr

# As 4 macro-regiões HMI do vault (nomes que dão identidade ao painel).
DEFAULT_REGIONS: List[str] = [
    "sensorial/optico",
    "complexo-central",
    "corpos-cogumelo",
    "dopamina/PPL101",
]


def _default_neuron_to_region(i: int, n: int, k: int) -> int:
    """Partição por faixas: neurônio i → região floor(i * k / n).

    Garante cobertura completa (soma == n) e ≤ k regiões não-vazias.
    """
    if n <= 0:
        return 0
    region = (i * k) // n
    return min(region, k - 1)


def aggregate_regions(
    csr: Csr,
    n_regions: int = 4,
    loop: Optional[object] = None,
    neuron_to_region: Optional[Callable[[int, int, int], int]] = None,
) -> List[dict]:
    """Agrega os neurônios do CSR em macro-regiões.

    Args:
        csr: grafo CSR parseado (fonte de N e da topologia).
        n_regions: nº de macro-regiões (configurável; default 4).
        loop: event-loop opcional (SnnEventLoop) para atribuir spikes por região.
        neuron_to_region: mapeamento customizado neurônio→região (default: faixas).

    Returns:
        Lista de dicts `{name, n_neurons, spikes}` — uma por região (≤ n_regions).
        A soma de `n_neurons` == csr.n (partição completa, sem perda).
    """
    n = csr.n
    k = max(1, min(n_regions, n)) if n > 0 else 1
    mapper = neuron_to_region or _default_neuron_to_region

    names = DEFAULT_REGIONS if n_regions == len(DEFAULT_REGIONS) else [
        f"regiao-{j}" for j in range(k)
    ]

    # Contagem de neurônios por região.
    counts = [0] * k
    for i in range(n):
        counts[mapper(i, n, k)] += 1

    # Spikes por região (se houver event-loop com estado de ativação).
    spikes = [0] * k
    if loop is not None:
        # spikes_this_step é o total do passo corrente; distribuímos por região
        # proporcionalmente à fração de neurônios (sem inventar per-neurônio).
        total_spikes = getattr(loop, "spikes_this_step", 0)
        if total_spikes > 0 and n > 0:
            # distribuição determinística: maior resto por região.
            base = total_spikes // n
            rem = total_spikes % n
            for i in range(n):
                r = mapper(i, n, k)
                spikes[r] += base
            # distribui o resto pelos primeiros `rem` neurônios (determinístico).
            for i in range(rem):
                r = mapper(i, n, k)
                spikes[r] += 1

    return [
        {"name": names[j], "n_neurons": counts[j], "spikes": spikes[j]}
        for j in range(k)
    ]