# Biblioteca de Canais — lote2 2026-09-17 (2 links, apoio cognitivo: ComfyUI vídeo + 3D)

> Status: **INGERIDO 2026-09-17** — 2/2 novos com transcrição auto-sub PT-orig (yt-dlp 2026.08.19).
> Tema do pedido (visão-edge) **DIVERGIU de novo**: 0 vídeos de VLM edge/inspeção (sem Florence-2/Moondream/SmolVLM/Qwen2.5-VL/YOLO/mmproj-inspeção).
> Lote real = ComfyUI vídeo T2V local (1) + ComfyUI image-to-3D + Blender (1). Decisão R94: arquivo lote2 separado (não append no lote-17d),
> pois o tema efetivo é P2-asset-pipeline, não visão-edge.
> Falhas de legenda traduzida EN/ES (HTTP 429 YouTube) nos 2 vídeos — registrado só o PT-orig; originais baixaram sem retry.

## Canais do lote (novos ou reforçados)

| Canal | Foco útil | Etiquetas | Status |
|---|---|---|---|
| @VITOR JERE (PT-BR) | ComfyUI vídeo local (LTX-2.5 T2V, RunPod template, testes de velocidade × qualidade) | [S-ca][L-e] | NOVO — 1 vídeo no lote (hjsixN0Jhq0) |
| @Willian IA (PT-BR) | Assets 3D/jogos com IA no ComfyUI (TRELLIS.2 + "Pixal 3D", Blender, otimização de malha) | [S-ca][L-e] | NOVO — 1 vídeo no lote (KBvtZqjPsDc) |

## Vídeos do lote (com veredito nos dois trilhos)

| Vídeo | Título (yt-dlp) | Autor | Trilho (a) visão/guardrail | Trilho (b) P2 vídeo/ComfyUI | Uso / Status |
|---|---|---|---|---|---|
| hjsixN0Jhq0 | LTX 2.5 no ComfyUI: Vídeo T2V em SEGUNDOS! É o modelo mais rápido! Mas e a qualidade? — 19:59 | VITOR JERE | BAIXA (vídeo generativo, sem VLM/inspeção; metodologia de stress-test de prompt-aderência transfere p/ avaliação de guardrail) | **ALTA** (workflow T2V ComfyUI nativo/template, timings locais, operação RunPod, cache de tokens) | Transcrito PT-orig 373 cues (746 brutos). Veredito: velocidade >> qualidade vs Minimax H3 |
| KBvtZqjPsDc | Crie Assets 3D e Jogos com IA no Piloto Automático (100% Grátis) — 52:25 | Willian IA | BAIXA (geração 3D, sem VLM; QA de topologia de malha é mentalidade de inspeção, não ferramenta) | **MÉDIA-ALTA** (image-to-3D no ComfyUI com tiers de VRAM + pipeline Blender de otimização; companion direto do vídeo GPT-6/Stefan-3D do lote-17d) | Transcrito PT-orig 1416 cues (2832 brutos). Atenção especial ~8:09 = instalação do custom node via git em `custom_nodes` |

## Números técnicos acionáveis (com cue/timestamp do VTT original)

- **hjsixN0Jhq0 (LTX-2.5 T2V no ComfyUI, PT)**: claim oficial no site: vídeo 10s em 6.8s local (placa B200, verbatim do autor "se não me engano") + ~23s via API, vs Minimax H3 180s [00:03:24–00:03:40]. Autor discorda do claim de qualidade (truco): Minimax acerta de 1ª, LTX exige 5–6 rodadas p/ encaixar [00:04:00–00:04:18]. Setup do autor: RunPod (template oficial SEM suporte ao workflow → 2º ComfyUI no último commit, porta extra 8189) [00:07:54–00:08:37]; workflow nativo dos templates ComfyUI, modelo variante menor (não-full) + 2 text encoders + 2 VAEs (vídeo+áudio) + upscaler embutido (gera em baixa e upscale) [00:04:51–00:05:35]. Timings medidos ao vivo: 10s de vídeo em 1:30 e 1:33 (primeira pessoa/mata, shooter) [00:10:38/00:11:24]; 10s em 1:45, kart 1:30 [00:14:00–00:14:35]; 5s em 17s com tokens em cache vs 29s com tokens frescos (tokenização+text-encoder explicam o delta) [00:15:19–00:15:25/00:17:54–00:18:03]; 1:18 p/ 10s no teste do macaco [00:17:29]. Multishot (multi-corte com personagem consistente em 1 rodada) não testado — plano de maquinário de shorts 60s [00:05:53–00:06:37]. GPU citada verbatim: "RTX 4500 de 32 GB" [00:09:49–00:09:53] — FLAG: modelo não confere (4500 Ada = 24GB); provável confusão com RAM do pod. Prompt-engineering via ChatGPT com regras do site (mini-RAG) p/ stress: lutas, render de texto, 1ª pessoa [00:09:07–00:09:36].
- **KBvtZqjPsDc (image-to-3D no ComfyUI + Blender, PT)**: stack = ComfyUI Windows Portable + update + custom node via `git clone` em `custom_nodes` (~8:09, nome ouvido como "Pixaroma" — FLAG: verificar nome exato do repo) + workflows da "ferramenta" (Browse Templates → "3D": TRELLIS.2 [Microsoft, verbatim] + "Pixal 3D" [verbatim, mapear] em image-to-3D) [00:06:39–00:10:29]. Duas variantes por modelo: LowRAM p/ placas básicas vs HQ + PBR textures (só em placa forte) [00:10:41–00:10:47]. Timings do mantenedor do workflow: TRELLIS.2 LowRAM — RTX 2060 6GB = 2:10 vs RTX 4090 24GB = 0:25 [00:20:00–00:20:09]; workflow parrudo — 2060 = 40min vs RTX 5060 Ti 16GB (autor) = ≤5min [00:20:36–00:20:42]. Parâmetro default 1536 (subir só se a placa aguentar, senão crash) [00:23:04–00:23:13]. Ponto negativo central: topologia de malha IA = densa/confusa (ex.: 700k triângulos) [00:05:43–00:05:52]; otimização no Blender (gratuito) = −96%, machado ficou com 3,7% do peso [00:05:56–00:06:10]; ganho alegado no jogo ≈80% [00:46:32]. Comparativo Trellis vs Pixal (mesma ref, gatinho): sem grande diferença no LowRAM; HQ ganha em textura/PBR [00:29:55–00:30:12]. Timestamps-capítulo da descrição: exemplos 02:37, ponto negativo 05:35, dependências 06:36, workflow 14:34, comparações 29:10, otimização 36:56/40:30.

## Recomendações dos autores (síntese)

- VITOR JERE: LTX-2.5 = iteração ultra-rápida (rode 5–6x até encaixar); Minimax H3 = qualidade de 1ª; não conserte o template RunPod oficial — suba 2º ComfyUI atualizado na porta 8189; reuse prompt (tokens em cache) p/ cortar tempo ~40%.
- Willian IA: 3D grátis local = ComfyUI (LowRAM em 6GB) + Blender p/ retopologia/otimização (malha IA crua é inutilizável em jogo); compare LowRAM vs HQ na mesma imagem antes de escolher; texto→3D via ChatGPT p/ refinar o prompt da imagem de referência.

## Tese do lote2

**Zero evidência nova p/ VLM edge/inspeção (gap visão-edge segue aberto — 2º lote seguido). O valor é 100% P2-asset-pipeline: (1) LTX-2.5 como gerador T2V de iteração rápida no ComfyUI local (doutrina: velocidade p/ rascunho, modelo maior p/ final); (2) image-to-3D local com tiers de VRAM documentados (2060-6GB viável em LowRAM) + Blender como etapa obrigatória de otimização (−96%). Junto com o vídeo GPT-6/Stefan-3D do lote-17d (custo cloud + MCP Unity), forma-se o triângulo: gerar barato local (LTX/TRELLIS) → otimizar (Blender) → montar com agente (Unity MCP).**

## Impacto na spec P2 / stack de visão

1. **P2 spec § render local — ADIÇÃO CANDIDATA**: LTX-2.5 (T2V segundos, workflow template nativo) como Tier-rascunho de vídeo; TRELLIS.2-LowRAM (2:10 em 6GB) + Blender (−96% malha) como pipeline de assets 3D. Ambos locais, sem custo cloud — testar em quarentena R87 antes de canonizar.
2. **Stack de visão (skill guardrail) — NÃO MUDA** (nenhum VLM/inspeção nos 2 vídeos).
3. **Doutrina de quant/VRAM — REFORÇA**: tiers explícitos por VRAM (6GB/16GB/24GB) com timings medidos; token-cache como alavanca de latência (17s vs 29s).

## Falhas brutas / pendências honestas

- Legendas traduzidas EN (`hjsixN0Jhq0.en`, `KBvtZqjPsDc.en`) e ES (`hjsixN0Jhq0.es`) → HTTP 429 YouTube em todas as tentativas (com backoff 13–14s); registrado só PT-orig. ES de KBvtZqjPsDc nem tentado (mesmo bucket de rate-limit) — pendência opcional.
- `pt` e `pt-orig` vieram idênticos nos 2 vídeos (alias do YouTube) — mantido `pt-orig` como canônico.
- Nomes ouvidos via auto-sub sem verificação: "Pixaroma" (custom node, ~00:07:27), "Pixal 3D", "Trelis 2", "LHRAM/LowRAM", "Minimx H3", "RTX 4500 32GB" — FLAGGED acima; confirmar contra descrição/repos antes de citar como fato.
- Descrições puxadas desta vez (links RunPod ref + capítulos Willian) — repos/modelos (links nº 1/2 do comentário fixado de KBvtZqjPsDc: ComfyUI Portable + custom node + workflows) ainda não extraídos como URLs — próxima varredura.
