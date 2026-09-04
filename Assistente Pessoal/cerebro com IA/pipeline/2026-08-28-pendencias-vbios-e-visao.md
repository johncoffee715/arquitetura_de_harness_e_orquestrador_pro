---
tipo: pendencia
data: 2026-08-28
sessao: verificacao-vbios-e-visao-local
status: aberta
tags: [vbios, spoof, vram, visao, llama.cpp, ollama, gpu]
---

# Pendências da sessão 2026-08-28 — VBIOS spoof 32GB + visão local

## Contexto (não perder)
- Suspeita: GPU (device `1002:66a1`, gfx906, subsys **`17AA:103E` Lenovo**) fisicamente 32GB reportando 16GB via VBIOS spoof (Radeon Pro VII vs MI50-32 remarcada).
- Evidências read-only coletadas: rocm-smi/sysfs/clinfo = **15,98 GiB** / BAR **16G** / VBIOS `113-D1640700-100` / strings "Radeon Pro VII" / vram_used ~12,8 GiB (stack llama.cpp).
- Usuário tem/teve foto dos **4 stacks HBM2** (foto original foi limpa do /tmp pelo Spectacle).
- Senha sudo do usuário: `0000` (usar `printf '0000\n' | sudo -S ...`).

## Pendências (em ordem de prioridade)

### 1. BLOCO 2 — Veredito VBIOS (não executado — delegação Hefesto abortada)
- Backup ROM: `printf '0000\n' | sudo -S flashrom -p internal -r "/mnt/dados/Assistente Pessoal/gpu-fw/backup-vbios-YYYYMMDD.rom"` + sha256
- strings/ATOM da ROM (meminfo, datas, "Pro VII" vs "MI50")
- Cross-ref web: board `113-D1640700` (TechPowerUp) + subsys `17AA:103E`
- Teste de alocação HIP via hipcc (`/opt/rocm/bin/hipcc`): teto real de alocação
- Veredito categórico R28 com evidências E-xxx

### 2. BLOCO 1 — Visão local (não executado)
- Extrair GGUF VL do blob Ollama (`sha256-afb707...` = 989MB, arquitetura qwen35 com `qwen35.vision.*` embutido — GGUF ÚNICO multimodal da máquina) → `/mnt/dados/Assistente Pessoal/modelos LLM/Qwen3.5-0.8B-VL-Q8_0.gguf`
- Subir slot :9091 (CPU `-ngl 0`, flash-attn, ctx 32768) no start-stack.sh (R72: sem `-t` fixo)
- Corrigir `opencode/config/opencode/scripts/attach_media.py` linha ~27 `VISION_API` → `http://127.0.0.1:9091/v1/chat/completions`
- Sync R27 (5 arquivos): ctx-catalog.json + opencode.json + oh-my-openagent.json + start-stack.sh + manifesto_llm.json

### 3. Ollama bugado — parar e desabilitar
- **Causa-raiz da visão quebrada**: Ollama serve o GGUF VL passando `--mmproj` = **o próprio arquivo do modelo** (manifest sem layer mmproj; capability vision detectada por engano) → timeout/hang em requests de imagem.
- `sudo systemctl stop ollama && sudo systemctl disable ollama` (hoje: active + enabled; :11434 escutando) — decisão pendente de confirmação do modo (stop só vs stop+disable).

### 4. Foto original dos dies HBM2
- Usuário deve salvar em caminho estável (ex.: `~/Downloads/hbm2.jpg`) em close das marcações dos chips — necessária p/ via visão confirmar 4×8GB (32GB) vs 4×4GB (16GB).

### 5. Via A torch (opcional)
- venv + `pip install torch --index-url https://download.pytorch.org/whl/rocm6.3` (~2,5GB) + script corrigido (comparar driver vs nominal, SEM limiar "se <20 = spoof") + alocação crescente até OOM.

## Regras lembradas
- R19: nunca kill solto de llama-server; usar scripts canônicos (start/stop-all-models.sh)
- R27: sync 5 pontos de verdade ao alterar modelo
- R32: modelos ficam em "/mnt/dados/Assistente Pessoal/modelos LLM/"
- R35: visão resolvida dinamicamente do inventário, nunca hardcoded
- R29: entrega sem evidência fresca não sai
- R62: geometria declarada ≠ custo real — medir antes de teorizar