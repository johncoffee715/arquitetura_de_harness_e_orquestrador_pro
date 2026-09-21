---
data: 2026-09-17
tipo: aprendizado (lição empírica)
---

# Lição: serving subótimo falsifica benchmark de CPU (GM MoE)

**A lição**: o "CPU puro 3.4 t/s" medido no Ornith-IQ2_XXS era **artefato de serving subótimo**
(o runner usava `-t 18` e nenhum knob). Com os MESMOS knobs que o Qwen-35B usa
(`-b 4096 -ub 1024 --flash-attn on --prio 2 --mlock -t 36`), o Ornith-IQ2_XXS faz
**44.5 t/s decode / 103.4 t/s prefill em CPU** — 13x mais rápido.

## Regra derivada (R-régua de benchmark)

1. **Todo benchmark de LLM deve usar a config de serving canônica do papel** — nunca o default
   do runner. `-t 18` sem knobs = medição de artefato, não do modelo.
2. **Knobs que importam em CPU (Xeon E5-2699v3, 36 threads)**:
   - `-t 36 -tb 36` (threads nativos, não 18)
   - `-b 4096 -ub 1024` (batch grande)
   - `--flash-attn on` (obrigatório com KV q4_0/q4_0)
   - `--prio 2` (prioridade alta)
   - `--mlock` (modelo preso na RAM, sem page-out)
   - `--cache-type-k q4_0 --cache-type-v q4_0` (KV compacto)
3. **Referência de serving GM MoE** (config canônica para Qwen-35B-A3B, Ornith-35B-A3B e
   futuros MoE que passarem pelo crivo; **LLM denso precisa ser testado para identificar se
   também é apto a otimizações similares** — a régua não assume transferência automática
   MoE→denso):
   ```bash
   llama-server -m <MODELO> -c 65536 -np 1 -t 36 -tb 36 \
     --flash-attn on --cache-type-k q4_0 --cache-type-v q4_0 \
     -b 4096 -ub 1024 --jinja --prio 2 --mlock
   ```
4. **full-GPU (ngl 99) segue campeão** quando VRAM permite (79.4 dec no Ornith) — mas
   CPU-knobs é o melhor sem VRAM dedicada (44.5 dec).

## Evidência
- Ornith-IQ2_XXS CPU-knobs: dec 44.5 (300 tok) / pre 103.4 — medido 2026-09-17 ~16:15
- Ornith-IQ2_XXS "CPU puro" (runner -t18): dec 3.4 — artefato, descartado
- Ornith-IQ2_XXS full-GPU ngl99: dec 79.4 / pre 46.8 — campeão absoluto

## Ação
- Config canônica registrada como referência de serving GM MoE (skills/gran-mestre + este vault).
- Próximo: testar MTP/DFlash da família CERTA (não Abliterated) para fechar o crivo.