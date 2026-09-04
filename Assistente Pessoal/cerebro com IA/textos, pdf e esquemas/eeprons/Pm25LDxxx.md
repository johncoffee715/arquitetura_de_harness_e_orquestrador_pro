---
aliases:
  - "Pm25LDxxx"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "Pm25LDxxx.pdf"
---

# Pm25LDxxx

![[Pm25LDxxx.pdf]]

## Informações

- **Arquivo original:** `Pm25LDxxx.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/eeprons/Pm25LDxxx.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

512Kbit/1 Mbit / 2 Mbit Single Operating Voltage Serial
                                                     Flash Memory With 100 MHz Dual-Output SPI Bus
                                                     Interface
                                                                               Pm25LD512/010/ 020

FEATURES

• Single Power Supply Operation                             • Low Power Consumption
- Low voltage range: 2.3 V – 3.6 V                          - Typical 10 mA active read current
                                                            - Typical 15 mA program/erase current
• Memory Organization
- Pm25LD512: 64K x 8 (512 Kbit)                             • Hardware Write Protection
- Pm25LD010: 128K x 8 (1 Mbit)                              - Protect and unprotect the device from write
- Pm25LD020: 256K x 8 (2 Mbit)                              operation by Write Protect (WP#) Pin

• Cost Effective Sector/Block Architecture                  • Software Write Protection
- 512Kb : Uniform 4KByte sectors / Two uniform              - The Block Protect (BP2, BP1, BP0) bits allow
        32KByte blocks                                      partial or entire memory to be configured as read-
- 1Mb : Uniform 4KByte sectors / Four uniform               only
        32KByte blocks
- 2Mb : Uniform 4KByte sectors / Four uniform               • High Product Endurance
        64KByte blocks                                      - Guaranteed 200,000 program/erase cycles per
                                                            single sector
• Low standby current 1uA (Typ)                             - Minimum 20 years data retention
• Serial Peripheral Interface (SPI) Compatible
- Supports single- or dual-output                           • Industrial Standard Pin-out and Package
- Supports SPI Modes 0 and 3                                - 8-pin 150mil SOIC
- Maximum 33 MHz clock rate for normal read                 - 8-pin 208mil SOIC for Pm25LD040
- Maximum 100 MHz clock rate for fast read                  - 8-pin 300mil PDIP for Pm25LD040
                                                            - 8-contact WSON
• Page Program (up to 256 Bytes) Operation                  - 8-pin TSSOP
- Typical 2 ms per page program                             - Lead-free (Pb-free), halogen-free package
• Sector, Block or Chip Erase Operation
- Maximum 10 ms sector, block or chip erase

GENERAL DESCRIPTION
The Pm25LD512/010/020 are 512Kbit/ 1Mbit / 2Mbit Serial Peripheral Interface (SPI) Flash memories, providing
single- or dual-output. The devices are designed to support a 33 MHz clock rate in normal read mode, and 100
MHz in fast read, the fastest in the industry. The devices use a single low voltage power supply, wide operating
voltage ranging from 2.3 Volt to 3.6 Volt, to perform read, erase and program operations. The devices can be
programmed in standard EPROM programmers.

The Pm25LD512/010/020 are accessed through a 4-wire SPI Interface consisting of Serial Data Input/Output
(SlO), Serial Data Output (SO), Serial Clock (SCK), and Chip Enable (CE#) pins. They comply with all
recognized command codes and operations. The dual-output fast read operation provides and effective serial
data rate of 200MHz.

The devices support page program mode, where 1 to 256 bytes data can be programmed into the memory in
one program operation. These devices are divided into uniform 4 KByte sectors or uniform 32 KByte
blocks.(Pm25LD020 is uniform 4 KByte sectors or uniform 64 KByte).

The Pm25LD512/010/020 are manufactured on pFLASH™’s advanced non-volatile technology. The devices are
offered in 8-pin SOIC 150mil, 8-contact WSON and 8-pin TSSOP. The devices operate at wide temperatures
between -40°C to +105°C.




Confidential information
Chingis Technology Corp.                              1                  DRAFT Date: August, 2010, Rev:0.4
                                                                  Pm25LD512/010/ 020


PRODUCT ORDERING INFORMATION
Pm25LDxxx - S C E

                                                    Environmental Attribute
                                                    E = Lead-free (Pb-free) and Halogen- free
                                                    package

                                                    Temperature Range
                                                    C = Commercial Grade (-40°C to +105°C)

                                                    Package Type
                                                    S = 8-pin SOIC 150mil (8S)
                                                    B = 8-pin SOIC 208mil (8B)
                                                    P = 8-pin PDIP 300 mil (8P)
                                                    K = 8-contact WSON (8K)


                                                    pFlash Device Number
                                                    Pm25LD512/010/020




Part Number                Operating Frequ...

<!-- OCR_EXTRACT_END -->