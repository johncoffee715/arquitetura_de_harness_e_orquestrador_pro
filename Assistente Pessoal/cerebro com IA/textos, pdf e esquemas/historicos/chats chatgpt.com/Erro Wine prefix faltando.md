---
title: "Erro Wine prefix faltando"
source: "https://chatgpt.com/c/68e94500-d64c-8323-bdeb-d21219db5dd5"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 2 messages"
tags:
  - "clippings"
---
**Você disse**

Traceback (most recent call last): File "/usr/lib/python3.13/site-packages/lutris/exception\_backstops.py", line 79, in error\_wrapper return handler(\*args, \*\*kwargs) File "/usr/lib/python3.13/site-packages/lutris/gui/widgets/game\_bar.py", line 266, in on\_link\_button\_clicked callback(button) ~~~~~~~~^^^^^^^^ File "/usr/lib/python3.13/site-packages/lutris/runners/wine.py", line 920, in run\_wineconsole self.\_run\_executable("wineconsole") ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^ File "/usr/lib/python3.13/site-packages/lutris/runners/wine.py", line 898, in \_run\_executable wineexec( ~~~~~~~~^ executable, ^^^^^^^^^^^...<5 lines>... runner=self, ^^^^^^^^^^^^ ) ^ File "/usr/lib/python3.13/site-packages/lutris/runners/commands/wine.py", line 321, in wineexec create\_prefix(prefix, wine\_path=wine\_bin, arch=arch, runner=runner) ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ File "/usr/lib/python3.13/site-packages/lutris/runners/commands/wine.py", line 105, in create\_prefix raise ValueError("No Wine prefix path given") ValueError: No Wine prefix path given Lutris log: \[INFO:2025-10-10 14:28:44,160:application\]: Starting Lutris 0.5.19 \[INFO:2025-10-10 14:28:44,316:startup\]: "card1" is AMD Radeon Pro VII (1002:66a1 1002:081e amdgpu) Driver 25.2.4 \[ERROR:2025-10-10 14:28:44,322:system\]: \['vulkaninfo', '--summary'\] command failed: Command '\['vulkaninfo', '--summary'\]' returned non-zero exit status 1. \[INFO:2025-10-10 14:28:44,342:startup\]: "card0" is NVIDIA Corporation GK208B \[GeForce GT 710\] (10de:128b 10de:118b nouveau) Driver 25.2.4 \[WARNING:2025-10-10 14:29:13,059:system\]: Non existent path: /home/johncoffee/.local/share/lutris/runners/proton/ge-proton \[INFO:2025-10-10 14:36:06,449:game\_common\]: Creating new configuration with runner wine \[WARNING:2025-10-10 14:36:09,315:runner\]: Accessing game config while runner wasn't given one. \[WARNING:2025-10-10 14:36:09,321:runner\]: Accessing game config while runner wasn't given one. \[ERROR:2025-10-10 14:36:09,321:wine\]: The game doesn't have an executable \[ERROR:2025-10-10 14:38:36,361:game\]: The game 'the crew' has no ID, it is not stored in the database. \[ERROR:2025-10-10 14:39:29,174:exception\_backstops\]: Error handling signal 'clicked': No Wine prefix path given Traceback (most recent call last): File "/usr/lib/python3.13/site-packages/lutris/exception\_backstops.py", line 79, in error\_wrapper return handler(\*args, \*\*kwargs) File "/usr/lib/python3.13/site-packages/lutris/gui/widgets/game\_bar.py", line 266, in on\_link\_button\_clicked callback(button) ~~~~~~~~^^^^^^^^ File "/usr/lib/python3.13/site-packages/lutris/runners/wine.py", line 920, in run\_wineconsole self.\_run\_executable("wineconsole") ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^ File "/usr/lib/python3.13/site-packages/lutris/runners/wine.py", line 898, in \_run\_executable wineexec( ~~~~~~~~^ executable, ^^^^^^^^^^^...<5 lines>... runner=self, ^^^^^^^^^^^^ ) ^ File "/usr/lib/python3.13/site-packages/lutris/runners/commands/wine.py", line 321, in wineexec create\_prefix(prefix, wine\_path=wine\_bin, arch=arch, runner=runner) ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ File "/usr/lib/python3.13/site-packages/lutris/runners/commands/wine.py", line 105, in create\_prefix raise ValueError("No Wine prefix path given") ValueError: No Wine prefix path given \[ERROR:2025-10-10 14:39:48,226:exception\_backstops\]: Error handling signal 'clicked': No Wine prefix path given Traceback (most recent call last): File "/usr/lib/python3.13/site-packages/lutris/exception\_backstops.py", line 79, in error\_wrapper return handler(\*args, \*\*kwargs) File "/usr/lib/python3.13/site-packages/lutris/gui/widgets/game\_bar.py", line 266, in on\_link\_button\_clicked callback(button) ~~~~~~~~^^^^^^^^ File "/usr/lib/python3.13/site-packages/lutris/runners/wine.py", line 920, in run\_wineconsole self.\_run\_executable("wineconsole") ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^ File "/usr/lib/python3.13/site-packages/lutris/runners/wine.py", line 898, in \_run\_executable wineexec( ~~~~~~~~^ executable, ^^^^^^^^^^^...<5 lines>... runner=self, ^^^^^^^^^^^^ ) ^ File "/usr/lib/python3.13/site-packages/lutris/runners/commands/wine.py", line 321, in wineexec create\_prefix(prefix, wine\_path=wine\_bin, arch=arch, runner=runner) ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ File "/usr/lib/python3.13/site-packages/lutris/runners/commands/wine.py", line 105, in create\_prefix raise ValueError("No Wine prefix path given") ValueError: No Wine prefix path given

---

Beleza. O erro é **claríssimo**:

> `ValueError: No Wine prefix path given`  
> O Lutris tentou rodar o *wineconsole* (ou o jogo), **mas não há prefixo configurado**.  
> Sem `WINEPREFIX`, o Lutris não sabe onde criar ou usar o ambiente do jogo (o “C:\\fake Windows”).

Vamos direto ao ponto:

---

### 🧩 CAUSA

O Lutris não tem um **Wine prefix configurado** para o jogo “The Crew”.  
Isso acontece quando:

1. O jogo foi adicionado manualmente, mas você não escolheu o runner “Wine” com prefixo.
2. A instalação do jogo falhou ou foi apagada.
3. O campo “Executable” do jogo está vazio.
4. O runner “Wine/Proton” não está corretamente instalado (veja o aviso `Non existent path: .../proton/ge-proton`).

---

### ⚙️ SOLUÇÃO RÁPIDA

1. **Abra o Lutris.**
2. Clique com **botão direito no “The Crew” → Configurar.**
3. Vá até a aba **“Runner options”**:
	- Runner: `Wine`
		- **Wine version:** escolha uma instalada (ex: `lutris-GE-Proton8-25` ou `system`)
		- **Wine prefix:** defina um caminho válido, por exemplo:
		```
		/home/johncoffee/Games/the-crew
		```
		ou
		```
		/home/johncoffee/.wine-thecrew
		```
4. Vá na aba **“Game options”**:
	- **Executable:** selecione o `.exe` real do jogo (ex: `TheCrew.exe` dentro da pasta do jogo).
		- **Working directory:** coloque a pasta onde o `.exe` está.
5. Clique em **Salvar** e **Executar novamente.**

---

### 🚀 DICA EXTRA

Se o Wine prefix ainda **não existir**, você pode criá-lo manualmente antes de abrir o Lutris:

```bash
WINEPREFIX=~/.wine-thecrew WINEARCH=win64 wineboot
```

Isso inicializa um prefixo limpo.

---

### ⚠️ CHECAR

Veja se o Lutris reconhece runners instalados:

```bash
lutris -l
```

Se não aparecer nada tipo `lutris-GE-Proton...`, instale um runner GE manualmente:

```bash
lutris -i https://github.com/GloriousEggroll/proton-ge-custom/releases/latest/download/lutris-GE-Proton8-25-x86_64.tar.gz
```

(ajuste o nome conforme a versão disponível)

---

### ✅ RESUMO PRÁTICO

| Problema | Solução direta |
| --- | --- |
| “No Wine prefix path given” | Definir o prefixo válido em “Runner options” |
| “The game doesn’t have an executable” | Escolher o `.exe` correto do jogo |
| “Non existent path: proton/ge-proton” | Instalar o runner GE-Proton correto |

---

Quer que eu te mande um comando shell que **cria o prefixo**, **instala DXVK**, e **configura o Lutris automaticamente** pra The Crew?  
Assim você só copia e cola.