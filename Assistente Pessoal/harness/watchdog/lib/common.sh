#!/bin/bash
LOG="/mnt/dados/Assistente Pessoal/harness/logs/wd-modular.log"
log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }
notify() { command -v notify-send >/dev/null 2>&1 && notify-send -u critical "wd-modular" "$1" 2>/dev/null; }
health() { curl -sf -m 3 "http://127.0.0.1:$1/health" >/dev/null 2>&1; }
jfield() { python3 -c "import json,sys;print(json.load(sys.stdin).get('$2',''))" <<< "$1"; }
