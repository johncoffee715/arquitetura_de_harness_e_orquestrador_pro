#!/usr/bin/env python3
"""TDD tests for harness/safety/completion_contract.py (P2 — contracts)."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.safety.completion_contract import (
    CONTRACTS,
    validate_contract,
    required_evidence,
    required_artifacts,
    artifacts_ok,
)


class CompletionContractTest(unittest.TestCase):
    def test_all_six_phases_have_contracts(self):
        self.assertEqual(
            sorted(CONTRACTS),
            ["contract", "deliver", "discovery", "execute", "plan", "review"],
        )

    def test_required_evidence_catalog(self):
        self.assertIn("iron_evidence", required_evidence("deliver"))
        self.assertIn("tdd_written", required_evidence("plan"))
        self.assertIn("context_gathered", required_evidence("discovery"))

    def test_deliver_strict_requires_evidence(self):
        ok, errors = validate_contract("deliver", {}, strict=True)
        self.assertFalse(ok)
        self.assertGreaterEqual(len(errors), 3)

    def test_deliver_strict_passes_with_full_evidence(self):
        ok, errors = validate_contract(
            "deliver",
            {"iron_evidence": True, "final_validation": True,
             "conformity_verdict": True},
            strict=True,
        )
        self.assertTrue(ok, errors)

    def test_additive_mode_warns_but_passes(self):
        ok, errors = validate_contract("plan", {"sha_checkpoint": "abc123"})
        self.assertTrue(ok)
        self.assertTrue(any("aviso" in e for e in errors))

    def test_artifact_required_by_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".planning").mkdir()
            (root / ".planning" / "SPEC.md").write_text("# spec")
            ok, errors = validate_contract("contract", {"spec_validated": True},
                                           strict=True, project_root=root)
            self.assertTrue(ok, errors)
            (root / ".planning" / "SPEC.md").unlink()
            ok, errors = validate_contract("contract", {"spec_validated": True},
                                           strict=True, project_root=root)
            self.assertFalse(ok)
            self.assertTrue(any("SPEC.md" in e for e in errors))

    def test_artifact_path_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".planning").mkdir()
            alt = root / "custom-spec.md"
            alt.write_text("# spec")
            ok, errors = validate_contract(
                "contract",
                {"spec_validated": True,
                 "artifact_paths": {"SPEC.md": str(alt)}},
                strict=True, project_root=root,
            )
            self.assertTrue(ok, errors)

    def test_artifacts_ok_reports_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".planning").mkdir()
            errs = artifacts_ok("contract", project_root=root)
            self.assertEqual(len(errs), 1)


if __name__ == "__main__":
    unittest.main()