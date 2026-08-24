#!/bin/bash
# capture.sh — captura o orquestrador REAL em :8083 e sincroniza a config (R69)
# modelo+ctx → state/history · limit.context+name do provider seguem o modelo REAL
STATE=/mnt/dados/harness/watchdog/orchestrator-state.json
HIST=/mnt/dados/harness/watchdog/orchestrator-history.jsonl
OC=/mnt/dados/opencode/config/opencode.json
RAW=$(curl -s -m 3 http://127.0.0.1:8083/props 2>/dev/null)
[ -z "$RAW" ] && { echo "{\"status\":\"down\",\"ts\":\"$(date -Iseconds)\"}" > "$STATE" 2>/dev/null; exit 0; }
python3 - "$RAW" "$STATE" "$HIST" "$OC" <<'PY'
import json, sys, datetime, os
raw, STATE, HIST, OC = sys.argv[1:5]
d = json.loads(raw)
g = d.get("default_generation_settings", {})
modelo = os.path.basename(str(d.get("model_path", "?"))).replace(".gguf", "")
ctx = g.get("n_ctx")
ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

# state atual
prev_modelo = ""
try:
    prev = json.load(open(STATE))
    prev_modelo = prev.get("modelo", "")
except Exception:
    pass
json.dump({"status":"up","modelo":modelo,"ctx":ctx,
           "model_path":str(d.get("model_path","")),"ts":ts},
          open(STATE,"w"), indent=1)

# history: registra troca de modelo
if modelo != prev_modelo:
    open(HIST,"a").write(json.dumps(
        {"evento":"troca_orquestrador","modelo":modelo,"ctx":ctx,"ts":ts},
        ensure_ascii=False)+"\n")
    print(f"TROCA registrada: {modelo} ctx {ctx}")

# provider sync (R69): limit.context + name seguem o modelo REAL
try:
    oc = json.load(open(OC))
    mm = oc["provider"]["local-orchestrator"]["models"]["orchestrator"]
    changed = []
    lim = mm.setdefault("limit", {})
    if lim.get("context") != ctx:
        lim["context"] = ctx; changed.append(f"context={ctx}")
    nome = f"{modelo} (orquestrador) · GPU :8083"
    if mm.get("name") != nome:
        mm["name"] = nome; changed.append(f"name={nome}")
    if changed:
        json.dump(oc, open(OC,"w"), indent=1, ensure_ascii=False)
        print("R69 provider sync:", " · ".join(changed))
except Exception as e:
    print("provider sync erro:", e)
PY
