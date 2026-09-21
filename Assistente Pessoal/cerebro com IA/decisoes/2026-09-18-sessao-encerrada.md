---
data: 2026-09-18
tipo: sessao-encerrada (Gari R99)
---

# Sessão encerrada — 2026-09-18 (Gari)

## Pérolas quantitativas
- Ornith-1.5-35B-A3B-IQ2_XXS coroado GM: **dec 81.0 / pre 123.8 t/s** (CPU-knobs b4096/fa/prio/mlock/t36), crivo B=6.0, peso 9.55G
- CPU-knobs = **13x** sobre serving subótimo (3.4 → 44.5 t/s em CPU puro; 81.0 com GPU)
- Piso-absorção R104 ≈ **2.3bpw** (IQ2_XS passa, IQ2_S 2.17 falha) — 27B e 35B confirmaram
- Qwen3.5-35B-IQ3_XXS: 26.5 t/s → substituído (3x mais lento que Ornith)
- gemma-4-26B: A=4.6/B=5.2 — descartado (abaixo da barra B≥5.7)
- Bonsai-2-27B-PTQ1_0 (ternário 1-bit, 5.95G) — aguardando crivo R104

## Pérolas qualitativas
- R103 (régua justa A/B) + R104 (criva do piso) canonizados no vault
- MTP/DFlash: bloqueados por build (ggml_abort/mismatch) — não decisivos
- Lição: serving subótimo falsifica benchmark de CPU (`-t 18` sem knobs = artefato)
- Hefesto absorveu jev-eval + vepforge (skills com quarteto)
- ctx da sessão corrigido: orchestrator 65536 → 262144 (casa com Ornith nativo)
- opencode atualizado: 1.18.29 → **1.18.31**
- CIVITAI_API_KEY configurada e validada (MCP civitai-orchestration respondeu)

## Divergência registrada (esperada)
- `sync-llm-stack.py --check`: opencode.jsonc diverge do manifesto — CAUSA: mudança de ctx 262k (intencional, documentada)

## Estado
- GM :8083 = Ornith ✓ · Modo autônomo OFF ✓ · Units falhadas 0 ✓ · Disco 39G ✓