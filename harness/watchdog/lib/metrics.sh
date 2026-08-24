#!/bin/bash
# metrics.sh — métricas DO ORQUESTRADOR (R67: sem rótulos, sem plugins)
# Diff de contadores cumulativos do :8083 → t/s real por intervalo.
STATE=/mnt/dados/harness/watchdog/orchestrator-metrics.state
OUT=/mnt/dados/harness/watchdog/orchestrator-metrics.jsonl
NOW=$(date +%s.%N)
RAW=$(curl -s -m 3 http://127.0.0.1:8083/slots 2>/dev/null)
[ -z "$RAW" ] && exit 0
read -r PPROMPT PDECODE <<< "$(echo "$RAW" | python3 -c "
import json,sys
s=json.load(sys.stdin)
pp=sum(x.get('n_prompt_tokens_processed',0) for x in s)
dc=sum((x.get('next_token') or [{}])[0].get('n_decoded',0) for x in s)
print(pp,dc)")"
PREV=$(cat "$STATE" 2>/dev/null)
echo "$NOW $PPROMPT $PDECODE" > "$STATE"
[ -z "$PREV" ] && exit 0
PT=$(echo $PREV | cut -d" " -f1); PP=$(echo $PREV | cut -d" " -f2); PD=$(echo $PREV | cut -d" " -f3)
DT=$(python3 -c "print(f'{$NOW-$PT:.3f}')")
[ "$(python3 -c "print(1 if $NOW-$PT>0.5 else 0)")" = "0" ] && exit 0
MODEL=$(python3 -c "import json;print(json.load(open('/mnt/dados/harness/watchdog/orchestrator-state.json')).get('modelo','?'))" 2>/dev/null)
DP=$((PPROMPT-PD0)); DD=$((PDECODE-PD0))
DPR=$((PPROMPT-PP)); DDC=$((PDECODE-PD))
python3 -c "
import json,datetime
dp=max($DPR,0); dd=max($DDC,0); dt=float('$DT')
rec={'ts':datetime.datetime.now(datetime.timezone.utc).isoformat(),'modelo':'$MODEL',
 'prefill_tokens':dp,'decode_tokens':dd,'intervalo_s':dt,
 'prefill_tps':round(dp/dt,1) if dt>0 else 0,'decode_tps':round(dd/dt,1) if dt>0 else 0}
open('$OUT','a').write(json.dumps(rec,ensure_ascii=False)+'\n')
if dp>0 or dd>0: print(f\"GM metrics: prefill {rec['prefill_tps']} t/s · decode {rec['decode_tps']} t/s ({dp}+{dd} tok/{dt}s)\")"
