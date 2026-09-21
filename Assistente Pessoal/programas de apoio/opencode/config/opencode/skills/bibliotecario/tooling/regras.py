#!/usr/bin/env python3
"""
regras.py — Synclink + retrieval do setor de regras (R101)

Determinístico (zero LLM): lê as notas individuais em `cerebro com IA/regras/` (RXX-*.md)
e devolve o "puro suco" de uma regra sob demanda. Reduz o system prompt do orquestrador:
em vez de carregar ~150KB, o orquestrador pede SÓ a regra relevante via tool call.

Origem: hefesto: forja R101 (2026-09-11); atualizado 2026-09-11 p/ ler das notas do vault
(AGENTS.md virou núcleo enxuto — a fonte completa vive nas notas).
"""
import re
import sys
import json
from pathlib import Path

REGRAS_DIR = Path("/mnt/dados/Assistente Pessoal/cerebro com IA/regras")


def _notes() -> list:
    """Lista as notas de regra (RXX-*.md), excluindo index/nucleo/backup."""
    return sorted(
        p for p in REGRAS_DIR.glob("r*.md")
        if not p.name.lower().startswith(("index", "nucleo", "agents"))
    )


def _find(rule_id: str):
    """Encontra a nota de uma regra. Aceita R46 (primário) e R46-v2 (duplicata)."""
    rid = rule_id.upper().replace("/", "-")
    want_v2 = "-V2" in rid
    base = rid.replace("-V2", "")
    for p in _notes():
        name = p.name.lower()
        if not name.startswith(base.lower()):
            continue
        is_v2 = "-v2" in name
        if want_v2 == is_v2:
            return p
    return None


def index() -> dict:
    notes = _notes()
    return {
        "fonte": str(REGRAS_DIR),
        "total_regras": len(notes),
        "regras": [p.name for p in notes],
    }


def get(rule_id: str) -> dict:
    p = _find(rule_id)
    if not p:
        return {"status": "NOT_FOUND", "rule": rule_id}
    text = p.read_text(encoding="utf-8")
    body = re.sub(r"^---\n.*?\n---\n\n", "", text, count=1, flags=re.DOTALL).strip()
    return {
        "status": "OK",
        "rule": rule_id,
        "path": str(p),
        "suco": body,
        "tokens_approx": len(body) // 4,
    }


def synclink(rule_id: str) -> dict:
    p = _find(rule_id)
    present = p is not None
    return {
        "status": "SYNCED" if present else "DRIFT",
        "rule": rule_id,
        "present_in_vault": present,
        "path": str(p) if p else None,
        "verdict": "PASSOU_CATEGORICO" if present else "NAO_PASSOU",
    }


def search(query: str, top_k: int = 3) -> dict:
    """Fallback semântico R100: busca lexical das regras mais relevantes à query."""
    terms = [t for t in re.findall(r"[a-zà-ú0-9]+", query.lower()) if len(t) > 2]
    scored = []
    for p in _notes():
        bl = p.read_text(encoding="utf-8").lower()
        score = sum(bl.count(t) for t in terms)
        if score > 0:
            scored.append((score, p.name))
    scored.sort(reverse=True)
    return {
        "query": query,
        "matches": [{"rule": name, "score": s} for s, name in scored[:top_k]],
        "total": len(scored),
    }


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "index"
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd == "index":
        print(json.dumps(index(), ensure_ascii=False, indent=2))
    elif cmd == "get" and arg:
        print(json.dumps(get(arg), ensure_ascii=False, indent=2))
    elif cmd == "synclink" and arg:
        print(json.dumps(synclink(arg), ensure_ascii=False, indent=2))
    elif cmd == "search" and arg:
        print(json.dumps(search(arg), ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"usage": "regras.py [index|get <R-id>|synclink <R-id>|search <query>]"}, ensure_ascii=False))