---
setor: marca
tipo: spec-video
projeto: P2-video-20-30s-FullHD-macro-solda + loop-mascote
data: 2026-09-17
status: v1.0 — extração do vault concluída; veredito honesto: SEM spec melhor que LTX-2B no acervo
hardware_alvo: "AMD Radeon Pro VII 16GB (ROCm) + 32GB RAM"
stack_local_verificada: "ComfyUI 0.36.0 (decisao 2026-09-16, :8188 — OFF nesta sessão) + ltx-video-2b-v0.9.5.safetensors 6.3GB + sd_xl_base_1.0 6.9GB + t5xxl_fp8_e4m3fn 4.9GB (filesystem 2026-09-17)"
fontes: [biblioteca-canais.md §7, aprendizados/2026-09-09_biblioteca-canais-lote-usuario.md, textos/0LtdXQ_deUA-transcricao-PT.md, textos/YD0LbCaLOv4-transcricao-PT.md, marca/cenario-video-macro-solda.md, marca/brand-guide-academy-of-eletronic.md, marca/auditoria-consistencia-2026-09-17.md, benchmarks/2026-09-16-crivo-llm-fotografo-vlm.md, decisoes/2026-09-16-tabela-verdade-final.md]
---

# Spec técnica de vídeo P2 — extração do vault (2026-09-17)

## 0. Veredito executivo (R28 — PASSOU_CATEGORICO)

**Os links de apoio do vault NÃO contêm nenhuma spec de modelo de vídeo melhor nem mais viável que o LTX-Video-2B já instalado.**
Evidência: dos 3 vídeos candidatos, um (Astra 6) é agente *cloud* sem peso local, um (Director Studio) orquestra modelo *cloud* (MiniMax H3),
e um (NoConvert) é conversor de formato, não gerador. Nenhum cita VRAM, ComfyUI-nodes, fps ou resolução de diffusion local.
Detalhes nos §§1–2; o que falta levantar está no §6.

## 1. O que cada vídeo relevante realmente entrega

### 1.1 `0LtdXQ_deUA` — "Astra 6" (Macks Wendhell, 8:07, PT transcrito 218 cues) — FONTE: `textos, pdf e esquemas/0LtdXQ_deUA-transcricao-PT.md`

- **O que é o "Astra 6"**: "o novo modelo da Openii" — agente de código *cloud* estilo Codex, app desktop com skills/plugins na nuvem (cues 3–48).
  **NÃO é modelo diffusion local; NÃO roda no harness.**
- **Vídeo educativo**: gerado por prompt simples (~15 min de build, cues 62–65), motion graphics via código (skill estilo Remotion p/ Codex — o autor
  cita vídeo próprio anterior sobre "remotion pra Practice", cues 24–30). Saída = aula de biologia narrada, não footage fotorrealista.
- **Projeto 3D**: célula eucariótica navegável (web), **90 estruturas + 27 processos** a partir de prompt único (cues 119–122), referência livro Alberts via NCBI.
- **Spec técnica p/ P2: ZERO** — sem VRAM, sem nodes, sem fps/resolução, sem repo de peso. Descrição do vídeo = só links afiliados (Hotmart, notebook, Ryzen, HD, mic, webcam).
- **Aproveitamento residual**: padrão "agente planeja → código gera motion" (útil p/ end-card/HUD programático via Remotion/ffmpeg, NÃO p/ footage de solda).
- Correção de registro: o lote §7 dizia "216 cues" —Download atual retornou **218 cues PT** (consistente; classificação "3D/motion" mantida, com a ressalva *cloud*).

### 1.2 `YX90I23Ys1Y` — "Qwen3.8 27B Directs H3 | Director Studio Is Now Open Source" (Tao of AI, 12:32) — SEM legenda

- `yt-dlp --list-subs` retorna **"has no subtitles"** (verificado 2026-09-17) — sem transcrição possível por essa rota. Fonte = **descrição do vídeo** (yt-dlp --print, evidência abaixo).
- **Repo**: `https://github.com/ai2764/Director-Studio` (+ build portátil Google Drive + guia de instalação portátil no cap. 10:34).
- **Arquitetura real**: LLM diretor local **Qwen3.8-27B** (planeja história → quebra em shots → atribui personagem/figurino/cenário/prop → prepara prompts) +
  motor de vídeo **MiniMax H3 (H3 Ref2AV)** — modelo **cloud/API**, não local. Capítulos: Intro 00:00 · Story 01:26 · Asset Library 02:03 · Replanning 03:23 ·
  Layout Refs 04:27 · H3 Prompting 05:14 · Video Generation 05:38 · Mobile 06:39 · Continuity 08:29 · Changing Refs 09:08 · Install 10:34.
- **Ponte ComfyUI** (padrão reutilizável): workflow custom exportado em **formato API**, importado em Settings→Workflows→H3, validação contra nó
  `MiniMaxH3ReferenceToVideo` + seed, teste isolado com asset Picture. Exige ComfyUI rodando + custom nodes + MCP tools do Director Studio (`Install-Tools.cmd` no portátil).
- **Correção de registro**: o lote §7 anotou "Qwen3.5-27B" — o título/descrição oficial diz **Qwen3.8-27B**. (R28: título verificado via oembed/yt-dlp.)
- **Spec técnica p/ P2: ZERO modelo local novo** — mas o **padrão diretor-LLM → prompts por shot + refs** é diretamente reaproveitável (§4).

### 1.3 `YD0LbCaLOv4` — NoCloud Bulk Image Converter v3.0.5 (Manuel Cabrera, 10:54, PT 231 cues) — FONTE: `textos/YD0LbCaLOv4-transcricao-PT.md`

- **O que é**: conversor de formato em lote (Java, multiplataforma, GitHub, paralelo). PNG→JPG/TIF/BMP/GIF/ICNS. **Não gera imagem nem vídeo.**
- **Bug documentado**: não skipa destino existente — duplica (149→249 arquivos no teste).
- **Aproveitamento residual**: normalizar keyframes SDXL em lote; alternativa nativa já disponível (`mogrify`/ffmpeg).

### 1.4 Outros varridos e descartados (com motivo)

- `Te3Jfa8sLVI` (Chiara, transcrição grátis), `3ll53QrbiN0`, `pAOOfeKYaSQ`, `PMQsuN5-g6E` — pipeline de transcrição, não video-gen.
- `s91eRxGn17A` / `KeIrjviQ3kk` (DLSS 5/OptiScaler) — suporte-fraco GPU gaming; OptiScaler não serve a ComfyUI/ROCm.
- Canal `@a_chiaraa` ("sites com IA sem cara de IA — Claude Code + Higgsfield"): **Higgsfield é video-gen cloud**; sem vídeo ID no lote → gap, não evidência.
- `benchmarks/2026-09-16-crivo-llm-fotografo-vlm.md:40` — única menção video-gen no vault fora dos links: **stabilityai SVD (licença gated)** como alternativa de peso; sem download, sem teste.
- `raw/videos-harness-2026-08-10/` (11 transcrições lote R14/R23): tema harness/agentes LLM — fora do escopo vídeo.

## 2. Modelos rankeados (viabilidade em 16GB ROCm primeiro)

| # | Modelo | VRAM pesada | Resolução/fps plausível | Fonte | Veredito |
|---|---|---|---|---|---|
| 1 | **LTX-Video-2B v0.9.5** (img2vid) | **6,3 GB** safetensors em `checkpoints/` (verificado filesystem 2026-09-17) | 720p @24fps, clips ~5s (121 frames) por chunk; upscale pós | `decisoes/2026-09-16-tabela-verdade-final.md:44` + `cenario-video-macro-solda.md:8` + ls pesos | **BASE CANÔNICA P2 — único testável hoje** |
| 2 | SDXL base 1.0 | 6,9 GB em `checkpoints/` | keyframes 1024² p/ img2vid | mesmos que acima | keyframe/draft canônico |
| 3 | T5-XXL fp8 | 4,9 GB em `clip/` | text-encoder do LTX | ls pesos 2026-09-17 | dependência do #1, OK |
| 4 | SVD (Stability Video Diffusion) | desconhecida | desconhecida | `benchmarks/2026-09-16-crivo-llm-fotografo-vlm.md:40` (só menção "gated") | **GAP**: licença + sem peso + sem crivo |
| 5 | MiniMax H3 Ref2AV | cloud/API (fora do requisito local) | n/d local | descrição `YX90I23Ys1Y` | **DESCARTADO p/ render local**; padrão de orquestração aproveitável |
| 6 | "Astra 6" (Openii) | cloud/agente | n/a | `textos/0LtdXQ_deUA-transcricao-PT.md` cues 3–16 | **DESCARTADO** — não é diffusion |
| — | Wan 2.x / HunyuanVideo / Mochi / LTXV quants / AnimateDiff-ROCm | — | — | **ausentes no vault** | **GAP §6**: survey externo pendente |

> Nota de VRAM: 6,3 (LTX) + 4,9 (T5) ≈ 11,2 GB antes de VAE/offload — cabe nos 16 GB com folga p/Provided text, mas o crivo real é o primeiro render (motivo: `vae/` e `diffusion_models/` vazios; LTX embute VAE no checkpoint — confirmar no smoke test).

## 3. Workflow recomendado (LTX-2B; sem alternativa local evidenciada)

1. **Keyframes SDXL** (1024²) por shot a partir dos prompts de `cenario-video-macro-solda.md:29-33` + referência visual do mp4 canônico
   `avatar mascote da empresa.mp4` (1920×1088 @24fps, 5,2 s — `brand-guide:67`) como âncora de continuidade/personagem.
2. **img2vid LTX-2B**: 5 shots × ~5 s (121 frames @24fps cada, conforme decupagem S1–S5) — chunking obrigatório (modelo não sustenta 30 s contínuos).
3. **Montagem ffmpeg**: concat + end-card (logo ouro `logo 0.png` + equação oficial) + grade oliva `#A3A44A` + grão fino (regras `cenario:39-44`).
4. **Upscale**: 4x-UltraSharp p/ trechos sub-HD (ex.: mp4 "correndo" 1152×640) — **CONFIRMADO no filesystem** (`ConfyUI/models/upscale_models/4x-UltraSharp.pth`, 66.961.958 bytes, torch.load OK — verificado pelo GM 2026-09-17). Revisão da nota anterior: o falso-negativo desta linha veio de olhar o path externo `pesos confyui/upscale_models/` (não mapeado). RESOLVIDO.
5. **Interpolação temporal** (RIFE/film): gap — nada no vault, nada instalado.
6. **Loop mascote**: S5 (pull-out) cortado p/ end-card + loop do mp4 5,2 s como bumper; reels 9×16 e feed 1×1 centrados em S3/S4 (macro).
7. **Padrão importado do Director Studio**: LLM local (Qwen/NeoHorse do harness) como *diretor* — gera/revisa prompts por shot em conversa,
   com biblioteca de refs (personagem ouro-branco, bancada, macro-solda); ComfyUI em formato API p/ repetibilidade.

## 4. Decisões

### Tomadas (com fonte)

- D1: Engine = LTX-2B img2vid + SDXL keyframes + ffmpeg (`cenario-video-macro-solda.md:8`). **Mantida** — sem rival evidenciado.
- D2: Identidade ouro `#A3A44A` sobre preto; azul só apoio (`brand-guide:22-24,71-75`; R-1 da auditoria pendente de aprovação do dono).
- D3: Texto das fichas HUD = vetor recriado (IA corrompe microtipografia — `auditoria:49-59`); vale p/ textos no vídeo (end-card em overlay, nunca baked pelo diffusion).
- D4: `avatar mascote da empresa.mp4` (FullHD) = loop-base (`auditoria:66`).
- D5: ComfyUI :8188 + pesos no path com espaço `/home/johncoffee/pesos confyui/` (`tabela-verdade:44`; pesos **reverificados 2026-09-17**).

### Pendentes do usuário

- P1: R-1 da auditoria — canonizar ouro absoluto e re-cor de ~3 assets azuis (bloqueia paleta final do vídeo).
- P2: R-2 — saneamento tipográfico das fichas (bloqueia end-card com texto).
- P3: **ComfyUI OFF nesta sessão** (`ss`: nada em :8188; path de instalação não localizado) — revalidar path/start antes do render.
- P4: 4x-UltraSharp — informar path real ou reinstalar em `models/upscale_models/`.
- P5: Autorizar survey externo (§6) — Wan 2.1/2.2-FP8, HunyuanVideo, Mochi-1, quants LTX, RIFE-ROCm, estado Director-Studio (pode ter backend local novo).

## 5. Sem resposta (ficou sem fonte no vault)

- Nenhum número de VRAM/fps/resolução p/ qualquer modelo de vídeo além do LTX instalado (cujos números de regime ainda exigem smoke test).
- Nós ComfyUI exatos (VideoHelperSuite? KJNodes? RIFE? Upscale?) — vault não registra o graph instalado.
- Timestamps internos dos vídeos (transcrições limpas sem timecodes; capítulos só do Director Studio via descrição).
- Conteúdo do vídeo `tT5ya2HKazo` (mencionado na descrição do Astra) — fora do escopo pedido, não baixado.
- Repo Director-Studio não clonado nem auditado (código third-party → quarentena R87 + sentinel antes de qualquer uso).

## 6. Next steps propostos

1. Smoke test LTX-2B (S3 macro, 121f @24fps 720p) e registrar VRAM pico/tempo no `marca/` — vira a primeira spec *medida* do P2.
2. Localizar ComfyUI + nodes instalados; inventariar graph de vídeo existente.
3. Resolver P3 (start :8188). P4 RESOLVIDO (UltraSharp confirmado — ver §3.4).
4. Survey externo PARCIALMENTE FEITO (§7 MiniMax H3); restam: Wan 2.2-FP8 em 16 GB ROCm, HunyuanVideo 13B offload, Mochi-1, LTX-2B GGUF/quants, RIFE-ROCm.
5. Decisão P1/P2 do dono (paleta + tipografia) antes do render final.

## 7. Amendo 2026-09-17b — SURVEY EXTERNO: MiniMax H3 (pedido explícito do dono)

Fonte: comfy.org/minimax-h3, docs.comfy.org tutorials, minimax-h3.app local guide, HF MiniMaxAI/MiniMax-H3, Comfy-Org/MiniMax-H3.

**Fatos verificados:**
- Lançado 2026-07-31 (API) + **open-weights 2026-08-03** (H3-Base). 33B Omni Transformer (~13B AdaLN pré-computáveis).
- **Omni-modal**: T2V / I2V / first+last-frame / R2V (até 9 imagens + 3 clips vídeo + 3 áudios de referência) + **áudio estéreo nativo 32 kHz no mesmo forward**.
- Canvas nativo: **768p short edge** (16:9 ≈ 1344×768, ~1 MP, grid múltiplo de 32). Clips 5–15 s. 2K só via H3-Regenerate-2K (NÃO open-source ainda).
- Arquivos oficiais (Comfy-Org, reduced-memory): diffusion `minimax_h3_fl2va_pruned_int8_convrot.safetensors` **~21 GB** + text encoder `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` **~15,7 GB** + video VAE fp16 **~5,2 GB** + audio VAE fp32 **~0,6 GB** ≈ **42,5 GB de download total**.
- VRAM (guia, "planejamento, não garantia"): 12 GB possível com offload agressivo (lento); **16–24 GB "prático com offload"**; 32 GB+ confortável. Caminho documentado = NVIDIA/CUDA; **AMD/ROCm não documentado** (nossa Radeon Pro VII = terreno experimental). GGUF = só builds comunitários.
- ComfyUI 0.30+ com templates nativos H3 (temos 0.36.0 ✓; blueprint stock `Image to Video (MiniMax H3).json` já presente).
- **LICENÇA: MiniMax H3 Community License com TERRITÓRIO EXCLUÍDO = EU, UK, Coreia do Sul, EUA. Brasil NÃO está excluído** → uso local ostensivamente permitido; registrar revisão formal antes de uso comercial/publicado.

**Posicionamento no P2 (decisão de arquitetura, proposta):**
- **Tier A (agora)**: LTX-2B permanece base do entregável 20–30 s (cabe folgado em 16 GB, já instalado).
- **Tier B (upgrade hero)**: H3-Base local quando VRAM liberar — como *shot herói* (ex.: S3 macro-solda 10–15 s @1344×768 com áudio nativo) ou loop mascote premium; budget: ~42,5 GB disco + render lento com offload. Alternativa: H3 via API hosted p/ validar qualidade antes do download pesado.
- FullHD final continua sendo: render 768p → 4x-UltraSharp → 1080p (idêntico nos dois tiers).

**Pendente do dono:** autorizar (a) download dos ~42,5 GB H3 e (b) validação da cláusula territorial p/ uso comercial da marca.

## 8. Amendo 2026-09-17c — lote ComfyUI (6 vídeos)

Fontes: `aprendizados/2026-09-17_biblioteca-canais-lote-comfyui.md` + `textos, pdf e esquemas/{7rzGKcHY1a0,0dme9aIJhC4,rAQXkBLrKak,Ilpwa9vqZ7s,Dp5MpUOrmNI,-fNe0O7xyo0}-transcricao-{PT,EN}.md`.
Lote: 4× Willian IA (PT) + Arctic Latent (EN) + Chiara Costa (PT). 6/6 transcritos (5 PT + 1 EN, auto-sub).

### 8.1 O que muda no plano

- **Tier-B H3 REFINADO (não refutado)**: pesos oficiais em 4 faixas — base 66GB / médios 34-40GB / leve 21GB (7rzGKcHY1a0 [00:12:12–00:12:34]). Stock ComfyUI mín 12GB VRAM; build leve 21GB roda em 12GB → **nossa Pro VII 16GB comporta o leve com folga p/ offload**. Download Tier-B cai de ~42,5GB (guia Comfy-Org, §7) p/ **~21GB se escolhermos só o leve + VAE** — revalidar lista exata de arquivos no download.
- **Receita de otimização H3 em 16GB (Ilpwa9vqZ7s)**: custom node H3 Easy (unifica I2V/T2V/first-last+R2V) + text encoder **Qwen3-4B no lugar do Qwen 32B** + **LoRA turbo** (tempo cai drasticamente, qualidade cai pouco) + SageAttention opcional (bypass Ctrl+B) + live preview. **Adotar os 4 itens no Tier-B.**
- **Fallback PC-fraco documentado (Wan2GP, 7rzGKcHY1a0 [00:25:05–00:26:11])**: 5-6GB VRAM → 5s/124f @480p (≤832×480); 8-9GB → 15s; HD só + upscale. Não é nosso caso (16GB), mas é o piso de degradação se o H3 pesado não couber: render 480p + 4x-UltraSharp.
- **Upscale validado por terceiros (rAQXkBLrKak [00:35:57–00:36:29])**: 4x-UltraSharp 1216→4864 no workflow Flux — **o mesmo checkpoint do nosso P2**. Confiança no passo §3.4 sobe.
- **Path GGUF low-VRAM (rAQXkBLrKak [00:36:50–00:38:29])**: trocar diffusion loader → Unet Loader GGUF + Dual-CLIP Loader GGUF (ex. Q3 ≈ 12GB). Vale p/ H3 se o safetensors leve estourar VRAM.
- **Linux +15% (rAQXkBLrKak [00:00:46–00:00:56])**: Fedora rende +15% no mesmo workflow Comfy vídeo vs Windows (n=1, autor). Nosso host já é Linux — nenhum ajuste, só registrar que o número de regime deve ser medido aqui.
- **ComfyUI MCP (0dme9aIJhC4)**: LLM instala modelos + gera workflows do zero + testa (incl. upscale 4K c/ textura). **Adotar como método**: gerar o graph LTX/H3 de upscale via MCP em vez de montar nó a nó — mesma classe do padrão diretor-LLM do §3.7.
- **Trilha sonora local (YuE2, -fNe0O7xyo0)**: checkpoints 4GB vs 8GB, mín 4GB VRAM, cover = checkpoint + audio encoder. **Candidata à trilha dos 20-30s** (Tier-C, após vídeo pronto). Benchmark > Suno é best-of-8 do próprio autor — não comparável, testar de ouvido.
- **FLUX 3 = watch, não base (7rzGKcHY1a0 [00:40:56–00:45:32])**: só API paga (R$63 de teste do autor); parkour fail vs H3; realista/cinemático bom; 5s por 95 créditos. Reavaliar quando sair open-weights.
- **Higgsfield/Seedance 2.0 = cloud (Dp5MpUOrmNI)**: fora do render local; padrão hero-loop reaproveitável p/ landing/mascote (converge §3.6).
- **Nenhum vídeo cita LTX / Wan / Hunyuan / AnimateDiff / VACE / RIFE** — GAP §6 permanece p/ esses modelos (só Wan aparece como app Wan2GP, sem números de peso).

### 8.2 Decisões novas propostas

- D6: Tier-B H3 = build leve 21GB + H3 Easy + encoder Qwen3-4B + LoRA turbo (16GB com offload). Download total estimado cai p/ ~21GB + VAEs — confirmar lista de arquivos antes de baixar.
- D7: Graph de upscale (LTX e H3) via ComfyUI MCP, não manual.
- D8: Trilha via YuE2 local (Tier-C, pós-vídeo).
- D9: FLUX 3 em watch (sem ação até open-weights).

### 8.3 Pendentes novos do dono

- P6: autorizar download H3 leve (~21GB + VAEs) — substitui/alivia o P5a do §4 (42,5GB era o pack completo).
- P7: aprovar instalação do custom node H3 Easy + SageAttention (third-party → quarentena R87 + sentinel antes).
- P8: aprovar YuE2 p/ trilha (download 4GB ou 8GB).


## 9. Amendo 2026-09-18 — REPROVAÇÃO do render local LTX 0.9 + pivot definitivo p/ H3 R2VA (Colab)

**Veredito do dono (ordem direta)**: o vídeo 30s renderizado localmente com LTX 0.9.1 foi **REPROVADO por completo**
("output péssimo, todos foram reprovados; LTX 0.9 é péssimo para geração de vídeo, só é bom para imagem").
Arquivos deletados pelo dono de `video-mascote-30s/output/` (sobreviveu só qa-r105.json).

**Lições registradas**:
1. R105 gate visual é insuficiente p/ VÍDEO: a VLM de stills (Qwen2-VL-7B) aprovou frames individuais mas não
   julga coerência de movimento/qualidade dinâmica. Critério de vídeo requer: julgamento multi-frame + o dono.
2. Vega 20 local: paredes definitivas mapeadas — torch ≥2.4 sem kernels gfx906 (bloqueia ComfyUI 0.36, H3, LTX-2);
   decode do VAE 0.9.5 pendura a stack mesmo com T5 fp8/VAE antigo. Stack local útil p/ IMAGEM (SDXL/LTX img2img),
   não p/ vídeo de qualidade.
3. LTX 0.9.x = só para keyframes/imagens (validado empiricamente pelo dono).

**Decisão (D10)**: vídeo de qualidade = **MiniMax H3 R2VA via Colab T4** (nota Reddit do dono: 2h de filme por
US$6,96; 15s/60s) ou LTX-2.3 GGUF 22B (futuro). Entregável pronto:
`projetos/video-mascote-30s/colab-h3-mascote-30s.ipynb` — notebook autônomo com 3 fichas embutidas como
refs R2VA (identidade travada), 3 atos de 8s com áudio estéreo nativo + turbo 4-step, endcard ouro, montagem
ffmpeg master 1080p + reels 9×16. Um passo humano: abrir no Colab + login Google + Run all (~40min).

Modelos (paths Comfy-Org/MiniMax-H3): ref2va_pruned_int8_convrot (19,5GB) + ref2v_turbo_4step LoRA (1,8GB)
+ qwen3vl_32b nvfp4 (14,6GB) + video_vae fp16 (4,9GB) + audio_vae fp32 (0,6GB) ≈ 42GB no disco do Colab.
