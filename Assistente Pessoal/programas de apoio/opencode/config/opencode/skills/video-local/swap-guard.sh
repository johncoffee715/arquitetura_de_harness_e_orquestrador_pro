#!/bin/bash
for i in $(seq 1 2600); do
  sleep 20
  U=$(free -g | awk '/Swap/{print $3}')
  if [ "$U" -ge 28 ]; then
    echo "GUARD: swap ${U}GB — abortando render" >> /tmp/opencode/swap-guard.log
    curl -sf -m 5 -X POST http://127.0.0.1:8189/queue -H 'Content-Type: application/json' -d '{"clear":true}' >/dev/null 2>&1
    sleep 5
    U2=$(free -g | awk '/Swap/{print $3}')
    if [ "$U2" -ge 28 ]; then
      P=$(pgrep -f "ConfyUI-vega/main" | head -1)
      [ -n "$P" ] && kill $P && echo "GUARD: servidor $P desligado" >> /tmp/opencode/swap-guard.log
    fi
    exit 0
  fi
done
echo "GUARD: janela encerrada sem disparo" >> /tmp/opencode/swap-guard.log
