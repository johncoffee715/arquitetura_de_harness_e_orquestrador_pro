#!/usr/bin/env python3
"""
Observability Layer for Gran-Mestre Hybrid Harness

Implements metrics logging, OpenTelemetry integration, and MELT tracking
for the 6-phase pipeline.
"""

import json
import os
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class Phase(str, Enum):
    DISCOVERY = "discovery"
    CONTRACT = "contract"
    PLAN = "plan"
    EXECUTE = "execute"
    REVIEW = "review"
    DELIVER = "deliver"


class Route(str, Enum):
    TRIVIAL = "TRIVIAL"
    SIMPLE = "SIMPLE"
    MEDIUM = "MEDIUM"
    COMPLEX = "COMPLEX"
    CRITICAL = "CRITICAL"
    FEATURE = "FEATURE"
    MIX = "MIX"


class Status(str, Enum):
    SUCCESS = "success"
    ESCALATED = "escalated"
    FAILED = "failed"
    PENDING = "pending"
    RUNNING = "running"


@dataclass
class PhaseMetrics:
    """Metrics for a single pipeline phase."""
    phase: Phase
    route: Route
    status: Status
    duration_seconds: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    llm_calls: int = 0
    tool_calls: int = 0
    cost: float = 0.0
    delegations: Dict[str, int] = field(default_factory=lambda: {
        "subagents": 0,
        "skills": 0,
        "mcps": 0
    })
    errors: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""


class ObservabilityLayer:
    """Observability layer for the harness pipeline."""

    def __init__(self, project_root: str = "/mnt/dados"):
        self.project_root = Path(project_root)
        self.context_file = self.project_root / ".planning" / "CONTEXT.md"
        self.metrics_file = self.project_root / "harness" / "metrics" / "pipeline-metrics.jsonl"
        self.events_file = self.project_root / "harness" / "metrics" / "events.jsonl"
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._current_metrics: Optional[PhaseMetrics] = None
        self._otel_counters: Optional[Dict[str, Any]] = None
        self._otel_duration: Optional[Any] = None

    def start_phase(self, phase: Phase, route: Route) -> PhaseMetrics:
        """Start tracking metrics for a phase."""
        metrics = PhaseMetrics(
            phase=phase,
            route=route,
            status=Status.RUNNING
        )
        self._current_metrics = metrics
        self._log_metrics(metrics)
        self._update_context_md(metrics)
        return metrics

    def end_phase(self, metrics: PhaseMetrics, status: Status = Status.SUCCESS,
                  notes: str = "", input_tokens: Optional[int] = None,
                  output_tokens: Optional[int] = None,
                  llm_calls: Optional[int] = None,
                  tool_calls: Optional[int] = None,
                  cost: Optional[float] = None) -> PhaseMetrics:
        """End tracking metrics for a phase.

        Backward compatible: existing callers may keep using
        (metrics, status, notes). Real token/call/cost counts are recorded
        when provided (via kwargs or set directly on the metrics object).
        """
        metrics.status = status
        metrics.notes = notes
        if input_tokens is not None:
            metrics.input_tokens = input_tokens
        if output_tokens is not None:
            metrics.output_tokens = output_tokens
        if llm_calls is not None:
            metrics.llm_calls = llm_calls
        if tool_calls is not None:
            metrics.tool_calls = tool_calls
        if cost is not None:
            metrics.cost = cost
        self._log_metrics(metrics)
        self._update_context_md(metrics)
        self._record_otel(metrics)
        if self._current_metrics is metrics:
            self._current_metrics = None
        return metrics

    def log_error(self, metrics: PhaseMetrics, error_msg: str) -> None:
        """Log an error during a phase."""
        metrics.errors += 1
        if not metrics.notes:
            metrics.notes = error_msg
        else:
            metrics.notes += f"; {error_msg}"
        self._log_metrics(metrics)

    def log_token_usage(self, metrics: PhaseMetrics, input_tokens: int,
                        output_tokens: int) -> None:
        """Log token usage for a phase."""
        metrics.input_tokens += input_tokens
        metrics.output_tokens += output_tokens
        self._log_metrics(metrics)

    def log_call(self, metrics: PhaseMetrics, call_type: str) -> None:
        """Log a call (LLM or tool) for a phase."""
        if call_type == "llm":
            metrics.llm_calls += 1
        elif call_type == "tool":
            metrics.tool_calls += 1
        self._log_metrics(metrics)

    def log_delegation(self, metrics: PhaseMetrics, delegation_type: str) -> None:
        """Log a delegation (subagent, skill, mcp) for a phase."""
        if delegation_type in metrics.delegations:
            metrics.delegations[delegation_type] += 1
        else:
            metrics.delegations[delegation_type] = 1
        self._log_metrics(metrics)

    def track_cost(self, cost: float) -> None:
        """Track cumulative cost for the current phase (USD).

        Falls back to a standalone OpenTelemetry counter when no phase
        is active. Never raises — observability is best-effort.
        """
        if self._current_metrics is not None:
            self._current_metrics.cost += cost
            self._log_metrics(self._current_metrics)
            return
        if OTEL_AVAILABLE and _otel_state is not None:
            try:
                _otel_state["meter"].create_counter(
                    "gran_mestre.cost", unit="USD",
                    description="Cumulative harness cost"
                ).add(float(cost))
            except Exception:
                pass

    def record_event(self, phase: Any, event: str,
                     attrs: Optional[Dict[str, Any]] = None) -> None:
        """Record a MELT 'events' entry appended to harness/metrics/events.jsonl.

        Args:
            phase: Phase enum or phase name string.
            event: Event identifier (e.g. "gate_passed", "model_selected").
            attrs: Optional structured attributes attached to the event.
        """
        phase_name = phase.value if isinstance(phase, Phase) else str(phase)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase_name,
            "event": event,
            "attrs": attrs or {}
        }
        with self._lock:
            with open(self.events_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        if OTEL_AVAILABLE and _otel_state is not None:
            try:
                tracer = _otel_state["tracer"]
                with tracer.start_as_current_span(f"event.{event}") as span:
                    span.set_attribute("phase", phase_name)
                    span.set_attribute("event", event)
                    for key, value in (attrs or {}).items():
                        span.set_attribute(f"event.{key}", value)
            except Exception:
                pass

    def _record_otel(self, metrics: PhaseMetrics) -> None:
        """Push phase metrics to OpenTelemetry counters/histograms.

        No-op unless OpenTelemetry initialized successfully. Wrapped in
        try/except — a collector outage must never crash the pipeline.
        """
        if not OTEL_AVAILABLE or _otel_state is None:
            return
        try:
            meter = _otel_state["meter"]
            key = "gran_mestre"
            if self._otel_counters is None:
                self._otel_counters = {
                    "input_tokens": meter.create_counter(
                        f"{key}.tokens.input", unit="1",
                        description="Input tokens processed"),
                    "output_tokens": meter.create_counter(
                        f"{key}.tokens.output", unit="1",
                        description="Output tokens generated"),
                    "llm_calls": meter.create_counter(
                        f"{key}.llm.calls", unit="1",
                        description="LLM calls made"),
                    "tool_calls": meter.create_counter(
                        f"{key}.tool.calls", unit="1",
                        description="Tool calls made"),
                    "cost": meter.create_counter(
                        f"{key}.cost", unit="USD",
                        description="Phase cost"),
                    "errors": meter.create_counter(
                        f"{key}.errors", unit="1",
                        description="Phase errors"),
                }
                self._otel_duration = meter.create_histogram(
                    f"{key}.duration", unit="s",
                    description="Phase duration")
            attrs = {
                "phase": metrics.phase.value,
                "route": metrics.route.value,
                "status": metrics.status.value,
            }
            counters = {
                "input_tokens": metrics.input_tokens,
                "output_tokens": metrics.output_tokens,
                "llm_calls": metrics.llm_calls,
                "tool_calls": metrics.tool_calls,
                "cost": metrics.cost,
                "errors": metrics.errors,
            }
            for name, value in counters.items():
                if value > 0:
                    self._otel_counters[name].add(value, attrs)
            if metrics.duration_seconds > 0:
                self._otel_duration.record(metrics.duration_seconds, attrs)
        except Exception:
            pass

    def _log_metrics(self, metrics: PhaseMetrics) -> None:
        """Log metrics to the metrics file."""
        with self._lock:
            with open(self.metrics_file, "a") as f:
                f.write(json.dumps({
                    "phase": metrics.phase.value,
                    "route": metrics.route.value,
                    "status": metrics.status.value,
                    "duration_seconds": metrics.duration_seconds,
                    "input_tokens": metrics.input_tokens,
                    "output_tokens": metrics.output_tokens,
                    "llm_calls": metrics.llm_calls,
                    "tool_calls": metrics.tool_calls,
                    "cost": metrics.cost,
                    "delegations": metrics.delegations,
                    "errors": metrics.errors,
                    "timestamp": metrics.timestamp,
                    "notes": metrics.notes
                }) + "\n")

    def _update_context_md(self, metrics: PhaseMetrics) -> None:
        """Update CONTEXT.md with metrics."""
        if not self.context_file.exists():
            return

        with open(self.context_file, "r") as f:
            content = f.read()

        import re

        # Update metrics section
        old_metrics = re.search(
            r'\[Metrics\] Phase:.*\n\[Metrics\] Route:.*\n\[Metrics\] Status:.*',
            content
        )

        new_metrics = (
            f'[Metrics] Phase: {metrics.phase.value}\n'
            f'[Metrics] Route: {metrics.route.value}\n'
            f'[Metrics] Status: {metrics.status.value}\n'
            f'[Metrics] Duration: {metrics.duration_seconds:.2f}s\n'
            f'[Metrics] Tokens: {metrics.input_tokens}/{metrics.output_tokens}\n'
            f'[Metrics] Calls: {metrics.llm_calls}\n'
            f'[Metrics] Tools: {metrics.tool_calls}\n'
            f'[Metrics] Delegations: {metrics.delegations["subagents"]}/{metrics.delegations["skills"]}/{metrics.delegations["mcps"]}\n'
            f'[Metrics] Errors: {metrics.errors}'
        )

        if old_metrics:
            content = content.replace(old_metrics.group(0), new_metrics)
        else:
            content += f"\n\n{new_metrics}\n"

        with open(self.context_file, "w") as f:
            f.write(content)

    def get_phase_summary(self) -> Dict[str, Any]:
        """Get a summary of all phases."""
        if not self.metrics_file.exists():
            return {}

        phases = {}
        with open(self.metrics_file, "r") as f:
            for line in f:
                data = json.loads(line)
                phase_name = data["phase"]
                if phase_name not in phases:
                    phases[phase_name] = []
                phases[phase_name].append(data)

        summary = {}
        for phase_name, entries in phases.items():
            latest = entries[-1]  # Get latest entry for each phase
            summary[phase_name] = {
                "route": latest["route"],
                "status": latest["status"],
                "duration_seconds": latest["duration_seconds"],
                "errors": latest["errors"],
                "timestamp": latest["timestamp"]
            }

        return summary

    def print_summary(self) -> None:
        """Print a summary of all phases."""
        summary = self.get_phase_summary()
        if not summary:
            print("No metrics recorded yet.")
            return

        print("\n" + "=" * 60)
        print("PIPELINE METRICS SUMMARY")
        print("=" * 60)

        for phase, data in summary.items():
            print(f"\n  Phase: {phase.upper()}")
            print(f"    Route: {data['route']}")
            print(f"    Status: {data['status']}")
            print(f"    Duration: {data['duration_seconds']:.2f}s")
            print(f"    Errors: {data['errors']}")
            print(f"    Timestamp: {data['timestamp']}")

        print("\n" + "=" * 60)


# OpenTelemetry integration (optional)
try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False

_otel_started = False
_otel_state: Optional[Dict[str, Any]] = None


def setup_opentelemetry(project_name: str = "gran-mestre-harness"):
    """Set up OpenTelemetry integration if available.

    Idempotent: initializes exactly once (module-level ``_otel_started``
    guard) and never raises — if the collector/exporter is unreachable the
    harness falls back to basic metrics logging.
    """
    global _otel_started, _otel_state
    if _otel_started:
        return _otel_state
    if not OTEL_AVAILABLE:
        print("[Observability] OpenTelemetry not available — using basic metrics only")
        _otel_started = True
        return None

    try:
        resource = Resource.create({
            "service.name": project_name,
            "service.version": "1.0.0",
            "platform": "IR",
        })

        # Set up tracing
        trace.set_tracer_provider(TracerProvider(resource=resource))
        tracer = trace.get_tracer(project_name)

        # Set up metrics
        metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(endpoint="localhost:4317", insecure=True)
        )
        metrics.set_meter_provider(MeterProvider(
            resource=resource,
            metric_readers=[metric_reader]
        ))
        meter = metrics.get_meter(project_name)

        _otel_state = {"tracer": tracer, "meter": meter}
        print("[Observability] OpenTelemetry configured")
    except Exception as exc:  # never crash on collector/export failures
        _otel_state = None
        print(f"[Observability] OpenTelemetry setup failed "
              f"({exc}) — continuing without tracing")
    finally:
        _otel_started = True
    return _otel_state


def shutdown_opentelemetry() -> None:
    """Flush and shut down OpenTelemetry providers.

    Safe to call at harness end (or multiple times). No-op when
    OpenTelemetry is unavailable or was never initialized.
    """
    if not OTEL_AVAILABLE or not _otel_started or _otel_state is None:
        return
    try:
        tracer_provider = trace.get_tracer_provider()
        if isinstance(tracer_provider, TracerProvider):
            tracer_provider.shutdown()
        meter_provider = metrics.get_meter_provider()
        if isinstance(meter_provider, MeterProvider):
            meter_provider.shutdown()
        print("[Observability] OpenTelemetry shutdown complete")
    except Exception as exc:
        print(f"[Observability] OpenTelemetry shutdown failed ({exc})")


# Initialize OpenTelemetry once at module import (best-effort)
setup_opentelemetry()


def main():
    """CLI interface for observability."""
    import argparse

    parser = argparse.ArgumentParser(description="Gran-Mestre Observability Layer")
    parser.add_argument("--summary", action="store_true", help="Print metrics summary")
    parser.add_argument("--phase", type=str, help="Filter by phase")
    parser.add_argument("--route", type=str, help="Set route")
    parser.add_argument("--status", type=str, help="Set status")
    parser.add_argument("--duration", type=float, help="Set duration")
    parser.add_argument("--log", type=str, help="Log a metric entry")

    args = parser.parse_args()

    obs = ObservabilityLayer()

    if args.summary:
        obs.print_summary()

    elif args.log:
        metrics = PhaseMetrics(
            phase=Phase(args.phase or "discovery"),
            route=Route(args.route or "MIX"),
            status=Status(args.status or "success"),
            duration_seconds=args.duration or 0.0
        )
        obs._log_metrics(metrics)
        obs._update_context_md(metrics)
        print(f"Logged: {metrics.phase.value} / {metrics.route.value} / {metrics.status.value}")


if __name__ == "__main__":
    main()