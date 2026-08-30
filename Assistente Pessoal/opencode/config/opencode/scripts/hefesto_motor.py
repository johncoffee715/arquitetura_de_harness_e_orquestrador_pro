#!/usr/bin/env python3
"""
HEFESTO MOTOR — Full Modular Engine v2.0.0 (Dispatcher)

Motor do Hefesto para resolução dinâmica de slots via inventário real (R75),
validação de gabarito (R77 camada 2) e execução do pipeline com Panteão (R34).

Origin: helenizado: hefesto-creationist-v6 (sha256 0057067d732eb4c1704fb3160a809d50375dfab8d84af4d50470e626c85ae793)
Refatorado 2026-08-30: role_mapping obsoleto (bonsai/nanbeige/ornith) → categorias R75.
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
SKILLS_DIR = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills")

# R75 — mapeamento fase → categoria (bindings por categoria, nunca nome de GGUF)
CATEGORY_ROUTES = {
    "decompilacao": "contrato-plano",
    "autofagia": "refutacao",
    "helenizacao": "contrato-plano",
    "forja": "forja",
}
# Fallback por categoria (R10/R9 — hot-swap quando primário offline)
FALLBACK_ROUTES = {
    "forja": "judge",
    "contrato-plano": "orquestrador",
    "refutacao": "contrato-plano",
}


def setup_logger(p="/tmp/opencode/hefesto.log"):
    """Setup logger com path seguro (não hardcoded /var/log)."""
    os.makedirs(os.path.dirname(p), exist_ok=True)
    l = logging.getLogger("HefestoMotor")
    l.setLevel(logging.WARNING)
    if not l.handlers:
        h = RotatingFileHandler(p, maxBytes=2 * 1024 * 1024, backupCount=2)
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
                "id": model.get("id"),
                "port": model.get("slot"),
                "category": model.get("category"),
                "ctx": model.get("ctx_allocated", 0),
                "temp": model.get("temp", 0.6),
            })
    return cpu_slots


def resolve_slot_for_role(role: str, logger) -> dict | None:
    """Resolve o melhor slot vivo para a fase/categoria (R75) com fallback (R10)."""
    inventory = load_inventory()
    models = inventory.get("models", [])

    # R75: fase → categoria (decompilacao → contrato-plano, etc.)
    category = CATEGORY_ROUTES.get(role, role)

    def find(cat: str) -> dict | None:
        for model in models:
            if model.get("category") == cat and model.get("status") == "online":
                return {
                    "id": model.get("id"),
                    "port": model.get("slot"),
                    "baseURL": f"http://localhost:{model.get('slot')}",
                    "ctx": model.get("ctx_allocated", 0),
                    "temp": model.get("temp", 0.6),
                    "category": cat,
                    "api": model.get("api", "openai"),
                }
        return None

    # Categoria direta (R75)
    slot = find(category)
    if slot:
        return slot
    # Fallback (R10/R9)
    fb = FALLBACK_ROUTES.get(category)
    if fb:
        slot = find(fb)
        if slot:
            logger.warning(f"Categoria {category} offline → fallback {fb}")
            slot["fallback_from"] = category
            return slot
    logger.warning(f"Categoria {category} (e fallback) não encontrada ou offline")
    return None


def validate_gabarito(skill_name: str, action: str, logger) -> bool:
    """R77 camada 2 — lê gabarito.json da skill e recusa ignição se violar deny."""
    gabarito_path = SKILLS_DIR / skill_name / "gabarito.json"
    if not gabarito_path.exists():
        logger.warning(f"Gabarito não encontrado para {skill_name} — ignorando validação")
        return True
    try:
        with open(gabarito_path, 'r', encoding='utf-8') as f:
            gabarito = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Gabarito inválido para {skill_name}: {e}")
        return False
    deny = gabarito.get("deny", {})
    denied = deny.get("behaviors", []) + deny.get("tools", []) + deny.get("paths", [])
    if action in denied:
        logger.error(f"REJEITADO: {skill_name}({action}) violou deny: {denied}")
        return False
    return True


def _evaluate_pillar(pillar_name: str, data: dict, logger) -> dict:
    """Avalia pilar com escala R34 (0.0000001-100). Sem evidência → UNKNOWN + piso."""
    evidence = data.get(f"{pillar_name}_evidence", [])
    if not evidence:
        return {"pillar": pillar_name, "score": 0.0000001, "status": "UNKNOWN",
                "note": "sem evidência — piso R34 (nunca default alto)"}
    score = float(data.get(f"{pillar_name}_score", 0.0))
    score = max(0.0000001, min(100.0, score))
    return {"pillar": pillar_name, "score": score, "status": "EVALUATED",
            "evidence_count": len(evidence)}


def execute_workflow(payload: dict, logger) -> dict:
    """Executa o workflow criacionista com Panteão de validadores (R28/R34)."""
    phase = payload.get("phase", "forja")
    artifact = payload.get("artifact", "unknown")
    skill_name = f"hefesto-{phase}"

    # Fase fora do pipeline = violação de escopo (R77 deny)
    if phase not in CATEGORY_ROUTES:
        return {"status": "GABARITO_VIOLADO", "skill": skill_name, "artifact": artifact,
                "error": f"fase '{phase}' fora do pipeline Hefesto"}

    # R77 camada 2 — valida gabarito antes de qualquer ignição
    if not validate_gabarito(skill_name, "execute", logger):
        return {"status": "GABARITO_VIOLADO", "skill": skill_name, "artifact": artifact}

    # R75 — resolve motor por categoria
    category = CATEGORY_ROUTES.get(phase, "contrato-plano")
    active_model = resolve_slot_for_role(category, logger)
    if not active_model:
        return {"status": "NO_BACKEND", "phase": phase, "artifact": artifact,
                "error": f"sem slot vivo para {category}"}

    # Panteão de validadores (R28)
    validators = {
        "autophagy": lambda d: _evaluate_pillar("autophagy", d, logger),
        "decompilation": lambda d: _evaluate_pillar("decompilation", d, logger),
        "helenization": lambda d: _evaluate_pillar("helenization", d, logger),
        "forging": lambda d: _evaluate_pillar("forging", d, logger),
    }
    scores = {pillar: fn(payload) for pillar, fn in validators.items()}
    total_score = sum(item["score"] for item in scores.values()) / len(scores)
    loop_terminated = total_score > 95.0

    return {
        "agent": "hefesto-motor",
        "version": "2.0.0",
        "artifact": artifact,
        "phase": phase,
        "category": category,
        "active_model": active_model,
        "gabarito_validado": True,
        "pantheon_audit": scores,
        "average_score": round(total_score, 5),
        "dev_loop_terminated": loop_terminated,
        "status": "OLYMPIAN_PERFECTION" if loop_terminated else "FREEZE_PAUSE_REQUIRED",
    }


def main():
    parser = argparse.ArgumentParser(description="Hefesto Motor v2.0.0 (Dispatcher)")
    parser.add_argument("--list-cpu", action="store_true", help="Listar slots CPU vivos (R35)")
    parser.add_argument("--resolve", type=str, help="Resolver categoria → slot (R75)")
    parser.add_argument("--execute", type=str, help="Executar workflow (JSON)")
    args = parser.parse_args()
    logger = setup_logger()

    if args.list_cpu:
        slots = list_cpu_slots(logger)
        print(json.dumps({"cpu_slots": slots}, indent=2, ensure_ascii=False))
        return 0

    if args.resolve:
        slot = resolve_slot_for_role(args.resolve, logger)
        if not slot:
            print(json.dumps({"error": f"categoria {args.resolve} indisponível"}, ensure_ascii=False))
            return 1
        print(json.dumps(slot, indent=2, ensure_ascii=False))
        return 0

    if args.execute:
        try:
            payload = json.loads(args.execute)
        except json.JSONDecodeError:
            print(json.dumps({"error": "JSON inválido"}, ensure_ascii=False))
            return 1
        result = execute_workflow(payload, logger)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("status") in ("OLYMPIAN_PERFECTION", "FREEZE_PAUSE_REQUIRED") else 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())