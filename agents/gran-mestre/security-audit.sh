#!/usr/bin/env bash
# gran-mestre-security-audit.sh — Auditoria de segurança completa
# Autofagia de: /home/johncoffee/Downloads/skill-security-audit.sh
# Adaptado para: Gran-Mestre Pipeline (skills, agents, scripts, metadata)

set -uo pipefail

# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

ROOTS=(
  "$HOME/.config/opencode/agents"
  "$HOME/.config/opencode/agents/gran-mestre"
  "$HOME/.opencode/skills"
  "$HOME/.config/opencode/skills"
)

# Incluir roots extras se fornecidos
if [ "${1:-}" != "" ]; then
  ROOTS+=("$1")
fi

OUT_DIR="$HOME/.opencode/security-audit-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT_DIR"
FINDINGS="$OUT_DIR/findings.tsv"
METADATA_GAPS="$OUT_DIR/metadata-gaps.tsv"
SUMMARY="$OUT_DIR/summary.json"

printf 'arquivo\ttipo\tpadrao\tlinha\ttrecho\n' > "$FINDINGS"
printf 'agent\tfield\tstatus\n' > "$METADATA_GAPS"

# =============================================================================
# PADRÕES PERIGOSOS (do original + expandidos)
# =============================================================================

DANGEROUS_PATTERNS=(
  # Padrões originais
  'rm[[:space:]]+-rf'
  'kill[[:space:]]+-9'
  '\bsudo\b'
  'curl[^|]*\|[[:space:]]*(ba)?sh'
  'wget[^|]*\|[[:space:]]*(ba)?sh'
  '\beval\('
  '\bexec\('
  'os\.system\('
  'subprocess\.(run|call|Popen)\(.*shell[[:space:]]*=[[:space:]]*True'
  'pickle\.loads?\('
  'yaml\.load\('
  'base64[[:space:]]+-d'
  '__import__\('
  'chmod[[:space:]]+777'
  '>[[:space:]]*/dev/sd[a-z]'
  '/etc/(passwd|shadow)'
  
  # Padrões expandidos (Gran-Mestre)
  'subprocess\.run\('
  'subprocess\.call\('
  'subprocess\.Popen\('
  'os\.popen\('
  'urllib\.request\.urlopen\('
  'requests\.get\('
  'requests\.post\('
  'http\.client\('
  'socket\.socket\('
  'open\([^)]*"/etc/'
  'open\([^)]*"/proc/'
  'open\([^)]*"/sys/'
  'Path\([^)]*\)\.read_text\('
  'Path\([^)]*\)\.read_bytes\('
  'hashlib\.sha256\('
  'hashlib\.md5\('
  'json\.loads\('
  'json\.load\('
  'yaml\.safe_load\('
  'pickle\.loads?\('
  'marshal\.loads?\('
  'shelve\.open\('
  'sqlite3\.connect\('
)

# =============================================================================
# CAMPOS OBRIGATÓRIOS DE METADATA
# =============================================================================

REQUIRED_METADATA=(
  "name"
  "description"
  "model"
  "mode"
  "origin"
  "metadata"
)

# =============================================================================
# FUNÇÕES
# =============================================================================

scan_file() {
  local f="$1" kind="$2"
  for pat in "${DANGEROUS_PATTERNS[@]}"; do
    grep -nEi "$pat" "$f" 2>/dev/null | while IFS=: read -r ln txt; do
      trecho="${txt:0:120}"
      printf '%s\t%s\t%s\t%s\t%s\n' "$f" "$kind" "$pat" "$ln" "$trecho" >> "$FINDINGS"
    done
  done
}

check_metadata() {
  local f="$1"
  local name=$(basename "$(dirname "$f")")
  
  for field in "${REQUIRED_METADATA[@]}"; do
    if grep -q "^${field}:" "$f" 2>/dev/null; then
      printf '%s\t%s\t%s\n' "$name" "$field" "present" >> "$METADATA_GAPS"
    else
      printf '%s\t%s\t%s\n' "$name" "$field" "missing" >> "$METADATA_GAPS"
    fi
  done
}

check_permissions() {
  local f="$1"
  local name=$(basename "$(dirname "$f")")
  
  # Verificar se é read-only
  if grep -q "edit/deny" "$f" || grep -q "write/deny" "$f"; then
    echo "  [PASS] $name: permissões restritivas"
  else
    echo "  [WARN] $name: permissões não verificadas"
  fi
  
  # Verificar se é read-only
  if grep -q "read-only" "$f" || grep -q "read/allow" "$f"; then
    echo "  [PASS] $name: modo read-only"
  else
    echo "  [WARN] $name: modo read-only não verificado"
  fi
}

# =============================================================================
# INVENTÁRIO REAL
# =============================================================================

echo "=== INVENTÁRIO REAL ==="
total_md=0
total_scripts=0
total_agents=0

for root in "${ROOTS[@]}"; do
  [ -d "$root" ] || continue
  
  n_md=$(find "$root" -iname "SKILL.md" -o -iname "*.md" 2>/dev/null | wc -l)
  n_scripts=$(find "$root" -type f \( -iname "*.sh" -o -iname "*.py" -o -iname "*.js" -o -iname "*.ts" \) 2>/dev/null | wc -l)
  n_agents=$(find "$root" -iname "*.md" -type f 2>/dev/null | wc -l)
  
  echo "$root : $n_md MD files | $n_scripts scripts | $n_agents agents"
  
  total_md=$((total_md + n_md))
  total_scripts=$((total_scripts + n_scripts))
  total_agents=$((total_agents + n_agents))
done

echo ""
echo "TOTAL: $total_md MD files | $total_scripts scripts | $total_agents agents"
echo ""

# =============================================================================
# VERIFICAÇÃO DE METADATA
# =============================================================================

echo "=== VERIFICAÇÃO DE METADATA ==="

for root in "${ROOTS[@]}"; do
  [ -d "$root" ] || continue
  
  while IFS= read -r -d '' f; do
    check_metadata "$f"
  done < <(find "$root" -iname "*.md" -type f -print0 2>/dev/null)
done

n_gaps=$(grep -c "missing" "$METADATA_GAPS" 2>/dev/null || echo "0")
echo "Gaps de metadata encontrados: $n_gaps"
echo ""

# =============================================================================
# VERIFICAÇÃO DE PERMISSÕES
# =============================================================================

echo "=== VERIFICAÇÃO DE PERMISSÕES ==="

for root in "${ROOTS[@]}"; do
  [ -d "$root" ] || continue
  
  while IFS= read -r -d '' f; do
    check_permissions "$f"
  done < <(find "$root" -iname "*.md" -type f -print0 2>/dev/null)
done

echo ""

# =============================================================================
# SCAN DE PADRÕES PERIGOSOS
# =============================================================================

echo "=== SCAN DE PADRÕES PERIGOSOS ==="

for root in "${ROOTS[@]}"; do
  [ -d "$root" ] || continue
  
  # Scan MD files
  while IFS= read -r -d '' f; do
    scan_file "$f" "md"
  done < <(find "$root" -iname "*.md" -type f -print0 2>/dev/null)
  
  # Scan scripts
  while IFS= read -r -d '' f; do
    scan_file "$f" "script"
  done < <(find "$root" -type f \( -iname "*.sh" -o -iname "*.py" -o -iname "*.js" -o -iname "*.ts" \) -print0 2>/dev/null)
done

n_findings=$(( $(wc -l < "$FINDINGS") - 1 ))
echo "Achados de padrão suspeito: $n_findings"
echo ""

# =============================================================================
# FERRAMENTAS DE ANÁLISE ESTÁTICA
# =============================================================================

echo "=== FERRAMENTAS DE ANÁLISE ESTATICA ==="

# ShellCheck
if command -v shellcheck >/dev/null 2>&1; then
  echo "shellcheck encontrado — analisando scripts .sh"
  : > "$OUT_DIR/shellcheck.log"
  for root in "${ROOTS[@]}"; do
    [ -d "$root" ] || continue
    while IFS= read -r -d '' f; do
      shellcheck -S warning "$f" >> "$OUT_DIR/shellcheck.log" 2>&1
    done < <(find "$root" -iname "*.sh" -print0 2>/dev/null)
  done
  echo "  -> $OUT_DIR/shellcheck.log"
else
  echo "shellcheck NÃO instalado — scripts .sh não tiveram análise estática real"
fi

# Bandit
if command -v bandit >/dev/null 2>&1; then
  echo "bandit encontrado — analisando scripts .py"
  : > "$OUT_DIR/bandit.log"
  for root in "${ROOTS[@]}"; do
    [ -d "$root" ] || continue
    while IFS= read -r -d '' f; do
      bandit -q "$f" >> "$OUT_DIR/bandit.log" 2>&1
    done < <(find "$root" -iname "*.py" -print0 2>/dev/null)
  done
  echo "  -> $OUT_DIR/bandit.log"
else
  echo "bandit NÃO instalado — scripts .py não tiveram análise estática real"
fi

echo ""

# =============================================================================
# VERIFICAÇÃO DE SEGURANÇA GRAN-MAESTRE
# =============================================================================

echo "=== VERIFICAÇÃO DE SEGURANÇA GRAN-MAESTRE ==="

# Verificar se Héstia e Atena são read-only
hestia="$HOME/.config/opencode/agents/gran-mestre/HESTIA.md"
athena="$HOME/.config/opencode/agents/gran-mestre/ATHENA.md"

for agent in "$hestia" "$athena"; do
  if [ -f "$agent" ]; then
    name=$(basename "$agent" .md)
    
    if grep -q "edit/deny" "$agent" && grep -q "write/deny" "$agent"; then
      echo "  [PASS] $name: permissões restritivas (edit/deny, write/deny)"
    else
      echo "  [WARN] $name: permissões não restritivas"
    fi
    
    if grep -q "read-only" "$agent"; then
      echo "  [PASS] $name: modo read-only"
    else
      echo "  [WARN] $name: modo read-only não verificado"
    fi
  fi
done

echo ""

# =============================================================================
# RELATÓRIO JSON
# =============================================================================

cat > "$SUMMARY" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "roots_scanned": ${#ROOTS[@]},
  "total_md_files": $total_md,
  "total_scripts": $total_scripts,
  "total_agents": $total_agents,
  "metadata_gaps": $n_gaps,
  "dangerous_patterns": $n_findings,
  "output_dir": "$OUT_DIR"
}
EOF

echo "Relatório JSON: $SUMMARY"

# =============================================================================
# RESUMO
# =============================================================================

echo ""
echo "=== RESUMO ==="
echo "MD files verificados:           $total_md"
echo "Scripts verificados:            $total_scripts"
echo "Agents verificados:             $total_agents"
echo "Gaps de metadata:               $n_gaps"
echo "Achados de padrão suspeito:     $n_findings"
echo ""
echo "Arquivos de saída:"
echo "  - Findings: $FINDINGS"
echo "  - Metadata gaps: $METADATA_GAPS"
echo "  - Summary: $SUMMARY"
echo ""
echo "IMPORTANTE:"
echo "  - Isto é triagem por padrão, NÃO prova de segurança."
echo "  - Zero achados NÃO significa seguro."
echo "  - Achado > 0 NÃO significa malicioso."
echo "  - Revise manualmente os findings com contexto."
echo ""

# Retornar código de saída
if [ $n_findings -gt 0 ] || [ $n_gaps -gt 0 ]; then
  echo "⚠️  AUDITORIA COMPLETA — $n_findings achados, $n_gaps gaps"
  exit 1
else
  echo "✅ AUDITORIA COMPLETA — SEM ACHADOS CRÍTICOS"
  exit 0
fi