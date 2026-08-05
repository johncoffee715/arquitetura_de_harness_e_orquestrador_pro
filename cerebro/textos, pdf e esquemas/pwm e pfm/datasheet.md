---
aliases:
  - "datasheet"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "datasheet.pdf"
---

# datasheet

![[datasheet.pdf]]

## Informações

- **Arquivo original:** `datasheet.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/pwm e pfm/datasheet.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

AOZ1237QI-01
                                                                       28V/8A Synchronous EZBuckTM Regulator




General Description                                            Features
The AOZ1237-01 is a high-efficiency, easy-to-use DC/DC          Wide input voltage range
synchronous buck regulator that operates up to 28V.              – 2.7V to 28V
The device is capable of supplying 8A of continuous
                                                                8A continuous output current
output current with an output voltage adjustable down to
0.8V (±1.0%).                                                   Output voltage adjustable down to 0.8V (±1.0%)
                                                                Low RDS(ON) internal NFETs
The AOZ1237-01 integrates an internal linear regulator
                                                                 – 35mΩ high-side
to generate 5.3V VCC from input. If input voltage is lower
than 5.3V, the linear regulator operates at low drop-            – 12mΩ low-side SRFET™
output mode, which allows the VCC voltage is equal to           Constant On-Time with input feed-forward
input voltage minus the drop-output voltage of the              Programmable frequency up to 1MHz
internal linear regulator.
                                                                Selectable PFM light load operation
A proprietary constant on-time PWM control with input           Ceramic capacitor stable
feed-forward results in ultra-fast transient response while     Adjustable soft start
maintaining relatively constant switching frequency over
                                                                Power Good output
the entire input voltage range. The switching frequency
can be externally programmed up to 1MHz.                        Integrated bootstrap diode
                                                                Cycle-by-cycle current limit
The device features multiple protection functions such as       Short-circuit protection
VCC under-voltage lockout, cycle-by-cycle current limit,
output over-voltage protection, short-circuit protection, as    Thermal shutdown
well as thermal shutdown.                                       Thermally enhanced 4mm x 4mm QFN-23L package

The AOZ1237-01 is available in a 4mm x 4mm QFN-23L             Applications
package and is rated over a -40°C to +85°C ambient
                                                                Portable computers
temperature range.
                                                                Compact desktop PCs
                                                                Servers
                                                                Graphics cards
                                                                Set-top boxes
                                                                LCD TVs
                                                                Cable modems
                                                                Point-of-load DC/DC converters
                                                                Telecom/Networking/Datacom equipment




  Rev. 2.0 October 2015                              www.aosmd.com                                          Page 1 of 16
                                                                                                              AOZ1237QI-01

Typical Application

                         Input                                                 RTON
                                                     IN
                                     C2                                TON
                                     22μF            AIN
                                                                       BST
                                                     VCC                       C5
                                                                               0.1μF
                                 R3        C4
                                 100kΩ     1μF             AOZ1237-01
                   Power Good                        PGOOD              LX                                Output
                                                                               L1
                                                                              1μH        R1
                            Off On                   EN
                                                                        FB                              C3
                                                                                                        100μF
                                                                                         R2

                                                     SS             AGND
                                           CSS
                                                                    PGND


                                                   Analog Ground
...

<!-- OCR_EXTRACT_END -->