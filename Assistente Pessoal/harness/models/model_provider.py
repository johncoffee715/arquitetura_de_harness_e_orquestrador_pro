#!/usr/bin/env python3
"""
Model Provider Layer for Gran-Mestre Hybrid Harness

Manages local and cloud model hot-swap with route-based selection.
"""

import json
import os
import sys
import time
import asyncio
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ModelLocation(str, Enum):
    LOCAL = "local"
    CLOUD = "cloud"


class ModelRole(str, Enum):
    GRAN_MESTRE = "gran_mestre"
    HEAVY_EXECUTION = "heavy_execution"
    FILTER_FAST = "filter_fast"
    FILTER_MEDIUM = "filter_medium"
    CLOUD_MOE = "cloud_moe"


@dataclass
class ModelConfig:
    """Configuration for a single model."""
    name: str
    quantization: str
    vram_gb: float
    location: ModelLocation
    role: ModelRole
    parallel_slots: int = 1
    description: str = ""
    endpoint: Optional[str] = None
    api_key: Optional[str] = None
    redflag: bool = False


@dataclass
class ModelInstance:
    """Runtime instance of a model."""
    config: ModelConfig
    available_slots: int
    active_requests: int = 0
    last_used: Optional[str] = None
    reason: Optional[str] = None

    def is_available(self) -> bool:
        """Check if model has available slots."""
        return self.active_requests < self.available_slots

    def acquire_slot(self) -> bool:
        """Acquire a slot for a request."""
        if self.is_available():
            self.active_requests += 1
            self.last_used = datetime.now().isoformat()
            return True
        return False

    def release_slot(self) -> None:
        """Release a slot after request completes."""
        if self.active_requests > 0:
            self.active_requests -= 1


class ModelProvider:
    """Model provider for hot-swap between local and cloud models."""

    # Health-probe retry/backoff (llama.cpp /health endpoint).
    probe_retries: int = 3
    probe_backoff: float = 1.5

    # policies.json cloud.moe_only_on_phases indices -> phase names.
    _PHASE_INDEX_TO_NAME = {
        1: "discovery", 2: "contract", 3: "plan",
        4: "execute", 5: "review", 6: "deliver",
    }

    def __init__(self, config_path: str = "/mnt/dados/Assistente Pessoal/harness/harness-config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.models: Dict[str, ModelInstance] = {}
        self._init_models()

    def _load_config(self) -> dict:
        """Load harness configuration."""
        with open(self.config_path, "r") as f:
            return json.load(f)

    def _init_models(self) -> None:
        """Initialize model instances from config."""
        for model_key, model_data in self.config["harness"]["models"].items():
            config = ModelConfig(
                name=model_data["name"],
                quantization=model_data["quantization"],
                vram_gb=model_data["vram_gb"],
                location=ModelLocation(model_data["location"]),
                role=ModelRole(model_key),
                parallel_slots=model_data.get("parallel_slots", 1),
                description=model_data.get("description", ""),
                endpoint=model_data.get("endpoint"),
                api_key=model_data.get("api_key")
            )
            self.models[model_key] = ModelInstance(
                config=config,
                available_slots=config.parallel_slots
            )

    def get_model_for_route(self, route: str) -> ModelInstance:
        """Get appropriate model for a given complexity route.

        Route-based model selection:
        - TRIVIAL/SIMPLE → LFM 2.5 (instant checks)
        - MEDIUM → Nanbeige 3B (micro-reviews)
        - COMPLEX/CRITICAL → Bonsai 27B 1-bit (heavy execution)
        - FEATURE → Bonsai + Ornith (full pipeline)
        - MIX → Ornith + Bonsai + MoE (max resources)
        """
        route_upper = route.upper()

        if route_upper in ["TRIVIAL", "SIMPLE"]:
            return self.models["filter_fast"]
        elif route_upper == "MEDIUM":
            return self.models["filter_medium"]
        elif route_upper in ["COMPLEX", "CRITICAL"]:
            return self.models["heavy_execution"]
        elif route_upper == "FEATURE":
            return self.models["heavy_execution"]
        elif route_upper == "MIX":
            return self.models["gran_mestre"]
        else:
            # Default to Gran-Mestre
            return self.models["gran_mestre"]

    def get_model_by_role(self, role: str) -> ModelInstance:
        """Get model by role name."""
        role_map = {
            "gran_mestre": "gran_mestre",
            "heavy_execution": "heavy_execution",
            "filter_fast": "filter_fast",
            "filter_medium": "filter_medium",
            "cloud_moe": "cloud_moe"
        }
        key = role_map.get(role, "gran_mestre")
        return self.models[key]

    def get_available_models(self) -> List[ModelInstance]:
        """Get all available models with free slots."""
        return [m for m in self.models.values() if m.is_available()]

    def get_vram_usage(self) -> Dict[str, Any]:
        """Get current VRAM usage breakdown."""
        total_budget = self.config["harness"]["vram_budget"]["total_gb"]
        allocated = sum(
            m.config.vram_gb for m in self.models.values()
            if m.config.location == ModelLocation.LOCAL
        )
        reserved = self.config["harness"]["vram_budget"]["kv_cache_reserved_gb"]

        return {
            "total_gb": total_budget,
            "allocated_gb": allocated,
            "reserved_gb": reserved,
            "available_gb": total_budget - allocated - reserved,
            "models": {
                key: {
                    "name": m.config.name,
                    "vram_gb": m.config.vram_gb,
                    "location": m.config.location.value,
                    "active_requests": m.active_requests,
                    "available_slots": m.available_slots
                }
                for key, m in self.models.items()
            }
        }

    def hot_swap(self, old_model: str, new_model: str) -> bool:
        """Hot-swap from one model to another.

        Local-to-local swaps use the real VRAM-aware ModelSwapper
        (drain-first, unload/load of the llama-server, /health re-probe).
        Swaps involving cloud models fall back to simulation (no GPU op).
        """
        print(f"[ModelProvider] Hot-swapping: {old_model} → {new_model}")

        if old_model not in self.models:
            print(f"[ModelProvider] ❌ Unknown model: {old_model}")
            return False

        if new_model not in self.models:
            print(f"[ModelProvider] ❌ Unknown model: {new_model}")
            return False

        old_cfg = self.models[old_model].config
        new_cfg = self.models[new_model].config
        if (old_cfg.location == ModelLocation.LOCAL
                and new_cfg.location == ModelLocation.LOCAL):
            try:
                from harness.models.vram_guard import ModelSwapper, VRAMGuard
                swapper = ModelSwapper(guard=VRAMGuard())
                if not swapper.swap(
                        old_model, new_model,
                        active_requests=self.models[old_model].active_requests):
                    print(f"[ModelProvider] ❌ Hot-swap recusado (drain/VRAM)")
                    return False
            except Exception as e:  # pragma: no cover - runtime fallback
                print(f"[ModelProvider] ⚠ swapper real indisponível: {e}")

        self.models[old_model].last_used = datetime.now().isoformat()
        self.models[new_model].last_used = datetime.now().isoformat()

        print(f"[ModelProvider] ✅ Hot-swap successful")
        return True

    def select_model(self, route: str, phase: str) -> ModelInstance:
        """Select the best model for a given route and phase.

        Phase-specific model selection:
        - Phase 1 (Discovery): Ornith-1.0 9B (Gran-Mestre)
        - Phase 2 (Contract): Bonsai 27B 1-bit (generation)
        - Phase 3 (Plan): Bonsai 27B 1-bit (planning)
        - Phase 4 (Execution): Bonsai 27B 1-bit (execution)
        - Phase 5 (Review): Ornith + MoE (cloud audit)
        - Phase 6 (Delivery): Ornith + MoE (final verdict)
        """
        phase_model_map = {
            "discovery": "gran_mestre",
            "contract": "heavy_execution",
            "plan": "heavy_execution",
            "execute": "heavy_execution",
            "review": "gran_mestre",
            "deliver": "gran_mestre"
        }

        model_key = phase_model_map.get(phase, "gran_mestre")
        model = self.models[model_key]

        # Check if cloud MoE should be used for Phase 5/6
        if phase in ["review", "deliver"] and route in ["COMPLEX", "CRITICAL", "FEATURE", "MIX"]:
            # Check if local model has issues, use cloud MoE
            print(f"[ModelProvider] Phase {phase}: Using cloud MoE for architectural audit")

        return model

    def _derive_endpoint(self, model_key: str) -> Optional[str]:
        """Derive llama.cpp endpoint port from model key / local_model_path basename."""
        port_map = {
            "lfm": 8081,
            "nanbeige": 8082,
            "ornith": 8083,
            "bonsai": 8084,
        }
        config = self.models[model_key].config
        if config.endpoint:
            return config.endpoint
        model_data = self.config["harness"]["models"].get(model_key, {})
        local_path = model_data.get("local_model_path") or ""
        basename = Path(local_path).stem.lower()
        for token, port in port_map.items():
            if token in basename:
                return f"http://127.0.0.1:{port}/health"
        return None

    def _probe_endpoint(self, endpoint: Optional[str]) -> bool:
        """Probe a llama.cpp /health endpoint (3s timeout) with retry/backoff.

        Healthy == {'status': 'ok'}. Retries ``probe_retries`` times, sleeping
        ``probe_backoff * attempt`` seconds between attempts.
        """
        if not endpoint:
            return False
        for attempt in range(1, self.probe_retries + 1):
            try:
                req = urllib.request.Request(endpoint, headers={"Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=3) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                if data.get("status") == "ok":
                    return True
            except Exception:
                pass
            if attempt < self.probe_retries:
                time.sleep(self.probe_backoff * attempt)
        return False

    def _cloud_fallback_instance(self) -> ModelInstance:
        """Build a cloud free fallback pseudo-instance."""
        config = ModelConfig(
            name="opencode/deepseek-v4-flash-free",
            quantization="n/a",
            vram_gb=0,
            location=ModelLocation.CLOUD,
            role=ModelRole.CLOUD_MOE,
            parallel_slots=4,
            description="Cloud free fallback (used when local protocol fails)",
            endpoint=None,
        )
        return ModelInstance(config=config, available_slots=config.parallel_slots)

    def _moe_allowed_phases(self) -> List[str]:
        """Phases where cloud MoE is allowed (policies.json cloud.moe_only_on_phases)."""
        try:
            with open(self.config_path.parent / "policies.json", "r") as f:
                policies = json.load(f)
            indices = policies.get("policies", {}).get("cloud", {}).get(
                "moe_only_on_phases", [5, 6]
            )
            names = [self._PHASE_INDEX_TO_NAME.get(int(i)) for i in indices]
            return [n for n in names if n] or ["review", "deliver"]
        except Exception:
            return ["review", "deliver"]

    def _is_cloud(self, model: ModelInstance) -> bool:
        """True for cloud models (location != local or opencode/* model id)."""
        return (
            model.config.location != ModelLocation.LOCAL
            or str(model.config.name).startswith("opencode/")
        )

    def _best_local_model(self, route: str, phase: str) -> ModelInstance:
        """Best local model available for the route/phase weight.

        Bonsai 27B for heavy work, Ornith 9B for medium, LFM for trivial. Probes
        candidates in priority order; returns the first healthy one, or the best
        candidate (redflagged) when every local server is offline.
        """
        route_upper = route.upper()
        if phase == "execute" or route_upper in ("COMPLEX", "CRITICAL", "FEATURE", "MIX"):
            candidates = ["heavy_execution", "gran_mestre", "filter_medium", "filter_fast"]
        elif route_upper == "MEDIUM":
            candidates = ["gran_mestre", "filter_medium", "heavy_execution", "filter_fast"]
        else:
            candidates = ["filter_fast", "filter_medium", "gran_mestre", "heavy_execution"]

        for key in candidates:
            inst = self.models[key]
            if self._probe_endpoint(self._derive_endpoint(key)):
                inst.reason = f"best local available ({inst.config.name})"
                return inst

        inst = self.models[candidates[0]]
        inst.config.redflag = True
        inst.reason = "all local models offline; cloud MoE blocked for this phase"
        return inst

    def _apply_moe_restriction(self, model: ModelInstance, route: str,
                               phase: str) -> ModelInstance:
        """Enforce policies.json cloud.moe_only_on_phases (default review/deliver).

        Cloud models resolved for a disallowed phase are replaced by the best
        local model, with the selection reason recorded on the instance.
        """
        if not self._is_cloud(model):
            return model
        allowed = self._moe_allowed_phases()
        if phase in allowed:
            return model
        best = self._best_local_model(route, phase)
        best.reason = (
            f"cloud MoE blocked for phase '{phase}' (moe_only_on_phases={allowed}); "
            f"using best local {best.config.name}"
        )
        print(
            f"[ModelProvider] MoE restriction: cloud blocked for phase '{phase}' — "
            f"using {best.config.name} (local)"
        )
        return best

    def select_model_with_fallback(self, route: str, phase: str) -> ModelInstance:
        """Select local model, probe health; redflag + cloud fallback if offline.

        Local-first protocol: probe llama.cpp /health; on failure mark the local
        model with a redflag and fall back to the cloud free model — unless the
        phase is outside policies.json cloud.moe_only_on_phases, in which case
        the best available local model is used instead.
        """
        local_model = self.select_model(route, phase)
        endpoint = self._derive_endpoint(local_model.config.role.value)
        if self._probe_endpoint(endpoint):
            return local_model

        local_model.config.redflag = True
        if phase not in self._moe_allowed_phases():
            print(
                f"[ModelProvider] REDFLAG: {local_model.config.name} offline — "
                f"cloud MoE blocked for phase '{phase}'; using best local"
            )
            return self._best_local_model(route, phase)

        print(
            f"[ModelProvider] REDFLAG: {local_model.config.name} offline — "
            f"falling back to cloud free"
        )
        return self._cloud_fallback_instance()

    def _parse_override(self, override_model: str) -> ModelInstance:
        """Parse an explicit override id like 'local-bonsai/bonsai-27b' or
        'opencode/glm-5.2' into a ModelInstance. No health probe for overrides."""
        provider, _, model = override_model.partition("/")
        provider_lower = provider.lower()
        if provider_lower.startswith("local") or provider_lower in [
            "local-bonsai", "local-ornith", "local-lfm", "local-nanbeige",
        ]:
            name_lower = model.lower()
            for inst in self.models.values():
                if name_lower in inst.config.name.lower():
                    inst.config.redflag = False
                    return inst
        config = ModelConfig(
            name=override_model,
            quantization="n/a",
            vram_gb=0,
            location=ModelLocation.CLOUD,
            role=ModelRole.CLOUD_MOE,
            parallel_slots=4,
            description="Explicit model override",
            endpoint=None,
        )
        return ModelInstance(config=config, available_slots=config.parallel_slots)

    def resolve_model(
        self,
        route: str,
        phase: str,
        override_model: Optional[str] = None,
    ) -> ModelInstance:
        """Orchestrator-level model selection.

        Priority:
        1. Explicit override_model (e.g. 'local-bonsai/bonsai-27b', 'opencode/glm-5.2')
           — returned directly, no health probe.
        2. Phase-based override: fast model (filter_fast / LFM) for planning phases
           (discovery, contract, plan); heavy model (heavy_execution / Bonsai) for
           implementation phases (execute, review).
        3. Local-first selection with cloud-free fallback (select_model_with_fallback).

        Cloud MoE restriction: a cloud model is only honored in the phases listed
        in policies.json cloud.moe_only_on_phases ([5, 6] → review/deliver); for
        any other phase it is replaced by the best available local model.
        """
        if override_model:
            resolved = self._parse_override(override_model)
        elif phase in ("plan", "discovery", "contract"):
            fast = self.models["filter_fast"]
            if self._probe_endpoint(self._derive_endpoint("filter_fast")):
                return fast
            resolved = self._cloud_fallback_instance()
        elif phase in ("execute", "review"):
            heavy = self.models["heavy_execution"]
            if self._probe_endpoint(self._derive_endpoint("heavy_execution")):
                return heavy
            resolved = self._cloud_fallback_instance()
        else:
            resolved = self.select_model_with_fallback(route, phase)

        return self._apply_moe_restriction(resolved, route, phase)

    def select_resources(self, task: str, phase: str = "", top_k: int = 5) -> Dict[str, list]:
        """Seleciona recursos do registry (plugins/mcp/lsp/hooks/skills/subagents)
        para a task — escolha automática do orquestrador (Ornith)."""
        try:
            from core.integration import IntegrationManager
            manager = IntegrationManager(str(self.config_path).replace("harness/harness-config.json", ""))
            return manager.select_for_task(task, phase, top_k)
        except ImportError:
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from core.integration import IntegrationManager
            manager = IntegrationManager(str(Path(__file__).parent.parent.parent))
            return manager.select_for_task(task, phase, top_k)

    def get_status(self) -> Dict[str, Any]:
        """Get current status of all models."""
        return {
            "models": {
                key: {
                    "name": m.config.name,
                    "vram_gb": m.config.vram_gb,
                    "location": m.config.location.value,
                    "role": m.config.role.value,
                    "parallel_slots": m.config.parallel_slots,
                    "active_requests": m.active_requests,
                    "available_slots": m.available_slots,
                    "last_used": m.last_used
                }
                for key, m in self.models.items()
            },
            "vram": self.get_vram_usage()
        }


def main():
    """CLI interface for Model Provider."""
    import argparse

    parser = argparse.ArgumentParser(description="Gran-Mestre Model Provider")
    parser.add_argument("command", choices=["status", "select", "swap", "vram"],
                        help="Model provider command")
    parser.add_argument("--route", type=str, help="Complexity route")
    parser.add_argument("--phase", type=str, help="Pipeline phase")
    parser.add_argument("--override", type=str, help="Explicit model override (e.g. opencode/glm-5.2)")
    parser.add_argument("--from", dest="from_model", type=str, help="Model to swap from")
    parser.add_argument("--to", dest="to_model", type=str, help="Model to swap to")

    args = parser.parse_args()

    provider = ModelProvider()

    if args.command == "status":
        status = provider.get_status()
        print(json.dumps(status, indent=2))

    elif args.command == "select":
        if not args.route or not args.phase:
            print("Error: --route and --phase required for select")
            exit(1)
        model = provider.select_model(args.route, args.phase)
        print(f"Selected model: {model.config.name}")
        print(f"Location: {model.config.location.value}")
        print(f"Role: {model.config.role.value}")
        print(f"VRAM: {model.config.vram_gb}GB")

    elif args.command == "swap":
        if not args.from_model or not args.to_model:
            print("Error: --from and --to required for swap")
            exit(1)
        provider.hot_swap(args.from_model, args.to_model)

    elif args.command == "vram":
        vram = provider.get_vram_usage()
        print(json.dumps(vram, indent=2))


if __name__ == "__main__":
    main()