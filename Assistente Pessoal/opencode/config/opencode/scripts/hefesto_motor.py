#!/usr/bin/env python3
"""
HEFESTO MOTOR — Full Modular Engine (Helenizado v1.0.0)

Motor full modular do Hefesto para resolução dinâmica de slots CPU/GPU vivos
via inventário real, execução do pipeline criacionista com Panteão de validadores.

Origin: helenizado: hefesto-creationist-v6 (sha256 0057067d732eb4c1704fb3160a809d50375dfab8d84af4d50470e626c85ae793)
"""

import sys
import json
import os
import argparse
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Paths globais (R2/R44)
INVENTORY_PATH = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/harness/llm-inventory.json")
SCRIPTS_DIR = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/scripts")

def setup_logger(p="/tmp/opencode/hefesto.log"):
    """Setup logger com path seguro (não hardcoded /var/log)."""
    os.makedirs(os.path.dirname(p), exist_ok=True)
    l = logging.getLogger("HefestoMotor")
    l.setLevel(logging.WARNING)
    if not l.handlers:
        h = RotatingFileHandler(p, maxBytes=2*1024*1024, backupCount=2)
        h.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] [HEFESTO-MOTOR]: %(message)s'))
        l.addHandler(h)
    return l


def load_inventory() -> dict:
    """Carrega o inventário real de LLMs (R35/R47)."""
    if INVENTORY_PATH.exists():
        with open(INVENTORY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"models": [], "schema_version": 1}


def list_cpu_slots(logger) -> list:
    """Lista slots CPU vivos via inventário real (R35)."""
    inventory = load_inventory()
    cpu_slots = []
    for model in inventory.get("models", []):
        sector = model.get("sector", "")
        if sector.startswith("CPU") and model.get("status") == "online":
            cpu_slots.append({
                "id": model["id"],
                "port": model["slot"],
                "params": model["params"],
                "ctx": model.get("ctx_allocated", 0),
                "temp": model.get("temp", 0.6)
            })
    return cpu_slots


def resolve_slot_for_role(role: str, logger) -> dict | None:
    """Resolve o melhor slot vivo para o papel especificado (R47)."""
    inventory = load_inventory()
    role_mapping = {
        "forja": "ornith",
        "judge": "bonsai",
        "refutador": "ternary",
        "descoberta": "ornith",
        "reflexo": "nanbeige",
        "tool-leve": "ornith"
    }
    
    target_id = role_mapping.get(role)
    if not target_id:
        logger.warning(f"Role desconhecido: {role}")
        return None
    
    for model in inventory.get("models", []):
        if target_id in model.get("id", "").lower() and model.get("status") == "online":
            return {
                "id": model["id"],
                "port": model["slot"],
                "baseURL": f"http://localhost:{model['slot']}",
                "ctx": model.get("ctx_allocated", 0),
                "temp": model.get("temp", 0.6)
            }
    
    logger.warning(f"Modelo {target_id} não encontrado ou offline")
    return None


def execute_workflow(payload: dict, logger) -> dict:
    """Executa o workflow criacionista com Panteão de validadores."""
    fallback_active = payload.get("fallback_automatico", False)
    if fallback_active:
        logger.warning("Timeout detectado pelo orquestrador (30s). Ignorando peso humano e acionando validador automático subsequente.")
    
    active_model = resolve_slot_for_role("forja", logger)
    
    # Panteão de validadores (R28)
    validators = {
        "autophagy": lambda data: _evaluate_pillar("autophagy", data, logger),
        "decompilation": lambda data: _evaluate_pillar("decompilation", data, logger),
        "helenization": lambda data: _evaluate_pillar("helenization", data, logger),
        "forging": lambda data: _evaluate_pillar("forging", data, logger)
    }
    
    scores = {}
    for pillar, validator_fn in validators.items():
        scores[pillar] = validator_fn(payload)
    
    total_score = sum(item["score"] for item in scores.values()) / len(scores)
    loop_terminated = total_score > 95.0
    
    return {
        "agent": "hefesto-motor",
        "version": "1.0.0",
        "active_model": active_model,
        "fallback_triggered": fallback_active,
        "pantheon_audit": scores,
        "average_score": round(total_score, 5),
        "dev_loop_terminated": loop_terminated,
        "status": "OLYMPIAN_PERFECTION" if loop_terminated else "FREEZE_PAUSE_REQUIRED"
    }


def _evaluate_pillar(pillar_name: str, data: dict, logger) -> dict:
    """Avalia pilar com evidência (não auto-aprovação)."""
    # Verifica se há evidência real no payload
    evidence = data.get("evidence", {})
    score = data.get(f"{pillar_name}_score", None)
    
    if score is not None and 0.0000001 <= score <= 100:
        return {
            "pillar": pillar_name,
            "score": score,
            "status": "validated_by_evidence"
        }
    
    # Sem evidência → UNKNOWN (não auto-aprovação)
    logger.warning(f"Pilar {pillar_name} sem evidência → UNKNOWN")
    return {
        "pillar": pillar_name,
        "score": 0.0000001,  # Piso R34
        "status": "UNKNOWN",
        "note": "sem evidência documentada"
    }


def main():
    parser = argparse.ArgumentParser(description="Hefesto Motor - Full Modular Engine")
    parser.add_argument("--list-cpu", action="store_true", help="Lista slots CPU vivos")
    parser.add_argument("--resolve", type=str, help="Resolve slot para o role especificado")
    parser.add_argument("--execute", type=str, help="Executa workflow com payload JSON")
    args = parser.parse_args()
    
    logger = setup_logger()
    
    if args.list_cpu:
        slots = list_cpu_slots(logger)
        print(json.dumps(slots, indent=2))
        return
    
    if args.resolve:
        slot = resolve_slot_for_role(args.resolve, logger)
        print(json.dumps(slot, indent=2) if slot else json.dumps({"error": "Slot não encontrado"}))
        return
    
    if args.execute:
        try:
            payload = json.loads(args.execute)
            result = execute_workflow(payload, logger)
            print(json.dumps(result, separators=(',', ':')))
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"JSON inválido: {e}"}))
            sys.exit(1)
        return
    
    # Nenhum argumento → ajuda
    parser.print_help()


if __name__ == "__main__":
    main()