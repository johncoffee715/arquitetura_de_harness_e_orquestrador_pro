---
data: 2026-09-16
hardware: MI50 16GB + Xeon E5-2699v3
tipo: duelo GM-parity (config canônica do 8083 aplicada aos rivais)
---

# 2026-09-16 — Duelo GM-Parity: rivais vs incumbent (crivo + t/s GPU)

> Método: cada modelo SOZINHO na GPU (sem contaminação), config GM-parity idêntica
> (`-c 262144 -np 1 -b 4096 -ub 1024 -ngl 36 -dev Vulkan0 --flash-attn on
> --cache-type-k q4_0 --cache-type-v q4_0 --jinja --chat-template-kwargs
> {"enable_thinking":false} --prio 2`), sonda 80 tokens temp 0, mediana de 3.

## Pódio final

| Modelo | Crivo B (/7) | decode t/s | prefill t/s | Veredito |
|---|---|---|---|---|
| **Ornith-1.5-35B-A3B-IQ2_XXS** (2.33bpw) | 6.0 | **22.7** 🥇 | 29.1 | vence t/s (+34% vs GM); crivo −0.2 |
| **Qwen3.5-35B-A3B-APEX-Mini** (3bpw) | **6.3** 🥇 | 17.7 | 23.9 | vence crivo (+0.1) E t/s (+5%) |
| 8083 incumbent (UD-IQ3_XXS ~2.9bpw) | 6.2 | 16.9 | 22.5 | referência |

## Descobertas de método (importantes)

1. **Contaminação por co-residência**: medir 2 modelos grandes na mesma GPU = ambos caem
   (8083+APEX juntos: 4.6-8.0 t/s vs 16.9-17.7 sozinhos). Duelo SÓ um-por-vez.
2. **Config GM não é universal**: `--prio 2`/`-b 4096`/`--flash-attn on` ajudaram o 8083
   (7.3→10.8→16.9 com GPU quieta) mas a variação entre modelos é dominada pela condição
   de GPU (clocks/contention), não pelas flags. APEX: 17.7 em qualquer combinação de flags.
3. **O 26.5 t/s histórico do 8083** era condição "stack completa + GPU ociosa" — não
   reproduzível em duelo isolado (16.9). Comparações devem ser sempre back-to-back.

## Implicação estratégica

- **APEX-Mini é o único rival que vence o incumbent nos DOIS eixos** (crivo 6.3>6.2, t/s 17.7>16.9).
  Candidato formal à coroa — decisão de troca é do user (R39: 8083 intocável sem ordem).
- **Ornith-35B-IQ2_XXS** = opção de velocidade pura (+34% t/s) com crivo quase-igual (6.0).
- Ambos exigem GPU dedicada (CPU: 3.4-4.0 t/s = inútil). VRAM: um por vez (13.2/10.3GB).

## Adendo — modo híbrido MoE (ngl99 GPU atenção + `--cpu-moe` experts na RAM, KV q4)

Teste pedido pelo user: simular o setup do GM (pesos RAM / experts VRAM / KV q4).

| Modelo | dec híbrido | pre híbrido | vs CPU puro | Δ |
|---|---|---|---|---|
| Ornith-35B-IQ2_XXS | **11.9** | 8.0 | 3.4/~1 | **+3.5x dec — híbrido COMPENSA** |
| APEX-Mini | 2.3 | 1.1 | 4.0/2.3 (era) | **piora** — arquitetura não lava (Dense-ish finetune?) |

Regra derivada: `--cpu-moe` (+ngl99) só ajuda quando o modelo é MoE roteável real (Ornith/Qwen-MoE). Em builds densos custom (APEX) penaliza. Sempre medir antes de canonizar o modo.

Pós-estado: stack GM restaurada no slot 8083 (`srv-gm-full`), 8090 liberada.
