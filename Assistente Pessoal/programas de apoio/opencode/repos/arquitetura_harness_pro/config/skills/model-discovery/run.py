#!/usr/bin/env python3
"""CLI helenizado: varre o MODEL_LIBRARY e (re)gera o registry."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, "/mnt/dados/opencode/harness")
from models.discovery import MODELS_DIR, scan_models_dir, write_registry


def main():
    parser = argparse.ArgumentParser(description="Discovery Engine — registry de LLMs locais")
    parser.add_argument("--dir", default=str(MODELS_DIR))
    parser.add_argument("--out", default="/mnt/dados/opencode/benchmark/runs/registry.json")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    registry = scan_models_dir(args.dir)
    prev_path = Path(args.out)
    if prev_path.exists():
        try:
            prev = json.loads(prev_path.read_text(encoding="utf-8")).get("models", {})
        except Exception:
            prev = {}
        for gid, entry in registry["models"].items():
            old = prev.get(gid)
            if not old:
                continue
            c_new = entry.setdefault("capabilities", {})
            c_old = old.get("capabilities", {}) or {}
            if not c_new.get("measured") and c_old.get("measured"):
                c_new["measured"] = c_old["measured"]
            if not c_new.get("confidence") and c_old.get("confidence"):
                c_new["confidence"] = c_old["confidence"]
            if old.get("runtime"):
                entry["runtime"] = old["runtime"]
            ph_old = old.get("performance_history") or {}
            ph_new = entry.setdefault("performance_history", {})
            for k, v in ph_old.items():
                if v not in (None, 0):
                    ph_new[k] = v
            h_old = old.get("health") or {}
            h_new = entry.setdefault("health", {})
            if h_old.get("consecutive_failures", 0) > h_new.get("consecutive_failures", 0):
                h_new["consecutive_failures"] = h_old["consecutive_failures"]
    out_path = write_registry(registry, args.out)
    if args.quiet:
        return
    total = registry["total_models"]
    print(f"{total} modelos | {registry['available_models']} aptos | "
          f"{registry['excluded_models']} excluidos -> {out_path}")
    for gid, entry in sorted(registry["models"].items()):
        status = entry["status"]
        flag = "OK " if status["available"] else "EXC"
        vram = entry.get("resources", {}).get("estimated_vram_gib", "-")
        health = entry["health"]["status"]
        reason = status.get("exclusion_reason") or ""
        print(f"{flag} {gid[:42]:42} {health:6} v32K={str(vram):5} {reason[:48]}")


if __name__ == "__main__":
    main()
