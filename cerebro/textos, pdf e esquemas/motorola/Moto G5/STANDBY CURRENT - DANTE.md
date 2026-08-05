---
aliases:
  - "STANDBY CURRENT - DANTE"
tags:
  - datasheet
  - esquematico
  - referencia
source: "/mnt/win2/textos, pdf e esquemas"
file: "STANDBY CURRENT - DANTE.pdf"
---

# STANDBY CURRENT DANTE

![[STANDBY CURRENT - DANTE.pdf]]

## Informações

- **Arquivo original:** `STANDBY CURRENT - DANTE.pdf`
- **Tipo:** PDF/Datasheet
- **Caminho:** `textos, pdf e esquemas/motorola/Moto G5/STANDBY CURRENT - DANTE.pdf`

<!-- OCR_EXTRACT_START -->
## 📝 Texto Extraído (OCR)

> [!info] Método: pdftotext
> Extraído automaticamente pelo OpenCode OCR Pipeline

PROCEDIMENTO DE ANALISE
               STAND BY CURRENT (mA)
CONFIDENTIAL
               Produto - DANTE
DANTE                                            Standby Current (mA)



- Necessario para realizar o teste....

- Fixture Analyzer (Dante)
- Fonte de Alimentação USB (5.0V)
- Fonte de Alimentação KEITHLEY Bateria (3.8V)
DANTE                                                                       Standby Current (mA)


    - Como realizar o teste...

    - O teste de Standby Current deve ser feito em modo BP_TOOLS.
    - Para isso devemos ligar o telefone primeiramente pela Bateria, da
    seguinte forma:

    - Colocamos o telefone no fixture analyzer com as fontes desligadas.
    - Após isso, ligar a fonte (KEITHLEY) e forçar a chave Power, até que
    ligue o telefone, em seguida volte a chave na posição neutra.
    - Ligue a fonte (USB), e conecte o cabo.


    - Dessa forma o telefone ira entrar em modo BP_TOOLS, como mostra
    o exemplo abaixo:


2
DANTE        Standby Current (mA)




- BP_TOOLS




3
DANTE                                                             Standby Current (mA)


- Abrir o QRCT (Não é preciso digitar endereço e porta no QPST)
- Com Port
- Mobile Mode Control (FTM)
- Tool (Send Sync)
DANTE   Standby Current (mA)




5
DANTE                    Standby Current (mA)


- Inserir o comando
     75 205 53 0

- Clicar em Send

- Aguarde o retorno no
QRCT Debug Message

- Em seguida,
desconecte o cabo USB.




6
DANTE                                                Standby Current (mA)



           Verifique o valor na fonte KEITHLEY


        A spec para esse teste vai de 25mA a 90mA.




7
DANTE                                                             Standby Current (mA)



    OBS: Todo telefone modelo DANTE sai da estação IFLASH em modo BP_TOOLS
         Todo telefone que falha na estação de BRD_TEST sai em modo BP_TOOLS
         Todo telefone que passa na estação de BRD_TEST sai em modo BLAN.

         BLAN - (Modo de comunicação usado pela JOT).



        Para que o telefone entre em modo BP_TOOLS, devemos liga-lo primeiro
        pela bateria usando botão PWR, em seguida plugamos o cabo USB.




8
    THANK YOU!




9

<!-- OCR_EXTRACT_END -->