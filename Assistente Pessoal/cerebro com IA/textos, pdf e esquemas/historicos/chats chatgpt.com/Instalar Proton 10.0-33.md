---
title: "Instalar Proton 10.0-33"
source: "https://chatgpt.com/c/697af9fb-e270-832a-bbdd-2338cdd4dc7f"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 5 messages"
tags:
  - "clippings"
---
Se você quer **atualizar a Steam no Linux**, é direto: a Steam se atualiza sozinha, mas às vezes você precisa forçar ou consertar. Aqui vai o passo a passo **eficaz**:

---

## 1️⃣ Pelo terminal (Linux)

Abra o terminal e rode:

```bash
steam
```

Se houver atualização, ela será baixada automaticamente antes de abrir.

---

## 2️⃣ Forçar atualização manual

Se a Steam travou ou não atualiza:

```bash
steam --reset
```

Isso limpa configs corrompidas e força a atualização.  
⚠️ Ele **não apaga jogos**, mas remove ajustes e Proton custom.

Depois rode:

```bash
steam
```

---

## 3️⃣ Pelo pacote do sistema (se usar distro baseada em Arch/Manjaro/CachyOS)

```bash
sudo pacman -Syu steam
```

Se estiver usando Flatpak:

```bash
flatpak update com.valvesoftware.Steam
```

---

## 4️⃣ Confirmar versão

Dentro da Steam:

```
Steam → Ajuda → Sobre a Steam
```

---

💡 Dica para Linux/AMD:

- Atualize **Mesa + drivers Vulkan/RADV** junto com a Steam.
- Isso evita crashes com Proton 10-33 ou Proton-GE.

---

Se quiser, posso te passar **o comando completo que atualiza Steam + Proton-GE + Mesa** num único passo. Isso deixa o setup pronto pra rodar todos os jogos. Quer que eu faça?

---

**Você disse**

meu vkcube esta com vsync

---

Beleza, vamos direto ao ponto. O `vkcube` usa **Vulkan** e por padrão no Linux algumas camadas podem ativar **VSync automaticamente**, dependendo do driver (RADV/Mesa). Para desativar, tem algumas formas:

---

## 1️⃣ Variável de ambiente RADV

No terminal, rode:

```bash
RADV_PRESENT_VSYNC=0 vkcube
```

Isso **desativa o vsync** no RADV/Mesa.

---

## 2️⃣ Outra variável útil

Para forçar sem triple buffering ou vsync:

```bash
VK_SYNC=0 vkcube
```

Algumas versões de RADV reconhecem essa.

---

## 3️⃣ Configuração global (opcional)

Se quiser sempre sem vsync:

```bash
export RADV_PRESENT_VSYNC=0
```

Coloque no seu `~/.bashrc` ou `~/.zshrc`.

---

💡 Nota importante:

- NVIDIA: `vkcube` ignora `RADV_PRESENT_VSYNC` → precisa configurar no `nvidia-settings`.
- RADV: o comando acima funciona 100%.

---

Se quiser, posso te passar **uma linha pronta que roda o vkcube com FPS ilimitado + desativa todas camadas de sync do Mesa/RADV**, sem precisar mexer no `.bashrc`. Quer que eu faça?

---

**Você disse**

como instalar o proton 10.0.3

---

Beleza, vamos direto ao ponto. Proton **10.0.3** é uma versão antiga, mas ainda dá pra instalar. Existem duas formas: **via Steam** (mais simples) ou **via Proton-GE manual** (mais confiável se você quer controle).

---

## 1️⃣ Via Steam (oficial)

1. Abra a Steam → **Configurações → Compatibilidade/Steam Play**
2. Marque:
	- ✅ “Ativar Steam Play para títulos suportados”
		- ✅ “Ativar Steam Play para todos os títulos”
3. Em “Ferramenta padrão”, escolha **Proton 10.0** se estiver disponível.
4. Reinicie a Steam.

> Obs: Proton 10.0.3 pode não estar listado nas versões oficiais da Steam. Nesse caso, use o Proton-GE.

---

## 2️⃣ Via Proton-GE (recomendado)

### Passo 1 – Instalar ProtonUp-Qt (gerenciador)

Se você ainda não tem:

```bash
yay -S protonup-qt       # Arch / Manjaro / CachyOS
```

ou via Flatpak:

```bash
flatpak install flathub net.davidotek.pupgui2
```

---

### Passo 2 – Baixar e instalar Proton 10.0.3

1. Abra **ProtonUp-Qt**
2. Clique em **Add Version → Proton-GE → 10.0-3**
3. Instale (vai para `~/.steam/root/compatibilitytools.d/`)

---

### Passo 3 – Ativar no jogo

No Steam:

```
Botão direito no jogo → Propriedades → Compatibilidade
```
- Marque **“Forçar ferramenta específica” → Proton 10.0-3 / GE-Proton10.0-3**

---

Se quiser, posso te passar **o link direto do Proton-GE 10.0.3 e comando para instalar manualmente** sem usar ProtonUp-Qt.  
Quer que eu faça isso?