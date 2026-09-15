"""Render HMI macro-regiões (Task 5.2) — texto/terminal.

Renderiza as macro-regiões agregadas + estado de ativação do event-loop em uma
tabela de texto (terminal), sem travar e sem dependência gráfica. Saída limitada:
resumo por região + top-N (nunca dump total — R22/constraint).

Sem dependências externas (stdlib apenas). Sem chamadas a LLMs.
"""

from __future__ import annotations

from typing import List, Sequence


def render_hmi(
    regions: Sequence[dict],
    total_neurons: int,
    total_spikes: int,
    top_n: int = 5,
) -> str:
    """Renderiza a tabela HMI em texto puro.

    Args:
        regions: lista de dicts `{name, n_neurons, spikes}` (saída do aggregate).
        total_neurons: N total do CSR (para a linha de rodapé).
        total_spikes: total de spikes do passo corrente.
        top_n: nº máximo de regiões exibidas no topo (limite de saída).

    Returns:
        String multi-linha com a tabela HMI (região, nº neurônios, spikes, taxa).
    """
    lines: List[str] = []
    lines.append("=" * 56)
    lines.append("HMI — Cérebro Simulado (macro-regiões)")
    lines.append("=" * 56)
    lines.append(f"{'região':<22} {'neurônios':>10} {'spikes':>8} {'taxa':>8}")
    lines.append("-" * 56)

    # Ordena por nº de neurônios decrescente (regiões maiores primeiro).
    ordered = sorted(regions, key=lambda r: r["n_neurons"], reverse=True)

    for r in ordered[:top_n]:
        n_neurons = r["n_neurons"]
        spikes = r["spikes"]
        # taxa = spikes por neurônio (evita divisão por zero).
        rate = (spikes / n_neurons) if n_neurons > 0 else 0.0
        lines.append(
            f"{r['name']:<22} {n_neurons:>10} {spikes:>8} {rate:>8.3f}"
        )

    lines.append("-" * 56)
    lines.append(f"total neurônios: {total_neurons}")
    lines.append(f"total spikes (passo): {total_spikes}")
    lines.append("=" * 56)
    return "\n".join(lines)