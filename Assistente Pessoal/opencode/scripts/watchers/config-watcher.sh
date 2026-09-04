#!/bin/bash
# config-watcher.sh — vigia a saúde da config da árvore portátil OpenCode
# Árvore: /mnt/dados/Assistente Pessoal/opencode/ (XDG dirs customizados no wrapper)
# Checagens: JSONC parseável · AGENTS.md · binários executáveis · repos git
# Anti-spam: dedupe por hash de assinatura — notify-send só em CRÍTICO novo
# NUNCA auto-conserta (apenas alerta)
set -uo pipefail

ROOT="/mnt/dados/Assistente Pessoal/opencode"
CFG="$ROOT/config/opencode"
STATE="$ROOT/state/watcher"
LOG="$STATE/config-watcher.log"
HASHFILE="$STATE/.last-alert-hash"
INTERVAL="${1:-60}"

mkdir -p "$STATE"

log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }
notify() {
  # dedupe: só notifica se assinatura mudou
  local sig
  sig=$(printf '%s' "$1" | md5sum | cut -d' ' -f1)
  [ -f "$HASHFILE" ] && [ "$(cat "$HASHFILE" 2>/dev/null)" = "$sig" ] && return 0
  echo "$sig" > "$HASHFILE"
  command -v notify-send >/dev/null && notify-send -u critical "config-watcher" "$1" 2>/dev/null
}

check_json() { # $1=path — JSON sintaticamente válido
  [ -f "$1" ] || { echo "CRITICO json ausente: $1"; return 0; }
  jq empty "$1" >/dev/null 2>&1 || echo "CRITICO json invalido: $1"
}
check_exec() { # $1=path executável
  [ -f "$1" ] || { echo "CRITICO binario ausente: $1"; return 0; }
  [ -x "$1" ] || echo "CRITICO sem permissao de execucao: $1"
}
check_file() { # $1=path arquivo obrigatório
  [ -s "$1" ] || echo "CRITICO arquivo vazio/ausente: $1"
}
check_repos() { # repos versionados íntegros
  local r
  for r in "$ROOT"/repos/*/; do
    [ -d "$r" ] || continue
    git -C "$r" rev-parse --git-dir >/dev/null 2>&1 || echo "WARN repo git quebrado: $r"
  done
}
check_frontmatter() { # amostragem: name==pasta nas skills ativas do usuário
  python3 - <<'PY'
import glob, re, sys
for f in glob.glob("/home/johncoffee/.agents/skills/*/SKILL.md"):
    try:
        txt = open(f, encoding="utf-8", errors="replace").read(2000)
    except OSError:
        continue
    m = re.match(r"---\n(.*?)\n---", txt, re.S)
    if not m:
        continue
    nm = re.search(r"^name:\s*['\"]?([\w-]+)", m.group(1), re.M)
    folder = f.split("/")[-2]
    if nm and nm.group(1) != folder:
        print(f"WARN name!=pasta: {folder}")
PY
}

cycle() {
  local out
  out=$(mktemp)
  check_json   "$CFG/opencode.jsonc"      >> "$out"
  check_file   "$CFG/AGENTS.md"           >> "$out"
  check_exec   "$ROOT/bin/opencode"       >> "$out"
  check_exec   "$ROOT/bin/opencode.real"  >> "$out"
  check_repos                             >> "$out"
  check_frontmatter                       >> "$out"

  if [ -s "$out" ]; then
    local crit=""
    while IFS= read -r line; do
      log "$line"
      case "$line" in CRITICO*) crit+="$line"$'\n' ;; esac
    done < "$out"
    [ -n "$crit" ] && notify "$crit"
  else
    # estado saudável: limpar hash para permitir re-alerta em falha futura
    rm -f "$HASHFILE"
  fi
  rm -f "$out"
}

log "watcher iniciado (intervalo ${INTERVAL}s) — árvore portátil $ROOT"
while true; do cycle; sleep "$INTERVAL"; done
