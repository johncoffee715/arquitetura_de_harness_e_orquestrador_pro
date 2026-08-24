---
title: "Comando para atualizar Heroic"
source: "https://chatgpt.com/c/69ee1a14-2700-83e9-a9e5-743187eebe3c"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 2 messages"
tags:
  - "clippings"
---
**Você disse**

preciso de comando via termianal para essa atualizaçao: https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher/releases/tag/v2.21.0

---

Direto ao ponto — 3 formas via terminal pra atualizar o **Heroic 2.21.0** (escolhe conforme como você instalou):

---

## ✅ 1. Flatpak (RECOMENDADO)

Se instalou via Flathub:

```bash
flatpak update com.heroicgameslauncher.hgl
```

Ou atualizar tudo:

```bash
flatpak update
```

Se quiser forçar reinstalação limpa (resolve bug):

```bash
flatpak install --reinstall com.heroicgameslauncher.hgl
```

👉 Esse é o método mais estável no Linux [^1]

---

## ⚡ 2. AppImage (manual – mais controle)

Baixa direto a v2.21.0:

```bash
wget https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher/releases/download/v2.21.0/Heroic-2.21.0.AppImage
chmod +x Heroic-2.21.0.AppImage
./Heroic-2.21.0.AppImage
```

👉 Não instala no sistema, roda direto (ideal pra testes/mods)

---

## ⚙️ 3. Arch / CachyOS (teu caso provável)

Se estiver usando AUR:

```bash
yay -Syu heroic-games-launcher-bin
```

ou:

```bash
paru -Syu heroic-games-launcher-bin
```

⚠️ Importante: pacote `heroic-games-launcher` antigo pode estar morto — usa o `-bin` [^2]

---

## 🔧 Diagnóstico rápido (se não atualizar)

Roda:

```bash
heroic --version
```

Se não bater com `2.21.0`, você está em outro método de instalação (conflito comum).

---

## 🔥 Insight (nível engenharia)

Evita misturar:

- Flatpak + AUR + AppImage ao mesmo tempo

Escolhe **1 só**, senão:

- conflito de PATH
- duplicidade de libs (Wine/Proton)
- comportamento inconsistente (já vi isso quebrar launcher)

---

Se quiser, me manda:

```bash
which heroic
```

ou

```bash
flatpak list | grep heroic
```

que eu te digo exatamente onde tá instalado e otimizo teu setup (inclusive Wine/Proton alinhado com tua MI50).

[^1]: [github.com](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher/wiki/Linux-Quick-Start-Guide?utm_source=chatgpt.com)

[^2]: [discuss.cachyos.org](https://discuss.cachyos.org/t/updating-heroic-games-launcher/28350?utm_source=chatgpt.com)