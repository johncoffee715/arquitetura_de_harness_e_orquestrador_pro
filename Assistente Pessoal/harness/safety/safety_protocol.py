#!/usr/bin/env python3
"""
Safety Protocol for Gran-Mestre Hybrid Harness

Implements SHA checkpointing, git diff validation, and automatic rollback
for the 6-phase pipeline.

Safety Protocol Flow:
  Phase 3 (Plan) → Save SHA
  Phase 4 (Execution) → Check git diff --quiet
  Any failure → Rollback to SHA
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class SafetyProtocol:
    """Safety protocol manager for the harness pipeline."""

    def __init__(self, project_root: str = "/mnt/dados"):
        self.project_root = Path(project_root)
        self.context_file = self.project_root / ".planning" / "CONTEXT.md"
        self.sha_file = self.project_root / ".git_harness_sha"
        self.config_file = self.project_root / "harness" / "harness-config.json"

    def load_config(self) -> dict:
        """Load harness configuration."""
        with open(self.config_file, "r") as f:
            return json.load(f)

    def get_current_sha(self) -> str:
        """Get the current git HEAD SHA."""
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to get git SHA: {result.stderr}")
        return result.stdout.strip()

    def save_sha_checkpoint(self, phase: str = "plan") -> str:
        """Save current SHA as a checkpoint.

        Called at Phase 3 (Plan) before Phase 4 (Execution).
        """
        sha = self.get_current_sha()

        # Save to .git_harness_sha file
        with open(self.sha_file, "w") as f:
            f.write(sha)

        # Update CONTEXT.md
        self._update_context_md(sha, phase, "checkpoint_saved")

        print(f"[Safety] SHA checkpoint saved: {sha}")
        print(f"[Safety] Phase: {phase}")
        print(f"[Safety] File: {self.sha_file}")

        return sha

    def check_git_diff(self) -> bool:
        """Check if there are uncommitted changes.

        Called before Phase 4 (Execution) to ensure clean state.
        """
        result = subprocess.run(
            ["git", "diff", "--quiet"],
            cwd=self.project_root,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("[Safety] Git diff check passed — no uncommitted changes")
            return True
        else:
            print("[Safety] ⚠ Git diff check FAILED — uncommitted changes detected")
            print(f"[Safety] Error: {result.stderr}")
            return False

    def rollback(self, sha: str) -> bool:
        """Rollback to a saved SHA.

        Called on any phase failure.
        """
        print(f"[Safety] Rolling back to SHA: {sha}")

        result = subprocess.run(
            ["git", "reset", "--hard", sha],
            cwd=self.project_root,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"[Safety] ❌ Rollback FAILED: {result.stderr}")
            return False

        print(f"[Safety] ✅ Rollback successful to SHA: {sha}")
        self._update_context_md(sha, "rollback", "executed")
        return True

    def get_saved_sha(self) -> Optional[str]:
        """Get the saved SHA from the checkpoint file."""
        if not self.sha_file.exists():
            return None

        with open(self.sha_file, "r") as f:
            return f.read().strip()

    def validate_before_execution(self) -> bool:
        """Validate safety protocol before Phase 4 execution.

        Checks:
        1. SHA checkpoint exists
        2. Git diff is clean
        """
        sha = self.get_saved_sha()
        if not sha:
            print("[Safety] ❌ No SHA checkpoint found — aborting execution")
            return False

        print(f"[Safety] SHA checkpoint verified: {sha}")

        if not self.check_git_diff():
            print("[Safety] ❌ Git diff check failed — aborting execution")
            return False

        print("[Safety] ✅ All safety checks passed — proceeding with execution")
        return True

    def _update_context_md(self, sha: str, phase: str, status: str):
        """Update CONTEXT.md with safety protocol status."""
        if not self.context_file.exists():
            return

        with open(self.context_file, "r") as f:
            content = f.read()

        # Update SHA in context
        import re
        content = re.sub(
            r'- \[Safety\] SHA:.*',
            f'- [Safety] SHA: {sha} (saved at Phase 3 completion)',
            content
        )

        # Update git status
        content = re.sub(
            r'- \[Safety\] Git Status:.*',
            f'- [Safety] Git Status: {status}',
            content
        )

        # Update rollback plan
        content = re.sub(
            r'- \[Safety\] Rollback Plan:.*',
            f'- [Safety] Rollback Plan: git reset --hard {sha} on any phase failure',
            content
        )

        # Update metrics
        metrics_match = re.search(
            r'\[Metrics\] Phase:.*\n\[Metrics\] Route:.*\n\[Metrics\] Status:.*',
            content
        )
        if metrics_match:
            content = content.replace(
                metrics_match.group(0),
                f'[Metrics] Phase: {phase}\n[Metrics] Route: MIX\n[Metrics] Status: {status}'
            )

        with open(self.context_file, "w") as f:
            f.write(content)

    def report_failure(self, phase: str, error: str) -> None:
        """Report a failure and execute rollback."""
        sha = self.get_saved_sha()
        if sha:
            self.rollback(sha)

        print(f"\n❌ Rollback executado.")
        print(f"SHA anterior: {sha}")
        print(f"Erro: {error}")
        print(f"\nOpções:")
        print(f"  1. Tentar abordagem diferente")
        print(f"  2. Revisar o plano com Prometheus")
        print(f"  3. Cancelar pipeline")

    def create_state_file(self, state: str, data: dict = None) -> None:
        """Create/update the harness state file for pipeline management."""
        state_file = self.project_root / "harness_state.json"

        state_data = {
            "timestamp": datetime.now().isoformat(),
            "state": state,
            "data": data or {}
        }

        with open(state_file, "w") as f:
            json.dump(state_data, f, indent=2)

        print(f"[Safety] State file updated: {state_file}")


def main():
    """CLI interface for safety protocol."""
    import argparse

    parser = argparse.ArgumentParser(description="Gran-Mestre Safety Protocol")
    parser.add_argument("command", choices=["checkpoint", "validate", "rollback", "state"],
                        help="Safety protocol command")
    parser.add_argument("--sha", type=str, help="SHA to rollback to")
    parser.add_argument("--phase", type=str, default="plan", help="Phase name")
    parser.add_argument("--error", type=str, help="Error description for failure report")
    parser.add_argument("--state", type=str, help="Pipeline state")
    parser.add_argument("--data", type=str, help="JSON data for state")

    args = parser.parse_args()

    protocol = SafetyProtocol()

    if args.command == "checkpoint":
        sha = protocol.save_sha_checkpoint(args.phase)
        print(f"Checkpoint saved: {sha}")

    elif args.command == "validate":
        if protocol.validate_before_execution():
            print("Validation passed")
            sys.exit(0)
        else:
            print("Validation failed")
            sys.exit(1)

    elif args.command == "rollback":
        sha = args.sha or protocol.get_saved_sha()
        if not sha:
            print("No SHA available for rollback")
            sys.exit(1)
        if protocol.rollback(sha):
            print(f"Rollback to {sha} successful")
        else:
            print(f"Rollback to {sha} failed")
            sys.exit(1)

    elif args.command == "state":
        data = json.loads(args.data) if args.data else None
        protocol.create_state_file(args.state, data)
        print(f"State updated: {args.state}")


if __name__ == "__main__":
    main()