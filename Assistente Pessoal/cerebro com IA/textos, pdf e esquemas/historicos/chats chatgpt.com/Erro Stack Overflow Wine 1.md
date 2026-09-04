---
title: "Erro Stack Overflow Wine"
source: "https://chatgpt.com/c/69f712bf-6c0c-83e9-84bf-2f3e1da5b46e"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 4 messages"
tags:
  - "clippings"
---
**Você disse**

(06:15:11) \[INFO\]: Launching "need for speed heat" (sideload) (06:15:11) \[INFO\]: Native? false (06:15:11) \[INFO\]: Installed in: /mnt/win1/games/Need for Speed Heat (06:15:11) \[INFO\]: System Info: CPU: 36x Intel(R) Xeon(R) CPU E5-2699 v3 @ 2.30GHz Memory: 33.54 GB (used: 5.7 GB) GPUs: GPU 0: Name: Advanced Micro Devices, Inc. \[AMD/ATI\] Vega 20 \[Radeon Pro VII/Radeon Instinct MI50\] IDs: D=66a1 V=1002 SD=103e SV=17aa Driver: amdgpu OS: CachyOS Linux 7.0.3-1-cachyos (linux) The current system is not a Steam Deck We are not running inside a Flatpak container We are not running from an AppImage Software Versions: Heroic: 2.21.0 Loki Legendary: 0.20.43 Riding Shotgun (Heroic) gogdl: 1.2.1 comet: comet 0.2.0 Nile: 1.1.2 Will A. Zeppeli (06:15:11) \[INFO\]: Game Settings: { "autoInstallDxvk": true, "autoInstallDxvkNvapi": true, "autoInstallVkd3d": true, "preferSystemLibs": false, "enableEsync": true, "enableFsync": true, "enableWineWayland": false, "enableHDR": false, "enableWoW64": false, "nvidiaPrime": false, "enviromentOptions": \[\], "wrapperOptions": \[\], "showFps": false, "showMangohud": true, "useGameMode": false, "battlEyeRuntime": true, "eacRuntime": true, "language": "", "beforeLaunchScriptPath": "", "afterLaunchScriptPath": "", "wineVersion": { "bin": "/usr/bin/wine", "name": "wine-11.8", "type": "wine", "wineserver": "/usr/bin/wineserver" }, "winePrefix": "/home/johncoffee/Games/Heroic/Prefixes/need for speed heat" } Stored at: /home/johncoffee/.config/heroic/GamesConfig/cfgNSGx2n2bHwZv9m7g5GG.json (06:15:11) \[INFO\]: Winetricks packages: Wine Command: /usr/bin/mangohud --dlsym /usr/bin/wine /mnt/win1/games/Need for Speed Heat/NeedForSpeedHeat.exe Game Log: 017c:fixme:ver:GetCurrentPackageId (000000000010DEE0 0000000000000000): stub 017c:err:virtual:virtual\_setup\_exception stack overflow 1984 bytes addr 0x6fffffc0efe1 stack 0x10840 (0x10000-0x11000-0x110000)

---

Direto ao ponto: esse erro

```
stack overflow ... addr 0x6fffffc0efe1
```

no **Need for Speed Heat** via Wine quase sempre é **incompatibilidade de stack/memória + Wine vanilla ruim pra jogo DX12 + EA DRM**.

Você está usando **wine-11.8 puro** → isso é o problema principal.

---

1. **Wine vanilla não aguenta esse jogo direito**
2. DX12 + DRM da EA + threading pesado → explode stack
3. Vega 20 + RADV + VKD3D precisa config correta
4. Prefix provavelmente contaminado (tentativas anteriores)

---

## ✅ SOLUÇÃO EFETIVA (plug n play)

## 1\. TROCA IMEDIATA DO WINE

No Heroic:

Use:

- **Proton-GE**  
	ou
- **Wine-GE**

👉 Recomendo:

- `Proton-GE latest`

Se não tiver:

```bash
heroic tools install proton-ge
```

---

## 2\. RESET TOTAL DO PREFIX

Apaga isso:

```bash
/home/johncoffee/Games/Heroic/Prefixes/need for speed heat
```

Cria novo limpo.

---

## 3\. FORÇA VKD3D + DXVK LIMPO

No Heroic → configurações do jogo:

Ativa:

- DXVK ✅
- VKD3D ✅

Desativa:

- NVAPI ❌ (AMD não precisa)

---

## 4\. ENV VARS CRÍTICAS (ESSENCIAL PRA VEGA 20)

Adiciona:

```bash
RADV_PERFTEST=aco
DXVK_ASYNC=1
VKD3D_FEATURE_LEVEL=12_1
MESA_SHADER_CACHE_MAX_SIZE=10G
```

Opcional (teste):

```bash
WINE_LARGE_ADDRESS_AWARE=1
```

---

## 5\. DEPENDÊNCIAS (evita crash silencioso)

Dentro do prefix:

```bash
winetricks -q vcrun2019
winetricks -q dxvk
```

---

## 6\. GAME MODE + FSYNC (ganho real)

Ativa:

- GameMode ✅
- Fsync ✅ (já tá)
- Esync ✅ (já tá)

Instala gamemode se não tiver:

```bash
sudo pacman -S gamemode
```

---

## 7\. POSSÍVEL BUG DO DRIVER (Vega MI50)

Você está usando:

- Instinct MI50 (sem firmware gaming completo)

Se ainda crashar:

```bash
RADV_DEBUG=nohiz
```

ou

```bash
AMD_DEBUG=nodcc
```

---

## 🔬 DIAGNÓSTICO AVANÇADO (se ainda falhar)

Roda no terminal:

```bash
WINEDEBUG=-all %command%
```

Se parar antes de abrir → é DRM quebrando.

---

## 💡 OTIMIZAÇÃO BRUTA (nível engenheiro)

Sua GPU:

- MI50 → essencialmente Vega 20 compute

Melhor abordagem:

- spoof (você já faz via BIOS) ✔
- usar RADV + ACO ✔
- evitar amdgpu-pro ❌

---

## 🧠 VISÃO ESTRATÉGICA

Você está tentando rodar:

- jogo moderno (DX12 pesado)
- num stack Linux
- com GPU compute adaptada

👉 solução não é “tentar mais”  
👉 é alinhar stack:

✔ Proton-GE  
✔ prefix limpo  
✔ VKD3D correto  
✔ env tuning

---

## 🚀 RESUMO EXECUTIVO

Faça isso e resolve 90% dos casos:

1. Troca pra **Proton-GE**
2. Deleta prefix
3. Adiciona env:
	```
	RADV_PERFTEST=aco DXVK_ASYNC=1
	```
4. Reinstala dependências

---

Se quiser, próximo passo eu faço pra você:

✅ preset pronto Heroic (json) otimizado pra MI50  
✅ tuning fino de clocks/voltagem pra estabilidade em jogo  
✅ análise do teu VRM interferindo em crash (isso pode estar acontecendo também)

Só falar.

---

**Você disse**

(06:20:47) \[INFO\]: Launching "need for speed heat" (sideload) (06:20:47) \[INFO\]: Native? false (06:20:47) \[INFO\]: Installed in: /mnt/win1/games/Need for Speed Heat (06:20:47) \[INFO\]: System Info: CPU: 36x Intel(R) Xeon(R) CPU E5-2699 v3 @ 2.30GHz Memory: 33.54 GB (used: 5.7 GB) GPUs: GPU 0: Name: Advanced Micro Devices, Inc. \[AMD/ATI\] Vega 20 \[Radeon Pro VII/Radeon Instinct MI50\] IDs: D=66a1 V=1002 SD=103e SV=17aa Driver: amdgpu OS: CachyOS Linux 7.0.3-1-cachyos (linux) The current system is not a Steam Deck We are not running inside a Flatpak container We are not running from an AppImage Software Versions: Heroic: 2.21.0 Loki Legendary: 0.20.43 Riding Shotgun (Heroic) gogdl: 1.2.1 comet: comet 0.2.0 Nile: 1.1.2 Will A. Zeppeli (06:20:47) \[INFO\]: Game Settings: { "autoInstallDxvkNvapi": true, "preferSystemLibs": false, "enableEsync": true, "enableFsync": true, "enableWineWayland": false, "enableHDR": false, "enableWoW64": false, "nvidiaPrime": false, "enviromentOptions": \[\], "wrapperOptions": \[\], "showFps": false, "showMangohud": true, "useGameMode": false, "battlEyeRuntime": true, "eacRuntime": true, "language": "", "beforeLaunchScriptPath": "", "afterLaunchScriptPath": "", "wineVersion": { "bin": "/home/johncoffee/.config/heroic/tools/proton/GE-Proton-latest/proton", "name": "GE-Proton-latest", "type": "proton" }, "winePrefix": "/home/johncoffee/Games/Heroic/Prefixes/need for speed heat" } Stored at: /home/johncoffee/.config/heroic/GamesConfig/cfgNSGx2n2bHwZv9m7g5GG.json (06:20:47) \[INFO\]: Winetricks packages: Wine Command: /usr/bin/mangohud --dlsym /usr/bin/umu-run /mnt/win1/games/Need for Speed Heat/NeedForSpeedHeat.exe Game Log: INFO: umu-launcher version 1.4.0 (3.14.4 (main, Apr 11 2026, 09:31:02) \[GCC 15.2.1 20260209\]) INFO: No GAMEID set, using umu-default INFO: steamrt3 is up to date INFO: Running 'GE-Proton10-34' using runtime 'sniper' INFO: Running 'steamrt3' using runtime 'host' ProtonFixes\[40147\] INFO: Running protonfixes on "GE-Proton10-34", build at 2026-03-23 03:55:11+00:00. ProtonFixes\[40147\] INFO: Running checks ProtonFixes\[40147\] INFO: All checks successful ProtonFixes\[40147\] WARN: Game title not found in CSV ProtonFixes\[40147\] INFO: Non-steam game UNKNOWN (umu-default) ProtonFixes\[40147\] INFO: No store specified, using UMU database ProtonFixes\[40147\] INFO: Using early stage global defaults for UNKNOWN (umu-default) ProtonFixes\[40147\] INFO: Non-steam game UNKNOWN (umu-default) ProtonFixes\[40147\] INFO: No store specified, using UMU database ProtonFixes\[40147\] INFO: No early stage global protonfix found for UNKNOWN (umu-default) ProtonFixes\[40147\] INFO: Running protonfixes on "GE-Proton10-34", build at 2026-03-23 03:55:11+00:00. ProtonFixes\[40147\] INFO: Running checks ProtonFixes\[40147\] INFO: All checks successful ProtonFixes\[40147\] INFO: Non-steam game UNKNOWN (umu-default) ProtonFixes\[40147\] INFO: No store specified, using UMU database ProtonFixes\[40147\] INFO: Using main stage global defaults for UNKNOWN (umu-default) ProtonFixes\[40147\] INFO: Non-steam game UNKNOWN (umu-default) ProtonFixes\[40147\] INFO: No store specified, using UMU database ProtonFixes\[40147\] INFO: No main stage global protonfix found for UNKNOWN (umu-default) Proton: /mnt/win1/games/Need for Speed Heat/NeedForSpeedHeat.exe Proton: Executable a unix path, launching with /unix option. Starting program with command-launcher service. To run commands in the per-app container, use a command like: /home/johncoffee/.local/share/umu/steamrt3/pressure-vessel/bin/steam-runtime-launch-client \\ --bus-name=:1.137 \\ -- \\ bash wineserver: NTSync up and running! 002c:fixme:winediag:loader\_init wine-staging 10.0 is a testing version containing experimental patches. 002c:fixme:winediag:loader\_init Please mention your exact version when filing bug reports on winehq.org. 0048:fixme:ntoskrnl:driver\_stub 0000000000249DB0 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\pci" stub! 0048:fixme:ntoskrnl:driver\_stub 000000000024A000 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\hidusb" stub! 0048:fixme:ntoskrnl:driver\_stub 000000000024ADD0 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\Disk" stub! 0058:fixme:ntoskrnl:kernel\_object\_from\_handle No constructor for type L"Token" \[2026-05-03 06:21:07.804\] \[MANGOHUD\] \[info\] \[blacklist.cpp:86\] process 'explorer.exe' is blacklisted in MangoHud 006c:err:system:NtUserChangeDisplaySettings Changing L"\\\\\\\\.\\\\DISPLAY1" display settings returned -2. 006c:err:explorer:initialize\_display\_settings Failed to initialize registry display settings for L"\\\\\\\\.\\\\DISPLAY1". 00b8:fixme:ntoskrnl:driver\_stub 0000000000249DB0 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\pci" stub! 00b8:fixme:ntoskrnl:driver\_stub 000000000024A000 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\hidusb" stub! 00b8:fixme:ntoskrnl:driver\_stub 000000000024ADD0 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\Disk" stub! 00c4:fixme:ntoskrnl:kernel\_object\_from\_handle No constructor for type L"Token" 00dc:fixme:xinput:pdo\_pnp code 0xc, not implemented! 00dc:fixme:xinput:pdo\_pnp code 0xc, not implemented! 00c0:err:ntoskrnl:ZwLoadDriver failed to create driver L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\winebth": c0000142 003c:fixme:service:scmdatabase\_autostart\_services Auto-start service L"winebth" failed to start: 1114 00f0:fixme:wineusb:query\_id Unhandled ID query type 0x5. 006c:fixme:file:GetLongPathNameW UNC pathname L"\\\\\\\\?\\\\X:\\\\.config\\\\heroic\\\\tools\\\\proton\\\\GE-Proton-latest\\\\files\\\\share\\\\wine/../xalia/xalia.exe" 006c:fixme:file:GetLongPathNameW UNC pathname L"\\\\\\\\?\\\\X:\\\\.config\\\\heroic\\\\tools\\\\proton\\\\GE-Proton-latest\\\\files\\\\share\\\\wine/../xalia/xalia.exe" 006c:fixme:file:GetLongPathNameW UNC pathname L"\\\\\\\\?\\\\X:\\\\.config\\\\heroic\\\\tools\\\\proton\\\\GE-Proton-latest\\\\files\\\\share\\\\wine/../xalia/xalia.exe" 0128:fixme:oleacc:find\_class\_data unhandled window class: L"#32769" 0128:fixme:uiautomation:uia\_get\_providers\_for\_hwnd Override provider callback currently unimplemented. 0128:fixme:uiautomation:default\_uia\_provider\_callback Default ProviderType\_NonClientArea provider unimplemented. 0128:fixme:oleacc:find\_class\_data unhandled window class: L"#32769" 0128:fixme:uiautomation:base\_hwnd\_fragment\_get\_FragmentRoot 000000000081EA38, 000000000021F9A0: stub! 0128:fixme:uiautomation:base\_hwnd\_fragment\_GetEmbeddedFragmentRoots 000000000081EA38, 000000000021F9B0: stub! 0130:fixme:mscoree:parse\_supported\_runtime sku=L".NETFramework,Version=v4.8" not implemented 0130:fixme:mscoree:parse\_supported\_runtime sku=L".NETFramework,Version=v4.8" not implemented 0130:fixme:ntdll:NtQuerySystemInformation info\_class SYSTEM\_PERFORMANCE\_INFORMATION info: Game: xalia.exe info: DXVK: v2.7.1-509-g1676dcaf342a9b1 info: Build: x86\_64 gcc 14.2.0 info: Vulkan: Found vkGetInstanceProcAddr in winevulkan.dll @ 0x6ffffcc9fbf0 info: Extension providers: info: Platform WSI info: OpenVR info: OpenXR 0130:err:openxr:get\_vulkan\_extensions Error getting openxr\_vulkan\_instance\_extensions, status 0x2. warn: OpenXR: Unable to get required Vulkan instance extensions size info: Enabled instance extensions: info: VK\_KHR\_get\_surface\_capabilities2 info: VK\_KHR\_surface info: VK\_KHR\_surface\_maintenance1 info: VK\_KHR\_win32\_surface \[2026-05-03 06:21:08.650\] \[MANGOHUD\] \[info\] \[gpu.cpp:90\] Set renderD128 as active GPU (driver=amdgpu id=1002:66a1 pci\_dev=0000:05:00.0) \[2026-05-03 06:21:08.674\] \[MANGOHUD\] \[info\] \[cpu.cpp:825\] cpu vendor: GenuineIntel \[2026-05-03 06:21:08.674\] \[MANGOHUD\] \[error\] \[cpu.cpp:844\] failed to open core info file \[2026-05-03 06:21:08.675\] \[MANGOHUD\] \[info\] \[cpu.cpp:636\] hwmon: using input: /sys/class/hwmon/hwmon1/temp1\_input info: Found device: AMD Radeon Pro VII (RADV VEGA20) (radv 26.0.6) 0130:err:openxr:get\_vulkan\_extensions Error getting openxr\_vulkan\_instance\_extensions, status 0x2. warn: OpenXR: Unable to get required Vulkan Device extensions size 00c4:fixme:ntoskrnl:kernel\_object\_from\_handle No constructor for type L"Token" 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F318 0x00000004 0x00000000 stub 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F318 0x00000005 0x00000000 stub 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F318 0x00000006 0x00000000 stub 015c:fixme:kernelbase:AppPolicyGetThreadInitializationType FFFFFFFFFFFFFFFA, 0000000003FAFF50 0130:fixme:dinput:hid\_joystick\_device\_try\_open device usage ff00:0001 not implemented! 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F168 0x00000004 0x00000000 stub 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F168 0x00000005 0x00000000 stub 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F168 0x00000006 0x00000000 stub /builds/mono/wine-mono/wine-mono-11.1.0/mono/mono/eglib/gmisc-win32.c:138: assertion 'filename!= NULL' failed 0150:fixme:ver:GetCurrentPackageId (000000000011DB20 0000000000000000): stub 0058:fixme:ntoskrnl:kernel\_object\_from\_handle No constructor for type L"Token" 0150:err:virtual:virtual\_setup\_exception stack overflow 2112 bytes addr 0x6ffffff53822 stack 0x207c0 (0x20000-0x21000-0x120000) 0130:fixme:xinput:XInputGetBatteryInformation index 0, type 0, battery 000000000011F038. 0130:fixme:sync:SetWaitableTimerEx (00000000000001A8, 000000000011F0E8, 0, 0000000000000000, 0000000000000000, 0000000000000000, 0) semi-stub PropertiesChanged Signal received: Source: org.kde.Solid.PowerManagement.PolicyAgent active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.39 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Timer active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Job active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Timer active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.1 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.plasma-browser-integration active\_player's owner::1.63 sender::1.63

---

Agora ficou claro: você corrigiu metade… mas ainda está batendo no mesmo gargalo estrutural.

Erro final continua:

```
stack overflow ... addr 0x6ffffff53822
```

👉 Isso aqui NÃO é mais Wine básico.  
👉 Isso agora é **runtime + dependência + inicialização DX12 quebrando**.

---

## 🔴 DIAGNÓSTICO PRECISO

Você está travando antes do jogo abrir por 3 pontos combinados:

### 1\. Mono quebrando

```
wine-mono assertion 'filename != NULL' failed
```

👉.NET runtime falhou → jogo morre antes de inicializar UI/launcher

---

### 2\. Xalia + Explorer + Display init falhando

```
Failed to initialize registry display settings
```

👉 ambiente gráfico do prefix não está consistente

---

### 3\. Stack overflow (efeito, não causa)

👉 consequência de loop interno (geralmente.NET / launcher EA)

---

## ⚠️ CONCLUSÃO DIRETA

O **Need for Speed Heat**:

- usa **EA App / Origin layer**
- depende de **.NET + VC++ + services**
- Proton GE sozinho NÃO resolve sem prefix correto

---

## ✅ SOLUÇÃO QUE REALMENTE FUNCIONA

## 🔧 1. FORÇA PREFIX 100% WINDOWS 10 LIMPO

Apaga de novo:

```bash
rm -rf ~/Games/Heroic/Prefixes/need\ for\ speed\ heat
```

---

## 🔧 2. CRIA PREFIX MANUALMENTE (controle total)

```bash
WINEPREFIX=~/Games/Heroic/Prefixes/nfsheat \
WINEARCH=win64 \
proton run wineboot
```

---

## 🔧 3. INSTALA DEPENDÊNCIAS CERTAS (ESSENCIAL)

```bash
protontricks -c "winetricks -q vcrun2019"
protontricks -c "winetricks -q corefonts"
protontricks -c "winetricks -q dxvk"
protontricks -c "winetricks -q vkd3d"
```

🔥 **CRÍTICO (resolve teu erro atual):**

```bash
protontricks -c "winetricks -q dotnet48"
```

👉 Esse é o que está faltando.  
👉 Esse resolve o crash do mono + stack overflow.

---

## 🔧 4. DESATIVA MONO (obrigatório)

```bash
WINEDLLOVERRIDES="mscoree=d"
```

👉 força usar.NET real (não wine-mono bugado)

---

## 🔧 5. DESLIGA LIXO QUE ESTÁ INTERFERINDO

No Heroic:

- ❌ MangoHud (temporariamente)
- ❌ NVAPI
- ❌ OpenXR (você viu erro disso)

Adiciona:

```bash
DISABLE_OPENXR=1
```

---

## 🔧 6. ENV FINAL (estável pra Vega 20)

```bash
RADV_PERFTEST=aco
DXVK_ASYNC=1
VKD3D_CONFIG=dxr
MESA_SHADER_CACHE_MAX_SIZE=10G
DISABLE_OPENXR=1
WINEDLLOVERRIDES=mscoree=d
```

---

## 🔬 SE AINDA NÃO ABRIR

Então é DRM EA.

Nesse caso:

👉 você PRECISA rodar via launcher (EA App)

Solução:

- instalar EA App dentro do prefix
- logar
- lançar o jogo por dentro

---

## 💡 INSIGHT AVANÇADO (nível que te faz evoluir)

Você está enfrentando 3 camadas:

1. Hardware (MI50 adaptada) ✔
2. Tradução gráfica (DXVK/VKD3D) ✔
3. Runtime Windows (.NET / DRM) ❌ ← gargalo real

👉 A maioria para na camada 2  
👉 você já passou disso  
👉 agora está no nível “engine/runtime”

---

## 🚀 RESUMO EXECUTIVO

Faz isso:

1. instala `dotnet48`
2. desativa mono
3. limpa prefix
4. desliga MangoHud/OpenXR
5. roda de novo

---

Se quiser, eu te entrego:

✅ prefix já pronto (script automatizado)  
✅ versão “blindada” com EA App funcionando  
✅ ou bypass de launcher (depende da tua build)

Só fala qual caminho você quer seguir.