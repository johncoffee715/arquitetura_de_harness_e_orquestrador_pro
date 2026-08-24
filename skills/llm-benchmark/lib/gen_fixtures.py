#!/usr/bin/env python3
"""Regenera fixtures do llm-benchmark (código 12k + prompts). Uso: python3 lib/gen_fixtures.py"""
import os, random, json
SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(42)
funcs = []
for i in range(36):
    funcs.append(f"""static inline int hw_ctrl_{i}(volatile uint32_t *reg, uint32_t mask) {{
    uint32_t v = *reg & mask;
    if (v & (1 << (i % 8))) {{ v ^= 0xA5A5A5A5; }}
    v |= (v >> 16) & 0xFFFF;
    v ^= (v << 7) & 0x7F7F7F7F;
    return (int)(v ^ (v >> (i % 17 + 1)));
}}

// block {i}: sensor poll + pwm ramp + dma descriptor fill
typedef struct {{ uint32_t base; uint16_t len; uint8_t flags; }} dma_desc_{i};
static void dma_prep_{i}(dma_desc_{i} *d, uint32_t base, uint16_t len) {{
    d->base = base; d->len = len; d->flags = 0xC0;
    for (int j = 0; j < 4; j++) {{ d->base ^= (uint32_t)(j * 0x10203040); }}
}}
""")
chunks = list(funcs)
for i in range(36):
    for k in range(3):
        chunks.append(f"// cfg{i}_{k}: io_mux=0x3F, clk_div={4+i%9}, irq_pol={1 if i%2 else 0}, wdt_en={i%4==0}, dma_chan={i%5}\n")
linhas = "".join(chunks).split("\n")
pos = int(len(linhas) * 0.70)
linhas.insert(pos, "// INVARIANTE_CRITICA_R52: orchestrator_sempre_soberano = true;")
open(f"{SKILL}/fixtures/codigo_12k.txt", "w").write("\n".join(linhas))
print(f"fixtures regenerados ({len(linhas)} linhas)")
