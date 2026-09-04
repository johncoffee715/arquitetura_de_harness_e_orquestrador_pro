---
aliases:
  - "06_MT6572W_NAND-EMMC_LPDDR2_SKY77590_GPS_NFC_V1.0"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "06_MT6572W_NAND-EMMC_LPDDR2_SKY77590_GPS_NFC_V1.0.pdf"
---

# 06 MT6572W NAND EMMC LPDDR2 SKY77590 GPS NFC V1.0

![[06_MT6572W_NAND-EMMC_LPDDR2_SKY77590_GPS_NFC_V1.0.pdf]]

## Informações

- **Arquivo original:** `06_MT6572W_NAND-EMMC_LPDDR2_SKY77590_GPS_NFC_V1.0.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/06_MT6572W_NAND-EMMC_LPDDR2_SKY77590_GPS_NFC_V1.0.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

5                                           4                            3                               2                                                                     1




    Project : MT6572
                                                                                                                                                                        Celullar ANT
    REF_SCH TOP LEVEL
                                                                                                   BPI, APC                                         FEM
                                  EMI        x32
                                                              EMI
                                                                                                                                               TX         RX
                        Memory
                        MCP
D                                 NFI                                                              RF IQ                                                                                                                       D
                                                              NFI
                                                                                                                                                    RX
                                                                                                   BSI ctrl
                                                                                                                   MT6166                           balun


                    micro SD            MSDC 4-bit           MSDC1
                                                                                                26M_BB
                    + hot-plug                                                                                                                       26M
                                                                                                       26M_AUD    DCXO ctrl

                                                                                                                   26M_CN
                                                                                          ABB   26M_CN




                     ATV
                                                              i2S
                                                                             MT6572             CONN IQ
                                                                                                                                                     TCXO
                                                                                                                                                                        Connectivity ANT

                         MT5193
                                                                                                CONN ctrl
                                                                                                                  MT6627
                     NFC
                         MT6605
C                                                                                                                                                                                                                              C




                                                                                                32K_BB                             RTC              32K
                    Camera        Camera IF                  CAM
                    Module                                   (MIPI / Parallel)


                    2nd Camera    Camera IF
                                                                                                                  MT6323                 Headset
                                                                                                                                         (HPL, HPR, AU_VIN1)
                    Module

                                                   I2C
                                                         i2C_0                                                                                  Class D/AB


                    LCD            LCD IF                    LCD                                                               Audio
                    module                                   (MIPI / Parallel)                  AUD I/F                        Speech           Receiver



                    CTP            I2C
                                                         i2C_1                                                                                         AU_VIN0
                    controller     EINT
B                                                                                                                                                                                                                              B

            ...

<!-- OCR_EXTRACT_END -->