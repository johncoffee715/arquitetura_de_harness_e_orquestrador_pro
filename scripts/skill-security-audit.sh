#!/usr/bin/env bash
# skill-security-audit.sh — auditoria real de skills (.md + scripts associados)
# Cobre a lacuna da auditoria anterior: aquela so tocou SKILL.md, nunca scripts.
# Uso: bash skill-security-audit.sh [diretorio-raiz-opcional]

set -uo pipefail

ROOTS=(
  "$HOME/.claude/skills"
  "$HOME/.config/opencode/skills"
  "$HOME/.opencode/skills"
)

if [ "${1:-}" != "" ]; then
  ROOTS=("$1")
fi

OUT_DIR="$HOME/.ecc/security-audit-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT_DIR"
FINDINGS="$OUT_DIR/findings.tsv"
printf 'arquivo\ttipo\tpadrao\tlinha\ttrecho\n' > "$FINDINGS"

# --- Passo 1: inventario real (resolve a divergencia 3 vs 84) ---
echo "=== INVENTARIO REAL ==="
total_md=0
total_scripts=0
for root in "${ROOTS[@]}"; do
  [ -d "$root" ] || continue
  n_md=$(find "$root" -iname "SKILL.md" 2>/dev/null | wc -l)
  n_scripts=$(find "$root" -type f \( -iname "*.sh" -o -iname "*.py" -o -iname "*.js" -o -iname "*.ts" \) 2>/dev/null | wc -l)
  echo "$root : $n_md SKILL.md | $n_scripts scripts associados"
  total_md=$((total_md + n_md))
  total_scripts=$((total_scripts + n_scripts))
done
echo "TOTAL: $total_md SKILL.md | $total_scripts scripts"
echo "(compare com os numeros dos relatorios anteriores: 3, 72 ou 84 —"
echo " esse aqui e o que existe de fato no disco agora)"
echo ""

# --- Passo 2: padroes perigosos, ampliados alem dos 5 originais ---
DANGEROUS_PATTERNS=(
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
)

scan_file() {
  local f="$1" kind="$2"
  for pat in "${DANGEROUS_PATTERNS[@]}"; do
    grep -nEi "$pat" "$f" 2>/dev/null | while IFS=: read -r ln txt; do
      trecho="${txt:0:120}"
      printf '%s\t%s\t%s\t%s\t%s\n' "$f" "$kind" "$pat" "$ln" "$trecho" >> "$FINDINGS"
    done
  done
}

for root in "${ROOTS[@]}"; do
  [ -d "$root" ] || continue
  while IFS= read -r -d '' f; do
    scan_file "$f" "md"
  done < <(find "$root" -iname "SKILL.md" -print0 2>/dev/null)

  while IFS= read -r -d '' f; do
    scan_file "$f" "script"
  done < <(find "$root" -type f \( -iname "*.sh" -o -iname "*.py" -o -iname "*.js" -o -iname "*.ts" \) -print0 2>/dev/null)
done

# --- Passo 3: ferramentas de analise estatica real, se disponiveis ---
echo "=== FERRAMENTAS DE ANALISE ESTATICA ==="
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
  echo "shellcheck NAO instalado (sudo pacman -S shellcheck) — scripts .sh nao tiveram analise estatica real"
fi

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
  echo "bandit NAO instalado (pip install bandit --break-system-packages) — scripts .py nao tiveram analise estatica real"
fi
echo ""

# --- Resumo ---
n_findings=$(( $(wc -l < "$FINDINGS") - 1 ))
echo "=== RESUMO ==="
echo "SKILL.md verificados:            $total_md"
echo "Scripts associados verificados:  $total_scripts"
echo "Achados de padrao suspeito:      $n_findings"
echo "Detalhes linha a linha:          $FINDINGS"
echo ""
echo "IMPORTANTE:"
echo "  - Isto e triagem por padrao, NAO prova de seguranca."
echo "  - Zero achados NAO significa seguro (nao pega ofuscacao,"
echo "    exfiltracao em duas etapas, nem instrucao manipulativa no"
echo "    texto da propria SKILL.md)."
echo "  - Achado > 0 NAO significa malicioso — precisa de revisao"
echo "    humana com contexto, caso a caso."
echo "  - Revise manualmente os 4 scripts de ecc-autofagia primeiro:"
echo "    sao os que implementam o proprio safety protocol e nunca"
echo "    foram cobertos pela auditoria anterior."
