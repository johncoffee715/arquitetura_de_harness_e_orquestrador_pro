---
aliases:
  - "FUSB302-D"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "FUSB302-D.PDF"
---

# FUSB302 D

![[FUSB302-D.PDF]]

## Informações

- **Arquivo original:** `FUSB302-D.PDF`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/FUSB302-D.PDF`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

FUSB302 — Programmable USB Type-C Controller w/PD
                                                                                                               July 2017




     FUSB302
     Programmable USB Type-C Controller w/PD
     Features                                                        Description
          Dual-Role Functionality with Autonomous DRP               The FUSB302 targets system designers looking to
           Toggle                                                    implement a DRP/SRC/SNK USB Type-C connector
          Ability to connect as either a host or a device based     with low amount of programmability.
           on what has been attached.                                The FUSB302 enables the USB Type-C detection
          Software configurable either as a dedicated host,         including attach, and orientation. The FUSB302
           dedicated device, or dual role.                           integrates the physical layer of the USB BMC power
                                                                     delivery protocol to allow up to 100 W of power and role
           - Dedicated devices can operate both on a Type-C          swap. The BMC PD block enables full support for
             receptacle or a Type-C plug with a fixed CC and         alternative interfaces of the Type-C specification.
             VCONN channel.
          Full Type-C 1.1 Support. Integrates the following         Applications
           functionality of the CC pin
                                                                        Smartphones
           - Attach/Detach Detection as Host
                                                                        Tablets
           - Current Capability Indication as Host
                                                                        Laptops
           - Current Capability Detection as Device
                                                                        Notebooks
           - Audio Adapter Accessory Mode
           - Debug Accessory Mode                                       Power Adapters

           - Active Cable Detection                                     Cameras

          Integrates CCx to VCONN switch with over-current
                                                                        Dongles
           limiting for powering USB3.1 Full Featured cables.
          USB Power Delivery (PD) 2.0, Version 1.1 Support
           - Automatic GoodCRC Packet Response
           - Automatic retries of sending a packet if a
             GoodCRC is not received
           - Automatic soft reset packet sent with retries if
             needed
           - Automatic Hard Reset Ordered Set Sent
          Dead Battery Support (SNK Mode Support when
           No Power Applied)
          Low Power Operation: ICC = 25 μA (Typical)
          Packaged in 9-Ball WLCSP (1.215 mm x
           1.260 mm) and 14-lead MLP (2.5 mm x 2.5 mm,                             Figure 1.   Block Diagram
           0.5 mm Pitch)

     Ordering Information
                                 Operating                                                                      Packing
         Part Number                                                         Package
                              Temperature Range                                                                 Method
                                                          9-Ball Wafer-Level Chip Scale Package (WLCSP),
         FUSB302UCX
                                     -40 to 85°C          0.4 mm Pitch                                        Tape and Reel
         FUSB302MPX                                       14-Lead MLP 2.5 mm x 2.5 mm, 0.5 mm Pitch

© 2015 Semiconductor Components Industries, LLC.                                                               www.fairchildsemi.com
FUSB302 • Rev. 2                                                                                                   www.onsemi.com
                                                                                                                                                                                        FUSB302 — Programmable USB Type-C Controller w/PD
     Typical Application
                                                                                                                           BATTERY
                                                                                                                                        V3P3
                                                                                                                                                 PMIC [Charger +
                                                                                                                                       VBUS       VCONN Buck]



                                                                                                                          ...

<!-- OCR_EXTRACT_END -->