---
name: prompt-h3
description: >
  Gerador de prompts para MiniMax H3: escolhe o modo (T2VA/I2V/FL2VA/L2VA/REF2VA), aplica
  first-lines canônicas, 6 seções Full Reference com retention levels, câmera como ação,
  voz/fala/canto, som diegético vs trilha, e valida 12 contratos antes de entregar.
  Use ao escrever ou revisar qualquer prompt destinado ao H3 (local, Colab ou cloud).
origin: "helenizado: tranqueiras/INSTRUCOES-GERADOR-PROMPTS-MINIMAX-H3.md (sha 5aa300c7) + guias oficiais MiniMax HF"
mode: skill
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-09-20
  source_hash: "5aa300c7eb439f48cd3343bc78ac600cc803e78e6c05fc5e9981f884852b1fce"
---

# prompt-h3 — Prompts MiniMax H3

## Regras de ferro
- Prompt final em **inglês** (só falas/letras em `<d>[Language] ...</d>` e texto de tela entre aspas ficam no original).
- **Bloco único contínuo, sem linhas vazias** (WanGP/ComfyUI interpreta linha vazia como outro vídeo). Sem título, sem `#`, sem explicações.
- Nunca inventar fala, letra, texto de tela ou conteúdo de referência não observável. Perguntar SÓ o indispensável (qual imagem é first-frame, identidade de cada arquivo).

## Modos (um só por prompt)
- **T2VA**: só texto. **I2VA**: uma imagem = quadro 0.00s. **FL2VA**: início + fim fixos.
  **L2VA**: só o fim fixo. **REF2VA/Omni**: refs orientam identidade/estilo/ação sem serem quadros.
- Imagem que só mantém rosto/figurino/cenário = `<Subject N>`, não `<Picture N>`.

## First-lines canônicas
- I2VA: `For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.`
- FL2VA/L2VA: `How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark...; Picture 2 (from Shot N) aligns with the S.SS-second mark...`

## Base (3 campos, nesta ordem)
`integrated_multimodal_description: [Shot 1] ...` · `overall_soundscape: ...` (1-4 frases; `N/A` só p/ silêncio pedido) · `non_diegetic_music: ...` (1-3 frases de instrumentos/ritmo; `N/A` se sem trilha).

## Linha do tempo e câmera
- `[Shot 1]` sem timestamp; cortes seguintes com tempos crescentes dentro da duração; cada corte = mudança relevante.
- Câmera como ação (`push in`, `pull out`, `truck left`, `arc shot`, `static shot`...), com amplitude/velocidade só quando não-médias.
- Ações fisicamente executáveis no tempo; vídeos curtos: cortar detalhes, nunca acelerar tudo.

## Voz e texto
- IDs vocais estáveis `(S1)`, `(S2)`; `<Subject 2> (S1)` combina aparência + voz no REF2VA.
- Voice-over: `says in an off-screen voiceover` + lábios do visível fechados. Fala entre cortes: `<scenetrans>`. Fala cortada pelo fim: `<cutoff>`. Ininteligível: `[unclear]`.
- Texto visível entre aspas, exato, sem invenção.

## REF2VA (6 seções, nesta ordem)
`subject_definitions:` · `summary:` (`[keyframe completion | reference generation | video editing | video continuation | audio reuse | audio reference]`, combináveis com ` + `) · `retention_analysis:` (visual: `fully_preserved | partially_preserved | attribute_transfer | weak_reference`; áudio: `fully_copy | partially_copy | reference | weak_reference`) · `detailed_description:` (350–500 palavras, estética + planos + refs por plano) · `overall_soundscape:` · `non_diegetic_music:`.

## 12 contratos (validar silenciosamente antes de entregar)
Modo↔arquivos · duração exata · Shot 1 sem timestamp + cortes crescentes · ações cabem no tempo · consistência (identidade/roupa/cenário) · falas em `<d>` · IDs de voz · som vs música separados · rótulos consistentes nas 6 seções · inglês (exceto diálogo/texto) · um bloco, zero linhas vazias · só o prompt final.

## Fontes
Guias oficiais MiniMax HF (base + ref) prevalecem sobre este documento quando divergirem.
