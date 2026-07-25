#!/bin/bash
# Preflight Check — verifica componentes antes de começar a sessão
# Chamado pelo hook SessionStart.
# Exit 0 = tudo OK, Exit 1 = algo offline (não bloqueante)

echo "[Preflight] === Preflight System Check ==="
echo "[Preflight] Time: $(date -Iseconds)"
echo ""

# 1. GhidraMCP — verifica se o servidor SSE está respondendo
GHIDRA_URL="${GHIDRA_MCP_URL:-http://localhost:8182}"
if command -v curl &>/dev/null; then
  GHIDRA_CHECK=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "$GHIDRA_URL" 2>/dev/null || echo "000")
  if [ "$GHIDRA_CHECK" = "000" ]; then
    echo "[Preflight] ⚠️  GhidraMCP ($GHIDRA_URL): OFFLINE — agente 'reverser' não funcionará"
  else
    echo "[Preflight] ✅ GhidraMCP ($GHIDRA_URL): HTTP $GHIDRA_CHECK"
  fi
else
  echo "[Preflight] ⚠️  curl not available, skipping GhidraMCP check"
fi

# 2. LSP — verifica se há servidores configurados
LSP_CONFIG="$HOME/.config/opencode/lsp.json"
if [ -f "$LSP_CONFIG" ]; then
  LSP_COUNT=$(grep -c '"name"' "$LSP_CONFIG" 2>/dev/null || echo 0)
  echo "[Preflight] ✅ LSP config found: ~${LSP_COUNT} servers"
else
  echo "[Preflight] ⚠️  No LSP config file at $LSP_CONFIG"
fi

# 3. Skills root
SKILLS_DIRS=("$HOME/.opencode/skills" "$HOME/.config/opencode/skills")
for dir in "${SKILLS_DIRS[@]}"; do
  if [ -d "$dir" ]; then
    COUNT=$(find "$dir" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l)
    echo "[Preflight] ✅ Skills @ $dir: $COUNT skills"
  fi
done

# 4. OpenCode version
if command -v opencode &>/dev/null; then
  VERSION=$(opencode --version 2>/dev/null | head -1)
  echo "[Preflight] ✅ OpenCode: $VERSION"
fi

# 5. Disk space on working dirs
for mp in /mnt/dados /home /tmp; do
  if [ -d "$mp" ]; then
    AVAIL=$(df -h "$mp" 2>/dev/null | awk 'NR==2{print $4}')
    echo "[Preflight] 💾  $mp: ${AVAIL} free"
  fi
done

echo ""
echo "[Preflight] === Done ==="
echo "[Preflight] Nota: agente 'reverser' requer GhidraMCP online (SSE端口 $GHIDRA_URL)"
echo "[Preflight] Se for usar o reverser, inicie o Ghidra + MCP plugin primeiro."
