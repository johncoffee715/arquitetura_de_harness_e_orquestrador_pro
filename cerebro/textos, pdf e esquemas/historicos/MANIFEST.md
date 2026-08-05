# MANIFESTO — X99-D8 BIOS Modding Archive

## 01_roms_originais/ — ROMs enviados pelo usuário (ou baixados do GitHub para análise)

| Arquivo | FD[0x17] | Compatível D8? | Observação |
|---|---|---|---|
| d8_unlock.rom | 0x02 | ✅ | oficial D8, minimal |
| X99-D8-v003-stock-timings_VK239.bin | 0x02 | ✅ | oficial D8, timings ajustados |
| HNX99T8_200525_kot_v007_00C8B3E5_pulsating_blacklight_ON_UPT.bin | 0x02 | ✅ | base histórica principal (T8_UPT) |
| HNX99T8_200525_kot_v007_00C8B3E5-upt.bin | 0x02 | ✅ | mesma base, variante plain |
| HNX99F8_200525_kot_v011_FC9BA40E-upt.bin | 0x02 | ✅ | irmã do T8, koshak v011 |
| HNX99TF_200525_kot_v007_B20DBCC3_ALC883_887_888_VSCC.bin | 0x02 | ✅ | fonte microcode rev 0x48 + VSCC fix |
| HNX99TF_200525_kot_v010_BA62B793.bin | 0x02 | ✅ | TF v010 |
| HNX99TF_200525_kot_v011_5B7C6A7F-upt.bin | 0x02 | ✅ | TF v011 |
| mod_bios_x99-TF_stoc_25052020_LOGO_ME_100.bin | 0x02 | ✅ | TF stock + logo + ME100 |
| CX99DE30FIT_ALC883_887_888.bin | 0x02 | ✅ | **BASE VENCEDORA FINAL** (iEngineer) |
| JSX998D3_190806_kot_v002-upt.bin | 0x02 | ❌ trava 0x79 | tem TrEEPei/TcgPei (TPM PEI) |
| MNX99RS9_201015_kot_v002_6D7EAE53-upt.bin | 0x02 | ❌ trava 0x79 | tem TPM PEI |
| HNX99ZD4_201220_kot_v002_B598D0CE-upt.bin | 0x02 | ❌ trava 0x79 | tem TPM PEI |
| MNX99K9_200603_kot_v004_5F5DDD03-upt.bin | 0x03 | ❌ | incompatível |
| X99PG7_1.72 | 0x03 | ❌ | incompatível |
| X99OCF3.40 | 0x03 | ❌ POST 9C→D6→A9 | ASRock OC Formula |
| X99EX63.50 | 0x03 | ❌ d4/53 oscilando | ASRock |
| X99TC_1.82 | 0x03 | ❌ d4/53 oscilando | ASRock |
| X99UD5W.24c | 0x03 | ❌ FF direto | Gigabyte UD5 WIFI original |
| E7A54IMS.330 / .341 | 0x03 | ❌ | MSI X99A-SLI |
| E7885IMS.HH2 | 0x03 | ❌ | MSI variante |
| huanan-x99-me-cleaned-*payne0/50/microcodeupdated.bin | 0x03 | ❌ | mesma família ASRock/OCF |
| V3UNLOCK*/2HEADER*/MOUSE-FIX*/PS2FIX*/REBUILD*-JWAGNERVAZ.rom | 0x03 | ❌ | JWagner — confirmado base Gigabyte UD5WIFI |
| huananzhi-x99-f8.cx99de28.rom | 0x02 | ✅ | baixado do GitHub miyconst/Mi899 (fonte microcode 0x44) |

## 02_versoes_modificadas_claude/ — ROMs construídas nesta sessão (histórico completo v3→v19)

| Versão | Base | Mods | Resultado |
|---|---|---|---|
| Ultimate_v3 | T8 | AMITSE swap | ❌ FF direto |
| NVMe_mod_v3 | T8 | NVMe (método antigo) | parcial |
| NVMe_v4_SAFE | T8 | NvmExpressDxe | ✅ **funcionou, referência** |
| NVMe_mod_FINAL | T8 | NVMe refinado | ✅ |
| GigaGUI_mod / _FINAL | T8 | tentativa GUI | ❌ não portável |
| v5_IFR_unlock | T8 | 30 IFR patches | ⚠️ bugado (checkboxes fantasma) |
| v6_Frankenstein | T8 | IFR + microcode | ⚠️ bugado |
| v7_Surgical | T8 | IFR seletivo (4) | ❌ quebrou (BIOS Lock inconsistente) |
| v8_FullUnlock | TF | 38 IFR | ❌ só Intel RC (placa errada) |
| v9_Native | JSX998D3 | base nativa | ❌ trava 0x79 (TPM) |
| v11_Final / v11_FIXED | T8 | 38 IFR + MC + NVMe | ⚠️ AMIBCP não abria (LZMA header bug, corrigido em FIXED) |
| v12_ClockFix | T8 | + PowerLimitDxe | sem efeito real |
| v13_Safe | T8 | reset, sem IFR | ✅ estável |
| v14_Final | T8 | VSCC+MC0x48+NVMe+PWR | ✅ boota, sem diferença de clock |
| v15_ClockFix | CX99DE30 | MC removido + hook bootblock | ❌ FF no POST (#GP, MSR cedo demais) |
| v16_ClockFix | CX99DE30 | MC removido + DXE driver | ❌ FF no load SO (subsystem/DEPEX errado) |
| v17_CLEAN | CX99DE30 | MC removido + NVMe (offset errado) | ❌ SSD não reconhecido |
| v18_FINAL | CX99DE30 | MC invalidado (8 bytes) | ✅ boota, SEM NVMe |
| **v19_NVMe_DEPEX** | CX99DE30 | MC invalidado + NVMe com DEPEX | 🔄 **última versão, teste pendente** |
| JWAGNERVAZ_REBUILD_NVMe_v4/v5 | JWagner rebuild | tentativa NVMe | experimental |

## Ferramentas de apoio (clock fix via SO, não via BIOS)
Ver pasta separada de outputs: `xeon-clock-unlock.sh` + `.service` — aplica MSR 0x610 
(remove Package Power Limit) e MSR 0x1AD/1AE/1AF (turbo ratio 36) via CachyOS,
contornando os problemas de timing que quebraram as tentativas em BIOS (v15/v16).

## Regra de ouro para o OpenCode
FD[0x17] deve ser 0x02. Verificar ausência de TrEEPei/TcgPei (GUIDs 
961c19be-d1ac-4ba7-87af-4ae0f09df2a6 e 34989d8e-930a-4a95-ab04-2e6cfdff6631) 
antes de testar qualquer ROM nova como base.
