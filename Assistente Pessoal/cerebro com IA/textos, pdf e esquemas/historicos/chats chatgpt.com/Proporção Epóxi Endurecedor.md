---
title: "Proporção Epóxi Endurecedor"
source: "https://chatgpt.com/c/69ffb95b-48bc-83e9-9b48-8067d88c2247"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 4 messages"
tags:
  - "clippings"
---
**Você disse**

Qual é a proporção de epóxi e endurecedor

---

Depende do sistema químico da resina. Não existe proporção universal. Os mais comuns são:

- **1:1** → muito usado em epóxi transparente/artesanato.
- **2:1** → comum em resinas estruturais e laminação.
- **3:1 / 4:1 / 5:1** → industriais, náuticas, compósitos.
- Alguns usam **proporção por peso**, outros por volume.

Erro de proporção = cura incompleta, excesso de calor, fragilidade ou resina pegajosa.

Regra prática:

- Sempre siga a ficha técnica do fabricante.
- Misture lentamente por 2–5 min raspando laterais e fundo.
- Precisão ideal: balança digital de 0,1 g.

Química básica:  
A reação depende da estequiometria entre grupos epóxi e amina. Se faltar endurecedor, sobra epóxi não reagido. Se sobrar endurecedor, a peça pode ficar mole, quebradiça ou suar amina.

Exemplo comum:  
Se a resina diz:

- “100 g de resina: 50 g de endurecedor”

Então a proporção é:

$$
\frac{100}{50}=2:1
$$

Ou seja:

- 20 g resina → 10 g endurecedor
- 200 g resina → 100 g endurecedor

Para bancada eletrônica e encapsulamento:

- Prefira epóxi de baixa viscosidade.
- Evite excesso de massa num único recipiente (runaway térmico).
- Degasificação a vácuo melhora MUITO encapsulamento fino/BGA/alta tensão.

Se quiser, posso te explicar:

- proporção para encapsular eletrônica,
- epóxi para alta temperatura,
- epóxi térmico para GPU/VRM,
- epóxi UV,
- cálculo automático por peso/volume,
- ou como identificar a proporção sem ficha técnica.

---

**Você disse**

E pra fazer o reservatório de Watercooler

---

Para reservatório de watercooler, o ideal é usar:

- **Epóxi cristal de baixa contração**
- Resistência térmica mínima de ~70–90 °C
- Baixa absorção de água
- Cura lenta (menos bolha e menos empeno)

A proporção vai depender da resina escolhida, mas as mais usadas são:

- **2:1** (mais comum em resina estrutural/transparente boa)
- **1:1** (mais fácil, porém geralmente menos resistente)

Problema crítico:  
Epóxi comum de artesanato pode:

- amarelar,
- microtrincar,
- vazar com pressão/temperatura,
- contaminar loop.

Para um reservatório confiável:

- Parede mínima: 5–8 mm
- Cura total: 5–7 dias antes de usar líquido
- Faça pós-cura térmica leve (~40–50 °C)
- Nunca use álcool forte ou thinner para limpeza interna.

Melhor arquitetura:

- Tubo de acrílico/PETG + tampas usinadas em alumínio ou nylon
- Epóxi apenas como vedação
- Não faça o reservatório inteiro só de epóxi se quiser durabilidade industrial.

Para vedação:

- O-ring de silicone ou NBR
- Rosca G1/4 padrão WC

Se quiser fabricar um “tank” custom bruto:

- Fibra de vidro + epóxi estrutural → muito mais resistente
- Ou impressão 3D + selagem interna com epóxi

Para teu perfil técnico, eu faria assim:

1. Corpo em acrílico usinado
2. Tampa CNC/impressa
3. Inserto metálico G1/4
4. Epóxi apenas estrutural e de vedação
5. Teste hidrostático 24h antes de instalar

Isso evita:

- fissura por vibração,
- fadiga térmica,
- vazamento em loop de alta vazão/D5/DDC.

Se quiser, posso te passar:

- projeto de reservatório estilo industrial,
- fórmula de volume ideal do loop,
- escolha do epóxi correto,
- ou desenho técnico para fabricar no laboratório.