#!/usr/bin/env bash
# stackctl.sh — Interruptor Stack A (LLMs) ⇄ Stack B (audiovisual) — MI50 16GB
# Uso: stackctl.sh {av-on|av-off|gpu-free|llm-on|status}
# Regra de ouro: as duas NUNCA coexistem em GPU (R21). Interlock: /tmp/stack-interlock/
set -uo pipefail

B="/mnt/dados/Assistente Pessoal/programas de apoio/fotografo"
LLAMA_BIN="/mnt/dados/Assistente Pessoal/programas de apoio/opencode/llama.cpp/bin/llama-server"
START_STACK="/mnt/dados/Assistente Pessoal/programas de apoio/opencode/scripts/start-stack.sh"
CONFY="/mnt/dados/Assistente Pessoal/programas de apoio/ConfyUI"
LOCK="/tmp/stack-interlock/fotografo-apitest.json"
GPU_SLOTS=(8083 9084 9088 9095)   # slots llama-server com -ngl>0 (VRAM)

log() { echo "[$(date -Iseconds)] $*" | tee -a "$B/logs/stackctl.log"; }

pid_of_port() { ss -tlnp 2>/dev/null | grep ":$1 " | grep -oE "pid=[0-9]+" | head -1 | cut -d= -f2; }

vram_used_gb() {
  rocm-smi --showmeminfo vram 2>/dev/null | grep -i "used memory" | grep -oE "[0-9]+" | head -1
}

set_owner() { # $1 = dono_gpu
  [ -f "$LOCK" ] || return 0
  sed -i "s/\"dono_gpu_atual\": \"[^\"]*\"/\"dono_gpu_atual\": \"$1\"/" "$LOCK" 2>/dev/null || true
}

cmd_gpu_free() {
  log "gpu-free: derrubando slots GPU ${GPU_SLOTS[*]} (CPU e API-TEST intocados)"
  for p in "${GPU_SLOTS[@]}"; do
    pid=$(pid_of_port "$p"); [ -n "$pid" ] && kill "$pid" && log "  :$p pid $pid TERM enviado"
  done
  sleep 8
  log "  vram usada agora: $(vram_used_gb) bytes"
  set_owner "nenhum (transicao)"
}

cmd_av_on() {
  log "av-on: subindo ComfyUI :8188 (venv311 torch rocm gfx906)"
  pid=$(pid_of_port 8188); [ -n "$pid" ] && { log "  já no ar (pid $pid)"; return 0; }
  setsid env PYTORCH_HIP_ALLOC_CONF=garbage_collection_threshold:0.9 \
    "$B/venv311/bin/python" "$CONFY/main.py" --listen 127.0.0.1 --port 8188 \
    > "$B/logs/comfyui.log" 2>&1 < /dev/null &
  for i in $(seq 1 30); do curl -sf -m 3 http://127.0.0.1:8188/system_stats >/dev/null 2>&1 && { log "  :8188 OK"; set_owner "fotografo-comfyui"; return 0; }; sleep 5; done
  log "  FALHA: :8188 não respondeu em 150s — ver logs/comfyui.log"; return 1
}

cmd_av_off() {
  pid=$(pid_of_port 8188); [ -n "$pid" ] && kill "$pid" && log "av-off: :8188 derrubado" || log "av-off: já estava fora"
  set_owner "nenhum (transicao)"
}

cmd_llm_on() {
  log "llm-on: religando stack LLM completa (start-stack.sh all)"
  [ -x "$START_STACK" ] || { log "  start-stack.sh ausente!"; return 1; }
  MODE_WARM=0 nohup bash "$START_STACK" all >> "$B/logs/stackctl-startstack.log" 2>&1 &
  set_owner "stack-llm"
  log "  start disparado (assíncrono; confira saúde das portas)"
}

cmd_status() {
  echo "=== VRAM ==="; rocm-smi --showmeminfo vram 2>/dev/null | grep -E "Total|Used"
  echo "=== Portas chave ==="
  for p in 8188 9188 8083 9084 9086 9088 9090 9092 8090; do
    if curl -sf -m 2 "http://127.0.0.1:$p/health" >/dev/null 2>&1 || curl -sf -m 2 "http://127.0.0.1:$p/system_stats" >/dev/null 2>&1; then
      echo "  :$p UP"
    else
      echo "  :$p down"
    fi
  done
  [ -f "$LOCK" ] && { echo "=== interlock ==="; cat "$LOCK"; }
}

case "${1:-status}" in
  gpu-free) cmd_gpu_free ;;
  av-on)    cmd_av_on ;;
  av-off)   cmd_av_off ;;
  llm-on)   cmd_llm_on ;;
  status)   cmd_status ;;
  *) echo "uso: $0 {av-on|av-off|gpu-free|llm-on|status}"; exit 1 ;;
esac
