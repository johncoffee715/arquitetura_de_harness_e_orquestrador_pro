---
setor: marca
tipo: cenario-video
marca: The Academy of Eletronic
data: 2026-09-16
status: v1.0 — aprovado conceitualmente, aguardando render (Stack B)
duracao_alvo: 20–30s
engine: LTX-Video 2B (img2vid) + SDXL (keyframes/draft) + ffmpeg montagem
---

# Cenário: "Macro-Solda" — Ato de Precisão do Mascote

## Decupagem (storyboard diretor)

| Shot | Tempo | Câmera | Ação |
|---|---|---|---|
| S1 | 0–4s | Zenital estática (top-down) | Bancada de eletrônica de alta gama: multímetros, fontes programáveis, PCBs espelhadas, pinças ESD, estação de solda. Mascote ciborgue calvo de costas-para-cima, braços mecânicos branco-porcelana com anéis ouro (#A3A44A) posicionados sobre a placa |
| S2 | 4–9s | Push-in suave (dolly-in) | Câmera desce sobre o ombro mecânico; musculatura biológica do torso em contraste com braços hidráulicos; foco desliza para as mãos |
| S3 | 9–16s | **Macro extremo** | Ponta do ferro de solda toca pinos de chip BGA/QFP; liga de estanho funde; fumaça volumétrica do fluxo sobe orgânica |
| S4 | 16–20s | Macro com rack focus | Fumaça se dissipa revelando pontos de solda perfeitos; reflexo ouro nas trilhas de cobre |
| S5 | 20–24s | Pull-out lento | Revela a cena inteira; HUD dourado sutil pisca OFF → corte para end-card (F5: logo ouro + "THE ACADEMY OF ELETRONIC") |

## Prompt mestre de geração (EN — input do modelo)

> A hyper-realistic, cinematic video sequence of a high-tech electronics repair. The scene starts with a zenithal (top-down) establishing shot of a professional electronics workbench cluttered with digital multimeters, programmable power supplies, scattered PCBs, and ESD tweezers. The operator is a bald cybernetic humanoid with a muscular biological torso and exposed, highly detailed mechanical arms featuring hydraulic actuators, white matte ceramic plating and subtle gold ring accents. The cyborg is performing board-level microsoldering on a complex, high-density GPU circuit board. The camera dynamically pushes in, smoothly transitioning into an extreme macro close-up of the soldering action. A robotic manipulator arm holds a soldering iron with micro-metric precision, melting a tin alloy onto the pins of a BGA chip and exposed copper traces. Volumetric smoke from the heat-activated soldering flux rises organically into the air. Cinematic lab lighting, cool key light with warm tungsten rim reflections on metal, sharp shallow depth of field, 8k, shot on RED Komodo.

### Por-shot (segmentação para geração clipe-a-clipe, 121 frames @ 24fps cada)

- **S1 (zenital)**: "Static top-down zenithal shot, professional electronics workbench, digital multimeters, programmable power supply, scattered PCBs, ESD tweezers, soldering station, bald cybernetic humanoid with white ceramic mechanical arms and gold ring accents leaning over a high-density GPU circuit board, cinematic lab lighting, photorealistic, 8k"
- **S2 (push-in)**: "Slow cinematic camera push-in over a cybernetic humanoid's shoulder, exposed hydraulic actuators and white ceramic arm plating with gold accents, muscular biological torso, focus gliding toward hands hovering above a complex GPU motherboard, shallow depth of field, cool key light, warm tungsten rim light"
- **S3 (macro solda)**: "Extreme macro close-up, robotic fingers holding a soldering iron tip with micrometric stability onto BGA chip pins, tin alloy melting onto exposed copper traces, volumetric flux smoke rising organically, glistening molten solder joints, macro lens, razor-thin depth of field, photorealistic"
- **S4 (revelação)**: "Extreme macro, flux smoke dissipating to reveal perfect solder joints on copper traces glowing with warm gold reflections, tiny SMD components, cinematic rack focus, photorealistic"
- **S5 (pull-out)**: "Slow camera pull-out from macro electronics repair to full view of cybernetic humanoid at a dark high-tech workbench, subtle gold HUD interface elements fading on edges of frame, moody cinematic lighting"

### Negative prompt (todos os shots)

`text, watermark, logo, cartoon, anime, deformed hands, extra fingers, extra limbs, low resolution, jittery camera, shaky footage, distorted tools, melted PCB, oversaturated`

## Regras de marca embutidas

1. Braços do mascote = **cerâmica branca + anéis ouro** (fichas AMALGAMA); nunca braços industriais amarelos genéricos.
2. HUD/acento = ouro `#A3A44A` (também no grade pós).
3. Sem azul como acento (azul = trilha de apoio apenas).
4. Pós: grade leve oliva, grão fino, letra da equação "HUMANO + BIOMECATRÔNICA + IA = EVOLUÇÃO" opcional no end-card.

## Saídas planejadas (F5)

- `master-16x9.mp4` — 20–30s, loop-friendly (S5 corta ecamente p/ end-card)
- `reels-9x16.mp4` e `feed-1x1.mp4` — cortes centrados no macro (S3/S4 como núcleo)
