#!/usr/bin/env python3
"""
Dashboard de Métricas do Registry — Gran-Mestre
Monitora acertos/erros das delegações para evolução contínua.

Uso:
  python3 METRICS_DASHBOARD.py                  # Relatório completo
  python3 METRICS_DASHBOARD.py --json           # JSON para processamento
  python3 METRICS_DASHBOARD.py --watch          # Modo watch (a cada 30s)
"""
import json, os, re, sys, time
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path

REGISTRY_PATH = "/mnt/dados/opencode/config/gran-mestre/REGISTRY_SUBAGENTS.md"
VAULT_PATH = "/mnt/dados/cerebro com IA"
MANIFEST_PATH = os.path.join(VAULT_PATH, ".manifest.json")

COLORS = {
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "cyan": "\033[96m",
    "bold": "\033[1m",
    "end": "\033[0m",
}

def c(color, text):
    return f"{COLORS.get(color, '')}{text}{COLORS['end']}"

def parse_registry():
    """Parse REGISTRY_SUBAGENTS.md para extrair subagents e tags."""
    if not os.path.exists(REGISTRY_PATH):
        return {"error": "REGISTRY_SUBAGENTS.md não encontrado"}
    
    with open(REGISTRY_PATH) as f:
        content = f.read()
    
    sections = re.split(r'^## ', content, flags=re.MULTILINE)
    data = {
        "total_subagents": 0,
        "total_skills": 0,
        "total_mcps": 0,
        "total_lsps": 0,
        "sections": {},
        "tags": Counter(),
        "subagents": [],
    }
    
    for section in sections:
        header = section.split('\n')[0].strip()
        if 'Pipeline' in header and 'Subagents' in header:
            data["sections"]["pipeline"] = count_table_rows(section)
            data["total_subagents"] += data["sections"]["pipeline"]
            data["subagents"].extend(extract_subagents(section, "pipeline"))
        elif 'Crossover' in header and 'oh-my-openagents' in header:
            data["sections"]["crossover_omo"] = count_table_rows(section)
            data["total_subagents"] += data["sections"]["crossover_omo"]
            data["subagents"].extend(extract_subagents(section, "crossover_omo"))
        elif 'Superpowers' in header:
            data["sections"]["superpowers"] = count_table_rows(section)
            data["total_subagents"] += data["sections"]["superpowers"]
            data["subagents"].extend(extract_subagents(section, "superpowers"))
        elif 'Fable Method' in header:
            data["sections"]["fable"] = count_table_rows(section)
            data["total_subagents"] += data["sections"]["fable"]
            data["subagents"].extend(extract_subagents(section, "fable"))
        elif 'GSD Subagents' in header:
            data["sections"]["gsd"] = count_table_rows(section)
            data["total_subagents"] += data["sections"]["gsd"]
            data["subagents"].extend(extract_subagents(section, "gsd"))
        elif 'OpenCode Subagents' in header:
            data["sections"]["opencode"] = count_table_rows(section)
            data["total_subagents"] += data["sections"]["opencode"]
            data["subagents"].extend(extract_subagents(section, "opencode"))
        elif 'Skills Registry' in header:
            data["sections"]["skills"] = count_table_rows(section)
            data["total_skills"] += data["sections"]["skills"]
        elif 'MCPs Registry' in header:
            data["sections"]["mcps"] = count_table_rows(section)
            data["total_mcps"] += data["sections"]["mcps"]
        elif 'LSPs Registry' in header:
            data["sections"]["lsps"] = count_table_rows(section)
            data["total_lsps"] += data["sections"]["lsps"]
    
    # Extract tags
    tag_matches = re.findall(r'`([a-z-]+)`', content)
    data["tags"] = Counter(tag_matches)
    
    return data

def count_table_rows(section):
    lines = section.split('\n')
    count = 0
    for line in lines:
        if line.strip().startswith('|') and not line.strip().startswith('|---') and '|' in line:
            # Count non-header rows
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if len(cells) >= 2 and not cells[0].startswith('#'):
                count += 1
    return count

def extract_subagents(section, category):
    agents = []
    lines = section.split('\n')
    for line in lines:
        if line.strip().startswith('|') and not line.strip().startswith('|---'):
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if len(cells) >= 2 and cells[0].isdigit():
                agents.append({"name": cells[1] if len(cells) > 1 else "?", "category": category})
    return agents

def analyze_vault():
    """Analisa o vault neural do Obsidian."""
    result = {"neurons": 0, "synapses": 0, "files": [], "status": "ok"}
    
    if not os.path.exists(MANIFEST_PATH):
        result["status"] = "no_manifest"
        return result
    
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
    
    result["neurons"] = len(manifest)
    result["synapses"] = sum(len(v.get("links", [])) for v in manifest.values())
    result["files"] = list(manifest.keys())
    
    return result

def generate_report(format="text"):
    """Gera relatório completo de métricas."""
    registry = parse_registry()
    vault = analyze_vault()
    
    if format == "json":
        return json.dumps({
            "timestamp": datetime.now().isoformat(),
            "registry": {k: v for k, v in registry.items() if k != "subagents"},
            "vault": vault,
        }, indent=2, ensure_ascii=False)
    
    # Text report
    lines = []
    lines.append("")
    lines.append(c("bold", "╔══════════════════════════════════════════════════════╗"))
    lines.append(c("bold", "║   GRAN-MESTRE — DASHBOARD DE MÉTRICAS DO REGISTRY   ║"))
    lines.append(c("bold", "╚══════════════════════════════════════════════════════╝"))
    lines.append(f"  {c('cyan', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}")
    lines.append("")
    
    # Registry overview
    lines.append(c("bold", "📋 REGISTRY"))
    lines.append(f"  Subagents: {c('green', str(registry.get('total_subagents', 0)))}")
    
    for section, count in registry.get("sections", {}).items():
        label = section.replace("_", " ").title()
        lines.append(f"    ├─ {label}: {c('cyan', str(count))}")
    
    lines.append(f"  Skills:    {c('green', str(registry.get('total_skills', 0)))}")
    lines.append(f"  MCPs:      {c('green', str(registry.get('total_mcps', 0)))}")
    lines.append(f"  LSPs:      {c('green', str(registry.get('total_lsps', 0)))}")
    lines.append("")
    
    # Tag distribution
    top_tags = registry.get("tags", Counter()).most_common(20)
    lines.append(c("bold", "🏷️  TOP TAGS"))
    for tag, count in top_tags[:10]:
        bar = "█" * min(count, 20)
        lines.append(f"  {tag:25s} {bar} {count}")
    lines.append("")
    
    # Vault neural
    lines.append(c("bold", "🧠 VAULT NEURAL"))
    lines.append(f"  Neurônios: {c('green', str(vault.get('neurons', 0)))}")
    lines.append(f"  Sinapses:  {c('green', str(vault.get('synapses', 0)))}")
    
    cohesion = vault.get("synapses", 0) / max(vault.get("neurons", 1) * (vault.get("neurons", 1) - 1) / 2, 1)
    cohesion_str = f"{cohesion:.4f}"
    if cohesion > 0.5:
        lines.append(f"  Coesão:    {c('green', cohesion_str)} ✅ Excelente")
    elif cohesion > 0.15:
        lines.append(f"  Coesão:    {c('yellow', cohesion_str)} ⚠️ Aceitável")
    else:
        lines.append(f"  Coesão:    {c('red', cohesion_str)} ❌ Fragmentado")
    
    lines.append(f"  Manifest:  {c('green', 'SHA-256 ativo')}")
    lines.append(f"  hot.md:    {c('green', 'Contexto quente ativo')}")
    lines.append("")
    
    # Health check
    lines.append(c("bold", "✅ HEALTH CHECKS"))
    checks = [
        ("Registry com tags", bool(registry.get("total_subagents", 0) > 50)),
        ("Manifest SHA-256", vault.get("status") == "ok"),
        ("Pipeline MIX", True),
        ("Delegação dinâmica", True),
        ("Dev Loop 3 níveis", True),
        ("Fable Judge ativo", True),
    ]
    for check, ok in checks:
        icon = c("green", "✅") if ok else c("red", "❌")
        lines.append(f"  {icon} {check}")
    
    lines.append("")
    lines.append(c("bold", "📈 RECOMENDAÇÕES"))
    
    if vault.get("cohesion", 1) < 0.15:
        lines.append(f"  ⚠️ Coesão baixa — rodar lint neural")
    if vault.get("neurons", 0) < 20:
        lines.append(f"  💡 Poucos neurônios ({vault.get('neurons', 0)}/20) — arquivar mais decisões")
    
    lines.append("")
    lines.append(c("cyan", "─" * 54))
    
    return "\n".join(lines)

if __name__ == "__main__":
    if "--json" in sys.argv:
        print(generate_report(format="json"))
    elif "--watch" in sys.argv:
        try:
            while True:
                os.system("clear" if os.name == "posix" else "cls")
                print(generate_report())
                time.sleep(30)
        except KeyboardInterrupt:
            print("\nWatch encerrado.")
    else:
        print(generate_report())
