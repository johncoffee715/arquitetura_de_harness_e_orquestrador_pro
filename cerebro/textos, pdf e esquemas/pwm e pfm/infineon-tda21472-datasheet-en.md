---
aliases:
  - "infineon-tda21472-datasheet-en"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "infineon-tda21472-datasheet-en.pdf"
---

# infineon tda21472 datasheet en

![[infineon-tda21472-datasheet-en.pdf]]

## Informações

- **Arquivo original:** `infineon-tda21472-datasheet-en.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/pwm e pfm/infineon-tda21472-datasheet-en.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

TDA21472



  OptimosTM Powerstage
  TDA21472

  1            Description
  •   High frequency, low profile dc-dc converters
  •   Voltage Regulators for CPUs, GPUs, and DDR memory arrays


  The TDA21472 power stage contains a low quiescent-current synchronous buck gate-driver IC co-packaged with
  Schottky diode, and high-side and low-side MOSFETs. The package is optimized for PCB layout, heat transfer,
  driver/MOSFET control timing, and minimal switch node ringing when layout guidelines are followed. The gate
  driver and MOSFET combination enables higher efficiency at the lower output voltages required by cutting edge
  CPU, GPU and DDR memory designs.
  The TDA21472 internal MOSFET current sense algorithm with temperature compensation achieves superior
  current sense accuracy versus best-in-class controller-based inductor DCR sense methods. Protection includes
  cycle-by-cycle over current protection with programmable threshold, VCC/VDRV UVLO protection, phase fault
  detection, IC temperature reporting and thermal shutdown. The TDA21472 also features auto-replenishment of
  the bootstrap capacitor to prevent over-discharging. The TDA21472 features a deep-sleep power saving mode,
  which greatly reduces the power consumption when the multiphase system enters PS3/PS4 mode.
  Operation at switching frequency as high as 1.5 MHz enables high performance transient response, allowing
  reduction of output inductance and output capacitance while maintaining industry leading efficiency.
  The TDA21472 is optimized for CPU core power delivery in server applications. The ability to meet the stringent
  requirements of the server market also makes it ideally suited for powering GPU and DDR memory designs.

  2            Features
      •   Co-packaged driver, Schottky diode, and high-side and low-side MOSFETs
      •   5-mV/A on-chip MOSFET current sensing with temperature compensated reporting
      •   Input voltage (VIN) range of 4.25 V to 16 V
      •   VCC and VDRV supply of 4.25 V to 5.5 V
      •   Output voltage range from 0.25 V up to 5.5 V
      •   80A Output Over-Current Protection (OCP) capability
      •   Operation up to 1.5 MHz
      •   VCC/VDRV under voltage lockout (UVLO)
      •   8-mV/°C temperature analog output
      •   Thermal shutdown and fault flag
      •   Cycle-by-cycle over current protection with programmable threshold and fault flag
      •   MOSFET phase fault detection and flag
      •   Auto-replenishment of bootstrap capacitor
      •   Deep-sleep mode for power saving
      •   Compatible with 3.3-V tri-state PWM input
      •   Body-Braking load transient support
      •   Small 5 mm x 6 mm x 1 mm PQFN package
      •   Lead free RoHS compliant package

  Datasheet               Please read the Important Notice and Warnings at the end of this document   <Revision 2.0>
  www.infineon.com                                                                                     <2020-11-02>
OptimosTM Powerstage
TDA21472
Description

 Table 1       Product Identification
 Part Number             Temp Range       Package                               Marking
 TDA21472                -40C to 125C   PQFN 5 mm x 6 mm                     TDA21472



                                            TDA21472                 Product Marking

                                                                     Data Matrix Code

                                             HYYWW                   Date code [YY=Year, WW=Week]
                                             AXXX                    Lot code


                                                                     Assembly Site Code


Figure 1      Picture of the Product


3             Description

3.1           Pinout




Figure 2      Pinout, Numbering and Name of Pins (transparent top view)


Datasheet                                           2                                      <Revision 2.0>
                                                                                            <2020-11-02>
OptimosTM Powerstage
TDA21472
Block Diagram
4                Block Diagram
                                                                                       VDRV                        BOOT NC PHASE            VIN VIN
                                                                                        4                             33    31   32         30 29
                                                                                                                                                       28   VIN
                      UVLO                           UVLO
                                                                                                                                                       27   VIN

                                                                HS FET Short
                                                                                SW                                            ...

<!-- OCR_EXTRACT_END -->