---
title: "Testes e otimização MI50"
source: "https://chatgpt.com/c/6a08cd22-63c0-83e9-944f-82adc60301c2"
author:
published:
created: 2026-07-17
description: "O ChatGPT é seu assistente de IA para uso diário. Converse com a IA mais avançada para explorar ideias, resolver problemas e aprender mais rápido."
tags:
  - "clippings"
---
**Você disse**

testes e otimizaçao

---

Para o teu cenário — laboratório híbrido Linux + MI50 + engenharia reversa + IA local + CachyOS — “testes e otimização” precisam seguir uma lógica de engenharia real:

Ordem certa:

1. estabilidade elétrica
2. estabilidade térmica
3. estabilidade kernel/driver
4. throughput GPU
5. latência IO
6. tuning de inferência
7. automação/autocorreção

A maioria tenta começar no item 6 e quebra tudo.

---

## 2\. Benchmark base obrigatório

Antes de otimizar qualquer coisa:

## CPU

```bash
stress-ng --cpu 36 --cpu-method matrixprod --timeout 300s --metrics-brief
```

## RAM

```bash
stress-ng --vm 8 --vm-bytes 24G --timeout 300s --metrics-brief
```

## SSD/NVMe

```bash
fio --name=randrw \
--rw=randrw \
--size=8G \
--bs=4k \
--iodepth=64 \
--runtime=60 \
--numjobs=4 \
--time_based
```

Instala:

```bash
sudo pacman -S stress-ng fio
```

---

## 3\. Diagnóstico real da MI50

Tua MI50 é Vega20 enterprise.

O gargalo normalmente NÃO é shader.

É:

- power throttling
- hotspot
- HBM clock instability
- PCIe ASPM
- scheduler do kernel
- ROCm incompleto
- VRM entrando em proteção

---

## 4\. Teste REAL da GPU

## Instalar ferramentas

```bash
sudo pacman -S radeontop vulkan-tools mesa-utils
```

## Uso GPU realtime

```bash
radeontop
```

## Vulkan

```bash
vkcube
```

## OpenGL

```bash
glxgears
```

---

## 5\. Verificar clocks reais

```bash
watch -n1 cat /sys/class/drm/card1/device/pp_dpm_sclk
```

HBM:

```bash
watch -n1 cat /sys/class/drm/card1/device/pp_dpm_mclk
```

Temperatura:

```bash
watch -n1 cat /sys/class/drm/card1/device/hwmon/hwmon*/temp1_input
```

---

## 6\. ASPM — desabilitar

Vega20 sofre MUITO com ASPM.

No GRUB:

```bash
pcie_aspm=off
```

Editar:

```bash
sudo nano /etc/default/grub
```

Adicionar em:

```bash
GRUB_CMDLINE_LINUX_DEFAULT=
```

Depois:

```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

---

## 7\. Scheduler ideal CachyOS

Pra IA + inferência:

## Melhor:

- BORE
- sched-ext

---

**Você disse**

examine problema: ~ ❯ bash \[johncoffee@JohnCoffeeDesk ~\]$ # numactl reduz latência NUMA no Xeon v3 numactl --cpunodebind=0 --membind=0 \\./llama-server \\ --model qwen2.5-coder-14b-q4.gguf \\ -ngl 99 \\ # todas as layers na MI50 -c 8192 \\ # contexto conservador --batch-size 128 \\ # Xeon v3 suporta --ubatch-size 64 \\ # micro-batch reduz latência --threads 12 \\ # metade dos cores do v3 --host 0.0.0.0 --port 8080 numactl: execution of `./llama-server': No such file or directory bash: -c: comando não encontrado bash: --batch-size: comando não encontrado bash: --ubatch-size: comando não encontrado bash: --threads: comando não encontrado bash: --host: comando não encontrado [johncoffee@JohnCoffeeDesk ~]$ [johncoffee@JohnCoffeeDesk ~]$ HSA_OVERRIDE_GFX_VERSION=9.0.6 HSA_ENABLE_SDMA=0 # evita crash no gfx906 GPU_MAX_ALLOC_PERCENT=100 # usa VRAM completa ROCM_PATH=/opt/rocm [johncoffee@JohnCoffeeDesk ~]$ ` resposta: # 1. Variáveis de Ambiente ROCM (Configurações de GPU) export HSA\_OVERRIDE\_GFX\_VERSION=9.0.6 export HSA\_ENABLE\_SDMA=0 export GPU\_MAX\_ALLOC\_PERCENT=100 export ROCM\_PATH=/opt/rocm # 2. Execução do Servidor (Comando Limpo) numactl --cpunodebind=0 --membind=0./llama-server \\ --model qwen2.5-coder-14b-q4.gguf \\ -ngl 99 \\ -c 8192 \\ --batch-size 128 \\ --ubatch-size 64 \\ --threads 12 \\ --host 0.0.0.0 \\ --port 8080

---

O problema foi sintaxe shell quebrada.

Você colou comentários `#` no meio da continuação `\`.

No Bash:

```bash
comando \
# comentario
argumento
```

\= quebra a linha anterior.

Então o shell tentou executar:

```bash
--batch-size
```

como comando separado.

Além disso:

```bash
numactl: execution of './llama-server': No such file or directory
```

significa:

- você NÃO estava no diretório do `llama-server`  
	OU
- binário não compilado  
	OU
- nome diferente (`llama-cli`, `server`, etc)

## Diagnóstico correto

## 1\. Verificar binário

Execute:

```bash
find ~/ -name "llama-server" 2>/dev/null
```

ou:

```bash
find /mnt/win2 -name "llama-server" 2>/dev/null
```

---

## 2\. Entrar no diretório correto

Exemplo:

```bash
cd /mnt/win2/Assistente\ Pessoal/llama.cpp
```

---

## 3\. Confirmar existência

```bash
ls -lah
```

Você precisa ver:

```bash
llama-server
```

ou:

```bash
bin/llama-server
```

---

## 4\. Comando correto

SEM comentários quebrando linha:

```bash
export HSA_OVERRIDE_GFX_VERSION=9.0.6
export HSA_ENABLE_SDMA=0
export GPU_MAX_ALLOC_PERCENT=100
export ROCM_PATH=/opt/rocm

numactl --cpunodebind=0 --membind=0 \
./llama-server \
--model qwen2.5-coder-14b-q4.gguf \
-ngl 99 \
-c 8192 \
--batch-size 128 \
--ubatch-size 64 \
--threads 12 \
--host 0.0.0.0 \
--port 8080
```

---

## 5\. Melhor ainda pro teu setup

Xeon v3 + MI50 + ROCm:

```bash
export HSA_OVERRIDE_GFX_VERSION=9.0.6
export HSA_ENABLE_SDMA=0
export GPU_MAX_ALLOC_PERCENT=100
export GPU_SINGLE_ALLOC_PERCENT=100
export HIP_VISIBLE_DEVICES=0
export OMP_NUM_THREADS=12
export GGML_NUMA=1

numactl --cpunodebind=0 --membind=0 \
./llama-server \
--model qwen2.5-coder-14b-q4.gguf \
-ngl 99 \
-c 8192 \
--batch-size 256 \
--ubatch-size 64 \
--threads 12 \
--flash-attn \
--mlock \
--host 0.0.0.0 \
--port 8080
```

---

## 6\. Possível próximo erro

Se aparecer:

```bash
HIP error
```

ou:

```bash
invalid device function
```

então:

- teu llama.cpp NÃO foi compilado com ROCm  
	OU
- compilou com arquitetura errada

---

## 7\. Build correto da MI50

Vega20 = gfx906

Compila assim:

```bash
cmake -B build \
-DGGML_HIP=ON \
-DAMDGPU_TARGETS=gfx906 \
-DCMAKE_BUILD_TYPE=Release

cmake --build build -j$(nproc)
```

Executa:

```bash
./build/bin/llama-server
```

---

## 8\. Otimização REAL pra tua máquina

Teu setup provavelmente performa melhor com:

| parâmetro | valor |
| --- | --- |
| threads | 12 |
| batch-size | 256 |
| ubatch-size | 64 |
| ngl | 99 |
| ctx | 8192 |
| flash-attn | ON |
| numa | ON |

Porque:

- Xeon v3 sofre com cross-node latency
- MI50 gosta de batch maior
- ubatch pequeno estabiliza HBM
- flash-attn reduz gargalo memória

---

## 9\. Teste de throughput

Depois roda:

```bash
curl http://127.0.0.1:8080/health
```

Benchmark:

```bash
./llama-bench -m qwen2.5-coder-14b-q4.gguf -ngl 99
```

---

## 10\. Gargalo oculto do teu setup

Muito provavelmente hoje:

- PCIe ASPM
- NUMA mal distribuído
- HBM throttling
- scheduler
- ROCm fragmentando VRAM

não a GPU em si.

A MI50 ainda é extremamente forte pra inferência Q4/Q5.