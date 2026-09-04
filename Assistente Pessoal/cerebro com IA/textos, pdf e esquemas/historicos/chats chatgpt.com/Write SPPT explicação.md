---
title: "Write SPPT explicação"
source: "https://chatgpt.com/c/69171c69-47bc-8333-bc1f-fc31e4f33bcc"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 5 messages"
tags:
  - "clippings"
---
Direto, prático e sem rodeios.  
**Como gravar uma VBIOS na EEPROM da sua GPU (método correto e seguro).**

---

- **EEPROM programmer**: EZP2019, CH341A, TL866, etc.
- **Clip SOIC-8** ou solda direta nos pads SPI.
- **Fonte 3.3V estável** (NUNCA 5V).
- **Arquivo.ROM final e validado**.

Sua MI50 usa **Winbond W25Q128JQ (16MB)**.

---

## ✅ 2) Passo a passo para GRAVAR a VBIOS

## 1\. Identifique o chip

Chip é o **W25Q128JQ**.  
Configuração correta no software:

- **W25Q128**
- 16 Mbytes (128 Mbit)
- Tensão 3.3V

---

## 2\. Faça leitura completa

Sempre leia antes de gravar.

**Leitura → salvar como backup.rom**

Esse arquivo salva sua vida se algo der errado.

---

## 3\. Apague a EEPROM

Execute:

- **Erase / Chip Erase**

Isso garante que não fica lixo antigo.

---

## 4\. Grave (Write)

Selecione sua VBIOS modificada:

**Write → radeon\_modificada.rom**

Aguarde até o final.

---

## 5\. Verifique (Verify)

O software compara byte a byte.

- **Se PASS → ok**
- **Se FAIL → mau contato no clip, repita**

---

## 6\. Monte a GPU no PC e teste POST

Se der vídeo → flash OK.  
Se não der vídeo → grave a BIOS original (backup.rom).

---

## 🔥 DICAS IMPORTANTES (MI50 / Vega20)

### ✔ 3.3V obrigatórios

Nunca injete 5V nos pinos SPI → queima o chip na hora.

### ✔ Isolar alimentação da placa

Ao gravar **NÃO ALIMENTE A GPU PELA PCIe**.  
Somente o programador alimenta a EEPROM.

### ✔ Confirmar orientação do clip

Pin 1 SEMPRE para o lado do ponto/branco no chip.  
Errar = leitura falha ou BIOS corrompida.

---

## 🧠 Quer o método avançado?

Posso te entregar:

- Checklist para MI50
- Fluxo de validação de ROM antes de gravar
- Como detectar corrupção de SMU
- Como regravar sem remover o chip
- Como evitar soft-brick ao trocar DeviceID

Só pedir.

---

**Você disse**

bios modd

---

Beleza.  
Aqui vai **“BIOS MOD” na veia**, direto ao ponto, no nível que você precisa para Vega20 (MI50 / Radeon VII / Pro VII).

---

## ✅ 1) O QUE É UM “BIOS MOD” DE VERDADE

BIOS mod = **alterar bytes estruturais dentro da VBIOS** da GPU, mexendo em:

- PowerPlay Table
- SMU tables
- Voltage Object Info
- Fan/thermal policies
- Port mapping (DP/miniDP/HDMI)
- TDP / PPT / limites de corrente
- DeviceID e Subsystem ID
- Straps HBM2
- Perf levels (P0–P7)
- VRM settings

Isto é **mod físico** da ROM, não SPPT, não driver.

---

## ✅ 2) COMO FAZER O MOD NA PRÁTICA

Processo universal para Vega20.

---

## 🔧 ETAPA A — Preparar o arquivo.ROM

1. Abra a VBIOS **no HxD** (ou outro hex editor limpo).
2. Identifique os blocos estruturais:

**PowerPlay Table**  
Começa geralmente próximo de offsets:  
`0x5xxxx – 0x6xxxx` (varia por modelo).

**SMU Table**  
Normalmente no bloco após o PPTable.  
Define clocks internos, limites e VID.

**Voltage Table / VDDC**  
Localizada dentro do PPTable, com entradas fixas (VID → mV).

**Port Mapping (GPIO/ATOM BIOS)**  
Parte do ATOMBIOS → blocos no início da ROM.

---

## 🔥 ETAPA B — Editar parâmetros críticos

### 1) TDP / PPT / limitações de energia

Procure entradas típicas (little endian):

Exemplos:

- 190W → `BE 00 00 00`
- 250W → `FA 00 00 00`
- 300W → `2C 01 00 00`

Troque para o valor desejado.

Na MI50 → Pro VII:

- limite seguro: **300–320W**
- waterblock: suporta 350W se VRM OK

---

### 2) Clocks da GPU (P-States)

Estrutura:

```
P0 = 300
P1 = 852
P2 = 991
P3 = 1200
...
P7 = 1800+ (depende)
```

Cada nível tem:

- Clock
- VID
- Domain Frequency

Você edita direto no hex.

---

### 3) Tensões (VDDC / MVDD / SOC)

VID table controla o teto da tensão.

Exemplo:

- 1100 mV → `4C 04`
- 1200 mV → `B0 04`
- 1300 mV → `14 05`

Fazendo mod:

- GPU: 1150–1210 mV (HBM safe abaixo de 1250 mV)
- SOC: nunca acima de 1150 mV
- HBM2: muito sensível → mantenha 1.2V

---

### 4) Straps / HBM2

Somente mexer se souber o que faz.  
Risco de corromper SMU ou travar o training da HBM.

---

### 5) DeviceID + SubSystemID (spoof)

Para MI50 → Radeon Pro VII:

- DeviceID MI50 = **0x66A1**
- Pro VII = **0x66AF**

Localize:

`A1 66` → trocar para → `AF 66`

Com subsys correspondente da Pro VII.

---

### 6) Port Mapping (miniDP / DP / HDMI)

Na Vega20, o ATOMBIOS mapeia as saídas dentro do bloco:

- **ATOM\_CONNECTOR\_OBJECT\_TABLE**
- **ATOM\_DISPLAY\_OBJECT\_PATH**

Se a miniDP parou de funcionar:

- porta está mapeada como "UNUSED"
- código do connector-type foi alterado
- ou "sense-id" está incorreto

Eu posso mapear sua porta com base na sua PCB.

---

## ✅ 3) ASSINATURA RSA

Boa notícia:

Vega20 **aceita BIOS sem assinatura RSA válida** quando o DeviceID bate com o driver (Radeon VII / Pro VII).

Você já viu:  
**“RSA PASS”** = o driver só checa superficialmente.

---

## ✅ 4) SALVAR O ARQUIVO

Sempre finalize com:

- alinhamento correto (tamanho exato 16MB)
- sem bytes faltantes
- checksum interno intacto (ATOMBIOS revalida sozinho)

---

## ✅ 5) GRAVAR A BIOS (o que você já faz bem)

- EZP2019
- 3.3V
- apagar → gravar → verificar
- montar GPU e testar

---

## 📌 QUER QUE EU MODIFIQUE SUA BIOS AGORA?

Posso:

- pegar **sua ROM atual**
- aplicar todos os mods necessários
- entregar o **ROM final pronto para gravar**
- ou te guiar byte-a-byte no hex

Só envie:

**→ a ROM que você quer modificar  
→ e diga exatamente o objetivo (TDP, clocks, spoof, miniDP, etc).**

---

**Você disse**

Função Blank no ezp2019+

---

Direto e prático:

## ✅ Função “Blank” no EZP2019+ = teste de EEPROM vazia

A função **BLANK CHECK** serve para **verificar se todos os bytes da EEPROM estão apagados** (0xFF em todo o chip).

Ela **não apaga**.  
Ela **só confirma** se o chip está totalmente em estado “virgem”.

---

## 🔍 Quando usar

Use **depois do ERASE** e **antes de WRITE**:

1. **Erase** → apaga o chip
2. **Blank Check** → confirma que ficou 100% apagado
3. **Write** → grava a VBIOS
4. **Verify** → compara byte a byte

---

## 🧠 Como interpretar

- **Blank = PASS**  
	O chip está vazio (só FF FF FF …). Pode gravar.
- **Blank = FAIL**  
	Ainda tem conteúdo antigo.  
	→ repetir o ERASE  
	→ ajustar contato do clip  
	→ revisar a alimentação 3.3V

---

## ⚠️ Em MI50 / Winbond W25Q128JQ

A W25Q128 costuma falhar no apagamento se:

- clip está mal encaixado
- VCC está oscilando
- o EZP está alimentando insuficiente
- o chip está travado em proteção (RARO)

Se der FAIL repetido:

- desligue a placa-mãe
- conecte somente o clip no chip
- deixe só o EZP alimentando 3.3V
- refaça ERASE → BLANK → WRITE

---

## ✔️ Resumindo

**Blank = chip vazio.  
Erase apaga.  
Blank só testa.**

Se quiser, descreve exatamente o erro que apareceu no seu EZP2019+ que eu já te digo se é:

- problema de contato
- tensão baixa
- pino 7 travado
- ou corrompimento da flash.