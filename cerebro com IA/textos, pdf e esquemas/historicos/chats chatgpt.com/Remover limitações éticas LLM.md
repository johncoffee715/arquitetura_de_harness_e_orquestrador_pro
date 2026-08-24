---
title: "Remover limitações éticas LLM"
source: "https://chatgpt.com/c/69e6481c-3ecc-83e9-bb81-74a45f93f1bb"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 6 messages"
tags:
  - "clippings"
---
**Você disse**

desejo que adapte isso ao meu modelo atual

---

O problema NÃO é GPU fraca.  
É stack quebrado + offload errado + OpenClaude corrompido + Ollama provavelmente caindo em CPU fallback silencioso.

Você já deixou rastros claros:

- MI50 quase sem uso
- consumo ~20W
- GPU use 0–20%
- resposta lenta
- `openclaude` quebrado (`SyntaxError: Unexpected end of input`)
- Node instalado em NTFS
- possível corrupção/truncamento do `cli.mjs`
- ROCm provavelmente não está sendo realmente usado pelo runner

Diagnóstico direto:

---

Esse erro:

```bash
SyntaxError: Unexpected end of input
```

significa:

- arquivo truncado
- npm install interrompido
- NTFS corrompeu stream
- pacote parcialmente escrito

E você confirmou:

```bash
node -c cli.mjs
SyntaxError
```

Ou seja:

✅ NÃO é PATH  
✅ NÃO é Fish  
✅ NÃO é Ollama  
❌ é o pacote OpenClaude quebrado

---

## 2\. NÃO USE NODE\_MODULES EM NTFS PARA TOOLING CRÍTICO

Isso aqui é o gargalo arquitetural:

```
/mnt/win2/Assistente Pessoal/node/
```

NTFS + milhões de arquivos JS + symlink + npm = inferno.

Especialmente:

- ESM
- symlink
- watcher
- package-lock
- cache
- permission
- inode emulado

Isso mata:

- performance
- integridade
- startup time

---

## 3\. ARQUITETURA CORRETA

Você já quase chegou nela.

Faça assim:

## SLAVE NTFS

Somente:

- modelos
- scripts
- configs
- snapshots
- prompts
- backups

## MASTER EXT4

Tudo que:

- compila
- gera cache
- usa inode pesado
- npm
- venv
- WAL
- banco
- embeddings

---

## 4\. REFAÇA O OPENCLAUDE EM EXT4

APAGUE a instalação quebrada:

```bash
rm -rf "/mnt/win2/Assistente Pessoal/node"
```

Agora recrie corretamente:

```bash
mkdir -p ~/.local/ai-stack/node
cd ~/.local/ai-stack
```

Baixe Node:

```bash
curl -LO https://nodejs.org/dist/v22.13.1/node-v22.13.1-linux-x64.tar.xz
tar -xf node-v22.13.1-linux-x64.tar.xz
mv node-v22.13.1-linux-x64 node
```

PATH:

```
set -Ux PATH ~/.local/ai-stack/node/bin $PATH
```

Teste:

```bash
node --version
npm --version
```

Agora:

```bash
npm install -g @gitlawb/openclaude
```

Teste:

```bash
which openclaude
openclaude --help
```

---

## 5\. OLLAMA ESTÁ PROVAVELMENTE EM CPU FALLBACK

Seu sintoma:

- lentidão extrema
- GPU quase idle
- VRAM ocupada
- pouco power draw

Isso normalmente significa:

```
modelo parcialmente carregado em VRAM
+
inferência principal em CPU
```

---

## 6\. FORCE ROCm

Crie:

```bash
kate ~/.config/fish/config.fish
```

Adicione:

```
set -Ux HSA_OVERRIDE_GFX_VERSION 9.0.6
set -Ux ROC_ENABLE_PRE_VEGA 1
set -Ux HCC_AMDGPU_TARGET gfx906
set -Ux OLLAMA_GPU_OVERHEAD 0
set -Ux OLLAMA_NUM_PARALLEL 1
set -Ux OLLAMA_MAX_LOADED_MODELS 1
```

---

## 7\. TESTE REAL DE GPU

Rode:

```bash
watch -n 0.5 rocm-smi
```

Em outro terminal:

```bash
OLLAMA_DEBUG=1 ollama run qwen2.5-coder:14b
```

Pergunta:

```
Explique recursão em C.
```

Se GPU estiver OK:

- GPU% sobe
- power 80–180W
- clocks sobem
- resposta acelera

Se continuar 20W:  
❌ ROCm não está sendo usado direito.

---

## 8\. MISTRAL-SMALL 22B É PESADO PRA MI50

Mesmo 16GB HBM2:

- 22B Q4 já estrangula
- KV cache pesa
- contexto longo mata throughput

Para engenharia reversa:  
melhor combinação hoje no teu hardware:

| Modelo | Uso |
| --- | --- |
| qwen2.5-coder:14b | principal |
| deepseek-coder-v2:16b | análise pesada |
| mistral-nemo | reasoning rápido |
| phi3:medium | automação |

---

## 9\. O QUE MAIS ESTÁ MATANDO PERFORMANCE

Você está usando:

```
Kernel 7.0
Wayland
KDE
4K
30Hz
Open-WebUI
Qdrant
Ollama
watch
ROCm
```

Tudo junto.

MI50 é compute.  
Não é desktop GPU.

Então:

- VRAM fragmenta
- compositor pesa
- mmap aumenta
- latência sobe

---

## 10\. OTIMIZAÇÃO REAL

Adicione no Ollama:

```
set -Ux OLLAMA_FLASH_ATTENTION 1
set -Ux OLLAMA_KV_CACHE_TYPE q8_0
```

E rode modelos Q4\_K\_M.

---

## 11\. O MAIOR PROBLEMA DO TEU STACK

Você tentou fazer:

- soberania
- persistência
- AI infra
- coding agent
- RAG
- vector DB
- automation
- ROCm
- OpenWebUI

ANTES de estabilizar:

- ROCm
- Ollama
- throughput

Ordem correta:

```
1. ROCm puro
2. Ollama puro
3. throughput validado
4. modelos estáveis
5. OpenWebUI
6. Qdrant
7. RAG
8. agents
9. automation
10. orchestration
```

Hoje teu stack está sofisticado demais para uma base ainda instável.

Primeiro estabiliza:

- GPU
- inferência
- Node
- filesystem

Depois sobe o restante.

---

**Você disse**

\# ── CachyOS Base ────────────────────────────────────────────── # Carregamento do framework CachyOS apenas em shells interativos if status is-interactive source /usr/share/cachyos-fish-config/cachyos-config.fish end # ── AI-Lab Global Environment ────────────────────────────────── # Escapamento rigoroso para caminhos com espaços set -gx AI\_LAB\_BASE "/mnt/win2/Assistente Pessoal" set -gx AI\_LAB\_PROMPT "$AI\_LAB\_BASE/Prompts/engineering\_v5.1.txt" # fish\_add\_path é idempotente e lida nativamente com caminhos complexos fish\_add\_path "$AI\_LAB\_BASE/scripts" # ── Legacy Bridge: Bash-to-Fish Env Importer ─────────────────── set -l env\_file "$AI\_LAB\_BASE/config/env\_vars.sh" if test -f "$env\_file" # Otimização: Capturamos tudo em um bloco Bash único para reduzir forks # Usamos o prefixo estrito para evitar poluição do namespace do Fish set -l env\_data (bash -c "source '$env\_file' && env" | grep -E "^(OLLAMA|HSA|GPU\_|ROCM|HIP|AMDGPU|AI\_LAB|QDRANT)") for line in $env\_data # split -m 1: Protege valores que contenham '=' (comum em chaves ou tokens) set -l kv (string split -m 1 "=" -- $line) if test (count $kv) -eq 2 # Exportação global para visibilidade em instâncias ROCm/Ollama set -gx $kv\[1\] $kv\[2\] end end end # ── Performance Tuning & Aliases ────────────────────────────── # Prioridade de CPU (Nice -10) para garantir estabilidade no processamento de LLMs alias ollama="nice -n -10 ollama" # Alias para o binário de orquestração alias ai-lab="bash /usr/local/bin/ai-lab" # ── Funções de Utilitário ───────────────────────────────────── # Recarga rápida do ambiente após alterações em env\_vars ou prompts function reload\_ai\_env --description "Recarrega ambiente AI-LAB e configurações do Fish" source ~/.config/fish/config.fish echo (set\_color green)"\[OK\]" (set\_color normal)"Ambiente AI-LAB recarregado com sucesso." end # Monitor rápido de VRAM para a MI50 (via rocm-smi) function vram --description "Monitora uso de VRAM da GPU AMD" watch -n 1 rocm-smi --showmeminfo vram end ## ── Funções de Utilitário ───────────────────────────────────── function reload\_ai\_env --description "Recarrega ambiente AI-LAB e configurações do Fish" source ~/.config/fish/config.fish echo (set\_color green)"\[OK\]" (set\_color normal)"Ambiente AI-LAB recarregado com sucesso." end function vram --description "Monitora uso de VRAM da GPU AMD" watch -n 1 rocm-smi --showmeminfo vram end # Função Plug n' Play para Systemd-boot (John Coffee Edition) function gpu-unlock --description "Autonomia Técnica: Desbloqueio de 300W MI50" # 1. Gera o binário persistente\[cite: 1\] sudo /usr/local/bin/deploy-gpu-300w # 2. Prevenção: Injeção no Systemd-boot apenas se necessário\[cite: 1\] sudo python3 -c ' import glob, os param = "amdgpu.pptable\_name=amdgpu/mi50\_300w.bin" entries = glob.glob("/boot/loader/entries/\*.conf") for entry in entries: with open(entry, "r+") as f: content = f.read() if "options" in content and param not in content: f.seek(0) f.write(content.replace("options ", f"options {param} ")) print(f"\[+\] Bootloader atualizado: {entry}") ' # 3. Refatoração de Initramfs: Garante que o firmware esteja no estágio inicial do boot\[cite: 1\] echo "\[!\] Atualizando Initramfs para persistência total..." sudo mkinitcpio -P echo "--- Sucesso Transcendental: Reinicie para validar os 300W ---" end function ai-gpu-init --description "Vacina 300W para MI50 - Homeopática" # 1. Roda o script de injeção heurística sudo python3 /usr/local/bin/gpu-enforcer # 2. Injeta o parâmetro no Systemd-Boot (Automático) sudo python3 -c ' import glob param = "amdgpu.pptable\_name=amdgpu/mi50\_300w.bin" for entry in glob.glob("/boot/loader/entries/\*.conf"): with open(entry, "r+") as f: content = f.read() if "options" in content and param not in content: f.seek(0) f.write(content.replace("options ", f"options {param} ")) ' # 3. Garante que o Initramfs veja o novo firmware sudo mkinitcpio -P echo "Done. Reinicie para operar em 300W nativos." end# ── CachyOS Base ────────────────────────────────────────────── # Carregamento do framework CachyOS apenas em shells interativos if status is-interactive source /usr/share/cachyos-fish-config/cachyos-config.fish end # ── AI-Lab Global Environment ────────────────────────────────── # Escapamento rigoroso para caminhos com espaços set -gx AI\_LAB\_BASE "/mnt/win2/Assistente Pessoal" set -gx AI\_LAB\_PROMPT "$AI\_LAB\_BASE/Prompts/engineering\_v5.1.txt" # fish\_add\_path é idempotente e lida nativamente com caminhos complexos fish\_add\_path "$AI\_LAB\_BASE/scripts" # ── Legacy Bridge: Bash-to-Fish Env Importer ─────────────────── set -l env\_file "$AI\_LAB\_BASE/config/env\_vars.sh" if test -f "$env\_file" # Otimização: Capturamos tudo em um bloco Bash único para reduzir forks # Usamos o prefixo estrito para evitar poluição do namespace do Fish set -l env\_data (bash -c "source '$env\_file' && env" | grep -E "^(OLLAMA|HSA|GPU\_|ROCM|HIP|AMDGPU|AI\_LAB|QDRANT)") for line in $env\_data # split -m 1: Protege valores que contenham '=' (comum em chaves ou tokens) set -l kv (string split -m 1 "=" -- $line) if test (count $kv) -eq 2 # Exportação global para visibilidade em instâncias ROCm/Ollama set -gx $kv\[1\] $kv\[2\] end end end # ── Performance Tuning & Aliases ────────────────────────────── # Prioridade de CPU (Nice -10) para garantir estabilidade no processamento de LLMs alias ollama="nice -n -10 ollama" # Alias para o binário de orquestração alias ai-lab="bash /usr/local/bin/ai-lab" # ── Funções de Utilitário ───────────────────────────────────── # Recarga rápida do ambiente após alterações em env\_vars ou prompts function reload\_ai\_env --description "Recarrega ambiente AI-LAB e configurações do Fish" source ~/.config/fish/config.fish echo (set\_color green)"\[OK\]" (set\_color normal)"Ambiente AI-LAB recarregado com sucesso." end # Monitor rápido de VRAM para a MI50 (via rocm-smi) function vram --description "Monitora uso de VRAM da GPU AMD" watch -n 1 rocm-smi --showmeminfo vram end ## ── Funções de Utilitário ───────────────────────────────────── function reload\_ai\_env --description "Recarrega ambiente AI-LAB e configurações do Fish" source ~/.config/fish/config.fish echo (set\_color green)"\[OK\]" (set\_color normal)"Ambiente AI-LAB recarregado com sucesso." end function vram --description "Monitora uso de VRAM da GPU AMD" watch -n 1 rocm-smi --showmeminfo vram end # Função Plug n' Play para Systemd-boot (John Coffee Edition) function gpu-unlock --description "Autonomia Técnica: Desbloqueio de 300W MI50" # 1. Gera o binário persistente\[cite: 1\] sudo /usr/local/bin/deploy-gpu-300w # 2. Prevenção: Injeção no Systemd-boot apenas se necessário\[cite: 1\] sudo python3 -c ' import glob, os param = "amdgpu.pptable\_name=amdgpu/mi50\_300w.bin" entries = glob.glob("/boot/loader/entries/\*.conf") for entry in entries: with open(entry, "r+") as f: content = f.read() if "options" in content and param not in content: f.seek(0) f.write(content.replace("options ", f"options {param} ")) print(f"\[+\] Bootloader atualizado: {entry}") ' # 3. Refatoração de Initramfs: Garante que o firmware esteja no estágio inicial do boot\[cite: 1\] echo "\[!\] Atualizando Initramfs para persistência total..." sudo mkinitcpio -P echo "--- Sucesso Transcendental: Reinicie para validar os 300W ---" end function ai-gpu-init --description "Vacina 300W para MI50 - Homeopática" # 1. Roda o script de injeção heurística sudo python3 /usr/local/bin/gpu-enforcer # 2. Injeta o parâmetro no Systemd-Boot (Automático) sudo python3 -c ' import glob param = "amdgpu.pptable\_name=amdgpu/mi50\_300w.bin" for entry in glob.glob("/boot/loader/entries/\*.conf"): with open(entry, "r+") as f: content = f.read() if "options" in content and param not in content: f.seek(0) f.write(content.replace("options ", f"options {param} ")) ' # 3. Garante que o Initramfs veja o novo firmware sudo mkinitcpio -P echo "Done. Reinicie para operar em 300W nativos." end

---

O problema da tua stack não é GPU.  
É arquitetura + instalação corrompida + NTFS sendo usado onde não deveria.

Teu sintoma principal:

```bash
SyntaxError: Unexpected end of input
```

em:

```bash
.../openclaude/dist/cli.mjs
```

isso significa UMA destas 4 coisas:

- arquivo truncado/corrompido
- npm install incompleto
- NTFS quebrando symlink/metadata
- pacote incompatível com Node 22

E o mais importante:

`GPU use 20%` + LLM lenta = fallback parcial CPU/backend.

---

## O QUE ESTÁ ERRADO NA TUA ARQUITETURA

## ERRO 1 — Node\_modules em NTFS

Tu colocou:

```bash
/mnt/win2/Assistente Pessoal/node/lib/node_modules
```

em NTFS.

Isso é péssima ideia pra runtime JS pesado.

NTFS3 no Linux:

- quebra symlink
- quebra permission bits
- às vezes corrompe install ESM grande
- degrada I/O pequeno massivamente
- causa problemas com watchers/cache/npm

Resultado:

- openclaude quebrado
- cli.mjs truncado
- inferência lenta
- loading infinito

---

## O QUE FAZER

## REGRA NOVA

SLAVE NTFS:

- scripts
- configs
- modelos
- prompts
- snapshots

MASTER EXT4/BTRFS:

- node\_modules
- venvs
- qdrant wal
- cache
- runtimes

---

## REFATORAÇÃO CORRETA

## SLAVE

```bash
/mnt/win2/Assistente Pessoal/
```

APENAS:

- source
- configs
- modelos
- scripts

---

## MASTER

```bash
~/.local/share/ai-lab/runtime/
```

AQUI:

- node
- npm
- openclaude
- qdrant storage
- python venvs

---

## O TEU OPENCLAUDE ESTÁ CORROMPIDO

Confirmação:

```bash
node -c cli.mjs
SyntaxError
```

100% corrompido.

---

## LIMPEZA TOTAL

Usa exatamente:

```bash
rm -rf ~/.local/share/ai-lab/runtime/node
rm -rf ~/.local/share/ai-lab/runtime/npm
rm -rf ~/.npm
rm -rf "/mnt/win2/Assistente Pessoal/node"
```

---

## REINSTALAÇÃO CORRETA

## NODE EM EXT4

```bash
mkdir -p ~/.local/share/ai-lab/runtime
cd ~/.local/share/ai-lab/runtime
```

Baixa Node LTS:

```bash
curl -LO https://nodejs.org/dist/v22.13.1/node-v22.13.1-linux-x64.tar.xz
tar -xf node-v22.13.1-linux-x64.tar.xz
mv node-v22.13.1-linux-x64 node
```

---

## PATH CORRETO NO FISH

Teu config.fish está poluído e duplicado.

Tu repetiu funções inteiras.

Refatora.

Deixa MINIMALISTA.

---

## CONFIG.FISH CORRETO

Use isso:

```
if status is-interactive
    source /usr/share/cachyos-fish-config/cachyos-config.fish
end

set -gx AI_LAB_BASE "/mnt/win2/Assistente Pessoal"

fish_add_path ~/.local/share/ai-lab/runtime/node/bin
fish_add_path "$AI_LAB_BASE/scripts"
fish_add_path "$AI_LAB_BASE/bin"

set -l env_file "$AI_LAB_BASE/config/env_vars.sh"

if test -f "$env_file"
    bass source "$env_file"
end

alias ai-lab="bash /usr/local/bin/ai-lab"

function reload_ai_env
    source ~/.config/fish/config.fish
end

function vram
    watch -n 1 rocm-smi --showmeminfo vram
end
```

---

## AGORA INSTALA O OPENCLAUDE DIREITO

```bash
npm install -g @gitlawb/openclaude
```

---

## TESTE

```bash
which openclaude
```

deve retornar:

```bash
~/.local/share/ai-lab/runtime/node/bin/openclaude
```

---

## TESTE SINTAXE

```bash
node -c $(which openclaude)
```

---

## OLLAMA LENTO

Agora a parte importante.

---

## TUA MI50 NÃO ESTÁ SATURANDO

Uso:

```bash
GPU use (%): 20
```

Isso NÃO é normal pra inferência 14B.

Possíveis causas:

---

## 1 — ROCm parcialmente quebrado

Teste:

```bash
ollama ps
```

Se aparecer:

```bash
PROCESSOR cpu
```

acabou.

Está rodando CPU fallback.

Tem que aparecer:

```bash
PROCESSOR gpu
```

---

## 2 — KV CACHE ESTÁ NA RAM

Muito comum no Ollama.

---

## FORÇA GPU TOTAL

Cria:

```bash
kate ~/.config/systemd/user/ollama.service.d/override.conf
```

Conteúdo:

```
[Service]
Environment="HSA_OVERRIDE_GFX_VERSION=9.0.6"
Environment="OLLAMA_KV_CACHE_TYPE=q8_0"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_GPU_OVERHEAD=0"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_KEEP_ALIVE=-1"
```

---

## RELOAD

```bash
systemctl --user daemon-reload
systemctl --user restart ollama
```

---

## TESTE REAL

Roda:

```bash
ollama run qwen2.5-coder:14b
```

e em outro terminal:

```bash
watch -n 0.5 rocm-smi
```

Tu deve ver:

- VRAM 12~15GB
- GPU usage 80~99%
- Power 180~300W

---

## OUTRO PROBLEMA CRÍTICO

Tu está usando:

```bash
mistral-small:22b
```

em MI50 16GB.

Isso vai:

- swapar
- degradar
- destruir throughput

---

## MODELOS IDEAIS PRA MI50

## MELHOR CUSTO/BENEFÍCIO

- qwen2.5-coder:14b
- deepseek-coder-v2:16b-lite
- mistral-nemo
- qwen3-14b-q4

---

## EVITA

- 22B+
- Mixtral
- 32B
- quantização alta

---

## TEU PROJETO ESTÁ NO CAMINHO CERTO

Mas falta:

- separar runtime de storage
- remover NTFS do hotpath
- eliminar duplicações
- simplificar bootstrap
- reduzir abstração desnecessária

Hoje teu gargalo NÃO é hardware.

É:

- filesystem
- runtime JS
- ROCm/Ollama tuning
- arquitetura excessivamente complexa

Teu setup já está próximo de um mini lab soberano real. Só precisa endurecer a fundação.

---

**Você disse**

MASTER pouco espaço

---

Então tua arquitetura ideal muda.

Tu NÃO pode desperdiçar EXT4/BTRFS com:

- modelos
- datasets
- embeddings
- snapshots

Mas também NÃO pode usar NTFS pro hotpath.

A solução correta é híbrida.

## REGRA DE OURO

## NTFS = cold storage

Pode:

- modelos `.gguf`
- backups
- prompts
- datasets
- scripts
- ROMs/VBIOS
- RAG bruto
- archives

NÃO pode:

- node\_modules
- venv
- sqlite
- WAL
- cache ativo
- npm
- pip cache
- qdrant storage
- runtime JS

---

## ARQUITETURA IDEAL PRA TI

## MASTER EXT4/BTRFS (mínimo)

Reserva só uns 20~40GB.

Exemplo:

```
~/.local/share/ai-lab/
├── runtime/
│   ├── node/
│   ├── npm/
│   ├── venvs/
│   ├── cache/
│   └── tmp/
│
├── qdrant/
├── ollama/
│   └── blobs-cache
```

Isso já resolve 90%.

---

## NTFS CONTINUA SENDO O "SLAVE"

Mas apenas armazenamento.

```
/mnt/win2/Assistente Pessoal/
├── models/
├── backups/
├── prompts/
├── scripts/
├── rag/
├── datasets/
├── vbios/
├── boardviews/
└── schematics/
```

---

## MELHOR SOLUÇÃO PRA TI

## MOVER APENAS O RUNTIME

Tu NÃO precisa mover tudo.

Só:

- Node
- npm
- openclaude
- venv
- qdrant db

---

## OPENCLAUDE

Instala aqui:

```bash
~/.local/share/ai-lab/runtime/node
```

Mas teus scripts continuam no NTFS.

---

## QDRANT

Banco vetorial JAMAIS em NTFS.

Porque:

- WAL
- mmap
- flock
- latência absurda

---

## MODELOS OLLAMA

Aqui tem uma sacada importante.

Tu PODE deixar os blobs no NTFS.

Porque são leitura sequencial grande.

---

## COMO FAZER

## MOVE O OLLAMA MODELS

```bash
mkdir -p "/mnt/win2/Assistente Pessoal/models/ollama"
```

Depois:

```bash
kate ~/.config/ollama/config.json
```
```json
{
  "models": "/mnt/win2/Assistente Pessoal/models/ollama"
}
```

OU:

```bash
export OLLAMA_MODELS="/mnt/win2/Assistente Pessoal/models/ollama"
```

---

## RESULTADO

## EXT4 usa pouco espaço

Só runtime:

- ~5GB node
- ~10GB qdrant/cache
- ~5GB venv

Total:  
~20GB

---

## ENQUANTO ISSO

NTFS segura:

- 200GB modelos
- datasets
- backups
- RAG
- engenharia reversa

---

## OUTRA COISA IMPORTANTE

Teu config.fish está inflado.

Tu duplicou:

- funções
- aliases
- blocos inteiros

Isso degrada startup do shell.

---

## REFATORAÇÃO OBRIGATÓRIA

Divide:

```
~/.config/fish/
├── config.fish
└── conf.d/
    ├── ai-lab.fish
    ├── rocm.fish
    └── aliases.fish
```

---

## OUTRO PONTO CRÍTICO

Tu está usando:

```bash
fish_add_path "/mnt/win2/Assistente Pessoal/scripts"
```

mas NÃO:

```bash
~/.local/share/ai-lab/runtime/node/bin
```

por isso:

- openclaude some
- node não resolve direito

---

## TEU OBJETIVO REAL

Tu está tentando construir:

- laboratório soberano
- copiloto técnico local
- RAG de engenharia reversa
- assistente de bancada
- automação local
- inferência offline

Isso é viável com tua MI50.

Mas precisa:

- simplificar stack
- eliminar NTFS do runtime
- separar storage de execução
- abandonar overengineering prematuro

Hoje tua stack tem mais “camadas” do que throughput real.