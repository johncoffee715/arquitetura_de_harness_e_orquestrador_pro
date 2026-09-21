# Stack recovery — snapshot 2026-09-14 (cmdlines exatas via pgrep, pré-restart)

Pós-reboot: colar num terminal (um por linha, cada um com `&` já incluso via nohup) ou salvar como .sh e executar.

```bash
BIN="/mnt/dados/Assistente Pessoal/programas de apoio/opencode/llama.cpp/bin/llama-server.real"
M="/mnt/dados/Assistente Pessoal/modelos LLM"
nohup "$BIN" -m "$M/Qwen3.5-35B-A3B-UD-IQ3_XXS.gguf" --port 8083 --host 127.0.0.1 -c 262144 -np 1 -b 4096 -ub 1024 -ngl 36 -dev Vulkan0 --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6 --top-p 0.95 --top-k 20 --chat-template-kwargs '{"enable_thinking": false}' > /tmp/opencode/raw-8083.log 2>&1 &
nohup "$BIN" -m "$M/RWKV7-G1d-0.4B-Instruct-FP16.gguf" --port 9084 --host 127.0.0.1 -c 1048576 -np 1 -b 512 -ngl 999 -dev Vulkan0 --cache-type-k q4_0 --cache-type-v q4_0 --jinja > /tmp/opencode/raw-9084.log 2>&1 &
nohup "$BIN" -m "$M/LFM2.5-1.2B-Thinking-ToMoE-Q4_K_M.gguf" --port 9086 --host 127.0.0.1 -c 128000 -np 1 --flash-attn on -b 512 -ngl 0 --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.05 > /tmp/opencode/raw-9086.log 2>&1 &
nohup "$BIN" -m "$M/Llama-3.2-1B-Instruct-IQ4_XS.gguf" --port 9088 --host 127.0.0.1 -c 131072 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6 > /tmp/opencode/raw-9088.log 2>&1 &
nohup "$BIN" -m "$M/Llama-3.2-3B-Instruct-UD-IQ3_XXS.gguf" --port 9090 --host 127.0.0.1 -c 32768 -np 1 --flash-attn on -b 512 -ngl 0 --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6 > /tmp/opencode/raw-9090.log 2>&1 &
nohup "$BIN" -m "$M/smollm2-1.7b-instruct-q4_k_m.gguf" --port 9092 --host 127.0.0.1 -c 32768 -np 1 --flash-attn on -b 512 -ngl 0 --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6 > /tmp/opencode/raw-9092.log 2>&1 &
nohup "$BIN" -m "$M/SmolLM2-360M-Instruct-Q8_0.gguf" --port 9093 --host 127.0.0.1 -c 4096 -np 1 --flash-attn on -b 512 -ngl 999 -dev Vulkan0 --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6 > /tmp/opencode/raw-9093.log 2>&1 &
nohup "$BIN" -m "$M/Qwen1.5-MoE-A2.7B-Q3_K_M.gguf" --port 9095 --host 127.0.0.1 -c 8192 -np 1 --flash-attn on -b 512 -ngl 0 --cache-type-k q4_0 --cache-type-v q4_0 --jinja --temp 0.6 > /tmp/opencode/raw-9095.log 2>&1 &
sleep 45; for p in 8083 9084 9086 9088 9090 9092 9093 9095; do printf "%s:%s " "$p" "$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 http://localhost:$p/health)"; done; echo
```

NOTA: :9094/:9097 (embedders) DOWN desde antes da auditoria — fora do snapshot.
