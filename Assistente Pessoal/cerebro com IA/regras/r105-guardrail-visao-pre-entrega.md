---
setor: regras
tipo: regra-universal
id: R105
data: 2026-09-17
promulgada_por: usuário (ordem direta)
status: ativa
sinônimos: [guardrail visão, pre-entrega visual, 4-self visual]
---

# R105 — Guardrail universal: visão obrigatória antes de entregar produto visual

> Ordem direta do usuário (2026-09-17): "sempre use a skill de visão setada para algum LLM
> com capacidade de visão para avaliar qualidade visual do produto antes da entrega ao user,
> assim aplicando os 4 self antes mesmo do output ser validado pelo user."

## Regra

Antes de entregar ao usuário QUALQUER produto visual (UI/página, imagem gerada, frame/thumbnail
de vídeo, PDF/deck, asset de marca, screenshot de app), o pipeline OBRIGATORIAMENTE:

1. **Renderiza evidência visual** (screenshot, frame, export do artefato).
2. **Passa pela skill de visão** apontada para um LLM com capacidade visual
   (padrão da stack: SilverHawk/VLM local quando slot VLM estiver no ar, ex. Qwen2-VL;
   fallback: foto real do artefato avaliada por modelo multimodal disponível no inventário,
   R8/R13 — nunca entrega cega).
3. **Aplica os 4-self** na avaliação (auto-crítica da própria avaliação: a imagem é a do
   produto certo? a avaliação cobriu o critério pedido? o julgamento é legível/verificável?
   o veredito é categórico R28?).
4. **Registra o veredito** (nota/veredito + path da evidência) ANTES de submeter ao usuário.
5. Só então o usuário valida — o usuário nunca é a primeira linha de defesa visual.

## Falha/abstenção

- Sem VLM disponível (VRAM/ stack): **registrar a isenção explicitamente** ("vision-gate
  adiado — evidência anexada, pendente reavaliação quando slot VLM subir") e a entrega é
  marcada como `visual-unverified` até a reavaliação. A regra NÃO é suspensa; fica vinculada.
- Produto sem cara visual (puro backend/log) não dispara a regra.

## Integrações

- R28/R53: veredito categórico. R29: evidência fresca (screenshot da sessão, nunca cache antigo).
- R8: catálogo primeiro — skill de visão existente antes de criar nova.
- Skills/subagents envolvidos: fotografo (assets), fable-judge/hestia (gates), slots VLM do inventário.

## Histórico

- 2026-09-17 — promulgada por ordem direta do usuário após entrega da landing Academy (P3),
  que foi avaliada visualmente pelo orquestrador (multimodal) mas sem passar pela skill de visão
  dedicada — gap que motivou a universalização da regra.
