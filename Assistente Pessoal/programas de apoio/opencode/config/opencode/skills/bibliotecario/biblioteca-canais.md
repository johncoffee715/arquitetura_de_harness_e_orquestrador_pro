# Biblioteca de Canais de Apoio Cognitivo — do Bibliotecário (R90)

> Viva: acrescente canais por survey (R80) → classifique por missão → append + log.
> O Bibliotecário CONSULTA esta biblioteca antes de vasculhar a internet.
> Fonte para os 4 selfs do RAG cerebral (R86): cada canal carrega a(s) etiqueta(s).

Legenda de etiquetas: `[S-ca]` scaffolding · `[H-e]` healing · `[L-e]` learning · `[A-m]` ameliorative.

## 1. YouTube — LLMs locais e serving (núcleo)

| Canal | Foco útil | Etiquetas | Status |
|---|---|---|---|
| @nichonauta (ES) | MoE-350M/230M, Qwen3.5-0.8B, spec-decoding, quants extremas, Ornith/Qwen3.6 | [S-ca][L-e] | ATIVO — 10 transcritos (2B Qwen3.5-2B/Gema4E2B 179t/s simple-ok/code-fraco R45; Ling-3.0-Tiny eficiente 131K KV~0, veredito baixar; Gema4-12B QAT+MTP 9.8G 256K multimodal, melhor 12GB; MiniCPM-1B TERRIVEL (recomenda Qwen3.5-0.8B = nosso draft, validação externa); Tiel-Coder-35B PERDE do Qwen3.6-35B stock por muito (validação externa do GM); lote27: Qwen3.8-free/veloz, Qwen+ClaudeCode-local, Phi4mini-vale?, Qwen3.8-extrema-8GB, K2-0.9B-vs-Qwen3.5, Grok-Code-open-local; Unsloth/QLoRA fine-tuning ES) |
| @venelin_valkov (EN) | Testes locais llama.cpp c/ OpenCode: Ornith-1.5-35B, Qwen3.8-27B, DeepSeek V4, Nemotron 3.5 | [L-e][A-m] | ATIVO — refutação/apoio de canonização |
| @fahdmirza (EN) | K2 0.9/7/32B testado, TimesFM-3 local | [L-e] | ATIVO — 2 transcritos (novo: OmegaClaw agente simbólico Hyperon — loop contínuo, memória persistente, proof-trail, self-rewrite skills [S-ca]; PFlash+DFlash 10x prefill Qwen3.6-27B (transcrito pendente); Spark-X2.5-4B local, MiniCPM5-2B-SOTA-or-Scam)) |
| @tylerwhatsgood (EN) | Qwen3.8/GLM Flash, spec-decoding (DFlash2) | [L-e] | PARCIAL — EXL3 incompatível c/ llama.cpp (filtrado c/ motivo) |
| @The-Stack-ai (EN) | Serving (27B em 3090, 27B sem GPU), repos underrated, mini-PC | [L-e] | ATIVO |
| @Cloud-Codes (EN) | Qwen3.8-27B em 8.4GB, análise CUDA/distill | [L-e] | ATIVO (novo: 9.3GB-build vence p/ 12-16GB — embed/output-head bits custam pontos grátis, Unsloth 95x dl; Flash-Next: Qwen4-esqueleto 125B+6B+51B-phrasebook OFF-fast-memory (tese: vencer = menos params na VRAM, R21)) |
| @AI-with-Eric (EN) | Qwen3.8-27B coding 10h não-supervisionado, SWE-bench | [L-e][A-m] | ATIVO |
| @RayCodingCorner (EN) | TimesFM-3 330M CPU, Archify GitHub, Breeze TTS 3B local; sanoTTS 5MB CPU 50ms (edge-TTS); YuE2-3B música local 4GB | [S-ca][H-e] | ATIVO (LFM2.5-VL-3B visão; MiniCPM5-2B 128K reasoning — contrasta c/ MiniCPM-1B terrível; transcritos pendentes) |
| @BartSlodyczka (EN) | Ornith-35B no Mac, Qwen3.8 web design, voice agent open-weights | [L-e] | ATIVO |
| @WiseBuilder01 (EN) | Engenharia de coding agents (OpenCode×Cline×Pi), MCP spec, caching | [S-ca] | ATIVO |
| @Luke's Dev Lab (EN) | Tiel Coder 35B-A3B em 16GB local (classe do nosso GM) | [L-e] | NOVO (Qwen3.8-GSQ-RCO-16GB; Dirk-Qwen3.8-27B; transcrito pendente) |
| @Execute Automation (EN) | Qwen3.8-27B GSQ-RCO em Mac 24GB | [L-e] | NOVO — transcrito pendente |
| @Ricardo Bertran (ES) | Comparativa Llama3.1 vs Gemma4 vs Qwen3.8 | [L-e] | NOVO — transcrito pendente |

## 2. YouTube — infra e SO (suporte)

| Canal | Foco útil | Etiquetas |
|---|---|---|
| @portallinux (PT) | NVIDIA no Linux, drivers, hardware | [H-e] |
| @YouTuxChannel (EN) | Kernel, Xlibre, open source | [H-e] |
| @SirRobLinux (PT) | Linux desktop, notícias kernel | [H-e] |
| @AI ProgBr (PT-BR) | Muse Spark 1.3 ($0,20/1M, bate gigantes) — economia do fallback nuvem (R20) | [L-e] | NOVO — transcrito pendente (429) |
| @Ruan Braz (PT-BR) | Claude Ultracode multi-agentes | [L-e] | ATIVO (guia Claude Code iniciantes; transcrito pendente) |
| @AlejoGamerZone (ES) | Unity MCP + agente IA grátis (MCP p/ gamedev) | [S-ca] | NOVO — transcrito pendente |
| @Adriano AOli (PT-BR) | .env segurança/boas práticas (rel. hook sensitive-data) | [H-e] | NOVO |
| @Dev Knives (ES) | agentes em servidores (alívio do PC) | [H-e] | NOVO |
| @Facundo Corengia (ES) | Obsidian como sistema, não 2º cérebro (R86) | [L-e] | NOVO |
| @Matheus Battisti (PT-BR) | skill apresentações + RTK sessões 3x; Claude Code+Obsidian/Karpathy | [S-ca] | NOVO |
| @David Ondrej (EN) | 8 OpenCode use cases | [S-ca] | NOVO |
| @WorldofAI (EN) | Antigravity+OpenCode workflow | [S-ca] | NOVO |
| @Serial Entrepreneur (EN) | DeepSeek V4 no Antigravity | [L-e] | NOVO |
| @Rafael QuantBrasil (PT-BR) | agente Agno+FastAPI+Claude; Obsidian-cérebro p/ agentes IA; modelos 3D com IA | [S-ca] | NOVO |
| @Augusto Galego (PT-BR) | Akita+IA boas práticas | [L-e] | NOVO |
| @Breno LionLab (PT-BR) | harness de IA + disciplina (2 vídeos) | [S-ca] | NOVO |
| @Michelli Brito (PT-BR) | Embeddings (RAG) | [L-e] | NOVO |
| @nodesabe (PT-BR) | Obsidian audiovisual: wallpaper/background via AnuPpuccin + custom-background.css (ground truth que destravou o carrossel: tinta no .app-container, véu por backdrop-filter) | [S-ca][L-e] | NOVO — transcrito PT (trecho fundo 14:26–17:33), técnica absorvida na forja carrossel v1.2 |
| @LonSeidman (EN) | Lon.TV: hardware local p/ IA (Tesla V100 32GB barata), NAS, self-hosting | [H-e] | NOVO — vídeo V100 p/ Local AI |
| @attekitadev (PT-BR) | Obsidian em projetos com IA (workflow dev) | [S-ca][L-e] | NOVO |
| @DevSoutinho (PT-BR) | Mario Souto: guia Obsidian definitivo | [L-e] | NOVO |
| @andre-arcas (PT-BR) | Obsidian zero→avançado em 9min | [L-e] | NOVO |
| @AlexandreCardoso (PT-BR) | Clube Full-Stack: Obsidian bonito/conforto de leitura (CSS) | [S-ca][L-e] | NOVO |
| @linkingyourthinking (EN) | Nick Milo: sistema Obsidian (80% em 15min, novidades out/2025, iniciantes) | [L-e] | NOVO ×3 vídeos |
| @Navegamente (PT-BR) | setup 2º cérebro do zero | [L-e] | NOVO |
| @anajords (PT-BR) | 2º cérebro com IA (Claude Code + Obsidian) | [S-ca][L-e] | NOVO |
| @paivame (PT-BR) | Obsidian iniciantes + Zettelkasten p/ estudo | [L-e] | NOVO ×2 vídeos |
| @JessikaRocha (PT-BR) | anotações conectadas no Obsidian | [L-e] | NOVO |
| @TheEricMichaud (EN) | Obsidian SYSTEM-not-second-brain (converge R86) | [L-e] | NOVO ×2 vídeos |
| @FormacaoAI (PT-BR) | PARA + Zettelkasten | [L-e] | NOVO |
| @OutroRataque (PT-BR) | uso prático do 2º cérebro | [L-e] | NOVO |
| @RachelVMadrigal (EN) | tutorial iniciante 5min | [L-e] | NOVO |
| @benscyberlife (EN) | setup definitivo | [L-e] | NOVO |
| @InaraSouza (PT-BR) | 2º cérebro 2026 iniciantes | [L-e] | NOVO |
| @Itssssss_Jack (EN) | Hermes KB que self-improves (self-scaffolding) | [S-ca] | NOVO |
| @odysseas__ (EN) | guia completo learning tools | [L-e] | NOVO |
| @ShuOmi_Official (EN) | contraponto: largou o Obsidian (veracidade/visão crítica) | [L-e] | NOVO |
| @TimeGardenObsidian (EN) | Karlos: library linda sem código | [S-ca][L-e] | NOVO |
| @VladilenMinin (RU) | guia RU iniciantes (cobertura R80) | [L-e] | NOVO |
| @Elton_Labs (RU) | Obsidian na vida, em RU (cobertura R80) | [L-e] | NOVO |
| @Orafavoss (PT-BR) | Rafa Voss: Obsidian + Claude Cowork (método) | [S-ca][L-e] | NOVO |
| @JansenSec (PT-BR) | produtividade + anotar como mestre | [L-e] | NOVO |
| @kingloxii (EN) | jornada artista/escritor (uso não-técnico) | [L-e] | NOVO |
| @vinispira (PT-BR) | estudar + criar ideias | [L-e] | NOVO |
| @rhawk-mercado (PT-BR) | Ronnald Hawk/Mercado de IA: IA Vertical — HARNESS mais importante que modelo (tese convergente R44/R67) | [S-ca][L-e] | NOVO |
| @SampaioDev (PT-BR) | OpenCode+DeepSeek agente do ZERO, bots PDF/e-mail, freelancer Python | [S-ca][L-e] | NOVO ×3 vídeos (PZ5CXW2, uZK8ph, k0HfhGe) |
| @a_chiaraa (PT-BR) | Chiara Costa: sites com IA sem cara de IA (Claude Code + Higgsfield) | [S-ca] | NOVO |
| @CanalDotNET (PT-BR) | Extração texto em imagens/PDFs c/ Foundry+APISIX | [S-ca] | NOVO |
| @Duvenox (ES) | Orange Pi IA local grátis (edge) | [H-e] | NOVO |
| @xcreate (EN) | DeepSeek V4.1 24h local — Local AGI | [L-e] | NOVO |
| @AIProgBr (PT-BR) | Qwen3-Coder-Next melhor open-source p/ programadores | [L-e] | NOVO |
| @airevolutionx_pt (PT-BR) | SO totalmente baseado em IA | [L-e] | NOVO |
| @kipperdev (PT-BR) | Fernanda Kipper: Forward Deployed Engineer | [L-e] | NOVO |
| @0x5am5 (EN) | Samuel Gregory: Hermes escolhe modelo local | [L-e] | NOVO |
| @berolab (PT-BR) | 340s obcecado por programação | [L-e] | NOVO |
| @CountryBoyComputers (EN) | 7900 XTX + MI50-32GB Aliança ROCm | [H-e] | NOVO |
| @PandaMakingMoney (EN) | DeepSeek Harness vs Prime vs Pi vs OpenCode | [S-ca] | NOVO |

## 3. GitHub / HuggingFace — repos e modelos

| Repo | Uso |
|---|---|
| ggml-org/llama.cpp | motor (flags, GBNF, KV, FA — fonte de verdade do serving) |
| Nichonauta (HF) | MoE-350M/230M-ToMoE-GGUF, 1.2B-ToMoE-GGUF (quarentena→crivo) |
| unsloth / bartowski | quants comunitárias (R87: quarentena + crivo, nunca direto) |
| ISTA-DASLab/GSQ-RCO (HF) | GSQ+RCO per-tensor mixed-precision (403K dl/mês, Apache-2.0): IQ3_S task-lossless 11.8G, builds -mtp +0.35G, allocation-dumps+imatrix publicados [L-e] — doutrina: precisão por sensibilidade > uniforme (R76/R78); ver Fahd-UTJEKStLaok |
| DavidAU/dark-moes (HF collection) | 24 MoEs uncensored criativos [L-e] — Llama-3.x 18-47B, Mistral, Qwen3, GLM-4.7-Flash-CODE (37.4k★/418); quarentena R87; sem fit imediato (todos ≥17B); shortlist futuro: GLM-CODE p/ proposer, Qwen3-24B-A4B p/ refuter-CPU |
| Archify (ratificado p/ vídeo RayCodingCorner) | visualização de codebase (converge c/ skill archify) |
| unsloth/Nemotron-3-Nano-30B-A3B-GGUF | Nemotron híbrido Mamba-2 (arch `nemotron_h_moe` carrega!; IQ3 16.9GB; crivo 1.8/6 loops) [L-e] — paradigma validado, exemplar instável |
| unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF | Qwen3-Coder qwen3moe (IQ3 12GB; crivo 2.7/6, T4 perfeito!) [S-ca][L-e] — melhor coder testado, quarentena code-specialist |
| unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF | Devstral usa arch `mistral3` (carrega!; Q4 13.35GB; crivo 0.9/6 vazio/eco) [L-e] — SWE-bench não traduziu |
| unsloth/Magistral-Small-2509-GGUF | Magistral usa arch `llama` (carrega!; Q4 13.35GB; crivo 0.5/6 eco-loop) [L-e] |
| ibm-granite/granite-4.1-{3b,8b}-GGUF | Granite híbrido SSM (arch `granite` carrega!; 3B Q4 2GB crivo 2.0/6 schema-1.0-via-chat; 8B crivo 2.9/6 T4 0.8!) [S-ca][L-e] — melhor small, quarentena roteador/supervisor |
| bartowski/Qwen3.8-27B-GGUF | Qwen3.8 oficial (IQ3 11.76GB; crivo 2.9/6) [L-e] — quarentena reserva |
| mradermacher/Qwen3.8-27B-ComfyUI-GGUF | FrankenMoE ComfyUI Q2_K (10.12GB; crivo **3.1/6 melhor não-GM**, supera base!) [L-e][A-m] — R87 parcialmente refutado; quarentena challenger-record |
| DavidAU/Qwen3.8-27B-TURBO-*-MTP-GGUF | FrankenMoE TURBO c/ MTP-head (IQ3 13GB; crivo 2.5/6; think queima budget) [L-e] — R87 confirmado p/ este exemplar |
| bartowski/c4ai-command-r-v01-GGUF | Command-R 35B (Q3 16.4GB; crivo **0.2/6 pior geral**, scraps de fórum!) [L-e] — dataset contaminado visível |
| unsloth/gpt-oss-20b-GGUF + lmstudio-community/ERNIE-4.5-21B-A3B-PT-GGUF | gpt-oss (único poison-resistant!) + ERNIE (poison 1.0) — ambos apagados pós-campanha, registros no decision-log [L-e] |
| microsoft/BitNet (build) | bitnet.cpp: server+cli compilados (target llama-server exigiu TOOLS+COMMON=ON); i2_s regenerado mas smoke de geração FALHOU sem maquiagem [S-ca][H-e] |
| ornith-ai/Ornith-1.5-9B-GGUF | ex-GM 9B (Q5 6.19GB; crivo 2.6/6 T4 0.8, think leaky) [L-e] — conta mas não disciplina |

## 4. Docs e FAQ (referência viva)

- `tranquileiras/autofagia e helenização/rag_cerebral_cognitivo_regra_universal.md` (R86, v2.0)
- `Downloads/rag_cerebral_cognitivo_otimizacao_moe.md` (conflitado 05/09: 9 refutações + 4 confirmações)
- `Downloads/files/` — PACOTE EXAMINADO E DESCARTADO (ver decision-log linha-defesa-exame)
- `https://docs.anythingllm.com/installation-desktop/linux` — docs AnythingLLM RAG local (instalação Linux)
- `tranquileiras/autofagia e helenização/lista apoio auditoria-moe-gguf-huggingface-set2026.md` — auditoria MoE-GGUF set/2026 (nativos+FrankenMoE+compat MI50/48GB; fatos novos: ERNIE-4.5-21B Q3 10.5G cabe na VRAM; GLM-4.7 MXFP4 17.3G; Qwen3.6 UD-IQ1_M 10G) [L-e]

## 5. Descartados com motivo (não re-survey sem mudança)

@PandaMakingMoney, @datascienceinyourpocket (SaaS/hype) · @MarkGadala (uncensored/vídeo off-mission) ·
@PCExpert186 (reparo hardware RU) · UCc-Nvq1/UCNMCT (subscriptions) · tyler-EXL3 (formato incompatível) ·
t-LEOVSxysg ADATA NO PARAGUAI (economia off-mission) · ZACsLS2Gawc MARIA MADALENA (religião off-mission).

## 6. Canais indicados pelo usuário (apoio cognitivo geral — lote 2026-09-09)

| Canal | Foco útil | Etiquetas | Status |
|---|---|---|---|
| @VKav (ViktorKav) | Apps minimalistas locais (Buzz/Slack 159MB), comportamento multi-agente OpenAI; Obsidian+Claude Code no trabalho | [S-ca][L-e] | ATIVO — 2 vídeos no lote |
| @TaoofAI (EN) | IA open source aplicada (Director Studio OSS c/ Qwen3.5-27B) | [S-ca][L-e] | ATIVO — 1 vídeo no lote |
| @codigofontetv (PT-BR) | Porta de entrada programação (Gabriel Fróes + Vanessa Weber, 773k subs, desde 2016; Compilado podcast) | [L-e][S-ca] | ATIVO — survey 2026-09-10: notícias IA/coding agents (DeepSeek-liberdade, carta OpenAI+Anthropic, MYTHOS eng-social); didático base |
| @leonardobissoli (PT-BR) | Claude Code, harness/looping/graph engineering, setup local Ollama | [S-ca] | ATIVO — 1 vídeo no lote; converge c/ skill engenharia-de-harness |
| @devknives (ES) | Agentes em servidores (alívio do PC) — já citado na §2, promovido a apoio geral | [H-e][S-ca] | ATIVO — survey 2026-09-10: agentes em servidores, ADE, MCPs (6-MCPs-setup, Hermes-MCP), Kimi+OpenCode, local-vs-API |
| @CodeSimple (UC6YGMbIuzh_9nrTWpFZMK3Q) | Programação simplificada (escopo a confirmar) | [L-e] | ATIVO — survey 2026-09-10: tutoriais práticos Spring Boot/JPA/Git/NPM (escopo confirmado: programação tradicional, apoio didático) |
| @Cognix (UCWZugiDyg24JI4ClOI9ZcNA) | Arquiteturas que quebram gargalo de VRAM (Flash-Next) — confirmado via título da página | [L-e][A-m] | NOVO — 1 vídeo no lote (PxD1rF-kvns); link repetido = duplicata ignorada |
| @leorobit (PT-BR) | IA local prática (Maple Preview 20B/1Bativo, custom-llama.cpp, Mac Mini) | [L-e] | NOVO — 1 vídeo (8j5o-1gIHsQ); transcrito PT 213 cues ingerido |
| @betterstack | Observabilidade (uptime/logs/status pages) + IA local mínima (Needle 2 14MB) | [H-e][L-e] | ATIVO — 1 vídeo no lote (M24yg6ZM7-I); converge self-healing/monitoramento |
| @Fazt (emergente) | Repos open-source que substituem assinaturas de IA | [S-ca][L-e] | NOVO — 1 vídeo (5JJgfcJxyyg) |
| @AISeeKing (emergente) | Modelos grátis p/ OpenCode | [S-ca][L-e] | NOVO — 1 vídeo (JEGM4dwKZSA) |
| @AICodeKing (emergente) | Coding agents locais (Qwen/Hermes/OpenCode/OpenClaw) | [S-ca][L-e] | NOVO — 1 vídeo (SjBBUB1njBc) |
| @Manuel Cabrera Caballero / DriveMeca (ES) | IA local aplicada (imagem local sem nuvem) | [L-e][S-ca] | NOVO — 1 vídeo no lote (YD0LbCaLOv4) |
| @TechWithTim (EN) | Coding agents locais avaliados com honestidade | [S-ca][L-e] | NOVO — 1 vídeo no lote (8JRJq4EEdik) |

## 7. Vídeos de apoio cognitivo (lote 2026-09-09)

| Vídeo | Título (oembed) | Autor | Etiquetas | Uso / Status |
|---|---|---|---|---|
| IIuWBVwzJzI | LFM 2.5: I Ran 230M AI Model on My CPU! | Ray Codes | [L-e] | Small-first R87 |
| K9RD4EgFAvU | Como funciona um harness corporativo de IA | Breno Vieira LionLab | [L-e][A-m] | Apoio cognitivo R86 — harness corporativo, orquestração |
| OvvrEpMoodU | Finalmente testei o Google Antigravity para programar | Cortes do Rafael Quintanilha | [L-e] | Apoio R20 — fallback nuvem, janela curta |
| 4myNRufwdxQ | I Ran DeepSeek V4.1 Locally for 24 Hours... Local AGI is HERE!? 🤯 | xCreate | [L-e][A-m] | Apoio R45 — benchmark especulativo, debilidades/capacidades |
| o65mCkBNspY | Como usar Múltiplos modelos ao mesmo tempo e dar superpoderes ao Opencode | AI ProgBr | [L-e][A-m] | Apoio R80 — pesquisa multi-idioma, MoE não-oficiais |
| BiZHi9LSbkQ | O FreeLLMAPI te dá 4 bilhões de tokens grátis por mês (teste completo) | Matheus Battisti | [L-e] | Apoio R76 — onboarding LLM batch/KV/MTP |
| AuHPSkiOlo0 | Lançou o Grok Bot! Será que vale a pena? Testei tudo (que deu..) | Matheus Battisti | [L-e] | Apoio R79 — benchmark completo especulativo |
| hi5LhipHpv0 | DeepSeek Harness vs Prime Agent vs Pi vs OpenCode (2026) | Panda Making Money | [L-e][A-m] | Apoio R80 — pesquisa comunitária multi-idioma |
| 1wFbUGfBlxo | Extração de texto em imagens e PDFs usando IAs Generativas: um exemplo com Foundry + APISIX! | Canal dotNET | [L-e] | Apoio R86 — extração/transcrição pipeline |
| 6Z5UZW96FDQ | Buzz: o Slack do Jack Dorsey Cabe em 159 MB | ViktorKav | [S-ca][L-e] | Minimalismo local |
| 0LtdXQ_deUA | Eu Não Esperava Que Ele Fizesse Isso (= teste Astra 6 p/ 3D + vídeo educativo) | Macks Wendhell | [L-e][S-ca] | CLASSIFICADO via PT-subs (216 cues): modelo novo p/ criação 3D/motion + workflow skills/agents/hooks — ATIVO |
| SZrYOKxtJ-Q | Qwen 3.5 27B: A IA do Hype 100% Local e Grátis | Leonardo Bissoli | [L-e] | Canonização Qwen3.5-27B |
| OAgJyOWr0tY | Nuevo Qwen3.5 4B Q2: ¿Vale la pena esta Cuantización EXTREMA? | Nichonauta | [L-e] | Quant extrema (converge §1) |
| I_kc873zAow | IA Local para Programar: Qwen con llama.cpp y OpenCode | Nichonauta | [S-ca] | Setup executor local |
| A8UEvIPaAZo | Qwen3.5: Pequeño de PESOS ABIERTOS, Análisis Completo | Nichonauta | [L-e] | Análise Qwen3.5 |
| 6pUY79VJmxc | I Made Fable 5 and Qwen3.6 27B Build the same Web App | Token Chaser | [S-ca][L-e] | Comparativo agentic |
| YX90I23Ys1Y | Qwen3.5 27B Directs H3 \| Director Studio Open Source | Tao of AI | [S-ca][L-e] | Agente dirige vídeo OSS |
| s91eRxGn17A | RESPOSTA DA AMD AO DLSS 5 DA NVIDIA! | T-Rocha Hard Tec | [H-e] | Suporte-fraco (GPU) |
| KeIrjviQ3kk | O DLSS 5 ESTÁ EVOLUINDO RÁPIDO! OptiScaler | Teaser Games | [H-e] | Suporte-fraco (GPU) |
| L5CCF3IPcoY | Qwen 3.6 35B A3B: el Modelo MoE más RÁPIDO y EFICIENTE | Nichonauta | [L-e] | Classe do GM 35B |
| V1QrCqSoC38 | Qwen 3.5 2B: el MEJOR Modelo Pequeño MULTIUSO | Nichonauta | [L-e] | Small-first |
| okhh5h201w0 | JetSpec Locally: Breaking Speed Ceiling, Up to 9x | Fahd Mirza | [L-e][A-m] | Spec-decoding 9x |
| goEJypwd7XQ | Seu Agente de Código começa cego (o Graft resolve) | Matheus Battisti | [S-ca] | Contexto de agente (graft) |
| v88cvk6fBYU | Billions vs Bits: ¿Modelo GRANDE o PEQUEÑO? | Nichonauta | [L-e] | Tese small-first R87 |
| 5mVlLjMLv24 | As IAs da OpenAI Montaram uma Sociedade Secreta | ViktorKav | [L-e] | Comportamento multi-agente |
| -9OsXESRdaI | Ling3.0 Tiny: el Modelo MoE RÁPIDO para Programar | Nichonauta | [L-e] | MoE coding rápido |
| BdDVYNeX440 | Você Pode Rodar um Modelo de 177 Bilhões no PC? | Onde eu Clico | [L-e] | Serving gigante local |
| LgJREY0bcUU | Dirk Qwen 3.8 27B tested - Local LLM setup | Luke's Dev Lab | [L-e] | Setup 27B (converge §1) |
| KC-Dx9hj-e0 | Comparativa de Speculative Decoding | Nichonauta | [L-e][A-m] | Aceleração geração |
| xC0ZiB9CrO0 | Monetiza los TOKENS de tu LLM Local | Nichonauta | [L-e] | Economia fallback |
| qgV2XLln9DM | Train Your Own CPU TTS Model, Any Language/Voice | Fahd Mirza | [S-ca][L-e] | TTS CPU (converge Breeze) |
| Rq-b5umGldY | Cómo usar un MODELO GRANDE en GPU PEQUEÑA (Gemma 4 26B) | Nichonauta | [L-e] | Offload/VRAM (R21) |
| ERNNwzXWoSg | TurboQuant en llama.cpp: Reducir VRAM sin Perder Calidad | Nichonauta | [A-m][L-e] | Quant VRAM |
| V66RccByLbc | Qué es RAG en IA: evitar Alucinaciones con AnythingLLM | Nichonauta | [L-e][S-ca] | Apoio direto R86 |
| Ato5qq80XtM | OpenCode Desktop: Tutorial Completo (MCP, Skills, Agentes) | AloiTech | [S-ca] | OpenCode prático |
| C3SvSQwylW4 | Nunca te ensinaram Claude Code assim (GUIA COMPLETO) | Renato Asse | [S-ca] | Coding-agent |
| j_DZO06gSMk | Qwen 3.5 e Muse Glimmer fizeram a mesma feature (addendum) | Cortes do Rafael Quintanilha | [S-ca][L-e] | Comparativo agentic — converge §2 QuantBrasil |
| wY9P25ptf-4 | Muse Glimmer 30B: Instalar y Compilar con llama.cpp en tu GPU (addendum) | Nichonauta | [L-e][S-ca] | Modelo novo 30B local — flag p/ scout R87/quarentena |
| bEqh4ZwWYm4 | Liquid LFM 2.5: Modelo Extremadamente EFICIENTE y RÁPIDO (addendum) | Nichonauta | [L-e] | LFM eficiente — converge reflexo :9086 + IIuWBVwzJzI |
| mlGUBf1Mo2s | Qwen 3.5 + Ollama: AGENTE LOCAL que ENCUENTRA VULNERABILIDADES (addendum) | Ricardo Bertran | [S-ca][L-e] | Agente segurança local — converge §1 Bertran + security-methodology |
| H-xJ_7nZurY | Depois de uma semana: opinião sobre o Grok Bot (addendum) | Rafael Quintanilha – QuantBrasil | [L-e] | Review de agente — converge §2 QuantBrasil |
| GlRHi8SmmQ0 | Introducción a la Programación con IA: GUÍA COMPLETA desde Cero (addendum) — ⭐ PÉROLA DA STACK | Nichonauta | [L-e][S-ca] | 12:52, pub. 2026-09-09. Índice: prog. assistida c/ LLMs, fundamentos/história, Turing, revolução generativa, hierarquia IA, Python, RAG, temp/top-k/top-p, orquestração de agentes. Por que pérola: base didática teoria+prática p/ codar com IA sob disciplina de engenharia — converge proposer/executor, R61 sampling, RAG/R86 e skill sdd. Transcrito-desc pendente (yt-dlp subs) |
| 9qJIJz2HLws | Spec Driven Development (SDD): a melhor forma de programar com IA? (addendum) | Rafael Quintanilha – QuantBrasil | [S-ca][L-e] | SDD p/ coding-agents — converge skill sdd + §2 QuantBrasil — ATIVO |
| 3ll53QrbiN0 | COMO EXTRAIR UM TEXTO DE UM VÍDEO (addendum) | Ediel Costa | [S-ca] | Ferramenta extração — apoio direto pipeline transcrição — ATIVO |
| Te3Jfa8sLVI | IA para Transcrever Video em Texto (100% GRÁTIS) (addendum) | Chiara Costa | [S-ca] | Transcrição grátis — apoio pipeline — ATIVO |
| pAOOfeKYaSQ | How to Scrape ANY YouTube Video Transcript with n8n! (addendum) | AI Foundations | [S-ca] | Scraping via orquestrador n8n — apoio pipeline — ATIVO |
| PMQsuN5-g6E | Automating YouTube Transcription & Summarization with AI Agents (addendum) | OneClick IT Consultancy | [S-ca][L-e] | Transcrever+sumarizar c/ agentes — apoio pipeline — ATIVO |
| xca3Di02kVg | Qwen 3.6 35B: El nuevo modelo de PESOS ABIERTOS que REEMPLAZA a los Densos (addendum) | Nichonauta | [L-e] | Classe GM 35B open-weights — apoio learning — ATIVO |
| kIddP67Ux9Y | Ollama vs llama.cpp: Cuál es MEJOR para IA en Windows (addendum) | Nichonauta | [L-e] | Comparativo serving — apoio learning — ATIVO |
| DN4c6KrBOv8 | 5 Trucos para EXPRIMIR Qwen en Local con Ollama (addendum) | Ricardo Bertran | [L-e][S-ca] | Truques Qwen local — converge §1 Bertran — ATIVO |
| PxD1rF-kvns | Qwen3.8-Flash-Next: ¿El FIN de los LLM con cuello de botella de VRAM? (addendum) | Cognix (canal novo emergente) | [L-e][A-m] | Arquitetura Flash-Next/VRAM — ATIVO; Cognix entra na §6 como NOVO |
| mUFHiVir5KA | KAT Coder V2.5 Dev tested vs Base Qwen 35B A3B - 16GB Local LLM setup (addendum) | Luke's Dev Lab | [L-e] | Coder 35B-classe p/ 16GB vs base — ATIVO + flag scout-R87 (executor 16GB); converge §1 |
| M24yg6ZM7-I | I Can't Believe This AI Model Fits in 14 Megabytes (Needle 2) (addendum) | Better Stack | [S-ca][L-e] | Needle 2 14MB — converge skill roteador-hibrido/needle — ATIVO |
| 5JJgfcJxyyg | Dejé de pagar 4 suscripciones de IA por ESTOS repos (addendum) | Fazt | [S-ca][L-e] | Repos substituem subs — ATIVO |
| JEGM4dwKZSA | OpenCode's NEW FREE Model OPTIONS: People are IGNORING THIS! (addendum) | AISeeKing | [S-ca][L-e] | Modelos grátis OpenCode — ATIVO |
| SjBBUB1njBc | Qwen 3.6 27B + Hermes, OpenCode, OpenClaw: BEST LOCAL AI CODER (addendum) | AICodeKing | [S-ca][L-e] | Stack coder local — ATIVO |
| YD0LbCaLOv4 | Adiós a la nube: Convierte imágenes en segundos con esta herramienta local (addendum) | Manuel Cabrera Caballero | [L-e][S-ca] | Imagem local sem nuvem — ATIVO (visão segue R35-descontinuada até canonizar) |
| y2W4FNAuPEA | Deep dive on LLM Inference at Scale — Audible + Independent AI (addendum) | AI Engineer | [L-e][A-m] | Inferência em escala — apoio serving/otimização — ATIVO |
| 8JRJq4EEdik | Is Local AI Coding Actually Good? (addendum) | Tech With Tim | [S-ca][L-e] | Avaliação honesta de coding local — ATIVO |
| mgPj252Dek8 | Run a $10,000 AI Model at Home, Here's How (addendum) | David Ondrej | [L-e] | Serving de modelo caro em casa — ATIVO; converge §2 David Ondrej |
| LUKaaW_Rz9c | 6 MCPs That Changed How I Code With AI (Real Setup) (survey devknives) | Dev Knives | [S-ca] | Setup MCP real — converge MCPs do harness — ATIVO |
| GfjbBO8s_gI | This is how you do AGENTIC programming in 2026 (survey devknives) | Dev Knives | [S-ca][L-e] | Programação agentic — ATIVO |
| NPBZ-SxXWzo | How to run local AI on your computer. Stop paying for APIs! (survey devknives) | Dev Knives | [L-e] | Local vs API — converge R20 economia — ATIVO |
| DRcknO84EZk | Qwen en Claude Code: Programación LOCAL con IA y llama.cpp (survey nichonauta) | Nichonauta | [S-ca][L-e] | Qwen3.5-4B local p/ coding — INGERIDA (textos/DRcknO84EZk-transcricao-ES.md, 414 cues) — ATIVO |
| sYRz6Cjf8hE | Skill que FORÇA a IA entregar sistemas melhores! Unlazy (addendum) | Matheus Battisti | [S-ca] | Quality-enforcer p/ skills — converge gabaritos — ATIVO |
| OdK6iUHGamo | Proxy Atómico: Creé un Potenciador IA INFINITO y GRATIS (addendum pós-lote) | Nichonauta | [S-ca][L-e] | Proxy/free-tier p/ fallback nuvem (R20) — converge §1 |
| 8j5o-1gIHsQ | IA Local: rodei o MAPLE PREVIEW no Kit Xeon (addendum pós-lote) | Leo Robit | [L-e] | MoE 20B/1Bativo 5.3GB, 218tok/s Mac Mini, exige llama.cpp CUSTOM (Deep Grove fork!) — flag compat R87; transcrito PT ingerido |
| ctKNiHvZXOE | Gemma 4 26B vs Qwen 3.6 35B: qual roda melhor no Xeon? (addendum pós-lote) | Leo Robit | [L-e] | Xeon 2683v4+64GB: Qwen3.6 ~8-9tok/s vs Gemma4 ~10.7tok/s (QAT, 14GB, 4B ativos); Gemma menos assertivo; transcrito PT 354 cues ingerido |
| vKy0154ey90 | Nail Qwen 35B A3B tested - 16GB Local LLM setup (addendum pós-lote) | Luke's Dev Lab | [S-ca][L-e] | Nail-Qwen3.6-35B c/ MTP-head (peculiar-ragdoll, 18k dl; 36/48=75%, memoria excelente, MCP-Blender sofreu; prefere teal-coder); transcrito EN 427 cues ingerido |
| t-LEOVSxysg | ADATA NO PARAGUAI (imposto) | Papo Libertário | — | DESCARTADO §5 (economia off-mission) |
| ZACsLS2Gawc | MARIA MADALENA (arqueologia) | TIKTAL | — | DESCARTADO §5 (religião off-mission) |

## 8. Como usar nos 4 selfs + FAQ (R86)

| Self | Quando consultar | Exemplos do lote |
|---|---|---|
| self-scaffolding [S-ca] | Antes de criar skill/feature | Ato5qq80XtM, goEJypwd7XQ, YX90I23Ys1Y, qgV2XLln9DM |
| self-healing [H-e] | Antes de diagnosticar infra/serving | §2 + s91eRxGn17A/KeIrjviQ3kk (fraco) |
| self-learning [L-e] | Antes de canonizar/scout (R87) — APOIO, crivo local prevalece (R45) | L5CCF3IPcoY, v88cvk6fBYU, BdDVYNeX440, SZrYOKxtJ-Q |
| self-ameliorative [A-m] | Antes de otimizar (quant/spec) | okhh5h201w0, KC-Dx9hj-e0, ERNNwzXWoSg |

FAQ: credencial? Não (30/30 público; paywall = gap). Off-mission? Descarta §5 com motivo. Título genérico? MAPEAMENTO_PENDENTE + transcrever (yt-dlp). Fonte externa? APOIO (R45/R50); vídeo nunca canoniza sozinho (quarentena R87).

## 9. Pipeline de transcrição p/ ingestão RAG (guia do usuário helenizado 2026-09-09)

> Status ambiente (verificado): yt-dlp 2026.08.19 OK · `youtube-transcript-api` AUSENTE (`pip install` pendente).
> Rota padrão = yt-dlp (já instalado); yta-lib = opcional.

1. **yt-dlp (padrão)**: `yt-dlp --write-auto-sub --sub-lang "pt,en,es" --sub-format vtt --skip-download -o "/tmp/opencode/subs/%(id)s.%(ext)s" <URL>` → sanitizar VTT→txt (strip timestamps/cues `[Música]`) → salvar em `cerebro com IA/textos, pdf e esquemas/` → watcher do Bibliotecário reindexa no Qdrant.
2. **youtube-transcript-api (opcional)**: `pip install youtube-transcript-api` → script do usuário (get_clean_transcript, langs pt/en) — sem baixar áudio/Whisper; cai p/ yt-dlp se IP for rate-limitado.
3. **REST p/ orquestradores (n8n/Make)**: endpoint fino sobre o método 1; cloud (Supadata/AssemblyAI) só se local falhar — empírico local prevalece (R45).
- **Chunking**: 500–1000 tokens, overlap 10–15% (RecursiveCharacterTextSplitter ou equivalente local).
- **Metadados por chunk**: video_id + título + URL + etiqueta 4-selfs + origem (auto/manual) — citação direta no agente.
- **Fila de digestão**: 0LtdXQ_deUA CLASSIFICADO (216 cues PT) · GlRHi8SmmQ0 PÉROLA INGERIDA · lote tooling sob demanda. Prática padrão: aprendizados/2026-09-09_pratica-padrao-ingestao-transcricoes.md.

## Protocolo de agregação (obrigatório)

1. Survey (títulos recentes via yt-dlp flat) → 2. classifica (núcleo/suporte/descarta-c-motivo) →
3. append nesta biblioteca → 4. log no decision-log → 5. usa nos 4 selfs (R86) e no scout (R87).
Credenciais: NUNCA pedidas nem guardadas — público basta; members-only = gap registrado.
