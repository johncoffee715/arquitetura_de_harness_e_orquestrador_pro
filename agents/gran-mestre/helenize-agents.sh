#!/usr/bin/env bash
# helenize-agents.sh — Heleniza agents GSD para padrão OpenCode

AGENTS_DIR="$HOME/.config/opencode/agents"
BACKUP_DIR="$HOME/.opencode/backup-orphaned-$(date +%Y%m%d-%H%M%S)"

mkdir -p "$BACKUP_DIR"

echo "=== HELENIZAÇÃO DE AGENTS GSD ==="
echo ""

helenize_agent() {
  local file="$1"
  local name=$(basename "$file" .md)
  
  # Verificar se já tem metadata completa
  local has_model=$(grep -c "^model:" "$file" 2>/dev/null)
  local has_mode=$(grep -c "^mode:" "$file" 2>/dev/null)
  local has_origin=$(grep -c "^origin:" "$file" 2>/dev/null)
  
  if [ "$has_model" -gt 0 ] && [ "$has_mode" -gt 0 ] && [ "$has_origin" -gt 0 ]; then
    echo "OK: $name (já helenizado)"
    return 0
  fi
  
  # Extrair descrição existente
  local description=$(grep -A1 "^description:" "$file" 2>/dev/null | head -1 | sed 's/^ *//' | sed 's/^"//' | sed 's/"$//')
  if [ -z "$description" ]; then
    description="Agent $name"
  fi
  
  # Determinar categoria
  local category="utility"
  if [[ "$name" == *"reviewer"* ]] || [[ "$name" == *"audit"* ]]; then
    category="review"
  elif [[ "$name" == *"planner"* ]] || [[ "$name" == *"researcher"* ]]; then
    category="research"
  elif [[ "$name" == *"executor"* ]] || [[ "$name" == *"fixer"* ]]; then
    category="execution"
  elif [[ "$name" == *"debugger"* ]]; then
    category="debug"
  fi
  
  # Backup do arquivo original
  cp "$file" "$BACKUP_DIR/${name}.md.bak"
  
  # Criar nova metadata
  local metadata="---
name: $name
description: \"$description\"
model: github-copilot/claude-opus-4.7
mode: agent
origin: gsd-helenizado
metadata:
  category: $category
  version: 1.0.0
  author: Gran-Mestre (helenizado de GSD)
---"
  
  # Combinar metadata com conteúdo existente
  local content=$(sed '/^---$/,/^---$/d' "$file")
  
  echo "$metadata" > "$file"
  echo "" >> "$file"
  echo "$content" >> "$file"
  
  echo "HELENIZADO: $name → model=claude-opus-4.7, mode=agent, origin=gsd-helenizado"
}

# Helenizar todos os agents GSD
for file in "$AGENTS_DIR"/gsd-*.md; do
  if [ -f "$file" ]; then
    helenize_agent "$file"
  fi
done

echo ""
echo "=== RESUMO ==="
echo "Backup salvo em: $BACKUP_DIR"
echo "Agents helenizados: $(ls "$BACKUP_DIR"/*.md.bak 2>/dev/null | wc -l)"
echo ""
echo "=== PRÓXIMOS PASSOS ==="
echo "1. Verificar agents helenizados"
echo "2. Atualizar registry"
echo "3. Testar Gran-Mestre pipeline"