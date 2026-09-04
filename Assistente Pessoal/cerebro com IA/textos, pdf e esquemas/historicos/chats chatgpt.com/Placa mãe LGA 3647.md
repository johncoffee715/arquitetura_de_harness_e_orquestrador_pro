---
title: "Placa mãe LGA 3647"
source: "https://chatgpt.com/c/6a024034-6c94-83e9-8898-c452f2054cbf"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 2 messages"
tags:
  - "clippings"
---
**Você disse**

Existe placa mãe pra uso doméstico da liga 3647?

---

Sim. Existem placas-mãe LGA 3647 voltadas pra workstation/HEDT que funcionam perfeitamente em uso “doméstico avançado”, homelab, IA local, virtualização pesada, render, engenharia reversa, etc.

As principais são:

- ASUS [ASUS Pro WS C621-64L SAGE](https://www.asus.com/uk/motherboards-components/motherboards/workstation/pro-ws-c621-64l-sage/?utm_source=chatgpt.com)  
	Uma das mais famosas. Suporta Xeon Scalable e Xeon W-3200. Tem:
	- até 4 GPUs
		- ECC RDIMM/LRDIMM
		- muitos PCIe
		- formato CEB
		- foco workstation real [^1]
- ASUS [ROG Dominus Extreme](https://www.performancesolutions.com.br/placa-mae-asus-rog-dominus-extreme-lga3647?utm_source=chatgpt.com)  
	A mais “doméstica extrema” já feita pra LGA3647.  
	Foi criada pro Xeon W-3175X.  
	Basicamente um monstro HEDT:
	- overclock
		- RGB
		- áudio onboard decente
		- rede 10G
		- VRM absurdo
		- foco enthusiast/workstation [^2]
- Gigabyte [Gigabyte C621 AORUS XTREME](https://www.gigabyte.com/br/Motherboard/C621-AORUS-XTREME-rev-10/sp?utm_source=chatgpt.com)  
	Outra workstation/HEDT absurda:
	- 32 fases VRM
		- OC no Xeon W-3175X
		- 7 PCIe x16
		- áudio onboard estilo gamer
		- visual AORUS [^3]

Agora a realidade nua e crua:

- LGA3647 NÃO virou plataforma doméstica mainstream.
- O custo das placas é o problema, não os Xeons.
- Xeon Gold/Silver hoje são baratos.
- As motherboards continuam caras e raras. [^4]

Pra você, tecnicamente, faz muito sentido se quiser:

- laboratório IA local
- múltiplas GPUs
- PCIe lanes absurdas
- ECC massivo
- virtualização
- passthrough
- servidores híbridos workstation
- engenharia reversa pesada

Mas tem pegadinhas:

| Problema | Impacto |
| --- | --- |
| Consumo elétrico | Muito alto |
| Tamanho | EEB/CEB gigantes |
| Cooler | LGA3647 usa fixação específica |
| BIOS | Às vezes chata com ES/QS |
| RAM | Muitas usam ECC Registered |
| Gabinete | Nem ATX comum serve |
| VRM/PSU | Precisa fonte séria |

Pra teu perfil técnico, eu diria:

- Se quiser custo-benefício brutal → dual Xeon LGA3647 usado + Linux + Proxmox + GPUs datacenter.
- Se quiser workstation “quase gamer” extrema → Dominus Extreme ou C621 AORUS.
- Se quiser equilíbrio profissional → ASUS WS C621 Sage.

Hoje, honestamente, muita gente migra pra:

- Threadripper Pro
- EPYC SP3
- AM5 Ryzen 7950X/9950X

Porque entregam:

- menos consumo
- mais compatibilidade
- placas mais fáceis
- melhor single-thread

Mas em PCIe lanes + ECC + homelab bruto, LGA3647 ainda é um animal.

[^1]: [asus.com](https://www.asus.com/uk/motherboards-components/motherboards/workstation/pro-ws-c621-64l-sage/?utm_source=chatgpt.com)

[^2]: [performancesolutions.com.br](https://www.performancesolutions.com.br/placa-mae-asus-rog-dominus-extreme-lga3647?utm_source=chatgpt.com)

[^3]: [gigabyte.com](https://www.gigabyte.com/br/Motherboard/C621-AORUS-XTREME-rev-10/sp?utm_source=chatgpt.com)

[^4]: [reddit.com](https://www.reddit.com/r/homelab/comments/1suzl0j/motherboard_for_xeon_gold/?utm_source=chatgpt.com)