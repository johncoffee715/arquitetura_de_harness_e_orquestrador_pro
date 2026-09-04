---
aliases:
  - "Ball_Grid_Array(BGA)_Solder_Joint Intermittency_Detection_SJ_BIST"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "Ball_Grid_Array(BGA)_Solder_Joint Intermittency_Detection_SJ_BIST.PDF"
---

# Ball Grid Array(BGA) Solder Joint Intermittency Detection SJ BIST

![[Ball_Grid_Array(BGA)_Solder_Joint Intermittency_Detection_SJ_BIST.PDF]]

## Informações

- **Arquivo original:** `Ball_Grid_Array(BGA)_Solder_Joint Intermittency_Detection_SJ_BIST.PDF`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/Ball_Grid_Array(BGA)_Solder_Joint Intermittency_Detection_SJ_BIST.PDF`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

Ball Grid Array (BGA) Solder Joint Intermittency
                          Detection: SJ BIST™
         James P. Hofmeister                                   Pradeep Lall                                   Norman N. Roth
         Ridgetop Group, Inc.                            Dhananjay Panchagade                               DaimlerChrysler AG
         3580 West Ina Road                                Auburn University                               Cabin/Power Train E/E
          Tucson, AZ 85741                       Dept. of Mech. Engineering and CAVE                      050/G009-BB GR/EEH
           (520) 742-3300                                  Auburn, AL 36849                             71059 Sindelfingen, Germany
      hoffy@ridgetop-group.com                               (334) 844-3424                                49-(0) 7031-4389-398
                                                          lall@eng.auburn.edu                        norman.n.roth@daimlerchrysler.com
                                                          panchdr@auburn.edu

            Terry A. Tracy                                      Justin B. Judkins
       Raytheon Missile Systems                                Kenneth L. Harris
         Bldg. M02, MS T15                                   Ridgetop Group, Inc.
         1151 Hermans Road                                    3580 West Ina Road
       Tucson, AZ 85706-1151                                   Tucson, AZ 85741
            (520) 794-3962                                       (520) 742-3300
        tatracy@raytheon.com                              justin@ridgetop-group.com
                                                         kharris@ridgetop-group.com

Abstract—This paper presents test results and specifications
for SJ BIST™, an innovative sensing method for detecting                                                 1. INTRODUCTION
faults in solder-joint networks that belong to the I/O ports of
Field Programmable Gate Arrays (FPGAs), especially in
                                                                                     This paper presents test results and specifications for SJ
Ball Grid Array packages. It is well-known that fractured
                                                                                     BIST™ (Solder Joint Built-in-Self-Test™), which is an
solder joints typically maintain sufficient electrical contact
                                                                                     innovative sensing method for detecting faults in solder-joint
to operate correctly for long periods of time. Subsequently
                                                                                     networks that belong to the I/O ports of Field Programmable
the damaged joint begins to exhibit intermittent failures: the
                                                                                     Gate Arrays (FPGAs), especially FPGAs in Ball Grid Array
faces of a fracture separate during periods of stress, causing
                                                                                     (BGA) packages such as a XILINX® FG1156 [1-6].
incorrect FPGA signals. SJ BIST detects faults of 100 or                           FPGAs are widely used as controllers in aerospace
lower with zero false alarms: minimum detectable fault                               applications, and being able to detect solder joint faults
period is one-half the period of the FPGA clock; guaranteed                          increases both fault coverage and health management
detection is two clock periods. Being able to detect solder                          capabilities and support for condition-based and reliability-
joint faults in FPGAs increases fault coverage and health                            centered maintenance. As both the pitch between the solder
management capabilities, and provides support for                                    balls of the solder joints of BGA packages and the diameter
condition-based and reliability-centered maintenance12.                              of the solder balls decrease, the importance a real-time
                                                                                     solder-joint fault sensor for FPGAs increases. SJ BIST is the
                           TABLE OF CONTENTS                                         first known for detecting high-resistance faults in solder
1. INTRODUCTION...................................................... 1              joint networks of operational FPGAs.
2. SJ BIST ................................................................. 4
3. INTERMITTENCY MITIGATION ............................. 5                          The current version of SJ BIST is a Verilog-based, two-pin
4. PIN SELECTION ..................................................... 5             test group core intended to be incorporated within an end-
5. TEST ACTIVITIES ........................

<!-- OCR_EXTRACT_END -->