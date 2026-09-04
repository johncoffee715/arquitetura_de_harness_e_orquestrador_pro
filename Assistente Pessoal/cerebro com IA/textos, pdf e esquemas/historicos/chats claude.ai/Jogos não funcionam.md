---
title: "Jogos não funcionam"
source: "https://claude.ai/chat/c4bb9dcc-44bd-457c-8d6d-8b3d38e2a644"
author:
published:
created: 2026-07-17
description: "Claude is Anthropic's AI, built for problem solvers. Tackle complex challenges, analyze data, write code, and think through your hardest work."
tags:
  - "clippings"
---
**Claude**

Tudo em mãos. Vamos resolver o 60Hz agora, depois confirmar Ollama e jogos.

### Fix 4K@60Hz — editar config do KWin diretamente

O `kwinoutputconfig.json` tem o modo travado em `refreshRate: 30000`. O EDID confirma suporte a VIC 97 (60Hz, 594MHz). A TV tem HDMI 2.0 nativo — se o adaptador for ativo (com chip), funciona. Vamos forçar:

```bash
# Backup primeiro
cp ~/.config/kwinoutputconfig.json ~/.config/kwinoutputconfig.json.bak

# Injetar custom mode 60Hz e mudar refresh
python3 << 'EOF'
import json

path = "/home/johncoffee/.config/kwinoutputconfig.json"
with open(path) as f:
    config = json.load(f)

for group in config:
    for item in group.get("data", []):
        if item.get("connectorName") == "DP-2":
            item["customModes"] = [{"height": 2160, "refreshRate": 60000, "width": 3840}]
            item["mode"]["refreshRate"] = 60000
            print("DP-2 atualizado:", item["mode"])

with open(path, "w") as f:
    json.dump(config, f, indent=4)
print("Salvo.")
EOF

# Aplicar sem logout — reiniciar o KWin
kwin_wayland --replace &
```

Se o display ficar sem sinal ou piscar, o adaptador é passivo e não aguenta — volta com:

```bash
cp ~/.config/kwinoutputconfig.json.bak ~/.config/kwinoutputconfig.json && kwin_wayland --replace &
```

---

### Ollama — confirmar GPU (55s parece CPU)

55 segundos para `mistral-nemo` é suspeito — pode ter sido só o carregamento frio do modelo, mas vamos confirmar:

```bash
# Testar de novo (modelo já na memória)
time ollama run mistral-nemo "oi" 2>&1 | tail -3

# Ver se VRAM subiu durante inferência
watch -n1 'cat /sys/class/drm/renderD128/device/mem_info_vram_used'
```

---

### Jogos — testa agora

Com os prefixes limpos, lança **Tekken 8** e **SW Jedi Fallen Order** pelo Heroic e manda os logs. O prefix vai ser recriado do zero na primeira inicialização — normal demorar um pouco na primeira vez.

---

**You**

❯ bash \[johncoffee@JohnCoffeeDesk ~\]$ # Backup primeiro cp ~/.config/kwinoutputconfig.json ~/.config/kwinoutputconfig.json.bak # Injetar custom mode 60Hz e mudar refresh python3 << 'EOF' import json path = "/home/johncoffee/.config/kwinoutputconfig.json" with open(path) as f: config = json.load(f) for group in config: for item in group.get("data", \[\]): if item.get("connectorName") == "DP-2": item\["customModes"\] = \[{"height": 2160, "refreshRate": 60000, "width": 3840}\] item\["mode"\]\["refreshRate"\] = 60000 print("DP-2 atualizado:", item\["mode"\]) with open(path, "w") as f: json.dump(config, f, indent=4) print("Salvo.") EOF # Aplicar sem logout — reiniciar o KWin kwin\_wayland --replace & DP-2 atualizado: {'flags': 0, 'height': 2160, 'refreshRate': 60000, 'width': 3840} Salvo. \[1\] 35633 \[johncoffee@JohnCoffeeDesk ~\]$

---

**Claude**

O KWin está reiniciando em background (PID 35633). Aguarda 3–5 segundos e verifica se pegou:

```bash
sleep 4 && kscreen-doctor -o | grep -E "mode.*\*|Modes:|current|refresh|Scale" | head -10
```

Se o display ficou estável (sem piscar/sem sinal), o adaptador suporta — confirma com:

```bash
# Verificar refresh rate atual
kscreen-doctor -o | grep -E "\*"
```

Deve aparecer algo como `3840x2160@60.00*`.

Se o monitor ficou sem sinal ou piscando, roda agora:

```bash
cp ~/.config/kwinoutputconfig.json.bak ~/.config/kwinoutputconfig.json && kwin_wayland --replace &
```

O que aconteceu na tela?

---

**You**

~ ❯ sleep 4 && kscreen-doctor -o | grep -E "mode.\*\\\*|Modes:|current|refresh|Scale" | head -10 Modes: 1:1920x1080@60.00! 2:4096x2160@30.00 3:4096x2160@29.97 4:4096x2160@25.00 5:4096x2160@24.00 6:4096x2160@23.98 7:3840x2160@30.00\* 8:3840x2160@29.97 9:3840x2160@25.00 10:3840x2160@24.00 11:3840x2160@23.98 12:1920x1080@60.00 13:1920x1080@59.94 14:1920x1080@50.00 15:1920x1080@30.00 16:1920x1080@29.97 17:1920x1080@25.00 18:1920x1080@24.00 19:1920x1080@23.98 20:1280x1024@60.02 21:1360x768@60.01 22:1152x864@59.97 23:1280x720@60.00 24:1280x720@60.00 25:1280x720@59.94 26:1280x720@50.00 27:1024x768@60.00 28:800x600@60.32 29:720x576@50.00 30:720x480@60.00 31:720x480@60.00 32:720x480@59.94 33:720x480@59.94 34:640x480@60.00 35:640x480@59.94 36:640x480@59.94 37:720x400@70.08 38:1280x800@59.81 39:1600x900@59.95 40:1368x768@59.88 Scale: 1.75 ~ ❯ # Verificar refresh rate atual kscreen-doctor -o | grep -E "\\\*" Modes: 1:1920x1080@60.00! 2:4096x2160@30.00 3:4096x2160@29.97 4:4096x2160@25.00 5:4096x2160@24.00 6:4096x2160@23.98 7:3840x2160@30.00\* 8:3840x2160@29.97 9:3840x2160@25.00 10:3840x2160@24.00 11:3840x2160@23.98 12:1920x1080@60.00 13:1920x1080@59.94 14:1920x1080@50.00 15:1920x1080@30.00 16:1920x1080@29.97 17:1920x1080@25.00 18:1920x1080@24.00 19:1920x1080@23.98 20:1280x1024@60.02 21:1360x768@60.01 22:1152x864@59.97 23:1280x720@60.00 24:1280x720@60.00 25:1280x720@59.94 26:1280x720@50.00 27:1024x768@60.00 28:800x600@60.32 29:720x576@50.00 30:720x480@60.00 31:720x480@60.00 32:720x480@59.94 33:720x480@59.94 34:640x480@60.00 35:640x480@59.94 36:640x480@59.94 37:720x400@70.08 38:1280x800@59.81 39:1600x900@59.95 40:1368x768@59.88 ~

---

**Claude**

O custom mode foi ignorado pelo DRM — o KWin tentou estabelecer o link com 594MHz de pixel clock e o adaptador mini-DP → HDMI não conseguiu. Isso confirma que é um **adaptador passivo** — ele converte o sinal elétrico DP→HDMI mas não tem chip para renegociar o link rate. Para 4K@60Hz você precisa de um adaptador ativo (com chip, custa ~R$60–80 no ML).

Quando "alguns jogos rodam 4K@60Hz" provavelmente significa que eles abrem em **1080p@60Hz** (modo 12 na lista, que funciona), não 4K@60Hz real.

Por enquanto, configura 1080p@60Hz como padrão do desktop — fica fluido para uso geral:

```bash
kscreen-doctor output.DP-2.mode.12
```

---

### Voltando ao objetivo principal — os jogos

Com os prefixes deletados, vamos testar. Antes de lançar qualquer jogo, uma coisa que vai afetar todos: o `LD_LIBRARY_PATH` herdado tem `/opt/rocm/lib` no meio, o que pode fazer o Wine carregar libs ROCm erradas. Verifica de onde vem:

```bash
grep -r "opt/rocm" \
  ~/.config/fish/config.fish \
  ~/.config/fish/conf.d/ \
  /etc/profile.d/ \
  ~/.config/environment.d/ \
  /etc/environment 2>/dev/null
```

Agora lança o **Tekken 8** pelo Heroic e manda o log. Ele tem o prefix mais simples (sem EAC problemático) e vai confirmar se o fix dos prefixes resolveu o problema sistêmico.

---

**You**

(16:18:58) \[INFO\]: Launching "tekken 8" (sideload) (16:18:58) \[INFO\]: Native? false (16:18:58) \[INFO\]: Installed in: /mnt/win2/games/Tekken 8

(16:18:58) \[INFO\]: System Info: CPU: 36x Intel(R) Xeon(R) CPU E5-2699 v3 @ 2.30GHz Memory: 33.47 GB (used: 6 GB) GPUs: GPU 0: Name: Advanced Micro Devices, Inc. \[AMD/ATI\] Vega 20 \[Radeon Pro VII/Radeon Instinct MI50\] IDs: D=66a1 V=1002 SD=103e SV=17aa Driver: amdgpu OS: CachyOS Linux 7.0.11-1-cachyos (linux)

The current system is not a Steam Deck We are not running inside a Flatpak container We are not running from an AppImage

Software Versions: Heroic: 2.22.0 Hajrudin Legendary: 0.20.43 Riding Shotgun (Heroic) gogdl: 1.2.1 comet: comet 0.2.0 Nile: 1.1.2 Will A. Zeppeli

(16:18:58) \[INFO\]: Game Settings: { "autoInstallDxvk": true, "autoInstallDxvkNvapi": true, "autoInstallVkd3d": true, "preferSystemLibs": false, "enableEsync": true, "enableFsync": true, "enableWineWayland": false, "enableHDR": false, "enableWoW64": false, "nvidiaPrime": false, "enviromentOptions": \[\], "wrapperOptions": \[\], "showFps": true, "showMangohud": true, "useGameMode": false, "battlEyeRuntime": true, "eacRuntime": true, "language": "", "beforeLaunchScriptPath": "", "afterLaunchScriptPath": "", "wineVersion": { "bin": "/home/johncoffee/.config/heroic/tools/wine/Wine-GE-latest/bin/wine", "name": "Wine-GE-latest", "type": "wine", "lib": "/home/johncoffee/.config/heroic/tools/wine/Wine-GE-latest/lib64", "lib32": "/home/johncoffee/.config/heroic/tools/wine/Wine-GE-latest/lib", "wineserver": "/home/johncoffee/.config/heroic/tools/wine/Wine-GE-latest/bin/wineserver" }, "winePrefix": "/mnt/win2/prefixos/tekken 8" } Stored at: /home/johncoffee/.config/heroic/GamesConfig/b7cLh4aVn9d16dCrFm4hDV.json

(16:18:58) \[INFO\]: Winetricks packages: ~ ❯ grep -r "opt/rocm" \\ ~/.config/fish/config.fish \\ ~/.config/fish/conf.d/ \\ /etc/profile.d/ \\ ~/.config/environment.d/ \\ /etc/environment 2>/dev/null /etc/profile.d/rocm.sh:export ROCM\_PATH=/opt/rocm /etc/profile.d/rocm.sh:append\_path '/opt/rocm/bin' ~ ❯

---

**Claude**

Achado — o ROCm entra pelo `/etc/profile.d/rocm.sh` e vai direto para o `LD_LIBRARY_PATH` de todos os processos, incluindo Wine. O log do Tekken cortou antes do Game Log — o jogo abriu ou crashou?

Manda a parte que falta (o "Game Log:" em diante) ou me diz o que apareceu na tela.

Enquanto isso, o fix para o ROCm não contaminar os jogos: adicionar nas **configurações globais do Heroic** (Settings → Game Defaults → Environment Variables) para todos os jogos de uma vez:

| Chave | Valor |
| --- | --- |
| `LD_LIBRARY_PATH` | `/usr/lib:/usr/lib32` |

Isso sobrescreve o LD\_LIBRARY\_PATH herdado do shell para os jogos, sem tocar no ROCm do sistema. O Wine tem as libs que precisa em `/usr/lib` e `/usr/lib32` — não precisa do `/opt/rocm/lib`.

Mas confirma primeiro se o Tekken abriu — se sim, pode ser que o problema já estava só nos prefixes e o ROCm não estava afetando. Se ainda crashou, aplica o fix acima e testa de novo.