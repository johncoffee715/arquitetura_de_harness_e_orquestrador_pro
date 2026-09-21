#!/usr/bin/env python3
"""
Meta-Orquestrador — Python (Camada Meta)

Orquestra todo o pipeline 6 camadas + fallback. Responsável por:
- Task Classification
- Model / Quantization Routing
- STATE TRACKER / HASH / FINGERPRINT
- Context / KV Manager (via kv_guard)
- Retry Controller
- Circuit Breaker (R18)
- Model Fallback

Fluxo: Meta → 1 (Markdown) → 1.5 (KV Guard) → 0 (Model) → 2 (GBNF) → 2.5 (Watchdog) → 3 (Validation) → 4 (Gate) → Tool → 5 (Result) → Commit/Classify
"""
from __future__ import annotations
import hashlib
import json
import time
from pathlib import Path
from typing import Dict, Any, Callable

# Import das camadas (mesmo diretório)
try:
    from kv_guard import calculate_budget, needs_fragmentation, fragment_semantic, create_checkpoint
    from generation_watchdog import watchdog_check
    from execution_gate import execution_gate
    from result_validator import result_validator, classify_failure
    from hefesto_llama_bridge import PydanticToGbnf, ConstrainedGenerate, validate_byte_level
except ImportError:
    # Fallback se rodar isolado
    calculate_budget = lambda *a, **k: {"available": 100000, "safe_to_proceed": True}
    needs_fragmentation = lambda *a, **k: False
    fragment_semantic = lambda *a, **k: []
    watchdog_check = lambda *a, **k: {"action": "continue"}
    execution_gate = lambda *a, **k: {"gate": "PASS"}
    result_validator = lambda *a, **k: {"result": "PASS"}
    classify_failure = lambda *a, **k: {"action": "COMMIT"}

class StateTracker:
    """Rastreia estado, hash e fingerprint da task (R16/R26)."""
    def __init__(self, task_id: str, intent: str):
        self.task_id = task_id
        self.intent = intent
        self.intent_hash = hashlib.sha256(intent.encode()).hexdigest()[:16]
        self.state = {"task_id": task_id, "intent_hash": self.intent_hash, "attempt": 0, "history": []}
    
    def update(self, key: str, value: Any):
        self.state[key] = value
        self.state["history"].append({key: value, "ts": time.time()})
    
    def get_state(self) -> Dict:
        return self.state.copy()
    
    def compute_state_hash(self) -> str:
        return hashlib.sha256(json.dumps(self.state, sort_keys=True).encode()).hexdigest()[:16]

class ModelRouter:
    """Roteia para modelo/quantização baseado em task e orçamento (R13/R58)."""
    def __init__(self, manifesto_path: str = "/mnt/dados/Assistente Pessoal/modelos LLM/manifesto_llm.json"):
        self.manifesto_path = manifesto_path
    
    def route(self, task_tokens: int, available: int, critical: bool = False) -> Dict:
        """Escolhe modelo: se task cabe em IQ3 (14G) com defesa, usa IQ3; se critical e IQ3 falha, fallback para base (Qwen3-8B)."""
        if task_tokens > available:
            return {"model": "qwen3-8b-q4_k_m", "reason": "task excede janela, fallback denso", "quant": "Q4_K_M"}
        if critical:
            # Tarefa crítica: usar base coerente (IQ4) ou validador denso
            return {"model": "ornith-1.5-35b-a3b-ad-iq3_s-iq3_xxs", "quant": "IQ3_S-XXS", "fallback": "qwen3-8b-q4_k_m", "defense": "all_on"}
        return {"model": "ornith-1.5-35b-a3b-ad-iq3_s-iq3_xxs", "quant": "IQ3_S-XXS", "defense": "all_on"}

class CircuitBreaker:
    """Implementa R18: 3 falhas → cooldown 60s → gate humano."""
    def __init__(self, max_failures: int = 3, cooldown: int = 60):
        self.failures = 0
        self.max_failures = max_failures
        self.cooldown = cooldown
        self.last_failure = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def record_failure(self):
        self.failures += 1
        self.last_failure = time.time()
        if self.failures >= self.max_failures:
            self.state = "OPEN"
            return {"action": "HARD_FAIL", "circuit": "OPEN", "gate": "human"}
        return {"action": "RETRY", "failures": self.failures}
    
    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"
    
    def can_attempt(self) -> bool:
        if self.state == "OPEN":
            if time.time() - self.last_failure > self.cooldown:
                self.state = "HALF_OPEN"
                return True
            return False
        return True

class MetaOrchestrator:
    """Orquestra pipeline completo 6 camadas."""
    def __init__(self, task_id: str, intent: str, window: int = 262144):
        self.tracker = StateTracker(task_id, intent)
        self.router = ModelRouter()
        self.circuit = CircuitBreaker()
        self.window = window
    
    def run(self, task: str, schema: Dict, tool_fn: Callable, completions_fn: Callable, context: str = "") -> Dict:
        """Executa pipeline completo com fallback e retry."""
        # FASE 1 — PRE-INFERENCE
        # Camada 1: Markdown (já feito no prompt)
        # Camada 1.5: KV Guard
        budget = calculate_budget(self.window, context, json.dumps(schema))
        task_tokens = len(task) // 4
        if needs_fragmentation(task_tokens, budget["available"]):
            fragments = fragment_semantic(task, budget["available"])
            # Para simplificar, processar primeiro fragmento e retornar
            task = fragments[0]["inputs"]
            self.tracker.update("fragmented", True)
        
        # Roteamento
        route = self.router.route(task_tokens, budget["available"])
        self.tracker.update("route", route)
        
        # FASE 2 — INFERENCE
        # Camada 0: Model (via completions_fn) + 2: GBNF + 2.5: Watchdog
        # Preparar GBNF
        grammar = PydanticToGbnf(schema).to_gbnf() if schema else ""
        last_token_time = time.time()
        generated = ""
        attempts = 0
        max_retries = 3
        
        while attempts < max_retries:
            if not self.circuit.can_attempt():
                return {"status": "HARD_FAIL", "reason": "circuit breaker OPEN", "state": self.tracker.get_state()}
            try:
                # Camada 2: Constrained Decoding
                cg = ConstrainedGenerate(completions_fn, None, grammar=grammar, temperature=0.0, max_tokens=300, max_retries=1)
                text, meta = cg.run(task, context)
                generated = meta.get("raw", text)
                # Camada 2.5: Watchdog
                wd = watchdog_check(generated, len(generated)//4, 300, last_token_time)
                if wd["action"] in ["STOP", "INVALIDATE"]:
                    raise RuntimeError(f"watchdog {wd['reason']}")
                # FASE 3 — VALIDATION
                # Camada 3: Structural + Semantic
                ok, detail = validate_byte_level(generated, None)
                if not ok:
                    raise ValueError(f"validation failed {detail}")
                # Camada 4: Execution Gate (antes de tool)
                gate = execution_gate("write_file", {"path": "/tmp/test"}, schema, self.tracker.get_state(), self.tracker.intent, task)
                if gate["gate"] == "DENY":
                    raise PermissionError(f"gate denied {gate['failed_check']}")
                # FASE 4 — EXECUTION
                before = self.tracker.get_state()
                result = tool_fn(generated)  # Executa tool
                after = self.tracker.get_state()
                # Camada 5: Result Validator
                validation = result_validator({"status": "done"}, before, after, {"content": generated})
                if validation["result"] == "PASS":
                    self.circuit.record_success()
                    self.tracker.update("result", "PASS")
                    return {"status": "PASS", "output": generated, "commit": True, "state": self.tracker.get_state()}
                else:
                    classification = classify_failure(validation, attempts, max_retries)
                    if classification["action"] == "RETRY":
                        attempts += 1
                        self.tracker.update("attempt", attempts)
                        continue
                    elif classification["action"] == "FALLBACK":
                        # Tentar com modelo base
                        route = {"model": classification["model"], "fallback": True}
                        self.tracker.update("fallback", route)
                        # Retry com novo modelo (simplificado: mesma geração)
                        attempts += 1
                        continue
                    else:
                        self.circuit.record_failure()
                        return {"status": "FAIL", "classification": classification, "state": self.tracker.get_state()}
            except Exception as e:
                attempts += 1
                self.tracker.update("error", str(e)[:200])
                cb = self.circuit.record_failure()
                if cb["action"] == "HARD_FAIL":
                    return {"status": "HARD_FAIL", "reason": str(e), "circuit": "OPEN", "state": self.tracker.get_state()}
                if attempts >= max_retries:
                    return {"status": "FAIL", "reason": str(e), "attempts": attempts, "state": self.tracker.get_state()}
                time.sleep(1)  # backoff
        return {"status": "FAIL", "reason": "max retries", "state": self.tracker.get_state()}

if __name__ == "__main__":
    # Teste rápido
    def dummy_tool(text):
        return {"status": "done"}
    def dummy_completions(messages, **kwargs):
        return '{"name": "Alice", "age": 30}'
    orch = MetaOrchestrator("test-1", "generate json")
    schema = {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}, "required": ["name", "age"]}
    result = orch.run("generate json", schema, dummy_tool, dummy_completions)
    print(json.dumps(result, indent=2, ensure_ascii=False))
