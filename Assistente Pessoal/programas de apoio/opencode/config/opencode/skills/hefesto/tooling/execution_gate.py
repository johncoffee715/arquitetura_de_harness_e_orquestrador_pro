#!/usr/bin/env python3
"""
Execution Gate — Camada 4 (R77/R81)

Valida Tool Whitelist, Permission, State, Argumentos, Preconditions,
Safety Invariants e Intent Fingerprint antes de executar tool/API.

Ordem: Markdown (1) → KV Guard (1.5) → Model (0) → GBNF (2) → Watchdog (2.5) → JSON (3) → Gate (4) → Tool → Result (5)
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Any

# Gabarito allow/deny (R77) — exemplo, deve vir de gabarito.json real
DEFAULT_ALLOWLIST = {"read_file", "write_file", "execute_bash", "search", "validate_json", "create_artifact"}
DEFAULT_DENYLIST = {"rm -rf /", "shutdown", "mkfs", "dd of=/dev"}

def check_tool_whitelist(tool: str, allowlist: set = None) -> Dict:
    """Verifica se tool está na whitelist (R77 firewall)."""
    allow = allowlist or DEFAULT_ALLOWLIST
    allowed = tool in allow
    return {"allowed": allowed, "tool": tool, "action": "continue" if allowed else "deny"}

def check_permission(tool: str, params: Dict, user_permissions: Dict = None) -> Dict:
    """Verifica permissão do usuário para a tool (ex: external_directory allow)."""
    # Simplificado: checar se params tenta acessar path fora do allow
    if "path" in params:
        path = str(params["path"])
        if ".." in path or path.startswith("/etc") or path.startswith("/root"):
            return {"allowed": False, "reason": "path traversal ou acesso restrito", "action": "deny"}
    return {"allowed": True, "action": "continue"}

def check_state_validation(current_state: Dict, required_state: Dict) -> Dict:
    """Valida se estado atual permite a execução (ex: arquivo existe?)."""
    for key, expected in required_state.items():
        actual = current_state.get(key)
        if actual != expected:
            return {"valid": False, "key": key, "expected": expected, "actual": actual, "action": "deny"}
    return {"valid": True, "action": "continue"}

def check_argument_validation(tool: str, params: Dict, schema: Dict) -> Dict:
    """Valida argumentos contra JSON Schema (tipos, required, etc.)."""
    required = schema.get("required", [])
    props = schema.get("properties", {})
    for req in required:
        if req not in params:
            return {"valid": False, "missing": req, "action": "deny"}
    for k, v in params.items():
        if k in props:
            expected_type = props[k].get("type")
            if expected_type == "string" and not isinstance(v, str):
                return {"valid": False, "key": k, "expected": "string", "action": "deny"}
            if expected_type == "integer" and not isinstance(v, int):
                return {"valid": False, "key": k, "expected": "integer", "action": "deny"}
            if expected_type == "boolean" and not isinstance(v, bool):
                return {"valid": False, "key": k, "expected": "boolean", "action": "deny"}
    return {"valid": True, "action": "continue"}

def check_preconditions(tool: str, params: Dict) -> Dict:
    """Verifica precondições (ex: arquivo deve existir para read)."""
    if tool == "read_file" and "path" in params:
        if not Path(params["path"]).exists():
            return {"valid": False, "reason": f"arquivo não existe: {params['path']}", "action": "deny"}
    return {"valid": True, "action": "continue"}

def check_safety_invariants(tool: str, params: Dict) -> Dict:
    """Verifica invariants de segurança (ex: nunca rm -rf /)."""
    cmd = str(params.get("command", "")) + str(params.get("path", ""))
    for denied in DEFAULT_DENYLIST:
        if denied in cmd:
            return {"safe": False, "reason": f"comando negado: {denied}", "action": "deny"}
    return {"safe": True, "action": "continue"}

def compute_intent_fingerprint(intent: str) -> str:
    """Hash da intenção original (para detectar drift)."""
    return hashlib.sha256(intent.encode()).hexdigest()[:16]

def check_intent_fingerprint(original_intent: str, current_intent: str) -> Dict:
    """Verifica se intenção atual ainda alinha com original (evita drift)."""
    orig_hash = compute_intent_fingerprint(original_intent)
    curr_hash = compute_intent_fingerprint(current_intent)
    # Hash diferente indica drift, mas conteúdo pode ser similar — usar distância simples
    drift = orig_hash != curr_hash
    # Se drift, verificar se é apenas variação de parâmetros ou mudança de objetivo
    if drift and len(current_intent) > len(original_intent) * 2:
        return {"aligned": False, "drift": True, "action": "deny"}
    return {"aligned": True, "action": "continue"}

def execution_gate(tool: str, params: Dict, schema: Dict, current_state: Dict, original_intent: str, current_intent: str) -> Dict:
    """Orquestra todos os checks da Camada 4. Retorna PASS/FAIL e ação."""
    checks = [
        ("whitelist", check_tool_whitelist(tool)),
        ("permission", check_permission(tool, params)),
        ("state", check_state_validation(current_state, {})),
        ("arguments", check_argument_validation(tool, params, schema)),
        ("preconditions", check_preconditions(tool, params)),
        ("safety", check_safety_invariants(tool, params)),
        ("fingerprint", check_intent_fingerprint(original_intent, current_intent)),
    ]
    for name, result in checks:
        if result.get("action") == "deny" or not result.get("allowed", True) or not result.get("valid", True) or not result.get("safe", True) or not result.get("aligned", True):
            return {"gate": "DENY", "failed_check": name, "details": result, "action": "deny"}
    return {"gate": "PASS", "action": "continue", "details": {k: v for k, v in checks}}

if __name__ == "__main__":
    print(execution_gate("read_file", {"path": "/tmp/test.txt"}, {"required": ["path"], "properties": {"path": {"type": "string"}}}, {}, "read file", "read file"))
    print(execution_gate("rm -rf /", {"command": "rm -rf /"}, {}, {}, "delete", "delete"))
