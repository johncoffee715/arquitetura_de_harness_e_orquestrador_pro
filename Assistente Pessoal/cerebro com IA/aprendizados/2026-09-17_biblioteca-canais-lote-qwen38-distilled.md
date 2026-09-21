# Biblioteca de Canais — lote Qwen3.8-distilled 2026-09-17e (1 vídeo, tema DIVERGIU do lote ComfyUI)

> Status: **INGERIDO 2026-09-17** — 1/1 novo com transcrição (PT+EN), yt-dlp 2026.08.19.
> Pedido: lote-comfyui (6/6 DEDUPE confirmados em `2026-09-17_biblioteca-canais-lote-comfyui.md`) + 1 link novo `_YRUGkzllyA`.
> Tema do link novo **DIVERGIU**: não é ComfyUI/vídeo — é small-LLM local (Qwen 3.8 2B/4B/9B distilled p/ laptop). Lote próprio (R94), não seção do lote-17c.

## 6. Canais do lote (novos ou reforçados)

| Canal | Foco útil | Etiquetas | Status |
|---|---|---|---|
| @RayCodingCorner / Ray Codes (EN) | Builds locais práticos (Qwen-distilled small, Hy-MT2, LFM2.5-VL, Breeze TTS, YuE2) — já ATIVO §1, reforçado | [S-ca][H-e] | ATIVO — 1 vídeo no lote (_YRUGkzllyA) |

## 7. Vídeos do lote (com veredito nos dois trilhos)

| Vídeo | Título (yt-dlp) | Autor | Trilho (a) visão/guardrail | Trilho (b) P2 vídeo/ComfyUI | Uso / Status |
|---|---|---|---|---|---|
| _YRUGkzllyA | Qwen 3.8 2B /4B /9B Distilled: The Best Local LLM for Laptops? — 09:40 | Ray Codes | BAIXA (sem VLM/mmproj; LLM texto) | BAIXA (sem diffusion/ComfyUI; lição quant/VRAM transfere) | Transcrito PT+EN 609 cues cada. Valor = small local p/ harness low-end |

## Números técnicos acionáveis (com cue/timestamp do VTT original EN)

- **Lineup distilled (teacher→students)**: teacher 2.4T → students 9B/4B/2B [00:33–00:41]; 30.000 reasoning examples de alta qualidade vindos do teacher 2.4T [02:37–02:43].
- **2B (destaque)**: footprint 1.3GB; CPU-only 2–4GB RAM; 30–60 tok/s [00:51–01:00]; gotcha: 2GB é tight (SO mobile) → mín 4GB sistema recomendado [08:35–fim].
- **4B (meio)**: 2.5GB; sweet spot Q&A complexo + sumarização de arquivos longos, sem GPU cara [01:02–01:09].
- **9B + 27B**: smartest da linha; multi-step lógico/agentic 100% local [01:19–01:21].
- **Fórmula VRAM (autor)**: params×bits/8 ×1.2 overhead; 2B-Q4 = 2×4/8×1.2 = 1.2GB VRAM [01:56–02:14]; autor tem 4GB e roda fácil; abaixo disso roda em CPU/RAM [02:14–02:23]. GGUF single-file via HF (base tensor files ou GGUF comprimido) [01:34–01:52]; quant exibida 2-bit/4-bit na pasta models [05:20].
- **Bench vs base 3.5**: 2B = +26% reasoning (pure intelligence) [06:16–06:23]; 9B flagship = +20% step-by-step thinking [06:35–06:39].
- **Edge**: mobile 2–4GB RAM + Raspberry Pi citados [06:31–06:33]; exige execution engine atualizado (llama.cpp) [08:35–fim]; output vem com thinking tags → strip antes de apresentar [08:35–fim].
- **Demos no vídeo**: texture-data reasoning + audit report final; buy signal 90% confiança + targets [07:01–07:03]; high-volume breakout + 300% YoY demand surge [07:13–07:15]; anomalia 14 Aug $850 > $500 single-charge não-verificado + tabela sumário [07:29–07:38].
- **Repo**: github.com/47thtechcorner/RayCodes_Qwen3.8Distilled (código + readme passo-a-passo; link descrição + fixado).

## Recomendações do autor (síntese)

- Ray Codes: 2B p/ hardware fraquíssimo (CPU 2–4GB, 30–60 tok/s); 4B p/ Q&A/sumarização offline; 9B/27B p/ agentic sério local; dimensione por params×bits×1.2 e prefira GGUF; mantenha llama.cpp atualizado e remova thinking tags.

## Tese central do lote

**Qwen 3.8 distilled empurra o piso do reasoning local para 1.3GB/CPU (2B, 30–60 tok/s) com +26% sobre a base 3.5 — útil como camada fraca do harness (draft/router/supervisor low-end, fallback offline), sem interseção com o P2 vídeo (nenhum frame/diffusion/CFG/steps). Trilho (a) e (b): BAIXA/BAIXA; valor fora dos trilhos.**
