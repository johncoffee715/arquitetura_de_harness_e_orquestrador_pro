#!/usr/bin/env python3
"""
Result Validator — Camada 5 (R28/R34)

Valida expected effect, state transition, checksum, invariants e artifact integrity
após execução da tool. Decide PASS→COMMIT ou FAIL→CLASSIFY→RETRY/HARD_FAIL/MODEL_DEGRADE
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Dict, Any

def compute_checksum(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def check_expected_effect(expected: Dict, actual: Dict) -> Dict:
    """Verifica se efeito esperado ocorreu (ex: arquivo criado)."""
    for key, expected_val in expected.items():
        actual_val = actual.get(key)
        if actual_val != expected_val:
            return {"matched": False, "key": key, "expected": expected_val, "actual": actual_val}
    return {"matched": True}

def check_state_transition(before: Dict, after: Dict, expected_transition: Dict) -> Dict:
    """Verifica transição de estado (ex: status mudou de pending para done)."""
    for key, expected_val in expected_transition.items():
        before_val = before.get(key)
        after_val = after.get(key)
        if after_val != expected_val:
            return {"valid": False, "key": key, "before": before_val, "after": after_val, "expected": expected_val}
    return {"valid": True}

def check_invariants(artifacts: Dict, invariants: List[str]) -> Dict:
    """Verifica invariants (ex: JSON ainda válido, arquivo não vazio)."""
    for inv in invariants:
        if inv == "json_valid":
            try:
                json.loads(artifacts.get("content", ""))
            except:
                return {"valid": False, "invariant": inv}
        if inv == "file_not_empty" and not artifacts.get("content"):
            return {"valid": False, "invariant": inv}
        if inv == "no_fence" and artifacts.get("content", "").strip().startswith("```"):
            return {"valid": False, "invariant": inv}
    return {"valid": True}

def check_artifact_integrity(baseline_sha: str, current_content: str) -> Dict:
    """Verifica integridade do artefato (SHA baseline vs pós)."""
    current_sha = compute_checksum(current_content)
    # Se baseline é None, é criação nova, então integridade é se conteúdo existe
    if baseline_sha is None:
        return {"integrity": bool(current_content), "sha": current_sha}
    # Se baseline existe, verificar se mudou (deve ter mudado se foi write)
    changed = baseline_sha != current_sha
    return {"integrity": changed, "baseline": baseline_sha, "current": current_sha, "changed": changed}

def result_validator(expected_effect: Dict, before_state: Dict, after_state: Dict, artifacts: Dict, baseline_sha: str = None) -> Dict:
    """Orquestra validação da Camada 5. Retorna PASS/COMMIT ou FAIL/CLASSIFY."""
    checks = {
        "expected_effect": check_expected_effect(expected_effect, after_state),
        "state_transition": check_state_transition(before_state, after_state, expected_effect),
        "invariants": check_invariants(artifacts, ["json_valid", "file_not_empty", "no_fence"]),
        "integrity": check_artifact_integrity(baseline_sha, artifacts.get("content", "")),
    }
    # Se todos passarem → PASS
    all_pass = (
        checks["expected_effect"].get("matched", False) and
        checks["state_transition"].get("valid", False) and
        checks["invariants"].get("valid", False) and
        checks["integrity"].get("integrity", False)
    )
    if all_pass:
        return {"result": "PASS", "action": "COMMIT", "checks": checks, "commit": True}
    # Falha → classificar
    # Se integridade falhou mas expected effect ok → retry (pode ser escrita parcial)
    if not checks["integrity"].get("integrity"):
        return {"result": "FAIL", "classification": "RETRY", "checks": checks, "reason": "integridade falhou, retry com state atualizado"}
    if not checks["invariants"].get("valid"):
        return {"result": "FAIL", "classification": "HARD_FAIL", "checks": checks, "reason": "invariant violado, hard fail → circuit breaker"}
    # Se expected effect não bateu e já tentou 3x → model degrade
    return {"result": "FAIL", "classification": "MODEL_DEGRADE", "checks": checks, "reason": "efeito não atingido, tentar fallback modelo base"}

def classify_failure(validator_result: Dict, attempt: int, max_retries: int = 3) -> Dict:
    """Classifica falha para retry/hard fail/model degrade com base em tentativas."""
    if validator_result["result"] == "PASS":
        return {"action": "COMMIT"}
    classification = validator_result.get("classification", "RETRY")
    if classification == "RETRY" and attempt < max_retries:
        return {"action": "RETRY", "update_state": True}
    if classification == "RETRY" and attempt >= max_retries:
        return {"action": "HARD_FAIL", "circuit_breaker": "open", "gate": "human"}
    if classification == "HARD_FAIL":
        return {"action": "HARD_FAIL", "circuit_breaker": "open"}
    if classification == "MODEL_DEGRADE":
        return {"action": "FALLBACK", "model": "qwen3-8b-q4_k_m", "reason": "fallback para validador denso"}
    return {"action": classification}

if __name__ == "__main__":
    print(result_validator({"status": "done"}, {"status": "pending"}, {"status": "done"}, {"content": '{"a": 1}'}))
    print(result_validator({"status": "done"}, {"status": "pending"}, {"status": "pending"}, {"content": ""}))
