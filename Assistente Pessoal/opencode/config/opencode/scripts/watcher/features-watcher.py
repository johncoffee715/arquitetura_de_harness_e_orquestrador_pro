#!/usr/bin/env python3
"""
Features Watcher — Auditoria contínua de features instaladas no ecossistema
R48: Monitoramento Ativo (30s Cycle) · R68: Watchers iniciam com o orquestrador
"""

import json
import os
import sys
from datetime import datetime

WATCHER_NAME = "features-watcher"
BASE_PATH = "/mnt/dados/Assistente Pessoal/opencode/config/opencode"
STATE_PATH = "/mnt/dados/Assistente Pessoal/opencode/state"
LOG_PATH = os.path.join(STATE_PATH, "watcher", "features.log")


def log(msg: str) -> None:
    ts = datetime.now().isoformat()
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(f"[{ts}] [{WATCHER_NAME}] {msg}\n")


def audit_features() -> dict:
    """Audita todas as features instaladas no ecossistema."""
    features = {"skills": [], "agents": [], "hooks": [], "plugins": [], "scripts": []}

    # Skills
    skills_dir = os.path.join(BASE_PATH, "skills")
    if os.path.isdir(skills_dir):
        for item in sorted(os.listdir(skills_dir)):
            skill_file = os.path.join(skills_dir, item, "SKILL.md")
            if os.path.isfile(skill_file):
                features["skills"].append({
                    "name": item,
                    "path": skill_file,
                    "size": os.path.getsize(skill_file),
                    "status": "active" if os.path.getsize(skill_file) > 0 else "empty"
                })

    # Agents (arquivos .md na raiz + subdiretórios)
    agents_dir = os.path.join(BASE_PATH, "agent")
    if os.path.isdir(agents_dir):
        for root, dirs, files in os.walk(agents_dir):
            for f in sorted(files):
                if f.endswith(".md"):
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, agents_dir)
                    features["agents"].append({
                        "name": rel.replace(".md", ""),
                        "path": full,
                        "size": os.path.getsize(full),
                        "status": "active" if os.path.getsize(full) > 0 else "empty"
                    })

    # Hooks (arquivos .py na raiz + subdiretórios)
    hooks_dir = os.path.join(BASE_PATH, "hooks")
    if os.path.isdir(hooks_dir):
        for root, dirs, files in os.walk(hooks_dir):
            for f in sorted(files):
                if f.endswith(".py") and "__pycache__" not in root:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, hooks_dir)
                    features["hooks"].append({
                        "name": rel.replace(".py", ""),
                        "path": full,
                        "size": os.path.getsize(full),
                        "status": "active" if os.path.getsize(full) > 0 else "empty"
                    })

    # Plugins
    plugins_dir = os.path.join(BASE_PATH, "plugins")
    if os.path.isdir(plugins_dir):
        for f in sorted(os.listdir(plugins_dir)):
            full = os.path.join(plugins_dir, f)
            if os.path.isfile(full):
                features["plugins"].append({
                    "name": f,
                    "path": full,
                    "size": os.path.getsize(full),
                    "status": "active" if os.path.getsize(full) > 0 else "empty"
                })

    # Scripts (.py/.sh/.ts na raiz + subdiretórios)
    scripts_dir = os.path.join(BASE_PATH, "scripts")
    if os.path.isdir(scripts_dir):
        for root, dirs, files in os.walk(scripts_dir):
            for f in sorted(files):
                if f.endswith((".py", ".sh", ".ts")) and "__pycache__" not in root:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, scripts_dir)
                    features["scripts"].append({
                        "name": rel,
                        "path": full,
                        "size": os.path.getsize(full),
                        "status": "active" if os.path.getsize(full) > 0 else "empty"
                    })

    return features


def find_issues(features: dict) -> list:
    """Identifica features com problemas (vazias, quebradas, órfãs do registry)."""
    issues = []
    for category, items in features.items():
        for item in items:
            if item["status"] == "empty":
                issues.append(f"[{category}] {item['name']} — arquivo VAZIO (0 bytes)")
            if item["size"] < 10:
                issues.append(f"[{category}] {item['name']} — arquivo suspeito ({item['size']} bytes)")
    return issues


if __name__ == "__main__":
    features = audit_features()
    total = sum(len(v) for v in features.values())
    issues = find_issues(features)

    os.makedirs(os.path.join(STATE_PATH, "watcher"), exist_ok=True)
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "total_features": total,
        "breakdown": {k: len(v) for k, v in features.items()},
        "issues": issues,
        "healthy": len(issues) == 0
    }

    # Persistir snapshot
    with open(os.path.join(STATE_PATH, "watcher", "features-state.json"), "w") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    log(f"Auditoria: {total} features | issues={len(issues)} | healthy={snapshot['healthy']}")

    if "--json" in sys.argv:
        print(json.dumps(snapshot, indent=2, ensure_ascii=False))
    else:
        print(f"Features totais: {total}")
        for k, v in snapshot["breakdown"].items():
            print(f"  {k}: {v}")
        if issues:
            print("\n⚠️ ISSUES ENCONTRADAS:")
            for i in issues:
                print(f"  - {i}")
        else:
            print("\n✅ Nenhum issue encontrado. Todas as features saudáveis.")

    sys.exit(1 if issues else 0)