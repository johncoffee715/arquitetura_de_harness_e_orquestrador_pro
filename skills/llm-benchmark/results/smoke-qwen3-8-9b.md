# Smoke Tests (TIER A) — qwen3-8-9b
**Data:** 2026-08-21 07:36:54 | **Endpoint:** http://127.0.0.1:9095

| Teste | Pass | TPS | Duração | Notas |
|-------|:----:|:---:|:-------:|-------|
| A1_Pelican_SVG | ❌ | 74.64 | 13.72s | svg_valid=False; pelican=True; bike=True |
| A2_Strawberry | ✅ | 70.41 | 4.84s | count_3=True; reasoning=True |
| A3_JSON_Extract | ✅ | 58.49 | 1.59s | parseable=True; values_correct=True; markdown_fence=False |
| A4_Tool_Call | ✅ | 44.31 | 1.15s | tool_call_count=1; json_valid=True; name_args_ok=True |
| A5_Halluc_Guard | ❌ | 68.78 | 3.72s | admits_no_access=False; invented_number=False |

**Total: 3/5**

**Veredito: ⚠️ PARCIAL — investigar testes falhos (quant/template/tool parser)**