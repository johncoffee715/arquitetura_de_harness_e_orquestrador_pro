"""Event-loop SNN assíncrono (asyncio) — Task 3.2.

Consome o CSR do parser da Wave 1 (via import, NÃO duplica) e propaga spikes
com ordem determinística. Invariantes do esqueleto event_loop.rs:
  - Min-Heap de spikes futuros (heapq, O(log n) por push/pop).
  - Um passo = drenar spikes do timestep corrente → somar a v → disparos geram
    novos spikes com `time + delay`.
  - Ordem determinística: desempate por (time, target).

Sem dependências externas (stdlib apenas). Sem chamadas a LLMs.
"""

from __future__ import annotations

import asyncio
import heapq
from typing import List, Sequence, Tuple

from lif import LifNeuron


class SnnEventLoop:
    """Núcleo da simulação orientada a eventos sobre CSR."""

    def __init__(
        self,
        neurons: Sequence[LifNeuron],
        row_ptr: Sequence[int],
        col_idx: Sequence[int],
        weight: Sequence[int],
    ) -> None:
        self.neurons: List[LifNeuron] = list(neurons)
        self.row_ptr: List[int] = list(row_ptr)
        self.col_idx: List[int] = list(col_idx)
        self.weight: List[int] = list(weight)
        self.heap: List[Tuple[int, int, int]] = []  # (time, target, weight)
        self.now: int = 0
        self.spikes_this_step: int = 0

    def _out_neighbors(self, pre: int) -> List[Tuple[int, int]]:
        """Vizinhos pós-sinápticos de `pre` no CSR (ordenados por (pre, post))."""
        start = self.row_ptr[pre]
        end = self.row_ptr[pre + 1]
        return [(self.col_idx[i], self.weight[i]) for i in range(start, end)]

    def inject(self, target: int, weight: int) -> None:
        """Injeta um spike externo (estímulo sensorial) em `target`."""
        heapq.heappush(self.heap, (self.now, target, weight))

    def step(self) -> int:
        """Avança um timestep: entrega spikes agendados, propaga disparos.

        Retorna o nº de spikes entregues neste passo.
        """
        delivered = 0
        self.now += 1

        # 1) Drenar eventos do timestep corrente, acumulando disparos.
        fired: List[int] = []
        while self.heap and self.heap[0][0] <= self.now:
            time, target, w = heapq.heappop(self.heap)
            delivered += 1
            if self.neurons[target].receive(w):
                fired.append(target)

        # 2) Propagar disparos acumulados (ordem determinística por target).
        for source in sorted(fired):
            self._propagate(source)

        # 3) Decaimento passivo (leak) de todos os neurônios.
        for n in self.neurons:
            n.decay()

        self.spikes_this_step = delivered
        return delivered

    def _propagate(self, source: int) -> None:
        """Propaga o disparo de `source` aos vizinhos, empilhando no heap."""
        delay = self.neurons[source].delay
        time = self.now + delay
        for target, w in self._out_neighbors(source):
            heapq.heappush(self.heap, (time, target, w))


async def run_simulation(loop: SnnEventLoop, steps: int) -> int:
    """Executa `steps` passos de simulação de forma assíncrona (sem bloquear).

    Retorna o total de spikes entregues ao longo da simulação.
    """
    total = 0
    for _ in range(steps):
        # cede controle ao event-loop asyncio a cada passo (não bloqueia)
        await asyncio.sleep(0)
        total += loop.step()
    return total