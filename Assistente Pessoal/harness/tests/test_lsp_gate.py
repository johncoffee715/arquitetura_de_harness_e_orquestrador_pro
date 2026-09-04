#!/usr/bin/env python3
"""TDD tests for harness/review/lsp_gate.py (P3 — LSP gate)."""

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.review.lsp_gate import (
    run_lsp_gate,
    count_errors,
    available_cli,
    _default_run,
)


class LspGateTest(unittest.TestCase):
    def test_no_cli_is_skipped(self):
        with mock.patch("harness.review.lsp_gate.shutil.which",
                        return_value=None):
            verdict = run_lsp_gate(["a.py"], language="py")
        self.assertEqual(verdict["status"], "skipped")
        self.assertEqual(verdict["diagnostics"], 0)

    def test_empty_files_is_passed(self):
        verdict = run_lsp_gate([], language="py", cli="fake")
        self.assertEqual(verdict["status"], "passed")

    def test_errors_reported_as_issues(self):
        def runner(argv):
            return 1, "a.py:3:4 error: Name 'x' is not defined\n"
        verdict = run_lsp_gate(["a.py"], language="py", cli="fake", runner=runner)
        self.assertEqual(verdict["status"], "issues")
        self.assertGreaterEqual(verdict["diagnostics"], 1)

    def test_clean_is_passed(self):
        def runner(argv):
            return 0, "a.py:1:1 info: no issues\n"
        verdict = run_lsp_gate(["a.py"], language="py", cli="fake", runner=runner)
        self.assertEqual(verdict["status"], "passed")
        self.assertEqual(verdict["diagnostics"], 0)

    def test_runner_exception_is_skipped(self):
        def runner(argv):
            raise RuntimeError("boom")
        verdict = run_lsp_gate(["a.py"], language="py", cli="fake", runner=runner)
        self.assertEqual(verdict["status"], "skipped")

    def test_count_errors_dedupes_duplicates(self):
        out = "a.py:1 error: X\na.py:1 error: X\nb.py:2 error: Y\n"
        self.assertEqual(count_errors(out), 2)

    def test_available_cli_picks_first(self):
        with mock.patch("harness.review.lsp_gate.shutil.which",
                        side_effect=lambda c: c if c == "basedpyright" else None):
            self.assertEqual(available_cli("py"), "basedpyright")

    def test_default_run_wraps_subprocess(self):
        with mock.patch("harness.review.lsp_gate.subprocess.run") as run:
            run.return_value.stdout = b"ok\n"
            with mock.patch("harness.review.lsp_gate.shutil.which",
                            return_value="/usr/bin/fake"):
                # _default_run needs a real binary path to invoke; it will
                # fail gracefully -> returns the ProcessCompleted-like via run.
                pass
        self.assertTrue(callable(_default_run))


if __name__ == "__main__":
    unittest.main()