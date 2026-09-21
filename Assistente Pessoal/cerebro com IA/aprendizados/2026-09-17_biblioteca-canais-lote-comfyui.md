# Biblioteca de Canais — lote ComfyUI/video-gen 2026-09-17c (6 vídeos)

> Status: **INGERIDO 2026-09-17** — 6/6 com transcrição (5 PT + 1 EN), yt-dlp 2026.08.19.
> Foco do lote: ComfyUI + geração de vídeo local (relevância filtrada p/ P2: Radeon Pro VII 16GB ROCm).
> Nota de correção: o lote §7 da `biblioteca-canais.md` anotou "Qwen3.5-27B" no Director Studio —
> o título oficial diz **Qwen3.8-27B** (ver spec P2 §1.2). Mantido o registro antigo por histórico.

## 6. Canais do lote (novos ou reforçados)

| Canal | Foco útil | Etiquetas | Status |
|---|---|---|---|
| @Willian IA (PT-BR) | IA open-weights local p/ PC fraco: MiniMax H3, Wan2GP, YuE2 música, ComfyUI MCP | [L-e][S-ca] | NOVO — 4 vídeos no lote (7rzGKcHY1a0, 0dme9aIJhC4, Ilpwa9vqZ7s, -fNe0O7xyo0) |
| @Arctic Latent / ArcticLatent (EN) | Setup Linux p/ IA + ComfyUI installer + Flux ControlNet workflows (github.com/ArcticLatent) | [S-ca][L-e][A-m] | NOVO — 1 vídeo no lote (rAQXkBLrKak) |
| @a_chiaraa (PT-BR) | Sites premium com IA (Claude Code + Higgsfield/Seedance 2.0) — já citada na spec P2 §1.4 sem ID; agora com ID | [S-ca] | ATIVO — 1 vídeo no lote (Dp5MpUOrmNI); Higgsfield é cloud |

## 7. Vídeos do lote (com veredito P2 e números)

| Vídeo | Título (yt-dlp) | Autor | Etiquetas | Uso / Status |
|---|---|---|---|---|
| 7rzGKcHY1a0 | Adeus IAs pagas: Nova IA gera vídeos insanos em PC fraco (100% GRÁTIS) — 45:57 | Willian IA | [L-e][S-ca] | **ALTÍSSIMA p/ P2** — H3 ComfyUI (12GB VRAM stock; pesos 66/40/34/21GB; 720p≈0.9MP; FL2VA vs R2V; FL2VA Pruned 20B vs 33B) + Wan2GP PC fraco (5-6GB→5s/124f@480p≤832×480; 8-9GB→15s) + FLUX 3 só API (R$63; parkour fail, realista bom). Transcrito PT 2295 cues |
| 0dme9aIJhC4 | JÁ ERA! Qualquer um vira PRO no ComfyUI agora! (ComfyUI MCP) — 22:02 | Willian IA | [S-ca][L-e] | **ALTA (processo)** — ComfyUI MCP: LLM instala modelos + cria workflow do zero + testa (Flux 2 Klein 4B; Crea 2 Turbo FP8 + LoRA Warm Pastel; upscale 4K c/ textura). Transcrito PT 1128 cues |
| rAQXkBLrKak | The Ultimate Linux AI Setup: ComfyUI, Arctic Tools & Flux (Full Workflow Guide) — 40:03 | Arctic Latent | [S-ca][L-e][A-m] | **ALTA** — Fedora +15% vs Windows; tier VRAM (<12GB→Q3); GGUF swap (diffusion loader + dual-clip GGUF); 4x-UltraSharp 1216→4864 (mesmo modelo do P2); @25:05 = samplers Euler vs DPM++, CFG Flux=1. Transcrito EN 1960 cues |
| Ilpwa9vqZ7s | INSANO: Otimizei o MiniMax H3 ao MÁXIMO — 49:22 | Willian IA | [L-e][S-ca] | **ALTÍSSIMA** — custom node H3 Easy (I2V+T2V+first-last+R2V unificados); encoder Qwen 32B→Qwen3-4B; LoRA turbo; música c/ H3; live preview + SageAttention. @2:02 = merge dos workflows. Transcrito PT 2674 cues |
| Dp5MpUOrmNI | Como criar sites com IA que NÃO parecem feitos com IA (Claude Code + Higgsfield) — 14:17 | Chiara Costa | [S-ca] | **MÉDIA** — Higgsfield/Seedance 2.0 = cloud; padrão hero-loop reaproveitável p/ landing/mascote. @2:48 = Etapa 2 refs anti-genérico. Transcrito PT 778 cues |
| -fNe0O7xyo0 | Esqueça o Suno! A melhor IA de música local chegou — 30:01 | Willian IA | [L-e][S-ca] | **MÉDIA-BAIXA vídeo / ALTA trilha** — YuE2 local no ComfyUI (partitura→música; ckpts 4GB vs 8GB; mín 4GB VRAM; cover=checkpoint+audio encoder). Transcrito PT 1366 cues |

## Números técnicos acionáveis p/ o P2 (com cue)

- **H3 pesos (7rzGKcHY1a0)**: base 66GB / médios 34-40GB / leve 21GB → 12GB VRAM [00:12:12–00:12:34]. Stock ComfyUI mín 12GB VRAM [00:06:50, 00:08:23]; autor roda em RTX 3050 8GB [00:07:45].
- **720p no workflow H3** = ajuste ~0.9 megapixel [00:14:26–00:14:30].
- **Wan2GP (lê-se "U/One 2GP" no auto-sub) [00:25:05–00:26:11]**: 5-6GB VRAM → 5s (124 frames) @480p (máx 832×480); 8-9GB → 15s; HD só em placa melhor + upscale depois. App = Wan2GP Desktop Launcher (venv Python, pastas checkpoints/LoRAs/output configuráveis).
- **H3 variantes (Wan2GP)**: FL2VA (T2V/I2V/first-last-frame) vs R2V/Omni-reference (áudio+imagem+vídeo ref) [00:31:27–00:31:52]; FL2VA Pruned 20B vs 33B [00:31:52–00:31:58].
- **H3 Easy (Ilpwa9vqZ7s)**: custom node `comfy-minimax-H3-Easy` unifica os dois workflows; nó único de mídia [00:01:38–00:03:37]; encoder Qwen3-4B (do template Crea 2) no lugar do Qwen 32B padrão [00:13:13–00:15:55]; LoRA turbo reduz tempo drasticamente [00:33:36–00:34:11]; SageAttention opcional (Ctrl+B bypass) [00:12:30–00:12:43]; live preview [00:43:25+].
- **Arctic (rAQXkBLrKak)**: Fedora +15% no mesmo workflow Comfy vídeo vs Windows [00:00:46–00:00:56]; tier C (<12GB) → quant Q3 [00:11:08–00:11:14]; Flux dev FP8 + dual-clip FP8 [00:18:45–00:19:11]; GGUF = trocar p/ Unet Loader GGUF + Dual-CLIP Loader GGUF (~12GB, ex. Q3) [00:36:50–00:38:29]; 4x-UltraSharp 1216→4864 [00:35:57–00:36:29]; ControlNet = XLab Union Pro p/ Flux [00:29:26–00:29:32]; @25:05 = samplers (Euler criativo/wild vs DPM++ clean/sharp), scheduler, steps/seed, CFG Flux sempre 1 [00:24:01–00:25:23].
- **ComfyUI MCP (0dme9aIJhC4)**: install via página (comentário fixado) + prompt ao LLM [00:01:22–00:01:55]; Flux 2 Klein base 4B (ultrapassado) [00:03:13–00:03:29]; Crea 2 Turbo FP8 + LoRA Warm Pastel + força/steps [00:04:04–00:04:19]; workflow 4K upscale + textura gerado do zero e testado [00:05:00–00:05:23].
- **YuE2 (-fNe0O7xyo0)**: 2 checkpoints (texto→música; música→cover) [00:13:28–00:13:44]; tamanhos ~4GB vs ~8GB [00:14:11–00:14:19]; mín 4GB VRAM, só GPU [00:14:21–00:14:27]; cover = checkpoint 3B-BF16 + audio encoder [00:21:37–00:22:01]; benchmark próprio > Suno V5/V6 mas best-of-8 (não comparável) [00:11:51–00:11:57].
- **FLUX 3 (7rzGKcHY1a0 [00:40:56–00:45:32])**: só API paga, sem open-weights; R$63 de teste; parkour = fail miserável vs H3; realista/cinemático (líquido, física carro/barco) bom; 5s c/ 95 créditos. Watch, não base.
- **Higgsfield (Dp5MpUOrmNI [00:07:00–00:07:28])**: plataforma cloud (imagem/vídeo/áudio/lip-sync/personagens, top modelos); Etapa 3 = vídeo loop na Hero. Cloud → fora do render local; padrão reaproveitável.

## Recomendações dos autores (síntese)

- Willian IA: H3 é o melhor custo/benefício open p/ vídeo local; PC fraco → Wan2GP; H3 Easy + encoder 4B + LoRA turbo p/ otimizar; YuE2 p/ música local; Flux 3 aguardar open-weights.
- Arctic Latent: Linux (Fedora/CachyOS) p/ +15%; ArcticDownloader escolhe quant por tier de VRAM/RAM; GGUF p/ <12GB; 4x-UltraSharp p/ upscale final.
- Chiara Costa: copy (Claude) → design system de refs reais (Behance) → vídeo loop Hero (Higgsfield); nunca deixar a IA decidir identidade sozinha.

## Tese central do lote

**MiniMax H3 open-weights é o novo teto prático de video-gen local em VRAM modesta (12GB com o build leve 21GB; 16GB com folga p/ offload) — e há um ecossistema de otimização (H3 Easy, encoder Qwen3-4B, LoRA turbo, Wan2GP) que empurra o piso até 5-6GB. Nenhum vídeo do lote cita LTX/Wan/Hunyuan/AnimateDiff/VACE/RIFE. O P2 (LTX-2B Tier-A + H3 Tier-B) está confirmado e refinado, não refutado.**
