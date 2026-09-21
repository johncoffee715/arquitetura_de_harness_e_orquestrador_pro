# Biblioteca de Canais — lote misto 2026-09-17d (7 links, tema previsto visão-edge DIVERGIU)

> Status: **INGERIDO 2026-09-17** — 6/6 novos com transcrição auto-sub (2 PT-orig + 2 ES-orig + 2 EN), yt-dlp 2026.08.19. 1/7 DEDUPE.
> Tema provável do pedido (visão computacional/VLM/edge + ComfyUI) **NÃO se confirmou**: 0 vídeos de VLM edge/inspeção industrial (sem Florence-2/Moondream/SmolVLM/Qwen2.5-VL/YOLO/mmproj-inspeção). Lote real = LLMs locais quantizados (2) + ComfyUI cloud (1) + modelo stealth cloud (1) + tradução edge (1) + game-gen agentic (1).
> DEDUPE: `Dp5MpUOrmNI` já ingerido no lote 2026-09-17c (transcrição `textos, pdf e esquemas/Dp5MpUOrmNI-transcricao-PT.md`, 778 cues) — não re-transcrito; revisado sem delta (Chiara/Higgsfield = cloud, sem mudança de veredito).
> Falhas de legenda PT traduzida (HTTP 429 YouTube) nos 4 vídeos ES/EN — registrado só o idioma original; retry com backoff 12-15s resolveu o original, traduzido ficou pendente.

## 6. Canais do lote (novos ou reforçados)

| Canal | Foco útil | Etiquetas | Status |
|---|---|---|---|
| @Nichonauta (ES) | Quants extremas locais (Qwen3.8-Flash-Next GSQ-RCO, Qwen3.8-27B, MoE) — já ATIVO §1, reforçado | [L-e][A-m] | ATIVO — 1 vídeo no lote (nzsAJFW9rso) |
| @RayCodingCorner / Ray Codes (EN) | Builds locais práticos (Hy-MT2 tradução edge, LFM2.5-VL, Breeze TTS, YuE2) — já ATIVO §1, reforçado | [S-ca][H-e] | ATIVO — 1 vídeo no lote (z1E6h2Rc-j0) |
| @Matheus Battisti – Hora de Codar (PT-BR) | Coding-agents/notícias IA (Union Alpha stealth, Unlazy, Karpathy) — já citado §2, reforçado | [S-ca] | ATIVO — 1 vídeo no lote (aurtWKQ9zgc) |
| @Sansão Seara – Inteligência Artificial (PT-BR) | ComfyUI prático sem GPU (Colab T4, uncensored, Z-Image Turbo) | [S-ca][L-e] | NOVO — 1 vídeo no lote (gZcExW2J6WE) |
| @Ricardo Bertran (ES) | Comparativos locais rigorosos (Qwen3.6 vs Gemma4, Qwen local, Ollama) — já citado §2, reforçado | [L-e] | ATIVO — 1 vídeo no lote (LKuflAKJVfE) |
| @Stefan 3D AI (EN) | Game-gen agentic longa-duração (GPT-6 + Unity/Unreal MCP) | [S-ca] | NOVO — 1 vídeo no lote (9lFE4T7iZKM) |

## 7. Vídeos do lote (com veredito nos dois trilhos)

| Vídeo | Título (yt-dlp) | Autor | Trilho (a) visão/guardrail | Trilho (b) P2 vídeo/ComfyUI | Uso / Status |
|---|---|---|---|---|---|
| Dp5MpUOrmNI | Como criar sites com IA que NÃO parecem feitos com IA (Claude Code + Higgsfield) — 14:17 | Chiara Costa | BAIXA (sem VLM) | BAIXA (cloud) | **DEDUPE** — veredito lote-17c mantido: MÉDIA p/ landing/mascote, cloud fora do render local. Sem delta |
| nzsAJFW9rso | Cuantización Extrema de Qwen 3.8 Flash Next 🚀 ¿Mantiene la CALIDAD en Hardware Limitado? — 12:29 | Nichonauta | **MÉDIA-ALTA** (único com mmproj visão + GSQ-RCO + offload SSD; teste é texto, não inspeção) | BAIXA (sem diffusion; lição quant transfere) | Transcrito ES-orig 575 cues.closest do lote p/ stack visão-local |
| z1E6h2Rc-j0 | Destroys Google Translate? Tencent's New 440MB AI Runs 100% Offline (Hy-MT2 Review) — 11:01 | Ray Codes | **BAIXA-MÉDIA** (tradução, não visão; menciona parear com VLMs Qwen2.5-VL-2B/LFM2.5 + OCR screenshot) | BAIXA (sem vídeo; útil p/ legendas locais) | Transcrito EN-orig 653 cues |
| aurtWKQ9zgc | Lançou o Union Alpha: grátis, sem dono e a 1 ponto do Opus 5 (testei tudo) — 13:39 | Matheus Battisti | BAIXA (cloud stealth, sem peso local) | BAIXA (coding-agent cloud, sem ComfyUI) | Transcrito PT-orig 699 cues. Valor = fallback nuvem R20 |
| gZcExW2J6WE | Como Rodar ComfyUI Sem Censura Sem GPU (2026) — 13:02 | Sansão Seara | BAIXA (image-gen uncensored, não QA/VLM) | **ALTA** (ComfyUI cloud-overflow: T4 16GB, Drive trick, Z-Image Turbo) | Transcrito PT-orig 671 cues. Complemento direto P2 |
| LKuflAKJVfE | Qwen 3.6 35B A3B vs Gemma 4 26B A4B: ¿por qué uno es MUCHO más rápido? — 11:50 | Ricardo Bertran | BAIXA (LLM texto) | **BAIXA-MÉDIA** (serving MoE: IQ2 vs Q4, 12GB; transfere p/ P2/GM) | Transcrito ES-orig 659 cues |
| 9lFE4T7iZKM | I Ran GPT-6 for 3 Days Non-Stop and It Created This… — 16:03 | Stefan 3D AI | BAIXA (sem VLM/edge) | **MÉDIA-BAIXA** (não-ComfyUI; long-horizon agentic + custo assets transfere) | Transcrito EN 815 cues. Cloud-only |

## Números técnicos acionáveis (com cue/timestamp do VTT original)

- **nzsAJFW9rso (Qwen3.8-Flash-Next GSQ-RCO, ES)**: 180B total = 125B + 6B ativos + 51B n-grams (+4B MT); FP original ~360GB [00:01:12]. IQ2_XS = 68GB anunciados, 63.3GB em disco + mmproj visão 865MB [00:02:10–00:02:52]. Setup: RTX 3060 12GB + 128GB RAM (usa <64GB) [00:02:17–00:02:21]; 41 camadas experts em CPU, resto GPU [00:03:28]; ctx 131072 + KV Q8 + TurboQuant-style [00:04:04–00:04:07]; GPU ~10-11GB + RAM ~37GB (<40GB vs 360GB full) [00:08:26]. Throughput ~9 tok/s sem n-gram/MTP [00:09:26: 53min p/ ~30k tokens]; prompt-limite = 5h p/ 130k tokens e estouro de ctx sem resposta [00:10:58]. Conclusão do autor: prefere modelos menores (90 tok/s) p/ iteração.
- **z1E6h2Rc-j0 (Tencent Hy-MT2, EN)**: 1.8B leve (4/6/8-bit GGUF) + 30B server (só 3B ativos) [00:01:14–00:01:18]. Leve = 440MB (3.6GB orig) [00:01:22/00:03:11]; fórmula VRAM ≈ params×bits×1.2 → 1.8B-Q4 ≈ 1.2GB VRAM, roda em CPU [00:02:26–00:02:29]. 16-bit 1.8B ≈ 4GB (RTX 3050); 30B ativos ≈ 14GB pesos / 8GB VRAM (GPU high-end/Mac Studio). Comercial OK (licença permite), top-1 em instruction-following/formatting, 88% vs APIs comerciais com <0.5GB [00:05:34]. Pareamento VLM: Qwen2.5-VL-2B / LFM-2.5 p/ screenshot→OCR→tradução, latência sub-segundo em 8GB RAM + 4GB VRAM [00:04:13–00:04:19]. Demo: SRT 1:24 traduzido HI+ES em 2-3 (unidade do vídeo; lido como min) com timestamps preservados.
- **aurtWKQ9zgc (Union Alpha stealth, PT)**: free via OpenRouter + OpenCode Zen + Kilo (VS Code) desde 16/set [00:01:09–00:01:32]; suspeito família GLM (pós-GLM-5.3-Flash via Ox-alfa). Ctx ~260k / resposta ~130k [00:02:06–00:02:11]; trava em prompt muito longo (responde por promptinhos). Multimodal texto+imagem [00:02:41]. Bench Klein (parceiro, viés): ~1pt de GPT-6-Astra e Opus 5 [00:03:13–00:03:15/00:08:47]. Uso: coding-agents e frontends; latência alta sob demanda.
- **gZcExW2J6WE (ComfyUI sem GPU, PT)**: Colab free = T4 16GB, 5:30h/dia renováveis [00:00:12–00:00:16/00:02:15–00:02:41]. Multi-conta (1 conta/vez) → 16h+/dia [tail]. Drive 15GB intacto via symlink/atalho: modelos (ex. Qwen3-4B ~7GB, Z-Image, VAE, text-encoder) fora da cota. 1ª geração lenta (load modelo Drive→VRAM), seguintes rápidas. Z-Image Turbo = gerador open sem censura na opinião do autor; também gera vídeo/música (aulas futuras). Sem números de steps/CFG/resolução no trecho.
- **LKuflAKJVfE (Qwen3.6-35B-A3B IQ2 vs Gemma4-26B-A4B Q4, ES, RTX 5070 12GB)**: Q1 matemática 720 pacotes (90/180/135/210/105): Gemma ~35 t/s vs Qwen ~128 t/s, empate qualidade [00:03:16–00:03:54]. Código (janela consecutiva max-soma): Qwen ~100 t/s vs Gemma ~38 t/s [00:05:40]. Instruções ES + contexto longo com distratores/contradições: Qwen ~132 t/s / >130 t/s vs Gemma ~37 / ~33 t/s, ambos corretos [tail]. Caveat honesto do autor (2x): quants diferentes (IQ2 vs Q4) — gap não é só arquitetura [00:04:09–00:04:14/00:09:39–00:09:43]. Veredito: empate qualidade, Qwen vence no uso diário pela velocidade; Gemma tem mérito em 12GB com quant maior.
- **9lFE4T7iZKM (GPT-6 games, EN)**: 1B tokens / 3+ dias + resets p/ zombie shooter Unity [00:00:02]; iteração realista (personagens/armas) = 12h + 149M tokens [00:03:30]; total jogo 1 = 1.29B tokens / ~50h agente (~100h reais) [00:08:37]. Jogo 2 (GTA6 Unreal 5, amigo) = 2B tokens / 4+ dias non-stop. Assets: $40-85 (Tripo/Hexville team), ~51 modelos 3D, 24 vídeos ref, 247 falas IA. MCP: Unity CLI oficial (Codex/Claude) ou Ankle Breaker Unity MCP (MCP+skills) [00:01:53–00:02:11]; Unreal = lento, single-chat (recompile). Tese: one-shot = dead-end; iteração (2D proto → 3D FPS → realismo) + skills/MCP; GPT-6 ótimo em low-poly/stylized/VFX/som, fraco em rigging/prédios/carros (manual 3x mais rápido).

## Recomendações dos autores (síntese)

- Nichonauta: GSQ-RCO mantém qualidade em IQ2_XS, mas em PC fraco o throughput (9 t/s, 5h/130k) mata a iteração — desliga/throttle reasoning ou desce de modelo.
- Ray Codes: tradução 100% local (Hy-MT2 440MB) + GGUF por VRAM + parear com VLM pequeno p/ OCR; comercial OK.
- Battisti: Union Alpha grátis agora (OpenRouter/Zen/Kilo), hype com cautela (stealth coleta prompts, bench do parceiro, trava em ctx longo).
- Sansão Seara: sem GPU → Colab T4 + multi-conta + symlink Drive; Z-Image Turbo p/ sem-censura.
- Bertran: em 12GB, meça velocidade + qualidade juntas e declare a quant (IQ2 vs Q4 invalida duelo cego); repo com comandos na descrição.
- Stefan 3D: p/ game-gen, itere pequeno, dê MCP+skills ao agente, gere assets caros (carro/portas/prédios) em ferramenta 3D dedicada em vez de tokens.

## Tese central do lote

**Lote acidentalmente fora do tema: zero evidência nova p/ VLM edge/inspeção visual (nenhum Florence-2/Moondream/SmolVLM/Qwen2.5-VL testado, nenhum YOLO/QA industrial, nenhum mmproj de inspeção). O valor real está em (1) quant/offload extremo (GSQ-RCO + N-gram no SSD + IQ2 vs Q4) como doutrina de VRAM p/ P2/GM; (2) ComfyUI cloud-overflow (T4 + multi-conta) como retaguarda do render local; (3) edge-translation como pipeline de legendas. Nada no lote refuta a stack de visão nem a spec P2 — só confirma que o gap visão-edge continua aberto e deve ser suprido por survey dirigido (Canais §1: Ray/LFM2.5-VL, Nichonauta/mmproj).**

## Impacto na spec P2 / stack de visão (o que muda, exatamente)

1. **P2 spec § render local — NÃO MUDA; adiciona retaguarda cloud documentada**: gZcExW2J6WE dá o procedimento Colab T4-16GB (5:30h/dia/conta, multi-conta, symlink Drive p/ furar 15GB) como overflow quando a Radeon Pro VII 16GB estiver ocupada. Não substitui o Tier-A/B local; entra como apêndice operacional.
2. **Stack de visão (skill guardrail) — NÃO MUDA; 1 padrão novo aproveitável**: nzsAJFW9rso prova mmproj (865MB) + LLM gigante carregável em 12GB VRAM + RAM com parte das experts em CPU (41 camadas) e N-grams no SSD — padrão reutilizável quando o VLM de inspeção for escolhido (ex.: Qwen2.5-VL/MM-Proj análogo). Nenhum modelo de inspeção foi testado aqui.
3. **Doutrina de quant p/ GM/P2 — REFORÇA (com caveat)**: LKuflAKJVfE + nzsAJFW9rso juntos mostram que (i) IQ2 pode empatar qualidade com Q4 em uso real, mas (ii) duelo IQ2-vs-Q4 não prova superioridade arquitetural — declarar sempre a quant (nota p/ futuros crivos R83/R97).
4. **Pipeline de legendas — GANHO IMEDIATO**: z1E6h2Rc-j0 (Hy-MT2 440MB/Q4-1.2GB, CPU-ok, comercial) é candidato a tradutor local PT⇄ES⇄EN do pipeline R90, emparelhado com VLM pequeno p/ OCR — testar em quarentena R87 antes de canonizar.
5. **Fallback nuvem R20 — SINAL, não canonização**: Union Alpha (aurtWKQ9zgc) e GPT-6 (9lFE4T7iZKM) são cloud-only, com custo/token opaco (GPT-6: 1.29-2B tokens por jogo, $40-85 só de assets) — entram no radar R20/R87, sem tocar spec local.

## Falhas brutas / pendências honestas

- Traduções PT (yt-dlp `--sub-lang pt`) p/ nzsAJFW9rso / z1E6h2Rc-j0 / LKuflAKJVfE / 9lFE4T7iZKM retornaram HTTP 429 (rate-limit YouTube) — registrado o idioma original (ES/EN-orig). Retry: backoff 12-15s funcionou p/ originais; traduzidas ficam como pendência opcional (conteúdo já ingerido no original).
- gZcExW2J6WE: `pt` e `pt-orig` vieram idênticos (699/671 cues duplicados por alias do YouTube) — mantido `pt-orig` como canônico.
- 9lFE4T7iZKM lista 8 faixas EN + pt-BR manual no `--list-subs`; baixado só `en` auto (815 cues) — suficiente; `pt-BR` humano ficou como pendência opcional.
- Descrições completas (links de repos/modelos: Arctic/ArcticLatent não é deste lote; Bertran GitHub; Ray GitHub; Sansão Colab notebook) não foram puxadas (yt-dlp `--print description` não executado) — próxima varredura pode extrair URLs de repos/Colab p/ `biblioteca-canais.md` §3.
- Nenhum vídeo do lote cita Florence-2/Moondream/SmolVLM/Qwen2.5-VL-testado/YOLO/inspeção QA/llama.cpp mmproj-inspeção — gap visão-edge permanece; sugerir survey dirigido (busca `site:youtube.com SmolVLM2 radar industrial`, `Florence-2 defect detection ComfyUI`, `Qwen2.5-VL llama.cpp mmproj GGUF`).
