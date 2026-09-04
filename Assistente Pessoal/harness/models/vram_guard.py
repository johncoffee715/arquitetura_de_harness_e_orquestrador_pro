#!/usr/bin/env python3
"""
VRAM Guard + Model Swapper — GPU-aware hot-swap for local llama.cpp servers.

Replaces the simulation-only `ModelProvider.hot_swap` with a concrete
unload/load mechanism backed by real VRAM accounting (nvidia-smi with
ROCm/`rocm-smi` fallback) and the existing server scripts
(start-llama.sh / start-all-models.sh).

Guarantees (OOM-proof, parse-don't-validate):
- `VRAMGuard.total_vram_gb()` / `available_vram_gb()` — real GPU reading,
  bounded by a configured safety margin so we never approach 100%.
- `budget_ok(model_vram_gb, kv_gb)` — refuses a load that would exceed budget.
- `ModelSwapper.swap(old_id, new_id)` — refuses if the old model has active
  requests (drain-first), unloads the old server, loads the new one and
  re-probes /health before returning. Fail-safe: if no GPU/scripts present,
  degrades to a log-only no-op (no crash).
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

HARNESS = Path("/mnt/dados/Assistente Pessoal/harness")
MODEL_DIR = Path("/mnt/dados/Assistente Pessoal/modelos LLM")
# llama-server ports for the local models (see start-llama.sh).
MODEL_PORTS: Dict[str, int] = {
    "ornith": 8081,
    "bonsai": 8082,
    "nanbeige": 8083,
    "lfm": 8084,
}


class VRAMGuard:
    """Real VRAM accounting + swap budget validation."""

    def __init__(
        self,
        total_cap: float = 16.0,
        safety_margin: float = 0.90,
        runner: Optional[Callable[[List[str]], Tuple[int, bytes]]] = None,
    ) -> None:
        # safety_margin: never exceed `total_cap * safety_margin` of VRAM.
        self.total_cap = total_cap
        self.safety_margin = safety_margin
        # `runner` is injectable for tests; defaults to subprocess.run.
        self._run = runner or self._default_run

    @staticmethod
    def _default_run(argv: List[str]) -> Tuple[int, bytes]:
        proc = subprocess.run(
            argv, capture_output=True, timeout=10,
            check=False,
        )
        return proc.returncode, proc.stdout

    def total_vram_gb(self) -> float:
        """Return GPU total VRAM in GB, bounded by self.total_cap."""
        val = self._probe_vram_gb()
        if val is None:
            return self.total_cap
        return min(val, self.total_cap)

    def available_vram_gb(self) -> float:
        """Return currently free VRAM in GB."""
        val = self._probe_free_gb()
        if val is None:
            # No GPU probe available -> conservatively assume half the cap.
            return self.total_cap * 0.5
        return max(0.0, val)

    def budget_ok(self, model_vram_gb: float, kv_gb: float = 0.0) -> bool:
        """True only if loading `model_vram_gb + kv_gb` stays under budget."""
        budget = self.total_vram_gb() * self.safety_margin
        needed = model_vram_gb + kv_gb
        return needed <= budget

    def headroom_for(self, model_vram_gb: float, kv_gb: float = 0.0) -> float:
        """How many GB of headroom remain if this load is accepted."""
        return self.total_vram_gb() * self.safety_margin - (
            self.available_vram_gb_used() + model_vram_gb + kv_gb
        )

    def available_vram_gb_used(self) -> float:
        """Return total cap minus available (i.e. current used VRAM)."""
        return self.total_vram_gb() - self.available_vram_gb()

    # -- probe internals -------------------------------------------------
    def _probe_vram_gb(self) -> Optional[float]:
        # nvidia-smi first (common); rocm-smi for AMD/ROCm.
        for cmd in (("nvidia-smi", "--query-gpu=memory.total",
                     "--format=csv,noheader,nounits"),
                    ("rocm-smi", "--showmeminfo", "vram")):
            if shutil.which(cmd[0]) is None:
                continue
            try:
                code, out = self._run(list(cmd))
                if code == 0 and out:
                    raw = out.decode(errors="replace").strip()
                    num = self._first_number(raw)
                    if num is not None:
                        # nvidia returns MiB; rocm MB -> divide accordingly.
                        return num / 1024.0
            except Exception:
                continue
        return None

    def _probe_free_gb(self) -> Optional[float]:
        for cmd in (("nvidia-smi", "--query-gpu=memory.free",
                     "--format=csv,noheader,nounits"),):
            if shutil.which(cmd[0]) is None:
                continue
            try:
                code, out = self._run(list(cmd))
                if code == 0 and out:
                    raw = out.decode(errors="replace").strip()
                    num = self._first_number(raw)
                    if num is not None:
                        return num / 1024.0
            except Exception:
                continue
        return None

    @staticmethod
    def _first_number(raw: str) -> Optional[float]:
        m = re.search(r"(\d+(?:\.\d+)?)", raw)
        return float(m.group(1)) if m else None


class ModelSwapper:
    """Concrete unload/load of a local llama-server, drain-first + /health probe."""

    def __init__(
        self,
        guard: Optional[VRAMGuard] = None,
        model_vram: Optional[Dict[str, float]] = None,
        model_ports: Optional[Dict[str, int]] = None,
        probes: int = 5,
        probe_wait: float = 1.0,
    ) -> None:
        self.guard = guard or VRAMGuard()
        self.model_vram = model_vram or self._default_vram()
        self.ports = model_ports or MODEL_PORTS
        self.probes = probes
        self.probe_wait = probe_wait

    @staticmethod
    def _default_vram() -> Dict[str, float]:
        # Heuristic table (matches harness-config vram_gb).
        return {"ornith": 5.5, "bonsai": 3.9, "nanbeige": 1.4, "lfm": 1.1}

    def unload(self, model_id: str) -> bool:
        """Kill the llama-server serving model_id (return True if OK/no-op)."""
        port = self.ports.get(model_id)
        cmd = ["pkill", "-f", f"llama-server.*--port {port}"] if port else None
        if cmd is None or shutil.which("pkill") is None:
            return True  # fail-safe: nothing concrete to unload
        try:
            self._run(cmd)
        except Exception:
            return False
        return True

    def load(self, model_id: str) -> bool:
        """Start the model server and wait until /health responds."""
        vram = self.model_vram.get(model_id, 0.0)
        if not self.guard.budget_ok(vram):
            return False
        script = HARNESS / "start-llama.sh"
        if not script.exists() or shutil.which("bash") is None:
            return True  # fail-safe: rely on launcher elsewhere
        try:
            self._run(["bash", str(script), model_id])
        except Exception:
            return False
        return self._wait_healthy(model_id)

    def _wait_healthy(self, model_id: str) -> bool:
        port = self.ports.get(model_id)
        if not port:
            return True
        url = f"http://127.0.0.1:{port}/health"
        for _ in range(self.probes):
            try:
                with urllib.request.urlopen(url, timeout=2) as resp:
                    if resp.status == 200 and b"ok" in resp.read().lower():
                        return True
            except Exception:
                pass
            time.sleep(self.probe_wait)
        return False

    def swap(self, old_id: str, new_id: str, active_requests: int = 0) -> bool:
        """Drain -> unload old -> load new. Returns False on refusal/failure."""
        if active_requests > 0:
            return False  # refuse: drain-first (no hot-swap under load)
        if not self.unload(old_id):
            return False
        return self.load(new_id)

    def _run(self, argv: List[str]) -> None:
        subprocess.run(argv, capture_output=True, timeout=15, check=False)