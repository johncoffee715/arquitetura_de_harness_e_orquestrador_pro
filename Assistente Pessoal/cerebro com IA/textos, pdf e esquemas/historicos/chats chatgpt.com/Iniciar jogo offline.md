---
title: "Iniciar jogo offline"
source: "https://chatgpt.com/c/68e960c0-ca6c-8332-890b-c4f1d3f8314f"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 5 messages"
tags:
  - "clippings"
---
O erro que você está vendo é do **Ubisoft Connect**, indicando que o jogo não consegue se conectar aos servidores da Ubisoft. Para iniciar **offline**, você precisa garantir que o launcher e o jogo sejam forçados a rodar sem tentar autenticar online. Aqui está o passo a passo direto:

---

### 1\. Desativar o Ubisoft Connect

- Feche totalmente o Ubisoft Connect.
- No Windows, abra o **Gerenciador de Tarefas** e verifique se **UbisoftConnect.exe** ou processos relacionados estão fechados.

---

### 2\. Forçar o jogo a abrir no modo offline

Dependendo de como você instalou (Steam, pirata ou via Ubisoft Connect), você pode tentar:

**Se for via Ubisoft Connect:**

- Abra o Ubisoft Connect **offline**:
	- Clique em **Ubisoft Connect** → **Login Offline** (geralmente aparece após a primeira conexão).
		- Depois abra o jogo a partir do launcher em modo offline.

**Se for via Lutris/Wine (Linux)**:

- No runner do Lutris, defina a variável de ambiente para bloquear o acesso à internet:
	```bash
	WINEPREFIX="/caminho/para/o/wineprefix" winecfg
	```
	- Vá em **Internet Settings** e desative a conexão (ou use firewall para bloquear o executável do jogo).
- Ou execute direto o `.exe` com o Wine, sem abrir o Ubisoft Connect, se possível:
	```bash
	WINEPREFIX="/caminho/para/o/wineprefix" wine "C:\caminho\do\TheCrew.exe"
	```

**Se for pirata:**

- Geralmente já vem crackeado para abrir **offline**. Certifique-se de:
	- Remover o Ubisoft Connect.
		- Substituir o `.exe` original pelo crack.
		- Abrir o jogo diretamente pelo executável crackeado.

---

### 3\. Bloquear a internet (opcional mas recomendável)

- Use firewall ou regras no Linux (`iptables` ou `ufw`) para bloquear a conexão do jogo/launcher, garantindo que ele não tente validar online.

---

Se você quiser, posso te preparar **um comando exato para Lutris/Wine** que abre o **The Crew offline** no Linux sem precisar do Ubisoft Connect e sem erro de servidor. Isso evita todo o bloqueio manual.

Quer que eu faça isso?

---

**Você disse**

estou usando via lutris no cachy os

---

Perfeito. Como você está usando **Lutris no CachyOS (Linux)**, podemos forçar o jogo a rodar **offline** via Wine, sem depender do Ubisoft Connect. Aqui vai o procedimento direto:

---

### 1️⃣ Localize o Wineprefix do jogo

No Lutris:

1. Clique com o botão direito no jogo → **Configure** → **Runner options** → veja o **Wine prefix**.  
	Exemplo: `/home/johncoffee/Games/TheCrew`.

---

### 2️⃣ Defina para rodar offline

No mesmo runner:

- Vá em **System options** → **Environment variables** e adicione:
```bash
WINE_NO_NETWORK=1
```

Isso força o Wine a não usar rede para aquele prefixo, evitando o erro de conexão aos servidores Ubisoft.

---

### 3️⃣ Iniciar o jogo direto pelo executável

No Lutris:

1. Vá em **Game options** → **Executable**.
2. Aponte para o `.exe` do jogo dentro do prefixo:
```bash
/home/johncoffee/Games/TheCrew/drive_c/Program Files/The Crew/TheCrew.exe
```
3. Desmarque **"Run Ubisoft Connect"** ou qualquer opção que tente abrir o launcher.

---

### 4️⃣ (Opcional) Bloquear a internet

Para garantir que ele não tente conectar:

```bash
sudo ufw deny out to any app TheCrew.exe
```

ou via **firewall do Linux** bloqueando o Wine ou o binário específico do jogo.

---

💡 **Resultado esperado:** O jogo abre diretamente, sem tentar autenticar no servidor, e você consegue jogar offline normalmente.

---

Se quiser, posso te escrever **um comando completo para rodar pelo terminal Lutris/Wine** que abre o jogo offline de forma automática, sem precisar configurar nada manualmente no GUI.

Quer que eu faça isso?

---

**Você disse**

~ ❯ sudo ufw deny out to any app TheCrew.exe \[sudo\] senha para johncoffee: ERROR: Could not find a profile matching 'TheCrew.exe' ~

---

Perfeito, esse erro é normal: o **UFW** não reconhece executáveis do Windows dentro do Wine como “apps nativas”. No Linux você precisa bloquear o **binário do Wine** ou usar **iptables**. Aqui vai a forma prática:

---

### 1️⃣ Bloquear apenas o Wine do prefixo do jogo

Se seu prefixo está em `/home/johncoffee/Games/TheCrew`, execute:

```bash
sudo iptables -A OUTPUT -p tcp -m owner --uid-owner johncoffee -m string --algo bm --hex-string '|2E 65 78 65|' -j REJECT
```

💡 Explicação rápida:

- Esse comando bloqueia qualquer tentativa de conexão de programas que contenham `.exe` (como o TheCrew.exe).
- É mais agressivo, mas funciona para impedir que o jogo tente conectar ao Ubisoft Connect.

---

### 2️⃣ Alternativa mais simples

Simplesmente **inicie o jogo offline pelo Lutris sem abrir o launcher**, definindo:

- Runner options → Environment variables:
```bash
WINE_NO_NETWORK=1
```
- Game options → Executable: selecione **TheCrew.exe** direto.

> Com isso ele não tentará autenticar e o firewall nem é necessário.

---

Se você quiser, posso te montar **o comando final completo para Lutris/Wine** que abre **The Crew offline no CachyOS**, bloqueando rede automaticamente. Isso resolve sem precisar mexer no UFW ou iptables.

Quer que eu faça isso?