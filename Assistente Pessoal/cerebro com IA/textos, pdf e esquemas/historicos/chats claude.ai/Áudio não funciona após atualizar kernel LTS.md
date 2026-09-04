---
title: "Áudio não funciona após atualizar kernel LTS"
source: "https://claude.ai/chat/8f1b438b-e55c-47ec-ba87-dae805168be2"
author:
published:
created: 2026-07-17
description: "Claude is Anthropic's AI, built for problem solvers. Tackle complex challenges, analyze data, write code, and think through your hardest work."
tags:
  - "clippings"
---
**Claude**

Perfeito — tá lá:

```
00:1b.0 Audio device: Intel Corporation C610/X99 series chipset HD Audio Controller (rev 05)
```

`00:1b.0` de volta no barramento. Tudo certo.

---

**You**

mas to sem audio

---

**Claude**

Provavelmente ainda no kernel 7.0.11 que não tem os drivers HDA. Confirma rápido:

```bash
uname -r
aplay -l
lsmod | grep snd_hda
```

Se `uname -r` retornar `7.0.11-1-cachyos`, o problema é esse — o hardware voltou ao PCI mas o kernel atual não tem o módulo `snd_hda_intel`. Precisa bootar pelo LTS:

```bash
sudo bootctl set-oneshot linux-cachyos-lts.conf
sudo reboot
```

O `set-oneshot` faz bootar pelo LTS só na próxima vez, sem mudar o padrão. Após reiniciar no 6.18.33-lts o áudio deve aparecer automaticamente.

---

**You**

~ ❯ uname -r aplay -l lsmod | grep snd\_hda 7.0.11-1-cachyos aplay: device\_list:279: no soundcards found... snd\_hda\_intel 69632 0 snd\_hda\_codec 233472 1 snd\_hda\_intel snd\_hda\_core 155648 2 snd\_hda\_intel,snd\_hda\_codec snd\_intel\_dspcfg 49152 1 snd\_hda\_intel snd\_hwdep 24576 1 snd\_hda\_codec snd\_pcm 225280 3 snd\_hda\_intel,snd\_hda\_codec,snd\_hda\_core snd 159744 9 snd\_seq,snd\_seq\_device,snd\_hwdep,snd\_hda\_intel,snd\_hda\_codec,snd\_timer,snd\_pcm ~ ❯

---

**Claude**

Bom progresso — o módulo carregou (`snd_hda_intel` presente), mas com **0 usuários**, o que significa que ele inicializou sem conseguir detectar o codec. O hardware está no PCI mas o driver não está "conversando" com ele ainda.

Roda isso:

```bash
sudo journalctl -k --no-pager | grep -iE "hda|codec|azalia|snd" | tail -40
```

```bash
cat /proc/asound/cards
```

E tenta recarregar o módulo forçado:

```bash
sudo modprobe -r snd_hda_intel && sudo modprobe snd_hda_intel
aplay -l
```

A saída do `journalctl` vai mostrar exatamente onde o probe falhou — se é no codec ID, ACPI, ou se simplesmente precisa de um `probe_mask` ou quirk pra esse board.

---

**You**

perfeito subiu:

~ ❯ uname -r aplay -l lsmod | grep snd\_hda 7.0.11-1-cachyos aplay: device\_list:279: no soundcards found... snd\_hda\_intel 69632 0 snd\_hda\_codec 233472 1 snd\_hda\_intel snd\_hda\_core 155648 2 snd\_hda\_intel,snd\_hda\_codec snd\_intel\_dspcfg 49152 1 snd\_hda\_intel snd\_hwdep 24576 1 snd\_hda\_codec snd\_pcm 225280 3 snd\_hda\_intel,snd\_hda\_codec,snd\_hda\_core snd 159744 9 snd\_seq,snd\_seq\_device,snd\_hwdep,snd\_hda\_intel,snd\_hda\_codec,snd\_timer,snd\_pcm ~ ❯ sudo journalctl -k --no-pager | grep -iE "hda|codec|azalia|snd" | tail -40 jun 10 11:33:19 JohnCoffeeDesk kernel: snd\_hda\_intel 0000:00:1b.0: enabling device (0000 -> 0002) jun 10 11:33:19 JohnCoffeeDesk kernel: hdaudio hdaudioC0D0: no AFG or MFG node found jun 10 11:33:19 JohnCoffeeDesk kernel: snd\_hda\_intel 0000:00:1b.0: no codecs initialized ~ ❯ cat /proc/asound/cards --- no soundcards --- ~ ❯ sudo modprobe -r snd\_hda\_intel && sudo modprobe snd\_hda\_intel aplay -l aplay: device\_list:279: no soundcards found... ~ ❯

---

**Claude**

Erro claro agora:

```
hdaudio hdaudioC0D0: no AFG or MFG node found
snd_hda_intel 0000:00:1b.0: no codecs initialized
```

O controlador HDA ligou (`enabling device` ✓), encontrou algo na porta C0D0, mas o **codec não respondeu à enumeração**. Isso quase sempre acontece quando o hardware ficou sem energia por um tempo — um simples reboot não reseta completamente o estado do chip Realtek/Azalia. O módulo tenta conversar com o codec antes dele estar pronto.

**Fix 1 — Cold boot (mais provável de resolver):**

```bash
sudo poweroff
```

Espera 5–10 segundos com a máquina desligada (capacitores descarregam), depois liga. Um `reboot` não corta a alimentação do codec; um `poweroff` + ligar manualmente sim.

---

**Fix 2 — Se ainda falhar após cold boot, ajusta o timing do probe:**

```bash
echo "options snd_hda_intel power_save=0 probe_mask=1" | sudo tee /etc/modprobe.d/snd_hda_intel.conf
sudo modprobe -r snd_hda_intel
sudo modprobe snd_hda_intel
aplay -l
```

O `power_save=0` impede o codec de entrar em sleep durante o probe, e o `probe_mask=1` restringe a busca ao codec interno (evita conflito com o HDMI da MI50).

Tenta o poweroff primeiro.