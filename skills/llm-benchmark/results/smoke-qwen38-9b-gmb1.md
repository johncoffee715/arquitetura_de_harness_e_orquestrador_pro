# Smoke Tests (TIER A) — qwen38-9b-gmb1
**Data:** 2026-08-23 16:43:01 | **Endpoint:** http://127.0.0.1:8083

| Teste | Pass | TPS | Duração | Notas |
|-------|:----:|:---:|:-------:|-------|
| A1_Pelican_SVG | ❌ | 66.37 | 15.43s | svg_valid=False; pelican=False; bike=False |
| A2_Strawberry | ✅ | 65.84 | 5.35s | count_3=True; reasoning=True |
| A3_JSON_Extract | ✅ | 53.9 | 1.73s | parseable=True; values_correct=True; markdown_fence=False |
| A4_Tool_Call | ✅ | 41.98 | 1.21s | tool_call_count=1; json_valid=True; name_args_ok=True |
| A5_Halluc_Guard | ❌ | 63.86 | 4.01s | admits_no_access=False; invented_number=False |

**Total: 3/5**

**Veredito: ⚠️ PARCIAL — investigar testes falhos (quant/template/tool parser)**