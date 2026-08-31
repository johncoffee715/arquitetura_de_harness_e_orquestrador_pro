#!/usr/bin/env python3
"""llm-inventory.py — motor do Inventário Global de LLMs Locais (R52).

Fonte de verdade: config/opencode/harness/llm-inventory.json
Uso:
  llm-inventory.py --all                 # tabela da stack inteira (categoria/setor/status)
  llm-inventory.py --resolve <feature>   # melhor modelo por amálgama (cruzando saúde do slot)
  llm-inventory.py --probe               # health dos slots online/offline
  llm-inventory.py --show <id>           # ficha completa de um modelo
  llm-inventory.py --register <arquivo.gguf> --slot PORT --category ROLE
                                        # auto-cataloga novo LLM via header GGUF (R52 + R27)
  llm-inventory.py --validate            # sanidade do JSON (ids únicos, campos, notas 0-5)
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

CONFIG = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode")
INV_PATH = CONFIG / "harness" / "llm-inventory.json"
MODELS_DIR = Path("/mnt/dados/Assistente Pessoal/modelos LLM")

# chaves canônicas do amálgama (R52)
FEATURES = [
    "skill-prosa", "skill-tecnica", "skill-guardrail", "subagent-executor", "judge", "tool-calling",
    "gbnf-estrutura", "reflexo-r42", "criativo-f1", "contexto-longo", "memoria",
    "refutacao-r40",
]

CATEGORIES = {
    "orquestrador", "descoberta", "executor", "judge", "reflexo", "prosa",
    "tool-leve", "refutacao", "contrato-plano", "talamus-cortex",
}

# Roteamento canônico feature -> categoria de modelo (R65/R71, grafo cerebral)
FEATURE_CATEGORY_MAP = {
    "skill-prosa": "prosa",
    "skill-tecnica": "contrato-plano",
    "skill-guardrail": "contrato-plano",
    "subagent-executor": "executor",
    "judge": "judge",
    "tool-calling": "tool-leve",
    "gbnf-estrutura": "prosa",
    "reflexo-r42": "reflexo",
    "criativo-f1": "prosa",
    "contexto-longo": "executor",
    "memoria": "talamus-cortex",
    "refutacao-r40": "refutacao",
}


def load():
    with open(INV_PATH, encoding="utf-8") as f:
        return json.load(f)


def probe(port, timeout=2):
    try:
        out = subprocess.run(
            ["curl", "-sf", "-m", str(timeout), f"http://127.0.0.1:{port}/health"],
            capture_output=True, text=True, timeout=timeout + 1,
        ).returncode == 0
        return out
    except Exception:
        return False


def cmd_all():
    inv = load()
    print(f"{'ID':24s} {'SLOT':5s} {'CATEGORIA':16s} {'SETOR':18s} {'STATUS':8s} {'AFINIDADE-MAX':14s}")
    for m in sorted(inv["models"], key=lambda x: x["slot"]):
        best = m.get("category", "?")
        print(f"{m['id']:24s} {m['slot']:5s} {m['category']:16s} {m.get('sector', '-'):18s} "
              f"{m.get('status', '?'):8s} {best}={m.get('affinity', {}).get(best, '-')}")


def cmd_probe():
    inv = load()
    failed = []
    for m in inv["models"]:
        alive = probe(m["slot"])
        status = "online" if alive else "OFFLINE (probe)"
        if not alive:
            failed.append(m["slot"])
        print(f"{m['slot']:5s} {m['id']:24s} -> {status}")
    if failed:
        print(f"atencao: slots mortos {failed} (R9/R10: refatorar rota antes de resolve)")
    else:
        print("health: todos vivos")


def cmd_resolve(feature):
    if feature not in FEATURES:
        sys.exit(f"feature invalida. Escolha: {', '.join(FEATURES)}")
    inv = load()
    scored = []
    target_cat = FEATURE_CATEGORY_MAP.get(feature)
    for m in inv["models"]:
        # pontua por categoria canônica (grafo cerebral R65/R71) — o JSON de models não tem affinity
        if target_cat is None:
            continue
        base = 5.0 if m.get("category") == target_cat else 1.0
        alive = probe(m["slot"])
        score = base + (0.5 if alive else 0.0)
        scored.append((score, alive, m))
    # B-D01: slot OFFLINE não pode ser o "melhor" (R9/R52: rota morta não é rota)
    live = [x for x in scored if x[1]]
    dead = [x for x in scored if not x[1]]
    ranked = sorted(live, key=lambda x: (-x[0], str(x[2]["slot"]))) + sorted(dead, key=lambda x: (-x[0], str(x[2]["slot"])))
    print(f"AMALGAMA '{feature}' (feature->categoria '{target_cat}', cruzando saude do slot — R52/R65)")
    for score, alive, m in scored:
        print(f"  {score:4.1f} {'ON ' if alive else 'OFF'} {m['id']:24s} ctx={m['ctx_allocated']:7d} "
              f"KB/tok={m['kb_per_tok']:5.1f} | cat={m['category']}")
    best = ranked[0] if ranked else None
    if best:
        print(f"-> melhor: {best[2]['id']} (amalgama {best[0]:.1f}, slot :{best[2]['slot']})")
    else:
        print("-> nenhum modelo elegivel (feature sem categoria mapeada)")


# afinidade de SKILLS por feature (catálogo — R8/R52)
def cmd_skills(feature):
    inv = load()
    hits = []
    for s in inv.get("skills", []):
        aff = s.get("affinity", {})
        if isinstance(aff.get(feature), (int, float)):
            hits.append((aff[feature], s["id"]))
    hits.sort(reverse=True)
    print(f"SKILLS com afinidade para '{feature}':")
    for score, sid in hits[:10]:
        print(f"  {score:4.1f} {sid}")


def cmd_show(ident):
    inv = load()
    for m in inv["models"]:
        if m["id"] == ident or str(m["slot"]) == ident:
            print(json.dumps(m, ensure_ascii=False, indent=2))
            return
    sys.exit(f"modelo '{ident}' nao encontrado")


def cmd_register(gguf, slot, category, role=None):
    if category not in CATEGORIES:
        sys.exit(f"categoria invalida. Escolha: {sorted(CATEGORIES)}")
    path = MODELS_DIR / gguf if not (gguf.startswith("/")) else Path(gguf)
    if not path.exists():
        sys.exit(f"arquivo nao encontrado: {path}")
    name = path.stem
    existing = load()
    for m in existing["models"]:
        if m["file"] == path.name or str(m["slot"]) == slot:
            sys.exit(f"ja registrado: {m['id']} (slot {m['slot']}). Atualize manualmente.")
    # header minimo (tamanho gigabytes apenas; topologia completa: ctx-cost.py)
    size_gb = path.stat().st_size / 1e9
    offline = str(slot).lower() in {"none", "offline", "-"}
    entry = {
        "id": name.lower().replace(".gguf", "").replace("_", "-"),
        "slot": str(slot),
        "file": path.name,
        "params": "?", "quant": "?",
        "arch": "?", "n_ctx_train": "?", "ctx_allocated": "?",
        "kb_per_tok": "?",
        "temp": 0.6,
        "category": category,
        "sector": "unassigned" if offline else ("GPU-MI50-Vulkan" if slot == "8083" else "CPU-threads"),
        "status": "offline" if offline else "online",
        "size_gb": round(size_gb, 2),
        "capabilities": [],
        "weaknesses": [],
        "benchmarks": {"status": "UNKNOWN", "source": "registro R52 — preencher via MIX R50 e/ou empiria local", "items": []},
        "empirical": {"reason": "registro inicial — medir t/s e uso real"},
        "affinity": {k: 2 for k in FEATURES},
        "affinity_note": "valores default 2 — refine apos benchmark empirico (R52)",
    }
    existing["models"].append(entry)
    existing["last_updated"] = "2026-08-26"
    with open(INV_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    print(f"registrado {entry['id']} slot:{slot} cat:{category} ({size_gb:.2f} GB). "
          f"NEXT R52: achar bench publico multi-lingua e/ou medir empiricamente antes de usar.")


def cmd_validate():
    inv = load()
    ids, errs = set(), []
    for m in inv["models"]:
        if m["id"] in ids:
            errs.append(f"id duplicado: {m['id']}")
        ids.add(m["id"])
        if m["category"] not in CATEGORIES:
            errs.append(f"{m['id']}: categoria '{m['category']}' fora de {sorted(CATEGORIES)}")
        if not all(k in m for k in ("slot", "file", "n_ctx_train", "ctx_allocated", "kb_per_tok", "status")):
            errs.append(f"{m['id']}: campo obrigatorio ausente")
        if "category" in m and m["category"] == "talamus-cortex" and "talamus-cortex" not in CATEGORIES:
            errs.append(f"{m['id']}: talamus-cortex precisa estar em CATEGORIES")
    # valida skills/features (catálogo)
    for s in inv.get("skills", []):
        if not s.get("id") or not s.get("path"):
            errs.append("skill sem id/path")
    print("VALIDACAO:", "OK" if not errs else ("ERROS:\n" + "\n".join(errs)))
    if errs:
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description="Inventario Global de LLMs Locais (R52)")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--resolve", metavar="FEATURE")
    g.add_argument("--skills", metavar="FEATURE")
    g.add_argument("--probe", action="store_true")
    g.add_argument("--show", metavar="ID|PORT")
    g.add_argument("--register", metavar="MODELO.gguf")
    g.add_argument("--validate", action="store_true")
    p.add_argument("--slot")
    p.add_argument("--category")
    args = p.parse_args()

    if args.all:
        cmd_all()
    elif args.resolve:
        cmd_resolve(args.resolve)
    elif args.skills:
        cmd_skills(args.skills)
    elif args.probe:
        cmd_probe()
    elif args.show:
        cmd_show(args.show)
    elif args.validate:
        cmd_validate()
    elif args.register:
        if not args.slot or not args.category:
            sys.exit("--register exige --slot PORT e --category ROLE")
        cmd_register(args.register, args.slot, args.category)
    else:
        sys.exit("uso: llm-inventory.py --all | --resolve FEATURE | --probe | --show ID | --register GGUF (--slot P --category R) | --validate")


if __name__ == "__main__":
    main()
