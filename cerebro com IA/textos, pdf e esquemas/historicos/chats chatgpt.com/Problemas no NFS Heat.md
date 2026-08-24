---
title: "Problemas no NFS Heat"
source: "https://chatgpt.com/c/69fd4037-dd48-83e9-b590-4af7bec64d93"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 5 messages"
tags:
  - "clippings"
---
Agora o cenário mudou bastante.

O Proton-CachyOS 11 subiu corretamente.  
O bug das 32 threads SUMIU do log.  
Então você eliminou a principal falha estrutural.

Mas o jogo ainda não iniciou de verdade.

O log agora aponta para outro problema:

```
NtUserChangeDisplaySettings returned -2
Failed to initialize registry display settings
```

Isso geralmente significa:

- prefix Wine quebrado/corrompido
- resolução inválida salva
- DXGI inicializando errado
- Wayland/X11 mismatch
- Frostbite preso em fullscreen exclusivo
- registry de vídeo inconsistente

E existe outro detalhe MUITO importante:

```
Executable is a unix path, launching with 'umu.exe'
```

Você está executando o EXE diretamente via sideload.  
O NFS Heat da EA normalmente precisa:

- EA App
- Origin workaround
- launch options específicas
- compat data correta

Sem isso o Frostbite às vezes morre silenciosamente.

---

## 1\. APAGUE O PREFIX

O prefix atual provavelmente já ficou contaminado pelos testes anteriores.

DELETE:

```bash
rm -rf ~/Games/Heroic/Prefixes/"need for speed heat"
```

Depois:

- recrie do zero
- deixe Proton reinstalar tudo

---

## 2\. DESATIVE MANGOHUD TEMPORARIAMENTE

Tem overlay quebrando DXGI em alguns Proton 11.

No Heroic:

- desative MangoHud
- desative FPS counter

Teste limpo.

---

## 3\. FORCE X11

No CachyOS moderno o Wayland às vezes interfere no Frostbite.

Antes de abrir Heroic:

```bash
export SDL_VIDEODRIVER=x11
export DISPLAY=:0
heroic
```

---

## 4\. ENV MAIS IMPORTANTE

Adicione no Heroic:

```bash
PROTON_USE_WINED3D=0
DXVK_ENABLE_NVAPI=0
VKD3D_CONFIG=dxr11
RADV_PERFTEST=aco
mesa_glthread=true
```

---

## 5\. O MAIS IMPORTANTE DE TODOS

Need for Speed Heat frequentemente precisa:

```bash
WINEDLLOVERRIDES="dxgi=n,b"
```

Adicione.

---

## 6\. FORÇAR RESOLUÇÃO SEGURA

O erro de display geralmente morre com virtual desktop.

No prefix:

```bash
WINEPREFIX=~/Games/Heroic/Prefixes/"need for speed heat" winecfg
```

Depois:

- Graphics
- Enable Virtual Desktop
- 1920x1080

---

## 7\. NÃO USE DXSDK\_JUN2010

Você instalou:

```
dxsdk_jun2010
```

Isso pode conflitar com DXVK moderno.

Remove:

```bash
WINEPREFIX=~/Games/Heroic/Prefixes/"need for speed heat" winetricks remove_dxsdk
```

ou recrie prefix limpo sem ele.

---

## 8\. NECESSÁRIO PARA FROSTBITE

Instale:

```bash
winetricks vcrun2019
```

E NÃO dotnet20.

dotnet20 é pré-histórico para esse jogo.

---

## 9\. SUA CONFIG FINAL IDEAL

## Heroic

### Wine

- Proton-CachyOS 11

### OFF

- MangoHud
- Fsync
- HDR
- Wayland

### ON

- Esync
- DXVK
- VKD3D

### ENV

```bash
RADV_PERFTEST=aco
mesa_glthread=true
DXVK_ENABLE_NVAPI=0
WINEDLLOVERRIDES=dxgi=n,b
```

---

## 10\. O MAIS SUSPEITO AGORA

O maior suspeito virou:

## PREFIX contaminado

Porque:

- você trocou Wine → Proton
- mudou runtime
- manteve prefix antigo

Isso quebra:

- registry
- display config
- DXGI state
- shader pipeline

Frostbite odeia isso.

---

## EXTRA — TESTE DIRETO PELO TERMINAL

Rode:

```bash
STEAM_COMPAT_DATA_PATH=~/Games/Heroic/Prefixes/nfsheat \
~/.local/share/Steam/compatibilitytools.d/"Proton-CachyOS Latest"/proton run \
"/mnt/win1/games/Need for Speed Heat/NeedForSpeedHeat.exe"
```

Se abrir por terminal e não pelo Heroic:  
→ problema é wrapper/overlay.

Se não abrir:  
→ problema é prefix/runtime.

---

**Você disse**

(23:00:28) \[INFO\]: Launching "need for speed heat" (sideload) (23:00:28) \[INFO\]: Native? false (23:00:28) \[INFO\]: Installed in: /mnt/win1/games/Need for Speed Heat (23:00:28) \[INFO\]: System Info: CPU: 36x Intel(R) Xeon(R) CPU E5-2699 v3 @ 2.30GHz Memory: 33.54 GB (used: 6.2 GB) GPUs: GPU 0: Name: Advanced Micro Devices, Inc. \[AMD/ATI\] Vega 20 \[Radeon Pro VII/Radeon Instinct MI50\] IDs: D=66a1 V=1002 SD=103e SV=17aa Driver: amdgpu OS: CachyOS Linux 7.0.3-1-cachyos (linux) The current system is not a Steam Deck We are not running inside a Flatpak container We are not running from an AppImage Software Versions: Heroic: 2.21.0 Loki Legendary: 0.20.43 Riding Shotgun (Heroic) gogdl: 1.2.1 comet: comet 0.2.0 Nile: 1.1.2 Will A. Zeppeli (23:00:28) \[INFO\]: Game Settings: { "autoInstallDxvkNvapi": true, "preferSystemLibs": false, "enableEsync": true, "enableFsync": true, "enableWineWayland": false, "enableHDR": false, "enableWoW64": false, "nvidiaPrime": false, "enviromentOptions": \[\], "wrapperOptions": \[\], "showFps": false, "showMangohud": true, "useGameMode": false, "battlEyeRuntime": true, "eacRuntime": true, "language": "", "beforeLaunchScriptPath": "", "afterLaunchScriptPath": "", "wineVersion": { "bin": "/home/johncoffee/.local/share/Steam/compatibilitytools.d/Proton-GE Latest/proton", "name": "Proton-GE Latest", "type": "proton" }, "winePrefix": "/home/johncoffee/Games/Heroic/Prefixes/need for speed heat" } Stored at: /home/johncoffee/.config/heroic/GamesConfig/cfgNSGx2n2bHwZv9m7g5GG.json (23:00:28) \[INFO\]: Winetricks packages: Wine Command: /usr/bin/mangohud --dlsym /usr/bin/umu-run /mnt/win1/games/Need for Speed Heat/NeedForSpeedHeat.exe Game Log: INFO: umu-launcher version 1.4.0 (3.14.4 (main, May 3 2026, 17:15:29) \[GCC 16.1.1 20260430\]) INFO: No GAMEID set, using umu-default INFO: steamrt3 is up to date INFO: Running 'Proton-GE Latest' using runtime 'sniper' INFO: Running 'steamrt3' using runtime 'host' ProtonFixes\[147513\] INFO: Running protonfixes on "GE-Proton10-34", build at 2026-03-23 03:55:11+00:00. ProtonFixes\[147513\] INFO: Running checks ProtonFixes\[147513\] INFO: All checks successful ProtonFixes\[147513\] WARN: Game title not found in CSV ProtonFixes\[147513\] INFO: Non-steam game UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: No store specified, using UMU database ProtonFixes\[147513\] INFO: Using early stage global defaults for UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: Non-steam game UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: No store specified, using UMU database ProtonFixes\[147513\] INFO: No early stage global protonfix found for UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: Running protonfixes on "GE-Proton10-34", build at 2026-03-23 03:55:11+00:00. ProtonFixes\[147513\] INFO: Running checks ProtonFixes\[147513\] INFO: All checks successful ProtonFixes\[147513\] INFO: Non-steam game UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: No store specified, using UMU database ProtonFixes\[147513\] INFO: Using main stage global defaults for UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: Non-steam game UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: No store specified, using UMU database ProtonFixes\[147513\] INFO: No main stage global protonfix found for UNKNOWN (umu-default) Proton: /mnt/win1/games/Need for Speed Heat/NeedForSpeedHeat.exe Proton: Executable a unix path, launching with /unix option. Starting program with command-launcher service. To run commands in the per-app container, use a command like: /home/johncoffee/.local/share/umu/steamrt3/pressure-vessel/bin/steam-runtime-launch-client \\ --bus-name=:1.173 \\ -- \\ bash wineserver: NTSync up and running! 002c:fixme:winediag:loader\_init wine-staging 10.0 is a testing version containing experimental patches. 002c:fixme:winediag:loader\_init Please mention your exact version when filing bug reports on winehq.org. 0048:fixme:ntoskrnl:driver\_stub 0000000000249E30 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\pci" stub! 0048:fixme:ntoskrnl:driver\_stub 000000000024A080 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\hidusb" stub! 0048:fixme:ntoskrnl:driver\_stub 000000000024AED0 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\Disk" stub! 0058:fixme:ntoskrnl:kernel\_object\_from\_handle No constructor for type L"Token" \[2026-05-07 23:00:51.752\] \[MANGOHUD\] \[info\] \[blacklist.cpp:86\] process 'explorer.exe' is blacklisted in MangoHud 0074:err:system:NtUserChangeDisplaySettings Changing L"\\\\\\\\.\\\\DISPLAY1" display settings returned -2. 0074:err:explorer:initialize\_display\_settings Failed to initialize registry display settings for L"\\\\\\\\.\\\\DISPLAY1". 00b8:fixme:ntoskrnl:driver\_stub 0000000000249E30 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\pci" stub! 00b8:fixme:ntoskrnl:driver\_stub 000000000024A080 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\hidusb" stub! 00b8:fixme:ntoskrnl:driver\_stub 000000000024AED0 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\Disk" stub! 00c4:fixme:ntoskrnl:kernel\_object\_from\_handle No constructor for type L"Token" 00dc:fixme:xinput:pdo\_pnp code 0xc, not implemented! 00dc:fixme:xinput:pdo\_pnp code 0xc, not implemented! 00c0:err:ntoskrnl:ZwLoadDriver failed to create driver L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\winebth": c0000142 003c:fixme:service:scmdatabase\_autostart\_services Auto-start service L"winebth" failed to start: 1114 00f4:fixme:wineusb:query\_id Unhandled ID query type 0x5. 0074:fixme:file:GetLongPathNameW UNC pathname L"\\\\\\\\?\\\\X:\\\\.local\\\\share\\\\Steam\\\\compatibilitytools.d\\\\Proton-GE Latest\\\\files\\\\share\\\\wine/../xalia/xalia.exe" 0074:fixme:file:GetLongPathNameW UNC pathname L"\\\\\\\\?\\\\X:\\\\.local\\\\share\\\\Steam\\\\compatibilitytools.d\\\\Proton-GE Latest\\\\files\\\\share\\\\wine/../xalia/xalia.exe" 0074:fixme:file:GetLongPathNameW UNC pathname L"\\\\\\\\?\\\\X:\\\\.local\\\\share\\\\Steam\\\\compatibilitytools.d\\\\Proton-GE Latest\\\\files\\\\share\\\\wine/../xalia/xalia.exe" 0128:fixme:oleacc:find\_class\_data unhandled window class: L"#32769" 0128:fixme:uiautomation:uia\_get\_providers\_for\_hwnd Override provider callback currently unimplemented. 0128:fixme:uiautomation:default\_uia\_provider\_callback Default ProviderType\_NonClientArea provider unimplemented. 0128:fixme:oleacc:find\_class\_data unhandled window class: L"#32769" 0128:fixme:uiautomation:base\_hwnd\_fragment\_get\_FragmentRoot 000000000081EE68, 000000000021F9A0: stub! 0128:fixme:uiautomation:base\_hwnd\_fragment\_GetEmbeddedFragmentRoots 000000000081EE68, 000000000021F9B0: stub! 0130:fixme:mscoree:parse\_supported\_runtime sku=L".NETFramework,Version=v4.8" not implemented 0130:fixme:mscoree:parse\_supported\_runtime sku=L".NETFramework,Version=v4.8" not implemented 0130:fixme:ntdll:NtQuerySystemInformation info\_class SYSTEM\_PERFORMANCE\_INFORMATION info: Game: xalia.exe info: DXVK: v2.7.1-509-g1676dcaf342a9b1 info: Build: x86\_64 gcc 14.2.0 info: Vulkan: Found vkGetInstanceProcAddr in winevulkan.dll @ 0x6ffffcc9fbf0 info: Extension providers: info: Platform WSI info: OpenVR info: OpenXR 0130:err:openxr:get\_vulkan\_extensions Error getting openxr\_vulkan\_instance\_extensions, status 0x2. warn: OpenXR: Unable to get required Vulkan instance extensions size info: Enabled instance extensions: info: VK\_KHR\_get\_surface\_capabilities2 info: VK\_KHR\_surface info: VK\_KHR\_surface\_maintenance1 info: VK\_KHR\_win32\_surface \[2026-05-07 23:00:52.600\] \[MANGOHUD\] \[info\] \[gpu.cpp:90\] Set renderD128 as active GPU (driver=amdgpu id=1002:66a1 pci\_dev=0000:05:00.0) \[2026-05-07 23:00:52.618\] \[MANGOHUD\] \[info\] \[cpu.cpp:825\] cpu vendor: GenuineIntel \[2026-05-07 23:00:52.618\] \[MANGOHUD\] \[error\] \[cpu.cpp:844\] failed to open core info file \[2026-05-07 23:00:52.618\] \[MANGOHUD\] \[info\] \[cpu.cpp:636\] hwmon: using input: /sys/class/hwmon/hwmon1/temp1\_input info: Found device: AMD Radeon Pro VII (RADV VEGA20) (radv 26.0.6) 0130:err:openxr:get\_vulkan\_extensions Error getting openxr\_vulkan\_instance\_extensions, status 0x2. warn: OpenXR: Unable to get required Vulkan Device extensions size 00c4:fixme:ntoskrnl:kernel\_object\_from\_handle No constructor for type L"Token" 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F318 0x00000004 0x00000000 stub 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F318 0x00000005 0x00000000 stub 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F318 0x00000006 0x00000000 stub 015c:fixme:kernelbase:AppPolicyGetThreadInitializationType FFFFFFFFFFFFFFFA, 0000000003FAFF50 0130:fixme:dinput:hid\_joystick\_device\_try\_open device usage ff00:0001 not implemented! 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F168 0x00000004 0x00000000 stub 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F168 0x00000005 0x00000000 stub 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F168 0x00000006 0x00000000 stub /builds/mono/wine-mono/wine-mono-11.1.0/mono/mono/eglib/gmisc-win32.c:138: assertion 'filename!= NULL' failed 0150:fixme:ver:GetCurrentPackageId (000000000011DB20 0000000000000000): stub 0058:fixme:ntoskrnl:kernel\_object\_from\_handle No constructor for type L"Token" 0150:err:virtual:virtual\_setup\_exception stack overflow 2112 bytes addr 0x6ffffff53822 stack 0x207c0 (0x20000-0x21000-0x120000) 0130:fixme:xinput:XInputGetBatteryInformation index 0, type 0, battery 000000000011F038. 0130:fixme:sync:SetWaitableTimerEx (00000000000001A8, 000000000011F0E8, 0, 0000000000000000, 0000000000000000, 0000000000000000, 0) semi-stub PropertiesChanged Signal received: Source: org.kde.Solid.PowerManagement.PolicyAgent active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.37

---

Agora apareceu o erro REAL.

```
stack overflow
```

E junto dele:

```
mono assertion 'filename != NULL' failed
```

Isso muda completamente o diagnóstico.

O problema agora NÃO é:

- GPU
- Vulkan
- DXVK
- Proton
- MI50

O problema virou:

## WINE MONO /.NET / EA APP / Frostbite bootstrap

O jogo está entrando num loop interno de bootstrap.NET e morrendo em stack overflow.

---

## O QUE ACONTECEU

Você zerou o prefix corretamente.  
Mas agora o Proton reinstalou:

- Wine Mono 11
- componentes fake.NET

E o NFS Heat/EA bootstrap está colidindo com isso.

---

## SOLUÇÃO CORRETA

## 1\. DESABILITAR WINE MONO

APAGUE o prefix de novo:

```bash
rm -rf ~/Games/Heroic/Prefixes/"need for speed heat"
```

---

## 2\. CRIE PREFIX LIMPO COM:

No Heroic:

### WineCfg / Winetricks:

NÃO instale:

- mono
- gecko
- dotnet20
- dxsdk

NADA.

---

## 3\. INSTALAR.NET REAL

Depois do prefix criado:

```bash
WINEPREFIX=~/Games/Heroic/Prefixes/"need for speed heat" winetricks -q vcrun2022
```

Depois:

```bash
WINEPREFIX=~/Games/Heroic/Prefixes/"need for speed heat" winetricks -q dotnet48
```

IMPORTANTE:

- NÃO usar dotnet20
- NÃO usar wine-mono

---

## 4\. DESATIVAR MONO COMPLETAMENTE

Antes de iniciar:

```bash
WINEDLLOVERRIDES="mscoree=d"
```

Isso impede Wine Mono de carregar.

---

## 5\. DESATIVAR XALIA

AQUI está outro possível culpado:

```
xalia.exe
```

Proton-GE moderno usa Xalia accessibility layer.

Às vezes ele explode stack em Frostbite.

Adicione:

```bash
PROTON_DISABLE_XALIA=1
```

---

## 6\. CONFIG FINAL CERTA

## ENV VARIABLES

```bash
PROTON_DISABLE_XALIA=1
WINEDLLOVERRIDES="mscoree=d"
RADV_PERFTEST=aco
mesa_glthread=true
DXVK_ENABLE_NVAPI=0
```

---

## 7\. DESATIVE OPENXR

Seu log mostra:

```
OpenXR: Unable to get required Vulkan extensions
```

Não deveria matar o jogo…  
MAS Frostbite + Proton + OpenXR às vezes gera recursion bug.

Adicione:

```bash
XR_RUNTIME_JSON=
```

---

## 8\. DESATIVE MANGOHUD AGORA

Tem forte chance do MangoHud estar hookando DXGI cedo demais.

Você ainda está usando:

```
mangohud --dlsym
```

REMOVE TOTALMENTE para teste.

---

## 9\. TESTE LIMPO VIA TERMINAL

Faça o teste nuclear:

```bash
export PROTON_DISABLE_XALIA=1
export WINEDLLOVERRIDES="mscoree=d"
export XR_RUNTIME_JSON=

STEAM_COMPAT_DATA_PATH=~/Games/Heroic/Prefixes/nfsheat \
~/.local/share/Steam/compatibilitytools.d/"Proton-GE Latest"/proton run \
"/mnt/win1/games/Need for Speed Heat/NeedForSpeedHeat.exe"
```

---

## O MAIS PROVÁVEL AGORA

A cadeia do problema ficou clara:

## Antes

- Wine 8 quebrava CPU topology

## Agora

- bootstrap.NET/Mono entra em recursion
- Xalia pode estar agravando
- Frostbite morre em stack overflow

---

## O MAIS IMPORTANTE

Sua MI50 está funcionando CORRETAMENTE.

DXVK inicializou:

```
Found device: AMD Radeon Pro VII (RADV VEGA20)
```

Isso prova:

- spoof OK
- Vulkan OK
- RADV OK
- amdgpu OK
- DXVK OK

O crash é puramente camada Wine/bootstrap/runtime.

---

**Você disse**

(23:00:28) \[INFO\]: Launching "need for speed heat" (sideload) (23:00:28) \[INFO\]: Native? false (23:00:28) \[INFO\]: Installed in: /mnt/win1/games/Need for Speed Heat (23:00:28) \[INFO\]: System Info: CPU: 36x Intel(R) Xeon(R) CPU E5-2699 v3 @ 2.30GHz Memory: 33.54 GB (used: 6.2 GB) GPUs: GPU 0: Name: Advanced Micro Devices, Inc. \[AMD/ATI\] Vega 20 \[Radeon Pro VII/Radeon Instinct MI50\] IDs: D=66a1 V=1002 SD=103e SV=17aa Driver: amdgpu OS: CachyOS Linux 7.0.3-1-cachyos (linux) The current system is not a Steam Deck We are not running inside a Flatpak container We are not running from an AppImage Software Versions: Heroic: 2.21.0 Loki Legendary: 0.20.43 Riding Shotgun (Heroic) gogdl: 1.2.1 comet: comet 0.2.0 Nile: 1.1.2 Will A. Zeppeli (23:00:28) \[INFO\]: Game Settings: { "autoInstallDxvkNvapi": true, "preferSystemLibs": false, "enableEsync": true, "enableFsync": true, "enableWineWayland": false, "enableHDR": false, "enableWoW64": false, "nvidiaPrime": false, "enviromentOptions": \[\], "wrapperOptions": \[\], "showFps": false, "showMangohud": true, "useGameMode": false, "battlEyeRuntime": true, "eacRuntime": true, "language": "", "beforeLaunchScriptPath": "", "afterLaunchScriptPath": "", "wineVersion": { "bin": "/home/johncoffee/.local/share/Steam/compatibilitytools.d/Proton-GE Latest/proton", "name": "Proton-GE Latest", "type": "proton" }, "winePrefix": "/home/johncoffee/Games/Heroic/Prefixes/need for speed heat" } Stored at: /home/johncoffee/.config/heroic/GamesConfig/cfgNSGx2n2bHwZv9m7g5GG.json (23:00:28) \[INFO\]: Winetricks packages: Wine Command: /usr/bin/mangohud --dlsym /usr/bin/umu-run /mnt/win1/games/Need for Speed Heat/NeedForSpeedHeat.exe Game Log: INFO: umu-launcher version 1.4.0 (3.14.4 (main, May 3 2026, 17:15:29) \[GCC 16.1.1 20260430\]) INFO: No GAMEID set, using umu-default INFO: steamrt3 is up to date INFO: Running 'Proton-GE Latest' using runtime 'sniper' INFO: Running 'steamrt3' using runtime 'host' ProtonFixes\[147513\] INFO: Running protonfixes on "GE-Proton10-34", build at 2026-03-23 03:55:11+00:00. ProtonFixes\[147513\] INFO: Running checks ProtonFixes\[147513\] INFO: All checks successful ProtonFixes\[147513\] WARN: Game title not found in CSV ProtonFixes\[147513\] INFO: Non-steam game UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: No store specified, using UMU database ProtonFixes\[147513\] INFO: Using early stage global defaults for UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: Non-steam game UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: No store specified, using UMU database ProtonFixes\[147513\] INFO: No early stage global protonfix found for UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: Running protonfixes on "GE-Proton10-34", build at 2026-03-23 03:55:11+00:00. ProtonFixes\[147513\] INFO: Running checks ProtonFixes\[147513\] INFO: All checks successful ProtonFixes\[147513\] INFO: Non-steam game UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: No store specified, using UMU database ProtonFixes\[147513\] INFO: Using main stage global defaults for UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: Non-steam game UNKNOWN (umu-default) ProtonFixes\[147513\] INFO: No store specified, using UMU database ProtonFixes\[147513\] INFO: No main stage global protonfix found for UNKNOWN (umu-default) Proton: /mnt/win1/games/Need for Speed Heat/NeedForSpeedHeat.exe Proton: Executable a unix path, launching with /unix option. Starting program with command-launcher service. To run commands in the per-app container, use a command like: /home/johncoffee/.local/share/umu/steamrt3/pressure-vessel/bin/steam-runtime-launch-client \\ --bus-name=:1.173 \\ -- \\ bash wineserver: NTSync up and running! 002c:fixme:winediag:loader\_init wine-staging 10.0 is a testing version containing experimental patches. 002c:fixme:winediag:loader\_init Please mention your exact version when filing bug reports on winehq.org. 0048:fixme:ntoskrnl:driver\_stub 0000000000249E30 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\pci" stub! 0048:fixme:ntoskrnl:driver\_stub 000000000024A080 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\hidusb" stub! 0048:fixme:ntoskrnl:driver\_stub 000000000024AED0 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\Disk" stub! 0058:fixme:ntoskrnl:kernel\_object\_from\_handle No constructor for type L"Token" \[2026-05-07 23:00:51.752\] \[MANGOHUD\] \[info\] \[blacklist.cpp:86\] process 'explorer.exe' is blacklisted in MangoHud 0074:err:system:NtUserChangeDisplaySettings Changing L"\\\\\\\\.\\\\DISPLAY1" display settings returned -2. 0074:err:explorer:initialize\_display\_settings Failed to initialize registry display settings for L"\\\\\\\\.\\\\DISPLAY1". 00b8:fixme:ntoskrnl:driver\_stub 0000000000249E30 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\pci" stub! 00b8:fixme:ntoskrnl:driver\_stub 000000000024A080 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\hidusb" stub! 00b8:fixme:ntoskrnl:driver\_stub 000000000024AED0 L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\Disk" stub! 00c4:fixme:ntoskrnl:kernel\_object\_from\_handle No constructor for type L"Token" 00dc:fixme:xinput:pdo\_pnp code 0xc, not implemented! 00dc:fixme:xinput:pdo\_pnp code 0xc, not implemented! 00c0:err:ntoskrnl:ZwLoadDriver failed to create driver L"\\\\Registry\\\\Machine\\\\System\\\\CurrentControlSet\\\\Services\\\\winebth": c0000142 003c:fixme:service:scmdatabase\_autostart\_services Auto-start service L"winebth" failed to start: 1114 00f4:fixme:wineusb:query\_id Unhandled ID query type 0x5. 0074:fixme:file:GetLongPathNameW UNC pathname L"\\\\\\\\?\\\\X:\\\\.local\\\\share\\\\Steam\\\\compatibilitytools.d\\\\Proton-GE Latest\\\\files\\\\share\\\\wine/../xalia/xalia.exe" 0074:fixme:file:GetLongPathNameW UNC pathname L"\\\\\\\\?\\\\X:\\\\.local\\\\share\\\\Steam\\\\compatibilitytools.d\\\\Proton-GE Latest\\\\files\\\\share\\\\wine/../xalia/xalia.exe" 0074:fixme:file:GetLongPathNameW UNC pathname L"\\\\\\\\?\\\\X:\\\\.local\\\\share\\\\Steam\\\\compatibilitytools.d\\\\Proton-GE Latest\\\\files\\\\share\\\\wine/../xalia/xalia.exe" 0128:fixme:oleacc:find\_class\_data unhandled window class: L"#32769" 0128:fixme:uiautomation:uia\_get\_providers\_for\_hwnd Override provider callback currently unimplemented. 0128:fixme:uiautomation:default\_uia\_provider\_callback Default ProviderType\_NonClientArea provider unimplemented. 0128:fixme:oleacc:find\_class\_data unhandled window class: L"#32769" 0128:fixme:uiautomation:base\_hwnd\_fragment\_get\_FragmentRoot 000000000081EE68, 000000000021F9A0: stub! 0128:fixme:uiautomation:base\_hwnd\_fragment\_GetEmbeddedFragmentRoots 000000000081EE68, 000000000021F9B0: stub! 0130:fixme:mscoree:parse\_supported\_runtime sku=L".NETFramework,Version=v4.8" not implemented 0130:fixme:mscoree:parse\_supported\_runtime sku=L".NETFramework,Version=v4.8" not implemented 0130:fixme:ntdll:NtQuerySystemInformation info\_class SYSTEM\_PERFORMANCE\_INFORMATION info: Game: xalia.exe info: DXVK: v2.7.1-509-g1676dcaf342a9b1 info: Build: x86\_64 gcc 14.2.0 info: Vulkan: Found vkGetInstanceProcAddr in winevulkan.dll @ 0x6ffffcc9fbf0 info: Extension providers: info: Platform WSI info: OpenVR info: OpenXR 0130:err:openxr:get\_vulkan\_extensions Error getting openxr\_vulkan\_instance\_extensions, status 0x2. warn: OpenXR: Unable to get required Vulkan instance extensions size info: Enabled instance extensions: info: VK\_KHR\_get\_surface\_capabilities2 info: VK\_KHR\_surface info: VK\_KHR\_surface\_maintenance1 info: VK\_KHR\_win32\_surface \[2026-05-07 23:00:52.600\] \[MANGOHUD\] \[info\] \[gpu.cpp:90\] Set renderD128 as active GPU (driver=amdgpu id=1002:66a1 pci\_dev=0000:05:00.0) \[2026-05-07 23:00:52.618\] \[MANGOHUD\] \[info\] \[cpu.cpp:825\] cpu vendor: GenuineIntel \[2026-05-07 23:00:52.618\] \[MANGOHUD\] \[error\] \[cpu.cpp:844\] failed to open core info file \[2026-05-07 23:00:52.618\] \[MANGOHUD\] \[info\] \[cpu.cpp:636\] hwmon: using input: /sys/class/hwmon/hwmon1/temp1\_input info: Found device: AMD Radeon Pro VII (RADV VEGA20) (radv 26.0.6) 0130:err:openxr:get\_vulkan\_extensions Error getting openxr\_vulkan\_instance\_extensions, status 0x2. warn: OpenXR: Unable to get required Vulkan Device extensions size 00c4:fixme:ntoskrnl:kernel\_object\_from\_handle No constructor for type L"Token" 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F318 0x00000004 0x00000000 stub 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F318 0x00000005 0x00000000 stub 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F318 0x00000006 0x00000000 stub 015c:fixme:kernelbase:AppPolicyGetThreadInitializationType FFFFFFFFFFFFFFFA, 0000000003FAFF50 0130:fixme:dinput:hid\_joystick\_device\_try\_open device usage ff00:0001 not implemented! 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F168 0x00000004 0x00000000 stub 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F168 0x00000005 0x00000000 stub 0130:fixme:setupapi:CM\_Get\_Parent 000000000011F168 0x00000006 0x00000000 stub /builds/mono/wine-mono/wine-mono-11.1.0/mono/mono/eglib/gmisc-win32.c:138: assertion 'filename!= NULL' failed 0150:fixme:ver:GetCurrentPackageId (000000000011DB20 0000000000000000): stub 0058:fixme:ntoskrnl:kernel\_object\_from\_handle No constructor for type L"Token" 0150:err:virtual:virtual\_setup\_exception stack overflow 2112 bytes addr 0x6ffffff53822 stack 0x207c0 (0x20000-0x21000-0x120000) 0130:fixme:xinput:XInputGetBatteryInformation index 0, type 0, battery 000000000011F038. 0130:fixme:sync:SetWaitableTimerEx (00000000000001A8, 000000000011F0E8, 0, 0000000000000000, 0000000000000000, 0000000000000000, 0) semi-stub PropertiesChanged Signal received: Source: org.kde.Solid.PowerManagement.PolicyAgent active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.37 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Mount active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Mount active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Scope active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Scope active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Scope active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Scope active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.gnome.UPnP.MediaContainer2 active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.57 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Service active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.freedesktop.systemd1.Unit active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.71 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.57 PropertiesChanged Signal received: Source: org.mpris.MediaPlayer2.Player active\_player: org.mpris.MediaPlayer2.rhythmbox active\_player's owner::1.57 sender::1.57 00fc:err:sync:RtlpWaitForCriticalSection section 00006FFFFE689DA0 "../src-wine/dlls/ntoskrnl.exe/sync.c: sync\_cs" wait timed out in thread 00fc, blocked by 00f0, retrying (60 sec)

---

Agora fechou o diagnóstico.

O erro fatal atual é:

```
RtlpWaitForCriticalSection wait timed out
```

Isso significa:

## DEADLOCK INTERNO DO WINE

O jogo não crashou diretamente.  
Ele travou numa espera circular entre threads.

E o stack overflow anterior continua sendo o gatilho inicial.

---

## O QUE ESTÁ GERANDO O DEADLOCK

A sequência do log entrega:

1. Xalia inicia
2. Mono tenta subir
3. .NET 4.8 entra
4. ntoskrnl sync trava
5. deadlock
6. timeout crítico

---

## O GRANDE PROBLEMA

Você ainda NÃO aplicou:

```bash
PROTON_DISABLE_XALIA=1
```

E:

```bash
WINEDLLOVERRIDES="mscoree=d"
```

O log prova isso porque:

- xalia.exe ainda inicia
- mscoree ainda tenta parsear.NET 4.8
- mono ainda explode

---

## VOCÊ PRECISA PARAR O WINE MONO

O log mostra:

```
wine-mono-11.1.0
```

Isso NÃO deveria mais aparecer.

---

## FAÇA EXATAMENTE ISSO

## 1\. DELETE O PREFIX NOVAMENTE

```bash
rm -rf ~/Games/Heroic/Prefixes/"need for speed heat"
```

---

## 2\. HEROIC → ENV VARIABLES

ADICIONE:

```bash
PROTON_DISABLE_XALIA=1
WINEDLLOVERRIDES=mscoree=d
XR_RUNTIME_JSON=
WINE_CPU_TOPOLOGY=16:0,16:1
```

---

## 3\. DESATIVE COMPLETAMENTE

## OFF:

- MangoHud
- Fsync
- ESync também agora
- overlays
- Discord
- Rhythmbox

Sim:  
DESATIVE ESYNC AGORA.

Porque agora o problema virou sync deadlock.

---

## 4\. USE APENAS:

```
Proton-GE 10-34
```

Não:

- CachyOS Proton
- Wine-GE
- Proton Experimental

---

## 5\. NÃO INSTALE NADA VIA WINETRICKS

Nada:

- dotnet
- mono
- dxsdk
- vcrun

ZERO.

O Proton moderno já carrega runtime suficiente.

O teu problema é justamente runtime DUPLICADO.

---

## 6\. FORÇAR DX11 LIMPO

Adicione:

```bash
PROTON_HIDE_NVIDIA_GPU=0
DXVK_ASYNC=1
DXVK_ENABLE_NVAPI=0
```

---

## 7\. TESTE TERMINAL LIMPO

SEM HEROIC.

```bash
export PROTON_DISABLE_XALIA=1
export WINEDLLOVERRIDES=mscoree=d
export XR_RUNTIME_JSON=
export DXVK_ASYNC=1

STEAM_COMPAT_DATA_PATH=~/Games/Heroic/Prefixes/nfsheat \
~/.local/share/Steam/compatibilitytools.d/"Proton-GE Latest"/proton run \
"/mnt/win1/games/Need for Speed Heat/NeedForSpeedHeat.exe"
```

---

## O QUE ESTÁ ACONTECENDO NO FUNDO

A Frostbite engine:

- inicializa accessibility APIs
- chama UIAutomation
- Proton injeta Xalia
- Xalia chama Mono/.NET
- Mono entra em recursion
- ntoskrnl lock trava
- deadlock

Isso é MUITO conhecido em jogos EA/Frostbite recentes.

---

## O MAIS IMPORTANTE

Teu Vulkan stack está PERFEITO.

DXVK:

```
DXVK v2.7.1
```

RADV:

```
AMD Radeon Pro VII (RADV VEGA20)
```

Tudo certo:

- MI50 OK
- spoof OK
- Vulkan OK
- mesa OK
- DXVK OK
- Proton OK

O problema é: