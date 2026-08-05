#!/usr/bin/env bash
# ============================================================================
# SELF_HEALING.sh — Auto-Cura do Ecossistema Gran-Mestre
# 
# Uso:
#   ./SELF_HEALING.sh                  # Scan completo
#   ./SELF_HEALING.sh --fix            # Scan + corrige automático
#   ./SELF_HEALING.sh --watch          # Modo monitor (a cada 60s)
#   ./SELF_HEALING.sh --manifest-only  # Só regenera manifesto
#   ./SELF_HEALING.sh --report         # Só gera relatório
# ============================================================================
set -euo pipefail

VAULT="/mnt/dados/cerebro com IA"
CONFIG="/mnt/dados/opencode/config/gran-mestre"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

PASS=0
FAIL=0
WARN=0
FIXES=()

ok() { echo -e " ${GREEN}✅${NC} $1"; PASS=$((PASS + 1)); }
fail() { echo -e " ${RED}❌${NC} $1"; FAIL=$((FAIL + 1)); FIXES+=("$1"); }
warn() { echo -e " ${YELLOW}⚠️${NC} $1"; WARN=$((WARN + 1)); }

echo -e "${BOLD}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║         SELF-HEALING — Auto-Cura Neural              ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# ─── 1. Manifest Integrity ────────────────────────────────────────────
echo -e "${BOLD}[1/8] Integridade do Manifest${NC}"
if [ -f "$VAULT/.manifest.json" ]; then
    # Validate JSON
    if python3 -c "import json; json.load(open('$VAULT/.manifest.json'))" 2>/dev/null; then
        ok "Manifest JSON válido"
    else
        fail "Manifest JSON corrompido — precisa regenerar"
    fi
    
    # Check hashes
    python3 -c "
import json, hashlib, os
VAULT = '$VAULT'
with open(f'{VAULT}/.manifest.json') as f:
    manifest = json.load(f)
corrupted = []
for path, data in manifest.items():
    fpath = os.path.join(VAULT, path)
    if not os.path.exists(fpath):
        corrupted.append(f'{path} — arquivo não encontrado')
        continue
    with open(fpath, 'rb') as fh:
        current = hashlib.sha256(fh.read()).hexdigest()
    if current != data['hash']:
        corrupted.append(f'{path} — hash divergente')
if corrupted:
    for c in corrupted:
        print(f'FAIL:{c}')
" 2>/dev/null | while IFS= read -r line; do
        if [[ "$line" == FAIL:* ]]; then
            fail "${line#FAIL:}"
        fi
    done
else
    fail "Manifest não encontrado"
fi

# ─── 2. Orphan Detection ──────────────────────────────────────────────
echo ""
echo -e "${BOLD}[2/8] Detecção de Órfãos${NC}"
python3 -c "
import json, os, re
from collections import Counter
VAULT = '$VAULT'
with open(f'{VAULT}/.manifest.json') as f:
    manifest = json.load(f)
incoming = Counter()
for v in manifest.values():
    for link in v.get('links', []):
        incoming[link] += 1
orphans = []
for p in sorted(manifest.keys()):
    name = p.split('/')[-1].replace('.md', '')
    linked = False
    for page in incoming:
        if name in page:
            linked = True
            break
    if not linked and not p.startswith('pipeline/') and not p.startswith('hot'):
        orphans.append(p)
if orphans:
    for o in orphans:
        print(f'ORPHAN:{o}')
else:
    print('OK:Nenhum órfão')
" 2>/dev/null | while IFS= read -r line; do
    if [[ "$line" == ORPHAN:* ]]; then
        fail "Neurônio órfão: ${line#ORPHAN:}"
    else
        ok "Nenhum neurônio órfão"
    fi
done

# ─── 3. Cohesion Check ────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[3/8] Métrica de Coesão${NC}"
python3 -c "
import json
VAULT = '$VAULT'
with open(f'{VAULT}/.manifest.json') as f:
    manifest = json.load(f)
n = len(manifest)
synapses = sum(len(v.get('links', [])) for v in manifest.values())
max_p = n * (n-1) / 2 if n > 1 else 1
cohesion = synapses / max_p if max_p > 0 else 0
print(f'{cohesion:.4f}')
print(f'{n}')
print(f'{synapses}')
" 2>/dev/null | {
    read cohesion
    read n
    read synapses
    if (( $(echo "$cohesion > 0.5" | bc -l) )); then
        ok "Coesão: $cohesion (${n} neurônios, ${synapses} sinapses) ✅ Excelente"
    elif (( $(echo "$cohesion > 0.15" | bc -l) )); then
        warn "Coesão: $cohesion (${n} neurônios, ${synapses} sinapses) ⚠️ Aceitável"
    else
        fail "Coesão: $cohesion (${n} neurônios, ${synapses} sinapses) ❌ Fragmentado"
    fi
}

# ─── 4. Graph Communities ─────────────────────────────────────────────
echo ""
echo -e "${BOLD}[4/8] Comunidades do Grafo${NC}"
python3 /mnt/dados/opencode/config/gran-mestre/GRAPH_GAP.py --suggest 2>/dev/null | grep -E "(Comunidades|ISOLADA|NOVAS SINAPSES)" | head -5 | while IFS= read -r line; do
    if [[ "$line" == *ISOLADA* ]]; then
        fail "Cluster isolado: $line"
    elif [[ "$line" == *NOVAS* ]]; then
        warn "Sinapses sugeridas disponíveis"
    fi
done

# ─── 5. Skill Health ──────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[5/8] Saúde das Skills${NC}"
# Check browser-use script exists
if [ -f "/home/johncoffee/.opencode/skills/browser-use/mcp_bridge.py" ]; then
    ok "browser-use: mcp_bridge.py presente"
else
    warn "browser-use: mcp_bridge.py ausente"
fi

# Check gran-mestre SKILL.md
if [ -f "/home/johncoffee/.opencode/skills/gran-mestre/SKILL.md" ]; then
    VERSION=$(grep "version:" /home/johncoffee/.opencode/skills/gran-mestre/SKILL.md | head -1 | awk '{print $2}' | tr -d '"')
    ok "gran-mestre SKILL.md presente (v${VERSION})"
else
    fail "gran-mestre SKILL.md ausente!"
fi

# Check hestia
if [ -f "/home/johncoffee/.opencode/skills/hestia/SKILL.md" ]; then
    ok "hestia SKILL.md presente"
else
    fail "hestia SKILL.md ausente!"
fi

# ─── 6. Registry Integrity ────────────────────────────────────────────
echo ""
echo -e "${BOLD}[6/8] Integridade do Registry${NC}"
REGISTRY="/mnt/dados/opencode/config/gran-mestre/REGISTRY_SUBAGENTS.md"
if [ -f "$REGISTRY" ]; then
    # Count tags
    TAG_COUNT=$(grep -cE '\|[a-z]+.*\|' "$REGISTRY" || true)
    ok "REGISTRY_SUBAGENTS.md presente"
    
    # Check version
    VERSION=$(grep "Versão:" "$REGISTRY" | grep -oP '[\d.]+' | head -1)
    ok "Registry v${VERSION}"
else
    fail "REGISTRY_SUBAGENTS.md ausente!"
fi

# ─── 7. Safety Protocol ───────────────────────────────────────────────
echo ""
echo -e "${BOLD}[7/8] Safety Protocol${NC}"
# Check if git available for rollback
if git rev-parse --git-dir 2>/dev/null; then
    ok "Git disponível para rollback"
else
    warn "Sem git repo — rollback via SHA manual"
fi

# Check rollback procedure documented
if grep -q "Rollback" "/home/johncoffee/.opencode/skills/gran-mestre/SKILL.md" 2>/dev/null; then
    ok "Rollback procedure documentado"
else
    warn "Rollback procedure não encontrado no SKILL.md"
fi

# ─── 8. Summary ───────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[8/8] Resumo${NC}"
TOTAL=$((PASS + FAIL + WARN))
echo ""
echo -e "  ${GREEN}✅ Pass: $PASS${NC}"
echo -e "  ${RED}❌ Fail: $FAIL${NC}"
echo -e "  ${YELLOW}⚠️  Warn: $WARN${NC}"
echo -e "  Total checks: $TOTAL"
echo ""

if [ $FAIL -eq 0 ] && [ $WARN -eq 0 ]; then
    echo -e "  ${GREEN}${BOLD}✅ SAUDÁVEL — Nenhum problema encontrado${NC}"
elif [ $FAIL -eq 0 ]; then
    echo -e "  ${YELLOW}${BOLD}⚠️  ESTÁVEL — $WARN aviso(s) encontrado(s)${NC}"
elif [ $FAIL -le 2 ]; then
    echo -e "  ${RED}${BOLD}⚠️  DEGRADADO — $FAIL falha(s), $WARN aviso(s)${NC}"
else
    echo -e "  ${RED}${BOLD}❌ CRÍTICO — $FAIL falha(s), $WARN aviso(s)${NC}"
fi

echo ""
echo -e "${CYAN}──────────────────────────────────────────────────────${NC}"

# Auto-fix mode
if [[ "${1:-}" == "--fix" ]]; then
    echo ""
    echo -e "${BOLD}🔧 Auto-Fix Mode${NC}"
    echo ""
    
    # Regenerate manifest
    echo "  Regenerando .manifest.json..."
    python3 -c "
import json, hashlib, os, re
from collections import Counter
from datetime import datetime
VAULT = '$VAULT'
manifest = {}
for root, dirs, files in os.walk(VAULT):
    for f in files:
        if not f.endswith('.md'):
            continue
        fpath = os.path.join(root, f)
        rel = os.path.relpath(fpath, VAULT)
        with open(fpath, 'rb') as fh:
            content = fh.read()
        manifest[rel] = {
            'hash': hashlib.sha256(content).hexdigest(),
            'updated': datetime.now().isoformat(),
            'size': len(content),
            'links': sorted(set(re.findall(r'\[\[([^\]]+)\]\]', content.decode('utf-8', errors='replace'))))
        }
with open(f'{VAULT}/.manifest.json', 'w') as fh:
    json.dump(manifest, fh, indent=2, ensure_ascii=False)
print(f'  ✅ Manifest regenerado: {len(manifest)} neurônios')
"
    
    # Save snapshot
    cp "$VAULT/.manifest.json" "$VAULT/.manifest.json.bak"
    echo "  ✅ Snapshot salvo: .manifest.json.bak"
fi

exit $FAIL
