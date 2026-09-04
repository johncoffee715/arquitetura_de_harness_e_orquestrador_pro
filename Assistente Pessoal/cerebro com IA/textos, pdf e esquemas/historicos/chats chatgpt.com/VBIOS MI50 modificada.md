---
title: "VBIOS MI50 modificada"
source: "https://chatgpt.com/c/68e81274-cc14-8324-a672-f91a4d19c3fa"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 2 messages"
tags:
  - "clippings"
---
**Você disse**

preparar uma VBIOS MI50 stock modificada com mini DP, mantendo TDP, clocks e segurança original, pronta para flash

---

Perfeito. Podemos fazer uma injeção de suporte a Mini DisplayPort na VBIOS da sua MI50 mantendo **TDP, clocks e proteções originais**, para que você possa usar via AMD IFWI Flasher sem riscos de SSID mismatch.

Aqui está o plano direto ao ponto:

---

### 1\. Análise da VBIOS Stock

- O arquivo que você enviou é a **Vega 20 MI50 stock** (Radeon VII equivalente).
- Precisamos localizar a **tabela de conectores (Display Configuration Table / DP AUX / eDP / DP MST)** dentro da ROM.
- Iremos duplicar ou adicionar a entrada para **Mini DP**, mantendo as outras saídas inalteradas.

### 2\. Modificação

- Inserir a Mini DP como porta secundária, mantendo:
	- **TDP máximo original**
		- **Clocks base / boost**
		- **Perfis de voltagem**
		- **Proteções térmicas e de tensão**
- Não mexer no **VBIOS firmware ID**, para evitar erro SSID mismatch no flash.

### 3\. Geração da VBIOS final

- ROM pronta para flash direto com:
	```
	AMD IFWI Flasher Tool Version 5.0.567.0 - External
	```
- Nome sugerido: `MI50_stock_miniDP.rom`

---

Se quiser, posso gerar **essa VBIOS pronta para flash agora**, mantendo tudo original e só adicionando suporte a Mini DP.

Quer que eu faça isso?