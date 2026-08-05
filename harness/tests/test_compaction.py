"""Unit tests for the Global Context Compaction subsystem.

Run:  python3 -m unittest harness.tests.test_compaction -v
All tests are deterministic, dependency-free, and use tempfile directories —
they NEVER touch production /conversation_history or harness/metrics.
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from harness.context.compaction import ContextCompactor


def make_compactor():
    tmp = Path(tempfile.mkdtemp(prefix="compaction_test_"))
    c = ContextCompactor(project_root=str(tmp), offload_dir=str(tmp / "hist"))
    return c, tmp


class TriggerTests(unittest.TestCase):
    def test_trigger_none_below_min(self):
        c, tmp = make_compactor()
        try:
            self.assertEqual(c._trigger_for(0.749), "none")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_trigger_normal_at_min(self):
        c, tmp = make_compactor()
        try:
            self.assertEqual(c._trigger_for(0.75), "normal")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_trigger_critical_at_max(self):
        c, tmp = make_compactor()
        try:
            self.assertEqual(c._trigger_for(0.85), "critical")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_trigger_critical_above_max(self):
        c, tmp = make_compactor()
        try:
            self.assertEqual(c._trigger_for(0.90), "critical")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class ModelContextTests(unittest.TestCase):
    def test_model_max_context_from_config(self):
        # configured via harness-config.json loaded from project root
        c = ContextCompactor(project_root="/mnt/dados")
        self.assertEqual(c.model_max_context("filter_medium"), 32768)

    def test_model_max_context_default(self):
        c, tmp = make_compactor()
        try:
            self.assertEqual(c.model_max_context("unknown-model"), 8192)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class EstimatorTests(unittest.TestCase):
    def test_estimate_empty(self):
        self.assertEqual(ContextCompactor.estimate_tokens(""), 0)
        self.assertEqual(ContextCompactor.estimate_tokens("   "), 0)

    def test_estimate_monotonic(self):
        short = "a" * 40
        long = "a" * 400
        self.assertGreaterEqual(ContextCompactor.estimate_tokens(long),
                                ContextCompactor.estimate_tokens(short))


class CompactTests(unittest.TestCase):
    def test_compact_offloads_and_retains(self):
        c, tmp = make_compactor()
        try:
            history = ("linha de contexto demonstrativa para o teste\n" * 2000)
            used = int(8192 * 0.78)  # temp compactor resolves gran_mestre -> default 8192
            res = c.compact("th1", "gran_mestre", history, used,
                            task_intent="intenção", progress="50%", next_steps="fim")
            opath = Path(res.offload_path)
            self.assertTrue(opath.is_file())
            text = opath.read_text(encoding="utf-8")
            self.assertIn("## Window", text)
            self.assertIn("## Intenção da Tarefa", text)
            self.assertTrue(res.new_prompt.startswith("# Compaction Summary"))
            # dropped content absent from prompt but present in offload file
            self.assertEqual(res.trigger, "normal")
            self.assertGreater(res.retained_tokens, 0)
            self.assertLessEqual(res.ratio_after, 0.20)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_compact_idempotent_appends(self):
        c, tmp = make_compactor()
        try:
            history = ("x" * 200 + "\n") * 800
            used = int(262144 * 0.8)
            c.compact("th2", "gran_mestre", history, used)
            c.compact("th2", "gran_mestre", history, used)
            text = c.load_history("th2")
            self.assertEqual(text.count("## Window"), 2)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_compact_noop_below_threshold(self):
        c, tmp = make_compactor()
        try:
            res = c.compact("th3", "gran_mestre", "abc", 1000)
            self.assertEqual(res.trigger, "none")
            self.assertEqual(res.new_prompt, "abc")
            self.assertEqual(res.offload_path, "")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_compact_fallback_dir(self):
        # primary /proc is unwritable on real systems -> fallback to project
        c = ContextCompactor(project_root="/mnt/dados",
                             offload_dir="/proc/definitive/unwritable/x")
        self.assertTrue(str(c.offload_dir_effective).endswith("conversation_history"))


class InvariantTests(unittest.TestCase):
    def test_render_invariants(self):
        c, tmp = make_compactor()
        try:
            prompt = c.render_prompt("# Compaction Summary — t\n\nsum", "tail")
            self.assertTrue(prompt.startswith("# Compaction Summary"))
            self.assertIn("## Retained Recent Context", prompt)
            self.assertEqual(prompt.count("# Compaction Summary"), 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_config_defaults_when_missing(self):
        tmp = Path(tempfile.mkdtemp(prefix="compaction_cfg_"))
        try:
            c = ContextCompactor(project_root=str(tmp))  # no config file
            self.assertTrue(c.enabled)
            self.assertEqual(c.trigger_ratio_min, 0.75)
            self.assertEqual(c._effective_retain_ratio(), 0.15)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class OffloadTests(unittest.TestCase):
    def test_load_history_roundtrip(self):
        c, tmp = make_compactor()
        try:
            hist = "payload de histórico bruto\n" * 1000
            c.compact("th4", "filter_medium", hist, int(32768 * 0.8),
                      task_intent="t")
            loaded = c.load_history("th4")
            self.assertIn("## Window", loaded)
            self.assertIn("## Intenção da Tarefa", loaded)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_check_below_writes_no_compact_event(self):
        c, tmp = make_compactor()
        try:
            c.check("th5", "gran_mestre", 1000)  # trigger none
            kinds = [e.get("event") for e in c.events()]
            self.assertNotIn("compact", kinds)
            self.assertIn("track", kinds)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
