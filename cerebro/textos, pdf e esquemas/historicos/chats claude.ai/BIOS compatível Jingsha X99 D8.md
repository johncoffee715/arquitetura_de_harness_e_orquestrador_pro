**Claude**

Isso muda o quadro de forma importante — vou concluir com o que isso significa tecnicamente.

### O que muda com SAS como master

Se o **SSD SAS é reconhecido pela controladora SATA/SCU nativa do chipset C612** (a situação mais comum quando não há uma HBA dedicada), então:

- **Você não precisa mais do NvmExpressDxe.** SAS/SATA passam pelo storage stack padrão (AHCI/SCU) que já está embutido em qualquer BIOS Aptio V stock — inclusive a CX99DE30 sem nenhum mod.
- Toda a complexidade da **v19** (DEPEX, offset de injeção, risco de corromper o FV) deixa de ser necessária para o boot funcionar.
- **A v18 (microcode invalidado, 8 bytes, sem tocar no FV) volta a ser a versão certa** — é mais simples, mais segura, e resolve o que você quer (permitir o clock fix via SO) sem o risco que a v19 carrega.

Se em vez disso o SAS está ligado numa **HBA dedicada** (tipo LSI/Avago 9211-8i ou similar, comum em setups com SAS), aí a placa nem precisa reconhecer o drive diretamente — a HBA tem seu próprio Option ROM/UEFI driver. Nesse caso, o requisito é: **CSM habilitado** (se a HBA só tem Option ROM legado) ou a HBA já flashada em modo IT com firmware UEFI nativo. De novo, isso é independente dos nossos mods de BIOS.

### O 128GB "slave" (provavelmente storage do AI-Lab2)

Se for SATA também, mesma lógica — nenhum driver extra necessário. Se for NVMe, aí sim a v19 (com DEPEX) continua relevante especificamente para esse drive secundário — mas não seria mais o disco de boot, então uma falha de reconhecimento dele não trava o sistema, só limita o uso dele como storage adicional.

### Recomendação prática

**Volte para a v18** como base de testes agora:

---

**You**

pcb separada sata to sas ativa

---

**Claude**

Isso simplifica ainda mais o quadro. Uma placa conversora **SATA-to-SAS** (interposer ativo) não é uma controladora própria — ela faz a adaptação elétrica/protocolo entre o conector SAS do drive e a porta SATA nativa da placa-mãe. Do ponto de vista do firmware, **o C612 continua vendo isso como um dispositivo SATA/AHCI comum**, passando pelo storage stack padrão.

### Conclusão técnica

- **Não precisa de nenhum driver extra na BIOS.** Nem NvmExpressDxe, nem Option ROM de HBA, nem CSM. O AHCI nativo do chipset já resolve.
- A complexidade toda da **v19** (DEPEX, offset de injeção no FV) não tem função aqui — foi trabalho para um cenário (NVMe puro) que não é mais o seu.
- **v18\_FINAL é a versão certa**: microcode invalidado (8 bytes), FV\_MAIN intocado, risco mínimo de brick, e o storage boota pelo caminho nativo que já funciona desde a DE30 stock.

### Sequência final recomendada

1. Grave **v18\_FINAL** — deve bootar e reconhecer o SAS via SATA nativo sem qualquer trabalho adicional de driver
2. No CachyOS, instale o clock fix via systemd:

```bash
sudo pacman -S msr-tools cpupower
sudo cp xeon-clock-unlock.sh /usr/local/bin/
echo msr | sudo tee /etc/modules-load.d/msr.conf
sudo cp xeon-clock-unlock.service /etc/systemd/system/
sudo systemctl enable --now xeon-clock-unlock.service
```

3. Confirme com `sudo turbostat --interval 2` — Bzy\_MHz deve fixar em ~3600 sob carga total

Isso fecha o ciclo: BIOS mínima e segura (v18) + clock fix confiável via SO, sem nenhum dos riscos que quebraram v15-v17 tentando resolver um problema de storage que o SATA-to-SAS já não tem.

---

**You**

qual foi a bios official mais completa

---

**Claude**

A mais completa em termos de **Setup/opções** foi a **JSX998D3** (`JSX998D3_190806_kot_v002-upt.bin`) — mas com uma ressalva importante.

### Por que ela era a mais rica

| Métrica | JSX998D3 | Demais (T8/F8/TF/DE30) |
| --- | --- | --- |
| Setup decomprimido | **130KB** | ~90KB |
| SUPPRESS\_IF totais | 99 | 65 |
| Menus legítimos (StringID válido) | **57** | 38 |
| TPM 2.0 nativo | ✅ | ausente |
| "Quiet Boot" | ✅ | ausente |
| String explícita "NCT5532D Super IO Configuration" | ✅ | ausente |

Era **44% maior** que qualquer outra ROM que analisamos, com strings de identificação apontando diretamente para o seu SuperIO (NCT5532D) e o codename real da placa (X99-8D3 = D8).

### Por que não pôde ser usada

Apesar de ser a mais completa, ela **trava em POST 0x79** — porque inclui módulos `TrEEPei` / `TcgPei` (TPM 2.0 PEI) que esperam um chip TPM físico populado na placa. Sua D8 (AD12 v1.0) não tem esse header populado, então o PEI trava esperando hardware que não existe.

### Conclusão

A JSX998D3 provavelmente é a BIOS oficial de uma **revisão mais nova da D8** (com TPM header soldado), não da sua AD12 v1.0. É "mais completa" no sentido de ter mais recursos expostos nativamente, mas **inutilizável no seu hardware específico** sem primeiro neutralizar os módulos TPM PEI — algo que não tentamos fazer (seria um caminho possível para uma sessão futura: remover TrEEPei/TcgPei da JSX998D3 e ver se ela boota com os 57 menus intactos).

Entre as que **realmente funcionam** na sua placa, a mais rica é a base atual, **CX99DE30**, que você mesmo confirmou como a de melhor estabilidade e temperaturas.