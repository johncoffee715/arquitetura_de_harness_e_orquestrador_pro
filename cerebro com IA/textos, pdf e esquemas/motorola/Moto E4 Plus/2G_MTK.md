---
aliases:
  - "2G_MTK"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "2G_MTK.pdf"
---

# 2G MTK

![[2G_MTK.pdf]]

## Informações

- **Arquivo original:** `2G_MTK.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/motorola/Moto E4 Plus/2G_MTK.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

2G_MAUI_META_REV_A
                             Oct 28, 2015

                       FABIO MULLER
CONFIDENTIAL        PRODUCT ENGINNERING
MAUI META Setup Inicial:

1 – Baixar o pacote de ferramentas do Koleos direto do “FTDS” na aba
“Technical Documentation”

2 – Descompactar o arquivo “Maui META 3G ver 8.1520.0.0.zip”
                                                                             4
3 – Dar um duplo click no arquivo “Meta2_3G_C2K.exe”

4 – Em “Action” clicar em “Open NVRAM database”

5 – Na janela que abrir, selecionar o arquivo de database do telefone.
Obs_1: O arquivo sempre começa com “BPLGUInfoCustomAppSrcP”
e é diferente em cada versão de SW do telefone.
                                                                         5

Obs_2: Se estiver usando USB para comunicar com o telefone, Sempre
verificar se o Cabo USB é de 4 Vias, pois se for conectado um Cabo
USB de 5 Vias no telefone Koleos, o mesmo irá queimar.




  3
MAUI META Setup Inicial:

1 – Clicar em “Options” e selecionar “Connect Smart phone into
META mode”

2 – Escolher o tipo de conexão, se estiver usando UART selecionar a
                                                                         1
porta “COM equivalente”, caso esteja usando USB selecionar “USB
COM”

3 – Clicar em “Reconnect”

4 – Encaixar a placa no “Fixture de Analyzer”, conectar o “Cabo USB de
4 Vias” ou “Cabo UART” e aguardar a comunicação do Telefone.
Obs_1: O “Maui META” sempre abre a última ferramena que foi usada.       2

Obs_2: Se estiver usando USB para comunicar com o telefone, Sempre
verificar se o Cabo USB é de 4 Vias, pois se for conectado um Cabo
USB de 5 Vias no telefone Koleos, o mesmo irá queimar.

                                                                         3
RF TOOL (2G):

1 –Selecionar “RF Tool”




                          1
Gain Sweep _ Setup (Simulação):

1 – Selecionar a Aba “Gain Sweep”
                                                          1
2 – Selecionar a Banda de Testes
                                                      2   3   4
3 – Setar o Canal de Testes

4 – Clicar no botão “Start”

5 – Comparar os resultados com uma placa golden
                                                  5
Continous RX _ Setup (Debug):

1 – Selecionar a Aba “Continous RX”
                                                        1
2 – Selecionar a Banda de Testes
                                                2   3       4
3 – Setar o Canal de Testes

4 – Clicar no botão “Start”

5 – Medir o sinal de RX na placa seguindo o
caminho conforme é mostrado no Esquema
Elétrico, comparar os valores medidos com uma
placa golden.
TX Level and Profile _ Setup (Simulação):

1 – Selecionar a Aba “TX Level and Profile”
                                                                  1
2 – Setar a modulação
       - GMSK para GSM                            2   3   4 5 6       7
       - EPSK para EDGE

3 – Selecionar a Banda de Testes

4 – Setar o Canal de Testes

5 – Setar o Training Sequence

6 – Selecionar o “Power Control Level”

7 – Clicar no botão “Start”

8 – Comparar os resultados com uma placa golden
Continous TX _ Setup (Debug):

1 – Selecionar a Aba “Continous TX”
                                                                1
2 – Setar a modulação
       - GMSK para GSM                              3   4   5       6
       - EPSK para EDGE

3 – Selecionar a Banda de Testes
                                                2
4 – Setar o Canal de Testes

5 – Selecionar o “Power Control Level”

6 – Clicar no botão “Start”

7 – Medir o sinal de TX na placa seguindo o
caminho conforme é mostrado no Esquema
Elétrico, comparar os valores medidos com uma
placa golden.
     THANK YOU




10

<!-- OCR_EXTRACT_END -->