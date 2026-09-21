# Otimização do 35B CPU — pesquisa multi-idioma + vereditos R88 (2026-09-06)

> Restrição: SEM mexer nos outros slots (sem VRAM, sem restarts alheios). Alvo: :8083
> Qwen3.6-35B-A3B-UD-IQ3_XXS CPU puro (6.5 t/s). Fontes: EN (docs llama.cpp, PR #22673,
> KGP-Talkie 45 configs, MoE-Lens/Lightning, Intel Xeon, HF MoE-offload, issues FA/KV),
> ZH (gitcode, borninfreedom, eogee, trilium, AWS-CN), RU (habr ×2), DE. Vault: sem
> artefato prévio (só menção) — verdade prévia vive no manifesto/decision-log.

## Vereditos por ideia (fatos · dados · veredito)

| # | Ideia | Fatos | Veredito |
|---|---|---|---|
| 1 | MTP (`draft-mtp`) | Merge #22673; GPU A10G +83% (26→48); **CPU x86 MoE −18%** (AWS 16.81→13.75), Graviton −40%; nosso GGUF SEM heads MTP (0/733); prefill −50% com MTP | **REJECT p/ CPU** (local 30/08 + AWS ×2). Condicional: se 8083 voltar ao hybrid/GPU → baixar MTP GGUF + A/B |
| 2 | Draft model (`draft-simple`) | Pipeline 2026 mudou (p_min default 0→footgun; `p_min=0.75` restaura); nosso binário TEM `--spec-type`; Qwen3.5-0.8B em disco (27 t/s, mesma família); RAM livre 21G (draft CPU, 0 VRAM); teste antigo −40% era pipeline velha | **TESTAR** (A/B barato, reversível; checar vocab antes) |
| 3 | ngram (`simple/map`) | Zero pesos; bom p/ saída estruturada (tool-call/JSON = staple do 8083); KGP: ngram-mod = perda líquida; simple/map não medidos na pipeline nova | **TESTAR** (1 flag, minutos) |
| 4 | DFlash | Exige checkpoint draft p/ Qwen3.6-35B — NÃO existe (só Qwen3 4B/8B, e com bug acceptance 0.15) | **REJECT categórico** |
| 5 | EAGLE-3 | Exige head treinada p/ o alvo — NÃO existe p/ Qwen3.6-35B | **REJECT categórico** |
| 6 | Atomic (fork turboquant + UDT-MTP) | Fork: turbo3 KV 4.3× + NextN +24-36% MoE; exige trocar o binário (trust/manutenção; quarentena R87); ganho em Xeon AVX2-sem-AVX512 não provado | **SCOUT**: baixar UDT-MTP GGUF p/ fitragem (desbloqueia MTP futuro); fork só após esgotar upstream |
| 7 | Flash Attention CPU | Já off; x86: off ≥ on (−4.7% Comet Lake); nosso 30/08: <2% ruído | **MANTER OFF** |
| 8 | KV q4_0/q4_0 | ΔPPL +0.06%; KGP: q4_0 > f16 E > draft-depth | **MANTER** |
| 9 | Threads/pin | auto ótimo (t36 degrada 2.8×); single-socket sem NUMA | **MANTER** (pin só sob ordem + crivo) |
| 10 | mlock/ulimit | ulimit 8MB bloqueia; sem swap pressure (21G livres) ganho ≈ 0 | **REJECT** |
| 11 | THP/hugepages | Modo always MAS AnonHugePages=0 no 8083 (mmap weights + allocator) | **INVESTIGAR** (tunables exigem root; ganho incerto) |
| 12 | Build/ISA | AVX2+FMA ok; sem AVX-512/AMX (teto silício R46); IQ3_XXS já +122% decode vs IQ4 | **MANTER** (teto atingido nessa via) |
| 13 | Engenharia de contexto | Prefill CPU ~40 t/s → prompt 8K ≈ 200s TTFT; reuso de prefixo ATIVO (log LCP 1.000); `cache_prompt`, `--slot-save-path` warmup, prompts menores (needle) = ganho linear TTFT sem restart | **ADOTAR progressivo (P0)** |
| 14 | think-off | Já ativo (maior alavanca TTFT, 10× — KGP) | **MANTER** |
| 15 | Batch R91 | Sweep 04/09 vigente (2048/512) | **MANTER** |
| 16 | Hybrid ngl36 | 25 t/s mas exige 12.19G VRAM = despeja os outros | **REJECT sob a restrição atual** |

## Ordem de engajamento

P0 contexto (sem restart: `cache_prompt:true` + warmup + prompts menores, medir TTFT) →
P1 A/B `ngram-simple` → P2 A/B `draft-simple` (Qwen3.5-0.8B, vocab-check + `p_min=0.75`) →
P3 download UDT-MTP p/ fitragem → resto parkado. Nenhuma mudança executada nesta pesquisa.

## URLs-rastros

- PR #22673 MTP: https://github.com/ggml-org/llama.cpp/pull/22673
- MTP GGUFs: https://huggingface.co/ggml-org/Qwen3.6-35B-A3B-MTP-GGUF · unsloth/Qwen3.6-35B-A3B-MTP-GGUF · AtomicChat/Qwen3.6-35B-A3B-UDT-MTP-GGUF
- Fork atomic: https://github.com/AtomicBot-ai/atomic-llama-cpp-turboquant
- KGP 45 configs: https://kgptalkie.com/tutorials/llm-benchmarking/qwen-3-8-27b-llama-cpp-speed-settings
- AWS-CN MTP CPU×GPU: https://aws.amazon.com/cn/blogs/china/mtp-inference-best-practices-using-llama-cpp/
- DFlash acceptance bug: https://github.com/ggml-org/llama.cpp/issues/25792
- FA regressão Vulkan: issues #27137 · KV q4 collapse: #27109 · FA ARM: #27086
- HF MoE-offload guide: https://huggingface.co/blog/Doctor-Shotgun/llamacpp-moe-offload-guide
- Prompt caching server: https://multigrid.ai/learn/llamacpp-prompt-caching · discuss #13606
- ZH: blog.gitcode.com/963c37b19c1e8d321875ad56c11c497e · borninfreedom.github.io/posts/2026/07/blog-post-6 · eogee.com/article/74 · trilium.atibm.com/share/DlyGVyjOEZ4k
- RU: habr.com/ru/articles/1042716
