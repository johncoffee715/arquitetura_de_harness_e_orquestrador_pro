#!/bin/bash
# capture.sh — captura o orquestrador REAL em :8083 (modelo, ctx) para comparações
STATE=/mnt/dados/harness/watchdog/orchestrator-state.json
HIST=/mnt/dados/harness/watchdog/orchestrator-history.jsonl
RAW=$(curl -s -m 3 http://127.0.0.1:8083/props 2>/dev/null)
[ -z "$RAW" ] && { echo "{\"status\":\"down\",\"ts\":\"$(date -Iseconds)\"}" > "$STATE" 2>/dev/null; exit 0; }
echo "$RAW" | python3 -c "
import json,sys,datetime,os
d=json.load(sys.stdin)
g=d.get('default_generation_settings',{})
mp=d.get('model_path','?')
modelo=os.path.basename(str(mp)).replace('.gguf','')
ctx=g.get('n_ctx')
ts=datetime.datetime.now(datetime.timezone.utc).isoformat()
prev=''
try: prev=json.load(open('$STATE')).get('modelo','')
except: pass
state={'status':'up','modelo':modelo,'ctx':ctx,'model_path':str(mp),'ts':ts}
json.dump(state,open('$STATE','w'),indent=1)
if modelo!=prev:
    line=json.dumps({'evento':'troca_orquestrador','modelo':modelo,'ctx':ctx,'ts':ts},ensure_ascii=False)
    open('$HIST','a').write(line+'\n')
    print('TROCA registrada:',modelo,'ctx',ctx)
" 2>/dev/null
