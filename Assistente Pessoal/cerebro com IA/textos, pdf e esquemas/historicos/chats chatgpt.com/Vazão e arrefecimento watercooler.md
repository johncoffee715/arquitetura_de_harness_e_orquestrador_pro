---
title: "Vazão e arrefecimento watercooler"
source: "https://chatgpt.com/c/68f3285c-f45c-832a-b058-d5c3d2b80760"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 5 messages"
tags:
  - "clippings"
---
Perfeito — conexões **3/8" x 1/4"** muda tudo. Vamos direto ao impacto técnico e prático:

---

## ⚙️ INTERPRETAÇÃO DAS MEDIDAS

Essas medidas significam:

- **3/8"** = diâmetro interno do tubo (**~9,5 mm**)
- **1/4" BSP** = rosca do fitting (padrão G1/4, universal em watercoolers)

Ou seja, seu **tubo interno é ~9,5 mm**, e o **fitting é G1/4**.  
A bomba de 800 L/h (5 m head) vai enfrentar **alta resistência hidráulica** se o loop for longo e com blocos restritivos (como Bykski + CPU block).

---

## 🔍 EFEITO NA HIDRÁULICA

Com 9,5 mm interno:

- Vazão real cai pra cerca de **600–650 L/h**, mesmo com bomba de 800 L/h nominal.
- Velocidade de fluxo média: **≈ 1,4 m/s** (menor que no tubo 12 mm → 1,9 m/s).
- Reynolds ≈ **13.000–14.000** → ainda **turbulento**, mas perto do limite inferior (quanto mais perto do laminar, pior a troca térmica).

Ou seja:

- Ainda há **fluxo turbulento**, mas menos eficiente.
- **Qualquer aumento na restrição (dobras, curvas 90°, radiadores densos)** derruba a vazão rapidamente.
- A bomba começa a trabalhar “no limite” da curva de pressão/vazão.

---

## 🔥 IMPACTO NA TEMPERATURA

Com tubo **3/8"**, mesmo com loop bom:

- Diferença típica entre fluido e ambiente (ΔT) sobe de **~7 °C → 9–11 °C**, dependendo do fluxo de ar.
- Se aumentar o diâmetro para **1/2" (12,7 mm ID)** e a bomba aguentar, o ΔT pode cair **2–3 °C** facilmente.

Então:

| Ação | Efeito no ΔT líquido/ambiente |
| --- | --- |
| Ficar com 3/8" | ΔT ↑ levemente (~2 °C) |
| Trocar por 1/2" mantendo a mesma bomba | ΔT ↓ 2–3 °C |
| Trocar bomba + tubo 1/2" | ΔT ↓ até 4–5 °C |
| Reorientar radiadores p/ intake (ar frio) | ΔT ↓ 5–8 °C (maior impacto real) |

---

## ✅ CONCLUSÃO DIRETA

Com conexões **3/8" x 1/4"**:

- O **fluxo é turbulento, mas limitado**, e os ganhos de aumentar diâmetro seriam reais se você tiver bomba suficiente.
- **Aumentar diâmetro e head (pressão)** = melhora.
- **Aumentar só diâmetro sem trocar bomba** = melhora pequena.
- **Mudar radiadores para intake (puxando ar frio)** = maior benefício térmico de todos.

---

## 💡 Recomendação prática

1. Se o loop for longo ou com muitos blocos → **considere tubos 1/2" ID** e fittings G1/4 compatíveis.
2. Se ficar em 3/8", **minimize curvas, T’s e 90°**; use mangueira mais curta possível.
3. **Certifique-se que o fluxo é constante (sem bolhas)** — essencial pra manter o regime turbulento real.
4. **Radiadores puxando ar externo (intake)** = +5–8 °C de eficiência garantida.
5. Se quiser **otimizar tudo**, posso te ajudar a calcular a **curva de vazão real do loop (L/h)** e o **ponto ótimo de pressão da bomba**, baseado nas perdas do teu circuito.

Quer que eu monte essa simulação hidráulica do teu loop (com perdas por metro, restrições dos blocos, e queda de vazão real estimada)?

---

**Você disse**

E se diminuir o calibre das mangueiras

---

Direto ao ponto: **diminuir o calibre (diâmetro interno)** quase sempre **piora** o desempenho do loop, salvo se você aumentar muito a cabeça da bomba para compensar. Vou explicar o porquê — com números rápidos.

### Premissas usadas

- Situação atual: **3/8" ≈ 9,5 mm ID**, vazão real estimada no seu loop ≈ **650 L/h** (conforme conversa anterior).
- Novo caso hipotético: reduzir para **1/4" ≈ 6,35 mm ID**.
- Água com viscosidade cinemática ≈ **1·10⁻⁶ m²/s**.

### Efeito hidráulico (resumo numérico)

Para fluxo em regime turbulento, a perda de carga por trecho varia fortemente com o diâmetro; mantendo a mesma bomba (mesma curva de pressão), a vazão tende a escalar proportionalmente a **d^(2.5)** (regra prática para esse regime).  
Com isso:

- Razão de diâmetros: 6,35 / 9,5 ≈ 0,668
- Vazão estimada nova ≈ **0,668^(2.5)** × vazão atual ≈ **36.5%** da vazão atual.
	- Se antes tinha ~650 L/h → **~237 L/h** depois da redução de calibre.
- Velocidades médias no tubo: caem levemente na prática (ex.: ~2.55 m/s → ~2.08 m/s neste exemplo), porque a área muda muito e a vazão caiu muito.
- Número de Reynolds: cai de ~ **24k** → ~ **13k** — ainda turbulento, mas bem menor.

### O que isso causa nas temperaturas

- **Menos vazão volumétrica (Q) = menos massa de fluido por segundo passando pelos blocos** → **menor remoção de calor**.
- Resultado prático esperado: **aumento de temperatura** do líquido e, por consequência, CPU/GPU. Em termos práticos, pode ser **+2–6 °C** no ΔT dependendo de quão restritivo é o resto do loop (radiadores, blocos, comprimento de mangueira).
- Além disso: maior perda de carga = **maior esforço da bomba**, possível ruído e desgaste; risco de formação de ruído por cavitação se a sucção ficar comprometida; maior sensibilidade a bolhas/airlocks.

### Outros efeitos práticos

- Mais sensível a curvas, fittings e T’s — cada restrição penaliza mais.
- Dificulta purge (bolhas ficam mais “presas”).
- Conexões muito pequenas às vezes vazam mais ou exigem fittings diferentes.

### Conclusão direta

- **Diminuir calibre → normalmente PIORAR o arrefecimento**, porque a vazão real cai muito a menos que você aumente a pressão da bomba.
- Se você precisa de diâmetro menor por espaço ou estética, minimize perdas: mantenha trechos curtos, evite curvas/acoplamentos desnecessários, use fittings de baixo perfil e escolha um pump com mais head.

### Recomendação prática imediata

1. **Não reduza** para 1/4" se seu objetivo é performance térmica.
2. Se for inevitável, **compense trocando a bomba por uma com curva de head muito maior** (ou coloque duas em série) — e então recalculamos.
3. Priorize antes: **radiadores em intake** e remoção de restrições (menos 90° e T) — melhora mais que trocar calibre.

Quer que eu calcule para outros diâmetros (ex.: 10 mm → 12 mm → 14 mm) e te mostre estimativas de vazão e Re com sua bomba atual? Vou direto ao ponto e já trago números.

---

**Você disse**

Loop: Bomba >gpublock>CPU Block>radiador 360mm >radiador 240> reservatório 290mm>indicador de fluxo> filtro de piscina (inox)>bomba

---

Perfeito — vou direto ao ponto: análise do teu loop atual, problemas potenciais, estimativas e ações prioritárias com medidas concretas (sem enrolar).

## Loop que você informou

Bomba → GPU block → CPU block → Rad 360 → Rad 240 → Reservatório 290 mm → Indicador de fluxo → Filtro de piscina (inox) → bomba

---

## Observações técnicas imediatas (sem rodeios)

1. **Filtro de piscina no lado de sucção (antes da bomba)** é *muito* suspeito: filtros de piscina são projetados para altas vazões e baixa sensibilidade, mas o enrosco, malhas e entradas podem criar **perda de carga alta** e **vácuo na sucção** → risco de **cavitação** e enorme queda de vazão.
2. **Indicador de fluxo na sucção** também adiciona restrição e pode dar leituras erradas se houver bolhas.
3. Reservatório alimentando a bomba é bom — **reservatório antes da bomba = correto** — mas a sequência exata das peças no caminho da sucção importa (evitar itens muito restritivos entre reservatório e bomba).
4. Dois radiadores em série não são um problema grande; a queda mais significativa vem dos **blocos + filtro + fittings + curvas**.
5. Com 3/8" (≈9,5 mm) + filtro inox + indicador + 2 radiadores + 2 blocos restrictivos (Bykski + CPU), **vazão real estimada** pode cair para **~350–550 L/h** (pior caso com filtro muito restritivo → ~250–350 L/h). Isso reduz performance sensívelmente.

---

## Efeitos práticos esperados (números)

- Com vazão reduzida para **~350–500 L/h**: ΔT líquido↔ambiente sobe para **~9–12 °C** (dependendo de fans e orientação).
- Se filtro for muito restritivo e cair para ~250 L/h: ΔT pode subir mais **(+3–6 °C)** adicional.
- Remover/reposicionar o filtro e otimizar fittings pode recuperar **100–250 L/h** e reduzir ΔT **2–5 °C**.

---

## Ações imediatas e prioritárias — execute nesta ordem

1. **Mova o filtro para o lado de pressão (saída da bomba)**. Não coloque filtros restritivos na sucção.
	- Resultado esperado: evita cavitação, aumenta vazão e vida útil da bomba.
2. **Coloque o indicador de fluxo depois da bomba (lado de pressão)**, antes dos radiadores. Assim mede o fluxo real e não sofre com vácuo/bolhas.
3. **Minimize perdas na sucção**: mantenha o trecho entre reservatório e bomba o mais curto e reto possível; evite cotovelos, tees e adaptadores.
4. **Inspecione o filtro inox**: se a malha for muito fina, troque por um filtro de baixa perda voltado para sistemas de PC (ou remova se for apenas decorativo).
5. **Radiadores como INTAKE** (puxando ar frio de fora) — prioridade alta. Espera reduzir várias °C.
6. **Purge rigoroso**: pulsações, inclinar o case, ventilações do reservatório até não sair bolha. Teste com bomba em baixa e alta.
7. **Medição prática**: meça L/h com um galão de 1 L — cronometre quanto tempo leva para encher e calcule. Faça antes/depois das mudanças para comparar.
8. **Se ainda quiser mais fluxo**: considere tubo 1/2" ID e/ou bomba com mais head (ou duas bombas em série) — último recurso se já fez o acima.

---

## Checklist de testes (execute e registre)

- Antes: medir tempo para encher 1 L na linha de retorno → calcular L/h. Registrar temps idle/load (GPU/CPU e líquido).
- Mover filtro para saída da bomba + mover indicador após bomba. Purge. Medir L/h e temps novamente.
- Inverter radiadores para intake (um de cada vez) e re-testar.
- Opcional: trocar mangueira para 12–13 mm ID e/ou bomba por modelo com +head; medir novamente.

---

## Recomendação direta e final (o que faz mais diferença)

1. **Reposicionar filtro para PRESSÃO** e **indicador após bomba** — faz a maior diferença imediata em vazão e evita cavitação.
2. **Radiadores como intake** — maior impacto em temperatura.
3. Depois disso, se quiser ainda mais performance, **mude para tubo 1/2" ID** ou **aumente head da bomba**.

Quer que eu te entregue um passo-a-passo pronto para executar (ordem exata de desmontagem/montagem + como medir L/h e como purgar sem stress) com tempos estimados e metas de ΔT? Vou direto ao ponto e já te passo as instruções.