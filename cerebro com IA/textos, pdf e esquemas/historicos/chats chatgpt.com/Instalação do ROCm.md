---
title: "Instalação do ROCm"
source: "https://chatgpt.com/c/69f64042-1560-83e9-a0be-ce7fff0fe420"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 2 messages"
tags:
  - "clippings"
---
**Você disse**

~ ❯ rocm-smi fish: Unknown command: rocm-smi ~ ❯

---

Direto ao ponto: **o ROCm não está instalado corretamente (ou não está no PATH)**.

### 1\. Confirma se o pacote existe

No teu sistema (CachyOS/Arch-based), roda:

```bash
pacman -Qs rocm
```

Se não aparecer nada relevante → ROCm não está instalado.

---

### 2\. Instala o ROCm corretamente (Arch/CachyOS)

Para tua **MI50 (Vega 20)**, usa:

```bash
sudo pacman -S rocm-hip-sdk rocm-opencl-sdk rocm-smi-lib
```

Se quiser completo:

```bash
sudo pacman -S rocm-dev
```

---

### 3\. O binário pode ter nome diferente

No Arch, o comando geralmente é:

```bash
/opt/rocm/bin/rocm-smi
```

Testa direto:

```bash
/opt/rocm/bin/rocm-smi
```

Se funcionar → é só PATH errado.

---

### 4\. Corrige o PATH (fish)

Adiciona isso no teu config:

```
set -Ux PATH /opt/rocm/bin $PATH
```

Reabre o terminal.

---

### 5\. Teste real da GPU (mais confiável que rocm-smi)

```bash
/opt/rocm/bin/rocminfo
```

Se não listar a MI50 → problema mais profundo (driver/kernel/firmware).

---

### 6\. Ponto crítico pro teu setup (MI50 mod Pro VII)

Você está com VBIOS modificada → então:

- Kernel precisa ter suporte amdgpu correto
- Firmware precisa estar ok (`linux-firmware`)
- Parâmetro pode ser necessário:
```bash
amdgpu.ppfeaturemask=0xffffffff
```

---

### 7\. Diagnóstico rápido

Roda isso e me manda:

```bash
ls /opt/rocm/bin
lspci | grep VGA
dmesg | grep amdgpu
```

---

### Insight direto (nível engenharia)

`rocm-smi` é superficial. O que importa mesmo:

- `rocminfo` → detecta compute stack
- `hipcc --version` → toolchain
- `clinfo` → OpenCL funcional

Se esses 3 falharem → teu problema não é comando, é stack quebrada.

---

Se quiser, eu já te monto um **ambiente ROCm otimizado pra MI50 (com tuning + estabilidade VRM)** baseado no teu mod.