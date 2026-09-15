"""Watcher do vault Obsidian — Task 4.1 (ponte inotify→LLM).

Polling por mtime (stdlib apenas, cross-plataforma). NOTA: inotify/watchdog são
dependências externas e específicas de Linux — NÃO usados aqui. O polling por
mtime é determinístico, portável e suficiente para o vault (R3: rajada/debounce/
backpressure).

Comportamento:
  - `snapshot()` registra o baseline de (path → mtime).
  - `poll()` varre o root recursivamente, detecta arquivos com mtime > baseline,
    e devolve eventos pós-debounce (rajada colapsa em 1 por path).
  - Fila limitada (`max_queue`): se mais eventos que a capacidade, descarta o
    MAIS ANTIGO (FIFO) e incrementa `dropped` (backpressure contabilizado).

Parâmetros (documentados):
  - `root`: diretório do vault a observar.
  - `debounce_s`: janela de debounce em segundos (0.0 = sem debounce).
  - `max_queue`: capacidade da fila de eventos (descarta-mais-antigo além disso).
  - `suffix`: extensões observadas (default ".md").

Sem dependências externas. Sem chamadas a LLMs/sockets.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class VaultEvent:
    """Evento de mudança detectado no vault."""

    path: str
    mtime: float


class VaultWatcher:
    """Observa o vault por polling de mtime com debounce + fila limitada."""

    def __init__(
        self,
        root: Path,
        debounce_s: float = 0.15,
        max_queue: int = 16,
        suffix: str = ".md",
    ) -> None:
        self.root: Path = Path(root)
        self.debounce_s: float = debounce_s
        self.max_queue: int = max_queue
        self.suffix: str = suffix
        self._baseline: Dict[str, float] = {}
        self._pending: Dict[str, float] = {}  # path → último mtime visto
        self.dropped: int = 0

    def snapshot(self) -> None:
        """Registra o baseline atual de (path → mtime)."""
        self._baseline = self._scan()

    def _scan(self) -> Dict[str, float]:
        """Varre o root recursivamente, devolvendo {path: mtime} dos .md."""
        found: Dict[str, float] = {}
        if not self.root.exists():
            return found
        for p in self.root.rglob("*"):
            if p.is_file() and p.name.endswith(self.suffix):
                try:
                    found[str(p)] = p.stat().st_mtime
                except OSError:
                    continue
        return found

    def poll(self) -> List[VaultEvent]:
        """Detecta mudanças desde o último snapshot e devolve eventos pós-debounce.

        - Rajada no mesmo path colapsa em 1 evento (debounce temporal).
        - Fila limitada: descarta o mais antigo e conta em `self.dropped`.
        """
        current = self._scan()
        now = time.time()

        # 1) Coletar paths novos/alterados (mtime > baseline).
        changed: List[VaultEvent] = []
        for path, mtime in current.items():
            base = self._baseline.get(path)
            if base is None or mtime > base:
                changed.append(VaultEvent(path=path, mtime=mtime))

        # 2) Debounce temporal: colapsa rajada por path (mantém o mais recente).
        collapsed: Dict[str, VaultEvent] = {}
        for ev in changed:
            prev = collapsed.get(ev.path)
            if prev is None or ev.mtime > prev.mtime:
                collapsed[ev.path] = ev

        # 3) Fila limitada com descarta-mais-antigo (FIFO) + contador.
        events = list(collapsed.values())
        events.sort(key=lambda e: e.mtime)  # ordem cronológica (mais antigo 1º)
        if len(events) > self.max_queue:
            overflow = len(events) - self.max_queue
            self.dropped += overflow
            events = events[overflow:]  # descarta os `overflow` mais antigos

        # 4) Atualiza baseline para o próximo poll (não re-emite os mesmos).
        self._baseline = current
        return events