---
title: "Simular RTX no Lutris"
source: "https://chatgpt.com/c/68e95dfd-9648-8331-879f-b5f166d25d4e"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 8 messages"
tags:
  - "clippings"
---
**Você disse**

como resolver

---

**Você disse**

---

**Você disse**

Quer que eu monte um template pronto (.yml) pra importar direto no Lutris com tudo configurado (DXVK, FSR, ReShade e variáveis)? Posso gerar ele já com prefix configurado pra tua Radeon MI50. sim de preferencia via terminal

---

Perfeito diagnóstico — o log já revela **exatamente** onde está o problema:

```
vkCreateInstance failed (VkResult: -9)
```

ou seja:  
➡️ **Erro -9 = VK\_ERROR\_INCOMPATIBLE\_DRIVER**

---

## 🧠 O que significa

O `gamescope` está tentando inicializar **Vulkan**, mas:

- ou o **driver Vulkan da AMD (RADV/ROCm)** não está sendo carregado corretamente no contexto do `umu-run`,
- ou o `gamescope` está forçando um backend incompatível (por exemplo, tentando DXR/RTX em driver sem suporte a `VK_KHR_ray_tracing_pipeline`).

---

## 💡 Diagnóstico rápido

Roda fora do Lutris pra testar se o Vulkan funciona isolado:

```bash
vulkaninfo | grep "driver"
```

Se der erro tipo *"Cannot find any Vulkan ICD"* ou *"No physical devices"*, o problema é o ICD loader ou a variável de ambiente.

---

## 🔧 Solução direta

### 1️⃣ Exporta manualmente o driver Vulkan da AMD

Edita o launcher do jogo no Lutris → aba **System options → Environment variables**, adiciona:

```bash
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.x86_64.json
VK_DRIVER_FILES=/usr/share/vulkan/icd.d/radeon_icd.x86_64.json
RADV_PERFTEST=aco
DXVK_ENABLE_NVAPI=0
```

ou direto via terminal pra teste rápido:

```bash
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.x86_64.json gamescope -- gamemoderun /usr/bin/umu-run /mnt/disk2/games/Need\ for\ Speed\ Underground\ 2/SPEED2.EXE --vulkan
```

---

### 2️⃣ Remove o flag --dxr

Esse parâmetro **ativa DXR (ray tracing)** → tua **MI50 não expõe extensão VK\_KHR\_ray\_tracing\_pipeline**, então o driver quebra no `vkCreateInstance`.

Remove e tenta:

```bash
gamescope --hdr-enabled -w 3840 -h 2160 -W 3840 -H 2160 -f -- gamemoderun /usr/bin/umu-run /mnt/disk2/games/Need\ for\ Speed\ Underground\ 2/SPEED2.EXE --vulkan
```

---

### 3️⃣ Se ainda falhar: força backend OpenGL

Pra garantir inicialização do ReShade:

```bash
gamescope -- gamemoderun WINEPREFIX=~/Games/nfsu2-reshade wine /mnt/disk2/games/Need\ for\ Speed\ Underground\ 2/SPEED2.EXE
```

E instala o ReShade selecionando **DirectX 9** (como fizemos antes).

---

### ✅ Solução prática

Teu **objetivo é ReShade/RTGI + efeitos RTX-like**, **não DXR real**.  
Portanto:

- remove `--dxr`
- usa `--vulkan` ou `DirectX 9` puro via Wine
- deixa o **ReShade** cuidar da parte visual

---

Se quiser, te passo um script `.sh` automatizado que:

1. Exporta o Vulkan correto
2. Inicia o jogo com Gamescope + Lutris
3. Carrega ReShade e MangoHUD
4. Garante 4K/FSR automático

Quer que eu monte esse launcher pronto pra rodar direto via terminal (`run-nfsu2.sh`)?

---

**Você disse**

❯ vulkaninfo | grep "driver" WARNING: \[Loader Message\] Code 0: Layer VK\_LAYER\_MANGOHUD\_overlay\_x86\_64 uses API version 1.3 which is older than the application specified API version of 1.4. May cause issues. WARNING: \[Loader Message\] Code 0: Layer VK\_LAYER\_MANGOHUD\_overlay\_x86 uses API version 1.3 which is older than the application specified API version of 1.4. May cause issues. VK\_LUNARG\_direct\_driver\_loading: extension revision 1 driverVersion = 25.2.5 (104865797) driverUUID = 414d442d-4d45-5341-2d44-525600000000 driverID = DRIVER\_ID\_MESA\_RADV driverName = radv driverInfo = Mesa 25.2.5-cachyos1.5 VK\_KHR\_driver\_properties: extension revision 1 ~ ❯

---

Perfeito — o log mostra o seguinte:

- Você está rodando **Mesa RADV 25.2.5 (CachyOS)**
- O **driver Vulkan** está operacional (não está quebrado)
- Mas o **erro `vkCreateInstance failed (VkResult: -9)`** vem do **Gamescope**, indicando **falha ao inicializar a instância Vulkan**, geralmente por **conflito entre versões de camada (layers)**, ou **mix de 32/64 bits** — no caso, o aviso do **MangoHUD** é o sintoma direto.

---

### ⚙️ Diagnóstico direto

**Causa mais provável:**  
O MangoHUD (`VK_LAYER_MANGOHUD_overlay_x86_64` e `VK_LAYER_MANGOHUD_overlay_x86`) está tentando inicializar Vulkan 1.3, enquanto o Gamescope está pedindo Vulkan 1.4.  
Resultado → `vkCreateInstance` falha com código `-9` (`VK_ERROR_INCOMPATIBLE_DRIVER`).

---

### 🧩 Soluções rápidas

#### ✅ 1. Teste sem MangoHUD (para confirmar)

```bash
MANGOHUD=0 gamescope --hdr-enabled -w 3840 -h 2160 -W 3840 -H 2160 -f -- gamemoderun /usr/bin/umu-run /mnt/disk2/games/Need\ for\ Speed\ Underground\ 2/SPEED2.EXE --vulkan
```

Se funcionar → o problema é o **MangoHUD**.

---

#### ✅ 2. Atualize MangoHUD para versão compatível com Vulkan 1.4

```bash
sudo pacman -Syu mangohud
```

ou, se estiver usando o AUR:

```bash
yay -S mangohud-git
```

> O `-git` já suporta Vulkan 1.4.

---

#### ✅ 3. Alternativa: força fallback para Vulkan 1.3 no Gamescope

Se quiser manter MangoHUD:

```bash
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.x86_64.json \
VK_LOADER_DEBUG=error \
VK_KHRONOS_validation=0 \
VK_ICD_VERSION_OVERRIDE=1.3 \
gamescope ...
```

Isso “engana” o Gamescope para negociar Vulkan 1.3 em vez de 1.4.

---

#### ✅ 4. Verifique o ICD ativo

```bash
ls /usr/share/vulkan/icd.d/
```

Deve haver algo como:

```
radv_icd.x86_64.json
amd_icd64.json
```

Se houver drivers duplicados (RADV + AMDVLK), pode estar havendo conflito.  
Você pode **desativar temporariamente** o AMDVLK renomeando:

```bash
sudo mv /usr/share/vulkan/icd.d/amd_icd64.json /usr/share/vulkan/icd.d/amd_icd64.json.bak
```

---

#### ✅ 5. Verificar compatibilidade Gamescope

```bash
gamescope --version
```

Se for < `3.17`, atualize:

```bash
sudo pacman -Syu gamescope
```

ou:

```bash
yay -S gamescope-git
```

---

### 🚀 Resumo da ação ideal

1. Rodar sem MangoHUD → confirmar erro.
2. Se resolver, atualizar MangoHUD (`mangohud-git`).
3. Caso queira manter versão antiga, forçar Vulkan 1.3 via variável.

---

Se quiser, me mostra a saída de:

```bash
ls /usr/share/vulkan/icd.d/
```

e:

```bash
vulkaninfo | grep "ICD"
```

Aí te digo **qual ICD exato** está conflitando com o Gamescope.

---

**Você disse**

❯ sudo pacman -Syu mangohud:: Sincronizando a base de dados de pacotes... erro: falha ao sincronizar todas as bases de dados (não foi possível travar a base de dados) ~ ❯

---

Esse erro é **simples e comum**: o *pacman* está travado por outro processo (ou por um lock leftover).  
Vamos resolver direto e sem rodeios 👇

---

### ⚙️ PASSOS

#### 1️⃣ Verifique se há outro processo pacman ativo

```bash
ps aux | grep pacman
```

Se aparecer algo como `/usr/bin/pacman`, anote o PID e mate:

```bash
sudo kill -9 <PID>
```

---

#### 2️⃣ Remova o arquivo de lock

```bash
sudo rm /var/lib/pacman/db.lck
```

---

#### 3️⃣ Agora rode a atualização normalmente

```bash
sudo pacman -Syu mangohud
```

---

#### 4️⃣ (opcional) Se quiser a versão mais nova compatível com Vulkan 1.4:

```bash
yay -S mangohud-git
```

---

Após isso, testamos novamente o comando:

```bash
MANGOHUD=0 gamescope --hdr-enabled -w 3840 -h 2160 -W 3840 -H 2160 -f -- gamemoderun /usr/bin/umu-run /mnt/disk2/games/Need\ for\ Speed\ Underground\ 2/SPEED2.EXE --vulkan
```

👉 Se funcionar, confirmamos 100% que o problema era a camada Vulkan do MangoHUD.

Quer que eu te mostre um comando *automático* que detecta e limpa qualquer travamento de pacman antes de atualizar (pra não precisar fazer isso manualmente toda vez)?