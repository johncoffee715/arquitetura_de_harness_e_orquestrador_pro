---
title: "Erro ao atualizar BIOS"
source: "https://chatgpt.com/c/6a08b396-bf00-83e9-baaa-d52bea8a2e93"
author:
published:
created: 2026-07-17
description: "O ChatGPT é seu assistente de IA para uso diário. Converse com a IA mais avançada para explorar ideias, resolver problemas e aprender mais rápido."
tags:
  - "clippings"
---
**Você disse**

possuo um pendrive com ventoy, me diga o que fazzer. ~ ❯ sudo flashrom -p internal -c "W25Q128.V" \\ --ifd -i bios --noverify-all \\ -w \_\_"/mnt/win2/123 tranqueiras/FPTW/HNX99TF5050.rom"\_\_ \[sudo\] senha para johncoffee: flashrom v1.7.0 (git:v1.7.0) on Linux 6.18.31-1-cachyos-lts (x86\_64) flashrom is free software, get the source code at [https://flashrom.org](https://flashrom.org/) Found chipset "Intel C610/X99 (Wellsburg)". This chipset is marked as untested. If you are using an up-to-date version of flashrom \*and\* were (not) able to successfully update your firmware with it, then please email a report to flashrom@flashrom.org including a verbose (-V) log. Thank you! Enabling flash write... Warning: BIOS region SMM protection is enabled! Warning: Setting BIOS Control at 0xdc from 0x2a to 0x09 failed. New value is 0x2a. SPI Configuration is locked down. FREG0: Flash Descriptor region (0x00000000-0x00000fff) is read-write. FREG1: BIOS region (0x00800000-0x00ffffff) is read-write. FREG2: Management Engine region (0x00001000-0x007fffff) is read-write. OK. Found Winbond flash chip "W25Q128.V" (16384 kB, SPI) mapped at physical address 0x00000000ff000000. Reading ich descriptor... done. Couldn't parse the descriptor! ~ ❯ sudo flashrom -p internal -c "W25Q128.V" \\ --ifd -i bios \\ -w \_\_"/mnt/win2/123 tranqueiras/FPTW/HNX99TF5050.rom"\_\_ \\ -o /tmp/flashrom\_debug.log && cat /tmp/flashrom\_debug.log flashrom v1.7.0 (git:v1.7.0) on Linux 6.18.31-1-cachyos-lts (x86\_64) flashrom is free software, get the source code at [https://flashrom.org](https://flashrom.org/) Found chipset "Intel C610/X99 (Wellsburg)". This chipset is marked as untested. If you are using an up-to-date version of flashrom \*and\* were (not) able to successfully update your firmware with it, then please email a report to flashrom@flashrom.org including a verbose (-V) log. Thank you! Enabling flash write... Warning: BIOS region SMM protection is enabled! Warning: Setting BIOS Control at 0xdc from 0x2a to 0x09 failed. New value is 0x2a. SPI Configuration is locked down. FREG0: Flash Descriptor region (0x00000000-0x00000fff) is read-write. FREG1: BIOS region (0x00800000-0x00ffffff) is read-write. FREG2: Management Engine region (0x00001000-0x007fffff) is read-write. OK. Found Winbond flash chip "W25Q128.V" (16384 kB, SPI) mapped at physical address 0x00000000ff000000. Reading ich descriptor... done. Couldn't parse the descriptor! ~ ❯

---

<iframe title="internal://deep-research" src="https://connector_openai_deep_research.web-sandbox.oaiusercontent.com/?app=chatgpt&amp;darkModeType=increased&amp;locale=pt-BR&amp;deviceType=desktop" allow="camera *; clipboard-read *; clipboard-write *; fullscreen *; local-network-access *; microphone *; web-share *" allowfullscreen=""></iframe>

---

**Você disse**

so quero gravar

---

<iframe title="internal://deep-research" src="https://connector_openai_deep_research.web-sandbox.oaiusercontent.com/?app=chatgpt&amp;darkModeType=increased&amp;locale=pt-BR&amp;deviceType=desktop" allow="camera *; clipboard-read *; clipboard-write *; fullscreen *; local-network-access *; microphone *; web-share *" allowfullscreen=""></iframe>

---

**Você disse**

---

<iframe title="internal://deep-research" src="https://connector_openai_deep_research.web-sandbox.oaiusercontent.com/?app=chatgpt&amp;darkModeType=increased&amp;locale=pt-BR&amp;deviceType=desktop" allow="camera *; clipboard-read *; clipboard-write *; fullscreen *; local-network-access *; microphone *; web-share *" allowfullscreen=""></iframe>

---

**Você disse**

---

<iframe title="internal://deep-research" src="https://connector_openai_deep_research.web-sandbox.oaiusercontent.com/?app=chatgpt&amp;darkModeType=increased&amp;locale=pt-BR&amp;deviceType=desktop" allow="camera *; clipboard-read *; clipboard-write *; fullscreen *; local-network-access *; microphone *; web-share *" allowfullscreen=""></iframe>

---

**Você disse**

~ ❯ sudo flashrom -p internal -c "W25Q128.V" \\ --ifd -i bios --noverify-all \\ -w "/mnt/win2/123 tranqueiras/FPTW/HNX99TF5050.rom" \[sudo\] senha para johncoffee: flashrom v1.7.0 (git:v1.7.0) on Linux 6.18.31-1-cachyos-lts (x86\_64) flashrom is free software, get the source code at [https://flashrom.org](https://flashrom.org/) Found chipset "Intel C610/X99 (Wellsburg)". This chipset is marked as untested. If you are using an up-to-date version of flashrom \*and\* were (not) able to successfully update your firmware with it, then please email a report to flashrom@flashrom.org including a verbose (-V) log. Thank you! Enabling flash write... Warning: BIOS region SMM protection is enabled! Warning: Setting BIOS Control at 0xdc from 0x2a to 0x09 failed. New value is 0x2a. SPI Configuration is locked down. FREG0: Flash Descriptor region (0x00000000-0x00000fff) is read-write. FREG1: BIOS region (0x00800000-0x00ffffff) is read-write. FREG2: Management Engine region (0x00001000-0x007fffff) is read-write. OK. Found Winbond flash chip "W25Q128.V" (16384 kB, SPI) mapped at physical address 0x00000000ff000000. Reading ich descriptor... done. Couldn't parse the descriptor! ~ ❯ sudo flashrom -p internal -c "W25Q128.V" \\ --ifd -i bios \\ -w "/mnt/win2/123 tranqueiras/FPTW/HNX99TF5050.rom" \\ -o /tmp/flashrom\_debug.log && cat /tmp/flashrom\_debug.log flashrom v1.7.0 (git:v1.7.0) on Linux 6.18.31-1-cachyos-lts (x86\_64) flashrom is free software, get the source code at [https://flashrom.org](https://flashrom.org/) Found chipset "Intel C610/X99 (Wellsburg)". This chipset is marked as untested. If you are using an up-to-date version of flashrom \*and\* were (not) able to successfully update your firmware with it, then please email a report to flashrom@flashrom.org including a verbose (-V) log. Thank you! Enabling flash write... Warning: BIOS region SMM protection is enabled! Warning: Setting BIOS Control at 0xdc from 0x2a to 0x09 failed. New value is 0x2a. SPI Configuration is locked down. FREG0: Flash Descriptor region (0x00000000-0x00000fff) is read-write. FREG1: BIOS region (0x00800000-0x00ffffff) is read-write. FREG2: Management Engine region (0x00001000-0x007fffff) is read-write. OK. Found Winbond flash chip "W25Q128.V" (16384 kB, SPI) mapped at physical address 0x00000000ff000000. Reading ich descriptor... done. Couldn't parse the descriptor! ~ ❯ flashrom -p internal -c W25Q128.V -i bios -w HNX99TF5050.rom -V -v -o flash.log flashrom v1.7.0 (git:v1.7.0) on Linux 6.18.31-1-cachyos-lts (x86\_64) flashrom is free software, get the source code at [https://flashrom.org](https://flashrom.org/) More than one operation specified. Aborting. Please run "flashrom --help" for usage info. ~ ❯

---

<iframe title="internal://deep-research" src="https://connector_openai_deep_research.web-sandbox.oaiusercontent.com/?app=chatgpt&amp;darkModeType=increased&amp;locale=pt-BR&amp;deviceType=desktop" allow="camera *; clipboard-read *; clipboard-write *; fullscreen *; local-network-access *; microphone *; web-share *" allowfullscreen=""></iframe>