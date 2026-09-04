#!/usr/bin/env python3
"""
Dev Loop Integration for Gran-Mestre Hybrid Harness

Implements the 3-level Dev Loop methodology:
  N1: ReAct (Think → Act → Observe → Repeat) for trivial tasks
  N2: Mini Loop (Spec → TDD → Commit → Merge) for features
  N3: Human Loop (Decide → Metrics → Triage → Plan → PR → Decide) for epics
"""

import json
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class DevLoopLevel(str, Enum):
    N1_REACT = "N1-ReAct"
    N2_MINI = "N2-MiniLoop"
    N3_HUMAN = "N3-HumanLoop"


class TaskComplexity(str, Enum):
    TRIVIAL = "TRIVIAL"
    SIMPLE = "SIMPLE"
    MEDIUM = "MEDIUM"
    COMPLEX = "COMPLEX"
    CRITICAL = "CRITICAL"
    FEATURE = "FEATURE"
    MIX = "MIX"


@dataclass
class TaskResult:
    """Result of a task execution."""
    task_id: str
    description: str
    level: DevLoopLevel
    complexity: TaskComplexity
    success: bool
    iterations: int
    duration_seconds: float
    files_changed: List[str]
    errors: List[str]
    notes: str = ""


@dataclass
class LoopState:
    """State of the current Dev Loop iteration."""
    level: DevLoopLevel
    task_id: str
    iteration: int
    hypothesis: str = ""
    actions: List[str] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    escalations: int = 0
    max_iterations: int = 3
    used_tokens: int = 0
    max_context: int = 0
    compactions: int = 0


class DevLoop:
    """Dev Loop implementation for the harness."""

    def __init__(self, project_root: str = "/mnt/dados", compactor: Any = None):
        self.project_root = Path(project_root)
        self.compactor = compactor
        self.context_file = self.project_root / ".planning" / "CONTEXT.md"
        self.metrics_file = self.project_root / "harness" / "metrics" / "dev-loop-metrics.jsonl"
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self.current_state: Optional[LoopState] = None

    def classify_task(self, task_description: str, file_count: int = 1) -> TaskComplexity:
        """Classify task complexity to determine Dev Loop level.

        Uses the Gran-Mestre complexity routing table:
        - TRIVIAL: 1-step, obvious (N1)
        - SIMPLE: Small feature, clear requirements (N1)
        - MEDIUM: Multiple files, some complexity (N1 → N2)
        - COMPLEX/CRITICAL: Multiple resources needed (N2 → N3)
        - FEATURE: New feature with design in progress (N3)
        - MIX: Full pipeline (N3)
        """
        # Simple heuristic based on description and file count
        desc_lower = task_description.lower()

        if file_count <= 3 and any(word in desc_lower for word in ["fix", "typo", "simple", "quick"]):
            return TaskComplexity.TRIVIAL
        elif file_count <= 3 and "feature" not in desc_lower:
            return TaskComplexity.SIMPLE
        elif file_count <= 5:
            return TaskComplexity.MEDIUM
        elif "feature" in desc_lower or "architect" in desc_lower:
            return TaskComplexity.FEATURE
        elif "refactor" in desc_lower and "global" in desc_lower:
            return TaskComplexity.MIX
        elif "critical" in desc_lower or "security" in desc_lower:
            return TaskComplexity.CRITICAL
        else:
            return TaskComplexity.COMPLEX

    def get_loop_level(self, complexity: TaskComplexity) -> DevLoopLevel:
        """Determine Dev Loop level based on task complexity.

        N1: ReAct for TRIVIAL/SIMPLE
        N2: Mini Loop for MEDIUM/COMPLEX
        N3: Human Loop for CRITICAL/FEATURE/MIX
        """
        if complexity in [TaskComplexity.TRIVIAL, TaskComplexity.SIMPLE]:
            return DevLoopLevel.N1_REACT
        elif complexity in [TaskComplexity.MEDIUM, TaskComplexity.COMPLEX]:
            return DevLoopLevel.N2_MINI
        else:
            return DevLoopLevel.N3_HUMAN

    def start_loop(self, task_description: str, file_count: int = 1) -> LoopState:
        """Start a Dev Loop iteration."""
        complexity = self.classify_task(task_description, file_count)
        level = self.get_loop_level(complexity)

        task_id = f"task-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        self.current_state = LoopState(
            level=level,
            task_id=task_id,
            iteration=0,
            max_iterations=3 if level == DevLoopLevel.N1_REACT else 2
        )

        print(f"[DevLoop] Task: {task_description}")
        print(f"[DevLoop] Complexity: {complexity.value}")
        print(f"[DevLoop] Level: {level.value}")
        print(f"[DevLoop] Task ID: {task_id}")

        self._log_loop_start(task_id, task_description, complexity, level)
        return self.current_state

    def reconcile_context(self, used_tokens: int = 0) -> Optional[dict]:
        """Run the global context compaction check at a loop boundary.

        Delegates to the optional ``compactor`` (Global Rules R5/R6/R7). When no
        compactor is attached (``compactor=None``) or no tokens are known, this
        is a no-op — current behavior is fully preserved.
        """
        if self.compactor is None or self.current_state is None or used_tokens <= 0:
            return None
        try:
            plan = self.compactor.check(
                self.current_state.task_id, "heavy_execution", used_tokens
            )
            self.current_state.used_tokens = used_tokens
            self.current_state.max_context = plan.max_tokens
            if plan.trigger == "none":
                return None
            progress = " | ".join(self.current_state.observations[-3:]) or "loop ativo"
            result = self.compactor.compact(
                self.current_state.task_id, "heavy_execution",
                progress, used_tokens,
                task_intent=self.current_state.hypothesis or self.current_state.task_id,
                progress=progress,
                next_steps="continuar iteração do Dev Loop",
            )
            self.current_state.compactions += 1
            print(f"[DevLoop] [Compaction] trigger={plan.trigger} "
                  f"used={used_tokens}/{plan.max_tokens}")
            return {
                "trigger": plan.trigger,
                "used": used_tokens,
                "max": plan.max_tokens,
                "offload_path": result.offload_path,
            }
        except Exception as e:
            print(f"[DevLoop] [skip] reconcile_context indisponível: {e}")
            return None

    def react_loop(self, hypothesis: str, action_fn, observe_fn) -> bool:
        """Execute N1: ReAct loop.

        Cycle: think → act → observe → repeat
        Max 3 iterations before escalating to N2.
        """
        if not self.current_state:
            raise RuntimeError("No active Dev Loop state")

        state = self.current_state
        state.hypothesis = hypothesis

        print(f"\n[DevLoop N1] Hypothesis: {hypothesis}")

        for i in range(state.max_iterations):
            state.iteration = i + 1
            print(f"\n[DevLoop N1] Iteration {i + 1}/{state.max_iterations}")

            # ACT
            print(f"[DevLoop N1] [ACT] Executing action...")
            try:
                action_result = action_fn()
                state.actions.append(f"Iteration {i + 1}: {action_result}")
            except Exception as e:
                state.actions.append(f"Iteration {i + 1}: ERROR - {str(e)}")
                state.observations.append(f"Error: {str(e)}")

            # OBSERVE
            print(f"[DevLoop N1] [OBSERVE] Checking result...")
            try:
                observation = observe_fn()
                state.observations.append(observation)
                print(f"[DevLoop N1] Observation: {observation}")

                if "PASS" in observation or "success" in observation.lower():
                    print(f"[DevLoop N1] ✅ Task completed in {i + 1} iterations")
                    self._log_loop_result(state, True, i + 1)
                    return True
            except Exception as e:
                state.observations.append(f"Error: {str(e)}")
                print(f"[DevLoop N1] Observation error: {str(e)}")

        # Escalate to N2
        print(f"\n[DevLoop N1] ⚠ 3 failures — escalating to N2 (Mini Loop)")
        state.escalations += 1
        self._log_loop_result(state, False, state.max_iterations)
        return False

    def mini_loop(self, spec_fn, plan_fn, execute_fn, verify_fn) -> bool:
        """Execute N2: Mini Loop (Spec-Driven).

        Cycle: spec → plan → implement → verify → done
        Max 2 cycles before escalating to N3.
        """
        if not self.current_state:
            raise RuntimeError("No active Dev Loop state")

        state = self.current_state
        print(f"\n[DevLoop N2] Starting Mini Loop")

        for cycle in range(state.max_iterations):
            state.iteration = cycle + 1
            print(f"\n[DevLoop N2] Cycle {cycle + 1}/{state.max_iterations}")

            # SPEC
            print(f"[DevLoop N2] [SPEC] Defining feature spec...")
            spec = spec_fn()
            print(f"[DevLoop N2] Spec: {spec}")

            # PLAN
            print(f"[DevLoop N2] [PLAN] Breaking into atomic tasks...")
            tasks = plan_fn(spec)
            print(f"[DevLoop N2] Tasks: {len(tasks)} atomic tasks")

            # EXECUTE (TDD: test → code → pass)
            print(f"[DevLoop N2] [EXECUTE] Running TDD loop...")
            success = True
            for task in tasks:
                print(f"[DevLoop N2]   Task: {task}")
                try:
                    result = execute_fn(task)
                    if not result:
                        success = False
                        break
                except Exception as e:
                    print(f"[DevLoop N2]   Error: {str(e)}")
                    success = False
                    break

            if not success:
                print(f"[DevLoop N2] Cycle failed — retrying...")
                state.escalations += 1
                continue

            # VERIFY
            print(f"[DevLoop N2] [VERIFY] Running integration tests...")
            try:
                verified = verify_fn()
                if verified:
                    print(f"[DevLoop N2] ✅ Feature complete in {cycle + 1} cycles")
                    self._log_loop_result(state, True, cycle + 1)
                    return True
            except Exception as e:
                print(f"[DevLoop N2] Verification error: {str(e)}")

        # Escalate to N3
        print(f"\n[DevLoop N2] ⚠ 2 cycles failed — escalating to N3 (Human Loop)")
        state.escalations += 1
        self._log_loop_result(state, False, state.max_iterations)
        return False

    def human_loop(self, decide_fn, consult_fn, triage_fn, plan_fn, pr_fn) -> bool:
        """Execute N3: Human Loop.

        Cycle: decide → metrics → triage → plan → PR → decide
        Terminates only on human decision.
        """
        print(f"\n[DevLoop N3] Starting Human Loop")
        print(f"[DevLoop N3] Human decision required for architectural choices")

        while True:
            # DECIDE
            print(f"\n[DevLoop N3] [DECIDE] Human decides next step...")
            decision = decide_fn()
            print(f"[DevLoop N3] Decision: {decision}")

            if decision == "ENCERRAR":
                print(f"[DevLoop N3] ✅ Pipeline terminated by human")
                return True
            elif decision == "AJUSTAR":
                print(f"[DevLoop N3] Adjusting direction...")
                continue
            elif decision == "CONTINUAR":
                # CONSULT
                print(f"[DevLoop N3] [CONSULT] Gathering metrics...")
                metrics = consult_fn()
                print(f"[DevLoop N3] Metrics: {metrics}")

                # TRIAGE
                print(f"[DevLoop N3] [TRIAGE] Analyzing backlog...")
                triage = triage_fn()
                print(f"[DevLoop N3] Triage: {triage}")

                # PLAN
                print(f"[DevLoop N3] [PLAN] Planning next epic...")
                plan = plan_fn(triage)
                print(f"[DevLoop N3] Plan: {plan}")

                # PR
                print(f"[DevLoop N3] [PR] Creating Pull Request...")
                pr_result = pr_fn(plan)
                print(f"[DevLoop N3] PR: {pr_result}")
                continue

    def _log_loop_start(self, task_id: str, description: str,
                        complexity: TaskComplexity, level: DevLoopLevel) -> None:
        """Log loop start to metrics file."""
        with open(self.metrics_file, "a") as f:
            f.write(json.dumps({
                "task_id": task_id,
                "description": description,
                "complexity": complexity.value,
                "level": level.value,
                "timestamp": datetime.now().isoformat(),
                "event": "start"
            }) + "\n")

    def _log_loop_result(self, state: LoopState, success: bool, iterations: int) -> None:
        """Log loop result to metrics file."""
        with open(self.metrics_file, "a") as f:
            f.write(json.dumps({
                "task_id": state.task_id,
                "level": state.level.value,
                "success": success,
                "iterations": iterations,
                "escalations": state.escalations,
                "timestamp": datetime.now().isoformat(),
                "event": "result"
            }) + "\n")

        # Update CONTEXT.md
        self._update_context_md(state, success, iterations)

    def _update_context_md(self, state: LoopState, success: bool, iterations: int) -> None:
        """Update CONTEXT.md with Dev Loop metrics."""
        if not self.context_file.exists():
            return

        with open(self.context_file, "r") as f:
            content = f.read()

        import re

        dev_loop_metrics = (
            f'[DevLoop] Level: {state.level.value}\n'
            f'[DevLoop] Iteration: {iterations}\n'
            f'[DevLoop] Action: {"done" if success else "escalated"}\n'
            f'[DevLoop] Status: {"success" if success else "escalated"}'
        )

        # Check if DevLoop metrics already exist
        existing = re.search(r'\[DevLoop\].*', content)
        if existing:
            content = re.sub(r'\[DevLoop\].*', dev_loop_metrics, content)
        else:
            content += f"\n\n{dev_loop_metrics}\n"

        with open(self.context_file, "w") as f:
            f.write(content)

    def get_loop_summary(self) -> Dict[str, Any]:
        """Get summary of all Dev Loop iterations."""
        if not self.metrics_file.exists():
            return {}

        results = []
        with open(self.metrics_file, "r") as f:
            for line in f:
                data = json.loads(line)
                if data.get("event") == "result":
                    results.append(data)

        summary = {
            "total_iterations": len(results),
            "successful": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
            "escalations": sum(r.get("escalations", 0) for r in results),
            "by_level": {}
        }

        for r in results:
            level = r["level"]
            if level not in summary["by_level"]:
                summary["by_level"][level] = {"total": 0, "success": 0, "fail": 0}
            summary["by_level"][level]["total"] += 1
            if r["success"]:
                summary["by_level"][level]["success"] += 1
            else:
                summary["by_level"][level]["fail"] += 1

        return summary

    def print_summary(self) -> None:
        """Print Dev Loop summary."""
        summary = self.get_loop_summary()
        if not summary:
            print("No Dev Loop metrics recorded yet.")
            return

        print("\n" + "=" * 60)
        print("DEV LOOP SUMMARY")
        print("=" * 60)
        print(f"Total iterations: {summary['total_iterations']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        print(f"Escalations: {summary['escalations']}")

        print("\nBy Level:")
        for level, data in summary["by_level"].items():
            print(f"  {level}: {data['success']}/{data['total']} success")

        print("\n" + "=" * 60)


def main():
    """CLI interface for Dev Loop."""
    import argparse

    parser = argparse.ArgumentParser(description="Gran-Mestre Dev Loop")
    parser.add_argument("command", choices=["classify", "start", "summary"],
                        help="Dev Loop command")
    parser.add_argument("--task", type=str, help="Task description")
    parser.add_argument("--files", type=int, default=1, help="Number of files affected")
    parser.add_argument("--level", type=str, choices=["N1", "N2", "N3"], help="Force loop level")

    args = parser.parse_args()

    loop = DevLoop()

    if args.command == "classify":
        if not args.task:
            print("Error: --task required for classify")
            exit(1)
        complexity = loop.classify_task(args.task, args.files)
        level = loop.get_loop_level(complexity)
        print(f"Task: {args.task}")
        print(f"Complexity: {complexity.value}")
        print(f"Loop Level: {level.value}")

    elif args.command == "start":
        if not args.task:
            print("Error: --task required for start")
            exit(1)
        state = loop.start_loop(args.task, args.files)
        print(f"Started Dev Loop: {state.level.value}")
        print(f"Task ID: {state.task_id}")

    elif args.command == "summary":
        loop.print_summary()


if __name__ == "__main__":
    main()