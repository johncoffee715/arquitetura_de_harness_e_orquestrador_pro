---
title: "Adicionar mini DP BIOS"
source: "https://chatgpt.com/c/68dff1a4-c838-8327-b3bb-ebb25e720e61"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 6 messages"
tags:
  - "clippings"
---
**Você disse**

---

Beleza, então está claro:

Sua versão do **AMDVBFLASH/atiflash** é das recentes (≥3.31) → nelas **a opção `-f` foi removida**.  
Por isso, não tem como forçar flash de ROM com ID diferente via software.

👉 As únicas opções reais:

### 1\. Corrigir o ID da ROM

- A gente edita a ROM mesclada e coloca **o mesmo DeviceID + SubsystemID da sua Radeon VII original**.
- Assim, o programa não acusa mismatch → grava normalmente.
- É só substituir esses bytes na header da VBIOS.

### 2\. CH341A (método direto)

- Como você já tem a Winbond W25Q128JQ, basta gravar externo → ignora qualquer checagem.
- É 100% confiável e evita dor de cabeça.

---

💡 Minha sugestão: se você quer mesmo evitar abrir o PC e usar o gravador, o caminho é **ajustar o ID da ROM mesclada** para o mesmo da Radeon VII stock. Aí vai rodar sem erro no AMDVBFLASH.

👉 Me confirma: você prefere que eu já **modifique a ROM mesclada com o ID da Radeon VII stock** para você tentar flash direto pelo Windows/Linux, sem precisar do CH341A?

---

**Você disse**

V 3.04+external

---

Perfeito 👌

Se você está usando o **amdvbflash v3.04 + external**, essa versão ainda aceita `-f` e também grava via driver externo (não depende da checagem tão rígida das novas builds).

Então temos dois caminhos:

---

### 🔹 Opção A — Usar a ROM já mesclada

- Testar com:
	```
	amdvbflash -p 0 RadeonVII_stock_miniDP.rom -f
	```
- O `-p 0` é para a primeira GPU.
- Se ainda der `0FL01`, é mismatch de **board ID** → precisa corrigir.

---

### 🔹 Opção B — Ajustar IDs

- Eu extraio da **stock Radeon VII**:
	- `DeviceID`
		- `SubsystemID`
- E coloco esses mesmos na ROM mesclada.
- Resultado: a ROM fica “camuflada” de VII normal, mas com tabelas de conectores da Pro VII → flash sem precisar do `-f`.

---

⚡ Pergunto direto:  
Quer que eu **corrija os IDs da ROM mesclada agora** pra ela se passar por stock Radeon VII, e você tentar o flash de novo com sua versão 3.04?

---

**Você disse**

como editar essa vbios vega 20

---

Direto e prático, John 👇

### 🔧 Métodos para editar uma VBIOS Vega 20 (Radeon VII / Instinct / Pro VII)

AMD bloqueou quase todos os editores clássicos (tipo **PolarisBiosEditor**). Para **Vega 20** (Radeon VII, MI50, Pro VII), só rola edição manual ou via ferramentas específicas. Eis o mapa:

---

#### 1\. Ferramentas úteis

- **HxD (ou outro editor HEX)** → edição bruta de offsets.
- **Red BIOS Editor (RBE)** → funciona parcialmente em Vega, mas não abre tudo (melhor em Navi).
- **ATOMTableReader / ATOMDisassembler** → permite desmontar a VBIOS no formato **ATOMBIOS**, visualizar tabelas, objetos e offsets (ex.: connector/object table, powerplay table).
- **Vega20SoftPowerPlayTables (SPPT)** → não altera a VBIOS, mas injeta tabelas de clocks/tensão no driver (Windows registry hack).

---

#### 2\. O que dá pra editar

- **Connector/Object Table** → ativar/ocultar portas físicas (seu caso do MiniDP).
- **PowerPlay Table** → limites de TDP, clocks, voltagens (GPU/HBM2).
- **Fan & Thermal Table** → curvas de fan, limites de temperatura.
- **Straps de memória HBM2** → timings (bem delicado).
- **BoardID/SubsystemID** → “camuflar” a VBIOS para aceitar flash sem forçar.

---

#### 3\. Fluxo de edição

1. Abrir a ROM em **ATOMTableReader**.
2. Identificar a **Connector Table** → copiar da Pro VII para a VII stock.
3. Editar **DeviceID/SubsystemID** da Pro VII para bater com a VII stock (pode ser feito em **HxD** nos primeiros 0x50~0x60 bytes).
4. Salvar como nova ROM.
5. Flash via `amdvbflash -p 0 mod.rom` (se IDs conferirem, não pede `-f`).

---

#### 4\. Se for mexer em PowerPlay

- Offset costuma ficar em tabelas `PP_PhmSoftPowerPlayTable`.
- Com ATOMDisassembler dá pra exportar e editar (ou aplicar SPPT pelo Windows/Linux sem regravar a ROM).

---

👉 Resumindo:  
Pra editar **conector, IDs, clocks e limites** → precisa **ATOMTableReader + HxD**.  
Pra editar **clocks/voltagem de forma dinâmica** → mais prático usar **SPPT** (sem regravar a VBIOS).

---

⚡ Pergunto: você quer que eu já **prepare a ROM mesclada** com os **IDs da sua Radeon VII stock** (pra flash sem erro), ou prefere que eu te mostre exatamente **como localizar e alterar os bytes no hex** pra você mesmo editar?