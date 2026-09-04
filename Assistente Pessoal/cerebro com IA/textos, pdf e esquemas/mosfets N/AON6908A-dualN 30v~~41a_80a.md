---
aliases:
  - "AON6908A-dualN 30v~~41a_80a"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "AON6908A-dualN 30v~~41a_80a.pdf"
---

# AON6908A dualN 30v~~41a 80a

![[AON6908A-dualN 30v~~41a_80a.pdf]]

## Informações

- **Arquivo original:** `AON6908A-dualN 30v~~41a_80a.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/mosfets N/AON6908A-dualN 30v~~41a_80a.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

AON6908A
                                                                        30V Dual Asymmetric N-Channel MOSFET



    General Description                                                    Product Summary

  The AON6908A is designed to provide a high efficiency                                                    Q1           Q2
  synchronous buck power stage with optimal layout and                     VDS                             30V          30V
  board space utilization. It includes two specialized                     ID (at VGS=10V)                 46A          80A
  MOSFETs in a dual Power DFN5x6 package. The Q1 "High
                                                                           RDS(ON) (at VGS=10V)            <8.9mΩ       <3.6mΩ
  Side" MOSFET is desgined to minimze switching losses.
  The Q2 "Low Side" MOSFET is an SRFET™ that features                      RDS(ON) (at VGS = 4.5V)         <12.5mΩ      <4.5mΩ
  low RDS(ON) to reduce conduction losses as well as an
  integrated Schottky diode with low QRR and Vf to reduce                  100% UIS Tested
  switching losses. The AON6908A is well suited for use in                 100% Rg Tested
  compact DC/DC converter applications.




                        DFN5X6
         Top View                      Bottom View




                     PIN1
                                                                         Top View                                Bottom
                                                                                                                Bottom  View
                                                                                                                       View

  Absolute Maximum Ratings TA=25°C unless otherwise noted
  Parameter                                 Symbol        Max Q1                                        Max Q2                 Units
  Drain-Source Voltage                      VDS                                                   30                            V
  Gate-Source Voltage                                      VGS                      ±20                  ±12                    V
  Continuous Drain           TC=25°C                                                46                    80
                                                           ID
  CurrentG                   TC=100°C                                               28                    62                    A
                         C
  Pulsed Drain Current                                     IDM                      100                  200
  Continuous Drain           TA=25°C                                             11.5                     17
                                                           IDSM                                                                 A
  Current                    TA=70°C                                                9                    13.5
  Avalanche Current C                                      IAS, IAR                 27                    40                    A
  Avalanche Energy L=0.1mH C                               EAS, EAR                 36                    80                    mJ
  VDS Spike                  100ns                         VSPIKE                   36                    36                    V
                             TC=25°C                                                31                    78
                                                           PD                                                                   W
  Power Dissipation B        TC=100°C                                               12                    31
                             TA=25°C                                                1.9                  2.1
                                                           PDSM                                                                 W
  Power Dissipation A        TA=70°C                                                1.2                  1.3
  Junction and Storage Temperature Range                   TJ, TSTG                        -55 to 150                           °C

  Thermal Characteristics
  Parameter                                                Symbol         Typ Q1         Typ Q2    Max Q1 Max Q2               Units
  Maximum Junction-to-Ambient A             t ≤ 10s                         29             24        35     29                 °C/W
                                                                 RθJA
  Maximum Junction-to-Ambient A D           Steady-State                    56             50        67     60                 °C/W
  Maximum Junction-to-Case                  Steady-State         RθJC       3.3            1.2        4    1.6                 °C/W




Rev0 : Sep 2010                                            www.aosmd.com                                                        Page 1 of 11
                                                             ...

<!-- OCR_EXTRACT_END -->