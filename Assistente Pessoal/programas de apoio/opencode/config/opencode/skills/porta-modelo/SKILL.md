---
name: porta-modelo
description: >
  Onboarding de modelo novo (pesos) em estágios com checagens de paridade: formato → paths →
  smoke tiny → grade visual → baseline tempo/VRAM → promoção. Padrão helenizado do pipeline
  add-model 01-10 do FastVideo (.agents/skills), adaptado ao ComfyUI local. Use ao adicionar
  qualquer checkpoint/LoRA/VAE/encoder ao stack antes do primeiro render real.
origin: "helenizado: hao-ai-lab/FastVideo .agents/skills/add-model-* (Apache-2.0, 2026-09-20)"
mode: skill
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-09-20
  source_hash: "FastVideo main 2026-09-21; sessao 2026-09-18-autonoma"
---

# porta-modelo — Onboarding de pesos em estágios

Estágios (parar no primeiro que falhar; cada um com evidência):
1. **Formato**: layout esperado pelo loader (ex.: Comfy-Org single-file vs diffusers/ —
   FastH3 no HF é diffusers, NÃO drop-in no ComfyUI; preferir single-file).
2. **Paths**: arquivo resolvido via `extra_model_paths.yaml` + pasta correta
   (`text_encoders` enxerga `clip/`; `diffusion_models`, `vae`, `loras`, `clip`).
3. **Smoke tiny**: workflow mínimo (≤832×480, ≤25f, ≤8 steps) POSTado e executado;
   aceitar SOMENTE `success` com arquivo de saída real.
4. **Paridade**: checar armadilhas conhecidas antes de culpar os pesos —
   chaves dotted p/ autogrow (0.36), canais do VAE (Wan2.2 = 48, não 16),
   `weight_dtype`, `shift` do scheduler, device do encoder.
5. **Grade visual**: ≥3 frames do smoke inspecionados (zero distorção/smear) — dono julga o final.
6. **Baseline**: tempo + pico VRAM/RAM/swap do smoke registrados; extrapolação linear
   (pixels × frames × steps) com folga 1.5×; abortar se extrapolação > banda autorizada.
7. **Promoção**: somente então o modelo entra no render real; seeds, prompts e tempos
   vão ao decision-log (proveniência).

Anti-padrões (lições pagas): pular o smoke e renderizar direto; culpar VRAM quando é
canal de VAE errado; re-renderizar sem baseline após OOM; aprovar por stills.
