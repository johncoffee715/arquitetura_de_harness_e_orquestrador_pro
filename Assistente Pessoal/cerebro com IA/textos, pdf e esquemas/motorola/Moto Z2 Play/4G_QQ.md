---
aliases:
  - "4G_QQ"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "4G_QQ.pdf"
---

# 4G QQ

![[4G_QQ.pdf]]

## Informações

- **Arquivo original:** `4G_QQ.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/motorola/Moto Z2 Play/4G_QQ.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

LTE – Non-Sgnaling_RX_TX
CONFIDENTIAL                           Jun 24, 2015
                PRODUCT ENGINEERING – FABIO MULLER
 1 – Abrir o QRCT e estabelecer a comunicação conforme mostrado abaixo:




                              1


                                          2



                                                                  3




Fabio Muller – Product Engineering
LTE – NS_RX_TX
 2 – Em “FTM Command” selecionar a ferramenta abaixo:




     1 – FTM RF Verification




                                                  1




Fabio Muller – Product Engineering
LTE – NS_RX_TX
  3 – Setup do LTE_TX


1 – Selecionar à Aba “LTE”

2 – RF Band – Escolher a Banda do Teste (Banda 7)

3 – Tx Bandwidth – 10MHz

4 – Rx Bandwidth – 10MHz
                                                               1
5 – Set UL Channel – Canal de TX do Teste

6 – Modulation – QPSK

7 – Waveform – LTE PUSCH
                                                          2         6
8 – PUSCH RBs – “12 “                                     3         7
9 – PUCCH RBs – “0 “                                      4         8
                                                          5         9
10 – PUCCH Start RB – “19”
                                                                   10
11 – Set Tx Waveform
                                                                   11
12 – Set NS Value – “1”
                                                          13
13 – Set Tx On                                            15       12

14 – Set Tx Power (dBm*10):
                                                                   14
     – Clicar em Enable

     – Ajustar a Potencia desejada multiplicada por 10

     – Set Tx Power

15 – Para desligar a Transmissão clicar em - Set Tx Off


 Fabio Muller – Product Engineering
 LTE – NS_RX_TX
  4 – Setup do LTE_RX

1 – Selecionar à Aba “LTE”

2 – RF Band – Escolher a Banda do Teste (Banda 7)
                                                             1
3 – Tx Bandwidth – 10MHz

4 – Rx Bandwidth – 10MHz

5 – Set UL Channel – Canal de TX do Teste
                                                         2
6 – Sec Chain:                                           3
     – Main Antenna – Disable                            4
                                                         5
7 – Expected DL Level:

     – Setar o valor que foi ajustado no Equipamento

8 – Set LNA State

9 – Get Rx Level (dBm*10):

     – Clicar em “Get”

     – A resposta da potencia está multiplicada por 10

                                                                 6

                                                                 7

                                                                     8

                                                                 9


 Fabio Muller – Product Engineering
 LTE – NS_RX_TX
 5 – Setup do LTE_RX_DIVERSITY



                                     1
1 – FTM Command
                                         2
2 – RF                                       3   4

3 – LTE

4 – LTE (Primary Cell)




Fabio Muller – Product Engineering
LTE – NS_RX_TX
  6 – Setup do LTE_RX_DIVERSITY


1 – RF Band – Escolher a Banda do Teste (Banda 7)

2 – Tx Bandwidth – 10MHz

3 – Rx Bandwidth – 10MHz

4 – Set UL Channel – Canal de TX do Teste

5 – Sec Chain:

     – Diversity Antenna – Enable

6 – Modulation – QPSK

7 – Ajustar o LNA Range

8 – Get RX AGC


                                      1             7
                                      2
                                      3             8
                                      4
                                      5
                                      6




 Fabio Muller – Product Engineering
 LTE – NS_RX_TX
 7 – LTE_NS_CALL_SETUP – Setup do SET_MODE_ID

  1 – FTM Command
                                            1
  2 – FTM RF Verification
  3 – Selecionar à Aba “LTE”
  4 – RF Band – Escolher a Banda do Teste
  (Banda 7)
  5 – Tx Bandwidth – 10MHz
  6 – Rx Bandwidth – 10MHz




                        3




           4
                                                2
           5
           6




Fabio Muller – Product Engineering
LTE – NS_RX_TX
 8 – LTE_NS_CALL_SETUP



     1 – FTM Command                 1
     2 – Non-Signaling
     3 – LTE NS                          2



                                             3




Fabio Muller – Product Engineering
LTE – NS_RX_TX
  9 – LTE_NS_CALL_SETUP

1 – Enable LTE NS

2 – LTE RF Band :

      – Escolher a Banda do Teste (Banda 7)
                                                                       2
                                                       1       4       3
3 – Downlink Channel

4 – Acquire DL
                                                       5
5 – Start LTE NS Data Path:

      – C-RNTI (base 10) – “14”

      – Downlink LCID – “1”

      – UE Max Tx Power Limit – “23”

      – Network Sig Value – “1”

      – Uplink LCID – “2”

   ...

<!-- OCR_EXTRACT_END -->