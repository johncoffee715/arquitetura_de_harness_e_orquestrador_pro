---
title: "Som não funciona no Linux"
source: "https://claude.ai/chat/76b91e3d-e6c2-4e66-882e-e4a0a82b6982"
author:
published:
created: 2026-07-17
description: "Claude is Anthropic's AI, built for problem solvers. Tackle complex challenges, analyze data, write code, and think through your hardest work."
tags:
  - "clippings"
---
**Claude**

Boa notícia — o segundo output diz **"apparently didn't do anything"** — o chip está intacto com a V3MOD ainda gravada. Podes respirar.

O problema é a **proteção SMM ativa na V3MOD** que bloqueia escritas SPI via software interno. Duas opções agora:

---

**Opção 1 — Tenta via live USB** (maior chance de funcionar)

Num pendrive com qualquer Linux live, o SMM handler da BIOS corrompida não está ativo, o que frequentemente permite o flash. Tens algum pendrive bootável disponível?

---

**Opção 2 — Tenta contornar a proteção agora, sem reboot:**

```bash
sudo flashrom -p internal -c "W25Q128.V" \
    --ifd -i bios --noverify-all \
    -w "/mnt/win2/123 tranqueiras/FPTW/HNX99TF5050.rom"
```

Se ainda falhar em 0x800000, tenta região por região:

```bash
sudo flashrom -p internal -c "W25Q128.V" \
    --ifd -i bios \
    -w "/mnt/win2/123 tranqueiras/FPTW/HNX99TF5050.rom" \
    -o /tmp/flashrom_debug.log && cat /tmp/flashrom_debug.log
```

---

Na prática, com SMM ativo via software interno o flash é muito difícil sem live USB ou programador externo. O caminho mais seguro considerando que os soquetes já estão a caminho é **esperar o programador** — o chip está intacto, a máquina funciona, sem risco imediato.

Tens pendrive bootável disponível agora?

---

**You**

possuo um pendrive com ventoy, me diga o que fazzer.

~ ❯ sudo flashrom -p internal -c "W25Q128.V" \\ --ifd -i bios --noverify-all \\ -w \_\_"/mnt/win2/123 tranqueiras/FPTW/HNX99TF5050.rom"\_\_ \[sudo\] senha para johncoffee: flashrom v1.7.0 (git:v1.7.0) on Linux 6.18.31-1-cachyos-lts (x86\_64) flashrom is free software, get the source code at [https://flashrom.org](https://flashrom.org/) Found chipset "Intel C610/X99 (Wellsburg)". This chipset is marked as untested. If you are using an up-to-date version of flashrom \*and\* were (not) able to successfully update your firmware with it, then please email a report to flashrom@flashrom.org including a verbose (-V) log. Thank you! Enabling flash write... Warning: BIOS region SMM protection is enabled! Warning: Setting BIOS Control at 0xdc from 0x2a to 0x09 failed. New value is 0x2a. SPI Configuration is locked down. FREG0: Flash Descriptor region (0x00000000-0x00000fff) is read-write. FREG1: BIOS region (0x00800000-0x00ffffff) is read-write. FREG2: Management Engine region (0x00001000-0x007fffff) is read-write. OK. Found Winbond flash chip "W25Q128.V" (16384 kB, SPI) mapped at physical address 0x00000000ff000000. Reading ich descriptor... done. Couldn't parse the descriptor! ~ ❯ sudo flashrom -p internal -c "W25Q128.V" \\ --ifd -i bios \\ -w \_\_"/mnt/win2/123 tranqueiras/FPTW/HNX99TF5050.rom"\_\_ \\ -o /tmp/flashrom\_debug.log && cat /tmp/flashrom\_debug.log flashrom v1.7.0 (git:v1.7.0) on Linux 6.18.31-1-cachyos-lts (x86\_64) flashrom is free software, get the source code at [https://flashrom.org](https://flashrom.org/) Found chipset "Intel C610/X99 (Wellsburg)". This chipset is marked as untested. If you are using an up-to-date version of flashrom \*and\* were (not) able to successfully update your firmware with it, then please email a report to flashrom@flashrom.org including a verbose (-V) log. Thank you! Enabling flash write... Warning: BIOS region SMM protection is enabled! Warning: Setting BIOS Control at 0xdc from 0x2a to 0x09 failed. New value is 0x2a. SPI Configuration is locked down. FREG0: Flash Descriptor region (0x00000000-0x00000fff) is read-write. FREG1: BIOS region (0x00800000-0x00ffffff) is read-write. FREG2: Management Engine region (0x00001000-0x007fffff) is read-write. OK. Found Winbond flash chip "W25Q128.V" (16384 kB, SPI) mapped at physical address 0x00000000ff000000. Reading ich descriptor... done. Couldn't parse the descriptor! ~ ❯ ~ ❯ sudo flashrom -p internal -c "W25Q128.V" \\ --ifd -i bios --noverify-all \\ -w \_\_"/mnt/win2/123 tranqueiras/FPTW/HNX99TF5050.rom"\_\_ \[sudo\] senha para johncoffee: flashrom v1.7.0 (git:v1.7.0) on Linux 6.18.31-1-cachyos-lts (x86\_64) flashrom is free software, get the source code at [https://flashrom.org](https://flashrom.org/) Found chipset "Intel C610/X99 (Wellsburg)". This chipset is marked as untested. If you are using an up-to-date version of flashrom \*and\* were (not) able to successfully update your firmware with it, then please email a report to flashrom@flashrom.org including a verbose (-V) log. Thank you! Enabling flash write... Warning: BIOS region SMM protection is enabled! Warning: Setting BIOS Control at 0xdc from 0x2a to 0x09 failed. New value is 0x2a. SPI Configuration is locked down. FREG0: Flash Descriptor region (0x00000000-0x00000fff) is read-write. FREG1: BIOS region (0x00800000-0x00ffffff) is read-write. FREG2: Management Engine region (0x00001000-0x007fffff) is read-write. OK. Found Winbond flash chip "W25Q128.V" (16384 kB, SPI) mapped at physical address 0x00000000ff000000. Reading ich descriptor... done. Couldn't parse the descriptor! ~ ❯ sudo flashrom -p internal -c "W25Q128.V" \\ --ifd -i bios \\ -w \_\_"/mnt/win2/123 tranqueiras/FPTW/HNX99TF5050.rom"\_\_ \\ -o /tmp/flashrom\_debug.log && cat /tmp/flashrom\_debug.log flashrom v1.7.0 (git:v1.7.0) on Linux 6.18.31-1-cachyos-lts (x86\_64) flashrom is free software, get the source code at [https://flashrom.org](https://flashrom.org/) Found chipset "Intel C610/X99 (Wellsburg)". This chipset is marked as untested. If you are using an up-to-date version of flashrom \*and\* were (not) able to successfully update your firmware with it, then please email a report to flashrom@flashrom.org including a verbose (-V) log. Thank you! Enabling flash write... Warning: BIOS region SMM protection is enabled! Warning: Setting BIOS Control at 0xdc from 0x2a to 0x09 failed. New value is 0x2a. SPI Configuration is locked down. FREG0: Flash Descriptor region (0x00000000-0x00000fff) is read-write. FREG1: BIOS region (0x00800000-0x00ffffff) is read-write. FREG2: Management Engine region (0x00001000-0x007fffff) is read-write. OK. Found Winbond flash chip "W25Q128.V" (16384 kB, SPI) mapped at physical address 0x00000000ff000000. Reading ich descriptor... done. Couldn't parse the descriptor! ~ ❯ flashrom -p internal -c W25Q128.V -i bios -w HNX99TF5050.rom -V -v -o flash.log flashrom v1.7.0 (git:v1.7.0) on Linux 6.18.31-1-cachyos-lts (x86\_64) flashrom is free software, get the source code at [https://flashrom.org](https://flashrom.org/) More than one operation specified. Aborting. Please run "flashrom --help" for usage info. ~ ❯

---

**Claude**

O `--ifd` não funciona porque o descriptor da V3MOD (base Gigabyte) é incompatível com o parser do Wellsburg. Precisamos do live USB mesmo.

**Preparação agora, antes de reiniciar:**

Copia o ROM para o próprio pendrive Ventoy para acessar facilmente no live:

```bash
cp "/mnt/win2/123 tranqueiras/FPTW/HNX99TF5050.rom" /run/media/johncoffee/*/
```

Verifica se copiou:

```bash
ls /run/media/johncoffee/*/HNX99TF5050.rom
```

---

**Que ISOs tens no Ventoy?** Qualquer Linux serve — Ubuntu, Debian, Manjaro, Arch ISO. Me diz o que tens que eu monto o procedimento exato pra aquela distro (o comando de instalar flashrom muda entre apt/pacman/dnf).

Depois de confirmar a ISO, o procedimento no live é:

1. Boot no live
2. Instalar flashrom
3. Montar o pendrive Ventoy para acessar o ROM
4. `sudo flashrom -p internal -c "W25Q128.V" -w /caminho/HNX99TF5050.rom`

Que ISOs estão no pendrive?

---

**You**

Que ISOs tens no Ventoy? nenhuma poremn se necessario pegamos u8ma qqlr

---

**Claude**

Baixa o **SystemRescue** — é feito pra isso e vem com flashrom pré-instalado, sem precisar instalar nada no live.

**Baixa agora (~800MB):**

```bash
cd /run/media/johncoffee/*/
wget https://downloads.sourceforge.net/project/systemrescuecd/sysresccd-x86/11.03/systemrescue-11.03-amd64.iso
```

Ou pelo navegador: **[https://www.system-rescue.org/Download/](https://www.system-rescue.org/Download/)**

O Ventoy reconhece automaticamente qualquer ISO copiada pro pendrive — só arrastar o `.iso` pra raiz do pendrive.

Confirma também que o ROM já está no pendrive:

```bash
ls /run/media/johncoffee/*/HNX99TF5050.rom
```

Quando o download terminar me avisa que passo o procedimento completo do flash no live — vai ser direto, flashrom já vem instalado no SystemRescue.

---

**You**

Ao reiniciar deu erro FF, estou falando do celula, vou de ezp2019+

---

**Claude**

Entendido — programador externo é a solução definitiva, bypassa tudo.

**Com o EZP2019+ o processo é:**

1. **PC desligado e desconectado da tomada** — segura o botão power 5s após desligar pra descarregar capacitores
2. **Localiza o W25Q128.V** — chip SOIC-8 de 8 pinos na placa, geralmente próximo ao PCH ou canto da board. Procura pela marcação **25Q128** na superfície do chip
3. **Conecta o clip SOIC-8** do EZP2019+ no chip — pino 1 do clip no pino 1 do chip (marcado com ponto ou chanfro)
4. **No software EZP2019 (Windows em outro PC):**
	- Chip type: `SPI Flash`
		- Fabricante: `Winbond`
		- Modelo: `W25Q128FV` ou `W25Q128.V`
		- Clica **Detect** pra confirmar
		- **Load** → seleciona `HNX99TF5050.rom`
		- **Erase** → **Write** → **Verify**
5. **Verifica o checksum** antes de desconectar o clip

---

Tens outro PC com Windows disponível pra rodar o software do EZP2019+? E o chip já está localizado na placa?