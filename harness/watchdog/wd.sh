#!/bin/bash
# wd.sh — watchdog modular do grafo (R48/R63 · full modular 2026-08-24)
BASE="$(cd "$(dirname "$0")" && pwd)"
source "$BASE/lib/common.sh"
INTERVAL="${1:-30}"
SLOTS="$BASE/slots.json"
log "═══ wd modular iniciado (${INTERVAL}s · $(python3 -c "import json;print(len(json.load(open('$SLOTS'))['slots']))" 2>/dev/null) slots) ═══"
while true; do
  MISSING=0
  while IFS= read -r slot; do
    [ -z "$slot" ] && continue
    port=$(python3 -c "import json;print(json.loads('''$slot''')['port'])" 2>/dev/null)
    name=$(python3 -c "import json;print(json.loads('''$slot''')['name'])" 2>/dev/null)
    crit=$(python3 -c "import json;print(json.loads('''$slot''').get('critical',False))" 2>/dev/null)
    if health "$port"; then
      log "OK  :$port ($name)"
    else
      log "DOWN:$port ($name) critical=$crit — respawn"
      [ "$crit" = "True" ] && notify "slot :$port ($name) DOWN — respawn"
      bash "$BASE/actions/respawn.sh"
      MISSING=$((MISSING+1))
      [ "$MISSING" -ge 3 ] && { log "3+ ciclos com falha — cooldown 90s (R18)"; sleep 90; MISSING=0; }
    fi
  done < <(jq -c '.slots[]' "$SLOTS" 2>/dev/null)
  bash "$BASE/lib/capture.sh" >/dev/null 2>&1
  sleep "$INTERVAL"
done
