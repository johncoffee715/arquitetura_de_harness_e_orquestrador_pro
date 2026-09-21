---
source: "youtube DRcknO84EZk (Nichonauta)"
date: 2026-09-16
type: video
tags: [source/video, domain/ia, canal/nichonauta, llama-cpp, vlm]
etiquetas_4selfs: [S-ca, L-e]
asset_fonte: "textos, pdf e esquemas/DRcknO84EZk-transcricao-ES.md"
---
# Qwen3.5-4B + Claude Code 100% local via llama.cpp (Nichonauta)

## O suco (takeaways destilados)

1. **Modelo do vídeo**: Qwen3.5-4B (denso, Apache-2.0) — multimodal entrada (imagem+texto),
   janela 262.144 (expansível a ~1M), **MTP nativo** (draft model embutido → speculative
   decoding sem modelo separado), toggle de raciocínio, placar ~14 vs O3-mini-high ~13
   (nível "top de linha de 1,5 ano atrás", grátis e local). Quant testada: UD-Q4_KXL 2,99 GB
   + mmproj bf16 676 MB.
2. **Serving ótimo (receita)**: llama-server com KV q8_0, `min-p` para quebrar loops
   infinitos, `--image-min-tokens 1024` para visão rica, GPU full load ≈ 10,7 GB com ctx
   cheia + MTP + visão. Single request (`-np 1`) para estabilidade.
3. **Desempenho medido no vídeo**: ~93 t/s gerando (2,5k tokens, jogo Snake HTML5) na GPU do autor.
4. **Claude Code SEM conta Claude**: variáveis de ambiente apontando para o endpoint
   Anthropic-compatível do llama-server — funciona oficialmente, sem gambiarras.
5. **Demonstrações de agência**: o próprio agente instalou o MCP Context7 (lendo o manual
   em arquivo local), fez chamadas MCP de fato, entendeu imagem arrastada à CLI, navegou o
   filesystem do usuário. Zero falha de tool-call na sessão mostrada.
6. **Tese final (a citação de ouro do vídeo)**: a capacidade percebida = modelo × harness ×
   MCPs/skills/tools conectados — "nenhum modelo sabe tudo; com as ferramentas certas, até
   consulta internet". Frase gemea da arquitetura do nosso harness (R8 catálogo + R90 canais).

## Convergência DIRETA com a sessão atual
- É literalmente a receita do LLM-Fotógrafo: VLM GGUF + mmproj no llama-server :9188,
  JSON via grammar, MCPs ligando às ferramentas (ComfyUI :8188).
- **Qwen3.5-4B-UD-Q4_KXL entra no radar da fila fitragem** como candidato a futuros papéis
  (visão + 262k + MTP + tool-call zero-falha demonstrada).

## Entidades
- Nichonauta · Unsloth (quants UD) · Anthropic Claude Code CLI · Context7 MCP
