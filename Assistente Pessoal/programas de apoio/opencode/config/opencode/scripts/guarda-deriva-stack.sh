#!/usr/bin/env bash
# guarda-deriva-stack.sh — GUARD anti-recorrência do incidente stale-config (R96)
# Compara flags VIVAS (ps) contra reference/stack-final-flags.json e reporta
# OK ou DIVERGENTE por slot. Com --fix, relança via restart-stack.sh.
# Uso: bash guarda-deriva-stack.sh [--fix]   (leitura por padrão; --fix = humano)
# Log: /tmp/opencode/guarda-deriva.log
set -u
REF="/mnt/dados/Assistente Pessoal/programas de apoio/opencode/config/opencode/reference/stack-final-flags.json"
HERE="/mnt/dados/Assistente Pessoal/programas de apoio/opencode/config/opencode/scripts"
LOG="/tmp/opencode/guarda-deriva.log"
MODE="${1:-}"
mkdir -p /tmp/opencode
{
echo "=== $(date -u +%FT%TZ) modo=${MODE:-check} ==="
python3 - "$REF" <<'PYEOF'
import json, subprocess, sys
ref = json.load(open(sys.argv[1]))["slots"]
def ps_flags(pid):
    try:
        cmd = open(f"/proc/{pid}/cmdline", "rb").read().replace(b"\0", b" ").decode()
    except Exception:
        return {}
    import re
    out = {}
    for k, pat in (("ngl", r"-ngl (\d+)"), ("ctx", r"-c (\d+)"), ("batch", r"-b (\d+)")):
        m = re.search(pat, cmd)
        out[k] = m.group(1) if m else "?"
    out["gpu"] = "1" if "-dev Vulkan0" in cmd or "-ngl 999" in cmd else ("0" if "-ngl 0" in cmd else "?")
    return out
def pid_of(port):
    r = subprocess.run(["ss", "-ltnp"], capture_output=True, text=True)
    m = __import__("re").search(rf":{port}\b.*pid=(\d+)", r.stdout)
    return m.group(1) if m else None
def exp_ngl(dev):
    if "ngl999" in dev:
        return "999"
    if "ngl0" in dev:
        return "0"
    return "?"
bad = 0
for port, want in sorted(ref.items(), key=lambda kv: int(kv[0])):
    pid = pid_of(port)
    if not pid:
        print(f"{port}: DOWN (esperado: {want['device']})"); bad += 1; continue
    live = ps_flags(pid)
    w = {"ngl": exp_ngl(want["device"]), "ctx": str(want["ctx"]),
         "batch": str(want.get("batch", "?")).split("/")[0]}
    diffs = [k for k in w if live.get(k, "?") != "?" and w[k] != "?" and live[k] != w[k]]
    if diffs:
        print(f"{port}: DIVERGENTE pid={pid} diverge={diffs} vivo={live} att={w} [{want['model'][:40]}]")
        bad += 1
    else:
        print(f"{port}: OK pid={pid}")
print(f"RESULTADO: {'DIVERGENCIA' if bad else 'SINCRONIZADO'} ({bad} pendencias)")
PYEOF
} | tee -a "$LOG"
if [ "$MODE" = "--fix" ]; then
  echo "FIX autorizado: relançando via restart-stack.sh" | tee -a "$LOG"
  bash "$HERE/restart-stack.sh" 2>&1 | tee -a "$LOG"
else
  echo "CHECK apenas. Reemita com --fix para restaurar (humano)." | tee -a "$LOG"
fi
