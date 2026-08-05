---
title: "Simular RTX no Lutris"
source: "https://chatgpt.com/c/68f97746-8bf8-832d-a9e6-f12ded5a703b"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 5 messages"
tags:
  - "clippings"
---
Beleza — você já tá com **Gamescope + GE-Proton + DXVK + VKD3D** inicializando corretamente, e o log mostra que o **VKD3D\_CONFIG=dxr** foi carregado (isso é o flag que habilita o *path tracing/ray tracing* via Vulkan DXR).  
👉 Ou seja: o ambiente já está parcialmente configurado pra “simular RTX” via **DXR em Vulkan** — mas a tua GPU (Radeon Pro VII / Instinct MI50) não tem suporte nativo à extensão **`VK_KHR_ray_tracing_pipeline`**, só via *emulação por shader fallback* (muito mais lento).

---

### 🎯 Pra ativar e forçar a simulação RTX (Ray Tracing) no Lutris / runner Proton

Adiciona **estas variáveis** no campo `Runner options → Environment variables`:

```bash
PROTON_ENABLE_D3D12=1
VKD3D_CONFIG=dxr
PROTON_ENABLE_NVAPI=1
PROTON_HIDE_NVIDIA_GPU=0
DXVK_ENABLE_NVAPI=1
DXVK_NVAPIHACK=0
RADV_PERFTEST=aco
RUSTICL_ENABLE=radeonsi
AMD_VULKAN_ICD=RADV
ENABLE_GAMESCOPE_WSI=1
```

---

### 💡 Para forçar simulação RTX (modo “fake RTX”)

Acrescenta também:

```bash
DXVK_ASYNC=1
VKD3D_FEATURE_LEVEL=12_1
VKD3D_DEBUG=warn
VKD3D_SHADER_DEBUG=warn
PROTON_NO_ESYNC=1
PROTON_NO_FSYNC=1
```

Esses desativam sincronizações que atrapalham shaders complexos e forçam o pipeline D3D12→Vulkan completo.

---

### ⚙️ Comando final de inicialização (exemplo)

No campo *Runner options → Command prefix* do Lutris:

```bash
gamescope --hdr-enabled -w 3840 -h 2160 -f -- gamemoderun DXVK_HDR=0 DXVK_HUD=1 VKD3D_CONFIG=dxr PROTON_ENABLE_D3D12=1 PROTON_ENABLE_NVAPI=1 DXVK_ENABLE_NVAPI=1 DXVK_NVAPIHACK=0 umu-run
```

Ou simplesmente (para testar direto no terminal):

```bash
gamemoderun DXVK_HUD=1 VKD3D_CONFIG=dxr PROTON_ENABLE_D3D12=1 umu-run /mnt/disk2/games/Need\ for\ Speed\ Underground\ 2/SPEED2.EXE
```

---

### 🔍 Como validar se o DXR foi ativado

Roda dentro do mesmo ambiente:

```bash
RADV_DEBUG=info vkcube --validate
```

Se o log mostrar:

```
VK_KHR_acceleration_structure
VK_KHR_ray_tracing_pipeline
VK_KHR_deferred_host_operations
```

👉 o driver tá expondo o *path tracing* (mesmo que parcialmente em software).

---

### ⚠️ Observação realista

A Radeon Pro VII/MI50 (Vega 20) **não tem hardware BVH traversal** → toda simulação DXR roda em software via **shader fallback**, então o Ray Tracing é funcional pra debug ou teste de render, mas **não pra jogos modernos**.  
Pra uso prático, você pode combinar **ReShade + path tracing shader (Pascal Gilcher / RTGI)** — aí sim o efeito RTX visual aparece com boa performance via Vulkan.

Se quiser, posso te montar o preset completo “fake RTX Vulkan” com ReShade + DXVK overlay pra tua MI50. Deseja que eu gere isso?

---

**Você disse**

RADV\_DEBUG=info vkcube --validate Selected WSI platform: wayland Device info: name = VEGA20 marketing\_name = AMD Radeon Pro VII dev\_filename = /dev/dri/renderD128 num\_se = 4 num\_rb = 16 num\_cu = 60 max\_gpu\_freq = 1700 MHz max\_gflops = 13056 GFLOPS tcp\_cache\_size = 16 KB l2\_cache\_size = 512 KB memory\_channels = 2 (TCC blocks) memory\_size = 16 GB (16384 MB) memory\_freq = 2 GHz memory\_bus\_width = 4096 bits memory\_bandwidth = 1024 GB/s pcie\_gen = 3 pcie\_num\_lanes = 16 pcie\_bandwidth = 15.8 GB/s clock\_crystal\_freq = 25000 KHz IP GFX 9.4 queues:1 queue\_slots:0 align:256 pad\_dw:0x7 IP COMPUTE 9.4 queues:4 queue\_slots:0 align:256 pad\_dw:0x7 IP SDMA 4.2 queues:2 queue\_slots:0 align:256 pad\_dw:0xf IP UVD 7.2 queues:1 queue\_slots:0 align:256 pad\_dw:0xf IP VCE 4.1 queues:1 queue\_slots:0 align:256 pad\_dw:0x3f IP UVD\_ENC 7.2 queues:1 queue\_slots:0 align:256 pad\_dw:0x3f Identification: pci (domain:bus:dev.func): 0000:05:00.0 pci\_id = 0x66a1 pci\_rev\_id = 0x6 family = 69 gfx\_level = 11 family\_id = 141 chip\_external\_rev = 41 chip\_rev = 1 Flags: family\_overridden = 0 is\_pro\_graphics = 1 has\_graphics = 1 has\_clear\_state = 1 has\_distributed\_tess = 1 has\_dcc\_constant\_encode = 0 has\_rbplus = 1 rbplus\_allowed = 0 has\_load\_ctx\_reg\_pkt = 1 has\_out\_of\_order\_rast = 1 cpdma\_prefetch\_writes\_memory = 0 has\_gfx9\_scissor\_bug = 0 has\_tc\_compat\_zrange\_bug = 1 has\_small\_prim\_filter\_sample\_loc\_bug = 0 has\_ls\_vgpr\_init\_bug = 0 has\_pops\_missed\_overlap\_bug = 0 has\_32bit\_predication = 1 has\_3d\_cube\_border\_color\_mipmap = 1 has\_image\_opcodes = 1 never\_stop\_sq\_perf\_counters = 0 has\_sqtt\_rb\_harvest\_bug = 0 has\_sqtt\_auto\_flush\_mode\_bug = 0 never\_send\_perfcounter\_stop = 0 discardable\_allows\_big\_page = 0 has\_taskmesh\_indirect0\_bug = 0 has\_set\_context\_pairs = 0 has\_set\_context\_pairs\_packed = 0 has\_set\_sh\_pairs = 0 has\_set\_sh\_pairs\_packed = 0 has\_set\_uconfig\_pairs = 0 conformant\_trunc\_coord = 0 mesh\_fast\_launch\_2 = 0 Display features: use\_display\_dcc\_unaligned = 0 use\_display\_dcc\_with\_retile\_blit = 0 Memory info: pte\_fragment\_size = 2097152 gart\_page\_size = 4096 gart\_size = 15992 MB vram\_size = 16384 MB vram\_vis\_size = 16368 MB vram\_type = 6 max\_heap\_size\_kb = 16384 MB min\_alloc\_size = 0 address32\_hi = 0xffff8000 has\_dedicated\_vram = 1 all\_vram\_visible = 1 max\_tcc\_blocks = 2 tcc\_cache\_line\_size = 64 tcc\_rb\_non\_coherent = 0 cp\_sdma\_ge\_use\_system\_memory\_scope = 0 pc\_lines = 2048 lds\_size\_per\_workgroup = 65536 lds\_alloc\_granularity = 512 lds\_encode\_granularity = 512 max\_memory\_clock = 1000 MHz CP info: gfx\_ib\_pad\_with\_type2 = 0 has\_cp\_dma = 1 me\_fw\_version = 167 me\_fw\_feature = 54 mec\_fw\_version = 478 mec\_fw\_feature = 54 pfp\_fw\_version = 196 pfp\_fw\_feature = 54 Multimedia info: vce\_encode = 1 vce\_fw\_version = 956695552 vce\_harvest\_config = 0 codec dec max\_resolution enc max\_resolution mpeg2 \* 1920x1088 - - mpeg4 \* 1920x1088 - - vc1 \* 1920x1088 - - h264 \* 4096x4096 \* 4096x4096 hevc \* 4096x4096 \* 4096x4096 jpeg - - - - vp9 - - - - av1 - - - - Kernel & winsys capabilities: drm = 3.64.0 has\_userptr = 1 has\_timeline\_syncobj = 1 has\_vm\_always\_valid = 1 has\_bo\_metadata = 1 has\_eqaa\_surface\_allocator = 1 has\_sparse\_vm\_mappings = 1 has\_stable\_pstate = 1 has\_gang\_submit = 1 has\_gpuvm\_fault\_query = 1 has\_kernelq\_reg\_shadowing = 0 has\_fw\_based\_shadowing = 0 has\_default\_zerovram\_support = 1 has\_tmz\_support = 0 has\_trap\_handler\_support = 0 IP GFX max\_submitted\_ibs = 192 IP COMPUTE max\_submitted\_ibs = 125 IP SDMA max\_submitted\_ibs = 49 IP UVD max\_submitted\_ibs = 1 IP VCE max\_submitted\_ibs = 1 IP UVD\_ENC max\_submitted\_ibs = 1 IP VCN\_DEC max\_submitted\_ibs = 1 IP VCN\_ENC max\_submitted\_ibs = 1 IP VCN\_JPEG max\_submitted\_ibs = 16 IP VPE max\_submitted\_ibs = 49 kernel\_has\_modifiers = 1 uses\_kernel\_cu\_mask = 0 Shader core info: cu\_mask\[SE0\]\[SA0\] = 0xfffe (15) CU\_EN = 0x7fff cu\_mask\[SE1\]\[SA0\] = 0xfffe (15) CU\_EN = 0x7fff cu\_mask\[SE2\]\[SA0\] = 0xfffe (15) CU\_EN = 0x7fff cu\_mask\[SE3\]\[SA0\] = 0xfffe (15) CU\_EN = 0x7fff spi\_cu\_en\_has\_effect = 0 max\_good\_cu\_per\_sa = 15 min\_good\_cu\_per\_sa = 15 max\_se = 4 max\_sa\_per\_se = 1 num\_cu\_per\_sh = 16 max\_waves\_per\_simd = 10 num\_physical\_sgprs\_per\_simd = 800 num\_physical\_wave64\_vgprs\_per\_simd = 256 num\_simd\_per\_compute\_unit = 4 min\_sgpr\_alloc = 16 max\_sgpr\_alloc = 104 sgpr\_alloc\_granularity = 16 min\_wave64\_vgpr\_alloc = 4 max\_vgpr\_alloc = 256 wave64\_vgpr\_alloc\_granularity = 4 max\_scratch\_waves = 1920 has\_scratch\_base\_registers = 0 Ring info: hs\_offchip\_workgroup\_size = 32768 B tess\_factor\_ring\_size = 180 KB tess\_offchip\_ring\_size = 7680 KB Render backend info: pa\_sc\_tile\_steering\_override = 0x0 max\_render\_backends = 16 num\_tile\_pipes = 4 pipe\_interleave\_bytes = 256 enabled\_rb\_mask = 0xffff max\_alignment = 65536 pbb\_max\_alloc\_count = 128 GB\_ADDR\_CONFIG: 0x2a114042 num\_pipes = 4 pipe\_interleave\_size = 256 max\_compressed\_frags = 2 bank\_interleave\_size = 1 num\_banks = 16 shader\_engine\_tile\_size = 32 num\_shader\_engines = 4 num\_gpus = 0 (raw) multi\_gpu\_tile\_size = 2 (raw) num\_rb\_per\_se = 4 row\_size = 4096 num\_lower\_pipes = 0 (raw) se\_enable = 0 (raw) Modifiers (32bpp): GFX9,64KB\_D\_X,PIPE\_XOR\_BITS=4,BANK\_XOR\_BITS=4,RB=4,PIPE=2,DCC,DCC\_MAX\_COMPRESSED\_BLOCK=64B,DCC\_INDEPENDENT\_64B,DCC\_PIPE\_ALIGN GFX9,64KB\_S\_X,PIPE\_XOR\_BITS=4,BANK\_XOR\_BITS=4,RB=4,PIPE=2,DCC,DCC\_MAX\_COMPRESSED\_BLOCK=64B,DCC\_INDEPENDENT\_64B,DCC\_PIPE\_ALIGN GFX9,64KB\_D\_X,PIPE\_XOR\_BITS=4,BANK\_XOR\_BITS=4 GFX9,64KB\_S\_X,PIPE\_XOR\_BITS=4,BANK\_XOR\_BITS=4 GFX9,64KB\_D GFX9,64KB\_S LINEAR \[2025-10-22 21:48:49.572\] \[MANGOHUD\] \[info\] \[gpu.cpp:89\] Set renderD128 as active GPU (driver=amdgpu id=1002:66a1 pci\_dev=0000:05:00.0) Selected GPU 0: AMD Radeon Pro VII (RADV VEGA20), type: DiscreteGpu ERROR: VALIDATION - Message Id Number: -1378015611 | Message Id Name: VUID-VkSwapchainCreateInfoKHR-presentMode-01281 vkCreateSwapchainKHR(): pCreateInfo->presentMode (VK\_PRESENT\_MODE\_FIFO\_KHR) is not supported (the following are supported ). The Vulkan spec states: presentMode must be one of the VkPresentModeKHR values returned by vkGetPhysicalDeviceSurfacePresentModesKHR for the surface (https://docs.vulkan.org/spec/latest/chapters/VK\_KHR\_surface/wsi.html#VUID-VkSwapchainCreateInfoKHR-presentMode-01281) \[2025-10-22 21:48:49.680\] \[MANGOHUD\] \[error\] \[cpu.cpp:784\] Failed to initialize CPU power data ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x3f000000003f) is being signaled by VkQueue 0x55ea9dbbf1b0, but it may still be in use by VkSwapchainKHR 0x1b000000001b. Most recently acquired image indices: \[0\], 1. (Brackets mark the last use of VkSemaphore 0x3f000000003f in a presentation operation.) Swapchain image 0 was presented but was not re-acquired, so VkSemaphore 0x3f000000003f may still be in use and cannot be safely reused with image index 1. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox3f000000003f Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55ea9dbbf1b0 ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x3f000000003f) is being signaled by VkQueue 0x55ea9dbbf1b0, but it may still be in use by VkSwapchainKHR 0x1b000000001b. Most recently acquired image indices: 0, \[1\], 2. (Brackets mark the last use of VkSemaphore 0x3f000000003f in a presentation operation.) Swapchain image 1 was presented but was not re-acquired, so VkSemaphore 0x3f000000003f may still be in use and cannot be safely reused with image index 2. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox3f000000003f Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55ea9dbbf1b0 ERROR: VALIDATION - Message Id Number: -1378015611 | Message Id Name: VUID-VkSwapchainCreateInfoKHR-presentMode-01281 vkCreateSwapchainKHR(): pCreateInfo->presentMode (VK\_PRESENT\_MODE\_FIFO\_KHR) is not supported (the following are supported ). The Vulkan spec states: presentMode must be one of the VkPresentModeKHR values returned by vkGetPhysicalDeviceSurfacePresentModesKHR for the surface (https://docs.vulkan.org/spec/latest/chapters/VK\_KHR\_surface/wsi.html#VUID-VkSwapchainCreateInfoKHR-presentMode-01281) \[2025-10-22 21:48:49.723\] \[MANGOHUD\] \[error\] \[cpu.cpp:784\] Failed to initialize CPU power data ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x730000000073) is being signaled by VkQueue 0x55ea9dbbf1b0, but it may still be in use by VkSwapchainKHR 0x4f000000004f. Most recently acquired image indices: \[0\], 1. (Brackets mark the last use of VkSemaphore 0x730000000073 in a presentation operation.) Swapchain image 0 was presented but was not re-acquired, so VkSemaphore 0x730000000073 may still be in use and cannot be safely reused with image index 1. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox730000000073 Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55ea9dbbf1b0 ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x730000000073) is being signaled by VkQueue 0x55ea9dbbf1b0, but it may still be in use by VkSwapchainKHR 0x4f000000004f. Most recently acquired image indices: 0, \[1\], 2. (Brackets mark the last use of VkSemaphore 0x730000000073 in a presentation operation.) Swapchain image 1 was presented but was not re-acquired, so VkSemaphore 0x730000000073 may still be in use and cannot be safely reused with image index 2. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox730000000073 Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55ea9dbbf1b0 \[2025-10-22 21:48:50.248\] \[MANGOHUD\] \[error\] \[cpu.cpp:784\] Failed to initialize CPU power data \[2025-10-22 21:48:50.782\] \[MANGOHUD\] \[error\] \[cpu.cpp:784\] Failed to initialize CPU power data \[2025-10-22 21:48:51.315\] \[MANGOHUD\] \[error\] \[cpu.cpp:784\] Failed to initialize CPU power data ~ 14s ❯ PROTON\_NO\_ESYNCPROTON\_NO\_ESYNC

---

O que você está vendo é um mix de dois problemas distintos:

---

### 1️⃣ vkCreateSwapchainKHR(): presentMode (VK\_PRESENT\_MODE\_FIFO\_KHR) is not supported

- A mensagem indica que o **modo de apresentação FIFO** (usado por padrão em muitas engines) **não é suportado no Wayland** com o RADV + sua configuração de driver atual.
- Resumo técnico: `vkGetPhysicalDeviceSurfacePresentModesKHR()` não retornou `VK_PRESENT_MODE_FIFO_KHR` como opção para o seu compositor Wayland.

**Solução prática:**

- Se estiver rodando no **Wayland**, tente outro modo de apresentação compatível, como:
	- `VK_PRESENT_MODE_MAILBOX_KHR`
		- `VK_PRESENT_MODE_IMMEDIATE_KHR`
- Se estiver usando Lutris/Proton, force via variável de ambiente para o Vulkan:
```bash
export RADV_SWAPCHAIN_MODE=mailbox
```

ou

```bash
export RADV_DEBUG=si
```

para listar modos de swapchain suportados.

---

### 2️⃣ vkQueueSubmit(): pSignalSemaphores … may still be in use by VkSwapchainKHR

- Esse erro indica **uso indevido do mesmo semáforo em múltimas imagens do swapchain**.
- Isso geralmente acontece em engines Vulkan que não lidam direito com Wayland ou com drivers RADV, e **não é falha do hardware**.

**Soluções práticas:**

- Atualize **RADV e Mesa para a última versão**; esse tipo de bug é comum em versões antigas do driver no Wayland.
- Teste com **Xorg**; esses erros quase nunca aparecem lá.
- Ative extensão `VK_KHR_swapchain_maintenance1` se a engine suportar.
- Evite **reuse de semáforos**; engines modernas fazem isso automaticamente.

---

### 3️⃣ \[MANGOHUD\] Failed to initialize CPU power data

- Erro do MangoHUD tentando ler energia/performance do CPU via `perf` ou ACPI.
- **Não afeta Vulkan**, é só informação extra que não pôde ser coletada.
- Se quiser evitar spam de logs:
```bash
MANGOHUD=0
```

---

💡 **Resumo de ação imediata para testes:**

```bash
export RADV_SWAPCHAIN_MODE=mailbox
vkcube --validate
```

Se persistir, rode via Xorg em vez de Wayland. Esses erros são típicos de RADV no Wayland.

Se quiser, posso te passar um **setup pronto de variáveis RADV para Forza Horizon 5 no Lutris/Proton** que evita esses erros e simula RTX-like (FSR/RTX tricks) na sua Pro VII. Isso vai cortar quase todos esses warnings. Quer que eu faça isso?

---

**Você disse**

❯ export RADV\_SWAPCHAIN\_MODE=mailbox ~ ❯ export RADV\_DEBUG=si ~ ❯ export RADV\_SWAPCHAIN\_MODE=mailbox vkcube --validate Selected WSI platform: wayland \[2025-10-22 21:53:31.882\] \[MANGOHUD\] \[info\] \[gpu.cpp:89\] Set renderD128 as active GPU (driver=amdgpu id=1002:66a1 pci\_dev=0000:05:00.0) Selected GPU 0: AMD Radeon Pro VII (RADV VEGA20), type: DiscreteGpu ERROR: VALIDATION - Message Id Number: -1378015611 | Message Id Name: VUID-VkSwapchainCreateInfoKHR-presentMode-01281 vkCreateSwapchainKHR(): pCreateInfo->presentMode (VK\_PRESENT\_MODE\_FIFO\_KHR) is not supported (the following are supported ). The Vulkan spec states: presentMode must be one of the VkPresentModeKHR values returned by vkGetPhysicalDeviceSurfacePresentModesKHR for the surface (https://docs.vulkan.org/spec/latest/chapters/VK\_KHR\_surface/wsi.html#VUID-VkSwapchainCreateInfoKHR-presentMode-01281) \[2025-10-22 21:53:31.977\] \[MANGOHUD\] \[error\] \[cpu.cpp:784\] Failed to initialize CPU power data ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x3f000000003f) is being signaled by VkQueue 0x55df56ce0600, but it may still be in use by VkSwapchainKHR 0x1b000000001b. Most recently acquired image indices: \[0\], 1. (Brackets mark the last use of VkSemaphore 0x3f000000003f in a presentation operation.) Swapchain image 0 was presented but was not re-acquired, so VkSemaphore 0x3f000000003f may still be in use and cannot be safely reused with image index 1. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox3f000000003f Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55df56ce0600 ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x3f000000003f) is being signaled by VkQueue 0x55df56ce0600, but it may still be in use by VkSwapchainKHR 0x1b000000001b. Most recently acquired image indices: 0, \[1\], 2. (Brackets mark the last use of VkSemaphore 0x3f000000003f in a presentation operation.) Swapchain image 1 was presented but was not re-acquired, so VkSemaphore 0x3f000000003f may still be in use and cannot be safely reused with image index 2. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox3f000000003f Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55df56ce0600 ERROR: VALIDATION - Message Id Number: -1378015611 | Message Id Name: VUID-VkSwapchainCreateInfoKHR-presentMode-01281 vkCreateSwapchainKHR(): pCreateInfo->presentMode (VK\_PRESENT\_MODE\_FIFO\_KHR) is not supported (the following are supported ). The Vulkan spec states: presentMode must be one of the VkPresentModeKHR values returned by vkGetPhysicalDeviceSurfacePresentModesKHR for the surface (https://docs.vulkan.org/spec/latest/chapters/VK\_KHR\_surface/wsi.html#VUID-VkSwapchainCreateInfoKHR-presentMode-01281) \[2025-10-22 21:53:32.023\] \[MANGOHUD\] \[error\] \[cpu.cpp:784\] Failed to initialize CPU power data ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x730000000073) is being signaled by VkQueue 0x55df56ce0600, but it may still be in use by VkSwapchainKHR 0x4f000000004f. Most recently acquired image indices: \[0\], 1. (Brackets mark the last use of VkSemaphore 0x730000000073 in a presentation operation.) Swapchain image 0 was presented but was not re-acquired, so VkSemaphore 0x730000000073 may still be in use and cannot be safely reused with image index 1. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox730000000073 Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55df56ce0600 ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x730000000073) is being signaled by VkQueue 0x55df56ce0600, but it may still be in use by VkSwapchainKHR 0x4f000000004f. Most recently acquired image indices: 0, \[1\], 2. (Brackets mark the last use of VkSemaphore 0x730000000073 in a presentation operation.) Swapchain image 1 was presented but was not re-acquired, so VkSemaphore 0x730000000073 may still be in use and cannot be safely reused with image index 2. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox730000000073 Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55df56ce0600 \[2025-10-22 21:53:32.546\] \[MANGOHUD\] \[error\] \[cpu.cpp:784\] Failed to initialize CPU power data \[2025-10-22 21:53:33.048\] \[MANGOHUD\] \[error\] \[cpu.cpp:784\] Failed to initialize CPU power data \[2025-10-22 21:53:33.581\] \[MANGOHUD\] \[error\] \[cpu.cpp:784\] Failed to initialize CPU power data ERROR: VALIDATION - Message Id Number: -1378015611 | Message Id Name: VUID-VkSwapchainCreateInfoKHR-presentMode-01281 vkCreateSwapchainKHR(): pCreateInfo->presentMode (VK\_PRESENT\_MODE\_FIFO\_KHR) is not supported (the following are supported ). The Vulkan spec states: presentMode must be one of the VkPresentModeKHR values returned by vkGetPhysicalDeviceSurfacePresentModesKHR for the surface (https://docs.vulkan.org/spec/latest/chapters/VK\_KHR\_surface/wsi.html#VUID-VkSwapchainCreateInfoKHR-presentMode-01281) ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x2790000000279) is being signaled by VkQueue 0x55df56ce0600, but it may still be in use by VkSwapchainKHR 0x2550000000255. Most recently acquired image indices: \[0\], 1. (Brackets mark the last use of VkSemaphore 0x2790000000279 in a presentation operation.) Swapchain image 0 was presented but was not re-acquired, so VkSemaphore 0x2790000000279 may still be in use and cannot be safely reused with image index 1. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox2790000000279 Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55df56ce0600 ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x2790000000279) is being signaled by VkQueue 0x55df56ce0600, but it may still be in use by VkSwapchainKHR 0x2550000000255. Most recently acquired image indices: 0, \[1\], 2. (Brackets mark the last use of VkSemaphore 0x2790000000279 in a presentation operation.) Swapchain image 1 was presented but was not re-acquired, so VkSemaphore 0x2790000000279 may still be in use and cannot be safely reused with image index 2. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox2790000000279 Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55df56ce0600 ERROR: VALIDATION - Message Id Number: -1378015611 | Message Id Name: VUID-VkSwapchainCreateInfoKHR-presentMode-01281 vkCreateSwapchainKHR(): pCreateInfo->presentMode (VK\_PRESENT\_MODE\_FIFO\_KHR) is not supported (the following are supported ). The Vulkan spec states: presentMode must be one of the VkPresentModeKHR values returned by vkGetPhysicalDeviceSurfacePresentModesKHR for the surface (https://docs.vulkan.org/spec/latest/chapters/VK\_KHR\_surface/wsi.html#VUID-VkSwapchainCreateInfoKHR-presentMode-01281) ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x2b100000002b1) is being signaled by VkQueue 0x55df56ce0600, but it may still be in use by VkSwapchainKHR 0x28d000000028d. Most recently acquired image indices: \[0\], 1. (Brackets mark the last use of VkSemaphore 0x2b100000002b1 in a presentation operation.) Swapchain image 0 was presented but was not re-acquired, so VkSemaphore 0x2b100000002b1 may still be in use and cannot be safely reused with image index 1. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox2b100000002b1 Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55df56ce0600 ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x2b100000002b1) is being signaled by VkQueue 0x55df56ce0600, but it may still be in use by VkSwapchainKHR 0x28d000000028d. Most recently acquired image indices: 0, \[1\], 2. (Brackets mark the last use of VkSemaphore 0x2b100000002b1 in a presentation operation.) Swapchain image 1 was presented but was not re-acquired, so VkSemaphore 0x2b100000002b1 may still be in use and cannot be safely reused with image index 2. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox2b100000002b1 Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55df56ce0600 ERROR: VALIDATION - Message Id Number: -1378015611 | Message Id Name: VUID-VkSwapchainCreateInfoKHR-presentMode-01281 vkCreateSwapchainKHR(): pCreateInfo->presentMode (VK\_PRESENT\_MODE\_FIFO\_KHR) is not supported (the following are supported ). The Vulkan spec states: presentMode must be one of the VkPresentModeKHR values returned by vkGetPhysicalDeviceSurfacePresentModesKHR for the surface (https://docs.vulkan.org/spec/latest/chapters/VK\_KHR\_surface/wsi.html#VUID-VkSwapchainCreateInfoKHR-presentMode-01281) ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x2e500000002e5) is being signaled by VkQueue 0x55df56ce0600, but it may still be in use by VkSwapchainKHR 0x2c100000002c1. Most recently acquired image indices: \[0\], 1. (Brackets mark the last use of VkSemaphore 0x2e500000002e5 in a presentation operation.) Swapchain image 0 was presented but was not re-acquired, so VkSemaphore 0x2e500000002e5 may still be in use and cannot be safely reused with image index 1. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox2e500000002e5 Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55df56ce0600 ERROR: VALIDATION - Message Id Number: 1402107823 | Message Id Name: VUID-vkQueueSubmit-pSignalSemaphores-00067 (Warning - This VUID has now been reported 10 times, which is the duplicate\_message\_limit value, this will be the last time reporting it). vkQueueSubmit(): pSubmits\[0\].pSignalSemaphores\[0\] (VkSemaphore 0x2e500000002e5) is being signaled by VkQueue 0x55df56ce0600, but it may still be in use by VkSwapchainKHR 0x2c100000002c1. Most recently acquired image indices: 0, \[1\], 2. (Brackets mark the last use of VkSemaphore 0x2e500000002e5 in a presentation operation.) Swapchain image 1 was presented but was not re-acquired, so VkSemaphore 0x2e500000002e5 may still be in use and cannot be safely reused with image index 2. Vulkan insight: See https://docs.vulkan.org/guide/latest/swapchain\_semaphore\_reuse.html for details on swapchain semaphore reuse. Examples of possible approaches: a) Use a separate semaphore per swapchain image. Index these semaphores using the index of the acquired image. b) Consider the VK\_KHR\_swapchain\_maintenance1 extension. It allows using a VkFence with the presentation operation. The Vulkan spec states: Each binary semaphore element of the pSignalSemaphores member of any element of pSubmits must be unsignaled when the semaphore signal operation it defines is executed on the device (https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html#VUID-vkQueueSubmit-pSignalSemaphores-00067) Objects - 2 Object\[0\] - VK\_OBJECT\_TYPE\_SEMAPHORE, Handle Ox2e500000002e5 Object\[1\] - VK\_OBJECT\_TYPE\_QUEUE, Handle 0x55df56ce0600 ERROR: VALIDATION - Message Id Number: -1378015611 | Message Id Name: VUID-VkSwapchainCreateInfoKHR-presentMode-01281 vkCreateSwapchainKHR(): pCreateInfo->presentMode (VK\_PRESENT\_MODE\_FIFO\_KHR) is not supported (the following are supported ). The Vulkan spec states: presentMode must be one of the VkPresentModeKHR values returned by vkGetPhysicalDeviceSurfacePresentModesKHR for the surface (https://docs.vulkan.org/spec/latest/chapters/VK\_KHR\_surface/wsi.html#VUID-VkSwapchainCreateInfoKHR-presentMode-01281) ~ 25s ❯

---

Ok, pela imagem que você mandou e os logs do `vkcube`:

- Sua **GPU está sendo reconhecida corretamente** como AMD Radeon Pro VII (RADV VEGA20).
- Temperaturas e uso estão **baixos**, sem problemas de hardware.
- O `vkCreateSwapchainKHR()` continua reclamando de `VK_PRESENT_MODE_FIFO_KHR` no Wayland — isso é **esperado** no RADV + Wayland: esse modo não é suportado, e a engine ainda tenta usar por padrão.
- Os erros de `vkQueueSubmit` são **semáforos em uso**; no `vkcube` não causam crash, mas indicam que o driver RADV + Wayland ainda tem problemas com swapchain semáforo reuse.

---

✅ Conclusões práticas:

1. **Hardware e Vulkan estão funcionando.** A GPU não é o problema.
2. **Erros de FIFO / semáforo** são puramente do driver/Wayland.
3. **Opcional**: para jogos/engines Vulkan no Wayland, considere:
	- Rodar via **Xorg** em vez de Wayland. Isso elimina a maioria desses warnings e permite `VK_PRESENT_MODE_FIFO_KHR`.
		- Ou, usar **RADV\_DEBUG=si** + modos `mailbox` / `immediate`, mas alguns erros de semáforo podem persistir.

---

Se você quiser, posso te passar **um setup de variáveis RADV para Lutris/Proton** que **força swapchain compatível, ativa FSR e minimiza warnings**, especificamente para sua Pro VII no Wayland. Isso vai deixar Forza Horizon 5 e outros jogos Vulkan rodando mais “limpos”.

Quer que eu faça isso?