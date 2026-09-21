---
name: video-local
description: >
  Render local de vídeo via ComfyUI em GPU AMD/VRAM limitada (validado na Vega 20 16GB gfx906):
  doutrina distilled-first, quantização fp8/int8, políticas de offload nomeadas, decode tiled,
  QA por grade multi-frame e guarda de swap. Use ao planejar, estimar ou executar geração de
  vídeo local — ou ao decidir entre local vs nuvem vs Colab.
origin: "helenizado: hao-ai-lab/FastVideo (Apache-2.0, 2026-09-20 — P-01..P-07) × medidas Vega 2026-09-18/20"
mode: skill
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-09-20
  source_hash: "FastVideo main 2026-09-21; sessao 2026-09-18-autonoma"
---

# video-local — Vídeo local em hardware limitado

## Doutrina (ordem de prioridade)
1. **Distilled-first**: pesos few-step (LoRA turbo, checkpoints DMD2) antes de otimizar o resto.
   Cache de atenção (TeaCache-like) NÃO existe no FastVideo in-tree — não prometer o que não há.
2. **Memória antes de velocidade**: fp8/int8 nos pesos; encoder de texto no CPU quando VRAM < soma dos pesos;
   `--lowvram`; `VAEDecodeTiled` (tile 256/overlap 64) sempre acima de 480p.
3. **Atenção esparsa é direção, não dependência**: STA foi arquivado pelo próprio FastVideo em favor de VSA;
   receitas aqui são backend-agnósticas (nenhum kernel CUDA é requisito).
4. **RIFE temporal**: menos frames + interpolação (custom node ComfyUI-Frame-Interpolation) como alternativa
   a renders longos — reuse, não forja.

## Políticas de offload (nomes canônicos)
- `encoder-cpu`: text encoder no CPU (ex.: umt5 6.3GB fora da VRAM; exige RAM host livre).
- `lowvram-stream`: `--lowvram` (streaming de blocos; lento sob swap, mas sobrevive).
- `tiled-decode`: `VAEDecodeTiled` em qualquer decode >480p (corta pico de VRAM e RAM).
- `lazy-weights`: carregar só o necessário por ato; manter servidor UP entre atos (modelos residentes).
- `swap-guard`: `swap-guard.sh` (bundled) aborta a 28GB de swap — protege o host; OOM-killer real
  matou 2 servidores (22:24, 22:33, journalctl) antes da guarda existir.

## Números Vega 20 16GB (evidência fresca 2026-09-18/20, não estimativa)
- Wan 2.2 TI2V-5B fp16 + umt5 fp8 + wan2.2_vae (48 canais! wan_2.1_vae quebra o decode): tiny
  832×480×25f×8steps = **630s, sem distorção** (`smoke-wan_00001_.mp4`).
- Ato 1280×720×193f×20steps = **HIP OOM aos 29min** (teto VRAM). Ato 960×544 = swap 30GB
  (teto host). Box com baseline ~19GB ocupados NÃO comporta vídeo local agora.
- H3-33B int8 + Qwen 32B: load morto em ~2.4h (swap 30/31). Pesos guardados p/ RAM futura.
- Peculiaridades ComfyUI 0.36: inputs autogrow exigem **chaves dotted** (`ref_images.ref_image_0`,
  0-based); torch 2.3.1 precisa do shim `torch_customop_shim` + `torch_compat_24_shim` (RMSNorm,
  F.rms_norm, add_safe_globals) — ver sessão 2026-09-18.

## QA de vídeo (lição de 2 reprovações do dono)
- Stills aprovam, vídeo reprova: QA = **grade multi-frame** (≥6 frames equidistantes + tile)
  inspecionada visualmente + **dono como juiz final**. Reprovado 2×: LTX (péssimo) e chunks
  (distorção — smear t≈18s e frame escuro t≈24s detectados na grade ANTES do dono).
- Guardar sempre: grade + prompt_ids + seeds + tempos por ato (proveniência).

## Receita H3-16GB (D6/P7 — Willian IA Ilpwa9vqZ7s + trilha 2674 cues)
- **H3 Easy** (custom node third-party): I2V+T2V+R2V num workflow só — ⚠️ QUARENTENA R87
  (sentinel) antes de instalar (P7 pendente do dono).
- **Qwen3-4B no lugar do Qwen 32B** (text encoder leve) + **LoRA turbo** (≈-40% tempo, n=1).
- **Live preview** + SageAttention (bypass Ctrl+B) — Sage é NVIDIA-only: inútil na Vega.
- **Faixas de pesos**: 66GB base → médios → leve 21GB (ref2va int8 + VAE + LoRA).
- **Host**: RAM folgada + SSD/NVMe (offload joga p/ RAM); música H3 exige API (limite).
- Peculiaridades 0.36: chaves dotted p/ autogrow; shim torch 2.3.1 (ver sessão 2026-09-18).

## Quando NÃO renderizar local
- RAM disponível < 12GB ou swap livre < 20GB → abortar antes de submeter (teto empírico).
- Alternativas: cloud (chave no opencode.jsonc) ou Colab (`colab-h3-mascote-30s.ipynb`).
