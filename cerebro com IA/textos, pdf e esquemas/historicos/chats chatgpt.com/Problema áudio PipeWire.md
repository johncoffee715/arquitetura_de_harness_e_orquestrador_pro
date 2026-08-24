---
title: "Problema áudio PipeWire"
source: "https://chatgpt.com/c/6a051028-cfec-83e9-a9df-fe8057c2d57d"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 4 messages"
tags:
  - "clippings"
---
**Você disse**

nao esta reconhecendo minha porta de eudio traseira ou minha caixa de som

---

Pela imagem, o KDE/PipeWire não está vendo **nenhum dispositivo de áudio**. Isso geralmente é uma destas 4 coisas:

1. PipeWire/WirePlumber parado ou quebrado.
2. Perfil de áudio desligado.
3. ALSA detectou a placa, mas está mutado/desativado.
4. Controladora de áudio onboard desativada na BIOS ou driver HDA não carregou.

Faça em ordem.

---

## 1\. Reinstalar stack de áudio e reiniciar serviços

Cole no terminal:

```bash
sudo pacman -Syu --needed pipewire pipewire-pulse pipewire-alsa wireplumber alsa-utils pavucontrol sof-firmware
systemctl --user daemon-reload
systemctl --user enable --now pipewire pipewire-pulse wireplumber
systemctl --user restart pipewire pipewire-pulse wireplumber
```

Depois teste:

```bash
wpctl status
```

Se aparecer algo como `Audio`, `Sinks`, `Sources`, já voltou parcialmente.

---

## 2\. Resetar configuração quebrada do usuário

Se ainda aparecer “nenhum dispositivo”, rode:

```bash
mkdir -p ~/.backup-audio
mv ~/.config/pulse ~/.backup-audio/pulse.bak 2>/dev/null
mv ~/.local/state/wireplumber ~/.backup-audio/wireplumber.bak 2>/dev/null
mv ~/.config/pipewire ~/.backup-audio/pipewire.bak 2>/dev/null

systemctl --user restart pipewire pipewire-pulse wireplumber
```

Depois abra o controle de áudio:

```bash
pavucontrol
```

Vá em **Configuração** e veja se aparece algo como:

```
Áudio interno
Analog Stereo Output
```

Não deixe em `Off`.

---

## 3\. Ver se o Linux enxerga a controladora de áudio

Rode:

```bash
lspci -nnk | grep -A4 -i audio
aplay -l
```

### Resultado esperado

Algo parecido com:

```
Audio device: Intel Corporation ...
Kernel driver in use: snd_hda_intel
```

E no `aplay -l` algo como:

```
card 0: PCH [HDA Intel PCH]
```

Se **não aparecer nada**, o problema é antes do PipeWire: BIOS, kernel module ou controladora onboard desativada.

---

## 4\. Forçar reload do driver HDA Intel

Como sua plataforma é X99/Xeon, provavelmente usa `snd_hda_intel`.

Rode:

```bash
sudo modprobe -r snd_hda_intel snd_hda_codec_realtek snd_hda_codec_generic snd_hda_codec_hdmi 2>/dev/null
sudo modprobe snd_hda_intel
systemctl --user restart pipewire pipewire-pulse wireplumber
```

Teste de novo:

```bash
aplay -l
wpctl status
```

---

## 5\. Verificar mute no ALSA

Rode:

```bash
alsamixer
```

Dentro do `alsamixer`:

- pressione `F6`
- escolha sua placa de som
- veja `Master`, `Speaker`, `Headphone`, `PCM`, `Line Out`
- se tiver `MM`, está mutado
- aperte `M` para desmutar
- aumente com seta para cima

Depois salve:

```bash
sudo alsactl store
```

---

## 6\. Comando de diagnóstico rápido

Se nada resolver, rode este bloco e me mande a saída:

```bash
echo "===== PipeWire ====="
systemctl --user status pipewire pipewire-pulse wireplumber --no-pager

echo "===== WPCTL ====="
wpctl status

echo "===== ALSA CARDS ====="
cat /proc/asound/cards

echo "===== APLAY ====="
aplay -l

echo "===== PCI AUDIO ====="
lspci -nnk | grep -A4 -i audio

echo "===== KERNEL AUDIO ERRORS ====="
dmesg | grep -Ei "snd|hda|audio|codec|sof" | tail -80
```

---

## 7\. BIOS — ponto crítico

Se `lspci` não mostrar nenhum dispositivo de áudio, entre na BIOS e procure algo como:

```
Onboard Audio
HD Audio Controller
Azalia Audio
Intel HD Audio
```

Deixe como:

```
Enabled
```

Em placa X99 chinesa/modificada, BIOS mod às vezes desativa ou bagunça Azalia/HD Audio.

---

Minha aposta pela imagem: **PipeWire/WirePlumber parou ou perdeu a configuração**, porque o KDE não mostra nem entrada nem saída. Comece pelo passo 1 e 2.

---

**Você disse**

.-------------------------: johncoffee@JohnCoffeeDesk.+=========================. -------------------------:++===++==================-:++- OS: CachyOS x86\_64:\*++====+++++=============-.==: Host: X99-D8 -\*+++=====+\*\*\*++==========: Kernel: Linux 7.0.5-2-cachyos =\*++++========------------: Uptime: 2 hours, 57 mins =\*+++++=====-... Packages: 14 (flatpak), 1598 (pacman).+\*+++++=-===:.=+++=: Shell: fish 4.7.1:++++=====-==: -\*\*\*\*\*+ Display (LG TV): 3840x2160 @ 1.75x in 72", 30 Hz \[External\]:++========-=..=+\*\*+. DE: KDE Plasma 6.6.5.+==========-.. WM: KWin (Wayland):+++++++====-.--==-. WM Theme: Breeze:++==========.:+++++++: Theme: Breeze (Dark) \[Qt\], Breeze-Dark \[GTK2\], Breeze \[GTK3\].-===========. =\*\*\*\*\*+\*+ Icons: breeze-dark \[Qt\], breeze-dark \[GTK2/3/4\].-===========:.+\*\*\*\*\*+: Font: Noto Sans (10pt) \[Qt\], Noto Sans (10pt) \[GTK2/3/4\] -=======++++:::::::::::::::::::::::::-:.---: Cursor: capitaine (24px):======++++====+++\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*=. Terminal: konsole 26.4.1:=====+++==========++++++++++++++\*- CPU: Intel(R) Xeon(R) E5-2699 v3 (36) @ 3.60 GHz.====++==============++++++++++\*- GPU: AMD Radeon Pro VII/Radeon Instinct MI50 \[Discrete\].===+==================+++++++: Memory: 6.85 GiB / 31.23 GiB (22%).-=======================+++: Swap: 2.97 GiB / 31.23 GiB (9%).......................... Disk (/): 79.96 GiB / 117.24 GiB (68%) - btrfs Disk (/mnt/win1): 820.66 GiB / 931.51 GiB (88%) - ntfs3 Disk (/mnt/win2): 777.02 GiB / 931.51 GiB (83%) - ntfs3 Local IP (enp7s0): 192.168.18.14/24 Locale: pt\_BR.UTF-8 ~ ❯ sudo pacman -Syu --needed pipewire pipewire-pulse pipewire-alsa wireplumber alsa-utils pavucontrol sof-firmware systemctl --user daemon-reload systemctl --user enable --now pipewire pipewire-pulse wireplumber systemctl --user restart pipewire pipewire-pulse wireplumber \[sudo\] senha para johncoffee::: Sincronizando a base de dados de pacotes... cachyos-v3 está atualizado cachyos-extra-v3 está atualizado cachyos-core-v3 está atualizado cachyos 524,1 KiB 9,84 MiB/s 00:00 \[---------------------------------------------------------------------------\] 100% core está atualizado extra 8,2 MiB 51,4 MiB/s 00:00 \[---------------------------------------------------------------------------\] 100% multilib está atualizado atenção: pipewire-1:1.6.4-1.1 está atualizado -- ignorando atenção: pipewire-pulse-1:1.6.4-1.1 está atualizado -- ignorando atenção: pipewire-alsa-1:1.6.4-1.1 está atualizado -- ignorando atenção: wireplumber-0.5.14-1.1 está atualizado -- ignorando atenção: alsa-utils-1.2.15.2-2.1 está atualizado -- ignorando atenção: pavucontrol-1:6.2-1.1 está atualizado -- ignorando atenção: sof-firmware-2025.12.2-1 está atualizado -- ignorando:: Iniciando atualização completa do sistema... atenção: webkitgtk-6.0: local (2.52.3-1.1) é mais novo que extra (2.52.3-1) nada para fazer Created symlink '/home/johncoffee/.config/systemd/user/default.target.wants/pipewire.service' → '/usr/lib/systemd/user/pipewire.service'. Created symlink '/home/johncoffee/.config/systemd/user/sockets.target.wants/pipewire.socket' → '/usr/lib/systemd/user/pipewire.socket'. Created symlink '/home/johncoffee/.config/systemd/user/default.target.wants/pipewire-pulse.service' → '/usr/lib/systemd/user/pipewire-pulse.service'. Created symlink '/home/johncoffee/.config/systemd/user/sockets.target.wants/pipewire-pulse.socket' → '/usr/lib/systemd/user/pipewire-pulse.socket'. Created symlink '/home/johncoffee/.config/systemd/user/pipewire-session-manager.service' → '/usr/lib/systemd/user/wireplumber.service'. Created symlink '/home/johncoffee/.config/systemd/user/pipewire.service.wants/wireplumber.service' → '/usr/lib/systemd/user/wireplumber.service'. ~ 10s ❯

---

<iframe title="internal://deep-research" src="https://connector_openai_deep_research.web-sandbox.oaiusercontent.com/?app=chatgpt&amp;darkModeType=increased&amp;locale=pt-BR&amp;deviceType=desktop" allow="camera *; clipboard-read *; clipboard-write *; fullscreen *; local-network-access *; microphone *; web-share *" allowfullscreen=""></iframe>