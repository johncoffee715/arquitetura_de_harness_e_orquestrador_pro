---
aliases:
  - "SY8208BQNC_QFN10_3X3"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "SY8208BQNC_QFN10_3X3.pdf"
---

# SY8208BQNC QFN10 3X3

![[SY8208BQNC_QFN10_3X3.pdf]]

## Informações

- **Arquivo original:** `SY8208BQNC_QFN10_3X3.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/pwm e pfm/SY8208BQNC_QFN10_3X3.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

Application Notes: AN_SY8208A
                                                                                   High Efficiency Fast Response
                                                                              8A Continuous, 16A Peak, 28V Input
                                                                                Synchronous Step Down Regulator

General Description                                                           Features
The SY8208A develops a high efficiency synchronous                            • Low RDS(ON) for internal switches (top/bottom):
step-down DC-DC regulator capable of delivering 8A                              20/10 mΩ
continuous, 16A peak current. The SY8208A operates                            • Wide input voltage range: 4-28V
over a wide input voltage range from 4V to 28V and                            • Instant PWM architecture to achieve fast transient
integrates main switch and synchronous switch with                              responses
very low RDS(ON) to minimize the conduction loss.                             • Internal 400uS softstart limits the inrush current
                                                                              • Pseudo-constant frequency: 800kHz.
The SY8208A adopts the instant PWM architecture to                            • 8A continuous/16A peak output current capability
achieve fast transient responses for high step down
                                                                              • ±1.5% 0.6V reference
applications and high efficiency at light loads. In
                                                                              • Programmable peak current limit
addition, it operates at pseudo-constant frequency of
800kHz under continuous conduction mode to                                    • Power good indicator
minimize the size of inductor and capacitor.                                  • Output discharge function
                                                                              • Short circuit latch off protection
                                                                              • Over voltage latch off protection
Ordering Information                                                          • Input UVLO
SY8208 □(□□)□                                                                 • Over temperature protection
                    Temperature Code                                          • RoHS Compliant and Halogen Free
                    Package Code                                              • Compact package: QFN3x3-10
                    Optional Spec Code
Temperature Range: -40°C to 85°C
   Ordering Number            Package type           Note
                                                                              Applications
    SY8208AQNC                QFN3x3-10               --                      •   LCD-TV/Net-TV/3DTV
                                                                              •   Set Top Box
                                                                              •   Notebook
                                                                              •   High Power AP

Typical Applications

   VIN
                       IN
              CIN
            10uF
                       GND
                                 PG          PG (Open Drain Output)

                                 BS          CBS
High/Floating/Low      ILMT                  100nF
                                                                              VOUT=3.3V
   ON/OFF              EN         LX
                                                L 1.5uH               R1          COUT
                                                         C1
                                                                      100k        22uF×3
                                                      220pF
          CVCC         VCC        FB
          2.2uF                                                       R2
                                                                      22.1k




                    Figure 1 Schematic                                                            Figure 2. Efficiency



AN_SY8208A                                                                                                                       1
                                                                                        AN_SY8208A
Pinout (top view)




                                                 (QFN3x3-10)
            Top Mark: MRxyz, (Device code: MR, x=year code, y=week code, z= lot number code)
 Pin Name      Pin Number                                        Pin Description
    EN              1        Enable control. Pull this pin high to turn on the IC. Do not leave this pin floating.
                             Power good Indicator. Open drain output when the output voltage is within 90% to
   PG              2
                             120% of ...

<!-- OCR_EXTRACT_END -->