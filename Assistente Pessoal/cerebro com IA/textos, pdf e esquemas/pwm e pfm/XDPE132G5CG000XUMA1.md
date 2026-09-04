---
aliases:
  - "XDPE132G5CG000XUMA1"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "XDPE132G5CG000XUMA1.pdf"
---

# XDPE132G5CG000XUMA1

![[XDPE132G5CG000XUMA1.pdf]]

## Informações

- **Arquivo original:** `XDPE132G5CG000XUMA1.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/pwm e pfm/XDPE132G5CG000XUMA1.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

Preliminary
XDPE132G5C


    XDPE132G5C Digital Multi -phase Controller

    16-phase Dual Loop PWM Voltage Regulator

    Quality Requirement Category: Industrial                                                ipe r
    Features
     16-phase single or up to 8+8 dual loop configurable PWM Controller
    
    
        I2C and PMBus Rev 1.3 with AVSBus for output voltage control and telemetry
        0.625mV VID step via PMBUS VOUT_COMMAND
                                                                                    un
    
    
    
        AMD SVI2 Rev 1.07 compliant
        nVIDIA PWMVID compliant
        Phase Fault Protection and Flag with auto-compensation
                                                                            rJ
    
    
    
    
        Digitally Progammable Load Line – No external components
                                                                  l fo
        Min/Max Telemetry registers and real-time monitoring via PMBus and AVSBus (IOUT, VOUT, Temp)
        Phase current sense gain and offset calibration
        Cycle-by-cycle phase current limit
    
    
    
        Analog “IMON” for output current reporting
                                                          tia
        Two IOUT_WARN pins to flag an output OC condition on both loops
        Input Over Power flag


                                      nfi
       Catastophic Fault Output (CAT_FLT) pin
       Dual Enable Pins
    
    
                                          de
        Adaptive Transient Algorithm (ATA) minimizes output bulk capacitors and system cost
        Efficiency Shaping Features using Dynamic Phase Control and Diode Emulation
    
    
    
    
                                             n
        Protections: OVP, UVP, OC Warn, OCP, OT Warn, OTP, cycle-by-cycle per phase current limit
        Multiple Time Programming (MTP) with up to 25 writes for USER Section
        Compatible with 3.3 V tri-state Drivers
        200kHz to 2 MHz switching frequency per phase
    
    
                             Co
        +3.3 V supply voltage; -40 °C to 120 °C Ambient
        Pb-Free, Halogen Free, RoHS, 7x7 mm, 56-pin, 0.4 mm pitch QFN


    Applications
                    on
     AMD SVI2 GPU and CPU Processors
     nVIDIA GPU Processors
     High Performance ASIC Processors with AVSBus.



    Description
                ine
     High performance Ethernet Switching and Routing ASSPs




        Inf
    The XDPE132G5C is a digital multi-phase buck controller that can be configured in either a single loop or dual
    loop mode with a feature set optimized to support high performance processors that require AVSBus, AMD
    SVI2, or nVIDIA PWMVID. It can support up to 16 phases and allows flexible phase assignment between the
    two loops. The controller allows system voltage set point programming and margining through PMBus or
    dynamic voltage scaling through AVSBus. The output voltage set point can also be controlled through the SVI2
    bus or the nVIDIA PWM_VID.


    Datasheet              Please read the Important Notice and Warnings at the end of this document      Rev 1.31
    www.infineon.com                                                                                   2018-11-14
Preliminary
XDPE132G5C Digital Multi-phase Controller
16-phase Dual Loop PWM Voltage Regulator

The XDPE132G5C includes Efficiency Shaping Technology to deliver exceptional efficiency at minimum cost
across the entire load range. Dynamic Phase Control adds/drops phases based upon load current. The
XDPE132G5C can be configured to enter 1 or 2-phase operation and active diode emulation mode
automatically or by command (through PMBus, AVSBus, or SVI2 commands).
The XDPE132G5C offers digitally programmable load line thereby eliminating the need for any external load

Stages and provides accurate input and output current reporting.               ipe
line setting components. The controller is designed to work with internal current sense OptiMOS™ Power


                                                                                   r
A unique Adaptive Transient Algorithm (ATA), based on proprietary non-linear control algorithms provides
excellent transient response with reduced output capacitance. The controller also supports programmable

                                                                        un
cycle-by-cycle per phase current limit for superior dynamic current limiting.
The I2C/PMBus interface can communicate with up to 127 XDPE132G5C-based controllers. Device
configuration and fault parameters are easily defined using the OpenPower GUI and stored in on-chip
memory.
                                                                 rJ
The XDPE132G5C’s extensive fault protection includes output OV, UV and OC protection, with 2 OT protection
inputs with an OT Warning VRHOT signal output, and two output over-current warning flags.


                   ...

<!-- OCR_EXTRACT_END -->