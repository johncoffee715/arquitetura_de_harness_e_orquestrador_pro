---
aliases:
  - "AON6912A_30V_34a_52a_ Dual Asymmetric"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "AON6912A_30V_34a_52a_ Dual Asymmetric.pdf"
---

# AON6912A 30V 34a 52a Dual Asymmetric

![[AON6912A_30V_34a_52a_ Dual Asymmetric.pdf]]

## Informações

- **Arquivo original:** `AON6912A_30V_34a_52a_ Dual Asymmetric.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/mosfets N/AON6912A_30V_34a_52a_ Dual Asymmetric.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

AON6912A
                                                                    30V Dual Asymmetric N-Channel MOSFET



 General Description                                                  Product Summary

 The AON6912A is designed to provide a high efficiency                                                     Q1          Q2
 synchronous buck power stage with optimal layout and                 VDS                                  30V         30V
 board space utilization. It includes two specialized                 ID (at VGS=10V)                      34A         52A
 MOSFETs in a dual Power DFN5x6 package. The Q1
                                                                      RDS(ON) (at VGS=10V)                 <13.7mΩ     <7.3mΩ
 "High Side" MOSFET is designed to minimize switching
 losses. The Q2 "Low Side" MOSFET is designed for low                 RDS(ON) (at VGS = 4.5V)              <19.3mΩ     <10.4mΩ
 RDS(ON) to reduce conduction losses. The AON6912A is
 well suited for use in compact DC/DC converter                       100% UIS Tested
 applications.
                                                                      100% Rg Tested




                        DFN5X6
       Top View                     Bottom View




                        PIN1
                                                                     Top View                                    Bottom View

Absolute Maximum Ratings TA=25°C unless otherwise noted
Parameter                                 Symbol                            Max Q1                   Max Q2                     Units
Drain-Source Voltage                      VDS                                                 30                                 V
Gate-Source Voltage                                    VGS                                 ±20                                    V
Continuous Drain          TC=25°C                                               34                    52
                                                       ID
Current                   TC=100°C                                              21                     33                         A
Pulsed Drain Current C                                 IDM                      85                    130
Continuous Drain          TA=25°C                                               10                    13.8
                                                       IDSM                                                                       A
Current                   TA=70°C                                               8                     10.8
                    C
Avalanche Current                                      IAS, IAR                 22                     28                         A
Avalanche Energy L=0.1mH C                             EAS, EAR                 24                     80                        mJ
                          TC=25°C                                               22                     30
                    B
                                                       PD                                                                        W
Power Dissipation         TC=100°C                                              9                      12
                          TA=25°C                                            1.9                      2.1
                                                       PDSM                                                                      W
Power Dissipation A       TA=70°C                                            1.2                      1.3
Junction and Storage Temperature Range                 TJ, TSTG                         -55 to 150                               °C

Thermal Characteristics
Parameter                                              Symbol        Typ Q1          Typ Q2    Max Q1 Max Q2                    Units
Maximum Junction-to-Ambient A           t ≤ 10s                        29              24        35     29                      °C/W
                            AD                               RθJA
Maximum Junction-to-Ambient             Steady-State                   56              50        67     60                      °C/W
Maximum Junction-to-Case                Steady-State         RθJC      4.5             3.5      5.5    4.2                      °C/W




 Rev1: Mar. 2011                                       www.aosmd.com                                                           Page 1 of 10
                                                                                                                          AON6912A



Q1 Electrical Characteristics (TJ=25°C unless otherwise noted)


Symbol                        Parameter                      Conditions                                Min       Typ       Max      Units
STATIC PARAMETERS
BVDSS   Drain-Source Breakdown Voltage                       ID=250µA, VGS=0V                           30                             V
    ...

<!-- OCR_EXTRACT_END -->