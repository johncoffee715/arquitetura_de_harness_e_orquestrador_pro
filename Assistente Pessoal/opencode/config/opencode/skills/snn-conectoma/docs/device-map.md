---
name: snn-conectoma-device-map
description: "Device-map validado dos slots LLM para pinagem de threads SNN (taskset). Resolve a divergência flagada no CONTEXT.md entre manifesto stack_atual.gpu (stale) e start-stack.sh (fonte de física canônica)."
mode: doc
tags: "snn, device-map, taskset, cpu, gpu, slots"
origin: validado:snn-hefesto-absorb
metadata:
  category: doc
  version: 1.0.0
  date: 2026-09-13
  author: Hefesto (dispatcher snn-hefesto-absorb)
---

# Device-Map Validado — Slots LLM (para pinagem SNN)

## Método de validação

- **Fonte de física canônica**: `opencode/scripts/start-stack.sh` (flags `-ngl` / `-dev`).
- **Confirmação por processo vivo**: `/proc/<pid>/cmdline` de cada `llama-server`.
- **Health check HTTP**: `http://127.0.0.1:<port>/health`.

## Resultado (evidência real coletada 2026-09-13)

| Porta | Modelo | Papel | ngl | Device REAL |
|---|---|---|---|---|
| 8083 | Qwen3.5-35B | orquestrador | 36 | híbrido GPU/CPU |
| 9084 | RWKV7-0.4B | talamus-cortex | 999 | GPU Vulkan |
| **9086** | LFM-1.2B | reflexo | **0** | **CPU** |
| 9088 | Llama-1B | contrato-plano | 999 | GPU Vulkan |
| **9090** | Llama-3B | refutação | **0** | **CPU** |
| **9092** | SmolLM-1.7B | relay | **0** | **CPU** |

Health HTTP: 8083/9084/9086/9088/9090/9092/9093/9094/9095/9097 → 200.
Needle (8097/9091) → 404 em `/health` (binário nativo, usa `/complete`, não llama-server).

## Resolução da divergência

- CONTEXT.md flagava: manifesto `stack_atual.gpu` lista 9086/9090/9092 em VRAM,
  mas manifesto do usuário aloca em CPU.
- **Veredito**: `start-stack.sh` + `/proc` cmdline confirmam `-ngl 0` (CPU puro) para
  9086/9090/9092. A string `stack_atual.gpu` no manifesto está **stale** — não usar como
  fonte de pinagem.

## Pinagem recomendada (taskset) para threads SNN

- Slots CPU confirmados: **9086 / 9090 / 9092** (+8083 parcial, mas é orquestrador — evitar).
- NÃO pinar em 9088/9084/9093 (GPU ngl999 — não são CPU).
- Exemplo (ilustrativo, adaptar núcleos reais):
  `taskset -c 0-3 <binario-snn>` (núcleos livres, fora dos threads dos slots CPU acima).

## Evidência bruta (cmdline)

```
port 8083 → -ngl 36 -dev Vulkan0
port 9084 → -ngl 999 -dev Vulkan0
port 9086 → -ngl 0        (CPU)
port 9088 → -ngl 999 -dev Vulkan0
port 9090 → -ngl 0        (CPU)
port 9092 → -ngl 0        (CPU)
```