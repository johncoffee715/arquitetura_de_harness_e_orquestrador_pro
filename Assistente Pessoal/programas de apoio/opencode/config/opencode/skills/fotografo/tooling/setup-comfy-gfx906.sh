#!/usr/bin/env bash
# setup-comfy-gfx906.sh — venv py3.11 + torch 2.5.1+rocm6.2 (com kernels gfx906 p/ MI50)
set -uo pipefail
B="/mnt/dados/Assistente Pessoal/programas de apoio/fotografo"
L="$B/logs/setup-venv311.log"
V="$B/venv311"
echo "[$(date -Iseconds)] inicio setup venv311" >> "$L"

/usr/bin/python3.11 -m venv "$V" >> "$L" 2>&1 || { echo "FALHA venv create" >> "$L"; exit 1; }
"$V/bin/pip" install -q --upgrade pip >> "$L" 2>&1
echo "[$(date -Iseconds)] baixando torch rocm6.2 (~2GB)..." >> "$L"
"$V/bin/pip" install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 \
  --index-url https://download.pytorch.org/whl/rocm6.2 >> "$L" 2>&1 \
  && echo "[$(date -Iseconds)] TORCH_ROCM_OK" >> "$L" \
  || echo "[$(date -Iseconds)] FALHA torch" >> "$L"

grep -viE '^torch' "/mnt/dados/Assistente Pessoal/programas de apoio/ConfyUI/requirements.txt" > /tmp/req-comfy-notorch.txt
"$V/bin/pip" install -r /tmp/req-comfy-notorch.txt >> "$L" 2>&1 \
  && echo "[$(date -Iseconds)] REQS_OK" >> "$L" \
  || echo "[$(date -Iseconds)] FALHA reqs" >> "$L"

# verificacao de fumaça: matmul na gfx906 nativa
"$V/bin/python" -c "import torch; a=torch.randn(1024,1024,device='cuda'); print('MATMUL_GFX906_OK', float((a@a).sum()), torch.version.hip)" >> "$L" 2>&1 || echo "[$(date -Iseconds)] FALHA matmul" >> "$L"
echo "[$(date -Iseconds)] fim" >> "$L"
