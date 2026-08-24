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
# R69 — sync modular: limit.context do provider segue o ctx REAL do server
OC=/mnt/dados/opencode/config/opencode.json
CTX_REAL=$(echo "$RAW" | python3 -c "import json,sys;print(json.load(sys.stdin).get('default_generation_settings',{}).get('n_ctx',''))" 2>/dev/null)
[ -n "$CTX_REAL" ] && python3 -c "
import json
d=json.load(open('$OC'))
cur=d['provider']['local-orchestrator']['models']['orchestrator'].get('limit',{}).get('context')
if cur != $CTX_REAL:
    d['provider']['local-orchestrator']['models']['orchestrator']['limit']['context']=$CTX_REAL
    json.dump(d,open('$OC','w'),indent=1,ensure_ascii=False)
    print('R69: provider limit.context sincronizado →',$CTX_REAL)
" 2>/dev/null
