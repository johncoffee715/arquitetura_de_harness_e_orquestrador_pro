#!/usr/bin/env python3
"""
SESSION_DIFF.py — Compara dois manifests SHA-256 e mostra o delta.
Uso:
  python3 SESSION_DIFF.py .manifest.json .manifest.json.bak
  python3 SESSION_DIFF.py                     # auto: .manifest.json vs .manifest.json.bak
"""
import json, sys, os
from datetime import datetime

VAULT = "/mnt/dados/cerebro com IA"

def load_manifest(path):
    with open(path) as f:
        return json.load(f)

def diff_manifests(before, after):
    added = {}
    modified = {}
    deleted = {}
    unchanged = 0

    all_keys = set(list(before.keys()) + list(after.keys()))

    for key in sorted(all_keys):
        if key not in before:
            added[key] = after[key]
        elif key not in after:
            deleted[key] = before[key]
        elif before[key]["hash"] != after[key]["hash"]:
            modified[key] = {"old": before[key]["hash"][:12], "new": after[key]["hash"][:12]}
        else:
            unchanged += 1

    return added, modified, deleted, unchanged

def print_report(before_path, after_path):
    before = load_manifest(before_path)
    after = load_manifest(after_path)

    added, modified, deleted, unchanged = diff_manifests(before, after)

    print("=" * 56)
    print("  SESSION DIFF — Delta Tracking Neural")
    print("=" * 56)
    print(f"  Antes: {before_path}")
    print(f"  Depois: {after_path}")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    if added:
        print(f"  ➕ NEURÔNIOS NOVOS ({len(added)}):")
        for k, v in added.items():
            links = len(v.get("links", []))
            size = v.get("size", 0)
            print(f"    + {k:50s} ({size} bytes, {links} links)")
    else:
        print("  ➕ Nenhum neurônio novo")
    print()

    if modified:
        print(f"  ✏️  NEURÔNIOS MODIFICADOS ({len(modified)}):")
        for k, v in modified.items():
            print(f"    ~ {k:50s} {v['old']} → {v['new']}")
    else:
        print("  ✏️  Nenhum neurônio modificado")
    print()

    if deleted:
        print(f"  ❌ NEURÔNIOS DELETADOS ({len(deleted)}):")
        for k in deleted:
            print(f"    - {k}")
    else:
        print("  ❌ Nenhum neurônio deletado")
    print()

    print(f"  Inalterados: {unchanged}")
    total_before = len(before)
    total_after = len(after)
    print(f"  Total antes: {total_before} → depois: {total_after}")
    print()

    # Cohesion delta
    def cohesion(m):
        n = len(m)
        synapses = sum(len(v.get("links", [])) for v in m.values())
        max_p = n * (n - 1) / 2 if n > 1 else 1
        return synapses / max_p if max_p > 0 else 0

    c_before = cohesion(before)
    c_after = cohesion(after)
    delta = c_after - c_before
    arrow = "📈" if delta > 0 else "📉" if delta < 0 else "➡️"
    print(f"  Coesão: {c_before:.4f} → {c_after:.4f} ({delta:+.4f}) {arrow}")
    print("=" * 56)

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) >= 2:
        print_report(args[0], args[1])
    else:
        before_path = os.path.join(VAULT, ".manifest.json.bak")
        after_path = os.path.join(VAULT, ".manifest.json")

        if not os.path.exists(before_path):
            print("❌ .manifest.json.bak não encontrado.")
            print("   Crie um snapshot: cp .manifest.json .manifest.json.bak")
            sys.exit(1)

        print_report(before_path, after_path)
