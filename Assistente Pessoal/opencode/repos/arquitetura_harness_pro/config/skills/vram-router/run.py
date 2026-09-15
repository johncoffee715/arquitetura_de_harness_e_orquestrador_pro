#!/usr/bin/env python3
"""CLI helenizado: escolhe o melhor LLM local para uma task via MODEL_SCORE."""
import argparse
import json
import sys

sys.path.insert(0, "/mnt/dados/opencode/harness")
from models.router import route

ROLES = ["orchestrator", "planner", "coder", "critic", "reviewer", "judge"]


def main():
    parser = argparse.ArgumentParser(description="Router VRAM-aware de LLMs locais")
    parser.add_argument("--registry", default="/mnt/dados/opencode/benchmark/runs/registry.json")
    parser.add_argument("--role", required=True, choices=ROLES)
    parser.add_argument("--ctx", type=int, default=4096,
                        help="needed_ctx_tokens (escada progressiva até 192K)")
    parser.add_argument("--gpu-used", type=float, default=0.0)
    parser.add_argument("--top", type=int, default=3)
    args = parser.parse_args()

    with open(args.registry, encoding="utf-8") as fh:
        registry = json.load(fh)

    task = {"role": args.role, "needed_ctx_tokens": args.ctx}
    ranked = route(registry["models"], task, gpu_used_gib=args.gpu_used)
    if not ranked:
        print(f"UNSCHEDULABLE: role={args.role} ctx={args.ctx} fora da escada 64K-192K ou sem SAFE_LOAD")
        raise SystemExit(1)
    for item in ranked[: args.top]:
        need = item["vram_detail"]["need_gib"]
        basis = item["vram_detail"].get("basis", "?")
        print(f"[{item['level']:9}] {item['model_id'][:40]:40} score={item['score']:.3f} "
              f"resid={item['residency']:4} need={need}G({basis})")


if __name__ == "__main__":
    main()
