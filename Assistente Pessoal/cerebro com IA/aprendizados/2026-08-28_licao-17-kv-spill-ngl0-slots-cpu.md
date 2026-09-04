# Lição #17 — KV-spill por falta de `-ngl 0` em slots CPU

**Data:** 2026-08-28
**Regras:** R62 / R21 / R27 / R71
**Origem:** auditoria de lentidão do orquestrador + stack caindo sozinha

## Sintoma
- Ornith (:8083) decodava a **0.93 t/s** (baseline R63: 26 t/s)
- Stack derrubava sozinha (crash_anomalo_pos_prefill)
- VRAM 99% cheia (16.99/17.16 GiB) com "No KFD PIDs"

## Causa raiz
Slots "CPU" (9083–9090) **sem `-ngl 0`**: o llama.cpp com Vulkan detectado alocava **pesos + KV cache na MI50** mesmo para modelos CPU-only. Resultado: ~20GB de VRAM consumidos pelos 8 slots CPU → Ornith sem VRAM → **KV-spill para RAM do host** → decode colapsa.

## Evidência
| Métrica | Antes | Depois |
|---------|-------|--------|
| VRAM usada | 16.99 GiB | 12.3 GiB |
| Decode Ornith | 0.93 t/s | **57.62 t/s** (62×) |
| Clocks | mclk 350MHz | mclk 350MHz (DPM automático — NÃO era low-power) |

## Fix
1. `-ngl 0` em TODOS os slots CPU do `start-stack.sh`
2. Parsing rocm-smi corrigido: `grep -oP '\d+$'` (não `\d+` que pega o `0` de `GPU[0]`)
3. Ctx dinâmico do Ornith: KV q4/q4 ≈ **11KB/tok empírico** → 9.10GB VRAM = **258432** (n_ctx_train 262144)
4. `sync-llm-stack.py --apply` regenerou os 5 pontos de verdade (R27)

## Lição
> Todo slot CPU em stack híbrida com GPU Vulkan DEVE ter `-ngl 0` explícito — sem isso o llama.cpp offloada pesos+KV para VRAM e estrangula o slot GPU. Sintoma clássico: orquestrador lento + VRAM 99% + stack caindo sozinha.

## Contextos finais da stack (pós-fix)
| Slot | Modelo | Ctx | t/s |
|------|--------|-----|-----|
| :8083 | ornith-1.5-9b-q5 (GPU) | 258560 | 57.62 |
| :9083 | qwen3.5-4b-iq2xxs | 32768 | CPU |
| :9084 | rwkv7-0.4b (Córtex R71) | 1048576 | CPU |
| :9085 | llmjudge-qwen2.5-3b | 32768 | CPU |
| :9086 | lfm2.5-1.2b-thinking-tomoe | 32768 | CPU |
| :9087 | granite-4.2-3b-q4_k_m | 65536 | CPU |
| :9088 | qwen3.8-4b-distill | 65536 | CPU |
| :9089 | qwen3.8-2b-distill | 65536 | CPU |
| :9090 | ternary-bonsai-8b | 65536 | CPU |