---
data: 2026-09-14
tags: [snn, conectoma, malecns, doomfly, absorcao]
source: github.com/nftechie/doomfly
source_head: 71ecf53d78eaffaf1a57ed7b0ccf5d458abc9f33
task_id: snn-w0-ingest
---

# Doomfly — absorção de padrões (zero código copiado)

> Licença MIT (veredito abaixo). Absorvidos SÓ padrões/pseudocódigo, conforme NAO_FAZER.
> Clone de leitura em /tmp/opencode/repos/doomfly (depth 1, HEAD verificado igual ao pedido).

## LICENÇA — veredito: MIT permissiva, absorção de padrões OK
`LICENSE:1-10`: MIT, (c) 2026 nftechie and DOOMFLY contributors. Permite uso/cópia/modificação
com atribuição. Há `licenses/` + `THIRD_PARTY.md`/`THIRD_PARTY_NOTICES.md` (dados terceiros à parte).
Decisão: nenhum código copiado p/ o harness; só padrões descritos aqui + atribuição de source/head acima.

## (i) Frame Doom → 3.335 R1–R6 brilho + 811 R8 cor
- `doom/prepare.py:28-51`: coluna de cada R1–R6 inferida pela moda dos contatos R1-R6→L1/L2/L3
  (assignedOlHex1/2); embedding axial; viewports L/R sobrepostos (`uv`: L=.60*z, R=.40+.60*(1-z)).
- `doom/prepare.py:55-57`: manifesto registra retina_total/mapped/unmapped.
- `doom/README.md:36-41`: 3.335 de 3.377 R1–R6 recebem amostras RGB; 42 sem pixel; viewport experimental.
- `docs/doom-learning-iteration-log.md:19`: 330 R8p + 481 R8y = 811 R8 mapeadas.
- `doom_learning_v6/visual.py:15-43,50,59-60`: projeção R8 por votos |peso| p/ coluna anotada,
  mesmo viewport R1–R6; canal 2=B p/ R8p, 1=G p/ R8y (proxy sRGB, `visual.py:64-65`).
- `doom/engine.py:78-92`: por frame: low-pass discreto `alpha=1-exp(-dt/10ms)`,
  drive Naka-Rushton `30*L/(0.02+L)` nos receptores; `visual.py:70-89` amostra `frame[y,x,canal]`
  via UV + linearização sRGB. Padrão reutilizável: UV-map + low-pass + Naka-Rushton.

## (ii) 4 células DNp20/DNpe017 como decoder motor fixo
- `doom/engine.py:120-125` (modo bci): `turn=clip((R_DNp20−L_DNp20)*0.12, ±6)` graus/tic;
  `forward=clip(rate_DNpe017*0.4, 0–20)`; qualquer spike DNpe017 = attack por 1 tic.
- `docs/doom-neuroscience-review.md:186-193`: IDs DNp20 R=10059/L=10162, DNpe017 L=10527/R=555871.
- `doom/prepare.py:53-54,61`: readouts registrados do grafo; gains = joystick de engenharia,
  NÃO função motora natural (README:11 avisa o mesmo). Padrão: decoder linear fixo sobre rates
  com filtro `rates=rates*e^(-s/0.1)+raw*(1-...)` (`engine.py:111`).

## (iii) Reforço: dano → estímulo PPL101 (fórmula)
- `doom/training.py:57-66` (`DamageTraining.observe`): queda de health não-terminal →
  `until = cursor + 2000` steps (2000×0.1ms = 200 ms); dano terminal excluído.
- `doom/training.py:47,100`: pulso = corrente +4 mV-equivalente nas 2 PPL101 a partir do próximo
  tic; hits sobrepostos estendem; fórmula de dose = duração entregue, não nº de eventos.
- `doom_learning_v6/survival.py:45,50,55`: mesma fronteira exata de 2000 steps, inclusive no meio do tic.
- Regra plástica KC→MBON11 (4.184 conexões, `README:12`): `doom_learning_v6/rule.py:14-17`
  PARAMETERS `trace_kc=trace_dan=1s, decay=1800s, bounds=[0.1,2.0]` (fonte: Huang/Luo 2024
  doi:10.1038/s41586-024-07819-w, adaptado); `rule.py:24-44` `drive = eta*(kc*(Gᵀ·dmid) − (Gᵀ·dan)*kmid)`,
  memória de 2 estados (u/w) com solução fechada + clip que preserva sinal excitatório.

## (iv) Persistência de memória/eficácias entre rounds
- `doom/training.py:34-37` (`new_round`): morte cancela SÓ o pulso pendente (`cancelled_steps`);
  eficácias e estado neural NÃO são zerados. `training.py:101`: estado neural + eficácias +
  traços contínuos através dos resets; sem equilibração por round.
- `doom_learning_v6/brain.py:78-83` (`reset(keep_memory)`): restaura v/g/fila/luminância do
  `initial`, mas mantém `memory_u/memory_w`; pesos voltam ao baseline SÓ se keep_memory=False.
  `survival.py:25`: episódios chamam `b.reset(keep_memory=True)`.
- `doom/checkpoint.py:1-5,30-40,52-77`: checkpoint do baseline é recovery de processo
  (rejeita subclasses de aprendizado); modo `neural-state-with-new-arena`. Padrão: separar
  estado efêmero (restaurável) de estado plástico (persistente); reset parcial com flag.
