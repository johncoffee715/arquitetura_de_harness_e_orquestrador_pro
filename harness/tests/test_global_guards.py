"""Tests locking the anti-stall guard and the inter-resource brainstorm.

Guarantees the "impossible to recur" invariant:
  - guarded_resolve NEVER returns a binding to a dead backend; it raises
    StallGuardError FAST (fail-fast) instead of hanging on a silent stall.
  - the watchdog reports readiness truthfully.
  - the brainstorm board produces clean structured turns.

Uses tempfile configs and dead localhost ports, no network.
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from harness.models.model_inheritance import ModelInheritance, StallGuardError
from harness.safety.stall_watchdog import StallWatchdog
from harness.a2a.brainstorm import BrainstormBoard
from harness.safety.self_heal import LocalStackHealer, LOCAL_BACKENDS


DEAD_CFG = {
    "harness": {
        "model_inheritance": {
            "backends": {
                "dead-a": {"base_url": "http://127.0.0.1:9", "kind": "local", "priority": 1},
                "dead-b": {"base_url": "http://127.0.0.1:9", "kind": "gateway", "priority": 2},
            },
            "defaults": {"subagent": "dead-a"},
            "overrides": {},
        }
    }
}


def dead_compactor():
    tmp = Path(tempfile.mkdtemp(prefix="mi_test_"))
    cfg = tmp / "h.json"
    cfg.write_text(json.dumps(DEAD_CFG), encoding="utf-8")
    mi = ModelInheritance(project_root=str(tmp), config_path=str(cfg), health_timeout=1.0)
    return mi, tmp


class StallGuardTests(unittest.TestCase):
    def test_guarded_resolve_all_dead_raises_fast(self):
        mi, tmp = dead_compactor()
        try:
            with self.assertRaises(StallGuardError):
                mi.guarded_resolve("qualquer-recurso", "subagent")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_guarded_resolve_healthy_forced(self):
        mi, tmp = dead_compactor()
        try:
            def _fake(backend):
                return True, "HTTP 200"
            mi._probe = _fake
            binding = mi.guarded_resolve("x", "subagent")
            self.assertTrue(binding.healthy)
            self.assertIn(binding.backend, ("dead-a", "dead-b"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_stall_audit_reports_not_ready(self):
        mi, tmp = dead_compactor()
        try:
            audit = mi.stall_audit()
            self.assertFalse(audit["ready"])
            self.assertEqual(len(audit["down_backends"]), 2)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_watchdog_check_no_healthy(self):
        mi, tmp = dead_compactor()
        try:
            wd = StallWatchdog(project_root=str(tmp), inheritance=mi, interval_s=60.0)
            wd.check()
            self.assertFalse(wd.last_check["ready"])
            self.assertTrue(len(wd.history()) >= 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class BrainstormTests(unittest.TestCase):
    def test_board_roundtrip_and_parse(self):
        tmp = Path(tempfile.mkdtemp(prefix="bs_test_"))
        try:
            b = BrainstormBoard(project_root=str(tmp))
            b.start("tema", ["a", "b"], "ctx")
            b.post("tema", "a", "proposta")
            b.post("tema", "b", "reply")
            b.next_round("tema", "síntese")
            b.post("tema", "orc", "consenso final")
            turns = b.transcript("tema")
            self.assertEqual(len(turns), 3)
            self.assertEqual(turns[0]["participant"], "a")
            self.assertEqual(turns[0]["message"], "proposta")
            self.assertTrue(turns[-1]["message"].startswith("consenso"))
            self.assertIn("## Rodada", b.read("tema"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_board_persistent_on_disk(self):
        tmp = Path(tempfile.mkdtemp(prefix="bs_disk_"))
        try:
            b = BrainstormBoard(project_root=str(tmp))
            path = b.start("disc", ["x"], "")
            self.assertTrue(Path(path).is_file())
            self.assertEqual(b.post("disc", "x", "m1"), path)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class SelfHealTests(unittest.TestCase):
    def test_selfcheck_redflag_and_locals_down(self):
        tmp = Path(tempfile.mkdtemp(prefix="sh_test_"))
        try:
            cfg = tmp / "h.json"
            cfg.write_text(json.dumps({"harness": {"model_inheritance": {
                "backends": {n: {"base_url": "http://127.0.0.1:9", "kind": "local",
                                 "priority": i} for i, n in enumerate(LOCAL_BACKENDS)},
                "defaults": {}, "overrides": {},
            }}}), encoding="utf-8")
            mi = ModelInheritance(project_root=str(tmp), config_path=str(cfg), health_timeout=1.0)
            healer = LocalStackHealer(project_root=str(tmp), inheritance=mi,
                                      launch_cmd=["true"], timeout_s=2)
            local_up = healer._local_up()
            self.assertTrue(all(not v for v in local_up.values()))
            rec = healer.redflag("local-ornith", "teste")
            self.assertEqual(rec["kind"], "local_stack_down")
            self.assertIn("learned", rec)
            self.assertTrue((healer.redflags_path).is_file())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_heal_no_down_is_noop(self):
        tmp = Path(tempfile.mkdtemp(prefix="sh_noop_"))
        try:
            healer = LocalStackHealer(project_root=str(tmp), launch_cmd=["true"], timeout_s=2)
            # real model_inheritance -> locals down now; force empty by stubbing
            healer._local_up = lambda: {n: True for n in LOCAL_BACKENDS}
            report = healer.heal()
            self.assertFalse(report["attempted"])
            self.assertTrue(report["ok"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
