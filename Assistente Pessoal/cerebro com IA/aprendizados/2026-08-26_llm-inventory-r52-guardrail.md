---
tags: [R52, inventario, llm-inventory, guardrail, amalgama]
date: 2026-08-26
---

# R52 — Inventário Global de LLMs Locais + Amálgama LLM×Feature (Regra Global Guardrail)

## Resumo
Regra global criada sob pedido do usuário: inventário único com categoria/setor por LLM local,
alimentado automaticamente após registro (header GGUF + slot + papel), lacunas de benchmark
preenchidas via MIX multi-idioma (EN/PT/ZH/JA/KO/DE/RU/IT, ≥2 rodadas) ou benchmark empírico local.
Uso obrigatório: `llm-inventory.py --resolve <feature>` antes de escolher LLM para task/feature,
cruzando com R13/R23/R47/R46.

## Artefatos
- config/opencode/AGENTS.md §R52 (constituição)
- config/opencode/harness/llm-inventory.json (fonte de verdade, 9 modelos)
- config/opencode/harness/INVENTARIO.md (doutrina)
- config/opencode/scripts/llm-inventory.py (motor: --all/--resolve/--probe/--show/--register/--validate)

## Descobertas MIX (fonte: pesquisa multi-idioma 2026-08-26)
- Ornith-1.5-9B: modelo real (ornith.ai, base Qwen3.5-9B + RL); GPQA-D 86.4, SWE-bench 70.6, MCP-Atlas 54.2.
- Qwen3.5-4B: MMLU-Pro 79.1, GPQA-D 76.2, IFEval 89.8, TAU2 79.9, BFCL-V4 50.3; IQ2_XXS sem bench público (UNKNOWN → evitar tool estrito).
- Qwen3.5-0.8B: multimodal nativa, 262k; BFCL 25.3 fraco; thinking loops documentado.
- Qwen3.8-2B/4B/9B: NÃO oficiais — distillas comunitárias sem bench (UNKNOWN); oficial é só 27B (GPQA 89.2, LiveCodeBench 90.3).
- Qwen2.5-3B (LLMJudge): MMLU 65.6, IFEval 58.2, HumanEval 74.4; BFCL 3B não publicado.
- LFM2.5-230M: IFEval 71.71, BFCLv3 43.26; oficial: não p/ math/código/criativa; n_ctx_train 32768 (GGUF lê 128000 — divergência).
- Ternary-Bonsai-8B: Qwen3-8B ternário 1.58-bit, avg 75.5 vs 79.3; IFEval 81.8, BFCL 73.9; MMLU-R -10.4.

## Lição-chave
Benchmark público + status CONFIRMED/INFERRED/UNKNOWN + empiria local é a tríade anti-alucinação
de escolha LLM. Distillas comunitárias (Qwen3.8-*) não podem ser citadas por benchmark nominal.
