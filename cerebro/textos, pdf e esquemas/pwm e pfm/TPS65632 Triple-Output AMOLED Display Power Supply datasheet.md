---
aliases:
  - "TPS65632 Triple-Output AMOLED Display Power Supply datasheet"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "TPS65632 Triple-Output AMOLED Display Power Supply datasheet.pdf"
---

# TPS65632 Triple Output AMOLED Display Power Supply datasheet

![[TPS65632 Triple-Output AMOLED Display Power Supply datasheet.pdf]]

## Informações

- **Arquivo original:** `TPS65632 Triple-Output AMOLED Display Power Supply datasheet.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/pwm e pfm/TPS65632 Triple-Output AMOLED Display Power Supply datasheet.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

Product                  Sample &                   Technical                           Tools &           Support &
                                          Folder                   Buy                        Documents                           Software          Community



                                                                                                                                                                               TPS65632
                                                                                                                                                                    SLVSCY2 – MARCH 2015

                                      TPS65632 Triple-Output AMOLED Display Power Supply
1 Features                                                                                          2 Applications
•
1     2.9-V to 4.5-V Input Voltage Range                                                                      AMOLED Displays
•     Boost Converter 1 (VPOS)
                                                                                                    3 Description
      – 4.6-V Output Voltage
                                                                                                    The TPS65632 is designed to drive AMOLED
      – 0.5% Accuracy (25°C to 85°C )                                                               displays (Active Matrix Organic Light Emitting Diode)
      – Dedicated Output Sense Pin                                                                  requiring three supply rails, VPOS, VNEG and AVDD.
      – 300-mA Output Current                                                                       The device integrates a boost converter for VPOS, an
                                                                                                    inverting buck-boost converter for VNEG, and a boost
•     Inverting Buck-Boost Converter (VNEG)                                                         converter for AVDD, all of which are suitable for
      – –1.5-V to –5.4-V Programmable Output                                                        battery operated products. The digital control pin
         Voltage                                                                                    (CTRL) allows programming the negative output
      – –4-V Default Output Voltage                                                                 voltage in digital steps. The TPS65632 uses a novel
                                                                                                    technology enabling excellent line and load
      – 300-mA Output Current                                                                       regulation.
•     Boost Converter 2 (AVDD)
      – 5.8-V or 7.7-V Output Voltage                                                                                                        Device Information(1)
                                                                                                          PART NUMBER                             PACKAGE                BODY SIZE (NOM)
      – 30-mA Output Current
                                                                                                                           TPS65632               WQFN (16)           3.00 mm × 3.00 mm
•     Excellent Line Transient Regulation
•     Short-Circuit Protection                                                                       (1) For all available packages, see the orderable addendum at
                                                                                                         the end of the datasheet.
•     Thermal Shutdown
•     3-mm × 3-mm, 16-Pin WQFN Package

4 Simplified Schematic
                                                 L1
                                                 4.7 µH
                                                                                                                                    Efficiency vs Output Current
                    VI
                                        PVIN               SWP1                                                             100
        2.9 V to 4.5 V
                                        AVIN
                                                                                  VPOS
                                                                                                                                        AVDD
                      C1                                   OUTP1                                                            90
                 3×10 µF        C5                           FBS
                                                                                  4.6 V / 300 mA                                        VPOS & VNEG
                            100 nF                                      C2                                                  80
                                           ...

<!-- OCR_EXTRACT_END -->