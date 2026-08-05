#!/usr/bin/env python3
"""
Completion Contracts — schema-driven gate validation.

Each pipeline phase declares WHAT a completed phase must prove
(required evidence keys + required artifacts). Gates validate the
produced evidence against the schema instead of trusting an empty OK.

Usage:
    ok, errors = validate_contract("deliver", {"iron_evidence": True, ...})
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Phase -> contract definition.
CONTRACTS: Dict[str, Dict[str, object]] = {
    "discovery": {
        "required_evidence": ["direction", "context_gathered"],
        "required_artifacts": [],
    },
    "contract": {
        "required_evidence": ["spec_validated"],
        "required_artifacts": ["SPEC.md"],
    },
    "plan": {
        "required_evidence": ["tdd_written", "sha_checkpoint"],
        "required_artifacts": ["PLAN.md"],
    },
    "execute": {
        "required_evidence": ["tests_green", "atomic_commit", "verification_per_task"],
        "required_artifacts": [],
    },
    "review": {
        "required_evidence": ["diff_reviewed", "coherence_checked"],
        "required_artifacts": [],
    },
    "deliver": {
        "required_evidence": ["iron_evidence", "final_validation", "conformity_verdict"],
        "required_artifacts": [],
    },
}

_PLANNING = Path("/mnt/dados/.planning")


def required_evidence(phase: str) -> List[str]:
    return list(CONTRACTS.get(phase, {}).get("required_evidence", []))


def required_artifacts(phase: str) -> List[str]:
    return list(CONTRACTS.get(phase, {}).get("required_artifacts", []))


def artifacts_ok(phase: str, project_root: Optional[Path] = None,
                 evidence_paths: Optional[Dict[str, str]] = None) -> List[str]:
    """Return errors for missing required artifacts.

    An artifact name may be overridden by a path in `evidence_paths`
    (e.g. {"SPEC.md": "/custom/SPEC.md"}); otherwise it is looked up
    under the project root's .planning/ directory.
    """
    root = project_root or _PLANNING.parent
    evidence_paths = evidence_paths or {}
    errors: List[str] = []
    for name in required_artifacts(phase):
        path = Path(evidence_paths.get(name, root / ".planning" / name))
        if not path.exists():
            errors.append(f"artefato obrigatório ausente: {name} ({path})")
    return errors


def validate_contract(
    phase: str,
    evidence: Dict[str, object],
    strict: bool = False,
    project_root: Optional[Path] = None,
) -> Tuple[bool, List[str]]:
    """Validate evidence against the phase contract.

    - Every required evidence key must be present and truthy.
    - Required artifacts must exist on disk.
    - When `strict` is False (additive mode), missing evidence keys are
      reported as warnings and do NOT fail the contract; artifact
      presence is always enforced.
    """
    errors: List[str] = []
    for key in required_evidence(phase):
        value = evidence.get(key)
        if value is None or value is False:
            if strict:
                errors.append(f"evidência obrigatória ausente/falsa: {key}")
            elif key not in evidence:
                errors.append(f"evidência não declarada (aviso): {key}")
    errors.extend(artifacts_ok(phase, project_root=project_root,
                               evidence_paths=evidence.get("artifact_paths")))
    if strict:
        return not errors, errors
    hard_errors = [e for e in errors if not e.startswith("evidência não declarada")]
    return not hard_errors, errors