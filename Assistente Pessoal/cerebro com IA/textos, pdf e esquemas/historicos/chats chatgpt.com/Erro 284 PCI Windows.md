---
title: "Erro 284 PCI Windows"
source: "https://chatgpt.com/c/69dec4b3-6a60-83e9-b132-2b46ce17d668"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 6 messages"
tags:
  - "clippings"
---
**Você disse**

Microsoft Windows \[versão 10.0.26200.8037\] (c) Microsoft Corporation. Todos os direitos reservados. C:\\Windows\\System32>cd C:\\Users\\John Coffee\\Desktop\\Nova pasta C:\\Users\\John Coffee\\Desktop\\Nova pasta>fptw64 -d FPTw64.exe \[-H|?\] \[-VER\] \[-EXP\] \[-VERBOSE\] \[-Y\] \[-P\] \[-LIST\] \[-I\] \[-F\] \[-ERASE\] \[-VERIFY\] \[-D\] \[-DESC\] \[-BIOS\] \[-ME\] \[-GBE\] \[-PDR\] \[-SAVEMAC\] \[-SAVESXID\] \[-B\] \[-E\] \[-REWRITE\] \[-ADDRESS|A\] \[-LENGTH|L\] \[-FOVS\] \[-CFGGEN\] \[-U\] \[-O\] \[-IN\] \[-N\] \[-ID\] \[-V\] \[-LOCK\] \[-DUMPLOCK\] \[-PSKFILE\] \[-CLOSEMNF\] \[-GRESET\] \[-PAGE\] \[-SPIBAR\] \[-R\] \[-VARS\] \[-COMMIT\] \[-COMPARE\] \[-HASHED\] \[-DISABLEME\] \[-READFPF\] \[-READFPFATTRIB\] \[-COMPAREFPF\] \[-FPFS\] \[-COMMITFPF\] -H|? Displays help screen. -VER Displays version information. -EXP Displays example usage of this tool. -VERBOSE\<file> Display the debug information of the tool. -Y Do NOT prompt when a warning occurs. -P\<file> Specifies a flash part definition file to use. -LIST List all SPI devices supported. -I Displays information about the flash image. -F\<f>\[NoVerify\] Load binary file into flash. "NoVerify" skips verify. -ERASE Erase the contents of flash. -VERIFY\<file> Compare binary file to flash. -D\<file> Dump flash contents to file or "STDOUT". -DESC Load/verify/dump Descriptor region. -BIOS Load/verify/dump BIOS region. -ME Load/verify/dump ME region. -GBE Load/verify/dump GbE region. -PDR Load/verify/dump PDR region. -SAVEMAC Saves the GbE MAC when GbE is being reflashed. -SAVESXID Saves the GbE SSID and SVID when GbE is being reflashed. -B Check to see if the flash part is erased. -E Do NOT erase area before writing to flash. - Press any key to continue - -REWRITE Rewrite the SPI with file data even if flash is identical. -ADDRESS|A\<address> Flash address to load/verify/dump file. -LENGTH|L\<length> Number of bytes to load/verify/dump. -FOVS Displays list of FOVs supported. -CFGGEN Generates an FOV Input File. -U Update Variable. -O\<file> Sets an output file name. -IN\<file> Input param file. -N\<name> Name of variable. -ID\<id> Id of the FOV to be updated. -V\<value> Value for variable. -LOCK\[PDR\] Sets SPI flash region access to Intel recommended values. -DUMPLOCK Dumps the current lock settings to screen. -PSKFILE\<file> PSK key file name. -CLOSEMNF\[NO\] \[PDR\] End of Manufacturing. Details on NO & PDR use -exp option. -GRESET\[NO\] Global reset drives GPIO30 low unless "NO" is provided. -PAGE Pauses the screen when a page of text is reached. -SPIBAR Display the SPI BAR. -R\<name> Read a variable. -VARS Display supported variables. -COMMIT Commit updates to FOVs requiring a FW reset. -COMPARE\<file> Compare variable with expected value filled in a text file. -HASHED Display a variable (from read command) in hashed format. -DISABLEME Disables the ME. -READFPF\<name> Displays an FPF value. -READFPFATTRIB\<name> Displays an FPF Attribute. -COMPAREFPF\<name> Compares an FPF with the value passed in. -FPFS Displays the list of FPFs. -COMMITFPF\<name> Commits the FPFs. Intel (R) Flash Programming Tool. Version: 9.1.10.1000 Copyright (c) 2007 - 2014, Intel Corporation. All rights reserved. Error 200: Invalid parameter value specified by user. Use -? option to see help. C:\\Users\\John Coffee\\Desktop\\Nova pasta> C:\\Users\\John Coffee\\Desktop\\Nova pasta>

---

Erro simples aqui:

```
Error 200: Invalid parameter
```

👉 Você usou:

```
fptw64 -d
```

**Faltou o nome do arquivo de saída.**

---

## ✅ Comando correto

Para fazer dump completo:

```
fptw64 -d backup.bin
```

---

## 🔧 Dumps específicos (melhor prática)

### Só BIOS (mais seguro):

```
fptw64 -bios -d bios.bin
```

### ME:

```
fptw64 -me -d me.bin
```

### Descriptor:

```
fptw64 -desc -d fd.bin
```

---

## ⚠️ Insight importante (X99 chinês)

Na tua plataforma:

👉 muitas placas vêm com:

- **FD lockado**
- ME restrito

Se der erro tipo:

```
Error 26: The host CPU does not have read access
```

👉 significa:

- região protegida
- FPT limitado

---

## 🚀 Estratégia profissional

1. Testa:
```
fptw64 -bios -d bios.bin
```
2. Se funcionar → ok, BIOS liberada
3. Se falhar → esquece FPT → usa CH341A direto

---

## 💡 Dica avançada

Antes de qualquer flash:

```
fptw64 -i
```

Isso mostra:

- regiões
- permissões
- locks

---

## Resumo

✔ Erro foi só sintaxe  
✔ Corrige com nome de arquivo  
✔ Começa dumpando só BIOS

---

Se quiser, posso analisar teu `.rom` e te dizer:

- se tá íntegro
- se bate com layout X99
- se dá pra flashar via FPT ou só externo

Só falar.

---

**Você disse**

C:\\Users\\John Coffee\\Desktop\\Nova pasta>fptw64 -d backup.rom Intel (R) Flash Programming Tool. Version: 9.1.10.1000 Copyright (c) 2007 - 2014, Intel Corporation. All rights reserved. PMXUtil: Error during PMX Call: idrvdll.dll!IDRVInstallDriver(): Failed to start loaded service err: -2146762484 Error 284: Fail to load driver (PCI access for Windows). Tool needs to run with an administrator priviledge account. C:\\Users\\John Coffee\\Desktop\\Nova pasta>

---

Direto: **você não vai conseguir usar esse FPT 9.1 no seu Windows atual.**  
Não é mais questão de comando — é **bloqueio de driver no kernel**.

```
IDRVInstallDriver(): Failed to start loaded service
Error 284
```

👉 o driver `idrvdll.sys` é antigo e o Windows 10/11 bloqueia.

---

## 🔴 Situação real agora

Você já tentou:

- comando correto ✔
- caminho correto ✔

E mesmo assim falhou → **confirmado: bloqueio de driver**

---

## ✅ 3 caminhos que realmente funcionam

### 🔧 OPÇÃO 1 — (rápida, mas meio instável)

Tenta forçar no Windows:

1. Abre **CMD como administrador**
2. Desativa Hyper-V:
```
bcdedit /set hypervisorlaunchtype off
```
3. Reinicia com:
- SHIFT + Reiniciar
- F7 → desabilitar assinatura de driver
4. Tenta de novo:
```
fptw64 -bios -d bios.bin
```

👉 Pode funcionar… mas em 2026, raramente funciona com FPT 9.x

---

### 🧠 OPÇÃO 2 — (correta no Windows moderno)

👉 Usa **FPT versão mais nova (11.x ou 12.x)**

O teu é:

```
9.1.10.1000 (2014)
```

Isso é pré-Skylake → incompatível com segurança atual

✔ versões novas usam driver atualizado  
✔ passam pelo bloqueio do Windows

---

### 💣 OPÇÃO 3 — (nível profissional / zero dor de cabeça)

👉 **Abandona FPT no Windows**

Usa:

#### ✔ WinPE

ou

#### ✔ DOS bootável

Rodando:

```
fpt.exe -bios -d bios.bin
```

→ acesso direto ao hardware  
→ sem bloqueio  
→ funciona sempre

---

## 🚀 Melhor escolha pro teu perfil

Você já:

- usa CH341A
- mexe com SPI direto
- faz engenharia reversa

👉 então esquece FPT

### Caminho ideal:

1. Dump com CH341A
2. Modifica
3. Regrava direto

✔ sem ME lock  
✔ sem BIOS lock  
✔ sem erro 284 nunca mais

---

## ⚠️ Conclusão

✔ Não é erro teu  
✔ Não é permissão  
❌ É incompatibilidade do FPT com Windows moderno

---

## Se quiser avançar nível hard

Posso te guiar em:

- desbloquear FD (flash descriptor)
- extrair BIOS region limpa
- montar imagem híbrida segura pra flash

Só me fala:  
👉 vai insistir no FPT  
ou  
👉 vai partir pro CH341A direto (recomendado)

---

**Você disse**

verifique a minha rom q enviei

---

Análise direta do teu arquivo:

---

## 📦 Estrutura básica

✔ Tamanho:

```
16.777.216 bytes (16MB)
```

👉 compatível com chip **W25Q128** → OK

---

## 🧠 Descriptor (FD)

✔ Assinatura encontrada:

```
5A A5 F0 0F
```

👉 Isso confirma:

- Intel Flash Descriptor presente
- Layout completo (FD + ME + BIOS)

✔ **Imagem completa**, não é só BIOS region

---

## 🧩 UEFI / BIOS

✔ Encontrado:

```
_FVH (Firmware Volume Header)
```

👉 indica:

- BIOS UEFI válida
- estrutura interna consistente

---

## 📊 Integridade geral

✔ Arquivo não está truncado  
✔ Não é dump vazio  
✔ Não está corrompido estruturalmente

⚠️ ~70% FF → normal (áreas não usadas / padding)

---

## ⚠️ Pontos críticos (onde pode dar ruim)

Aqui é onde você precisa pensar como engenheiro:

### 1\. Compatibilidade com tua placa

Esse nome:

```
x99tf_kot / HNX99T8
```

👉 típico de X99 chinês (KOTIN / variante OEM)

**Risco:**

- VRM config diferente
- GPIO map diferente
- ME SKU diferente

---

### 2\. ME Region (ponto sensível)

Não achei string direta de ME (normal em builds compactadas)

👉 mas como tem FD:

- ME está presente
- pode estar incompatível com tua board

---

### 3\. Flash via FPT vs CH341A

Esse arquivo é:  
✔ FULL IMAGE

Se você fizer:

```
fptw64 -f arquivo.bin
```

👉 pode dar:

- erro de permissão (FD lock)
- ou brick se forçar

---

## 🚀 Conclusão prática

✔ Arquivo está **íntegro e válido**  
✔ Estrutura correta para X99  
❌ Não dá pra garantir compatibilidade sem comparar com dump original

---

## 🧠 Caminho profissional (recomendado)

Não faz flash direto.

### Faz isso:

1. Dump da tua BIOS atual (CH341A)
2. Extrai só a BIOS region
3. Injeta nesse arquivo
4. Mantém:
	- FD original
		- ME original

👉 isso elimina 90% do risco de brick

---

## 🔥 Se quiser ir nível hard

Posso te guiar pra:

- identificar offsets exatos (FD / ME / BIOS)
- fazer merge seguro
- desbloquear regiões (caso queira usar FPT depois)

Só manda:  
👉 dump da tua BIOS atual (mesmo que corrompida)

Aí a gente faz engenharia reversa de verdade.