#!/usr/bin/env python3
"""TDD tests for harness/models/vram_guard.py (P1 — VRAM hot-swap real)."""

import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.models.vram_guard import VRAMGuard, ModelSwapper


def _runner(responses):
    """Return a fake `runner` (argv -> (code, bytes)) from a response table."""
    calls = []

    def runner(argv):
        calls.append(argv)
        key = argv[0] + " " + argv[-1] if argv else ""
        for prefix, (code, out) in responses.items():
            if argv and argv[0] in prefix.split():
                return code, out
        return responses.get("default", (1, b""))

    runner.calls = calls
    return runner


class VRAMGuardTest(unittest.TestCase):
    def setUp(self):
        self.which = mock.patch(
            "harness.models.vram_guard.shutil.which",
            return_value="/usr/bin/nvidia-smi",
        )
        self.which.start()
        self.addCleanup(self.which.stop)

    def test_parse_nvidia_mib_total(self):
        fake = _runner({"nvidia-smi": (0, b"16384\n")})
        guard = VRAMGuard(total_cap=16.0, runner=fake)
        # 16384 MiB / 1024 = 16 GB
        self.assertAlmostEqual(guard.total_vram_gb(), 16.0)
        self.assertAlmostEqual(guard.available_vram_gb(), 16.0)

    def test_budget_ok_blocks_overload(self):
        fake = _runner({"nvidia-smi": (0, b"16384\n")})
        guard = VRAMGuard(total_cap=16.0, runner=fake)
        # budget = 16*0.90 = 14.4 GB -> loading a 16GB model must be refused
        self.assertFalse(guard.budget_ok(16.0))
        self.assertTrue(guard.budget_ok(5.5))
        # 3.9 + kv 9.0 = 12.9 < 14.4 -> OK
        self.assertTrue(guard.budget_ok(3.9, kv_gb=9.0))
        # 3.9 + kv 11.0 = 14.9 > 14.4 -> refused
        self.assertFalse(guard.budget_ok(3.9, kv_gb=11.0))

    def test_no_gpu_falls_back_conservative(self):
        # No GPU probe available -> total_cap, avail=half. Simulate by making
        # every runner invocation fail (returncode 1), independent of host GPU.
        fake = _runner({"default": (1, b"")})
        guard = VRAMGuard(total_cap=16.0, runner=fake)
        self.assertEqual(guard.total_vram_gb(), 16.0)
        self.assertAlmostEqual(guard.available_vram_gb(), 8.0)

    def test_unicode_garbage_parsed(self):
        # Adversarial: probe returns noise with a number.
        fake = _runner({"nvidia-smi": (0, b"total 16384 MiB (gpu_id=0)\n")})
        guard = VRAMGuard(total_cap=32.0, runner=fake)
        self.assertAlmostEqual(guard.total_vram_gb(), 16.0)


class ModelSwapperTest(unittest.TestCase):
    def setUp(self):
        self.port_patch = mock.patch("harness.models.vram_guard.shutil.which",
                                     return_value="/usr/bin/bash")
        self.pkill = self.port_patch.start()
        self.addCleanup(self.port_patch.stop)

    def test_swap_refuses_under_load(self):
        guard = VRAMGuard(total_cap=16.0)
        swapper = ModelSwapper(guard=guard)
        self.assertFalse(swapper.swap("ornith", "bonsai", active_requests=3))

    def test_unload_no_pkill_is_failsafe_ok(self):
        with mock.patch("harness.models.vram_guard.shutil.which",
                        return_value=None):
            guard = VRAMGuard(total_cap=16.0)
            swapper = ModelSwapper(guard=guard)
            # No pkill binary -> no-op OK (never crashes)
            self.assertTrue(swapper.unload("ornith"))

    def test_load_refused_when_over_budget(self):
        fake = _runner({"nvidia-smi": (0, b"16384\n")})
        guard = VRAMGuard(total_cap=6.0, runner=fake)  # tiny card (5.4 budget)
        swapper = ModelSwapper(guard=guard)
        # ornith needs 5.5 > 6*0.90=5.4 -> refused
        with mock.patch("harness.models.vram_guard.shutil.which",
                        return_value="/usr/bin/bash"), \
             mock.patch("harness.models.vram_guard.HARNESS") as hp:
            hp.join.return_value = __file__  # pretend script exists is not needed (refused before)
            self.assertFalse(swapper.load("ornith"))

    def test_swap_full_path_with_health(self):
        fake = _runner({"nvidia-smi": (0, b"16384\n")})
        guard = VRAMGuard(total_cap=16.0, runner=fake)
        swapper = ModelSwapper(guard=guard, probes=1, probe_wait=0)
        script = mock.MagicMock()
        script.exists.return_value = True
        with mock.patch("harness.models.vram_guard.shutil.which",
                        return_value="/usr/bin/bash"), \
             mock.patch("harness.models.vram_guard.HARNESS", script), \
             mock.patch("harness.models.vram_guard.subprocess.run") as run, \
             mock.patch("harness.models.vram_guard.urllib.request.urlopen") as urlopen:
            class Resp:
                status = 200
                def read(self):
                    return b"ok"
            urlopen.return_value.__enter__.return_value = Resp()
            # unload -> pkill ok (no-op), load -> /health ok
            self.assertTrue(swapper.swap("ornith", "bonsai", active_requests=0))
            self.assertTrue(run.called)


if __name__ == "__main__":
    unittest.main()