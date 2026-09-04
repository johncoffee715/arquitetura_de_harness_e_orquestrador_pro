---
title: "Engenharia reversa AMD Radeon MI50"
source: "https://claude.ai/chat/edb8f221-7cd0-4d1b-8231-9b779e76f9bc"
author:
published:
created: 2026-07-17
description: "Claude is Anthropic's AI, built for problem solvers. Tackle complex challenges, analyze data, write code, and think through your hardest work."
tags:
  - "clippings"
---
**You**

~ ❯ # Backup do pp\_table actual sudo cp /sys/class/drm/card1/device/pp\_table /tmp/pp\_orig.bin # Patch: activa ODFeatureCapabilities 0 (SCLK limits) e 2 (MCLK max) upp -p /tmp/pp\_orig.bin patch \\ -s 'OverDrive8Table/ODFeatureCapabilities\[0\]:1' \\ -s 'OverDrive8Table/ODFeatureCapabilities\[2\]:1' \\ -o /tmp/pp\_patched.bin # Aplica na placa ao vivo sudo tee /sys/class/drm/card1/device/pp\_table < /tmp/pp\_patched.bin > /dev/null # Verifica resultado — deve mostrar SCLK/MCLK ranges cat /sys/class/drm/card1/device/pp\_od\_clk\_voltage \[sudo\] senha para johncoffee: Sinto muito, tente novamente. \[sudo\] senha para johncoffee: Sinto muito, tente novamente. \[sudo\] senha para johncoffee: Usage: upp \[OPTIONS\] COMMAND \[ARGS\]... Try 'upp -h' for help. Error: No such command 'patch'. warning: An error occurred while redirecting file '/tmp/pp\_patched.bin' warning: Path '/tmp/pp\_patched.bin' does not exist OD\_RANGE: ~ ❯

---

**Claude**

`patch` não existe no UPP 0.2.4 — o comando é `set`. Mas vamos direto ao Python que é mais fiável:

---

**You**

~ ❯ bash \[johncoffee@JohnCoffeeDesk ~\]$ sudo python3 ~/Downloads/patch\_pp\_table.py cat /sys/class/drm/card1/device/pp\_od\_clk\_voltage \[sudo\] senha para johncoffee: python3: can't open file '/home/johncoffee/Downloads/patch\_pp\_table.py': \[Errno 2\] No such file or directory OD\_RANGE: \[johncoffee@JohnCoffeeDesk ~\]$ ^C \[johncoffee@JohnCoffeeDesk ~\]$ sudo python3 - << 'EOF' import sys, shutil, hashlib PP = "/sys/class/drm/card1/device/pp\_table" with open(PP, 'rb') as f: d = bytearray(f.read()) shutil.copy2(PP, "/tmp/pp\_backup.bin") pat = bytes(\[0,0,0,0,1,1,0,0,0,0,0,0,0,0,1\]) p = d.find(pat) if p == -1: print("padrão não encontrado"); sys.exit(1) print(f"Padrão @ 0x{p:04X}: {' '.join(f'{d\[p+i\]:02x}' for i in range(15))}") d\[p+0\] = 1 # SCLK limits d\[p+2\] = 1 # MCLK max print(f"Patchado: {' '.join(f'{d\[p+i\]:02x}' for i in range(15))}") with open(PP, 'wb') as f: f.write(d) print("✓ pp\_table actualizado") EOF # Verifica cat /sys/class/drm/card1/device/pp\_od\_clk\_voltage Padrão @ 0x00AC: 00 00 00 00 01 01 00 00 00 00 00 00 00 00 01 Patchado: 01 00 01 00 01 01 00 00 00 00 00 00 00 00 01 ✓ pp\_table actualizado OD\_RANGE: \[johncoffee@JohnCoffeeDesk ~\]$ sudo python3 - << 'EOF' import sys, shutil, hashlib PP = "/sys/class/drm/card1/device/pp\_table" with open(PP, 'rb') as f: d = bytearray(f.read()) shutil.copy2(PP, "/tmp/pp\_backup.bin") pat = bytes(\[0,0,0,0,1,1,0,0,0,0,0,0,0,0,1\]) p = d.find(pat) if p == -1: print("padrão não encontrado"); sys.exit(1) print(f"Padrão @ 0x{p:04X}: {' '.join(f'{d\[p+i\]:02x}' for i in range(15))}") d\[p+0\] = 1 # SCLK limits d\[p+2\] = 1 # MCLK max print(f"Patchado: {' '.join(f'{d\[p+i\]:02x}' for i in range(15))}") with open(PP, 'wb') as f: f.write(d) print("✓ pp\_table actualizado") EOF # Verifica cat /sys/class/drm/card1/device/pp\_od\_clk\_voltage padrão não encontrado OD\_RANGE: \[johncoffee@JohnCoffeeDesk ~\]$ # Verifica os comandos disponíveis primeiro upp --help 2>&1 | grep -E "command|set|patch|Commands" # Se existir 'set': sudo upp -p /sys/class/drm/card1/device/pp\_table set \\ 'OverDrive8Table/ODFeatureCapabilities\[0\]' 1 \\ 'OverDrive8Table/ODFeatureCapabilities\[2\]' 1 - By extracting PowerPlay table from Video ROM image (see extract command) Commands: set Set value to PowerPlay parameter(s). sudo: upp: comando não encontrado \[johncoffee@JohnCoffeeDesk ~\]$

---

**Claude**

O patch das capabilities funcionou ✓ — `01 00 01 00 01 01...` confirma. O `OD_RANGE:` está vazio porque `ODSettingsMax[0]` e `[2]` são 0 — o driver precisa de valores válidos para mostrar os ranges. Precisa de um segundo patch:

---

**You**

preciso de um relatorio em txt desta conversa detalhado

---

**Claude**

520 linhas, 24 KB — cobre tudo da sessão. O relatório inclui:

14 secções organizadas: identificação de hardware, família completa de BIOS, estrutura ATOM binária, PowerPlay table completa, mapa de tensões VRM, processo de OC unlock, análise térmica, benchmarks, patch MOONSHOT, contribuições para a comunidade, itens pendentes, e todos os ficheiros gerados.

Os três ficheiros desta sessão prontos para descarregar:

- `relatorio_sessao_MI50_RE.txt` — este relatório
- `MI50_16GB_VBIOS.md` — documento para o gist do evilJazz
- `MOONSHOT_D3600200-106_MI50patch.rom` — BIOS patchado aguarda flash
- `patch_pp_table.py` — script Python para OC em runtime