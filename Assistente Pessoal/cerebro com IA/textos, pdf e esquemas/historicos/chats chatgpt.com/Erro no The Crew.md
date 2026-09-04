---
title: "Erro no The Crew"
source: "https://chatgpt.com/c/68e93fbb-ed88-8330-bbea-8b6c60a815c8"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 8 messages"
tags:
  - "clippings"
---
**Você disse**

Não estou conseguindo entrar no jogo the crew via heroic

---

Beleza. A mensagem da imagem mostra:

> **"Falha ao iniciar o jogo! Você ainda não instalou o Uplay PC ou ele não está funcionando corretamente."**

Isso significa que o **The Crew (via Heroic Games Launcher)** não está conseguindo encontrar o **Ubisoft Connect (antigo Uplay)** dentro do prefixo Wine/Proton que o Heroic usa.

Vamos resolver de forma direta 👇

---

### ⚙️ ETAPAS PARA CORRIGIR

#### 1\. Feche o Heroic

Saia completamente do Heroic (não apenas minimize).

---

#### 2\. Localize o prefixo do jogo

O caminho padrão (no Linux) é:

```
~/.var/app/com.heroicgameslauncher.hgl/config/heroic/tools/wine/prefixes/
```

ou

```
~/.config/heroic/tools/wine/prefixes/
```

Dentro dessa pasta haverá uma subpasta com o nome do jogo ou com o ID dele (ex: `The Crew`).

---

#### 3\. Baixe o instalador do Ubisoft Connect

Baixe direto de:  
👉 [https://ubisoftconnect.com](https://ubisoftconnect.com/)

O arquivo será algo como:

```
UbisoftConnectInstaller.exe
```

---

#### 4\. Instale o Ubisoft Connect dentro do prefixo

Abra um terminal e rode:

```bash
flatpak run com.heroicgameslauncher.hgl --wine "wine path/do/UbisoftConnectInstaller.exe"
```

> (ou substitua `path/do/...` pelo caminho onde baixou o instalador)

Isso vai instalar o Ubisoft Connect dentro do mesmo ambiente Wine que o Heroic usa.

---

#### 5\. Verifique se ele inicia

Após instalado, execute:

```bash
flatpak run com.heroicgameslauncher.hgl --wine "wine 'C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\UbisoftConnect.exe'"
```

Se o launcher abrir e logar normalmente, tá certo.

---

#### 6\. Reabra o Heroic e inicie o jogo

Agora o The Crew deve detectar automaticamente o Ubisoft Connect e abrir normalmente.

---

### 🔧 Caso ainda falhe:

Abra as configurações do jogo no Heroic → vá em **Wine Settings → Environment Variables** e adicione:

```
UBISOFT_CONNECT_PATH=C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\
```

---

Se quiser, me diga:

- Qual distro você está usando (ex: CachyOS, Garuda, etc.)
- Se o jogo foi instalado via **Epic Games**, **Ubisoft** ou **Steam dentro do Heroic**

Aí posso te passar o comando exato e prefixo certo.

---

**Você disse**

jogo abre mas nao exibe imagem apenas audio

---

Beleza, John.  
O cenário está **90 % resolvido**, só falta alinhar o runner correto e confirmar que o DXVK está realmente sendo usado.

Resumo do que vimos:

- ✅ Prefixo `/mnt/disk2/games/The Crew` está correto.
- ✅ DXVK já está instalado (`dxgi.dll` presente).
- ⚠️ Mas: não existe runner chamado **lutris-GE-Proton9-5** — o que tu tens é  
	`wine-ge-8-26-x86_64` e `wine-10.16-staging-tkg-amd64`.  
	Ou seja, o Wine que o Lutris está rodando é **outro**.

---

## ⚙️ Ajuste imediato

### 1️⃣ Identifica qual Wine o The Crew usa

No Lutris:

> Clica **com o botão direito** no jogo → **Configurar → Runner options**  
> Em **Wine version**, escolhe:
> 
> ```
> wine-ge-8-26-x86_64
> ```
> 
> (ou se quiser testar: `wine-10.16-staging-tkg-amd64`)

Depois **salva**.

---

### 2️⃣ Instala DXVK com o mesmo Wine do runner

Como o runner é o `wine-ge-8-26-x86_64`, roda:

```bash
WINEPREFIX="/mnt/disk2/games/The Crew" \
env WINE="$HOME/.local/share/lutris/runners/wine/wine-ge-8-26-x86_64/bin/wine" \
winetricks -q dxvk
```

Se aparecer “Executing w\_do\_call dxvk” → instalado com sucesso.

---

### 3️⃣ Confirma se o DXVK carregou

Executa o jogo pelo Lutris e **olha o terminal** (roda com depuração):

```bash
WINEPREFIX="/mnt/disk2/games/The Crew" lutris -d
```

Procura linha semelhante a:

```
info:  DXVK: v2.x (RADV VEGA20)
```

Se aparecer isso, **DXVK inicializou** → imagem deve aparecer.

---

### 4️⃣ Se ainda tiver áudio sem vídeo

Força o uso do Vulkan renderer:

```bash
WINEPREFIX="/mnt/disk2/games/The Crew" \
wine reg add "HKCU\Software\Wine\Direct3D" /v Renderer /t REG_SZ /d vulkan /f
```

---

### 5️⃣ (Opcional) Testa o outro runner

Se o `wine-ge-8-26-x86_64` não der vídeo, testa:

```bash
WINEPREFIX="/mnt/disk2/games/The Crew" \
env WINE="$HOME/.local/share/lutris/runners/wine/wine-10.16-staging-tkg-amd64/bin/wine" \
winetricks -q dxvk
```

e depois muda o runner no Lutris pra `wine-10.16-staging-tkg-amd64`.

---

Depois de testar, me confirma:

- qual runner ficou ativo no Lutris,
- se apareceu a linha “DXVK: v…” no log.

Aí eu te passo o ajuste final (env vars de otimização específicas pra MI50).

---

**Você disse**

deu erro

---

Perfeito — isso confirma que **o DXVK e o Gamescope estão funcionando** (vide overlay no canto esquerdo), mas o erro vem do **Uplay (Ubisoft Connect)**, que não foi detectado dentro do prefixo Wine do jogo.

---

### 🧩 Causa

O executável do *The Crew* tenta abrir o **Ubisoft Connect** via caminho do Windows, mas o cliente **não está instalado dentro do mesmo prefixo** (`/mnt/disk2/games/The Crew`).

Sem ele, o jogo aborta logo no início.

---

## ⚙️ Solução direta

### 1️⃣ Baixar o instalador do Ubisoft Connect

Baixe o `.exe` oficial:

```bash
cd ~/Downloads
wget https://ubisoftconnect.com/UbisoftConnectInstaller.exe
```

---

### 2️⃣ Instalar dentro do mesmo prefixo

Executa o instalador **usando o mesmo runner e prefixo** do jogo:

```bash
WINEPREFIX="/mnt/disk2/games/The Crew" \
env WINE="$HOME/.local/share/lutris/runners/wine/wine-ge-8-26-x86_64/bin/wine" \
wine ~/Downloads/UbisoftConnectInstaller.exe
```

Durante a instalação:

- **não altere o caminho** (deixe em `C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher`)
- **desmarque** opções de abrir o cliente ao final (para evitar conflito).

---

### 3️⃣ Verifique se foi instalado

Deve existir a pasta:

```
/mnt/disk2/games/The Crew/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/
```

E dentro dela o arquivo `upc.exe`.

---

### 4️⃣ Rodar o Ubisoft Connect manualmente (primeira vez)

Antes de abrir o jogo:

```bash
WINEPREFIX="/mnt/disk2/games/The Crew" \
wine "C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\upc.exe"
```

Logue com sua conta Ubisoft, feche o cliente, e depois abra o The Crew pelo Lutris.

---

### 5️⃣ Se o Lutris não detectar automaticamente o Uplay

Abra o menu do jogo no Lutris → **Configurar → Game options → Executable**

E aponta manualmente para:

```
/mnt/disk2/games/The Crew/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/upc.exe
```

---

### 6️⃣ Teste final

Depois disso, ao abrir pelo Lutris:

- o Ubisoft Connect deve iniciar,
- sincronizar o jogo,
- e finalmente o The Crew abrir com imagem + áudio.

---

Quer que eu monte o script automático para reinstalar o Ubisoft Connect dentro do prefixo (sem precisar digitar tudo)?  
Posso gerar um `.sh` pronto só pra colar e rodar.

---

**Você disse**

mas o jogo e pirata

---

Entendido, John — mas **não posso te orientar em nada que envolva pirataria ou uso de software crackeado** (isso inclui ativar, contornar DRM, ou rodar versões não licenciadas).

👉 **Foco técnico legal:** o erro em si mostra apenas que o jogo tenta chamar o *launcher* da Ubisoft e não o encontra.  
Mesmo sem entrar no mérito de “versão”, o problema é **ausência do launcher que o executável referencia**.

Se tua intenção é **testar o funcionamento do DXVK / Gamescope / Wine** (parte técnica), podemos:

1. **Usar outro jogo gratuito e legal** pra validar a pipeline DXVK (ex.: *Warframe*, *Path of Exile*, *Unturned*, *World of Tanks Blitz* — todos via Lutris/Steam).
2. **Simular o mesmo engine** (AnvilNext da Ubisoft) com *Assassin’s Creed II Demo* — gratuito e roda com o mesmo comportamento técnico, ideal pra debugar o ambiente Wine.
3. **Rodar o executável do The Crew** apenas em modo offline isolado (sem login), se for pra estudo de compatibilidade de DXVK, sem instruções de ativação ou bypass.

Quer que eu te monte um ambiente DXVK/Wine estável com um desses jogos grátis (pra validar desempenho, imagem e Vulkan) — mantendo o mesmo prefixo e runner que usaste agora?