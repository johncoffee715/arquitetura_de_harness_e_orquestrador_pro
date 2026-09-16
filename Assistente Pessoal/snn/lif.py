"""Neurônio LIF (Leaky Integrate-and-Fire) — núcleo puro, sem I/O (Task 3.1).

Invariantes (espelhadas do esqueleto event_loop.rs):
  - `receive(w)` soma o peso à membrana; se v >= threshold, dispara e reseta.
  - `decay()` aplica leak passivo (v *= 1 - leak), chamado 1x por timestep.
  - `delay` = atraso axonal (em timesteps) antes do spike chegar ao pós-sináptico.

Sem dependências externas (stdlib apenas). Sem chamadas a LLMs.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LifNeuron:
    """Neurônio LIF com membrana, leak, threshold, reset e delay axonal."""

    v: float = 0.0          # potencial de membrana atual
    threshold: float = 1.0  # limiar de disparo
    reset: float = 0.0      # reset pós-disparo
    leak: float = 0.0       # decaimento por timestep (0.0 = sem leak)
    delay: int = 1          # atraso axonal em timesteps
    fired_count: int = 0    # contagem nativa de disparos (B5: sem monkey-patch)

    def receive(self, w: float) -> bool:
        """Aplica spike de entrada (peso) e retorna True se disparou."""
        self.v += w
        if self.v >= self.threshold:
            self.v = self.reset
            self.fired_count += 1
            return True
        return False

    def decay(self) -> None:
        """Decaimento passivo (leak) — chamado 1x por timestep."""
        self.v *= 1.0 - self.leak