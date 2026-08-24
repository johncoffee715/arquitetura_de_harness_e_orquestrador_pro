# R64 + R65 + manifesto_llm.json — canonização 2026-08-24 (tarde)

## R64 — Escada de contexto estática por vocação
Janelas são TOPOLOGIA congelada por papel: 16K Bonsai · 32K judge/qwen1.7B/ternary8b · 131–160K ornith/qwen0.8b/lfm · 262K qwen38-2b.
Scheduler dinâmico intra-modelo PROIBIDO por medida: llama.cpp fixa KV no boot; N instâncias = pesos×N (estoura MI50).
Ganho de TTFT mora na camada CONTEXTO (filtrar pré-prefill), não no serving.

## R65 — Roteamento híbrido em camadas
1. DISJUNTORES rígidos (incompensáveis): F4 tps≥100 · F1/F2/F5 GM-oficial≥60 · refutação tps≥180. Motivo F4: loop TDD multiplica latência 10× → thread starvation do loop externo.
2. SCORE elástico só dentro do elegível: w_logic*GM + w_speed*norm(tps), pesos por fase no manifesto.

## manifesto_llm.json — auditoria KV dos 9 slots (medida GGUF header)
| slot | dev | ctx | KB/tok | KV@ctx | tps | GM | bloqueado |
|---|---|---|---|---|---|---|---|
| :8083 Ornith-9B | GPU | 163840 | 52.0 | 8.12GB | 26 | 76.3 | F4 |
| :9083 Bonsai-27B | CPU | 16384 | 104.0 | 1.62GB | 15.7 | 62.2 | F4 |
| :9084 Qwen3.5-0.8B | CPU | 131072 | 19.5 | 2.44GB | 123 | — | — |
| :9085 Judge-3B | CPU | 32768 | híbrido | ~0.48GB | 139 | — | — |
| :9086 LFM2.5-230M | CPU | 128000 | híbrido | medir runtime | 228 | — | F1,F5 |
| :9087 Qwen3.8-2B | CPU | 262144 | 20.3 | 5.08GB | 155 | — | — |
| :9088 Qwen3-1.7B | CPU | 32768 | 45.5 | 1.42GB | 182.9 | — | — |
| :9089 Ternary-1.7B | CPU | 8192 | 45.5 | 0.36GB | 207 | — | F5 |
| :9090 Ternary-8B | CPU | 4096 | 58.5 | 0.23GB | 44.5 | — | F4 |

## EXPERIMENTO A/B FECHADO — K=q4_0+V=q4_0 @262144
Hipótese: dobrar janela com KV duplo-q4. Resultado: prefill **81 t/s** (replica 82 de 23/08) · decode **1.7 t/s** (colapso 15×) · VRAM ok mas inutilizável.
VEREDITO: REPROVADO — quantizar K no Vulkan quebra kernel FA otimizado. Rollback executado. Registro duplo datado na linha 103 do launcher.

## RETIFICAÇÃO R60-v2 — ctx Ornith fixado
KV@262K=13.95GB+pesos 5.24GB=OOM na MI50 → **ctx efetivo fixado 163840** (teto físico seguro, ~14.6-15.2GiB total). Propagado em: launcher, ctx-catalog.json, llama_budget.py, monolito, compacto, manifesto.

## Decisão orquestrador (Ornith vs Qwen3.8-27B)
Ornith PERMANECE Gran-Mestre (GM-local 76.3, prefill 770 t/s, harness-trained). Qwen3.8-27B IQ2_XXS = PLANNER WARM F1/F2/F5 via hot-swap (GPQA community 89.2 · TB 73.0 · DeepSWE 42.2; bloqueios medidos: cache-reuse disabled, prefill 86K≈9min). Reversão se qwen27b ≥76 no re-run GMB.

Tags: R60-v2, R64, R65, manifesto, auditoria-kv, experimento-kq4, decisao-orquestrador

## R60-v3 (FINAL 24/08 noite) — teto empiricamente validado
Sintoma: slot :8083 preso is_processing eterno com QUALQUER request @163840 (restart não resolve).
Causa: compute buffers dinâmicos do prefill estouram headroom Vulkan — a matemática estática de KV+pesos ignora esse buffer.
Teste controlado: rollback para -c 131072 → resposta em **0.4s, decode 71.3 t/s**, zero slots presos.
**FIXADO: 131072 = MAX VALIDADO** em launcher + ctx-catalog.json + llama_budget.py + manifesto.
Lição R62 reforçada: buffer dinâmico existe; teoria KV+pesos sem margem de compute = OOM escondido.
Achado ambiental: RAM 29/31GB + swap 16GB usado (pressão dos 8 slots CPU + desktop) — monitorar via llm-usage@.
Vídeo apoio Ornith: yt CSzffKuzUaI (ViktorKav) "a IA de 6GB que enfim termina o trabalho".
