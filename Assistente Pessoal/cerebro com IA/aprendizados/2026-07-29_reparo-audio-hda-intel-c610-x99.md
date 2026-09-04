---
tags: [audio, arch-linux, kernel, hda-intel, alsa, pipewire, hardware, c610, x99, live-usb]
categoria: hardware-fix
status: resolvido
kernel: 7.0.11-1-cachyos
distro: Arch Linux Live USB
data: 2026-07-29
---

# Reparo de Áudio — HDA Intel C610/X99 (Live USB)

## TL;DR

```bash
sudo modprobe -r snd_hda_intel snd_hda_codec snd_hda_core snd_intel_dspcfg snd_intel_sdw_acpi snd_hwdep snd_pcm
sudo modprobe snd_hda_intel probe_mask=1 single_cmd=1 enable_msi=0
amixer -c 0 set Master 80% unmute
systemctl --user restart pipewire pipewire-pulse wireplumber
```

## Problema

Sem som em Live USB (CachyOS). `aplay -l` lista **0** dispositivos. PipeWire só oferece "Dummy Output".

## Sintomas-chave

- `lspci | grep Audio` → Intel C610/X99 HD Audio Controller (00:1b.0) ✓
- `lsmod | grep snd_hda_intel` → carregado ✓
- `cat /proc/asound/cards` → card0 (HDA Intel PCH) ✓
- `/proc/asound/card0/` → só tem `id`, **sem `codec#0`** ✗
- `dmesg`:
  ```
  snd_hda_intel 0000:00:1b.0: enabling device (0000 -> 0002)
  snd_hda_intel 0000:00:1b.0: no codecs found!
  ```

## Causa raiz

Controlador HDA Intel C610/X99 não consegue comunicação CORB/RIRB com o codec. Comum em:

1. **Live USB** — o PCI device habilita tarde (`enabling device (0000 -> 0002)` em vez do boot), o que interfere na inicialização do codec.
2. **BIOS C610/X99** com inicialização preguiçosa do codec.
3. **Codec Realtek ALC892** que responde apenas via single-command (legado) e não via CORB/RIRB.

## Solução final

Descarregar os módulos HDA e recarregar com parâmetros alternativos:

```bash
sudo modprobe -r snd_hda_intel snd_hda_codec snd_hda_core \
  snd_intel_dspcfg snd_intel_sdw_acpi snd_hwdep snd_pcm
# O snd_timer pode falhar a sair (snd_seq usa), mas isso é OK

sudo modprobe snd_hda_intel probe_mask=1 single_cmd=1 enable_msi=0
```

### Parâmetros-chave

| Parâmetro | Função |
|-----------|--------|
| `single_cmd=1` | Usa método de comando único (legado) em vez de CORB/RIRB. **Essencial.** |
| `probe_mask=1` | Força probe do codec no slot 0. |
| `enable_msi=0` | Desabilita MSI (precaução em hardware legado). |

## Tentativas que falharam

| Tentativa | Por que falhou |
|-----------|---------------|
| `amixer set Master 80% unmute` | Aumenta volume mas sem codec não há hardware |
| `echo 1 > /sys/bus/pci/drivers/snd_hda_intel/.../remove` + rescan PCI | Codec não re-aparece |
| `echo on > /sys/devices/pci.../power/control` | Não afeta o codec |
| `modprobe -r snd_hda_intel` puro | Falha (snd_timer em uso) — mas descarregar dependentes antes resolve |
| `modprobe snd_hda_intel` sem parâmetros | Re-apresenta "no codecs found!" |

## Após o fix

```bash
# Configurar volumes
amixer -c 0 set Master 80% unmute
amixer -c 0 set Headphone 80% unmute
amixer -c 0 set Front 80% unmute

# Reiniciar PipeWire para detectar a card
systemctl --user restart pipewire pipewire-pulse wireplumber
```

### Resultado

- Codec **Realtek ALC892** (Vendor 0x10ec0892) detectado
- Devices: ALC892 Analog (device 0) + ALC892 Digital (device 1)
- Canais: Line Out Front/Surround/CLFE/Side, Headphone, Mic, Line, CD
- PipeWire sink: `alsa_output.pci-0000_00_1b.0.analog-stereo` RUNNING
- Áudio funcional (testado com `speaker-test` e Firefox)

## Diagnóstico rápido

```bash
# 1. Codec detectado?
cat /proc/asound/card0/codec#0 | head -3

# 2. Dispositivos de playback?
aplay -l

# 3. Sinks no PipeWire?
wpctl status | grep -A10 Sinks

# 4. Erros no kernel?
dmesg | grep -iE 'hda|codec' | tail -20

# 5. Módulo é built-in ou carregável?
ls /lib/modules/$(uname -r)/kernel/sound/hda/controllers/snd-hda-intel.ko.zst
```

## Tornar persistente (em instalação real, não Live USB)

```bash
# /etc/modprobe.d/alsa-fix.conf
options snd-hda-intel probe_mask=1 single_cmd=1 enable_msi=0
sudo mkinitcpio -P   # ou dracut --force
```

## Referências cruzadas

- Stack Overflow: "snd_hda_intel: no codecs found!" em C610/X99
- ALSA docs: parâmetro `single_cmd` documentado em `modinfo snd_hda_intel`
- Arch Wiki: HDA — solução de problemas com "no codecs found"

## Aprendizado

> Quando `aplay -l` lista 0 dispositivos mas `lspci` mostra hardware e `snd_hda_intel` está carregado, **sempre checar `dmesg | grep hda`** antes de qualquer outra ação. A mensagem "no codecs found!" tem diagnóstico e solução diretos via parâmetros do módulo.
