#!/usr/bin/env python3
"""
KV Guard — Camada 1.5 Context / KV Guard (R22)

Implementa token budget, context compaction, priority, degradation detection,
KV checkpoint e session reset para a Linha de Defesa 6 camadas.

Ordem: Markdown (1) → KV Guard (1.5) → Model (0) → GBNF (2) → Watchdog (2.5) → JSON (3) → Gate (4) → Result (5)
"""
from __future__ import annotations
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Heurística de orçamento (R22): window - system - tool_defs - reserved_output - safety_margin
SAFETY_MARGIN = 512
RESERVED_OUTPUT = 2048

def estimate_tokens(text: str) -> int:
    """Estimativa ~4 chars/token (conservadora, melhor que tiktoken sem dependência)."""
    if not text:
        return 0
    return max(1, len(text) // 4)

def calculate_budget(window: int, system_prompt: str = "", tool_defs: str = "", memory: str = "") -> Dict:
    """Calcula orçamento disponível (R22). Retorna dict com available, breakdown."""
    system_tokens = estimate_tokens(system_prompt)
    tool_tokens = estimate_tokens(tool_defs)
    memory_tokens = estimate_tokens(memory)
    reserved = RESERVED_OUTPUT + SAFETY_MARGIN
    available = window - system_tokens - tool_tokens - memory_tokens - reserved
    return {
        "window": window,
        "system_tokens": system_tokens,
        "tool_tokens": tool_tokens,
        "memory_tokens": memory_tokens,
        "reserved": reserved,
        "available": max(0, available),
        "safe_to_proceed": available > 0,
    }

def needs_fragmentation(task_tokens: int, available: int) -> bool:
    """True se task excede orçamento e precisa fragmentar (R22)."""
    return task_tokens > available

def fragment_semantic(text: str, max_tokens_per_fragment: int, overlap_ratio: float = 0.15) -> List[Dict]:
    """
    Fragmenta em fronteiras estruturais (nunca por contagem matemática):
    - Código: fim de blocos lógicos (funções, classes)
    - Texto: parágrafos fechados (\\n\\n)
    Overlap 15% para garantir continuidade.
    Retorna lista de fragmentos com envelope.
    """
    if not needs_fragmentation(estimate_tokens(text), max_tokens_per_fragment):
        return [{
            "task_id": "task-0",
            "parent_task": None,
            "sequence": 0,
            "objective": text[:100],
            "inputs": text,
            "constraints": [],
            "expected_output": "completo",
            "validation": "completo",
            "state_from_previous": {},
            "tokens": estimate_tokens(text),
        }]
    # Quebrar por parágrafos ou blocos
    # Tentar por \\n\\n primeiro (texto), depois por linhas de código
    if "\\n\\n" in text:
        blocks = text.split("\\n\\n")
        sep = "\\n\\n"
    else:
        # Código: tentar por linhas com indentação ou por funções
        blocks = re.split(r"(\\ndef |\\nclass |\\n\\n)", text)
        sep = ""
    fragments = []
    current = ""
    seq = 0
    overlap_tokens = int(max_tokens_per_fragment * overlap_ratio)
    for block in blocks:
        if not block.strip():
            continue
        candidate = current + sep + block if current else block
        if estimate_tokens(candidate) > max_tokens_per_fragment and current:
            # Finaliza fragmento atual, cria overlap para próximo
            fragments.append({
                "task_id": f"task-{seq}",
                "parent_task": "parent",
                "sequence": seq,
                "objective": f"fragmento {seq}",
                "inputs": current,
                "constraints": ["manter overlap 15%"],
                "expected_output": f"parte {seq}",
                "validation": "coerência com anterior",
                "state_from_previous": fragments[-1] if fragments else {},
                "tokens": estimate_tokens(current),
            })
            # Overlap: últimas linhas do fragmento anterior
            overlap_text = current[-overlap_tokens*4:] if overlap_tokens else ""
            current = overlap_text + sep + block
            seq += 1
        else:
            current = candidate
    if current.strip():
        fragments.append({
            "task_id": f"task-{seq}",
            "parent_task": "parent",
            "sequence": seq,
            "objective": f"fragmento {seq}",
            "inputs": current,
            "constraints": [],
            "expected_output": f"parte {seq}",
            "validation": "final",
            "state_from_previous": fragments[-1] if fragments else {},
            "tokens": estimate_tokens(current),
        })
    return fragments

def create_checkpoint(task_id: str, status: str, result: str, decisions: List[str], files_changed: List[str]) -> Dict:
    """Checkpoint obrigatório após cada fragmento (R22)."""
    return {
        "task_id": task_id,
        "status": status,
        "result": result[:200],
        "decisions": decisions,
        "files_changed": files_changed,
        "next_action": "continue" if status == "COMPLETED" else "retry",
    }

def detect_degradation(prev_output: str, curr_output: str) -> Dict:
    """Detecta degradação de contexto (repetição, perda de coerência)."""
    if not prev_output or not curr_output:
        return {"degraded": False}
    # Heurísticas simples: repetição de n-gram, similaridade baixa
    prev_tokens = set(prev_output.split())
    curr_tokens = set(curr_output.split())
    overlap = len(prev_tokens & curr_tokens) / max(1, len(prev_tokens | curr_tokens))
    # Se overlap muito alto (>0.9) pode ser repetição; muito baixo (<0.1) pode ser perda
    degraded = overlap > 0.9 or overlap < 0.1
    return {"degraded": degraded, "overlap": overlap, "action": "compact" if degraded else "continue"}

if __name__ == "__main__":
    # Teste rápido
    budget = calculate_budget(262144, "system prompt longo " * 100, "tool defs")
    print(f"budget available: {budget['available']}")
    frags = fragment_semantic("para1\\n\\npara2\\n\\npara3 " * 100, 100)
    print(f"fragmentos: {len(frags)}")
