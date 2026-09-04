---
aliases:
  - "4G_MTK"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "4G_MTK.pdf"
---

# 4G MTK

![[4G_MTK.pdf]]

## Informações

- **Arquivo original:** `4G_MTK.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/motorola/Moto E4 Plus/4G_MTK.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

4G_MAUI_META_REV_A
                             Oct 29, 2015

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
LTE RF Tool (4G):

1 –Selecionar “LTE RF Tool”




                         1
RSSI _ Setup (Simulação):

1 – Selecionar a Aba “RSSI”
                                                              1
2 – Selecionar a Banda de Testes
                                                                                     3   5
                                                      2
3 – Setar o Duplex conforme a necessidade do Teste,
“FDD” ou “TDD”                                        4


4 – Setar a frequência do canal de RX do Teste
acrescentando um “zero” no final.
Ex: Frequência 2593 MHz – Valor: 25930
                                                          6
Obs: No gerador, a frequência deverá ser ajustada
com um Offset de 100KHz – Ex: 2593,1MHz

5 – Clicar no botão “Start”                                       MAIN   DIVERSITY




6 – Comparar os resultados com uma placa golden
Continous RX _ Setup (Debug):

1 – Selecionar a Aba “Continuous RX”
                                                          1
2 – Selecionar a Banda de Testes
                                                      2       3   4
                                                                      5
3 – Setar a frequência de RX do Teste

4 – Setar o Duplex conforme a necessidade do Teste,
“FDD” ou “TDD”

5 – Clicar no botão “Start”

7 – Medir o sinal de RX na placa seguindo o caminho
conforme é mostrado no Esquema Elétrico, comparar
os valores medidos com uma placa golden.
PUSCH TX _ Setup (Simulação e Debug):
1 – Selecionar a Aba “PUSCH TX”

2 – Selecionar a Banda de Testes                           1
                                                   2   3       4   5
                                                                       7
3 – Setar o Duplex conforme a necessidade do
Teste, “FDD” ou “TDD”
                                                       6
4 – Setar a frequência de TX do Teste

5 – Para “FDD” setar a frequência de “RX”
  – Para “TDD” setar a mesma frequência de “TX”

6 – Setar a potência do Teste

7 – Clicar no botão “Start”

8 – Comparar os resultados com uma placa golden.
Caso encontre diferenças no resultado, medir o
sinal de TX na placa seguindo o caminho conforme
é mostrado no Esquema Elétrico, comparar os
valores medidos com a placa golden.
    THANK YOU




9

<!-- OCR_EXTRACT_END -->