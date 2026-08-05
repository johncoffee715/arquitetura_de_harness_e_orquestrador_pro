---
title: "Tensões necessárias para vbios"
source: "https://chatgpt.com/c/6909362c-e52c-8325-b47e-1ba90960e263"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 5 messages"
tags:
  - "clippings"
---
Perfeito, John.  
Vamos direto ao ponto técnico. Quando uma GPU (como tua **Radeon Instinct MI50**) não reconhece o VBIOS após várias gravações físicas (dessolda/solda da EEPROM), temos **dois blocos de tensão essenciais** que precisam estar **estáveis e dentro da faixa nominal** antes que o chip SPI (Winbond W25Q128JQ) possa ser lido no *boot strap* da GPU:

---

### ⚡ 1. TENSÕES FUNDAMENTAIS PARA O VBIOS (SPI FLASH)

| Linha | Tensão Nominal | Função | Observações |
| --- | --- | --- | --- |
| **VCC\_SPI** | **3.3 V ±5% (3.25–3.45 V)** | Alimentação principal da EEPROM | Deve vir diretamente do regulador 3V3\_STBY (sempre presente em estado S5/S3). Sem isso, a GPU não inicializa o controlador ROM. |
| **CS# (Chip Select)** | 3.3 V (idle) / 0 V (ativo) | Habilita o chip para leitura | Deve oscilar logo nos primeiros 100 ms após o “power good” do PCIe. |
| **CLK** | 3.3 Vpp clock SPI | Sincroniza leitura | Oscilação de 24 MHz típica. Sem clock → GPU não tenta ler o ROM. |
| **MISO/MOSI** | 3.3 Vpp | Dados da ROM | Deve haver alternância binária durante leitura. Linhas travadas em 0 V ou 3.3 V indicam curto, solda fria ou falha do chip. |
| **WP# e HOLD#** | **3.3 V** (puxadas para alto via pull-up 10k) | Proteção de gravação e pausa de barramento | Se uma delas estiver em 0 V → EEPROM bloqueada ou inativa. |

---

### ⚙️ 2. TENSÕES AUXILIARES QUE PERMITEM O BOOT DO CONTROLADOR

| Linha | Tensão | Origem | Função |
| --- | --- | --- | --- |
| **3V3\_STBY** | 3.3 V | Regulador standby (sempre ativo no PCIe) | Alimenta SPI, GPIOs e controlador I2C da GPU. |
| **1V8\_AUX** | 1.8 V | LDO interno da GPU ou regulador externo | Alimenta o *ROM interface logic* dentro do die da GPU. |
| **VDDC / VDD\_SOC / VDD\_MEM** | 0 V até boot | Só são ativadas **após** o ROM ser lido | Se essas tensões sobem antes da leitura → bug no PWM ou curto. |

---

### 🧩 3. DIAGNÓSTICO RÁPIDO

1. **Verifique VCC\_SPI (pino 8 da W25Q128JQ)** — tem de estar 3.3 V fixo com o PC ligado.
	- Se não tem → regulador 3V3\_STBY ausente ou trilha rompida.
2. **Teste WP# (pino 3)** e **HOLD# (pino 7)** — devem estar **altos (3.3 V)**.
	- Se estiverem em 0 V, a ROM fica bloqueada.
3. **Com o osciloscópio**, veja se **há clock** no pino 6 (CLK) nos 2 primeiros segundos de energização.
	- Se não há → GPU não tenta ler o ROM → possível falha no próprio die ou curto no SPI.
4. **Confirme integridade de solda e continuidade** entre a EEPROM e os pinos da GPU.
	- Muitas vezes o pad do **CS#** ou **MISO** trinca com o calor da dessolda e não reconecta.
5. **Evite EEPROMs clones** (como GD25Q128, MX25L128, etc.) — o firmware da AMD usa opcodes específicos da **Winbond**.

---

### 💡 Dica avançada

Se o CH341A consegue ler e verificar o ROM gravado **fora da placa**, mas **na placa não é reconhecido**, o defeito não está no arquivo e sim em:

- ausência dos **3.3 V** no VCC do chip;
- **WP#/HOLD#** presas em GND;
- ou falha na trilha de **CS#** até o die da GPU (muito comum em MI50/MI60 por stress térmico).

---

Se quiser, posso te ajudar a montar uma **checklist de medição por pino** da W25Q128JQ com mapa de continuidade até o controlador da GPU (local exato dos pads e vias), para você testar no microscópio e no multímetro.  
Quer que eu te mande isso em esquema visual?

---

**Você disse**

Check list pino a pino do sou gd25q80

---

Ótimo — checklist direto, pino a pino para **GD25Q80 (SOIC-8 / SOP-8)** com o que medir, o que esperar e causas comuns. Faça na ordem: **alimentação → GND → sinais**. Use multímetro (V/DC, continuidade), osciloscópio (SE TIVER) e microscópio para inspeção física. Valores e comportamento baseados no datasheet GigaDevice. [^1]

---

## Mapeamento rápido (Top view / padrão)

1 — **CS# (Chip Select)**  
2 — **SO / DO / IO1 (Data Out / MISO)**  
3 — **WP# (Write Protect / IO2)**  
4 — **VSS (GND)**  
5 — **VCC (VCCIO) — 3.3 V**  
6 — **HOLD# / IO3**  
7 — **SCLK (Serial Clock)**  
8 — **SI / DI / IO0 (Data In / MOSI)**. [^2]

---

## Checklist pino a pino (faça isto)

**Antes:** placa ligada (estado onde GPU tenta dar POST). Use óculos/máscara ESD.

## Pin 4 — VSS (GND)

- Esperado: **0 V** (referência).
- Teste: multímetro continuidade GND → pinos GND do conector PCIe / blindagem.
- Falha: alto R entre GNDs = solda fria / via rompida → VCC comporta-se mal.

## Pin 5 — VCC (VCC\_IO)

- Esperado: **~3.3 V ±5% (≈3.25–3.45 V)** enquanto placa energizada (standby/POST).
- Teste: medir com multímetro no power-on. Verificar capacitor de desacoplamento próximo (0.1µF).
- Falha: 0 V ou <3.0 V → regulador 3V3\_STBY ausente, sequência de power-good falhando, pad danificado. [^1]

## Pin 1 — CS# (Chip Select)

- Idle: **alto (3.3 V)**. Quando a GPU acessa a ROM, **vai baixo (0 V)** durante a transação.
- Teste: com osciloscópio verifique transição para LOW nos primeiros ~50–200 ms do boot. Multímetro em DC pode não captar o pulso.
- Falha: permanentemente alto (nunca ativa) → GPU não seleciona chip (trilha CS rompida, resistor série aberto, ou controlador morto). Se CS preso em LOW → SPI fica ocupado; pode travar boot.

## Pin 7 — SCLK (Clock)

- Idle: **0/3.3 V (pulsos)**. Ao iniciar leitura, deve aparecer **clock (típico tens a dezenas de MHz dependendo do modo)**.
- Teste: osciloscópio — se não há clock, GPU não está tentando ler (ou trilha interrompida).
- Falha: clock ausente → problema no controle SPI (GPU) ou curto na trilha.

## Pin 8 — SI / DI (MOSI / Data In)

- Idle: pull-up ou high impedance; durante escrita/commands deve alternar (0↔3.3V).
- Teste: oscilo para ver dados sendo empurrados quando CS baixo. Programador CH341A em modo in-circuit pode não conseguir escrever se WP#/HOLD# controlados pela placa.

## Pin 2 — SO / DO (MISO / Data Out)

- Deve alternar quando a ROM responde a um comando de leitura. Se ficar sempre em 3.3 V ou 0 V → curto, pad danificado, ou chip morto.
- Teste: enviar comando **Read JEDEC ID (0x9F)** com programador in-circuit — deve retornar ID. Se o programador lê ID fora da placa mas in-circuit não, problema de sinal/trilha. (Cuidado: alguns boards têm buffers / multiplexer). [^1]

## Pin 3 — WP# (Write Protect / IO2)

- Idle: **alto (3.3 V via pull-up ~10k)**. Se em **0 V**, chip pode ficar protegido contra escrita/erase.
- Teste: medir DC; procurar resistor pull-up para VCC. Se permanentemente baixo → trilha/curto (às vezes solda sobrando).
- Observação: em modo quad IO este pino pode atuar como IO2 se QE=1.

## Pin 6 — HOLD# (IO3)

- Idle: **alto (3.3 V via pull-up)**. Se travado em 0 V → bloqueio do barramento.
- Teste: medir DC; oscilo para ver transições se a placa usa toggling. Também pode ser IO3 em quad mode. [^2]

---

## Testes práticos — sequência recomendada (rápido e eficaz)

1. Visual: inspeção pad/pinos, rachaduras, resíduo de solda, ranhuras.
2. Continuidade GND (pin4) → massa da placa.
3. Com placa ligada: medir VCC (pin5) → deve ser ~3.3 V.
4. Medir WP# (pin3) e HOLD# (pin6) → devem estar altos (~3.3 V).
5. Usar osciloscópio: observar **CS# (pin1)** nos primeiros 0–500 ms do power-on — deve haver pulso de seleção; se não houver, problema upstream.
6. Observar **SCLK (pin7)** enquanto CS# é baixo — deve haver clock.
7. Enquanto CS ativo, observar **SO (pin2)** → deve haver resposta do chip.
8. Se tudo acima estiver correto e ainda não assina vídeo: testar continuidade de **CS#/SCLK/SO** até o die/GPU (vias/pads).
9. Teste final: **ler JEDEC ID (0x9F)** in-circuit com CH341A (modo “read ID”) — se retornar ID correto → ROM está funcional e comunicação elétrica OK; se não retornar, levantar CS (dessoldar/levantar 1 pino) e testar off-board. [^1]

---

## Valores de referência / componentes adjacentes

- Pull-up típicos: **10 kΩ** para WP# e HOLD#.
- Capacitor de desacoplamento perto do VCC: **0.1 µF** + cerâmico 1 µF/10 µF próximo.
- Clock típico: **modo SPI até ~104 MHz** em versões 3.3 V (varia conforme variante). [^3]

---

## Causas recorrentes quando “não reconhece VBIOS” após dessolda/reboba

- Pad ou via rompida no CS/CLK/MISO.
- Pull-up (WP/HOLD) solda “colada” no GND por excesso de fluxo/solda.
- Regulador 3.3V com dano térmico (VCC cai sob carga).
- EEPROM com pino interno danificado por calor (às vezes a memória funciona off-board mas não in-circuit por sinal).
- Problema no controlador SPI do die (menos comum, mas ocorre em GPUs com stress térmico).

---

## Ações imediatas recomendadas (priorize)

1. Meça VCC (p5) e GND (p4). Se não tiver 3.3 V — pare aí; corrija regulador.
2. Verifique WP# e HOLD# altos. Se não, limpe/resolde pull-ups.
3. Use osciloscópio/LED lógico para ver se CS e CLK pulsam no boot.
4. Se tudo elétrico OK, **levante o pino CS (ou 1 pino de dado)** e tente ler off-board com CH341A. Se off-board lê → problema de trilha/pad.
5. Se off-board não lê → possível gravação ruim ou chip danificado; substitua a EEPROM por uma testada GD25Q80 compatível (respeitar a versão Vcc e tensão). [^1]

---

Se quiser eu te mando **um checklist em formato de tabela imprimível** (CSV) com: `pino,nome,esperado,testes,resultado (PASS/FAIL)` — pronto para preencher no bancada. Quer que eu gere agora?

---

**Você disse**

Pinos 8 e 7 3.4v fixosd

---

Perfeito, John — **isso já revela um sintoma bem específico**.  
Vamos direto ao diagnóstico prático:

---

### ⚙️ Situação atual

> **Pino 8 (SI/MOSI)** → 3.4 V fixo  
> **Pino 7 (SCLK)** → 3.4 V fixo

---

### 🔍 Interpretação elétrica

| Linha | Função | Estado esperado | Teu sintoma | Diagnóstico provável |
| --- | --- | --- | --- | --- |
| **SCLK (p7)** | Clock da GPU p/ ROM | Deve oscilar (pulsos 0–3.3 V) nos 200 ms iniciais do boot | 3.4 V fixo (alto, sem clock) | **GPU não tenta ler o VBIOS.** Pode estar sem sequência de power-good, sem 3V3\_STBY real, ou barramento SPI travado. |
| **SI/MOSI (p8)** | Dados enviados da GPU para a ROM | Deve alternar quando CS# vai LOW | 3.4 V fixo (alto, inativo) | Barramento SPI em estado **idle permanente**. A controladora SPI da GPU nunca iniciou leitura. |

---

### 🧩 Interpretação técnica

Essas duas linhas **devem “viver”** — elas só ficam fixas em HIGH quando:

1. **GPU não recebeu sinal de reset liberado (GPU\_RST#)**;
2. **Sequência de power-good falhou** (VDDC, VDD\_SOC, 1V8\_AUX não estão prontos);
3. **CS# (pino 1)** não abaixa (GPU não habilita o chip, então o clock nunca parte);
4. **Trilha de CS# aberta** → GPU tenta, mas SPI fica inerte, e o pino de clock fica em tri-state com pull-up (3.3 V);
5. **Chip queimado internamente** ou **curto entre SCLK ↔ SI/MISO** (menos comum).

---

### ⚡ Teste rápido (3 passos)

1. **Meça o pino 1 (CS#):**
	- Deve ficar **alto (3.3 V)** e **puxar pra 0 V por breves instantes** no início do boot.
		- Se **nunca vai pra 0 V**, GPU não está tentando ler → *problema do lado da GPU / VRM / reset sequence*.
		- Se **fica sempre 0 V**, o chip SPI trava em “selecionado” → barramento fica morto e todos os sinais ficam altos ou flutuando.
2. **Verifique VCC (p5):**
	- 3.3 V estáveis? OK.
		- Se cair abaixo de 3.2 V quando alimenta, pode manter a controladora em standby.
3. **Checar WP# (p3)** e **HOLD# (p6)** — ambos devem estar **em 3.3 V fixo** (pull-up).
	- Se um estiver 0 V, o chip não responde e deixa o barramento “flutuando alto”.

---

### 💡 Conclusão prática

Se 7 e 8 estão 3.4 V fixos **sem clock**, significa:

> O barramento SPI **nunca iniciou comunicação** — GPU não chegou à fase de leitura de VBIOS.

**Causas mais prováveis (em ordem):**

1. Trilha **CS# rompida** (muito comum após ressolda).
2. GPU **sem sinal de “Power Good”** para iniciar o microcontrolador interno.
3. Falha no **regulador 1V8\_AUX** (sem ele, o subsistema SPI interno da GPU não liga).
4. EEPROM errada ou com curto interno nos pinos de dados.
5. EEPROM morta (drena barramento, mas mantém 3.4 V por pull-ups).

---

### 🧠 Ação imediata

- **Com o multímetro**, teste continuidade do pino 1 (CS#) da EEPROM até o ponto correspondente na GPU.
- Se **não houver continuidade**, refaça o jumper — é o defeito mais comum.
- Se **há continuidade e 3V3\_STBY ok**, verifica se existe **clock de 1.8 V LDO** no die da GPU (ponto de teste VDDIO / VDD\_AUX).
- Como teste final: dessolde o chip, grave fora da placa um dump funcional, **teste off-board (ler ID)**, e recoloca.
- Se mesmo assim 7 e 8 ficam altos → GPU não inicializa barramento ⇒ problema a montante (sequência de enable/reset).

---

Se quiser, te monto um **fluxo de diagnóstico progressivo** (com pontos de teste na placa da MI50, tensão esperada e comportamento) pra rastrear se o CS#/RESET da GPU estão chegando. Quer que eu desenhe esse mapa?

[^1]: [mouser.com](https://www.mouser.com/datasheet/2/870/DS_00478_GD25Q80E_Rev1_3-3435732.pdf?srsltid=AfmBOoqtu_ObqeeMs0l7SfR6mVlSvOqFVV_ZJqSJNtZTHEo8vNAAf6L-&utm_source=chatgpt.com)

[^2]: [mouser.com](https://www.mouser.com/datasheet/2/870/gd25lq80c_v1.9_20200509-1668184.pdf?srsltid=AfmBOoqpurRNlDeWYm09xCbPHtzjXQlVmjJn1TBWgHBykhekUgNlAbru&utm_source=chatgpt.com)

[^3]: [alibaba.com](https://www.alibaba.com/showroom/gd25q80csig-chips.html?utm_source=chatgpt.com)