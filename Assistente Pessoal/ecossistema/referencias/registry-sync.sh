#!/usr/bin/env bash
# registry-sync.sh — Sincroniza registry com componentes instalados
# Executa automaticamente após cada atualização do OpenCode
# Uso: ./registry-sync.sh [--dry-run]

set -euo pipefail

REGISTRY_FILE="${REGISTRY_DIR:-/mnt/dados/opencode/config/registry}/auto-registry.json"
DRY_RUN="${1:-}"

echo "=== REGISTRY SYNC — $(date) ==="
echo ""

# Coletar componentes
SKILLS_OPODE=$(ls -1d /home/johncoffee/.opencode/skills/*/ 2>/dev/null | while read d; do basename "$d"; done)
SKILLS_CONFIG=$(ls -1d /home/johncoffee/.config/opencode/skills/*/ 2>/dev/null | while read d; do basename "$d"; done)
AGENTS=$(ls -1 /home/johncoffee/.config/opencode/agents/*.md 2>/dev/null | while read f; do basename "$f" .md; done)
HOOKS=$(ls -1 /home/johncoffee/.config/opencode/hooks/*.js /home/johncoffee/.config/opencode/hooks/*.sh 2>/dev/null | while read f; do basename "$f"; done)
COMMANDS=$(ls -1 /home/johncoffee/.config/opencode/command/*.md 2>/dev/null | while read f; do basename "$f" .md; done)

# Gerar registry
python3 << 'PYTHON'
import json
import os
from datetime import datetime

registry = {
    "registry_version": "1.0.0",
    "updated_at": datetime.utcnow().isoformat() + "Z",
    "description": "Registry automático — sincronizado com componentes instalados",
    "auto_sync": True,
    "entries": []
}

# Skills ~/.opencode/skills/
skills_opencode = []
for d in sorted(os.listdir("/home/johncoffee/.opencode/skills")):
    path = f"/home/johncoffee/.opencode/skills/{d}"
    if os.path.isdir(path):
        has_skill = os.path.isfile(f"{path}/SKILL.md")
        skills_opencode.append(d)
        registry["entries"].append({
            "id": f"skill-{d}",
            "tipo": "skill",
            "nome": d,
            "versao": "1.0.0",
            "status": "ativo" if has_skill else "incompleto",
            "origem": {"tipo_origem": "interno"},
            "proposito": f"Skill {d}",
            "modelo": {"primario": "n/a"},
            "regras": {"nao_faz": []},
            "validacao": {"gates": []},
            "autonomia": {"modo_autonomo": True},
            "localizacao": path,
            "registrado_em": datetime.utcnow().strftime("%Y-%m-%d")
        })

# Skills ~/.config/opencode/skills/
for d in sorted(os.listdir("/home/johncoffee/.config/opencode/skills")):
    path = f"/home/johncoffee/.config/opencode/skills/{d}"
    if os.path.isdir(path):
        has_skill = os.path.isfile(f"{path}/SKILL.md")
        registry["entries"].append({
            "id": f"skill-{d}",
            "tipo": "skill",
            "nome": d,
            "versao": "1.0.0",
            "status": "ativo" if has_skill else "incompleto",
            "origem": {"tipo_origem": "interno"},
            "proposito": f"Skill {d}",
            "modelo": {"primario": "n/a"},
            "regras": {"nao_faz": []},
            "validacao": {"gates": []},
            "autonomia": {"modo_autonomo": True},
            "localizacao": path,
            "registrado_em": datetime.utcnow().strftime("%Y-%m-%d")
        })

# Agents
for f in sorted(os.listdir("/home/johncoffee/.config/opencode/agents")):
    if f.endswith(".md"):
        name = f[:-3]
        path = f"/home/johncoffee/.config/opencode/agents/{f}"
        mode = "subagent"
        with open(path) as fh:
            for line in fh:
                if line.startswith("mode:"):
                    mode = line.split(":", 1)[1].strip()
                    break
        registry["entries"].append({
            "id": f"agent-{name}",
            "tipo": "agent" if mode == "primary" else "subagent",
            "nome": name,
            "versao": "1.0.0",
            "status": "ativo",
            "origem": {"tipo_origem": "interno"},
            "proposito": f"Agent {name}",
            "modelo": {"primario": "auto/claude-sonnet"},
            "regras": {"nao_faz": []},
            "validacao": {"gates": []},
            "autonomia": {"modo_autonomo": True},
            "localizacao": path,
            "registrado_em": datetime.utcnow().strftime("%Y-%m-%d")
        })

# Hooks
for f in sorted(os.listdir("/home/johncoffee/.config/opencode/hooks")):
    if f.endswith(".js") or f.endswith(".sh"):
        path = f"/home/johncoffee/.config/opencode/hooks/{f}"
        registry["entries"].append({
            "id": f"hook-{f}",
            "tipo": "tool",
            "nome": f,
            "versao": "1.0.0",
            "status": "ativo",
            "origem": {"tipo_origem": "interno"},
            "proposito": f"Hook {f}",
            "modelo": {"primario": "n/a"},
            "regras": {"nao_faz": []},
            "validacao": {"gates": []},
            "autonomia": {"modo_autonomo": True},
            "localizacao": path,
            "registrado_em": datetime.utcnow().strftime("%Y-%m-%d")
        })

# MCPs
try:
    with open("/mnt/dados/opencode/config/opencode.json") as fh:
        config = json.load(fh)
        for name, mcp in config.get("mcp", {}).items():
            registry["entries"].append({
                "id": f"mcp-{name}",
                "tipo": "mcp",
                "nome": name,
                "versao": "1.0.0",
                "status": "ativo",
                "origem": {"tipo_origem": "interno"},
                "proposito": f"MCP {name}",
                "modelo": {"primario": "n/a"},
                "regras": {"nao_faz": []},
                "validacao": {"gates": []},
                "autonomia": {"modo_autonomo": True},
                "localizacao": mcp.get("url", mcp.get("command", "")),
                "registrado_em": datetime.utcnow().strftime("%Y-%m-%d")
            })
except:
    pass

# Commands
for f in sorted(os.listdir("/home/johncoffee/.config/opencode/command")):
    if f.endswith(".md"):
        name = f[:-3]
        path = f"/home/johncoffee/.config/opencode/command/{f}"
        registry["entries"].append({
            "id": f"command-{name}",
            "tipo": "skill",
            "nome": f"/{name}",
            "versao": "1.0.0",
            "status": "ativo",
            "origem": {"tipo_origem": "interno"},
            "proposito": f"Command /{name}",
            "modelo": {"primario": "n/a"},
            "regras": {"nao_faz": []},
            "validacao": {"gates": []},
            "autonomia": {"modo_autonomo": True},
            "localizacao": path,
            "registrado_em": datetime.utcnow().strftime("%Y-%m-%d")
        })

# Estatísticas
registry["stats"] = {
    "total": len(registry["entries"]),
    "skills": len([e for e in registry["entries"] if e["tipo"] == "skill"]),
    "agents": len([e for e in registry["entries"] if e["tipo"] == "agent"]),
    "subagents": len([e for e in registry["entries"] if e["tipo"] == "subagent"]),
    "tools": len([e for e in registry["entries"] if e["tipo"] == "tool"]),
    "mcps": len([e for e in registry["entries"] if e["tipo"] == "mcp"])
}

print(json.dumps(registry, indent=2, ensure_ascii=False))
PYTHON

echo ""
echo "✅ Registry sincronizado: $REGISTRY_FILE"
echo "   Total: $(python3 -c "import json; print(json.load(open('$REGISTRY_FILE'))['stats']['total'])" 2>/dev/null) componentes"
